from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_SSL_TLS: bool
    MAIL_STARTTLS: bool

    class Config:
        env_file = ".env"
        extra = "ignore"  # Игнорировать лишние переменные


conf = ConnectionConfig(**EmailSettings().model_dump())
