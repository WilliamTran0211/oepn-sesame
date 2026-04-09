from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repository.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.get_all(skip=skip, limit=limit, filters={"is_active": True})

    async def update_last_login(self, user_id: UUID) -> None:
        from datetime import datetime, timezone

        await self.update(user_id, last_login_at=datetime.now(timezone.utc))

    async def verify_email(self, user_id: UUID) -> None:
        await self.update(user_id, email_verified=True, is_verified=True)

    async def search_users(self, query: str, limit: int = 20) -> List[User]:
        search_query = (
            select(User)
            .where(
                or_(
                    User.email.ilike(f"%{query}%"),
                    User.full_name.ilike(f"%{query}%"),
                )
            )
            .limit(limit)
        )

        result = await self.db.execute(search_query)
        return list(result.scalars().all())

    async def get_superusers(self) -> List[User]:
        return await self.get_all(filters={"is_superuser": True})
