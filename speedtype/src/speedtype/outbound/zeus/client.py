from abc import ABC, abstractmethod
from urllib.parse import urljoin

from aiohttp import ClientSession

from speedtype.outbound.http.error import FailedRequest
from speedtype.outbound.zeus.contracts.get_text_config import TextConfigResponseContract
from speedtype.outbound.zeus.contracts.get_text_words import GetTextWordsResponseContract


class ZeusClient(ABC):
    @abstractmethod
    async def get_text_config(self) -> TextConfigResponseContract: ...

    @abstractmethod
    async def get_text_words(
        self,
        *,
        language: str,
        words_length: str,
        special_symbol_types: list[str] | None = None,
    ) -> GetTextWordsResponseContract: ...


class ZeusHTTPClient(ZeusClient):
    GET_TEXT_CONFIG = "/text/config"
    GET_TEXT_WORDS = "/text/words"

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

    async def get_text_words(
        self,
        *,
        language: str,
        words_length: str,
        special_symbol_types: list[str] | None = None,
    ) -> GetTextWordsResponseContract:
        payload = await self._request(
            method="POST",
            url=self.GET_TEXT_WORDS,
            body={
                "language": language,
                "words_length": words_length,
                "special_symbol_types": special_symbol_types,
            },
        )
        return GetTextWordsResponseContract(**payload)

    async def _request(
        self,
        *,
        method: str,
        url: str,
        body: object = None,
    ) -> dict[str, object]:
        response = await self._http_client.request(method=method, url=urljoin(self._zeus_url, url), json=body)

        if not response.ok:
            raise FailedRequest(
                details={
                    "status_code": response.status,
                    "details": response.content,
                }
            )

        return await response.json()
