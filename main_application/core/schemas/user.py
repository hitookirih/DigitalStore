from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: bytes


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
