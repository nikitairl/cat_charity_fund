from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BasedModel


class Donation(BasedModel):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)

    def __repr__(self) -> str:
        return (
            f"Donation(full_amount={self.full_amount}, "
            f"invested_amount={self.invested_amount})"
        )

    def __str__(self) -> str:
        return (
            f"Сумма пожертвования: {self.full_amount}, "
            f"Пожертвовано их этой суммы: {self.invested_amount} "
        )