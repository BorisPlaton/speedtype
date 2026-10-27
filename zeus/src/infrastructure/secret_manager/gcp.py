from google.cloud.secretmanager_v1 import SecretManagerServiceClient

from infrastructure.secret_manager.base import SecretManager


class GCPSecretManager(SecretManager):
    def __init__(
        self,
        *,
        gcp_project_id: str,
        env: str,
    ) -> None:
        self._client = SecretManagerServiceClient()
        self._gcp_project_id = gcp_project_id
        self._env = env

    def fetch_secret(
        self,
        *,
        name: str,
    ) -> str:
        name = f"projects/{self._gcp_project_id}/secrets/{name}_{self._env}/versions/latest"
        response = self._client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
