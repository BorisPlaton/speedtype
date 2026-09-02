from unittest.mock import AsyncMock, MagicMock

import pytest

from infrastructure.containers.application import ApplicationContainer
from infrastructure.migrations.migrations_list import MigrationID


async def test_migration_runner_execute_all_migrations(
    container: ApplicationContainer,
) -> None:
    migrations_repository = MagicMock()

    with container.infra.override_providers(migrations_repository=migrations_repository):
        migration = AsyncMock()
        migrations_repository.get_all.return_value = [migration]
        runner = container.infra.migrations_runner()

        await runner.run()

        migrations_repository.get_all.assert_called_once()
        migrations_repository.get_migration.assert_not_called()
        migration.execute.assert_awaited_once()


async def test_migration_runner_execute_specified_migration(
    container: ApplicationContainer,
) -> None:
    migrations_repository = MagicMock()

    with container.infra.override_providers(migrations_repository=migrations_repository):
        migration = AsyncMock()
        migrations_repository.get_migration.return_value = migration
        runner = container.infra.migrations_runner()

        await runner.run(migration_id=MigrationID.V1)

        migrations_repository.get_all.assert_not_called()
        migrations_repository.get_migration.assert_called_once()
        migration.execute.assert_awaited_once()


@pytest.mark.parametrize(
    "migration_id",
    [
        "v1-1",
        "qwerty",
        "v0",
    ],
)
async def test_migration_runner_fails_with_invalid_migration_id(
    migration_id: str,
    container: ApplicationContainer,
) -> None:
    runner = container.infra.migrations_runner()

    with pytest.raises(ValueError):
        await runner.run(migration_id=migration_id)
