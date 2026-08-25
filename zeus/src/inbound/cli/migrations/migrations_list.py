from enum import StrEnum, auto

from inbound.cli.migrations.v1 import MigrationV1
from inbound.cli.migrations.v2 import MigrationV2


class MigrationID(StrEnum):
    V1 = auto()
    V2 = auto()


MIGRATIONS = {
    MigrationID.V1: MigrationV1,
    MigrationID.V2: MigrationV2,
}
