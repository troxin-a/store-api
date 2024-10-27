from httpx import AsyncClient
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_list_product(ac: AsyncClient):
    """Попытка получения списка товаров"""
    response = await ac.get("/product")
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_read_product(ac: AsyncClient):
    """Попытка чтения товара"""
    response = await ac.get("/product/103")
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product(ac: AsyncClient):
    """Попытка удаления товара"""
    response = await ac.delete("/product/4")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product(ac: AsyncClient):
    """Попытка обновления товара"""
    response = await ac.patch("/product/1", json={"name": "test11"})
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_by_anonim(ac: AsyncClient):
    """Попытка создать товар"""

    response = await ac.post("/product", json={"name": "test11", "price": 10})
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_add_product_to_cart(ac: AsyncClient):
    """Попытка добавления товара"""
    response = await ac.post("/cart", json={"product_id": 101})
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_add_quantity_product_to_cart(ac: AsyncClient):
    """Попытка добавления единицы товара из корзины"""
    response = await ac.patch("/cart/add/101")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_sub_quantity_product_from_cart(ac: AsyncClient):
    """Попытка исключения единицы товара из корзины"""
    response = await ac.patch("/cart/sub/103")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_from_cart(ac: AsyncClient):
    """Попытка удаления товара"""
    response = await ac.delete("/cart/1000")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_clear_cart(ac: AsyncClient):
    """Попытка очистка корзины"""
    response = await ac.delete("/cart")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_get_cart(ac: AsyncClient):
    """Попытка получения корзины"""
    response = await ac.get("/cart")
    assert response.status_code == 401
