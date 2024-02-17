from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Boolean
from src.database import metadata, Base

user = Table(
	"user",
	metadata,
	Column("id", Integer, primary_key=True),
	Column("email", String, nullable=False),
	Column("username", String, nullable=False),
	Column("registered_at", TIMESTAMP, default=datetime.utcnow),
	Column("hashed_password", String, nullable=False),
	Column("register_ref_code", String, nullable=True, default=None),
	Column("is_active", Boolean, default=True, nullable=False),
	Column("is_superuser", Boolean, default=False, nullable=False),
	Column("is_verified", Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
	# __tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=False)
	username = Column(String, nullable=False, default='username')
	registered_at = Column(TIMESTAMP, default=datetime.utcnow)
	register_ref_code = Column(String, default=None)
	hashed_password: str = Column(String(length=1024), unique=True, nullable=False)
	is_active: bool = Column(Boolean, default=True, nullable=False)
	is_superuser: str = Column(Boolean, default=False, nullable=False)
	is_verified: str = Column(Boolean, default=False, nullable=False)
