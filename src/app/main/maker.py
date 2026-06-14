from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.main.config.loader import load_app_env_settings
from app.main.config.settings import AppSettings
from app.main.setup import setup_logging


def make_lifespan() -> Callable[[FastAPI], AbstractAsyncContextManager]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        # https://dishka.readthedocs.io/en/stable/integrations/fastapi.html
        container = app.state.dishka_container
        try:
            yield
        finally:
            await container.close()

    return lifespan


def make_app(app_settings: AppSettings | None = None) -> FastAPI:
    if app_settings is None:
        app_settings = load_app_env_settings()

    setup_logging(level=app_settings.logging_level)

    app = FastAPI(
        debug=app_settings.debug,
        title=app_settings.service_name,
        version=app_settings.service_version,
        summary=f"OpenAPI schema for {app_settings.service_name}",
    )

    return app
