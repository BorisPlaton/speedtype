from abc import ABC, abstractmethod


class SecretManager(ABC):
    @abstractmethod
    def fetch_secret(self, *, name: str) -> str | None: ...
