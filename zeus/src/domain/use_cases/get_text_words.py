import asyncio

from domain.entities.config import SpecialSymbols, TextLanguages, WordsLength
from domain.exceptions.config_option_doesnt_exist import ConfigOptionDoesntExist
from domain.repository.config import (
    SpecialSymbolsConfigRepository,
    TextLanguagesConfigRepository,
    WordsLengthConfigRepository,
)
from domain.repository.special_symbols import SpecialSymbolsRepository
from domain.repository.word import WordsRepository
from domain.use_cases.base import UseCase
from domain.use_cases.types.text_words import TextWords


class GetTextWords(UseCase[TextWords]):
    def __init__(
        self,
        *,
        words_repository: WordsRepository,
        special_symbols_repository: SpecialSymbolsRepository,
        words_length_config_repository: WordsLengthConfigRepository,
        text_languages_config_repository: TextLanguagesConfigRepository,
        special_symbols_config_repository: SpecialSymbolsConfigRepository,
    ) -> None:
        self._words_length_config_repository = words_length_config_repository
        self._text_languages_config_repository = text_languages_config_repository
        self._special_symbols_config_repository = special_symbols_config_repository
        self._special_symbols_repository = special_symbols_repository
        self._words_repository = words_repository

    async def execute(
        self,
        *,
        language: str,
        words_length: str,
        special_symbol_types: list[str] | None,
    ) -> TextWords:
        async with asyncio.TaskGroup() as tg:
            words_length_task = tg.create_task(self._words_length_config_repository.get())
            text_language_task = tg.create_task(self._text_languages_config_repository.get())

        words_length_config = words_length_task.result()
        text_language_config = text_language_task.result()

        if not (word_length_option := words_length_config.get_option(option=words_length)):
            raise ConfigOptionDoesntExist(
                config_name=WordsLength.name,
                non_existed_option=words_length,
            )

        if not (text_language_option := text_language_config.get_option(option=language)):
            raise ConfigOptionDoesntExist(
                config_name=TextLanguages.name,
                non_existed_option=language,
            )

        words = await self._words_repository.get_by_characteristics(
            language=text_language_option,
            word_length=word_length_option,
        )

        if special_symbol_types is None:
            return TextWords(
                words=words,
                special_symbols=None,
            )

        special_symbols_config = await self._special_symbols_config_repository.get()

        special_symbol_options = []
        for symbol_type in special_symbol_types:
            if not (special_symbol_option := special_symbols_config.get_option(option=symbol_type)):
                raise ConfigOptionDoesntExist(
                    config_name=SpecialSymbols.name,
                    non_existed_option=symbol_type,
                )
            special_symbol_options.append(special_symbol_option)

        special_symbols = await self._special_symbols_repository.get_by_types(
            special_symbol_types=special_symbol_options,
        )

        return TextWords(
            words=words,
            special_symbols=special_symbols,
        )
