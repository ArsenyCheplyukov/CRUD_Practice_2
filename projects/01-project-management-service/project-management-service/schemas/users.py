from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from schemas.projects import ProjectReadWithTasks


class UserRead(BaseModel):
    id: int
    name: Annotated[str, Field()]
    email: Annotated[str, Field()]
    is_active: Annotated[bool, Field()]
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class UserReadWithProjectsAndTasks(UserRead):
    projects: Annotated[list[ProjectReadWithTasks], Field()]


class UserCreate(BaseModel):
    name: Annotated[str, Field()]
    email: Annotated[str, Field()]
    password_hash: Annotated[str, Field()]
    is_active: Annotated[bool, Field()]


class UserUpdate(BaseModel):
    name: Annotated[str | None, Field()]
    email: Annotated[str | None, Field()]
    password_hash: Annotated[str | None, Field()]
    is_active: Annotated[bool | None, Field()]


class UserDelete(BaseModel):
    id: Annotated[int, Field()]
    name: Annotated[str, Field()]
