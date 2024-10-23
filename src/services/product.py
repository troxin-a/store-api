from typing import List
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from schemas.product import ProductBase, ProductRead


async def product_create(data: ProductBase, db: AsyncSession) -> ProductRead:
    """
    Создает новый продукт.
    """
    item = Product(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ProductRead.model_validate(item, from_attributes=True)


async def product_update(product_id: int, data: ProductBase, db: AsyncSession) -> ProductRead:
    """
    Обновляет продукт по его id.
    Если продукт не существует, возвращает ошибку 404.
    """
    query = select(Product).where(Product.id == product_id)
    response = await db.execute(query)
    item = response.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)

    return ProductRead.model_validate(item, from_attributes=True)


async def product_read(product_id: int, db: AsyncSession) -> ProductRead:
    """
    Возвращает продукт по его id.
    Если продукт не существует, возвращает ошибку 404.
    """
    query = select(Product).where(Product.id == product_id)
    response = await db.execute(query)
    item = response.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    return ProductRead.model_validate(item, from_attributes=True)


async def product_list(db: AsyncSession) -> List[ProductRead]:
    """
    Возвращает список всех продуктов.
    """
    query = select(Product).where(Product.is_active).order_by(Product.created_at.desc())
    response = await db.execute(query)
    items = response.scalars().all()
    result = [ProductRead.model_validate(el, from_attributes=True) for el in items]

    return result


async def product_delete(product_id: int, db: AsyncSession):
    """
    Удаляет продукт по его id.
    Если продукт не существует, возвращает ошибку 404.
    """
    stmt = delete(Product).where(Product.id == product_id)
    response = await db.execute(stmt)
    deleted_count = response.rowcount
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    return JSONResponse(status_code=200, content={"message": "Продукт успешно удалён"})
