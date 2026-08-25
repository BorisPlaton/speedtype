from typing import TypedDict

from domain.entities.config import WordsLength
from domain.value_objects.word_length_option import WordLengthOption
from infrastructure.repository.config import ConfigMongoDBRepository


class WordsLengthConfigMongoDBRepository(ConfigMongoDBRepository[WordsLength]):
    class WordsLengthRecord(TypedDict):
        options: list[WordsLengthConfigMongoDBRepository.WordsLengthRecordOption]

    class WordsLengthRecordOption(TypedDict):
        title: str
        value: str
        is_default: bool

    @property
    def _collection_name(self) -> str:
        return "words_length"

    def _to_json(self, *, entity: WordsLength) -> WordsLengthRecord:
        return {
            "options": [
                {
                    "title": option.title,
                    "value": option.value,
                    "is_default": option.is_default,
                }
                for option in entity.options
            ],
        }

    def _from_json(self, *, data: WordsLengthRecord) -> WordsLength:
        return WordsLength(
            options=[
                WordLengthOption(
                    is_default=option["is_default"],
                    value=option["value"],
                    title=option["title"],
                )
                for option in data["options"]
            ]
        )
