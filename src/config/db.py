import re
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr


from config.settings import settings

engine = create_async_engine(settings.db.url)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех моделей"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Задает имя таблицы в БД."""
        table_name = cls.__name__ + "s"
        table_name = re.sub(r"(?<!^)(?=[A-Z])", "_", table_name)
        return table_name.lower()
