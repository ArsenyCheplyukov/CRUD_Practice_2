from exceptions import (
    CommentNotFound,
    ProjectNotFound,
    TaskNotCreated,
    TaskNotDeleted,
    TaskNotFound,
    TaskNotUpdated,
    UserNotFound,
)
from models.tasks import Task
from repositories import (
    CommentRepository,
    ProjectRepository,
    TaskRepository,
    UserRepository,
)
from schemas.tasks import TaskCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class TaskService:
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
        return await self.task_repository.get_all()

    async def get_by_id(self, task_id: int):
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound()
        return task

    async def get_by_id_with_project(self, task_id: int):
        task = await self.task_repository.get_by_id_with_project(task_id)
        if not task:
            raise TaskNotFound()
        return task

    async def get_project_tasks(self, project_id: int):
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFound()
        return await self.task_repository.get_project_tasks(project_id)

    async def get_user_tasks(self, user_id: int):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        return await self.task_repository.get_user_tasks(user_id)

    async def get_comment_task(self, comment_id: int):
        comment = await self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise CommentNotFound()
        return await self.task_repository.get_comment_task(comment_id)

    async def create(self, task_data: TaskCreate):
        # Check if project exist, if not - raise exception
        project = await self.project_repository.get_by_id(task_data.project_id)
        if not project:
            raise ProjectNotFound()
        # Check if user exist, if not - raise exception
        user = await self.user_repository.get_by_id(task_data.assignee_id)
        if not user:
            raise UserNotFound()
        # Create task
        try:
            task = Task(**task_data.model_dump())
            return await self.task_repository.create(task)
        except IntegrityError:
            raise TaskNotCreated()

    async def update(self, task_id: int, task_data: TaskCreate):
        # Check if task exist, if not - raise exception
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound()
        # Check if user exist, if not - raise exception
        user = self.user_repository.get_by_id(task_data.assignee_id)
        if not user:
            raise UserNotFound()
        # Check if project exist, if not - raise exception
        project = await self.project_repository.get_by_id(task_data.project_id)
        if not project:
            raise ProjectNotFound()
        # Update task
        try:
            # refill task with new data
            for key, value in task_data.model_dump(exclude_unset=True).items():
                setattr(task, key, value)
            return await self.task_repository.create(task)
        except IntegrityError:
            raise TaskNotUpdated()

    async def delete(self, task_id: int):
        # Check if task exist, if not - raise exception
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound()
        # Delete task
        try:
            return await self.task_repository.delete(task_id)
        except IntegrityError:
            raise TaskNotDeleted()
