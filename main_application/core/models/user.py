from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)

    __table_args__ = (
        CheckConstraint(
            "email IS NOT NULL or phone IS NOT NULL", name="email_or_phone_required"
        ),
    )
