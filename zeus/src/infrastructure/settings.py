from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ZeusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ZEUS_")

    ROOT_DIR: str = str(Path(__file__).parent.parent.absolute())
    APP_NAME: str = "Zeus"
    LOG_LEVEL: str = "INFO"
    PORT: int = 8080
    DEBUG: bool = False


class MongoDBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MONGO_")

    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    DATABASE_NAME: str
    TIMEOUT: int = 5_000
    AUTH_SOURCE: str = "admin"

    @computed_field
    def uri(self) -> str:
        return f"mongodb://{self.HOST}:{self.PORT}/{self.DATABASE_NAME}"


class Settings(BaseSettings):
    zeus: ZeusSettings = ZeusSettings()
    mongodb: MongoDBSettings = MongoDBSettings()
