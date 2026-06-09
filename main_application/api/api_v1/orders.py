from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.orders import Order, OrderCreate
from crud import orders as crud_orders

router = APIRouter(tags=["Orders"])


@router.get("/", response_model=list[Order])
async def get_orders(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud_orders.get_orders(session)


@router.get("/user/{user_id}/", response_model=list[Order])
async def get_user_orders(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud_orders.get_user_orders(session, user_id)


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await crud_orders.create_order(session, order_in)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
