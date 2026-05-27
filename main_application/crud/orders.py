from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Order, Product
from core.schemas.orders import OrderCreate


async def get_orders(session: AsyncSession) -> list[Order]:
    result = await session.execute(select(Order).order_by(Order.id))
    return list(result.scalars().all())


async def get_user_orders(session: AsyncSession, user_id: int) -> list[Order]:
    result = await session.execute(
        select(Order).where(Order.user_id == user_id).order_by(Order.id)
    )
    return list(result.scalars().all())


async def create_order(
    session: AsyncSession,
    order_in: OrderCreate,
) -> Order:
    product = await session.get(Product, order_in.product_id)
    if product is None:
        raise ValueError(f"Product {order_in.product_id} not found")

    total_price = product.price * order_in.quantity

    order = Order(
        **order_in.model_dump(),
        total_price=total_price,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order
