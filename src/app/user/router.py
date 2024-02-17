from typing import Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.app.ref_system.schemas import ErrorRegisterCode
from src.app.user.service import check_email, add_user_by_ref_code, create_user
from src.auth.manager import get_user_manager
from src.app.user.schemas import UserRead, UserCreate, UserCreateByRef
from src.database import get_async_session

# Роутер для управления пользователями
router = APIRouter(
	tags=['User']
)


# Роутер для создания пользователя.
@router.post('/create_user', response_model=Union[UserRead, ErrorRegisterCode], status_code=status.HTTP_201_CREATED)
async def create_new_user(new_user_data: UserCreate, user_manager=Depends(get_user_manager)):
	if await check_email(new_user_data.email):
		answer = await create_user(new_user_data=new_user_data, user_manager=user_manager)
		return answer
	return {"error": "Email не валидный"}


# Роутер для создания пользователя через реферальный код.
@router.post('/create_user_by_ref_code/{ref_code}', response_model=Union[UserRead, ErrorRegisterCode])
async def create_user_by_ref_code(ref_code: str, new_user_data: UserCreateByRef, user_manager=Depends(get_user_manager),
							   session: AsyncSession = Depends(get_async_session)):
	if await check_email(new_user_data.email):
		answer = await add_user_by_ref_code(ref_code=ref_code,
											new_user_data=new_user_data,
											session=session,
											user_manager=user_manager)
		return answer
	return {"error": "Email не валидный"}
