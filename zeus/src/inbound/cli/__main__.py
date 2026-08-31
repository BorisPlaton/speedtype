from inbound.cli.app import CLIApp
from infrastructure.containers.utils import create_container


if __name__ == "__main__":
    CLIApp(container=create_container()).run()
