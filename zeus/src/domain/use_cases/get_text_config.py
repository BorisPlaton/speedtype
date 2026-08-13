import asyncio

from domain.repository.config import (
    SpecialSymbolsConfigRepository,
    TextLanguagesConfigRepository,
    TimeLimitsConfigRepository,
    WordsLengthConfigRepository,
)
from domain.use_cases.base import UseCase
from domain.use_cases.types.text_config import TextConfig


class GetTextConfig(UseCase[TextConfig]):
    def __init__(
        self,
        *,
        words_length_config_repository: WordsLengthConfigRepository,
        time_limits_config_repository: TimeLimitsConfigRepository,
        text_languages_config_repository: TextLanguagesConfigRepository,
        special_symbols_config_repository: SpecialSymbolsConfigRepository,
    ) -> None:
        self._words_length_config_repository = words_length_config_repository
        self._time_limits_config_repository = time_limits_config_repository
        self._text_languages_config_repository = text_languages_config_repository
        self._special_symbols_config_repository = special_symbols_config_repository

    async def execute(self) -> TextConfig:
        async with asyncio.TaskGroup() as tg:
            words_length_task = tg.create_task(self._words_length_config_repository.get())
            time_limit_task = tg.create_task(self._time_limits_config_repository.get())
            text_language_task = tg.create_task(self._text_languages_config_repository.get())
            special_symbols_task = tg.create_task(self._special_symbols_config_repository.get())

        return TextConfig(
            special_symbols=special_symbols_task.result(),
            words_length=words_length_task.result(),
            time_limits=time_limit_task.result(),
            text_languages=text_language_task.result(),
        )
