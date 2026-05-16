from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import UserRead, UserCreate
from crud import users as users_crud

router = APIRouter(tags=["Users"])


@router.get("/", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await users_crud.get_all_users(session=session)
    return users


@router.post("/", response_model=UserRead)
async def create_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    user = await users_crud.create_user(
        user_create=user_create,
        session=session,
    )
    return user
