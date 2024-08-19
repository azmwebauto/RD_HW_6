from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app import config


def create_engine():
    return create_async_engine(
        config.DB_URI,
        echo=False,
    )


@asynccontextmanager
async def make_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(engine)
    async with session_factory() as session:
        yield session
