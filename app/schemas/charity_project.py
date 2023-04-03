from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    @validator("name", "description")
    def check_for_valid_input(cls, value: str) -> str:
        if not value or value is None:
            raise ValueError("Поля не могут быть пустыми")
        return value


class CharityProjectUpdate(CharityProjectBase):
    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]

    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
