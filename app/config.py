import os
from functools import lru_cache

from pydantic_settings import BaseSettings

from app.common.enums import LoggingLevel
from app.common.logging import logging


def fall_back_and_warn_if_none(env_name: str, default):
    value = os.environ.get(env_name)
    if value is None:
        logging.warning(f"{env_name} env is missing will fall back to {default}")
        value = default
    return default


class BaseConfig(BaseSettings):
    production: bool = False
    testing: bool = False
    ENVIRONMENT: str = "default"
    default_allow_origins: list[str] = ["*"]
    APP_NAME: str = "tam-api"
    ALLOWED_HOSTS: list[str] = ["*"]
    # timezone
    APP_TZ: str = "Asia/Riyadh"

    FORWARDED_ALLOW_IPS: str = "*"
    CELERY_RESULT_BACKEND: str | None = None
    CELERY_BROKER_URL: str | None = None
    ENABLE_CELERY_RETRY: bool = True
    ENABLE_CELERY_RETRY_BACKOFF: bool = True
    CELERY_RETRY_MAX: int = 10
    CELERY_RETRY_BACKOFF_MAX: int = 3600
    CELERY_ENABLE_RESULT_BACKEND: bool = False

    REDIS_HOST: str | None = None
    REDIS_PORT: int | None = None
    REDIS_DB: int | None = None
    REDIS_CASHING_TTL: int = 3600
    REDIS_LOCAL_CASHING_TTL: int = 2
    REDIS_LOCAL_CASH_SIZE_LIMIT: int = 1000
    REDIS_TIMEOUT: int = 500
    REDIS_CONNECTION_POOL_SIZE: int = 20
    REDIS_SOCKET_KEEPALIVE: bool = True


    FEATURE_FLAG_LOCAL_CACHING_TTL: int = 5
    FEATURE_FLAG_LOCAL_CASH_SIZE_LIMIT: int = 100


    @property
    def allow_hosts(self):
        if os.environ.get("ALLOWED_HOSTS") is None:
            return self.default_allow_origins
        else:
            return os.environ.get("ALLOWED_HOSTS").split(",")

    @property
    def allow_core_origins(self):
        if os.environ.get("ALLOWED_CORS_ORIGINS") is None:
            return self.default_allow_origins
        else:
            return os.environ.get("ALLOWED_CORS_ORIGINS").split(",")

    openapi_url: str | None = "/openapi.json"
    docs_url: str = "/docs"


    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    READ_ONLY_DB_USER: str | None = None
    READ_ONLY_DB_PASSWORD: str | None = None
    READ_ONLY_DB_NAME: str | None = None
    READ_ONLY_DB_HOST: str | None = None
    READ_ONLY_DB_PORT: int | None = None

    # TODO will be removed it just for dev.
    SECRET_KEY: str | None = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
    ALGORITHM: str  | None = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ENABLE_CASHING: bool = True
    LOGGING_LEVEL: LoggingLevel = LoggingLevel.INFO
    RELEASE_SHA: str = "unknown"

    SMTP_SENDER: str | None = None
    SMTP_SENDERNAME: str = ""
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_HOST: str | None= None
    SMTP_TIMEOUT: float = 60
    SMTP_PORT: int = 587
    SMTP_ENCRYPTION: bool = False

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SQLALCHEMY_READ_DATABASE_URL(self) -> str:
        if self.READ_ONLY_DB_USER is not None:
            user = self.READ_ONLY_DB_USER
            password = self.READ_ONLY_DB_PASSWORD
            host = self.READ_ONLY_DB_HOST
            port = self.READ_ONLY_DB_PORT
            name = self.READ_ONLY_DB_NAME
            return f"postgresql://{user}:{password}@{host}:{port}/{name}"
        else:
            return self.SQLALCHEMY_DATABASE_URL

    SQL_POOL_SIZE: int = 40
    SQL_POOL_OVERFLOW_SIZE: int = 10
    SQL_POOL_ENABLED: bool = True

    LECTURE_START: int = 32
    LECTURE_END: int = 95
    SLOT_TIME: int = 15

    class Config:
        env_file = ".env"


# you can set the defaults from here or over ride all using .env


class ProductionConfig(BaseConfig):
    production: bool = True
    testing: bool = False
    ENVIRONMENT: str = "prod"
    openapi_url: str | None = None


class StagingConfig(BaseConfig):
    production: bool = True
    testing: bool = False
    ENVIRONMENT: str = "staging"
    LOGGING_LEVEL: LoggingLevel = LoggingLevel.DEBUG


class TestingConfig(BaseConfig):
    production: bool = False
    testing: bool = True
    ENVIRONMENT: str = "testing"
    SQL_POOL_ENABLED: bool = False


@lru_cache
def current_config(ProductionConfig, StagingConfig, TestingConfig, BaseConfig):
    """
    this will load the required config passed on STAGE env if not set it will load LocalConfig
    """
    stage = os.environ.get("ENVIRONMENT", "local")
    logging.info(f"loading {stage} Config...")

    if stage == "prod":
        config = ProductionConfig()
    elif stage == "staging":
        config = StagingConfig()
    elif stage == "testing":
        config = TestingConfig()
    elif stage == "local":
        config = BaseConfig()
    else:
        raise Exception(f"ENVIRONMENT: {stage} is not supported")

    return config


config: BaseConfig = current_config(
    ProductionConfig,
    StagingConfig,
    TestingConfig,
    BaseConfig,
)
