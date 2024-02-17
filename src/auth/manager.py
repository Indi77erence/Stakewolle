from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from ..auth.models import User
from src.auth.service import get_user_db
from src.config import SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
	reset_password_token_secret = SECRET
	verification_token_secret = SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
	yield UserManager(user_db)
