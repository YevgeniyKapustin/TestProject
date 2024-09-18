from typing import Any

import requests
from aiogram_dialog import Data, DialogManager
from requests import Response
from sqlalchemy import select

from config import settings
from database import get_db
from models.user import User


def add_user(data: Data, result: Any, manager: DialogManager):
    username = data.get('username')
    password = data.get('password')
    user_id = data.get('user_id')
    register(username, password)
    tokens: dict = get_access_tokens(username, password).json()
    with get_db as session:
        session.add(
            User(
                id=user_id,
                access_token=tokens.get('access'),
                refresh_token=tokens.get('refresh')
            )
        )


def register(username: str, password: str) -> Response:
    return requests.post(
        f'{settings.TODO_BACKEND_URL}/api/v1/user/',
        body={
            'username': username,
            'password': password
        }
    )


def get_access_tokens(username: str, password: str):
    return requests.post(
        f'{settings.TODO_BACKEND_URL}/api/v1/token/',
        headers={
            'username': username,
            'password': password
        }
    )


def get_new_access_token(refresh_token: str, user_id: int) -> int:
    response = requests.post(
        f'{settings.TODO_BACKEND_URL}/api/v1/token/refresh/',
        data={
            'refresh': refresh_token,
        }
    )
    access_token = response.json().get('access')
    with get_db as session:
        user = session.execute((
            select(User).
            where(User.id == user_id)
        )).scalars().all()
        user.refresh_token = access_token

        session.add(user)

    return access_token


def verify_access_token(access_token: str) -> bool:
    response = requests.post(
        f'{settings.TODO_BACKEND_URL}/api/v1/token/verify/',
        data={
            'access': access_token,
        }
    )
    return True if response.status_code == 200 else False
