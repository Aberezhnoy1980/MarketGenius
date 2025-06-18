from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException
from src.config import settings

from fastapi_mail import FastMail, MessageSchema
from src.email_config import conf


class EmailService:
    @staticmethod
    def create_email_token(email: str) -> str:
        """Генерация JWT для подтверждения email"""
        payload = {
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "sub": "email_verification"  # Добавляем тип токена
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def verify_email_token(token: str) -> str:
        """Верификация токена подтверждения email"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"require_sub": "email_verification"}  # Проверяем тип
            )
            return payload["email"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=400,
                detail="Ссылка подтверждения истекла"
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=400,
                detail="Неверная ссылка подтверждения"
            )

    @staticmethod
    async def send_verification_email(email: str, token: str):
        verification_url = f"https://market-genius/auth/verify-email?token={token}"

        message = MessageSchema(
            subject="Подтверждение email для MarketGenius",
            recipients=[email],
            body=f"""
            Добро пожаловать в MarketGenius!

            Для завершения регистрации перейдите по ссылке:
            {verification_url}

            Ссылка действительна 24 часа.
            """,
            subtype="plain"
        )

        fm = FastMail(conf)
        try:
            await fm.send_message(message)
            print(f"Письмо отправлено на {email}")  # Для дебага
        except Exception as e:
            print(f"Ошибка отправки: {e}")

    @staticmethod
    async def send_password_reset_email(email: str, token: str):
        reset_url = f"https://market-genius.ru/auth/reset-password?token={token}"

        message = MessageSchema(
            subject="Сброс пароля в MarketGenius",
            recipients=[email],
            body=f"""
            Для сброса пароля перейдите по ссылке:
            {reset_url}

            Ссылка действительна 1 час.
            """,
            subtype="html"
        )
        await FastMail(conf).send_message(message)
