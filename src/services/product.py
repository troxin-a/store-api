from typing import List, Union
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from models.users import User
from schemas.product import ProductBase, ProductRead


async def product_create(data: ProductBase, db: AsyncSession) -> ProductRead:
    """
    Создает новый товар.
    """
    item = Product(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ProductRead.model_validate(item, from_attributes=True)


async def get_product_by_id(product_id: int, db: AsyncSession, user: Union[User, None] = None) -> Product:
    """
    Возвращает товар по его id.
    """
    query = select(Product).where(Product.id == product_id)
    response = await db.execute(query)
    item = response.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if (not user or (user and not user.is_admin)) and not item.is_active:
        raise HTTPException(status_code=423, detail="Товар неактивен")

    return item


async def product_update(product_id: int, data: ProductBase, db: AsyncSession) -> ProductRead:
    """
    Обновляет товар по его id.
    """
    item = await get_product_by_id(product_id, db)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)

    return ProductRead.model_validate(item, from_attributes=True)


async def product_read(user: User, product_id: int, db: AsyncSession) -> ProductRead:
    """
    Возвращает товар по его id.
    """
    item = await get_product_by_id(product_id, db, user)

    return ProductRead.model_validate(item, from_attributes=True)


async def product_list(user: User, db: AsyncSession) -> List[ProductRead]:
    """
    Возвращает список активных товаров.
    Если пользователь админ, возвращает все товары.
    """
    query = select(Product).order_by(Product.id.desc())

    if (user and not user.is_admin) or not user:
        query = query.where(Product.is_active)

    response = await db.execute(query)
    items = response.scalars().all()
    result = [ProductRead.model_validate(el, from_attributes=True) for el in items]

    return result


async def product_delete(product_id: int, db: AsyncSession):
    """
    Удаляет товар по его id.
    Если товар не существует, возвращает ошибку 404.
    """
    stmt = delete(Product).where(Product.id == product_id)
    response = await db.execute(stmt)
    deleted_count = response.rowcount
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Товар не найден")

    await db.commit()
    return JSONResponse(status_code=200, content={"message": "Товар успешно удалён"})
