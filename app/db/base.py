from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import exc, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


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

    async def health_check(self) -> bool:
        """Check database connection health."""
        if not self._engine:
            return False

        try:
            async with self.session() as session:
                result = await session.execute(text("SELECT 1"))
                return result.scalar() == 1
        except Exception as e:
            return False

    # Dependency
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as session:
            yield session


session_manager = DatabaseSessionManager()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan - Initialize and cleanup database here.
    """
    # Startup: Initialize database
    print("🚀 Starting application...")

    # Initialize database with settings
    session_manager.init(database_url=settings.database_url)

    # Health check
    if await session_manager.health_check():
        print("✅ Database connected")
    else:
        print("❌ Database connection failed")
    yield

    # Shutdown: Cleanup database
    print("🛑 Shutting down...")
    await session_manager.close()
