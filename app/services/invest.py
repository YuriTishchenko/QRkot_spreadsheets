from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from app.models import CharityProject, Donation


async def get_last_obj(
    model,
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    """получить последний обьект"""
    db_obj = await session.execute(select(model).where(
        model.fully_invested.is_(False)
    ).order_by('create_date'))
    return db_obj.scalars().first()


async def modify_obj(obj) -> None:
    """Переключить статус проекта на завершенный"""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def invest_project(
    obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """Выделение инвестиций для проектов"""
    charity_project = await get_last_obj(CharityProject, session)
    donation = await get_last_obj(Donation, session)
    if not charity_project or not donation:
        await session.commit()
        await session.refresh(obj)
        return obj
    tail_project = charity_project.full_amount - charity_project.invested_amount
    tail_donation = donation.full_amount - donation.invested_amount
    if tail_project > tail_donation:
        charity_project.invested_amount += tail_donation
        donation.invested_amount += tail_donation
        await modify_obj(donation)
    if tail_project == tail_donation:
        charity_project.invested_amount += tail_donation
        donation.invested_amount += tail_donation
        await modify_obj(donation)
        await modify_obj(charity_project)
    if tail_project < tail_donation:
        charity_project.invested_amount += tail_project
        donation.invested_amount += tail_project
        await modify_obj(charity_project)
    session.add(charity_project)
    session.add(donation)
    await session.commit()
    await session.refresh(charity_project)
    await session.refresh(donation)
