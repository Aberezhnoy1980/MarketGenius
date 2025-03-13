from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr = Field(description="Электронная почта пользователя. Используется в том числе в качестве логина")
    password: str = Field(description="Сырой пароль")


class UserAdd(BaseModel):
    email: EmailStr = Field(description="Электронная почта пользователя. Используется в том числе в качестве логина")
    hashed_password: str = Field(description="Хэшированный пароль")


class User(BaseModel):
    id: int = Field(description="Идентификатор пользователя")
    email: EmailStr = Field(description="Электронная почта пользователя. Используется в том числе в качестве логина")

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str = Field(description="Хэшированный пароль")
