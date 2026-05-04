from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class CommentRead(BaseModel):
    id: int
    content: Annotated[str, Field()]
    task_id: Annotated[int, Field()]
    author_id: Annotated[int, Field()]
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: Annotated[str, Field()]
    task_id: Annotated[int, Field()]
    author_id: Annotated[int, Field()]


class CommentUpdate(BaseModel):
    content: Annotated[str | None, Field()]
    task_id: Annotated[int | None, Field()]
    author_id: Annotated[int | None, Field()]


class CommentDelete(BaseModel):
    id: Annotated[int, Field()]
    content: Annotated[str, Field()]
