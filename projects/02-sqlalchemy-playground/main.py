import asyncio

from app.db import Base, SessionLocal, engine
from app.queries import (
    get_task_with_assignee_project,
    get_tasks_by_project_id,
    get_tasks_with_assignee,
    get_user_projects,
    get_users,
    get_users_projects,
    users_with_task_count,
    users_with_task_count_more_than_one,
)
from app.seed import seed_data


async def main():
    # Create tables (turn async engine into sync)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Fill database
    async with SessionLocal() as session:
        await seed_data(session)

    # Run queries
    async with SessionLocal() as session:
        # get users
        users = await get_users(session)
        print(users)
        # get user projects
        projects = await get_user_projects(session, 1)
        print(projects)
        # get project tasks
        tasks = await get_tasks_by_project_id(session, 1)
        print(tasks)
        # get tasks with assignee
        tasks_assignees = await get_tasks_with_assignee(session, 1)
        print(tasks_assignees)
        # N + 1 problem
        await get_users_projects(session)
        # solved N + 1 problem
        await get_task_with_assignee_project(session)
        # get user names and their task count
        user_task_count = await users_with_task_count(session)
        print(user_task_count)
        # get user names and their task count if more than one
        user_tasks_cond = await users_with_task_count_more_than_one(session)
        print(user_tasks_cond)


if __name__ == "__main__":
    asyncio.run(main())
