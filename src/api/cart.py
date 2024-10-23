from typing import List
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from models.users import User
from schemas.cart_product import CartProductSchema
from services.cart import add_product_to_cart, get_cart
from services.users import get_current_active_user

cart_router = APIRouter(prefix="/cart", tags=["Cart"])


@cart_router.post(
    "/",
    summary="Добавить товар в корзину",
)
async def add_product(
    cart_product: CartProductSchema,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[CartProductSchema]:
    return await add_product_to_cart(cart_product, user, db)


@cart_router.get(
    "/",
    summary="Список корзины",
)
async def list_product(
    user: User = Depends(get_current_active_user),
    db=Depends(get_db),
) -> List[CartProductSchema]:
    return await get_cart(user, db)
