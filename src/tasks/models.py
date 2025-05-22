from datetime import datetime, timezone
from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class TaskStatus(StrEnum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class TaskPriority(StrEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    status: Mapped[TaskStatus]
    priority: Mapped[TaskPriority]
    assignee_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    created_at: Mapped[Base.utc_datetime]
    updated_at: Mapped[Base.utc_datetime] = mapped_column(onupdate=datetime.now(timezone.utc))
    due_date: Mapped[datetime]

    creator: Mapped["User"] = relationship(back_populates="created_tasks", foreign_keys=created_by)
    assignee: Mapped["User"] = relationship(back_populates="assigned_tasks", foreign_keys=assignee_id)
    comments: Mapped[list["Comment"]] = relationship(back_populates="task")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[Base.utc_datetime]
    updated_at: Mapped[Base.utc_datetime] = mapped_column(onupdate=datetime.now(timezone.utc))

    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    task: Mapped[Task] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")