from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base


class Cart(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="cart")
    products: Mapped[List["CartProduct"]] = relationship("CartProduct", back_populates="cart", lazy="joined")

    def get_total_cost(self):
        return sum([product.quantity * product.product.price for product in self.products])
