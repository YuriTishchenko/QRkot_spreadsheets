from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """базовая схема донатов"""
    comment: Optional[str]
    full_amount: PositiveInt


class DonationCreate(DonationBase):
    """схема создания доната"""
    pass


class DonationUser(DonationBase):
    """схема донатов для юзера"""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationUser):
    """Схема DB донатов"""
    user_id: int
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
