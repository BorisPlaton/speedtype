from abc import ABC, abstractmethod

from domain.entities.word import Word
from domain.value_objects.language import Language
from domain.value_objects.special_symbol import SpecialSymbol
from domain.value_objects.word_length import WordLength


class WordRepository(ABC):
    @abstractmethod
    async def upsert(self, *, word: Word) -> None: ...

    @abstractmethod
    async def get_by_word(self, *, word: str) -> Word | None: ...

    @abstractmethod
    async def get_by_characteristics(
        self,
        *,
        language: Language | None,
        word_length: WordLength | None,
        special_symbol: SpecialSymbol | None,
    ) -> list[Word]: ...
