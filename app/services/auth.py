from sqlalchemy.ext.asyncio import AsyncSession

from app.common.error_message import ErrorMessage
from app.core.exception import NotFoundError
from app.models.user import User
from app.models.user_session import UserSession
from app.repository.user import UserRepository
from app.repository.user_session import UserSessionRepository
from app.services.otp import OTPService
from app.services.user import UserService
from app.services.user_session import UserSessionService


class AuthService:

    def __init__(
        self, user_services: UserService, session_services: UserSessionService
    ):
        self.user_services = user_services
        self.session_services = session_services

    async def login(
        self, email: str, password: str, ip_address: str, user_agent: str
    ) -> tuple[User, UserSession]:
        user = await self.user_services.authenticate(email, password)
        session = await self.session_services.create_session(
            user.id, ip_address, user_agent
        )
        return user, session

    async def logout(self, session_id: str) -> None:
        await self.session_services.terminate_session(session_id)

    def authorize(self):
        pass

    def client_credentials(self):
        pass

    def refresh_token(self):
        pass

    def revoke_token(self):
        pass
