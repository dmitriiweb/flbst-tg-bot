from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sqlalchemy.orm as orm
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .. import config


class Base(orm.DeclarativeBase): ...


sqlalchemy_uri = (
    f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
    f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
)

engine = create_async_engine(
    sqlalchemy_uri,
    pool_size=5,  # Set pool size to 5
    pool_recycle=15 * 60,  # 15 min
    pool_pre_ping=True,
    future=True,
)


@asynccontextmanager
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSession(engine)
    try:
        yield session
    except Exception as e:
        error_msg = f"DB Session Error: {e}"
        logger.error(error_msg)
        await session.rollback()
        raise
    finally:
        await session.close()
