from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from schemas.users import Token, UserRead
from services.users import get_access_token, get_current_active_user

base_router = APIRouter(prefix="")


@base_router.get("/")
async def index(user: UserRead = Depends(get_current_active_user)):
    return {"message": "Started"}


@base_router.post(
    "/token",
    summary="Получить Bearer токен",
    tags=["Users"],
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Token:
    access_token = await get_access_token(db, form_data)
    return Token(access_token=access_token, token_type="bearer")
