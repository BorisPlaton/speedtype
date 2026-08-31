from typing import Annotated

from typer import Context, Exit, Option, Typer

from inbound.cli.migrations.migrations_list import MIGRATIONS, MigrationID
from inbound.cli.utils import async_command
from infrastructure.containers.application import ApplicationContainer


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

    if migration_id:
        if not (migration := MIGRATIONS.get(migration_id)):
            raise Exit(code=1)
        await migration(container=container).execute()

    for migration in MIGRATIONS.values():
        await migration(container=container).execute()
