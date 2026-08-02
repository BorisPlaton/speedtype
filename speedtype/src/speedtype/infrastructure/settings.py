from pydantic_settings import BaseSettings


class SpeedTypeSettings(BaseSettings):
    ZEUS_URL: str
    HTTP_TIMEOUT: int = 3
