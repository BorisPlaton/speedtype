from typing import TypedDict

from pymongo import UpdateOne

from domain.entities.word import Word
from domain.repository.word import WordsRepository
from domain.value_objects.language_option import LanguageOption
from domain.value_objects.word_length_option import WordLengthOption
from infrastructure.repository.base import BaseMongoDBRepository


class WordsMongoDBRepository(BaseMongoDBRepository, WordsRepository):
    class WordRecord(TypedDict):
        word: str
        language: str
        word_length: str

    async def upsert_many(
        self,
        *,
        entries: list[Word],
    ) -> None:
        operations = [
            UpdateOne(
                {"word": entry.value, "word_length": entry.word_length_value},
                {"$set": self._to_json(entity=entry)},
                upsert=True,
            )
            for entry in entries
        ]
        await self._collection.bulk_write(operations)

    async def get_by_characteristics(
        self,
        *,
        language: LanguageOption,
        word_length: WordLengthOption,
    ) -> list[Word]:
        words = await self._collection.find(
            {
                "language": language.value,
                "word_length": word_length.value,
            }
        ).to_list()

        return [self._from_json(data=record) for record in words]

    async def delete_all(self) -> None:
        await self._collection.delete_many({})

    @staticmethod
    def _to_json(
        *,
        entity: Word,
    ) -> WordRecord:
        return {
            "language": entity.language_value,
            "word_length": entity.word_length_value,
            "word": entity.value,
        }

    @staticmethod
    def _from_json(
        *,
        data: WordRecord,
    ) -> Word:
        return Word(
            value=data["word"],
            language_value=data["language"],
            word_length_value=data["word_length"],
        )

    @property
    def _collection_name(self) -> str:
        return "words"
