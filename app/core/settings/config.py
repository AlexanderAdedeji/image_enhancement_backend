import os
from typing import Any
from pydantic import BaseSettings
from pathlib import Path



class AppSettings(BaseSettings):
    APP_NAME:str
    DEVELOPMENT_DATABASE_URL:str
    PRODUCTION_DATABASE_URL:str
    DEBUG:bool
    REJECTED:str
    EDITED:str
    GOOD:str
    MULTI_GOOD:str
    API_URL_PREFIX:str
    SECRET_KEY: str
    ALLOWED_HOSTS:Any
    JWT_EXPIRE_MINUTES: int
    RESET_TOKEN_EXPIRE_MINUTES:int
    JWT_TOKEN_PREFIX: str
    JWT_ALGORITHM: str

    ADMIN_USER_TYPE:str = "ADMIN"
    REVIEWER_USER_TYPE:str = "REVIEWER"
    EDITOR_USER_TYPE:str = "EDITOR"
    SUPERUSER_TYPE:str = "SUPERUSER"
    HEADER_KEY:str

    class Config:
        env_file =os.getenv(
            "ENV_VARIABLE_PATH", Path(__file__).parent / "env_files/.env"
        )
    