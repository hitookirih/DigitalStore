from pathlib import Path
from typing import Sequence, Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_password
from core.models import User
from core.schemas.user import UserCreate, UserUpdatePartial


async def get_all_users(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user_by_email(
    session: AsyncSession,
    user_email: Annotated[str, Path],
) -> User | None:
    stmt = select(User).where(User.email == user_email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    user_data = user_create.model_dump()
    user_data["password"] = hash_password(user_data["password"])

    user = User(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()


async def update_user(
    session: AsyncSession,
    user: User,
    user_data: "UserUpdatePartial",
    partial: bool = True,
) -> User:
    for name, value in user_data.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    await session.refresh(user)
    return user
