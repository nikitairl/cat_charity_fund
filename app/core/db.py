from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()  # noqa

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

# Асинхронная функц. для доступа к БД
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


# Открытие доступа с помощью контекстного менеджера и yield
async def get_async_session():
    async with AsyncSessionLocal() as async_session:  # noqa
        yield async_session
