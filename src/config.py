import os
from functools import lru_cache
from logging import getLogger
from logging.config import dictConfig
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings
from pydantic.networks import AnyUrl


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    TESTING: bool = False
    SERVER_URL: AnyUrl = "http://127.0.0.1:8000"
    ORIGINS: Optional[str] = "*"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    settings_file = {"development": ".env.dev", "testing": ".env.test", "production": ".env.prod"}
    return Settings(_env_file=settings_file[os.environ.get("ENVIRONMENT", "development")], _env_file_encoding="utf-8")


settings = get_settings()

Path(f"{Path(__file__).parent.parent.resolve()}/logs/api.log").touch()


class LoggerSettings(BaseSettings):
    LOGGER_NAME: str = "API_LOGGER"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_FORMAT_COMPREHENSIVE: str = (
        "%(levelprefix)s | %(asctime)s | %(funcName)s() | L%(lineno)-4d | %(message)s | "
        "call_trace=%(pathname)s L%(lineno)-4d "
    )
    LOG_LEVEL: str = "DEBUG"

    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {"()": "uvicorn.logging.DefaultFormatter", "fmt": LOG_FORMAT, "datefmt": "%Y-%m-%d %H:%M:%S"},
        "comprehensive": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT_COMPREHENSIVE,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {"formatter": "default", "class": "logging.StreamHandler", "stream": "ext://sys.stderr"},
        "comprehensive": {"formatter": "comprehensive", "class": "logging.StreamHandler", "stream": "ext://sys.stderr"},
        "file": {
            "formatter": "comprehensive",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": f"{Path(__file__).parent.parent.resolve()}/logs/api.log",
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 4,
        },
    }
    loggers = {LOGGER_NAME: {"handlers": ["file"], "level": LOG_LEVEL}}


@lru_cache()
def get_logger_settings() -> BaseSettings:
    return LoggerSettings()


dictConfig(get_logger_settings().dict())
logger = getLogger("API_LOGGER")
