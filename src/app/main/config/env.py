from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.main.config.settings import AppSettings, PostgresSettings, SqlaSettings

_BASE_DIR: Final[Path] = Path(__file__).resolve().parents[4]
_ENV_FILE: Final[Path] = _BASE_DIR.joinpath(".env")
_BASE_SETTINGS_DICT: Final[SettingsConfigDict] = SettingsConfigDict(
    env_file=_ENV_FILE, env_file_encoding="utf-8", extra="ignore"
)


class AppEnvSettings(BaseSettings, AppSettings):
    model_config = _BASE_SETTINGS_DICT | SettingsConfigDict(env_prefix="APP_")


class PostgresEnvSettings(BaseSettings, PostgresSettings):
    model_config = _BASE_SETTINGS_DICT | SettingsConfigDict(env_prefix="POSTGRES_")


class SqlaEnvSettings(BaseSettings, SqlaSettings):
    model_config = _BASE_SETTINGS_DICT | SettingsConfigDict(env_prefix="SQLA_")
