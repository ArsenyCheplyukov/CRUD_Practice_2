from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from schemas.projects import ProjectRead


class TaskRead(BaseModel):
    id: int
    title: Annotated[str, Field()]
    description: Annotated[str, Field()]
    status: Annotated[str, Field()]
    priority: Annotated[int | None, Field()]
    project_id: Annotated[int, Field()]
    assignee_id: Annotated[int | None, Field()]
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class TaskReadWithProject(TaskRead):
    project: Annotated[ProjectRead, Field()]


class TaskCreate(BaseModel):
    title: Annotated[str, Field()]
    description: Annotated[str, Field()]
    status: Annotated[str, Field()]
    priority: Annotated[int | None, Field()]
    project_id: Annotated[int, Field()]
    assignee_id: Annotated[int | None, Field()]


class TaskUpdate(BaseModel):
    title: Annotated[str | None, Field()]
    description: Annotated[str | None, Field()]
    status: Annotated[str | None, Field()]
    priority: Annotated[int | None, Field()]
    project_id: Annotated[int | None, Field()]
    assignee_id: Annotated[int | None, Field()]


class TaskDelete(BaseModel):
    id: Annotated[int, Field()]
    title: Annotated[str, Field()]
