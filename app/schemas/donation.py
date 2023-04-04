from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt


class DonationPartDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: Optional[int]

    class Config:
        orm_mode = True

class DonationFullResponse(DonationPartDB):
    invested_amount: Optional[int]
    fully_invested: Optional[bool]

class DonationFullDB(DonationFullResponse):
    close_date: Optional[datetime]