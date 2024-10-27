from typing import List
from fastapi import Depends
from fastapi.routing import APIRouter
from config.db import get_db
from models.users import User
from schemas.product import ProductBase, ProductRead, ProductPatch
from services.product import product_create, product_delete, product_list, product_read, product_update
from services.users import get_current_user_or_none, is_admin

product_router = APIRouter(prefix="/product", tags=["Product"])


@product_router.post(
    "",
    summary="Новый товар",
    dependencies=[Depends(is_admin)],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
    status_code=201,
)
async def create_product(
    product: ProductBase,
    db=Depends(get_db),
) -> ProductRead:
    """
    Создает новый товар. Возвращает созданный товар (см. Информация о товаре).

    Только для администратора.

    Поля, к заполнению:
    - ***name**: Наименование
    - ***price**: Цена
    - **is_active**: Активен/Неактивен (необязательно, по умолчанию - true)
    """
    return await product_create(product, db)


@product_router.patch(
    "/{product_id}",
    summary="Редактировать товар",
    dependencies=[Depends(is_admin)],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Товар не найден"},
    },
)
async def update_product(
    product_id: int,
    product: ProductPatch,
    db=Depends(get_db),
) -> ProductPatch:
    """
    Вносит изменения в товар, определяя его по id.

    Только для администратора.

    Возвращает измененный товар (см. Информация о товаре).

    Поля, НЕ обязательны к заполнению:
    - **name**: Наименование
    - **price**: Цена
    - **is_active**: Активен/Неактивен
    """
    return await product_update(product_id, product, db)


@product_router.get(
    "/{product_id}",
    summary="Информация о товаре",
    responses={
        401: {"description": "Unauthorized"},
        423: {"description": "Товар неактивен"},
        404: {"description": "Товар не найден"},
    },
)
async def retrieve_product(
    product_id: int,
    user: User = Depends(get_current_user_or_none),
    db=Depends(get_db),
) -> ProductRead:
    """
    Возвращает товар из БД по его id
    - **name**: Наименование
    - **price**: Цена
    - **is_active**: Активен/Неактивен
    - **id**: Уникальный идентификатор
    - **created_at**: Дата и время добавления
    - **updated_at**: Дата и время последнего изменения

    **Авторизация - не обязательна.**
    """
    return await product_read(user, product_id, db)


@product_router.get(
    "",
    summary="Список товаров",
    responses={401: {"description": "Unauthorized"}},
)
async def list_product(
    user: User = Depends(get_current_user_or_none),
    db=Depends(get_db),
) -> List[ProductRead]:
    """
    Возвращает список активных товаров.

    Если пользователь админ, возвращает все товары (см. Информация о товаре)

    **Авторизация - не обязательна.**
    """
    return await product_list(user, db)


@product_router.delete(
    "/{product_id}",
    summary="Удалить товар",
    dependencies=[Depends(is_admin)],
    response_description="Товар удален",
    responses={
        200: {"description": "Успешное удаление"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Товар не найден"},
    },
)
async def delete_product(
    product_id: int,
    db=Depends(get_db),
):
    """
    Удаляет товар из БД по его id.

    Только для администратора.
    """
    return await product_delete(product_id, db)
