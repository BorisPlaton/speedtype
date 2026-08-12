from domain.entities.config import SpecialSymbols, TextLanguages, TimeLimits, WordsLength
from domain.value_objects.input_time_option import InputTimeOption
from domain.value_objects.language_option import LanguageOption
from domain.value_objects.special_symbol_type import SpecialSymbolType
from domain.value_objects.word_length_option import WordLengthOption
from inbound.cli.migrations.base import Migration
from infrastructure.containers.application import ApplicationContainer


TIME_LIMITS = [
    {
        "is_default": True,
        "seconds": 15,
    },
    {
        "is_default": False,
        "seconds": 30,
    },
    {
        "is_default": False,
        "seconds": 60,
    },
    {
        "is_default": False,
        "seconds": 90,
    },
]
WORDS_LENGTH = [
    {
        "is_default": False,
        "value": "short",
        "title": "SHORT",
    },
    {
        "is_default": True,
        "value": "regular",
        "title": "REGULAR",
    },
    {
        "is_default": False,
        "value": "long",
        "title": "LONG",
    },
]
TEXT_LANGUAGES = [
    {
        "is_default": True,
        "code": "en",
        "title": "ENGLISH",
    },
    {
        "is_default": False,
        "code": "ua",
        "title": "UKRAINIAN",
    },
    {
        "is_default": False,
        "code": "ru",
        "title": "RUSSIAN",
    },
]
SPECIAL_SYMBOLS = [
    {
        "is_default": False,
        "code": "special_symbols",
        "title": "SPECIAL SYMBOLS",
    },
    {
        "is_default": False,
        "code": "punctuation",
        "title": "PUNCTUATION",
    },
]


class MigrationV1(Migration):
    def __init__(
        self,
        *,
        container: ApplicationContainer,
    ) -> None:
        self._time_limits_repository = container.infra.time_limits_repository()
        self._words_length_repository = container.infra.words_length_config_repository()
        self._text_languages_repository = container.infra.text_languages_config_repository()
        self._special_symbols_repository = container.infra.special_symbols_config_repository()

    async def execute(self) -> None:
        if not await self._time_limits_repository.get():
            time_limits_config = TimeLimits.new(
                options=[InputTimeOption.new(**input_time) for input_time in TIME_LIMITS]
            )
            await self._time_limits_repository.upsert(config=time_limits_config)

        if not await self._words_length_repository.get():
            words_length_config = WordsLength.new(
                options=[WordLengthOption.new(**word_length) for word_length in WORDS_LENGTH]
            )
            await self._words_length_repository.upsert(config=words_length_config)

        if not await self._text_languages_repository.get():
            text_languages_config = TextLanguages.new(
                options=[LanguageOption.new(**text_language) for text_language in TEXT_LANGUAGES]
            )
            await self._text_languages_repository.upsert(config=text_languages_config)

        if not await self._special_symbols_repository.get():
            special_symbols_config = SpecialSymbols.new(
                options=[SpecialSymbolType.new(**special_symbol) for special_symbol in SPECIAL_SYMBOLS]
            )
            await self._special_symbols_repository.upsert(config=special_symbols_config)
