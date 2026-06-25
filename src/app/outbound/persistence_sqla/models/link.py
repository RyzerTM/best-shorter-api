import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    text as sql_text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.outbound.persistence_sqla.models.base import BaseModel
from app.outbound.persistence_sqla.models.mixins.active import IsActiveMixin
from app.outbound.persistence_sqla.models.mixins.expires import ExpiresAtMixin
from app.outbound.persistence_sqla.models.mixins.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.outbound.persistence_sqla.models.clicks import ClickModel
    from app.outbound.persistence_sqla.models.user import UserModel


class LinkModel(ExpiresAtMixin, IsActiveMixin, TimestampMixin, BaseModel):
    __tablename__ = "links"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    original_url_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    short_code: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    total_clicks: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        server_default="0",
        nullable=False,
    )
    unique_clicks: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        server_default="0",
        nullable=False,
    )

    last_clicked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    owner: Mapped["UserModel | None"] = relationship(back_populates="links")
    clicks: Mapped[list["ClickModel"]] = relationship(
        back_populates="link",
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint("short_code", name="uq_links_short_code"),
        Index(
            "ix_links_owner_created_at",
            "owner_id",
            sql_text("created_at DESC"),
            postgresql_where=sql_text("owner_id IS NOT NULL"),
        ),
        Index(
            "ix_links_active_expires_at",
            "expires_at",
            postgresql_where=sql_text("is_active = true AND expires_at IS NOT NULL"),
        ),
        Index(
            "ix_links_original_url_hash",
            "owner_id",
            "original_url_hash",
        ),
        CheckConstraint(
            "LENGTH(short_code) >= 4 AND LENGTH(short_code) <= 32",
            name="ch_short_code_length",
        ),
        CheckConstraint(
            "total_clicks >= 0",
            name="ch_links_total_clicks_nonnegative",
        ),
        CheckConstraint(
            "unique_clicks >= 0",
            name="ch_links_unique_clicks_nonnegative",
        ),
        CheckConstraint(
            "unique_clicks <= total_clicks",
            name="ch_links_unique_clicks_lte_total_clicks",
        ),
    )
