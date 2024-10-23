from datetime import datetime
from typing import Optional
from pydantic import BaseModel, PositiveInt


class ProductBase(BaseModel):
    name: str
    price: PositiveInt
    is_active: Optional[bool] = True


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
