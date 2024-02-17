from datetime import datetime, timedelta

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey

from src.database import metadata

referral_code = Table(
	"referral_code",
	metadata,
	Column("id", Integer, primary_key=True),
	Column("code", String, nullable=False, unique=True),
	Column("registered_code", TIMESTAMP, default=datetime.utcnow),
	Column("expiry_date", TIMESTAMP, default=datetime.utcnow() + timedelta(days=30), nullable=False),
	Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE")),
)
