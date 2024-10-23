from typing import Union
from pydantic import BaseModel, PositiveInt


class CartProductSchema(BaseModel):
    product_id: int
    quantity: Union[PositiveInt, None] = 1
