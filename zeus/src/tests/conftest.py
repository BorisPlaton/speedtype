from collections.abc import Generator

import pytest
from testcontainers.community.mongodb import MongoDbContainer

from infrastructure.containers.application import ApplicationContainer
from infrastructure.containers.utils import create_container


@pytest.fixture(scope="session")
def container() -> Generator[ApplicationContainer, None, None]:
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


@pytest.fixture(autouse=True)
def reset_container_singletons(container: ApplicationContainer) -> Generator[None, None, None]:
    yield
    container.reset_singletons()
