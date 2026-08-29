from typing import TypedDict

from domain.entities.config import WordsLength
from domain.value_objects.word_length_option import WordLengthOption
from infrastructure.repository.config import ConfigMongoDBRepository


class WordsLengthConfigMongoDBRepository(ConfigMongoDBRepository[WordsLength]):
    class WordsLengthRecord(TypedDict):
        config_name: str
        options: list[WordsLengthConfigMongoDBRepository.WordsLengthRecordOption]

    class WordsLengthRecordOption(TypedDict):
        title: str
        value: str
        is_default: bool

    def _to_json(self, *, entity: WordsLength) -> WordsLengthRecord:
        return {
            "config_name": WordsLength.name,
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

    @property
    def _config_class(self) -> type[WordsLength]:
        return WordsLength
