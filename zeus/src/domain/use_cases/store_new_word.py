import asyncio

from domain.entities.special_symbols import SpecialSymbols
from domain.entities.text_languages import TextLanguages
from domain.entities.word import Word
from domain.entities.words_length import WordsLength
from domain.exceptions.use_case.store_new_word import NonExistingOption, WordAlreadyExist
from domain.repository.special_symbols import SpecialSymbolsRepository
from domain.repository.text_languages import TextLanguagesRepository
from domain.repository.word import WordRepository
from domain.repository.words_length import WordsLengthRepository
from domain.use_cases.base import UseCase


class StoreNewWord(UseCase[None]):
    def __init__(
        self,
        *,
        word_repository: WordRepository,
        words_length_repository: WordsLengthRepository,
        text_languages_repository: TextLanguagesRepository,
        special_symbols_repository: SpecialSymbolsRepository,
    ) -> None:
        self._word_repository = word_repository
        self._words_length_repository = words_length_repository
        self._text_languages_repository = text_languages_repository
        self._special_symbols_repository = special_symbols_repository

    async def execute(
        self,
        *,
        word: str,
        language: str,
        word_length: str,
        special_symbol_type: str | None,
    ) -> None:
        already_created_word = await self._word_repository.get_by_word(word=word)

        if already_created_word:
            raise WordAlreadyExist(word=already_created_word.value)

        async with asyncio.TaskGroup() as tg:
            words_length_task = tg.create_task(self._words_length_repository.get())
            text_language_task = tg.create_task(self._text_languages_repository.get())
            special_symbols_task = tg.create_task(self._special_symbols_repository.get())

        words_length_config = words_length_task.result()
        text_languages_config = text_language_task.result()
        special_symbols_config = special_symbols_task.result()

        if not (word_length_option := words_length_config.get_option(option=word_length)):
            raise NonExistingOption(
                option=word_length,
                option_name=WordsLength.name,
            )

        if not (text_language_option := text_languages_config.get_option(option=language)):
            raise NonExistingOption(
                option=language,
                option_name=TextLanguages.name,
            )

        special_symbol_option = None
        if special_symbol_type and not (
            special_symbol_option := special_symbols_config.get_option(option=special_symbol_type)
        ):
            raise NonExistingOption(
                option=special_symbol_type,
                option_name=SpecialSymbols.name,
            )

        new_word = Word.new(
            value=word,
            word_length=word_length_option,
            language=text_language_option,
            special_symbol=special_symbol_option,
        )
        await self._word_repository.upsert(word=new_word)
