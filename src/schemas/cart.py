from typing import List, Union
from pydantic import BaseModel, PositiveInt

from schemas.product import ProductReadCart


class CartProductCreate(BaseModel):
    product_id: int
    quantity: Union[PositiveInt, None] = 1


class CartProductRead(BaseModel):
    quantity: PositiveInt
    product: ProductReadCart


class CartRead(BaseModel):
    total_cost: int
    cart: List[CartProductRead]


class CartChange(BaseModel):
    message: str = "Товар удален из корзины"
    total_cost: int
    cart: List[CartProductRead]


class CartChangeQuantity(BaseModel):
    message: str = "Количество товара в корзине обновлено"
    total_cost: int
    cart_item: CartProductRead
