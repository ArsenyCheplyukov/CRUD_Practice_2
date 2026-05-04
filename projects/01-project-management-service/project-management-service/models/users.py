from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from models import Comment, Project, Task


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_active: Mapped[bool]

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, is_active={self.is_active})"
