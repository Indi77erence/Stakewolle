import fastapi_users
import requests
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.ref_system.service import has_active_referral_code
from src.app.user.schemas import UserCreate
from src.config import KEYHUNTER


async def check_email(email: str):
    """
    Функция, которая проверяет валидность email при помощи сервиса "emailhunter".

    Принимает 1 аргумент:
    - email - email пользователя, который хочет зарегистрироваться.

    Возвращает валидность email адреса.
    """
    api_key = KEYHUNTER
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    if "errors" in data:
        return False
    result = data['data']['status']
    if result == "valid":
        return True
    return False


async def add_user_by_ref_code(ref_code: str, new_user_data: UserCreate, session: AsyncSession, user_manager):
    """
    Функция, которая регистрирует нового пользователя в системе через реферальный код.

    Принимает 3 аргумента:
    - session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
    - new_user_data - схема fastapi_users для валидации введенных данных пользователем при регистрации.
    - user_manager - объект fastapi_users для управления пользователями

    Функция возвращает данные зарегистрированного пользователя.
    """
    new_user_data.register_ref_code = ref_code
    if await has_active_referral_code(ref_code=ref_code, session=session):
        try:
            new_user = await user_manager.create(new_user_data)
            return new_user
        except fastapi_users.exceptions.UserAlreadyExists:
            return {"error": "Пользователь уже существует"}
    return {"error": "Данный реферальный код недействителен"}


async def create_user(new_user_data: UserCreate, user_manager):
    """
    Функция, которая регистрирует нового пользователя в системе.

    Принимает 2 аргумента:
    - new_user_data - схема fastapi_users для валидации введенных данных пользователем при регистрации.
    - user_manager - объект fastapi_users для управления пользователями.

    Функция возвращает данные зарегистрированного пользователя.
    """
    try:
        new_user = await user_manager.create(new_user_data)
        return new_user
    except fastapi_users.exceptions.UserAlreadyExists:
        return {"error": "Пользователь уже существует"}
