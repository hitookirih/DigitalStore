from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .orders import Order


class Product(IntIdPkMixin, Base):
    __tablename__ = "products"
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )
