from sqlalchemy import Boolean, true
from sqlalchemy.orm import Mapped, mapped_column


class IsActiveMixin:
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=true(),
        sort_order=999,
    )
