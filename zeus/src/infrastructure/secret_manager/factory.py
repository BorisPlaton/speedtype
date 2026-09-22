import google
from google.auth.compute_engine.credentials import Credentials as GCECredentials

from infrastructure.secret_manager.base import SecretManager
from infrastructure.secret_manager.gcp import GCPSecretManager
from infrastructure.secret_manager.local import LocalSecretManager
from infrastructure.settings import GCPConfig


def secret_manager_factory(gcp_config: GCPConfig) -> SecretManager:
    credentials, _ = google.auth.default()
    is_on_gcp = isinstance(credentials, GCECredentials)

    if is_on_gcp:
        return GCPSecretManager(
            gcp_project_id=gcp_config.PROJECT_ID,
            env=gcp_config.ENV,
        )

    return LocalSecretManager()
