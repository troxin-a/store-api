from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from schemas.users import Token, LoginSchema
from services.users import get_access_token

base_router = APIRouter(prefix="")


@base_router.post(
    "/token",
    summary="Получить токен",
    tags=["User"],
)
async def login_for_access_token(data: LoginSchema, db: AsyncSession = Depends(get_db)) -> Token:
    """
    Поля, к заполнению:
    - **username**: email или телефон в формате +70000000000
    - **password**: пароль
    """
    access_token = await get_access_token(db, data)
    return Token(access_token=access_token, token_type="bearer")
