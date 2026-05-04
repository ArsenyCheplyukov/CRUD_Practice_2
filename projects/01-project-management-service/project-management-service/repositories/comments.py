from models.comments import Comment
from models.tasks import Task
from schemas.comments import CommentCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        comments = await self.session.execute(select(Comment))
        return comments.scalars().all()

    async def get_by_id(self, comment_id: int):
        comment = await self.session.execute(
            select(Comment).where(Comment.id == comment_id)
        )
        return comment.scalar_one_or_none()

    async def get_task_comments(self, task_id: int):
        comments = await self.session.execute(
            select(Comment).where(Comment.task_id == task_id)
        )
        return comments.scalars().all()

    async def get_user_comments(self, user_id: int):
        comments = await self.session.execute(
            select(Comment).where(Comment.author_id == user_id)
        )
        return comments.scalars().all()

    async def get_project_comments(self, project_id: int):
        comments = await self.session.execute(
            select(Comment).join(Comment.task).where(Task.project_id == project_id)
        )
        return comments.scalars().all()

    async def get_task_user_comments(self, task_id: int, user_id: int):
        comments = await self.session.execute(
            select(Comment).where(
                Comment.task_id == task_id and Comment.author_id == user_id
            )
        )
        return comments.scalars().all()

    async def get_project_user_comments(self, project_id: int, user_id: int):
        comments = await self.session.execute(
            select(Comment)
            .join(Comment.task)
            .where(Task.project_id == project_id)
            .where(Comment.author_id == user_id)
        )
        return comments.scalars().all()

    async def create(self, comment: CommentCreate) -> Comment:
        self.session.add(comment)
        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def delete(self, comment_id: int) -> Comment:
        comment = await self.get_by_id(comment_id)
        self.session.delete(comment)
        return comment
