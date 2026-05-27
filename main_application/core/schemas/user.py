from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    phone: str
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
