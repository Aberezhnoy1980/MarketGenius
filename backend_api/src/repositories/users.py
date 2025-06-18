from pydantic import EmailStr
from sqlalchemy import select, exists, update

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, login: str):
        query = select(self.model).filter_by(login=login)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if not model:
            return None

        return UserWithHashedPassword.model_validate(model, from_attributes=True)

    async def verify_email(self, email: str):
        """Обновляет статус подтверждения email"""
        stmt = (
            update(self.model)
            .where(self.model.email == email)
            .values(email_verified=True)
        )
        await self.session.execute(stmt)

    async def email_exists(self, email: str) -> bool:
        query = select(exists().where(self.model.email == email))
        return (await self.session.execute(query)).scalar()

    async def login_exists(self, login: str) -> bool:
        query = select(exists().where(self.model.login == login))
        return (await self.session.execute(query)).scalar()

    async def decrement_trial_attempts(self, user_id: int) -> None:
        """Атомарное уменьшение trial_attempts"""
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(trial_attempts=self.model.trial_attempts - 1)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)

    async def get_by_email(self, email: str):
        """Поиск пользователя по email (возвращает ORM-объект)"""
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_password(self, user_id: int, new_hashed_password: str) -> None:
        """Обновление пароля в БД"""
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(hashed_password=new_hashed_password)
        )
        await self.session.execute(stmt)
