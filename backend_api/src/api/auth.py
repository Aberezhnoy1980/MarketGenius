from fastapi import APIRouter, Body, HTTPException, Response
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.utils.openapi_examples import user_examples

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    description="<h3>Добавляет запись данных пользователя в базу данных</h3>"
)
async def register_user(
        data: UserRequestAdd = Body(openapi_examples=user_examples),
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except IntegrityError:
            return {"status": "The email already exists"}

        return {"status": "OK"}


@router.post(
    "/login",
    summary="Вход пользователя в систему",
    description="Сверяет переданные пользователем логин и пароль с данными в базе данных"
)
async def login_user(
        response: Response,
        data: UserRequestAdd = Body(openapi_examples=user_examples),
):
    async with async_session_maker() as session:
        try:
            user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        except NoResultFound:
            raise HTTPException(status_code=401, detail=f"Пользователь с {data.email} не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неправильный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"status": "Login successfully", "access_token": access_token}


@router.post(
    "/logout",
    summary="Выход пользователя из системы",
    description="Удаляет токен из cookies клиента"
)
async def logout(
        response: Response
):
    response.delete_cookie("access_token")
    return {"status": "Logout successfully"}


@router.get(
    "/me",
    summary="Получение данных текущего пользователя",
    description="Возвращает данные текущего пользователя"
)
async def get_me(
        user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)

    return {"user": user}
