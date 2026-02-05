import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.session import session_manager
from app.logger.config import LOGGING_CONFIG
from app.middleware.logging import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan - Initialize and cleanup database.
    """
    # Startup
    print("🚀 Starting application...")

    settings = get_settings()

    # Initialize database
    session_manager.init(database_url=settings.database_url)

    # Health check
    if await session_manager.health_check():
        print("✅ Database connected successfully")
    else:
        print("❌ Database connection failed!")

    yield  # App runs here

    # Shutdown
    print("🛑 Shutting down application...")
    await session_manager.close()
    print("✅ Database connections closed")


def create_app() -> FastAPI:
    app = FastAPI(title="OS - Open Sesame", version="0.0.1", lifespan=lifespan)

    logging.config.dictConfig(LOGGING_CONFIG)

    # Custom middleware
    app.add_middleware(
        LoggingMiddleware,
    )

    # CORS (Cross-Origin Resource Sharing) middleware configuration
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "https://example.com",
        "https://www.example.com",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
