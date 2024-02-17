from typing import Optional
from fastapi_users import schemas
from pydantic import EmailStr


class UserCreate(schemas.BaseUserCreate):
	username: str
	email: EmailStr
	password: str
	is_active: Optional[bool] = True
	is_superuser: Optional[bool] = False
	is_verified: Optional[bool] = False


class UserRead(schemas.BaseUser[int]):
	id: int | None
	email: EmailStr | None
	username: str | None
	register_ref_code: str | None
	is_active: bool = True
	is_superuser: bool = False
	is_verified: bool = False


class UserCreateByRef(UserCreate):
	register_ref_code: str | None
