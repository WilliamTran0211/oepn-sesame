from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencices import get_redis_client
from app.core.redis import RedisClient
from app.db.dependencies import get_db
from app.services.auth import AuthService
from app.services.otp import OTPService
from app.services.user import UserService
from app.services.user_session import UserSessionService


def get_otp_service(redis_client=Depends(get_redis_client)) -> OTPService:
    return OTPService(redis_client)


def get_user_services(
    db: AsyncSession = Depends(get_db),
    otp_service: OTPService = Depends(get_otp_service),
) -> UserService:
    return UserService(db, otp_service)


def get_user_service_simple(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_auth_services(
    db: AsyncSession = Depends(get_db),
    redis_client: RedisClient = Depends(get_redis_client),
) -> AuthService:
    user_services = UserService(db)
    session_services = UserSessionService(db, redis_client)
    return AuthService(user_services, session_services)
