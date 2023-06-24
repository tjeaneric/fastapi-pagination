from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    db_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
