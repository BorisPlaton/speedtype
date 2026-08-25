from dataclasses import dataclass
from enum import StrEnum

from funcy import select


@dataclass(kw_only=True, slots=True, frozen=True)
class TextConfigOption:
    label: str
    value: str | None = None


class TextConfigName(StrEnum):
    TIME = "TIME"
    LANGUAGE = "LANGUAGE"
    SPECIAL_SYMBOLS = "SPECIAL_SYMBOLS"
    WORDS_LENGTH = "WORDS_LENGTH"


@dataclass(kw_only=True, slots=True)
class SelectedTextConfig:
    langauge: TextConfigOption | None
    time: TextConfigOption | None
    words_length: TextConfigOption | None
    special_symbols: tuple[TextConfigOption, ...]

    @classmethod
    def new(cls) -> SelectedTextConfig:
        return SelectedTextConfig(
            langauge=None,
            time=None,
            words_length=None,
            special_symbols=(),
        )

    def update_config_option(
        self,
        *,
        config_name: TextConfigName | str,
        option: TextConfigOption,
    ) -> None:
        match config_name:
            case TextConfigName.TIME:
                self.time = option
            case TextConfigName.LANGUAGE:
                self.langauge = option
            case TextConfigName.WORDS_LENGTH:
                self.words_length = option
            case TextConfigName.SPECIAL_SYMBOLS:
                self.special_symbols = self.special_symbols + (option,)
            case _:
                raise ValueError(f"Unknown config option: '{config_name}'.")

    def remove_config_option_by_value(
        self,
        *,
        config_name: TextConfigName | str,
        value: str,
    ) -> None:
        match config_name:
            case TextConfigName.TIME:
                self.time = None
            case TextConfigName.LANGUAGE:
                self.langauge = None
            case TextConfigName.WORDS_LENGTH:
                self.words_length = None
            case TextConfigName.SPECIAL_SYMBOLS:
                self.special_symbols = select(
                    lambda option: option.value != value,
                    self.special_symbols,
                )
            case _:
                raise ValueError(f"Unknown config option: '{config_name}'.")

    @property
    def input_time_seconds(self) -> int:
        return int(self.time.value)
