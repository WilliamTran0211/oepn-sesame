from fastapi import APIRouter
from .endpoints import auth, user, otp, projects, oauth, api_keys

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(otp.router, prefix="/otp", tags=["otp"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(oauth.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api_keys"])