from abc import ABC, abstractmethod

from domain.entities.word import Word
from domain.value_objects.language_option import LanguageOption
from domain.value_objects.word_length_option import WordLengthOption


class WordsRepository(ABC):
    @abstractmethod
    async def upsert_many(self, *, entries: list[Word]) -> None: ...

    @abstractmethod
    async def get_by_characteristics(
        self,
        *,
        language: LanguageOption,
        word_length: WordLengthOption,
    ) -> list[Word]: ...
