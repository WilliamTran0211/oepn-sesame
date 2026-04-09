import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class UserSession(UUIDMixin, TimestampMixin, Base):
    """
    Browser session là backbone của SSO.

    Flow:
    1. User login → tạo row này + lưu session_id vào Redis + set HttpOnly cookie.
    2. Project khác redirect /authorize → Open-sesame đọc cookie,
       tìm session còn active → skip login, cấp code ngay.
    3. Logout → terminated_at = now, xóa key Redis.

    Redis lưu:  session_id → user_id
    PostgreSQL: full record
    """

    __tablename__ = "user_sessions"

    # ── Session ID ────────────────────────────────────────────────
    session_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
    )
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    terminated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="NULL = still active. Set on explicit logout.",
    )

    user: Mapped["User"] = relationship("User", back_populates="sessions")

    __table_args__ = (Index("ix_user_sessions_expires_at", "expires_at"),)

    @property
    def is_active(self) -> bool:
        return (
            self.terminated_at is None and datetime.now(timezone.utc) < self.expires_at
        )

    def __repr__(self) -> str:
        return (
            f"<UserSession id={self.id} user_id={self.user_id} active={self.is_active}>"
        )
