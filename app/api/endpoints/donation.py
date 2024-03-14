from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import User, Donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationUser,
)
from app.services.invest import invest_project


router = APIRouter()


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> Donation:
    """создать донат"""

    new_donation = await donation_crud.create(donation, session, user)
    await invest_project(new_donation, session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUser],
    response_model_exclude={'user_id'},
)
async def get_my_reservations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> list[Donation]:
    """Получить список всех донатов для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_donations(
        session: AsyncSession = Depends(get_async_session),
) -> list[Donation]:
    """Получить все донаты"""
    donations = await donation_crud.get_multi(session)
    return donations
