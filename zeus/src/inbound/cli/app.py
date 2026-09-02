from typer import Context, Typer

from inbound.cli.commands import app as cli_app
from infrastructure.containers.application import ApplicationContainer
from infrastructure.containers.utils import create_container


def create_cli_app(*, container: ApplicationContainer | None = None) -> Typer:
    def callback(ctx: Context) -> None:
        ctx.obj = container

    app = Typer(
        help="The CLI tool for interaction with Zeus service.",
        no_args_is_help=True,
    )
    container = container or create_container()
    app.add_typer(cli_app)
    app.callback()(callback)

    return app
