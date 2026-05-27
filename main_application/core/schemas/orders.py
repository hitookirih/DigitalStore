from datetime import datetime
from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    id: int


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: datetime


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1
