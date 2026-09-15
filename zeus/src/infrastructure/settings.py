import tomllib
from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from infrastructure.secret_manager.base import SecretManager


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
    secret_manager: SecretManager = Field(exclude=True)

    HOST: str
    PORT: int
    DATABASE_NAME: str
    TIMEOUT: int = 5_000
    AUTH_SOURCE: str = "admin"

    @computed_field
    @property
    def URI(self) -> str:  # noqa: N802
        return (
            f"mongodb://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/"
            f"{self.DATABASE_NAME}?authSource={self.AUTH_SOURCE}"
        )

    @computed_field
    @property
    def PASSWORD(self) -> str:  # noqa: N802
        return self.secret_manager.fetch_secret(name="MONGO_PASSWORD")

    @computed_field
    @property
    def USERNAME(self) -> str:  # noqa: N802
        return self.secret_manager.fetch_secret(name="MONGO_USERNAME")


class GCPConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GCP_")

    PROJECT_ID: str | None = None
    ENV: str | None = None


class Settings(BaseSettings):
    zeus: ZeusSettings
    mongodb: MongoDBSettings

    @classmethod
    def new(
        cls,
        *,
        secret_manager: SecretManager,
    ) -> Settings:
        return cls(
            zeus=ZeusSettings(),
            mongodb=MongoDBSettings(
                secret_manager=secret_manager,
            ),
        )
