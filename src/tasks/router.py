from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException

from src.tasks.enums import TaskStatus
from src.tasks.schemas import TaskFiltersSchema, TaskSchema, TaskCreationSchema
from src.tasks.service import TaskService, get_task_service
from src.users.dependencies import get_current_user
from src.users.models import User
from src.users.service import UserService, get_user_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],

)


@router.get("", dependencies=[Depends(get_current_user)])
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    filters: Annotated[TaskFiltersSchema, Query()]
) -> list[TaskSchema]:
    query_filters = {
        filter_name: val
        for filter_name, val in (("status", filters.status), ("priority", filters.priority))
        if val is not None
    }

    if filters.assignee is not None:
        assignee = await user_service.get_user_by_login(filters.assignee)
        if assignee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="assignee not found")
        query_filters["assignee_id"] = assignee.id

    return await task_service.get_tasks_by_filters(**query_filters)


@router.get("/{task_id}", dependencies=[Depends(get_current_user)])
async def get_task(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    task_id: int
) -> TaskSchema:
    return await task_service.get_task_by_id(task_id)


@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task_status(
    user: Annotated[User, Depends(get_current_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    task_id: int,
    new_task_status: TaskStatus
):
    task = await task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    if user.id != task.assignee_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")
    await task_service.update_task(task, new_task_status)
    return {"status": "ok"}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    user: Annotated[User, Depends(get_current_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    task: TaskCreationSchema
) -> TaskSchema:
    creator_id = user.id
    assignee = await user_service.get_user_by_login(task.assignee)
    if assignee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="assignee not found")

    task_data = dict(task)
    task_data.pop("assignee")
    task_data["created_by"] = creator_id
    task_data["assignee_id"] = assignee.id

    created_task = await task_service.add_task(task_data)
    return created_task
