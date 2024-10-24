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
)
async def add_product_to_cart(
    cart_product: CartProductCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartRead:
    return await add_cart_product(cart_product, user, db)


@cart_router.patch(
    "/add/{product_id}",
    summary="Добавить единицу товара в корзине.",
)
async def add_quantity_product_in_cart(
    product_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartChangeQuantity:
    return await add_quantity_cart_product(product_id, user, db)


@cart_router.patch(
    "/sub/{product_id}",
    summary="Отнять единицу товара в корзине.",
)
async def sub_quantity_product_in_cart(
    product_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartChangeQuantity | CartChange:
    return await sub_quantity_cart_product(product_id, user, db)


@cart_router.delete(
    "/{product_id}",
    summary="Удалить товар из корзины",
)
async def delete_product_from_cart(
    product_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartChange:
    return await delete_cart_product(product_id, user, db)


@cart_router.delete(
    "/",
    summary="Очистить корзину",
)
async def clear_cart(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> CartChange:
    return await delete_all_cart_products(user, db)


@cart_router.get(
    "/",
    summary="Список товаров в корзине",
)
async def list_product(
    user: User = Depends(get_current_active_user),
) -> CartRead:
    return await get_cart(user)
