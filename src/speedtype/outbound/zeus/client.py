from abc import ABC

from speedtype.outbound.http.api_result import APIResult
from speedtype.outbound.http.client import HTTPClient
from speedtype.outbound.http.error import APIError
from speedtype.outbound.zeus.contracts.fetch_text_config import FetchTextConfigResponse


class ZeusClient(ABC):
    async def fetch_text_config(self) -> APIResult[FetchTextConfigResponse, APIError]:
        pass


class ZeusHTTPClient(ZeusClient, HTTPClient):
    async def fetch_text_config(self) -> APIResult[FetchTextConfigResponse, APIError]:
        pass

    @property
    def name(self) -> str:
        return "zeus"
