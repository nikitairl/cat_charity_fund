from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    validate_invested_on_delete,
    validate_charity_is_closed,
    validate_charity_new_and_old_amount,
    validate_for_duplicate,
    validate_project_exists,
    validate_charity_delete_if_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_projects import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.charity_projects import investment_when_create

router = APIRouter()


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary="Получить весь список проектов",
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на получение всех проектов"""
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    dependencies=[Depends(current_superuser)],
    summary="Создание благотворительного проекта",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_charity_project(
    charity_obj: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await validate_for_duplicate(charity_obj.name, session)
    new_charity_obj = await charity_project_crud.create(charity_obj, session)
    await investment_when_create(session)
    await session.commit()
    await session.refresh(new_charity_obj)
    return new_charity_obj


@router.delete(
    "/{project_id}",
    summary="Удаление благотворительного проекта",
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
)
async def remove_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    charity_obj = await validate_project_exists(charity_id=project_id, session=session)
    await validate_charity_delete_if_invested(charity_obj)
    await validate_invested_on_delete(charity_obj)
    return await charity_project_crud.remove(charity_obj, session)


@router.patch(
    "/{project_id}",
    dependencies=[Depends(current_superuser)],
    summary="Редактировать благотворительный проект",
    response_model=CharityProjectDB,
)
async def update_charity_project(
    project_id: int,
    new_charity_obj: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_obj = await validate_project_exists(charity_id=project_id, session=session)
    await validate_for_duplicate(new_charity_obj.name, session)
    await validate_charity_new_and_old_amount(charity_obj, new_charity_obj.full_amount)
    await validate_charity_is_closed(charity_obj)

    new_charity_obj = await charity_project_crud.update(
        charity_obj, new_charity_obj, session
    )
    return new_charity_obj
