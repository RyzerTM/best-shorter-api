from pydantic_settings import BaseSettings

from app.main.config.env import AppEnvSettings
from app.main.config.settings import AppSettings


def _load_env[E: BaseSettings](env_cls: type[E]) -> E:
    return env_cls()


def load_app_env_settings() -> AppSettings:
    return _load_env(AppEnvSettings)
