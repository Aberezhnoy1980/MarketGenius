from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings

# Testing
sync_users_engine = create_engine(settings.SYNC_USERS_DB_URL, echo=True)
sync_features_engine = create_engine(settings.SYNC_FEATURES_DB_URL, echo=True)

sync_users_session_maker = sessionmaker(bind=sync_users_engine, expire_on_commit=False)
sync_features_session_maker = sessionmaker(bind=sync_features_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
