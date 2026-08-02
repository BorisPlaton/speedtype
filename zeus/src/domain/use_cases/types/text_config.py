from dataclasses import dataclass

from domain.entities.special_symbols import SpecialSymbols
from domain.entities.text_languages import TextLanguages
from domain.entities.time_limits import TimeLimits
from domain.entities.words_length import WordsLength


@dataclass(frozen=True, kw_only=True, slots=True)
class TextConfig:
    special_symbols: SpecialSymbols
    text_languages: TextLanguages
    time_limits: TimeLimits
    words_length: WordsLength
