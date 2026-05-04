from core.db import get_session
from exceptions import (
    CommentNotFound,
    ProjectNotFound,
    TaskNotFound,
    UserAlreadyExists,
    UserNotCreated,
    UserNotDeleted,
    UserNotFound,
    UserNotUpdated,
)
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from schemas.users import (
    UserCreate,
    UserDelete,
    UserRead,
    UserUpdate,
)
from services.users import UserService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    return await service.get_all()


@router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        return await service.get_by_id(user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@router.get(
    "/project/{project_id}",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
)
async def get_project_users(
    project_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        return await service.get_project_users(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


@router.get(
    "/task/{task_id}",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
)
async def get_task_users(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        return await service.get_task_users(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.get(
    "/comment/{comment_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_comment_user(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        return await service.get_comment_user(comment_id)
    except CommentNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        return await service.create(user_data)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    except UserNotCreated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not created",
        )


@router.put(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        return await service.update(user_id, user_data)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except UserNotUpdated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not updated",
        )


@router.delete(
    "/{user_id}",
    response_model=UserDelete,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    try:
        return await service.delete(user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except UserNotDeleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not deleted",
        )
