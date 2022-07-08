from typing import Optional
from pydantic import BaseSettings, PostgresDsn, validator


class EnvSettings(BaseSettings):
    """Main settings"""
    # Token data
    SECRET_KEY: str = "most secret key ever"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Database settings
    DATABASE_USERNAME: Optional[str] = 'postgres'
    DATABASE_PASSWORD: Optional[str] = 'postgres'
    DATABASE_HOST: Optional[str] = 'localhost'
    DATABASE_PORT: Optional[int] = 5432
    DATABASE_NAME: Optional[str] = 'lego'
    DB_URI: Optional[PostgresDsn] = None

    @validator("DB_URI", pre=True)
    def validate_db_url(cls, v,  values):
        if isinstance(v, str):
            return v

        path = values.get("DATABASE_NAME", "")
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DATABASE_USERNAME"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=str(values.get("DATABASE_PORT")),
            path=f"/{path}",
        )


settings = EnvSettings()
