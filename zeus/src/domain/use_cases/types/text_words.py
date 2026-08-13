from dataclasses import dataclass

from domain.entities.special_symbol import SpecialSymbol
from domain.entities.word import Word


@dataclass(frozen=True, kw_only=True, slots=True)
class TextWords:
    words: list[Word]
    special_symbols: list[SpecialSymbol] | None
