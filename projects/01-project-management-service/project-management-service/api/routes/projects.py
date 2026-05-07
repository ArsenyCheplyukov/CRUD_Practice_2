from core.db import get_session
from exceptions import (
    CommentNotFound,
    ProjectNotCreated,
    ProjectNotDeleted,
    ProjectNotFound,
    ProjectNotUpdated,
    TaskNotFound,
    UserNotFound,
)
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from schemas.projects import (
    ProjectCreate,
    ProjectDelete,
    ProjectRead,
    ProjectReadWithTasks,
    ProjectUpdate,
)
from services.projects import ProjectService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get(
    "/",
    response_model=list[ProjectRead],
    status_code=status.HTTP_200_OK,
)
async def get_projects(
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    return await service.get_all()


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    status_code=status.HTTP_200_OK,
)
async def get_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    try:
        return await service.get_by_id(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


@router.get(
    "/{project_id}/with-tasks",
    response_model=ProjectReadWithTasks,
    status_code=status.HTTP_200_OK,
)
async def get_project_with_tasks(
    project_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    try:
        return await service.get_by_id_with_tasks(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


@router.get(
    "/user/{user_id}",
    response_model=list[ProjectRead],
    status_code=status.HTTP_200_OK,
)
async def get_user_projects(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    try:
        return await service.get_user_projects(user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get(
    "/task/{task_id}",
    response_model=ProjectRead,
    status_code=status.HTTP_200_OK,
)
async def get_task_project(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    try:
        return await service.get_task_project(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.get(
    "/comment/{comment_id}",
    response_model=ProjectRead,
)
async def get_comment_project(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    try:
        return await service.get_comment_project(comment_id)
    except CommentNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    try:
        return await service.create(project_data)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except ProjectNotCreated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Project not created"
        )


@router.put(
    "/{project_id}",
    response_model=ProjectRead,
    status_code=status.HTTP_200_OK,
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    try:
        return await service.update(project_id, project_data)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except ProjectNotUpdated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Project not updated"
        )


@router.delete(
    "/{project_id}",
    response_model=ProjectDelete,
    status_code=status.HTTP_200_OK,
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = ProjectService(session)
    try:
        return await service.delete(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    except ProjectNotDeleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Project not deleted"
        )
