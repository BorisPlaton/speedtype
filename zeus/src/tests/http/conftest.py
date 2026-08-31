from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx2 import ASGITransport, AsyncClient

from inbound.cli.migrations.migrations_list import MIGRATIONS
from inbound.http.app import create_app
from infrastructure.containers.application import ApplicationContainer


@pytest.fixture(scope="package", autouse=True)
async def apply_migrations(container: ApplicationContainer) -> AsyncGenerator[None, None]:
    migrations = list(MIGRATIONS.values())

    for migration in migrations:
        await migration(container=container).execute()

    yield

    for migration in migrations[::-1]:
        await migration(container=container).rollback()


@pytest_asyncio.fixture(loop_scope="session")
async def zeus_client(container: ApplicationContainer) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(
            app=create_app(app_container=container),
            raise_app_exceptions=False,
        ),
        base_url="http://test",
    ) as client:
        yield client
