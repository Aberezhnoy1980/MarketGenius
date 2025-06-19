import asyncio

import jwt
from fastapi import APIRouter, Body, HTTPException, Response
from fastapi import BackgroundTasks
from fastapi import Request

from src.schemas.response_model import AuthCheckResponse
from src.services.email_service import EmailService
from src.users_db import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRegisterRequest, UserLoginRequest
from src.services.auth_service import AuthService
from src.utils.openapi_examples import user_examples
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    description="<h3>Добавляет запись данных пользователя в базу данных</h3>",
)
async def register(
        user_data: UserRegisterRequest,
        background_tasks: BackgroundTasks
):
    """
    Регистрация нового пользователя
    - Сохраняет пользователя с email_verified=False
    - Генерирует токен подтверждения
    - Отправляет письмо со ссылкой для подтверждения
    """

    # Нормализация email
    email = user_data.email.strip().lower()

    async with async_session_maker() as session:
        # Проверка уникальности
        if await UsersRepository(session).email_exists(email):
            raise HTTPException(status_code=409, detail="Email уже занят")
        if await UsersRepository(session).login_exists(user_data.login):
            raise HTTPException(status_code=409, detail="Логин уже занят")

        # Хешируем только пароль
        hashed_password = AuthService().hash_password(user_data.password)

        # Сохраняем пользователя (email хранится как есть)
        new_user = UserAdd(
            login=user_data.login,
            email=email,
            hashed_password=hashed_password,
            email_verified=False
        )

        await UsersRepository(session).add(new_user)
        await session.commit()

    # 3. Генерируем токен подтверждения
    verify_token = EmailService().create_email_token(user_data.email)

    # 4. Отправляем письмо
    background_tasks.add_task(
        EmailService.send_verification_email,
        user_data.email,
        verify_token  # Отправляем токен, а не хеш
    )

    return {"status": "ok", "message": "Письмо с подтверждением отправлено"}


@router.get("/verify-email")
async def verify_email(token: str):
    """
    Подтверждение email по токену
    - Проверяет токен
    - Обновляет email_verified=True в БД
    """
    email = EmailService.verify_email_token(token)

    async with async_session_maker() as session:
        await UsersRepository(session).verify_email(email)
        await session.commit()

    return {"status": "ok", "message": "Email подтверждён"}


@router.post(
    "/login",
    summary="Вход пользователя в систему",
    description="Сверяет переданные пользователем логин и пароль с данными в базе данных"
)
async def login_user(
        response: Response,
        data: UserLoginRequest = Body(..., openapi_examples=user_examples),
):
    async with async_session_maker() as session:
        try:
            user = await UsersRepository(session).get_user_with_hashed_password(login=data.login)
            if not user:
                await asyncio.sleep(0.5)
                raise HTTPException(
                    status_code=401,
                    detail="Неверный логин или пароль",
                )

            # 2. Проверяем пароль
            if not AuthService().verify_password(data.password, user.hashed_password):
                await asyncio.sleep(0.5)
                raise HTTPException(status_code=401, detail="Неверный логин или пароль")

            # 3. Проверяем подтверждение email (если требуется)
            # if not user.email_verified:
            #     raise HTTPException(
            #         status_code=403,
            #         detail="Подтвердите email для входа",
            #     )

            # 4. Генерируем токен с полными данными пользователя
            access_token = AuthService().create_access_token({
                "user_id": user.id,
                "login": user.login,
                "email": user.email,
                "email_verified": user.email_verified,
                "subscription_expiry": str(user.subscription_expiry_date) if user.subscription_expiry_date else None,
                "trial_attempts": user.trial_attempts,
            })

            # 5. Устанавливаем cookie
            response.set_cookie(
                "mg_access_token",
                access_token,
                httponly=True,
                secure=True,  # Для HTTPS
                samesite="lax",
                max_age=30 * 60,  # 30 минут (как в JWT)
            )

            return {
                "status": "success",
                "user": {
                    "id": user.id,
                    "login": user.login,
                    "email": user.email,
                    "email_verified": user.email_verified,
                },
            }
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            await session.close()


@router.post(
    "/logout",
    summary="Выход пользователя из системы",
    description="Удаляет JWT из cookies и возвращает статус"
)
async def logout(response: Response):
    response.delete_cookie(
        "mg_access_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {
        "status": "success",
        "message": "Сессия завершена",
        "actions": ["clear_local_storage"]  # Указание фронтенду на дополнительные действия
    }


@router.get(
    "/check-auth",
    summary="Проверка авторизации",
    description="Проверяет валидность JWT и возвращает данные пользователя",
    response_model=AuthCheckResponse,
)
async def check_auth(request: Request):
    token = request.cookies.get("mg_access_token")
    if not token:
        return {"authenticated": False, "user": None}

    try:
        # Декодируем токен
        user_data = AuthService().decode_token(token)

        # Проверяем, существует ли пользователь в БД (опционально)
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_one_or_none(id=user_data["user_id"])
            if not user:
                return {"authenticated": False, "user": None}

        return {
            "authenticated": True,
            "user": {
                "id": user_data["user_id"],
                "login": user_data["login"],
                "email": user_data.get("email"),
                "email_verified": user_data.get("email_verified", False),
                "subscription_active": AuthService.check_subscription(
                    user_data.get("subscription_expiry")
                ),
            },
        }
    except (jwt.ExpiredSignatureError, jwt.PyJWTError, HTTPException):
        return {"authenticated": False}


@router.post("/password-reset/request")
async def request_password_reset(
        background_tasks: BackgroundTasks,
        email: str = Body(..., embed=True),
):
    """Запрос на сброс пароля (отправка письма)"""
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_by_email(email)
        if not user:
            return {"status": "ok"}

        reset_token = AuthService.create_password_reset_token(user.email)
        background_tasks.add_task(
            EmailService.send_password_reset_email,
            user.email,
            reset_token
        )
    return {"status": "ok"}


@router.post("/password-reset/confirm")
async def confirm_password_reset(
        token: str = Body(..., embed=True),
        new_password: str = Body(..., min_length=8, embed=True)
):
    """Подтверждение сброса пароля"""
    try:
        email = AuthService.verify_password_reset_token(token)
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            hashed_password = AuthService.hash_password(new_password)
            await UsersRepository(session).update_password(user.id, hashed_password)
            await session.commit()

        return {"status": "ok"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Ссылка устарела")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Неверный токен")
