from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.tasks.models import Task


class TaskService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_task_by_id(self, task_id: int):
        query = select(Task).filter_by(id=task_id)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def get_tasks_by_filters(self, **filters):
        query = select(Task).filter_by(**filters)
        res = await self._session.execute(query)
        return res.scalars().all()

    async def add_task(self, task_data: dict):
        task = Task(**task_data)
        self._session.add(task)
        await self._session.commit()
        return task

    async def update_task(self, task, new_task_status):
        task.status = new_task_status
        await self._session.commit()


async def get_task_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> TaskService:
    return TaskService(session)
