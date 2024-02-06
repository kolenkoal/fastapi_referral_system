from typing import Annotated

from sqlalchemy import NullPool, String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


DATABASE_URL = settings.DATABASE_URL_asyncpg

async_engine = create_async_engine(
    url=DATABASE_URL, echo=False, future=True
)

async_session_factory = async_sessionmaker(
    async_engine, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}
