from typer import Context, Typer

from inbound.cli.commands import app as cli_app
from infrastructure.containers.application import ApplicationContainer


class CLIApp:
    def __init__(
        self,
        *,
        container: ApplicationContainer,
    ) -> None:
        self._container = container
        self._app = Typer(
            help="The CLI tool for interaction with Zeus service.",
            no_args_is_help=True,
        )
        self._app.add_typer(cli_app)
        self._app.callback()(self._add_di)

    def run(self) -> None:
        self._app()

    def _add_di(self, ctx: Context) -> None:
        ctx.obj = self._container
