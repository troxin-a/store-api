from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base


class CartProduct(Base):
    """Ассоциативная таблица, связывающая товары и корзины (ManyToMany)."""

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"), primary_key=True)
    cart: Mapped["Cart"] = relationship(back_populates="products")

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    product: Mapped["Product"] = relationship("Product", lazy="joined", uselist=False)

    quantity: Mapped[int] = mapped_column(default=1)
