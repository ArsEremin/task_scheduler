from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.tasks.models import Task, Comment


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[Base.utc_datetime]

    created_tasks: Mapped[list[Task]] = relationship(back_populates="creator", foreign_keys=Task.created_by)
    assigned_tasks: Mapped[list[Task]] = relationship(back_populates="assignee", foreign_keys=Task.assignee_id)
    comments: Mapped[list[Comment]] = relationship(back_populates="author")
