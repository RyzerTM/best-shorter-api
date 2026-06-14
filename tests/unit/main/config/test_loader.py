import pytest

from app.main.config.loader import load_app_env_settings
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
