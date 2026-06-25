from pydantic_settings import BaseSettings

from app.main.config.env import AppEnvSettings, PostgresEnvSettings, SqlaEnvSettings
from app.main.config.settings import AppSettings, PostgresSettings, SqlaSettings


def _load_env[E: BaseSettings](env_cls: type[E]) -> E:
    return env_cls()


def load_app_env_settings() -> AppSettings:
    return _load_env(AppEnvSettings)


def load_postgres_env_settings() -> PostgresSettings:
    return _load_env(PostgresEnvSettings)


def load_sqla_env_settings() -> SqlaSettings:
    return _load_env(SqlaEnvSettings)
