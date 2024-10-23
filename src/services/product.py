from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from schemas.product import ProductBase, ProductRead


async def product_create(product: ProductBase, db: AsyncSession) -> ProductRead:
    item = Product(**product.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ProductRead.model_validate(item, from_attributes=True)


async def product_list(db: AsyncSession) -> List[ProductRead]:
    stmt = select(Product).where(Product.is_active)
    result = await db.execute(stmt)
    result = result.scalars().all()
    return result
