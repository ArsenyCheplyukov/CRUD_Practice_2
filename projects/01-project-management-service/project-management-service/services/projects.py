from exceptions import (
    CommentNotFound,
    ProjectNotCreated,
    ProjectNotDeleted,
    ProjectNotFound,
    ProjectNotUpdated,
    TaskNotFound,
    UserNotFound,
)
from models.projects import Project
from repositories import (
    CommentRepository,
    ProjectRepository,
    TaskRepository,
    UserRepository,
)
from schemas.projects import ProjectCreate, ProjectUpdate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class ProjectService:
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
        return await self.project_repository.get_all()

    async def get_by_id(self, project_id: int):
        return await self.project_repository.get_by_id(project_id)

    async def get_user_projects(self, user_id: int):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        return await self.project_repository.get_user_projects(user_id)

    async def get_task_project(self, task_id: int):
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound()
        return await self.project_repository.get_task_project(task_id)

    async def get_comment_project(self, comment_id: int):
        comment = await self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise CommentNotFound()
        return await self.project_repository.get_comment_project(comment_id)

    async def create(
        self,
        project_data: ProjectCreate,
    ):
        # Check if user exist
        project = await self.project_repository.get_by_id(project_data.owner_id)
        if project:
            raise UserNotFound()
        # Check if project exist
        try:
            project = Project(**project_data.model_dump())
            return await self.project_repository.create(project)
        except IntegrityError:
            raise ProjectNotCreated()

    async def update(
        self,
        project_id: int,
        project_data: ProjectUpdate,
    ):
        # Check if project exist
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFound()
        # Check if user exist
        user = await self.user_repository.get_by_id(project_data.owner_id)
        if not user:
            raise UserNotFound()
        # Update project
        try:
            # refill project with new data
            for key, value in project_data.model_dump(exclude_unset=True).items():
                setattr(project, key, value)
            project = await self.project_repository.create(project_data)
        except IntegrityError:
            raise ProjectNotUpdated()
        return project

    async def delete(self, project_id: int):
        # Check if project exist

        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFound()
        # Delete project
        try:
            project = await self.project_repository.delete(project_id)
        except IntegrityError:
            raise ProjectNotDeleted()
        return project
