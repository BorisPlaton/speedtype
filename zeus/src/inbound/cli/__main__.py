from inbound.cli.app import CLIApp
from infrastructure.containers.application import ApplicationContainer
from infrastructure.settings import Settings


if __name__ == "__main__":
    container = ApplicationContainer()
    container.config.from_pydantic(Settings(), required=True)
    CLIApp(container=container).run()
