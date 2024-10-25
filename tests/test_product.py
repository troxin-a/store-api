import asyncio
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(admin_token, user_token, ac: AsyncClient):

    headers = {"Authorization": f"Bearer {admin_token}"}

    queries = [
        ac.post("/product/", headers=headers, json={"name": "test1", "price": 10}),
        ac.post("/product/", headers=headers, json={"name": "test2", "price": 15}),
        ac.post("/product/", headers=headers, json={"name": "test3", "price": 35}),
        ac.post("/product/", headers=headers, json={"name": "test4", "price": 35}),
        ac.post("/product/", headers=headers, json={"name": "test5", "price": 35}),
        ac.post("/product/", headers=headers, json={"name": "test6"}),
    ]

    responses = await asyncio.gather(*queries)
    for response in responses[0:-1]:
        assert response.status_code == 201

    assert responses[0].json() == {
        "name": "test1",
        "price": 10,
        "is_active": True,
        "id": responses[0].json()["id"],
        "created_at": responses[0].json()["created_at"],
        "updated_at": responses[0].json()["updated_at"],
    }
    assert responses[-1].status_code == 422

    # Создание неактивного товара
    response = await ac.post("/product/", headers=headers, json={"name": "no_act", "price": 50, "is_active": False})
    assert response.status_code == 201
    response = await ac.post("/product/", headers=headers, json={"name": "act", "price": 70})
    assert response.status_code == 201

    # Проверка на запрос пользователем
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.post("/product/", headers=headers, json={"name": "test11", "price": 10})
    assert response.status_code == 403

    # Проверка на запрос анонимным пользователем
    response = await ac.post("/product/", json={"name": "test11", "price": 10})
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product(admin_token, user_token, ac: AsyncClient):

    headers = {"Authorization": f"Bearer {admin_token}"}

    queries = [
        ac.patch("/product/1", headers=headers, json={"name": "updated_test1", "price": 100}),
        ac.patch("/product/2", headers=headers, json={"name": "updated_test2", "price": 200, "is_active": False}),
    ]

    responses = await asyncio.gather(*queries)
    for response in responses:
        assert response.status_code == 200

    assert responses[0].json() == {
        "name": "updated_test1",
        "price": 100,
        "is_active": True,
    }
    assert responses[1].json() == {
        "name": "updated_test2",
        "price": 200,
        "is_active": False,
    }

    # Проверка на запрос пользователем
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.patch("/product/1", headers=headers, json={"name": "test11"})
    assert response.status_code == 403

    # Проверка на запрос анонимным пользователем
    response = await ac.patch("/product/1", json={"name": "test11"})
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product(admin_token, user_token, ac: AsyncClient):

    headers = {"Authorization": f"Bearer {admin_token}"}

    queries = [
        ac.delete("/product/1", headers=headers),
        ac.delete("/product/2", headers=headers),
    ]

    responses = await asyncio.gather(*queries)
    for response in responses:
        assert response.status_code == 200
        assert response.json() == {"message": "Товар успешно удалён"}

    # Проверка на запрос пользователем
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.delete("/product/3", headers=headers)
    assert response.status_code == 403

    # Проверка на запрос анонимным пользователем
    response = await ac.delete("/product/4")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_read_product(admin_token, user_token, ac: AsyncClient):

    headers = {"Authorization": f"Bearer {admin_token}"}

    queries = [
        ac.get("/product/1", headers=headers),
        ac.get("/product/6", headers=headers),
        ac.get("/product/7", headers=headers),
    ]

    responses = await asyncio.gather(*queries)
    assert responses[0].status_code == 404
    assert responses[0].json() == {"detail": "Товар не найден"}
    assert responses[1].status_code == 200
    assert responses[1].json() == {
        "id": 6,
        "name": "no_act",
        "price": 50,
        "is_active": False,
        "created_at": responses[1].json()["created_at"],
        "updated_at": responses[1].json()["updated_at"],
    }
    assert responses[2].status_code == 200
    assert responses[2].json() == {
        "id": 7,
        "name": "act",
        "price": 70,
        "is_active": True,
        "created_at": responses[2].json()["created_at"],
        "updated_at": responses[2].json()["updated_at"],
    }

    # Проверка на запрос пользователем
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.get("/product/6", headers=headers)
    assert response.status_code == 423
    assert response.json() == {"detail": "Товар неактивен"}
    response = await ac.get("/product/7", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "id": 7,
        "name": "act",
        "price": 70,
        "is_active": True,
        "created_at": responses[2].json()["created_at"],
        "updated_at": responses[2].json()["updated_at"],
    }

    # Проверка на запрос анонимным пользователем
    response = await ac.get("/product/1")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_list_product(admin_token, user_token, ac: AsyncClient):

    headers = {"Authorization": f"Bearer {admin_token}"}

    response = await ac.get("/product/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 5

    # Проверка на запрос пользователем
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.get("/product/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 4

    # Проверка на запрос анонимным пользователем
    response = await ac.get("/product/1")
    assert response.status_code == 401
