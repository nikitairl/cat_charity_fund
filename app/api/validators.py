from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


async def validate_for_duplicate(charity_name: str, session: AsyncSession) -> None:
    charity_id = await charity_project_crud.get_id_by_name(
        charity_name=charity_name, session=session
    )
    if charity_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def validate_invested_on_delete(
    charity_obj: CharityProject,
) -> None:
    if charity_obj.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=("В проект были внесены средства, не подлежит удалению!"),
        )


async def validate_project_exists(
    charity_id: int, session: AsyncSession
) -> CharityProject:
    charity_obj = await charity_project_crud.get(obj_id=charity_id, session=session)
    if charity_obj is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Проект не найден")
    return charity_obj


async def validate_charity_is_closed(
    charity_obj: CharityProject,
) -> None:
    if charity_obj.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )


async def validate_charity_delete_if_invested(
    charity_obj: CharityProject,
) -> None:
    if charity_obj.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def validate_charity_new_and_old_amount(
    charity_obj: CharityProject, new_amount: int
) -> None:
    if new_amount is not None:
        if new_amount < charity_obj.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=("Уже внесено больше чем устанавливаемый минимум."),
            )
