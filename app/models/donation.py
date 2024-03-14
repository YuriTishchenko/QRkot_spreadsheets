from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CharityDonation


class Donation(CharityDonation):
    """Модель для донатов"""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
