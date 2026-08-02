from enum import StrEnum, auto

from inbound.cli.migrations.v1 import MigrationV1


class MigrationID(StrEnum):
    V1 = auto()


MIGRATIONS = {
    MigrationID.V1: MigrationV1,
}
