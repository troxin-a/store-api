from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.cart import Cart
from models.cart_product import CartProduct
from models.users import User
from schemas.cart_product import CartProductSchema
from schemas.product import ProductRead
from services.product import product_read


async def create_cart(user: User, db: AsyncSession):
    cart = Cart(user_id=user.id)
    db.add(cart)
    await db.commit()


def search_product_in_cart(cart, product_id):
    """
    Поиск товара в корзине.
    Если товар найден, возвращает его индекс в коризне.
    """
    for index, product in enumerate(cart.products):
        if product.product_id == product_id:
            return index
    return -1


async def add_product_to_cart(
    cart_product: CartProductSchema, user: User, db: AsyncSession
) -> List[CartProductSchema]:
    """
    Добавляет товар в корзину.
    """
    cart: Cart = user.cart

    await product_read(user, cart_product.product_id, db)

    product_index_in_cart = search_product_in_cart(cart, cart_product.product_id)
    if product_index_in_cart != -1:
        cart.products[product_index_in_cart].quantity += cart_product.quantity
    else:
        cart_product_dump = cart_product.model_dump()
        cart_product_dump["cart_id"] = cart.id
        entry_cart_product = CartProduct(**cart_product_dump)
        db.add(entry_cart_product)

    await db.commit()
    await db.refresh(cart)
    return cart.products


async def get_cart(user: User, db: AsyncSession) -> List[ProductRead]:
    """
    Получение списка товаров из корзины.
    """
    cart: Cart = user.cart
    return cart.products
