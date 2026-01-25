from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from core.config import Settings, settings
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from core.config import settings


# create engine
class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, database_url: str):
        self._engine = create_async_engine(
            database_url,
            pool_pre_ping=True,  # checking connection
            pool_size=10,  # current connection in pool
            max_overflow=20,  # max connection
            pool_recycle=3600,  # Recycle connection after 1h
            echo=settings.DEBUG,  # Log SQL queries for DEBUG
        )

        self._sessionmaker = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def close(self):
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._sessionmaker is None:
            raise IOError("DatabaseSessionManager is not initialized")

        async with self._sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except exc.SQLAlchemyError:
                await session.rollback()
                raise
            finally:
                await session.close()

    # Dependency
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as session:
            yield session


session_manager = DatabaseSessionManager()
session_manager.init(Settings.DATABASE_URL)
