from collections.abc import Generator
from typing import Any

import pytest
from testcontainers.community.mongodb import MongoDbContainer

from infrastructure.containers.application import ApplicationContainer
from infrastructure.containers.utils import create_container


@pytest.fixture(scope="session")
def container() -> Generator[ApplicationContainer, Any, None]:
    container = create_container()

    with (
        MongoDbContainer(
            "mongo:7.0.34",
            username=container.config.mongodb.USERNAME(),
            password=container.config.mongodb.PASSWORD(),
            dbname=container.config.mongodb.DATABASE_NAME(),
        ) as mongodb,
        container.config.mongodb.URI.override(
            f"{mongodb.get_connection_url()}/{container.config.mongodb.DATABASE_NAME()}"
            f"?authSource={container.config.mongodb.AUTH_SOURCE()}",
        ),
        container.config.zeus.DEBUG.override(False),
    ):
        yield container
