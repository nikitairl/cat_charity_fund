from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class BasedModel(Base):

    __abstract__ = True

    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    # Для записи разных значений даты и времени мы передаем не вызов функции,
    # а саму функцию (datetime.now)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None, nullable=True)