from pathlib import Path

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def build_engine(database_url: str) -> AsyncEngine:
    url = make_url(database_url)
    if url.drivername.startswith("sqlite") and url.database not in (None, ":memory:"):
        Path(url.database).resolve().parent.mkdir(parents=True, exist_ok=True)
    return create_async_engine(database_url, echo=False)


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)
