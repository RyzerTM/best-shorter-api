from typing import Literal

from pydantic import BaseModel, PostgresDsn

from app.main.config.logging_ import LoggingLevel


class AppSettings(BaseModel):
    service_name: str = "Best-Shorter"
    service_version: Literal["prod", "dev"] = "dev"
    debug: bool = False
    logging_level: LoggingLevel = LoggingLevel.INFO
    root_path: str = "/"


class PostgresSettings(BaseModel):
    db: str
    host: str
    port: int
    user: str
    password: str

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db,
            )
        )


class SqlaSettings(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 15
    max_overflow: int = 10
