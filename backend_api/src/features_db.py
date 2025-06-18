from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

feature_engine = create_async_engine(settings.FEATURES_DB_URL, echo=True)

feature_async_session_maker = async_sessionmaker(bind=feature_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
