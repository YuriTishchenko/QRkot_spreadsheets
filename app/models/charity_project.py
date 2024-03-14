from sqlalchemy import Column, String, Text

from app.models.base import CharityDonation


class CharityProject(CharityDonation):
    """Модель для целевых проектов"""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
