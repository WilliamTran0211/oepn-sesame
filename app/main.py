import logging
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.logger.config import LOGGING_CONFIG
from app.middleware.logging import LoggingMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="OS - Open Sesame", version="0.0.1")

    logging.config.dictConfig(LOGGING_CONFIG)

    # Add middleware
    app.add_middleware(
        LoggingMiddleware,
    )

    # Include routers
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
