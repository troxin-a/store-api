from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base

uniq_str_an = Annotated[str, mapped_column(unique=True)]


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[uniq_str_an]
    phone: Mapped[uniq_str_an]
    password: Mapped[str]

    cart: Mapped["Cart"] = relationship(uselist=False, back_populates="user", lazy="joined")

    ## TODO Подтверждение пароля в схеме
