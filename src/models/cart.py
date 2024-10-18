from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base


class Cart(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="cart")

    products: Mapped[list["CartProduct"]] = relationship("CartProduct", back_populates="cart")


# Создать объект корзины, который будет содержать список товаров.
# Реализовать методы для добавления товаров в корзину (одного или нескольких), удаления товаров из корзины и полной очистки корзины.
# Реализовать метод для получения общей стоимости товаров в корзине.
