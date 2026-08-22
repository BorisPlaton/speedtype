from dataclasses import dataclass

from domain.constraints.not_empty_string import NotEmptyStringConstraint
from domain.value_objects.special_symbol_type import SpecialSymbolType


@dataclass(kw_only=True, slots=True)
class SpecialSymbol:
    value: str
    special_symbol_type: str

    @classmethod
    def new(
        cls,
        *,
        special_symbol: str,
        special_symbol_type: SpecialSymbolType,
    ) -> SpecialSymbol:
        NotEmptyStringConstraint(value=special_symbol, name="Special symbol's value").check()
        return cls(
            value=special_symbol,
            special_symbol_type=special_symbol_type.value,
        )
