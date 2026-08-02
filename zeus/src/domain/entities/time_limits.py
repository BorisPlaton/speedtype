from dataclasses import dataclass
from typing import ClassVar

from domain.entities.config import Config
from domain.value_objects.input_time import InputTime


@dataclass(kw_only=True, slots=True)
class TimeLimits(Config[InputTime]):
    is_required: ClassVar[bool] = True
    name: ClassVar[str] = "Time"
