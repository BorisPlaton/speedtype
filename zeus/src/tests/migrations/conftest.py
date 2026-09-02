from collections.abc import AsyncGenerator

import pytest

from infrastructure.containers.application import ApplicationContainer


@pytest.fixture
async def clean_mongodb(container: ApplicationContainer) -> AsyncGenerator[None, None]:
    yield
    db = container.infra.mongo_client().get_database()
    for collection in await db.list_collection_names():
        await db.drop_collection(collection)
