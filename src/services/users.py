from typing import Optional
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from config.settings import settings
from models.users import User
from schemas.users import CreateUser, UserRead, TokenData, LoginSchema
from config.db import get_db
from services.cart import create_cart


class SecurityBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"code": 401, "message": "Unauthorized"},
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication credentials",
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = SecurityBearer(scheme_name="Token", description="")


async def create_user(user: CreateUser, db: AsyncSession, is_admin=False):
    """
    Создает пользователя, хеширует пароль, сохраняет в БД и возвращает пользователя.
    """
    user_dump = user.model_dump(exclude=("password1", "password2"))
    user_dump["password"] = get_password_hash(user.password1)
    new_user = User(**user_dump)
    if is_admin:
        new_user.is_admin = True

    try:
        db.add(new_user)
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Пользователь с таким email или телефоном уже существует.")

    await db.refresh(new_user)
    await create_cart(new_user, db)

    return UserRead.model_validate(new_user)


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(db, username: str):
    query = select(User).where(
        or_(
            User.email == username,
            User.phone == username,
        )
    )

    result = await db.execute(query)
    user = result.scalars().first()

    return user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, key=settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Пользователь неактивен")
    return current_user


async def get_access_token(db: AsyncSession, data: LoginSchema):
    user = await authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Введен неверный email (телефон) или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.jwt.access_token_expire_minutes)

    return create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)


async def is_admin(user: User = Depends(get_current_active_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return True
