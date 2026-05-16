from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    phone: str
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
