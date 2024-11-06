import asyncio
from httpx import AsyncClient
import pytest


async def execute_register(ac: AsyncClient, new_user: dict, email: str, phone: str, password1: str, password2: str):
    new_user.update(
        email=email,
        phone=phone,
        password1=password1,
        password2=password2,
    )
    return await ac.post("/users/register", json=new_user)


@pytest.mark.asyncio(loop_scope="session")
async def test_registration(ac: AsyncClient):
    email = ["test", "test@test.ru"]
    phone = ["+80000000000", "700000000", "+70000000000"]
    password = ["qwerty12345!", "Qwerty1234567", "Qbgbgfwer!!!ty!", "qwerty12345!", "Qwerty12345!"]
    new_user = {
        "first_name": "string",
        "last_name": "string",
    }
    empty_user = {}

    queries = [
        execute_register(ac, new_user, email[0], phone[-1], password[-1], password[-1]),
        execute_register(ac, new_user, email[-1], phone[0], password[-1], password[-1]),
        execute_register(ac, new_user, email[-1], phone[1], password[-1], password[-1]),
        execute_register(ac, new_user, email[-1], phone[-1], password[0], password[0]),
        execute_register(ac, new_user, email[-1], phone[-1], password[1], password[1]),
        execute_register(ac, new_user, email[-1], phone[-1], password[2], password[2]),
        execute_register(ac, new_user, email[-1], phone[-1], password[3], password[3]),
        execute_register(ac, new_user, email[-1], phone[-1], password[-1], password[3]),
        execute_register(ac, new_user, email[-1], phone[-1], password[3], password[-1]),
        execute_register(ac, empty_user, email[-1], phone[-1], password[-1], password[-1]),
    ]

    responses = await asyncio.gather(*queries)
    for response in responses:
        assert response.status_code == 422

    response = await execute_register(ac, new_user, email[-1], phone[-1], password[-1], password[-1])
    assert response.status_code == 201
    assert response.json() == {
        "id": response.json()["id"],
        "first_name": "string",
        "last_name": "string",
        "email": email[-1],
        "phone": phone[-1],
        "is_active": True,
    }
    response = await execute_register(ac, new_user, email[-1], phone[-1], password[-1], password[-1])
    assert response.status_code == 409


@pytest.mark.asyncio(loop_scope="session")
async def test_authentication(ac: AsyncClient):
    queries = [
        ac.post("/users/login", json={"username": "test@wrong.ru", "password": "test"}),
        ac.post("/users/login", json={"username": "test@test.ru", "password": "test"}),
        ac.post("/users/login", json={"username": "user1@user.ru", "password": "Qwerty12345!"}),
        ac.post("/users/login", json={"username": "+77777777777", "password": "Qwerty12345!"}),
    ]

    def codes():
        lst = [401, 401, 200, 200]
        for code in lst:
            yield code

    codes = codes()

    responses = await asyncio.gather(*queries)
    for response in responses:
        assert response.status_code == next(codes)

    # Последний ответ содержит токен
    assert responses[-1].json() == {
        "token_type": "bearer",
        "access_token": responses[-1].json()["access_token"],
    }
