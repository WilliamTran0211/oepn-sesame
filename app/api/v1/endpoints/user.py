import logging
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_user_service_simple, get_user_services
from app.core.dependencices import get_redis_client
from app.core.redis import RedisClient
from app.db.dependencies import get_db
from app.schemas.user import CreateUserSchema, UserResponseSchema
from app.services.otp import OTPService
from app.services.user import UserService

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Open Sesame, User service!"}


@router.get("/me")
async def get_me():
    return


@router.patch("/me")
async def update_me():
    return


@router.post("/me/change-password")
async def change_password():
    return


@router.post("/register", response_model=UserResponseSchema)
async def register(
    user_data: CreateUserSchema, user_services: UserService = Depends(get_user_services)
):
    user = await user_services.create_user(user_data)
    return user


@router.post("/reset-password")
async def reset_password():
    return {"message": "reset password"}


@router.post("/verify")
async def verify_email():
    return {"message": "verify email"}


@router.get("/list", response_model=List[UserResponseSchema])
async def get_user_list(user_services: UserService = Depends(get_user_service_simple)):
    list_users = await user_services.get_multi()
    return list_users
