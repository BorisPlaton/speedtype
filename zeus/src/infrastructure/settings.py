import tomllib
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ZeusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ZEUS_")

    ROOT_DIR: Path = Path(__file__).parent.parent.absolute()
    APP_NAME: str = "Zeus"
    LOG_LEVEL: str = "INFO"
    PORT: int = 8080
    DEBUG: bool = False

    @computed_field
    @property
    def VERSION(self) -> str:  # noqa: N802
        pyproject_path = self.ROOT_DIR.parent / "pyproject.toml"
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]


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
    @property
    def URI(self) -> str:  # noqa: N802
        return f"mongodb://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE_NAME}?authSource={self.AUTH_SOURCE}"


class Settings(BaseSettings):
    zeus: ZeusSettings = ZeusSettings()
    mongodb: MongoDBSettings = MongoDBSettings()
