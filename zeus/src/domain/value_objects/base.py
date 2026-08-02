from abc import ABC
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class ConfigEntry[Value](ABC):
    is_default: bool
    value: Value

    def get_display_text(self) -> str:
        return str(self.value)
