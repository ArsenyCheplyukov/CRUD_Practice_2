from models.projects import Project
from models.users import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):

        users = await self.session.execute(select(User))
        return users.scalars().all()

    async def get_by_id(self, user_id: int):
        user = await self.session.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()

    async def get_by_id_with_projects_and_tasks(self, user_id: int):
        user = await self.session.execute(
            select(User)
            .options(selectinload(User.projects).selectinload(Project.tasks))
            .where(User.id == user_id)
        )
        return user.scalar_one_or_none()

    async def get_by_email(self, email: str):
        user = await self.session.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()

    async def get_project_users(self, project_id: int):
        users = await self.session.execute(
            select(User).join(User.projects).where(User.projects.id == project_id)
        )
        return users.scalars().all()

    async def get_task_users(self, task_id: int):
        users = await self.session.execute(
            select(User).join(User.tasks).where(User.tasks.id == task_id)
        )
        return users.scalars().all()

    async def get_comment_user(self, comment_id: int):
        user = await self.session.execute(
            select(User).join(User.comments).where(User.comments.id == comment_id)
        )
        return user.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> User:
        user = await self.get_by_id(user_id)
        self.session.delete(user)
        return user
