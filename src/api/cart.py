from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from models.users import User
from schemas.cart import CartChange, CartChangeQuantity, CartProductCreate, CartRead
from services.cart import (
    add_cart_product,
    add_quantity_cart_product,
    delete_all_cart_products,
    delete_cart_product,
    get_cart,
    sub_quantity_cart_product,
)
from services.users import get_current_active_user

cart_router = APIRouter(prefix="/cart", tags=["Cart"])


@cart_router.post(
    "/",
    summary="Добавить товар в корзину",
    responses={
        401: {"description": "Unauthorized"},
        423: {"description": "Товар неактивен"},
        404: {"description": "Товар не найден"},
    },
    status_code=201,
)
async def add_product_to_cart(
    cart_product: CartProductCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartRead:
    """
    Поля, к заполнению:
    - ***product_id**: Уникальный идентификатор продукта
    - **quantity**: Количество (необязательно, по умолчанию - 1)

    Возвращает список товаров и стоимость.
    - **total_cost**: Сумма стоимости оставшихся товаров в корзине
    - **cart**: Список оставшихся товаров
    """
    return await add_cart_product(cart_product, user, db)


@cart_router.patch(
    "/add/{product_id}",
    summary="Добавить единицу товара в корзине.",
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Товар в корзине не найден"},
    },
)
async def add_quantity_product_in_cart(
    product_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartChangeQuantity:
    """
    Возвращает измененный пункт корзины (количество и товар) и стоимость.
    - **total_cost**: Измененная суммма стоимости товаров в корзине
    - **cart_item**: Информация о пункте в корзине
    """
    return await add_quantity_cart_product(product_id, user, db)


@cart_router.patch(
    "/sub/{product_id}",
    summary="Отнять единицу товара в корзине.",
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Товар в корзине не найден"},
    },
)
async def sub_quantity_product_in_cart(
    product_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartChangeQuantity | CartChange:
    """
    Возвращает измененный пункт корзины (количество и товар) и стоимость.
    - **total_cost**: Сумма стоимости оставшихся товаров в корзине
    - **cart_item**: Информация о пункте в корзине

    Если количество при уменьшении достигает нуля, возвращает список оставшихся товаров и стоимость.
    - **total_cost**: Сумма стоимости оставшихся товаров в корзине
    - **cart**: Список оставшихся товаров
    """
    return await sub_quantity_cart_product(product_id, user, db)


@cart_router.delete(
    "/{product_id}",
    summary="Удалить товар из корзины по его id",
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Товар в корзине не найден"},
    },
)
async def delete_product_from_cart(
    product_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartChange:
    """
    Возвращает список товаров в корзине.

    - **total_cost**: Сумма стоимости оставшихся товаров в корзине
    - **cart**: Список оставшихся товаров
    """
    return await delete_cart_product(product_id, user, db)


@cart_router.delete(
    "/",
    summary="Очистить корзину",
    responses={
        401: {"description": "Unauthorized"},
    },
)
async def clear_cart(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartChange:
    return await delete_all_cart_products(user, db)


@cart_router.get(
    "/",
    summary="Список товаров в корзине",
    responses={
        401: {"description": "Unauthorized"},
    },
)
async def list_product(
    user: User = Depends(get_current_active_user),
) -> CartRead:
    """
    Возвращает список товаров в корзине.

    - **total_cost**: Сумма стоимости всех товаров в корзине
    - **cart**: Список товаров
    """
    return await get_cart(user)
