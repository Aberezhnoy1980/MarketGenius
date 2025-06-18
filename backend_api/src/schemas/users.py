from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserRequestAdd(BaseModel):
    login: str = Field(description="Уникальный псевдоним в качестве логина")
    email: str = Field(description="Адрес электронной почты")
    password: str = Field(description="Сырой пароль")


class UserAdd(BaseModel):
    login: str = Field(description="Уникальный псевдоним в качестве логина")
    email: str = Field(description="Адрес электронной почты")
    hashed_password: str = Field(description="Хэшированный пароль")
    email_verified: bool = False


class User(BaseModel):
    id: int = Field(description="Идентификатор пользователя")
    login: str = Field(description="Уникальный псевдоним в качестве логина")
    email: str = Field(description="Адрес электронной почты")
    subscription_expiry_date: datetime = Field(description="Время истечения подписки")
    email_verified: bool = False
    trial_attempts: int = Field(description="Количество гостевых запросов")

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str = Field(description="Хэшированный пароль")


class UserResponse(BaseModel):
    status: str = "success"
    user: dict  # Или отдельная модель User


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str


class UserLoginRequest(BaseModel):
    login: str
    password: str


class UserRegisterRequest(UserLoginRequest):
    email: str  # Добавляем email только для регистрации
