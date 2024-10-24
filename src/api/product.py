from typing import List
from fastapi import Depends
from fastapi.routing import APIRouter
from config.db import get_db
from models.users import User
from schemas.product import ProductBase, ProductRead, ProductPatch
from services.product import product_create, product_delete, product_list, product_read, product_update
from services.users import get_current_active_user, is_admin

product_router = APIRouter(prefix="/product", tags=["Product"])


@product_router.post(
    "/",
    summary="Новый товар",
    dependencies=[Depends(is_admin)],
)
async def create_product(
    product: ProductBase,
    db=Depends(get_db),
) -> ProductRead:
    return await product_create(product, db)


@product_router.patch(
    "/{product_id}",
    summary="Редактировать товар",
    dependencies=[Depends(is_admin)],
)
async def update_product(
    product_id: int,
    product: ProductPatch,
    db=Depends(get_db),
) -> ProductPatch:
    return await product_update(product_id, product, db)


@product_router.get(
    "/{product_id}",
    summary="Информация о товаре",
)
async def retrieve_product(
    product_id: int,
    user: User = Depends(get_current_active_user),
    db=Depends(get_db),
) -> ProductRead:
    return await product_read(user, product_id, db)


@product_router.get(
    "/",
    summary="Список товаров",
)
async def list_product(
    user: User = Depends(get_current_active_user),
    db=Depends(get_db),
) -> List[ProductRead]:
    return await product_list(user, db)


@product_router.delete(
    "/{product_id}",
    summary="Удалить товар",
    dependencies=[Depends(is_admin)],
)
async def delete_product(
    product_id: int,
    db=Depends(get_db),
):
    return await product_delete(product_id, db)
