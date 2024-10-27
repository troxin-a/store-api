from typing import Annotated
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base


uniq_str_an = Annotated[str, mapped_column(unique=True)]


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[uniq_str_an]
    phone: Mapped[uniq_str_an]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("'false'"))
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text("'false'"))

    cart: Mapped["Cart"] = relationship(uselist=False, back_populates="user", lazy="joined")
