
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    """Проверка дубликата имени проекта"""
    charity_project = await charity_project_crud.get_project_id_by_name(name, session)
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка на наличие проекта"""
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_invested_amount(
        charity_project: CharityProject,
) -> None:
    """Проверка на наличие вложенных средств"""
    money = charity_project.invested_amount
    if money > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def compare_invested_amount_full_amount(
        charity_project: CharityProject,
        new_amount: int,
) -> CharityProject:
    """Сравнение уже вложенных средств и требуемых"""
    money = charity_project.invested_amount
    if money > new_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Уже вложенно в проект {money}, нельзя назначить меньше '
        )
    return charity_project


async def check_fully_invested(
    charity_project: CharityProject,
) -> None:
    """Проверка закрыт ли проект"""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
