from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from .models import Project, Task, User


async def get_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_projects(session: AsyncSession, user_id: int):
    result = await session.execute(select(Project).where(Project.owner_id == user_id))
    return result.scalars().all()


async def get_tasks_by_project_id(session: AsyncSession, project_id: int):
    result = await session.execute(select(Task).where(Task.project_id == project_id))
    return result.scalars().all()


async def get_tasks_with_assignee(session: AsyncSession, project_id: int):
    result = await session.execute(
        select(Task.title, User.name)
        .join(User, Task.assignee_id == User.id)
        .where(Task.project_id == project_id)
    )
    return result.all()


async def get_users_projects(session: AsyncSession):
    result = await session.execute(select(User).options(selectinload(User.projects)))
    users = result.scalars().all()
    for user in users:
        print(user.name, user.projects)


async def get_task_with_assignee_project(session: AsyncSession):
    result = await session.execute(
        select(Task).options(joinedload(Task.project), joinedload(Task.assignee))
    )
    tasks = result.scalars().all()
    for task in tasks:
        print(task.project, task.assignee)


async def users_with_task_count(session: AsyncSession):
    result = await session.execute(
        select(User.name, func.count(Task.id))
        .join(Task, Task.assignee_id == User.id)
        .group_by(User.name)
    )
    return result.all()


async def users_with_task_count_more_than_one(session: AsyncSession):
    result = await session.execute(
        select(User.name, func.count(Task.id))
        .join(Task, Task.assignee_id == User.id)
        .group_by(User.name)
        .having(func.count(Task.id) > 1)
    )
    return result.all()
