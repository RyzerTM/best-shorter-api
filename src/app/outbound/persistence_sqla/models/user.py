import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import (
    ENUM as PGENUM,
    UUID as PGUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.common.enums.user_role import UserRole
from app.outbound.persistence_sqla.models.base import BaseModel
from app.outbound.persistence_sqla.models.mixins.active import IsActiveMixin
from app.outbound.persistence_sqla.models.mixins.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.outbound.persistence_sqla.models.link import LinkModel


class UserModel(IsActiveMixin, TimestampMixin, BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    role: Mapped[UserRole] = mapped_column(
        PGENUM(
            UserRole,
            name="user_role_enum",
        ),
        default=UserRole.USER,
        nullable=False,
    )

    links: Mapped[list["LinkModel"]] = relationship(
        back_populates="owner",
        passive_deletes=True,
    )

    __table_args__ = (
        Index(
            "ix_users_active_created_at",
            "is_active",
            "created_at",
        ),
    )

    def __repr__(self) -> str:
        return f"<UserModel {self.id}>"
