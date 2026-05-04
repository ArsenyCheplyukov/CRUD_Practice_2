from models import Comment, Task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        tasks = await self.session.execute(select(Task))
        return tasks.scalars().all()

    async def get_by_id(self, task_id: int):
        task = await self.session.execute(select(Task).where(Task.id == task_id))
        return task.scalar_one_or_none()

    async def get_by_title(self, title: str):
        task = await self.session.execute(select(Task).where(Task.title == title))
        return task.scalar_one_or_none()

    async def get_project_tasks(self, project_id: int):
        tasks = await self.session.execute(
            select(Task).where(Task.project_id == project_id)
        )
        return tasks.scalars().all()

    async def get_user_tasks(self, user_id: int):
        tasks = await self.session.execute(
            select(Task).where(Task.assignee_id == user_id)
        )
        return tasks.scalars().all()

    async def get_comment_task(self, comment_id: int):
        task = await self.session.execute(
            select(Task).join(Comment.task).where(Comment.id == comment_id)
        )
        return task.scalar_one_or_none()

    async def create(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: int) -> Task:
        task = await self.get_by_id(task_id)
        self.session.delete(task)
        return task
