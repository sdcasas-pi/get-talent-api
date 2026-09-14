from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# .../src/backend/app/infrastructure/config/settings.py -> .../src
_PROJECT_ROOT = Path(__file__).resolve().parents[4]
_DEFAULT_SQLITE_PATH = _PROJECT_ROOT / "data" / "db" / "students.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = Field(default="student-registration-service")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    database_url: str = Field(
        default=f"sqlite+aiosqlite:///{_DEFAULT_SQLITE_PATH}",
        description="Async SQLAlchemy database URL",
    )
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"],
        description="Allowed CORS origins",
    )
