from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from schemas.tasks import TaskRead


class ProjectRead(BaseModel):
    id: Annotated[int, Field()]
    title: Annotated[str, Field()]
    description: Annotated[str, Field()]
    owner_id: Annotated[int, Field()]
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ProjectReadWithTasks(ProjectRead):
    tasks: Annotated[list[TaskRead], Field()]


class ProjectCreate(BaseModel):
    title: Annotated[str, Field()]
    description: Annotated[str, Field()]
    owner_id: Annotated[int, Field()]


class ProjectUpdate(BaseModel):
    title: Annotated[str | None, Field(default=None)]
    description: Annotated[str | None, Field(default=None)]
    owner_id: Annotated[int | None, Field(default=None)]


class ProjectDelete(BaseModel):
    id: Annotated[int, Field()]
    title: Annotated[str, Field()]
