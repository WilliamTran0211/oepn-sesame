import uuid
from typing import TYPE_CHECKING, List, Optional
from unittest.mock import Base
from uuid import UUID

from sqlalchemy import ARRAY, Boolean, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.common.enum import ClientType
from app.models.base import Base, TimestampMixin, UUIDMixin


class OAuthClient(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "oauth_clients"

    # Client identity
    client_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )
    client_secret_hash: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    client_type: Mapped[ClientType] = mapped_column(
        Enum(ClientType, name="client_type_enum"),
        nullable=False,
        default=ClientType.CONFIDENTIAL,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # OAuth configuration
    redirect_uris: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    grant_types: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=lambda: ["authorization_code", "refresh_token"],
    )
    require_pkce: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Token TTL overrides in seconds
    access_token_ttl: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    refresh_token_ttl: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
