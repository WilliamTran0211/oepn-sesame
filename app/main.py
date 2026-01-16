from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="OS - Open Sesame", version="0.0.1")

    # Include routers
    app.include_router(api_router, prefix="/api/v1")


    

    return app


app = create_app()
