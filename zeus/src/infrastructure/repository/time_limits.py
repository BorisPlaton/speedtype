from typing import TypedDict

from domain.entities.time_limits import TimeLimits
from domain.value_objects.input_time import InputTime
from infrastructure.repository.config import ConfigMongoDBRepository


class TimeLimitsMongoDBRepository(ConfigMongoDBRepository[TimeLimits]):
    class TimeLimitsRecord(TypedDict):
        options: list[TimeLimitsMongoDBRepository.TimeLimitsRecordOption]

    class TimeLimitsRecordOption(TypedDict):
        value: int
        is_default: bool

    @property
    def collection_name(self) -> str:
        return "time_limits"

    def _to_json(
        self,
        *,
        entity: TimeLimits,
    ) -> TimeLimitsRecord:
        return {
            "options": [
                {
                    "value": option.value,
                    "is_default": option.is_default,
                }
                for option in entity.options
            ],
        }

    def _from_json(
        self,
        *,
        data: TimeLimitsRecord,
    ) -> TimeLimits:
        return TimeLimits(
            options=[
                InputTime(
                    is_default=option["is_default"],
                    value=option["value"],
                )
                for option in data["options"]
            ]
        )
