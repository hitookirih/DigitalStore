from sqlalchemy import CheckConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .orders import Order


class User(IntIdPkMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "email IS NOT NULL or phone IS NOT NULL", name="email_or_phone_required"
        ),
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
