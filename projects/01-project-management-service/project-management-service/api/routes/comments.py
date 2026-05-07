from core.db import get_session
from exceptions import (
    CommentNotCreated,
    CommentNotDeleted,
    CommentNotFound,
    ProjectNotFound,
    TaskNotFound,
    UserNotFound,
)
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from schemas.comments import (
    CommentCreate,
    CommentDelete,
    CommentRead,
    CommentReadWithDetails,
    CommentUpdate,
)
from services.comments import CommentService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get(
    "/",
    response_model=list[CommentRead],
    status_code=status.HTTP_200_OK,
)
async def get_comments(
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    return await service.get_all()


@router.get(
    "/{comment_id}",
    response_model=CommentRead,
    status_code=status.HTTP_200_OK,
)
async def get_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.get_by_id(comment_id)
    except CommentNotFound:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )


@router.get(
    "/{comment_id}",
    response_model=CommentReadWithDetails,
    status_code=status.HTTP_200_OK,
)
async def get_comment_with_details(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.get_by_id_with_details(comment_id)
    except CommentNotFound:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )


@router.get(
    "/task/{task_id}",
    response_model=list[CommentRead],
    status_code=status.HTTP_200_OK,
)
async def get_task_comments(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.get_task_comments(task_id)
    except TaskNotFound:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.get(
    "/user/{user_id}",
    response_model=list[CommentRead],
    status_code=status.HTTP_200_OK,
)
async def get_user_comments(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.get_user_comments(user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get(
    "/project/{project_id}",
    response_model=list[CommentRead],
    status_code=status.HTTP_200_OK,
)
async def get_project_comments(
    project_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.get_project_comments(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )


@router.get(
    "/task/{task_id}/user/{user_id}",
    response_model=list[CommentRead],
    status_code=status.HTTP_200_OK,
)
async def get_task_user_comments(
    task_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.get_task_user_comments(task_id, user_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get(
    "/project/{project_id}/user/{user_id}",
    response_model=list[CommentRead],
    status_code=status.HTTP_200_OK,
)
async def get_project_user_comments(
    project_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.get_project_user_comments(project_id, user_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post(
    "/",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    comment_data: CommentCreate,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.create(comment_data)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except CommentNotCreated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Comment not created"
        )


@router.put(
    "/{comment_id}",
    response_model=CommentRead,
    status_code=status.HTTP_200_OK,
)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.update(comment_id, comment_data)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except CommentNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Comment already exists"
        )
    except CommentNotCreated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Comment not created"
        )


@router.delete(
    "/{comment_id}",
    response_model=CommentDelete,
    status_code=status.HTTP_200_OK,
)
async def delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = CommentService(session)
    try:
        return await service.delete(comment_id)
    except CommentNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    except CommentNotDeleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Comment not deleted"
        )
