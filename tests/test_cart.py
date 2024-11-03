import asyncio
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_add_product_to_cart(user_token, ac: AsyncClient):
    """Успешное добавление товаров в корзину"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.post("/cart", headers=headers, json={"product_id": 101, "quantity": 10})
    assert response.status_code == 201
    response = await ac.post("/cart", headers=headers, json={"product_id": 104})
    assert response.status_code == 201
    response = await ac.post("/cart", headers=headers, json={"product_id": 103, "quantity": 1})
    assert response.status_code == 201
    response = await ac.post("/cart", headers=headers, json={"product_id": 103})
    assert response.status_code == 201
    assert response.json() == {
        "total_cost": 380,
        "cart": [
            {
                "quantity": 10,
                "product": {
                    "id": 101,
                    "is_active": True,
                    "name": "test1",
                    "price": 30,
                },
            },
            {
                "quantity": 2,
                "product": {
                    "id": 103,
                    "is_active": True,
                    "name": "test3",
                    "price": 35,
                },
            },
            {
                "quantity": 1,
                "product": {
                    "id": 104,
                    "is_active": True,
                    "name": "test4",
                    "price": 10,
                },
            },
        ],
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_add_non_active_product_to_cart(user_token, ac: AsyncClient):
    """Попытка добавления неактивного товара в корзину"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.post("/cart", headers=headers, json={"product_id": 102})
    assert response.status_code == 423
    assert response.json() == {"detail": "Товар неактивен"}


@pytest.mark.asyncio(loop_scope="session")
async def test_add_nonproduct_to_cart(user_token, ac: AsyncClient):
    """Попытка добавления несуществующего товара в корзину"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.post("/cart", headers=headers, json={"product_id": 1000})
    assert response.status_code == 404
    assert response.json() == {"detail": "Товар не найден"}


@pytest.mark.asyncio(loop_scope="session")
async def test_add_quantity_product_to_cart(user_token, ac: AsyncClient):
    """Успешное добавление единицы товара в корзине"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.patch("/cart/add/101", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Количество товара в корзине обновлено",
        "total_cost": 410,
        "cart_item": {
            "quantity": 11,
            "product": {
                "id": 101,
                "is_active": True,
                "name": "test1",
                "price": 30,
            },
        },
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_first_sub_quantity_product_from_cart(user_token, ac: AsyncClient):
    """Успешное исключение единицы товара в корзине"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.patch("/cart/sub/103", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Количество товара в корзине обновлено",
        "total_cost": 375,
        "cart_item": {
            "quantity": 1,
            "product": {
                "id": 103,
                "is_active": True,
                "name": "test3",
                "price": 35,
            },
        },
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_second_sub_quantity_product_from_cart(user_token, ac: AsyncClient):
    """Еще однно исключение единицы товара в корзине, приводящее к удалению записи"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.patch("/cart/sub/103", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Товар удален из корзины",
        "total_cost": 340,
        "cart": [
            {
                "quantity": 11,
                "product": {
                    "id": 101,
                    "is_active": True,
                    "name": "test1",
                    "price": 30,
                },
            },
            {
                "quantity": 1,
                "product": {
                    "id": 104,
                    "is_active": True,
                    "name": "test4",
                    "price": 10,
                },
            },
        ],
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_change_quantity_nonproduct_from_cart(user_token, ac: AsyncClient):
    """Попытка изменения идиницы товара, которого нет в корзине"""
    headers = {"Authorization": f"Bearer {user_token}"}

    queries = [
        ac.patch("/cart/sub/1000", headers=headers),
        ac.patch("/cart/add/1000", headers=headers),
    ]
    responses = await asyncio.gather(*queries)

    for response in responses:
        assert response.status_code == 404
        assert response.json() == {"detail": "Товар в корзине не найден"}


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_from_cart(user_token, ac: AsyncClient):
    """Успешное удаление товара из корзины"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.delete("/cart/104", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Товар удален из корзины",
        "cart": [
            {
                "quantity": 11,
                "product": {
                    "id": 101,
                    "is_active": True,
                    "name": "test1",
                    "price": 30,
                },
            },
        ],
        "total_cost": 330,
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_get_cart(user_token, ac: AsyncClient):
    """Получение корзины"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.get("/cart", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "total_cost": 330,
        "cart": [
            {
                "quantity": 11,
                "product": {
                    "id": 101,
                    "is_active": True,
                    "name": "test1",
                    "price": 30,
                },
            },
        ],
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_nonproduct_from_cart(user_token, ac: AsyncClient):
    """Попытка удаления товара, которого нет в корзине"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.delete("/cart/1000", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Товар в корзине не найден"}


@pytest.mark.asyncio(loop_scope="session")
async def test_clear_cart(user_token, ac: AsyncClient):
    """Очистка всей корзины"""
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await ac.delete("/cart", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Корзина очищена",
        "cart": [],
        "total_cost": 0,
    }
