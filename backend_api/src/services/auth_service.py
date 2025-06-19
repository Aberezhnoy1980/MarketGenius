from datetime import datetime, timezone, timedelta
from typing import Union

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from src.repositories.users import UsersRepository
from src.config import settings
from src.users_db import async_session_maker


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    TRIAL_ATTEMPTS = 3

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return AuthService.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return AuthService.pwd_context.hash(password)

    def create_access_token(self, user_data: dict) -> str:
        to_encode = user_data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode["exp"] = expire
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_exp": True},
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Токен истёк")
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail=f"Неверный токен: {str(e)}")

    @staticmethod
    def check_subscription(subscription_expiry: Union[str, datetime, None]) -> bool:
        if not subscription_expiry:
            return False
        try:
            expiry_date = (
                datetime.fromisoformat(subscription_expiry)
                if isinstance(subscription_expiry, str)
                else subscription_expiry
            )
            return expiry_date > datetime.now(timezone.utc)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def check_trial(trial_attempts: int) -> bool:
        """Проверяет, остались ли trial-попытки."""
        return trial_attempts > 0

    @staticmethod
    async def decrement_trial_attempts(
            user_id: int
    ) -> None:
        """Уменьшает количество trial-попыток в БД."""
        async with async_session_maker() as session:
            repo = UsersRepository(session)
            user = await repo.get_one_or_none(id=user_id)
            if user and user.trial_attempts > 0:
                await repo.decrement_trial_attempts(user_id)
                await session.commit()

    @staticmethod
    async def get_user(user_id: int):
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user

    @staticmethod
    def create_password_reset_token(email: str) -> str:
        """Генерация JWT для сброса пароля (живёт 1 час)"""
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
        return jwt.encode(
            {"email": email, "exp": expire, "sub": "password_reset"},
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def verify_password_reset_token(token: str) -> str:
        """Верификация токена сброса пароля"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"require_sub": "password_reset"}
            )
            return payload["email"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Ссылка сброса истекла")
        except jwt.PyJWTError:
            raise HTTPException(status_code=400, detail="Неверная ссылка сброса")