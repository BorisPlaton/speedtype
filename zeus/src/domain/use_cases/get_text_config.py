import asyncio

from domain.repository.special_symbols import SpecialSymbolsRepository
from domain.repository.text_languages import TextLanguagesRepository
from domain.repository.time_limits import TimeLimitsRepository
from domain.repository.words_length import WordsLengthRepository
from domain.use_cases.base import UseCase
from domain.use_cases.types.text_config import TextConfig


class GetTextConfig(UseCase[TextConfig]):
    def __init__(
        self,
        *,
        words_length_repository: WordsLengthRepository,
        time_limits_repository: TimeLimitsRepository,
        text_languages_repository: TextLanguagesRepository,
        special_symbols_repository: SpecialSymbolsRepository,
    ) -> None:
        self._words_length_repository = words_length_repository
        self._time_limit_repository = time_limits_repository
        self._text_languages_repository = text_languages_repository
        self._special_symbols_repository = special_symbols_repository

    async def execute(self) -> TextConfig:
        async with asyncio.TaskGroup() as tg:
            words_length_task = tg.create_task(self._words_length_repository.get())
            time_limit_task = tg.create_task(self._time_limit_repository.get())
            text_language_task = tg.create_task(self._text_languages_repository.get())
            special_symbols_task = tg.create_task(self._special_symbols_repository.get())

        return TextConfig(
            special_symbols=special_symbols_task.result(),
            words_length=words_length_task.result(),
            time_limits=time_limit_task.result(),
            text_languages=text_language_task.result(),
        )
