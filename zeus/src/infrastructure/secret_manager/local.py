import os

from infrastructure.secret_manager.base import SecretManager


class LocalSecretManager(SecretManager):
    def fetch_secret(
        self,
        *,
        name: str,
    ) -> str:
        return os.getenv(name)
