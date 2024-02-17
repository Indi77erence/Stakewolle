import datetime

from pydantic import BaseModel


class ReferralCode(BaseModel):
	id: int
	code: str
	registered_code: datetime.datetime
	expiry_date: datetime.datetime
	user_id: int


class ErrorRegisterCode(BaseModel):
	error: str
