from datetime import datetime
from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import Mapped, mapped_column
from config.db import Base


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=text("'false'"),
    )
