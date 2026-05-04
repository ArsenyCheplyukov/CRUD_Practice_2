from contextlib import asynccontextmanager

from api.routes import (
    comment_router,
    project_router,
    task_router,
    user_router,
)
from core.db import engine
from fastapi import FastAPI
from models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(comment_router)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def root():
    return {"status": "ok"}
