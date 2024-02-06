import os

from pydantic_settings import BaseSettings, SettingsConfigDict


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_file_path = os.path.join(root_dir, ".env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    JWT_SECRET_KEY: str

    ADMIN_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: str

    EMAIL_VERIFIER_API_KEY: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=env_file_path)


settings = Settings()
