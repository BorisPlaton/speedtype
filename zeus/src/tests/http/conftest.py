from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx2 import ASGITransport, AsyncClient

from inbound.http.app import create_app
from infrastructure.containers.application import ApplicationContainer


@pytest.fixture(scope="package", autouse=True)
async def apply_migrations(container: ApplicationContainer) -> AsyncGenerator[None, None]:
    migrations_runner = container.infra.migrations_runner()

    await migrations_runner.run()
    yield
    await migrations_runner.rollback()


@pytest_asyncio.fixture(loop_scope="session")
async def zeus_client(container: ApplicationContainer) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(
            app=create_app(container=container),
            raise_app_exceptions=False,
        ),
        base_url="http://test",
    ) as client:
        yield client
