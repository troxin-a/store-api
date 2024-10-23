from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from schemas.users import CreateUser, UserRead
from services.users import create_user

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post(
    "/register",
    summary="Регистрация",
)
async def registration(user: CreateUser, db: AsyncSession = Depends(get_db)) -> UserRead:
    return await create_user(user, db)
