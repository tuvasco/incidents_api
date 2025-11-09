from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: str = "sqlite:///./incidents.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
