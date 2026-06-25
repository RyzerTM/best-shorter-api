import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    text as sql_text,
)
from sqlalchemy.dialects.postgresql import (
    INET as PGINET,
    UUID as PGUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.outbound.persistence_sqla.models.base import BaseModel
from app.outbound.persistence_sqla.models.mixins.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.outbound.persistence_sqla.models.link import LinkModel


class ClickModel(TimestampMixin, BaseModel):
    __tablename__ = "clicks"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    link_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "links.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    ip_address: Mapped[str | None] = mapped_column(PGINET, nullable=True)
    visitor_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    device_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    os: Mapped[str | None] = mapped_column(String(50), nullable=True)
    browser: Mapped[str | None] = mapped_column(String(50), nullable=True)
    referrer: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    is_unique: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    link: Mapped["LinkModel"] = relationship(back_populates="clicks")

    __table_args__ = (
        Index(
            "ix_clicks_link_created_at",
            "link_id",
            sql_text("created_at DESC"),
        ),
        Index(
            "ix_clicks_link_visitor_hash",
            "link_id",
            "visitor_hash",
            postgresql_where=sql_text("visitor_hash IS NOT NULL"),
        ),
        Index(
            "ix_clicks_link_country_code",
            "link_id",
            "country_code",
        ),
        CheckConstraint(
            "country_code IS NULL OR LENGTH(country_code) = 2",
            name="ch_clicks_country_code_length",
        ),
    )

    def __repr__(self) -> str:
        return f"<ClickModel {self.id}>"
