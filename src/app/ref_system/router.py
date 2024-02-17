from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.ref_system.schemas import ReferralCode
from src.app.ref_system.service import create_refferal_code, delete_refferal_code, \
	get_refferal_code_by_email, get_info_ref
from src.app.user.schemas import UserRead
from src.database import get_async_session

# Роутер для управления реферальными данными.
router = APIRouter(
	# prefix='/referral_code',
	tags=['ReferralCode']
)


# Роутер для получения реферального кода по email адресу реферера.
@router.get('/referral_code_by_email')
async def get_ref_code_by_email(answer=Depends(get_refferal_code_by_email)):
	return answer


# Роутер для создания реферального кода пользователем.
@router.post('/referral_code', response_model=ReferralCode, status_code=status.HTTP_201_CREATED)
async def create_ref_code(answer=Depends(create_refferal_code)):
	return answer


# Роутер для удаления реферального кода пользователем.
@router.delete('/referral_code')
async def delete_ref_code(answer=Depends(delete_refferal_code)):
	return answer


# Роутер для получения информации о рефералах по id реферера.
@router.post('/referral_code/{id_ref}', response_model=list[UserRead])
async def get_info_ref_by_id(id_ref: int, session: AsyncSession = Depends(get_async_session)):
	answer = await get_info_ref(id_ref, session=session)
	return answer
