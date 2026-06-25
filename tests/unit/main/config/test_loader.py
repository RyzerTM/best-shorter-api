import pytest

from app.main.config.loader import (
    load_app_env_settings,
    load_postgres_env_settings,
    load_sqla_env_settings,
)
from app.main.config.logging_ import LoggingLevel


@pytest.mark.parametrize(
    "logging_level",
    [
        LoggingLevel.DEBUG,
        LoggingLevel.INFO,
        LoggingLevel.WARNING,
        LoggingLevel.ERROR,
        LoggingLevel.CRITICAL,
    ],
)
def test_load_app_env_settings_reads_app_prefixed_env_variables(
    monkeypatch: pytest.MonkeyPatch,
    logging_level: LoggingLevel,
) -> None:
    monkeypatch.setenv("APP_SERVICE_NAME", "test-service")
    monkeypatch.setenv("APP_SERVICE_VERSION", "prod")
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("APP_LOGGING_LEVEL", logging_level)
    monkeypatch.setenv("APP_ROOT_PATH", "test-path")

    sut = load_app_env_settings()

    assert sut.service_name == "test-service"
    assert sut.service_version == "prod"
    assert sut.debug is True
    assert sut.logging_level == logging_level
    assert sut.root_path == "test-path"


def test_load_postgres_env_settings_reads_postgres_prefixed_env_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("POSTGRES_DB", "best_shorter")
    monkeypatch.setenv("POSTGRES_HOST", "postgres")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_USER", "app")
    monkeypatch.setenv("POSTGRES_PASSWORD", "secret")

    sut = load_postgres_env_settings()

    assert sut.db == "best_shorter"
    assert sut.host == "postgres"
    assert sut.port == 5432
    assert sut.user == "app"
    assert sut.password == "secret"
    assert sut.dsn == "postgresql+asyncpg://app:secret@postgres:5432/best_shorter"


def test_load_sqla_env_settings_reads_sqla_prefixed_env_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SQLA_ECHO", "true")
    monkeypatch.setenv("SQLA_ECHO_POOL", "true")
    monkeypatch.setenv("SQLA_POOL_SIZE", "20")
    monkeypatch.setenv("SQLA_MAX_OVERFLOW", "30")

    sut = load_sqla_env_settings()

    assert sut.echo is True
    assert sut.echo_pool is True
    assert sut.pool_size == 20
    assert sut.max_overflow == 30


def test_load_sqla_env_settings_uses_defaults() -> None:
    sut = load_sqla_env_settings()

    assert sut.echo is False
    assert sut.echo_pool is False
    assert sut.pool_size == 15
    assert sut.max_overflow == 10
