from datetime import datetime

from pydantic import BaseModel, Field

from src.tasks.enums import TaskStatus, TaskPriority


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    created_by: int
    status: TaskStatus
    priority: TaskPriority
    assignee_id: int
    created_at: datetime
    updated_at: datetime
    due_date: datetime


class TaskCreationSchema(BaseModel):
    title: str = Field(max_length=100)
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: str
    due_date: datetime


class TaskFiltersSchema(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee: str | None = None
