from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationPartDB, DonationFullResponse
from app.services.charity_projects import investment_when_create

router = APIRouter()


@router.get(
    "/",
    summary="Получить список всех пожертвований",
    dependencies=[Depends(current_superuser)],
    response_model=List[DonationFullResponse],
)
async def get_all_donations_for_superuser(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    summary="Получить список всех пожертвований пользователя",
    dependencies=[Depends(current_user)],
    response_model=List[DonationPartDB],
    response_model_exclude={"user_id"},
)
async def get_donations_for_current_user(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_by_user(user, session)


@router.post(
    "/",
    summary="Сделать пожертвование",
    dependencies=[Depends(current_user)],
    response_model=DonationPartDB,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donation_obj = await donation_crud.create(donation, session, user)
    await investment_when_create(session)
    await session.commit()
    await session.refresh(donation_obj)
    return donation_obj