import os
from typing import List

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """
    API_V1_STR: str = os.getenv('API_V1_STR')
    DB_URL: str = os.getenv('DB_URL')
    DBBaseModel: any = declarative_base()

    JWT_SECRET: str = os.getenv('JWT_SECRET')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings = Settings()
