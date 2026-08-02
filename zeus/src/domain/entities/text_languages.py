from dataclasses import dataclass
from typing import ClassVar

from domain.entities.config import Config
from domain.value_objects.language import Language


@dataclass(kw_only=True, slots=True)
class TextLanguages(Config[Language]):
    is_required: ClassVar[bool] = True
    name: ClassVar[str] = "Languages"
