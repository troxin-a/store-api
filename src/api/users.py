from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from schemas.users import CreateUser, LoginSchema, UserRead, Token
from services.users import create_user, get_access_token

users_router = APIRouter(prefix="/users", tags=["User"])


@users_router.post(
    "/register",
    summary="Регистрация",
    response_description="Пользователь создан",
    response_model=UserRead,
    status_code=201,
)
async def registration(user: CreateUser, db: AsyncSession = Depends(get_db)):
    """
    Создает нового пользователя.
    Все поля обязательны к заполнению.

    - **first_name***: Имя
    - **last_name**: Фамилия
    - **email**: email с валидацией
    - **phone**: Телефон должен начинаться с +7 и содержать 10 цифр
    - **password1**: Пароль должен быть не менее 8 символов, только латиница, минимум 1
    цифра минимум 1 символ верхнего регистра, минимум 1 спец символ ($%&!:)
    - **password2**: Повтор пароля
    """
    return await create_user(user, db)

@users_router.post(
    "/login",
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
