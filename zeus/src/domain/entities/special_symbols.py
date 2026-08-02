from dataclasses import dataclass
from typing import ClassVar

from domain.entities.config import Config
from domain.value_objects.special_symbol import SpecialSymbol


@dataclass(kw_only=True, slots=True)
class SpecialSymbols(Config[SpecialSymbol]):
    is_required: ClassVar[bool] = False
    name: ClassVar[str] = "Special Symbols"
