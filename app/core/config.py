from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "QRCats - все для котиков!"
    app_description: str = (
        "Фонд помощи котикам. Помогаем собирать деньги на благотворительные проекты."
    )
    app_version: str = "1.0.0"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret_key: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()