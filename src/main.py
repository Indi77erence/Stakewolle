from fastapi import FastAPI

from src.auth.baseconfig import fastapi_users, auth_backend
from src.app.ref_system.router import router as refferal_system_router
from src.app.user.router import router as user_router


def create_app():
	app = FastAPI(title='Referral System APP')
	app.include_router(user_router, prefix="/api/v1")
	app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/api/v1/auth", tags=["auth"])
	app.include_router(refferal_system_router, prefix="/api/v1")

	return app
