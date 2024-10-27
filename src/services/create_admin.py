import asyncio
import getpass

from fastapi import HTTPException

from pydantic import ValidationError
from config.db import async_session_maker
from schemas.users import CreateUser
from services.users import create_user

from models.cart_product import CartProduct  # noqa # pylint:disable=unused-import
from models.cart import Cart  # noqa # pylint:disable=unused-import
from models.product import Product  # noqa # pylint:disable=unused-import


async def create_admin():
    """
    Создает администратора.
    """

    print("\nСоздание администратора.\n")

    default_name = getpass.getuser()
    default_email = "admin@admin.ru"
    default_phone = "+70000000000"

    email = input(f"Введите email (по умолчанию {default_email}): ")
    first_name = input(f"Введите имя (по умолчанию {default_name}): ")
    last_name = input(f"Введите фамилию (по умолчанию {default_name}): ")
    phone = input(f"Введите телефон (по умолчанию {default_phone}): ")
    password1 = getpass.getpass("Введите пароль: ")
    password2 = getpass.getpass("Повторите пароль: ")

    if not email:
        email = default_email
    if not first_name:
        first_name = default_name
    if not last_name:
        last_name = default_name
    if not phone:
        phone = default_phone

    try:
        user = CreateUser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password1=password1,
            password2=password2,
        )
    except ValidationError as e:
        print("\nПри создании администратора произошли ошибки:")
        for err in e.errors():
            print(f"- {err['msg']}")
        return

    async with async_session_maker() as db:
        try:
            created_user = await create_user(user, db, is_admin=True)
        except HTTPException as e:
            print("\nПри создании администратора произошли ошибки:")
            print(f"- {e.detail}")
        else:
            print("\nАдминистратор создан.")
            print(f"Email: {created_user.email}")
            print(f"Имя: {created_user.first_name} {created_user.last_name}")


if __name__ == "__main__":
    asyncio.run(create_admin())
