from aiohttp import ClientSession, ClientTimeout
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Provider, Singleton

from speedtype.outbound.zeus.client import ZeusClient, ZeusHTTPClient


class ApplicationContainer(DeclarativeContainer):
    config = Configuration(strict=True)

    http_timeout: Provider[ClientTimeout] = Singleton(
        ClientTimeout,
        total=config.HTTP_TIMEOUT,
    )
    http_client: Provider[ClientSession] = Singleton(
        ClientSession,
        timeout=http_timeout,
    )
    zeus_client: Provider[ZeusClient] = Singleton(
        ZeusHTTPClient,
        http_client=http_client,
        zeus_url=config.ZEUS_URL,
    )
