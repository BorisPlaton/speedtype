from pydantic_settings import BaseSettings


class SpeedTypeSettings(BaseSettings):
    ZEUS_URL: str = "http://136.82.106.43"
    HTTP_TIMEOUT: int = 3
