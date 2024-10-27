import asyncio
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(admin_token, ac: AsyncClient):
    """Успешное создание нескольких товаров"""
    headers = {"Authorization": f"Bearer {admin_token}"}

    queries = [
        ac.post("/product", headers=headers, json={"name": "test1", "price": 10}),
        ac.post("/product", headers=headers, json={"name": "test2", "price": 15}),
        ac.post("/product", headers=headers, json={"name": "test3", "price": 35}),
        ac.post("/product", headers=headers, json={"name": "test4", "price": 35}),
        ac.post("/product", headers=headers, json={"name": "test5", "price": 35}),
    ]

    responses = await asyncio.gather(*queries)
    for response in responses:
        assert response.status_code == 201

    assert responses[0].json() == {
        "name": "test1",
        "price": 10,
        "is_active": True,
        "id": responses[0].json()["id"],
        "created_at": responses[0].json()["created_at"],
        "updated_at": responses[0].json()["updated_at"],
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_active_noactive(admin_token, ac: AsyncClient):
    """Успешное создание двух товаров: с флагом Активен и с флагом Неактивен"""
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Создание неактивного товара
    response = await ac.post("/product", headers=headers, json={"name": "no_act", "price": 50, "is_active": False})
    assert response.status_code == 201
    response = await ac.post("/product", headers=headers, json={"name": "act", "price": 70})
    assert response.status_code == 201


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_error_validation(admin_token, ac: AsyncClient):
    """Ошибка валидации при создании товара"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await ac.post("/product", headers=headers, json={"name": "test6"})
    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_by_admin(user_token, ac: AsyncClient):
    """Попытка создать товар неадмином"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.post("/product", headers=headers, json={"name": "test11", "price": 10})
    assert response.status_code == 403


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product(admin_token, ac: AsyncClient):
    """Успешное обновление нескольких товаров"""
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


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_user(user_token, ac: AsyncClient):
    """Попытка обновления товара неадмином"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.patch("/product/1", headers=headers, json={"name": "test11"})
    assert response.status_code == 403


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_by_admin(admin_token, ac: AsyncClient):
    """Успешное удаление нескольких товаров"""
    headers = {"Authorization": f"Bearer {admin_token}"}

    queries = [
        ac.delete("/product/1", headers=headers),
        ac.delete("/product/2", headers=headers),
    ]

    responses = await asyncio.gather(*queries)
    for response in responses:
        assert response.status_code == 200
        assert response.json() == {"message": "Товар успешно удалён"}


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_by_user(user_token, ac: AsyncClient):
    """Попытка удаления товароа неадмином"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.delete("/product/3", headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio(loop_scope="session")
async def test_read_product_by_admin(admin_token, ac: AsyncClient):
    """Успешное чтение нескольких товаров админом"""
    headers = {"Authorization": f"Bearer {admin_token}"}

    queries = [
        ac.get("/product/6", headers=headers),
        ac.get("/product/7", headers=headers),
    ]

    responses = await asyncio.gather(*queries)
    assert responses[0].status_code == 200
    assert responses[0].json() == {
        "id": 6,
        "name": "no_act",
        "price": 50,
        "is_active": False,
        "created_at": responses[0].json()["created_at"],
        "updated_at": responses[0].json()["updated_at"],
    }
    assert responses[1].status_code == 200
    assert responses[1].json() == {
        "id": 7,
        "name": "act",
        "price": 70,
        "is_active": True,
        "created_at": responses[1].json()["created_at"],
        "updated_at": responses[1].json()["updated_at"],
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_read_none_product(admin_token, user_token, ac: AsyncClient):
    """Попытка получения несуществующего товара админом и пользователем"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await ac.get("/product/1", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Товар не найден"}

    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.get("/product/1", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Товар не найден"}


@pytest.mark.asyncio(loop_scope="session")
async def test_read_product_by_user(user_token, ac: AsyncClient):
    """Успешное чтение товара простым пользователем"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.get("/product/7", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "id": 7,
        "name": "act",
        "price": 70,
        "is_active": True,
        "created_at": response.json()["created_at"],
        "updated_at": response.json()["updated_at"],
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_read_noactive_product_by_user(user_token, ac: AsyncClient):
    """Попытка чтения НЕАКТИВНОГО товара простым пользователем"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.get("/product/6", headers=headers)
    assert response.status_code == 423
    assert response.json() == {"detail": "Товар неактивен"}


@pytest.mark.asyncio(loop_scope="session")
async def test_list_product_by_admin(admin_token, ac: AsyncClient):
    """Успешное получение списка товаров админом"""
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = await ac.get("/product", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 9


@pytest.mark.asyncio(loop_scope="session")
async def test_list_product_by_user(user_token, ac: AsyncClient):
    """Успешное получение списка товаров простым пользователем"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await ac.get("/product", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 7
