from typing import Annotated

from typer import Context, Exit, Option, Typer

from inbound.cli.utils import async_command
from infrastructure.containers.application import ApplicationContainer
from infrastructure.migrations.migrations_list import MigrationID


app = Typer()


@app.command()
@async_command
async def migrate(
    ctx: Context,
    migration_id: Annotated[
        MigrationID | None,
        Option(
            help="The specific migration to execute. If not specified, runs all migrations.",
            show_default=False,
        ),
    ] = None,
) -> None:
    """
    Performs application migration.

    Migrations are idempotent. So it is safe to run a single migration multiple times.
    If the `--migration-id` is provided, run only a specified migration.
    """
    container: ApplicationContainer = ctx.obj
    migrations_runner = container.infra.migrations_runner()

    try:
        await migrations_runner.run(migration_id=migration_id)
    except Exception as exc:
        print(exc)  # noqa: T201
        raise Exit(code=1) from exc
