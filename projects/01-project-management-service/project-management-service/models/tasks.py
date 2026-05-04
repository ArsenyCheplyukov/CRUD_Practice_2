from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from models import Comment, Project, User


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[str] = mapped_column(default="todo")
    priority: Mapped[int | None]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="tasks")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="task")
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}, status={self.status}, priority={self.priority}, project_id={self.project_id}, assignee_id={self.assignee_id})"
