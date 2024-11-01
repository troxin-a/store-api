from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, PositiveInt


class ProductBase(BaseModel):
    name: str
    price: PositiveInt
    is_active: Union[bool, None] = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ProductPatch(ProductBase):
    name: Optional[str] = None
    price: Optional[PositiveInt] = None
    is_active: Optional[bool] = None


class ProductReadCart(ProductBase):
    id: int
