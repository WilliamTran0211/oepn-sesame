from ast import List
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enum import VerificationPurpose
from app.common.error_message import ErrorMessage
from app.core import security
from app.core.exception import ConflictError, NotFoundError, UnauthorizedError
from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.user import CreateUserSchema, UpdateUserSchema
from app.services.otp import OTPService


class UserService:
    DUMMY_HASH = "$2b$12$eImiTXuWVxfM37uY4JANjQ" + "x" * 31

    def __init__(self, db: AsyncSession, otp_services: OTPService = None):
        self.repository = UserRepository(db)
        self._otp_services = otp_services

    async def get(self, id: str) -> User:
        return await self.repository.get(id)

    async def get_multi(
        self, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None
    ) -> List[User]:
        return await self.repository.get_all(skip=skip, limit=limit, filters=filters)

    async def create_user(self, data: CreateUserSchema) -> tuple[User, str]:
        check_user = await self.repository.get_by_email(data.email)

        if check_user:
            raise ConflictError(ErrorMessage.CONFLICT)

        pwd_hash = security.PasswordHelper.hash(data.password)

        user = await self.repository.create(
            email=data.email.lower(), hashed_password=pwd_hash, full_name=data.full_name
        )

        # gen OTP for verify
        otp_code = await self._otp_services.generate(
            user.id, purpose=VerificationPurpose.EMAIL_VERIFY
        )

        print(otp_code)

        return user

    async def update_user(self, user_id: str, data: UpdateUserSchema) -> User:
        check_user = await self.repository.get(id)

        if not check_user:
            raise NotFoundError(ErrorMessage.NOT_FOUND)

        user = await self.repository.update(check_user.id, data)

        return user

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.repository.get_by_email(email.lower())

        hashed_pwd = user.hashed_password if user else self.DUMMY_HASH

        is_valid = security.PasswordHelper.verify(
            password.encode(), hashed_pwd.encode()
        )

        if not user or not is_valid:
            raise UnauthorizedError(ErrorMessage.UNAUTHORIZED)

        return user

    async def verify_email(self, user_id: str, otp: str) -> User:
        check = await self._otp_services.verify(
            user_id, VerificationPurpose.EMAIL_VERIFY, otp
        )
        if not check:
            raise UnauthorizedError(ErrorMessage.UNAUTHORIZED)
        return await self.repository.update(user_id, {"is_verified": True})
