from exceptions import (
    CommentNotFound,
    ProjectNotFound,
    TaskNotFound,
    UserAlreadyExists,
    UserNotCreated,
    UserNotDeleted,
    UserNotFound,
    UserNotUpdated,
)
from models.users import User
from repositories import (
    CommentRepository,
    ProjectRepository,
    TaskRepository,
    UserRepository,
)
from schemas.users import UserCreate, UserUpdate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
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
        return await self.user_repository.get_all()

    async def get_by_id(
        self,
        user_id: int,
    ):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        return user

    async def get_by_email(
        self,
        email: str,
    ):
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFound()
        return user

    async def get_project_users(
        self,
        project_id: int,
    ):
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFound()
        users = await self.user_repository.get_project_users(project_id)
        return users

    async def get_task_users(
        self,
        task_id: int,
    ):
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound()
        users = await self.user_repository.get_task_users(task_id)
        return users

    async def get_comment_user(
        self,
        comment_id: int,
    ):
        comment = await self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise CommentNotFound()
        user = await self.user_repository.get_comment_user(comment_id)
        if not user:
            raise UserNotFound()
        return user

    async def create(
        self,
        user_data: UserCreate,
    ):
        user = await self.user_repository.get_by_email(user_data.email)
        if user:
            raise UserAlreadyExists()
        try:
            user = User(**user_data.model_dump())
            new_user = await self.user_repository.create(user)
        except IntegrityError:
            raise UserNotCreated()
        return new_user

    async def update(
        self,
        user_id: int,
        user_data: UserUpdate,
    ):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        try:
            # refill user with new data
            for key, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            updated_user = await self.user_repository.create(user)
        except IntegrityError:
            raise UserNotUpdated()
        return updated_user

    async def delete(
        self,
        user_id: int,
    ):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        try:
            deleted_user = await self.user_repository.delete(user_id)
        except IntegrityError:
            raise UserNotDeleted()
        return deleted_user
