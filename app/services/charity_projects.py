# app/services/investment_projects.py
from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession as session

from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation


def closing(db_obj: Union[Donation, CharityProject]) -> None:
    if db_obj.invested_amount == db_obj.full_amount:
        db_obj.fully_invested = True
        db_obj.close_date = datetime.now()

async def investment_when_create(session: session) -> None:
    projects = await charity_project_crud.get_not_closed(session)
    donations = await donation_crud.get_not_closed(session)
    project_index, projects_len = 0, len(projects)
    donation_index, donations_len = 0, len(donations)

    changed_objs = set()

    while donation_index < donations_len and project_index < projects_len:
        project = projects[project_index]
        donation = donations[donation_index]

        project_free_amount = project.full_amount - project.invested_amount
        donation_free_amount = donation.full_amount - donation.invested_amount

        if donation_free_amount >= project_free_amount:
            donation.invested_amount += project_free_amount
            project.invested_amount += project_free_amount

            closing(project)
            closing(donation)

            project_index += 1

            if donation.fully_invested:
                donation_index += 1

        else:
            donation.invested_amount += donation_free_amount
            project.invested_amount += donation_free_amount

            closing(donation)

            donation_index += 1

        changed_objs.update({project, donation})

    session.add_all(changed_objs)
    await session.commit()