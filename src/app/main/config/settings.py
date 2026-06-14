from typing import Literal

from pydantic import BaseModel

from app.main.config.logging_ import LoggingLevel


class AppSettings(BaseModel):
    service_name: str = "Best-Shorter"
    service_version: Literal["prod", "dev"] = "dev"
    debug: bool = False
    logging_level: LoggingLevel = LoggingLevel.INFO
    root_path: str = "/"
