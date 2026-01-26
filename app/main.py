import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import lifespan
from app.logger.config import LOGGING_CONFIG
from app.middleware.logging import LoggingMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="OS - Open Sesame", version="0.0.1", lifespan=lifespan)

    logging.config.dictConfig(LOGGING_CONFIG)

    # Custome middleware
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
