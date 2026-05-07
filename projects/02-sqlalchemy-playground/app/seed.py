from sqlalchemy.ext.asyncio import AsyncSession

from .models import Project, Task, User


async def seed_data(session: AsyncSession):
    user1 = User(name="Alice")
    user2 = User(name="Bob")

    project1 = Project(title="Project A", owner=user1)
    project2 = Project(title="Project B", owner=user2)

    task1 = Task(title="Task 1", project=project1, assignee=user1)
    task2 = Task(title="Task 2", project=project1, assignee=user2)
    task3 = Task(title="Task 3", project=project2, assignee=user2)

    session.add_all([user1, user2, project1, project2, task1, task2, task3])
    await session.commit()
