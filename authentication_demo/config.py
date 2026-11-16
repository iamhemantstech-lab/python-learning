# Environment configuration
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory pointing to the authentication_demo folder
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    # Database connection string loaded from .env (with fallback)
    DATABASE_URL: str = "mysql+pymysql://root:root123@localhost:3306/authentication_db"

    # JWT Security Settings
    SECRET_KEY: str = "dTmD3lb2ooG2jz3L6dG34W2kbIwP1rm0"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3


    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
