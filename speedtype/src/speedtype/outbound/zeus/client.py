from abc import ABC, abstractmethod
from urllib.parse import urljoin

from aiohttp import ClientSession

from speedtype.outbound.http.error import FailedRequest
from speedtype.outbound.zeus.contracts.fetch_text_config import TextConfigResponseContract


class ZeusClient(ABC):
    @abstractmethod
    async def get_text_config(self) -> TextConfigResponseContract: ...


class ZeusHTTPClient(ZeusClient):
    GET_TEXT_CONFIG = "/text/config"

    def __init__(
        self,
        *,
        http_client: ClientSession,
        zeus_url: str,
    ) -> None:
        self._http_client = http_client
        self._zeus_url = zeus_url

    async def get_text_config(self) -> TextConfigResponseContract:
        payload = await self._request(
            method="GET",
            url=self.GET_TEXT_CONFIG,
        )
        return TextConfigResponseContract(**payload)

    async def _request(
        self,
        *,
        method: str,
        url: str,
        json: object = None,
    ) -> dict[str, object]:
        response = await self._http_client.request(method=method, url=urljoin(self._zeus_url, url), json=json)

        if not response.ok:
            raise FailedRequest(
                details={
                    "status_code": response.status,
                    "details": response.content,
                }
            )

        return await response.json()
