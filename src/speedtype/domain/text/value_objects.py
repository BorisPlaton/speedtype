from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class TextConfig:
    languages: tuple[TextLanguage, ...]
    time_limits: tuple[TimeLimit, ...]
    words_configs: WordsConfigs


@dataclass(frozen=True, kw_only=True)
class TextLanguage:
    title: str
    code: str
    is_default: bool


@dataclass(frozen=True, kw_only=True)
class TimeLimit:
    seconds: int
    display_text: str
    is_default: bool


@dataclass(frozen=True, kw_only=True)
class WordsConfigs:
    word_lengths: TextModifier
    special_symbols: TextModifier


@dataclass(frozen=True, kw_only=True)
class TextModifier:
    options: tuple[TextOption, ...]
    is_required: bool


@dataclass(frozen=True, kw_only=True)
class TextOption:
    title: str
    code: str
    is_default: bool
