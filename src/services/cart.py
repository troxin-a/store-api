from typing import List
from fastapi import HTTPException
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.cart import Cart
from models.cart_product import CartProduct
from models.users import User
from schemas.cart import CartChange, CartChangeQuantity, CartProductCreate, CartProductRead, CartRead
from schemas.product import ProductReadCart
from services.product import product_read


def search_product_in_cart(cart, product_id):
    """
    Поиск товара в корзине.
    Если товар найден, возвращает его индекс в коризне.
    """
    for index, product in enumerate(cart.products):
        if product.product_id == product_id:
            return index
    return -1


def get_cart_item(product, quantity):
    product = ProductReadCart.model_validate(product, from_attributes=True)
    return CartProductRead(product=product, quantity=quantity)


async def create_cart(user: User, db: AsyncSession):
    cart = Cart(user_id=user.id)
    db.add(cart)
    await db.commit()


async def get_cart_product(cart_id: int, product_id: int, db) -> CartProduct:
    """
    Поиск записи товара в связанной таблице корзины.
    """

    query = select(CartProduct).where(
        and_(
            CartProduct.cart_id == cart_id,
            CartProduct.product_id == product_id,
        )
    )
    response = await db.execute(query)
    cart_product = response.scalars().first()
    if not cart_product:
        raise HTTPException(status_code=404, detail="Товар в корзине не найден")

    return cart_product


async def add_cart_product(cart_product: CartProductCreate, user: User, db: AsyncSession) -> List[CartProductCreate]:
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
    return await get_cart(user)


async def delete_cart_product(product_id: int, user: User, db: AsyncSession) -> CartChange:
    """
    Удаляет товар из корзины.
    """

    stmt = delete(CartProduct).where(
        and_(
            CartProduct.cart_id == user.cart.id,
            CartProduct.product_id == product_id,
        )
    )
    response = await db.execute(stmt)
    deleted_count = response.rowcount
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Товар в корзине не найден")

    await db.commit()
    await db.refresh(user)
    cart = await get_cart(user)
    cart = [cart_item.model_dump() for cart_item in cart.cart]
    return CartChange(
        message="Товар удален из корзины",
        cart=cart,
        total_cost=user.cart.get_total_cost(),
    )


async def delete_all_cart_products(user: User, db: AsyncSession) -> CartChange:
    """
    Удаляет все товары из корзины.
    """

    stmt = delete(CartProduct).where(CartProduct.cart_id == user.cart.id)
    await db.execute(stmt)
    await db.commit()
    await db.refresh(user)

    cart = await get_cart(user)
    cart = cart.model_dump()
    cart["message"] = "Корзина очищена"

    return CartChange(**cart)


async def add_quantity_cart_product(product_id: int, user: User, db: AsyncSession):
    """
    Добавить единицу товара в корзине.
    """

    cart_item = await get_cart_product(user.cart.id, product_id, db)
    cart_item.quantity += 1
    await db.commit()
    await db.refresh(cart_item)

    return CartChangeQuantity(
        message="Количество товара в корзине обновлено",
        cart_item=get_cart_item(cart_item.product, cart_item.quantity),
        total_cost=user.cart.get_total_cost(),
    )


async def sub_quantity_cart_product(product_id: int, user: User, db: AsyncSession):
    """
    Отнять единицу товара в корзине.
    """

    cart_item = await get_cart_product(user.cart.id, product_id, db)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        return await delete_cart_product(product_id, user, db)

    await db.commit()
    await db.refresh(cart_item)

    return CartChangeQuantity(
        message="Количество товара в корзине обновлено",
        cart_item=get_cart_item(cart_item.product, cart_item.quantity),
        total_cost=user.cart.get_total_cost(),
    )


async def get_cart(user: User) -> CartRead:
    """
    Получение списка товаров из корзины.
    """

    products = user.cart.products
    cart_items = [get_cart_item(item.product, item.quantity) for item in products]
    total_cost = user.cart.get_total_cost()

    return CartRead(total_cost=total_cost, cart=cart_items)
