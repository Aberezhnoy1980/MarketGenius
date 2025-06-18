from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    USERS_DB_HOST: str
    FEATURES_DB_HOST: str
    USERS_DB_PORT: int
    FEATURES_DB_PORT: int
    DB_USER: str
    DB_PASS: str
    FEATURES_DB_NAME: str
    USERS_DB_NAME: str

    @property
    def USERS_DB_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.USERS_DB_HOST}:{self.USERS_DB_PORT}/{self.USERS_DB_NAME}")

    @property
    def SYNC_USERS_DB_URL(self):
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.USERS_DB_HOST}:{self.USERS_DB_PORT}/{self.USERS_DB_NAME}")

    @property
    def FEATURES_DB_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.FEATURES_DB_HOST}:{self.FEATURES_DB_PORT}/{self.FEATURES_DB_NAME}")

    @property
    def SYNC_FEATURES_DB_URL(self):
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.FEATURES_DB_HOST}:{self.FEATURES_DB_PORT}/{self.FEATURES_DB_NAME}")

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # extra='ignore' при неиспользуемых переменных


settings = Settings()
