from infrastructure.migrations.base import Migration
from infrastructure.migrations.migrations_list import MigrationID
from infrastructure.migrations.versions.v1 import MigrationV1
from infrastructure.migrations.versions.v2 import MigrationV2


class MigrationsRepository:
    def __init__(
        self,
        *,
        migration_v1: MigrationV1,
        migration_v2: MigrationV2,
    ) -> None:
        self._migrations = {
            MigrationID.V1: migration_v1,
            MigrationID.V2: migration_v2,
        }

    def get_migration(self, *, migration_id: MigrationID) -> Migration | None:
        return self._migrations.get(migration_id)

    def get_all(self) -> list[Migration]:
        return list(self._migrations.values())
