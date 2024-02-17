from datetime import datetime, timedelta
import random
import string
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.ref_system.models import referral_code
from src.auth.models import user as user_tbl
from src.app.ref_system.schemas import ReferralCode
from src.auth.baseconfig import current_user
from src.auth.models import User
from src.app.user.schemas import UserRead
from src.database import get_async_session


async def has_active_referral_code(session: AsyncSession, user_id: int = None, ref_code: str = None):
	"""
	Функция, которая проверяет, является ли реферальный код пользователя действительным.

	Принимает 2 аргумента:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- user_id - id пользователя, чей реферальный код будет проверен.
	- ref_code - реферальный код, который будет проверен.

	Функция возвращает состояние проверки.
	"""
	stmt_id = select(referral_code.c.expiry_date).where(referral_code.c.user_id == user_id)
	stmt_ref_code = select(referral_code.c.expiry_date).where(referral_code.c.code == ref_code)
	if user_id:
		result_stmt = await session.execute(stmt_id)
		for date in result_stmt.fetchall():
			if date[0] > datetime.utcnow():
				return True
	if ref_code:
		result_stmt = await session.execute(stmt_ref_code)
		if result_stmt.fetchone()[0] > datetime.utcnow():
			return True
	return False


async def generate_referral_code(length: int = 10):
	"""
	Функция генерации реферального кода.

	Принимает 1 необязательный аргумент аргумента:
	- length - жедлаемая длинна реферального кода.

	Функция возвращает созданный реферальный код.
	"""
	letters_and_digits = string.ascii_letters + string.digits
	ref_code = ''.join(random.choice(letters_and_digits) for _ in range(length))
	return ref_code


async def generate_expiry_date(expiry_date: Optional[datetime] = None):
	"""
	Функция, задаёт срок действия реферального кода.

	Принимает 1 необязательный аргумент:
	- expiry_date - желаемый срок действия кода, либо по умолчанию равен 1 месяцу.

	Функция возвращает срок действия реферального кода.
	"""
	if expiry_date is not None:  # Если значение пустое или None, используйте текущую дату и время
		return expiry_date
	expiry_date = datetime.utcnow() + timedelta(days=30)
	return expiry_date


async def get_refferal_code_by_email(email: str, session: AsyncSession = Depends(get_async_session)):
	"""
	Функция для получения реферального кода по email адресу реферера.

	Принимает 2 аргумента:
	- email - email реферера, чей реферальный код необходимо получить.
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.

	Функция реферальный код пользователя.
	"""
	stmt = select(referral_code.c.code).where(user_tbl.c.email == email,
											  referral_code.c.expiry_date > datetime.utcnow()).join(referral_code)
	rez_query = await session.execute(stmt)
	result = rez_query.fetchone()
	if not result:
		return {"detail": f"У данного пользователя нет действующего реферального кода"}
	return {"ref_code": f"{result[0]}"}


async def create_refferal_code(expiry_date: datetime = Depends(generate_expiry_date),
							   session: AsyncSession = Depends(get_async_session),
							   user: User = Depends(current_user),
							   ref_code: str = Depends(generate_referral_code)):
	"""
	Функция для создания реферального кода пользователем.

	Принимает 4 аргумента:
	- expiry_date - срок действия кода, либо по умолчанию равен 1 месяцу.
	- user - пользователь, кто создает реферальный код.
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- ref_code - сгенерированный реферальный код.

	Функция возвращает данные реферального кода.
	"""
	if await has_active_referral_code(session=session, user_id=user.id):
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
							detail="У вас уже существует действующий реферальный код")
	stmt = insert(referral_code).values(code=ref_code,
										user_id=user.id,
										expiry_date=expiry_date).returning(referral_code)
	rez_query = await session.execute(stmt)
	result = rez_query.fetchone()
	if not result:
		raise HTTPException(status_code=403, detail="Доступ запрещен")
	await session.commit()
	info = ReferralCode(id=result.id, code=result.code, registered_code=result.registered_code,
						expiry_date=result.expiry_date, user_id=result.user_id)
	return info


async def delete_refferal_code(del_code: str,
							   session: AsyncSession = Depends(get_async_session),
							   user: User = Depends(current_user)):
	"""
	Функция для удаления реферального кода пользователем.

	Принимает 3 аргумента:
	- del_code - реферальный код, который необходимо удалить.
	- user - пользователь, который хочет удалить свой реферальный код.
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.

	Функция возвращает состояние удаления.
	"""
	stmt = delete(referral_code).where(referral_code.c.code == del_code, referral_code.c.user_id == user.id)
	result = await session.execute(stmt)
	if result.rowcount:
		await session.commit()
		return {"status": "Код удален"}
	return {"status": "У вас нет данного реферального кода"}


async def get_info_ref(id_ref: int, session: AsyncSession):
	"""
	Функция для получения информации о рефералах по id реферера.

	Принимает 2 аргумента:
	- id_ref - id пользователя, о рефералах которого запрашивается информация.
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.

	Функция возвращает список рефералов пользователя.
	"""
	stmt = select(user_tbl).join(referral_code, referral_code.c.user_id == id_ref).where(
		user_tbl.c.register_ref_code == referral_code.c.code)
	result = await session.execute(stmt)
	info = [UserRead(id=res.id, email=res.email, username=res.username, register_ref_code=res.register_ref_code)
			for res in result]
	return info
