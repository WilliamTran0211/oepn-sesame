from fastapi import FastAPI
from app.api.v1.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="OS - Open Sesame", version="0.0.1")

    # Include các router
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"message": "Open sesame!"}

    return app


app = create_app()
