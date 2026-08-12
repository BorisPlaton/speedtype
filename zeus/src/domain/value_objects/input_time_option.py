from dataclasses import dataclass

from domain.exceptions.input_time import InputTimeMustBeGreaterThanZero
from domain.value_objects.base import ConfigEntry


@dataclass(slots=True, frozen=True, kw_only=True)
class InputTimeOption(ConfigEntry[int]):
    @classmethod
    def new(
        cls,
        *,
        seconds: int,
        is_default: bool,
    ) -> InputTimeOption:
        cls._check_seconds(seconds=seconds)
        return InputTimeOption(
            value=seconds,
            is_default=is_default,
        )

    def get_display_text(self) -> str:
        return str(self.value)

    @staticmethod
    def _check_seconds(
        *,
        seconds: int,
    ) -> None:
        if seconds <= 0:
            raise InputTimeMustBeGreaterThanZero(actual_time=seconds)
