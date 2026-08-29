from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from funcy import first

from domain.constraints.display_unique_config_entries import DisplayUniqueConfigEntriesConstraint
from domain.constraints.one_default_config_entry import NotMoreThanOneDefaultConfigEntryConstraint
from domain.value_objects.base import ConfigEntry
from domain.value_objects.input_time_option import InputTimeOption
from domain.value_objects.language_option import LanguageOption
from domain.value_objects.special_symbol_type import SpecialSymbolType
from domain.value_objects.word_length_option import WordLengthOption


@dataclass(kw_only=True, slots=True)
class Config[Option: ConfigEntry[object]](ABC):
    is_required: ClassVar[bool]
    name: ClassVar[str]
    options: list[Option]

    @classmethod
    def new(
        cls,
        *,
        options: list[Option],
    ) -> Config:
        NotMoreThanOneDefaultConfigEntryConstraint(
            items=options,
            exact_one=cls.is_required,
            name=cls.name,
        ).check()
        DisplayUniqueConfigEntriesConstraint(
            items=options,
            name=cls.name,
        ).check()
        return cls(options=options)

    def get_option(
        self,
        *,
        option: object,
    ) -> Option | None:
        return next(filter(lambda x: x.value == option, self.options))

    @property
    def default_option(self) -> Option | None:
        return first(filter(lambda option: option.is_default, (option for option in self.options)))


@dataclass(kw_only=True, slots=True)
class SpecialSymbols(Config[SpecialSymbolType]):
    is_required: ClassVar[bool] = False
    name: ClassVar[str] = "Special Symbols"


@dataclass(kw_only=True, slots=True)
class TextLanguages(Config[LanguageOption]):
    is_required: ClassVar[bool] = True
    name: ClassVar[str] = "Languages"


@dataclass(kw_only=True, slots=True)
class TimeLimits(Config[InputTimeOption]):
    is_required: ClassVar[bool] = True
    name: ClassVar[str] = "Time"


@dataclass(kw_only=True, slots=True)
class WordsLength(Config[WordLengthOption]):
    is_required: ClassVar[bool] = True
    name: ClassVar[str] = "Words Length"
