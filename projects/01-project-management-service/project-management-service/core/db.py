import os
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DEBUG: Connecting to {DATABASE_URL}")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[Any, Any]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
