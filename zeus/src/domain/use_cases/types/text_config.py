from dataclasses import dataclass

from domain.entities.config import SpecialSymbols, TextLanguages, TimeLimits, WordsLength


@dataclass(frozen=True, kw_only=True, slots=True)
class TextConfig:
    special_symbols: SpecialSymbols
    text_languages: TextLanguages
    time_limits: TimeLimits
    words_length: WordsLength
