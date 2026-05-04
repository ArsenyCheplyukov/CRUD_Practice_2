from exceptions import (
    CommentNotCreated,
    CommentNotDeleted,
    CommentNotFound,
    CommentNotUpdated,
    ProjectNotFound,
    TaskNotFound,
    UserNotFound,
)
from models.comments import Comment
from repositories import (
    CommentRepository,
    ProjectRepository,
    TaskRepository,
    UserRepository,
)
from schemas.comments import CommentCreate, CommentUpdate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class CommentService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.user_repository = UserRepository(session)
        self.task_repository = TaskRepository(session)
        self.project_repository = ProjectRepository(session)
        self.comment_repository = CommentRepository(session)

    async def get_all(self):
        return await self.comment_repository.get_all()

    async def get_by_id(self, comment_id: int):

        return await self.comment_repository.get_by_id(comment_id)

    async def get_task_comments(self, task_id: int):
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound()
        return await self.comment_repository.get_task_comments(task_id)

    async def get_user_comments(self, user_id: int):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        return await self.comment_repository.get_user_comments(user_id)

    async def get_project_comments(self, project_id: int):
        # Check if project exist
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFound()
        # Check if comments found
        return await self.comment_repository.get_project_comments(project_id)

    async def get_task_user_comments(
        self,
        task_id: int,
        user_id: int,
    ):
        # Check if task exist
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound()
        # Check if user exist
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        # Check if comments found
        return await self.comment_repository.get_task_user_comments(task_id, user_id)

    async def get_project_user_comments(
        self,
        project_id: int,
        user_id: int,
    ):
        # Check if project exist
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFound()
        # Check if user exist
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        # Check if comments found
        return await self.comment_repository.get_project_user_comments(
            project_id, user_id
        )

    async def create(
        self,
        comment_data: CommentCreate,
    ):
        # Check if user exist
        user = await self.user_repository.get_by_id(comment_data.author_id)
        if not user:
            raise UserNotFound()
        # Check if task exist
        task = await self.task_repository.get_by_id(comment_data.task_id)
        if not task:
            raise TaskNotFound()
        # Create comment
        try:
            comment = Comment(**comment_data.model_dump())
            created_data = await self.comment_repository.create(comment)
        except IntegrityError:
            raise CommentNotCreated()
        return created_data

    async def update(
        self,
        comment_id: int,
        comment_data: CommentUpdate,
    ):
        # Check if comment exist
        comment = await self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise CommentNotFound()
        # Check if user exist
        user = await self.user_repository.get_by_id(comment_data.author_id)
        if not user:
            raise UserNotFound()
        # Check if task exist
        task = await self.task_repository.get_by_id(comment_data.task_id)
        if not task:
            raise TaskNotFound()
        # Update comment
        try:
            # refill comment with new data
            for key, value in comment_data.model_dump(exclude_unset=True).items():
                setattr(comment, key, value)
            updated_comment = await self.comment_repository.create(comment)
        except IntegrityError:
            raise CommentNotUpdated()
        return updated_comment

    async def delete(
        self,
        comment_id: int,
    ):
        # Check if comment exist
        comment = await self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise CommentNotFound()
        # Delete comment
        try:
            deleted_comment = await self.comment_repository.delete(comment_id)
        except IntegrityError:
            raise CommentNotDeleted()
        return deleted_comment
