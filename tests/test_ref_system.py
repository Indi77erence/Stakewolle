
from http import HTTPStatus
import urllib.parse

import httpx
from httpx import AsyncClient

from src.config import CSRFTOKEN, MY_COOKIES
from tests.conftest import get_ref_code
from tests.data_for_test import data_for_create_user, field_user, data_for_login, data_for_create_user_by_ref_code


async def test_create_user(ac: AsyncClient):
	response = await ac.post('/api/v1/create_user', json=data_for_create_user)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in field_user:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_login(ac: AsyncClient):
	data_encoded = urllib.parse.urlencode(data_for_login)
	headers = {
		"Content-Type": "application/x-www-form-urlencoded"
	}
	response = await ac.post('/api/v1/auth/login', data=data_encoded, headers=headers)
	assert response.status_code == HTTPStatus.NO_CONTENT, "Статус ответа не 204."


async def test_create_ref_code(ac: AsyncClient):
	cookies = httpx.Cookies({"csrftoken": CSRFTOKEN,
							 "my_cookies": MY_COOKIES})
	response = await ac.post('/api/v1/referral_code', params={"length": 10}, cookies=cookies)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	assert "id" in answer_response, "Отсутствует поле 'id' в ответе."
	assert "code" in answer_response, "Отсутствует поле 'code' в ответе."
	assert "registered_code" in answer_response, "Отсутствует поле 'registered_code' в ответе."
	assert "expiry_date" in answer_response, "Отсутствует поле 'expiry_date' в ответе."
	assert "user_id" in answer_response, "Отсутствует поле 'user_id' в ответе."


async def test_create_user_by_ref(ac: AsyncClient):
	rez = await get_ref_code()
	data_for_create_user_by_ref_code["ref_code"] = rez
	response = await ac.post('/api/v1/create_user_by_ref_code/{ref_code}', json=data_for_create_user_by_ref_code)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in field_user:
		assert field in answer_response, f"В меню нет поля {field}."
