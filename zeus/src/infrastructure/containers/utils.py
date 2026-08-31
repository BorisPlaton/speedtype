from infrastructure.containers.application import ApplicationContainer
from infrastructure.settings import Settings


def create_container() -> ApplicationContainer:
    container = ApplicationContainer()
    container.config.from_pydantic(Settings(), required=True)
    return container
