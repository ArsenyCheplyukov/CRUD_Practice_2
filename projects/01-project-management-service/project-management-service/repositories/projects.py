from models import Comment, Project, Task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        projects = await self.session.execute(select(Project))
        return projects.scalars().all()

    async def get_by_id(self, project_id: int):
        project = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        return project.scalar_one_or_none()

    async def get_by_title(self, title: str):
        project = await self.session.execute(
            select(Project).where(Project.title == title)
        )
        return project.scalar_one_or_none()

    async def get_user_projects(self, user_id: int):
        projects = await self.session.execute(
            select(Project).where(Project.owner_id == user_id)
        )
        return projects.scalars().all()

    async def get_task_project(self, project_id: int):
        project = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        return project.scalar_one_or_none()

    async def get_comment_project(self, comment_id: int):
        project = await self.session.execute(
            select(Project)
            .join(Project.tasks)
            .join(Task.comments)
            .where(Comment.id == comment_id)
        )
        return project.scalar_one_or_none()

    async def create(self, project: Project) -> Project:
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def delete(self, project_id: int) -> Project:
        project = await self.get_by_id(project_id)
        self.session.delete(project)
        return project
