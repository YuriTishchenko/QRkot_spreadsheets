from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """получение id проекта по имени"""
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        project_id = project_id.scalars().first()
        return project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> List[CharityProject]:
        """список со всеми закрытыми проектами по количеству времени, которое понадобилось на сбор средств"""
        charity_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested.is_(True))
        )
        charity_projects = charity_projects.scalars().all()
        for charity_project in charity_projects:
            create_date = charity_project.create_date
            close_date = charity_project.close_date
            days_to_complete = (
                close_date.day - create_date.day +
                (close_date.month - create_date.month) * 30 +
                (close_date.year - create_date.year) * 365
            )
            charity_project.days_to_complete = days_to_complete
        sorted_projects = sorted(charity_projects, key=lambda x: x.days_to_complete)
        return sorted_projects


charity_project_crud = CRUDCharityProject(CharityProject)