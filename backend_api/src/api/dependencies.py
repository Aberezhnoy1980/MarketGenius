from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.repositories.users import UsersRepository
from src.services.auth_service import AuthService
from src.users_db import async_session_maker

security = HTTPBearer()


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Токен не предоставлен")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


async def get_current_user(request: Request) -> dict:
    """Зависимость для проверки JWT и подписки."""
    token = request.cookies.get("mg_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Требуется авторизация")

    try:
        user_data = AuthService().decode_token(token)

        # Проверяем, что пользователь существует в БД
        user = await AuthService.get_user(user_data["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

            # Проверяем подписку или trial-попытки
            # if not (AuthService.check_subscription(user.subscription_expiry_date) or
            #         AuthService.check_trial(user.trial_attempts)):
            #     raise HTTPException(status_code=403, detail="Нет доступа")

        return user_data  # Возвращаем данные из токена

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")


UserDep = Annotated[dict, Depends(get_current_user)]


async def check_access(user_data: UserDep):
    """Проверяет подписку/trial попытки"""
    user = await AuthService.get_user(user_data["user_id"])

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if AuthService.check_subscription(user.subscription_expiry_date):
        return {"user": user, "access_type": "subscription"}

    if AuthService.check_trial(user.trial_attempts):
        return {"user": user, "access_type": "trial"}

    raise HTTPException(status_code=403, detail="Нет доступа")


AccessDep = Annotated[dict, Depends(check_access)]
