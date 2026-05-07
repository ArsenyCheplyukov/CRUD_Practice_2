from core.db import get_session
from exceptions import (
    ProjectNotFound,
    TaskNotCreated,
    TaskNotDeleted,
    TaskNotFound,
    TaskNotUpdated,
    UserNotFound,
)
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from schemas.tasks import (
    TaskCreate,
    TaskDelete,
    TaskRead,
    TaskUpdate,
    TaskReadWithProject,
)
from services.tasks import TaskService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "/",
    response_model=list[TaskRead],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    session: AsyncSession = Depends(get_session),
):
    service = TaskService(session)
    return await service.get_all()


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = TaskService(session)
    try:
        return await service.get_by_id(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.get(
    "/{task_id}/with-project",
    response_model=TaskReadWithProject,
    status_code=status.HTTP_200_OK,
)
async def get_task_with_project(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = TaskService(session)
    try:
        return await service.get_by_id_with_project(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.get(
    "/project/{project_id}",
    response_model=list[TaskRead],
    status_code=status.HTTP_200_OK,
)
async def get_project_tasks(
    project_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = TaskService(session)
    try:
        return await service.get_project_tasks(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


@router.get(
    "/user/{user_id}",
    response_model=list[TaskRead],
    status_code=status.HTTP_200_OK,
)
async def get_user_tasks(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = TaskService(session)
    try:
        return await service.get_user_tasks(user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
):
    service = TaskService(session)
    try:
        return await service.create(task_data)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except TaskNotCreated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task not created",
        )


@router.put(
    "/{task_id}",
    response_model=TaskRead,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
):
    service = TaskService(session)
    try:
        return await service.update(task_id, task_data)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    except TaskNotUpdated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task not updated",
        )


@router.delete(
    "/{task_id}",
    response_model=TaskDelete,
    status_code=status.HTTP_200_OK,
)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = TaskService(session)
    try:
        return await service.delete(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    except TaskNotDeleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task not deleted",
        )
