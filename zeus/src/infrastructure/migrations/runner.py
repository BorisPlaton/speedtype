from infrastructure.migrations.migrations_list import MigrationID
from infrastructure.repository.migrations import MigrationsRepository


class MigrationRunner:
    def __init__(
        self,
        *,
        migrations_repository: MigrationsRepository,
    ) -> None:
        self._migrations_repository = migrations_repository

    async def run(
        self,
        *,
        migration_id: MigrationID | None = None,
    ) -> None:
        if migration_id:
            if not (migration := self._migrations_repository.get_migration(migration_id=migration_id)):
                raise ValueError(f"Unknown migration '{migration_id}'.")
            await migration.execute()
            return

        for migration in self._migrations_repository.get_all():
            await migration.execute()

    async def rollback(
        self,
        *,
        migration_id: MigrationID | None = None,
    ) -> None:
        if migration_id:
            if not (migration := self._migrations_repository.get_migration(migration_id=migration_id)):
                raise ValueError(f"Unknown migration '{migration_id}'.")
            await migration.rollback()
            return

        for migration in self._migrations_repository.get_all()[::-1]:
            await migration.rollback()
