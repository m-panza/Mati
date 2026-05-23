from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://sigrav:sigrav123@db:5432/sigrav"
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    uploads_dir: str = "/app/uploads"
    cors_origins: List[str] = ["http://localhost:5173"]
    app_base_url: str = "http://localhost:8000"
    qr_base_url: str = "https://sigrav.app/q"

    class Config:
        env_file = ".env"


settings = Settings()
