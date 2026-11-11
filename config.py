from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI SaaS Boilerplate"
    APP_VERSION: str = "0.1.0"
    APP_ENV: Literal["local", "staging", "production"] = "local"
    APP_DEBUG: bool = True
    APP_KEY: str = "super-secret-key-change-in-production"

    APP_HOST: str = "localhost"
    APP_PORT: int = 8000

    ALLOWED_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # Split Database Environment Variables
    DB_CONNECTION: str = "postgresql+asyncpg"
    DB_HOST: str = "localhost"
    DB_PORT: int = Field(default=5432, ge=1, le=65535)
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: SecretStr

    @property
    def database_url(self) -> str:
        return (
            f"{self.DB_CONNECTION}://{self.DB_USERNAME}:{self.DB_PASSWORD.get_secret_value()}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        )

    # Split Redis Environment Variables
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = Field(default=6379, ge=1, le=65535)
    REDIS_PASSWORD: SecretStr
    REDIS_DB: int = 0

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD.get_secret_value()}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Security & JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
