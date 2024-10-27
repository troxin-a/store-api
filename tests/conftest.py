from typing import AsyncGenerator
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config.db import Base, get_db
from config.settings import settings
from main import app
from models.product import Product
from schemas.users import CreateUser
from services.users import create_user, get_access_token


engine_test = create_async_engine(f"{settings.db.url}_test")
async_test_session_maker = async_sessionmaker(
    bind=engine_test,
    expire_on_commit=False,
    autoflush=False,
)


async def get_test_db():
    async with async_test_session_maker() as db:
        yield db


app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)


products = [
    {"id": 101, "name": "test1", "price": 30, "is_active": True},
    {"id": 102, "name": "test2", "price": 25, "is_active": False},
    {"id": 103, "name": "test3", "price": 35, "is_active": True},
    {"id": 104, "name": "test4", "price": 10, "is_active": True},
]


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(Product.__table__.insert(), products)
    yield
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as session:
        yield session


@pytest.fixture(scope="session")
async def admin_token():
    user = CreateUser(
        email="admin@admin.ru",
        first_name="admin",
        last_name="admin",
        phone="+79999999999",
        password1="Qwerty12345!",
        password2="Qwerty12345!",
    )

    async with async_test_session_maker() as db:
        user = await create_user(user, db, is_admin=True)
        form_data = OAuth2PasswordRequestForm(username="admin@admin.ru", password="Qwerty12345!")
        token = await get_access_token(db, form_data)

    return token


@pytest.fixture(scope="session")
async def user_token():
    user = CreateUser(
        email="user1@user.ru",
        first_name="user1",
        last_name="user1",
        phone="+77777777777",
        password1="Qwerty12345!",
        password2="Qwerty12345!",
    )

    async with async_test_session_maker() as db:
        user = await create_user(user, db, is_admin=False)
        form_data = OAuth2PasswordRequestForm(username="user1@user.ru", password="Qwerty12345!")
        token = await get_access_token(db, form_data)

    return token
