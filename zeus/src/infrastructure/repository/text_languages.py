from typing import TypedDict

from domain.entities.text_languages import TextLanguages
from domain.value_objects.language import Language
from infrastructure.repository.config import ConfigMongoDBRepository


class TextLanguagesMongoDBRepository(ConfigMongoDBRepository[TextLanguages]):
    class TextLanguagesRecord(TypedDict):
        options: list[TextLanguagesMongoDBRepository.TextLanguagesRecordOption]

    class TextLanguagesRecordOption(TypedDict):
        title: str
        value: str
        is_default: bool

    @property
    def collection_name(self) -> str:
        return "text_languages"

    def _to_json(
        self,
        *,
        entity: TextLanguages,
    ) -> TextLanguagesRecord:
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

    def _from_json(
        self,
        *,
        data: TextLanguagesRecord,
    ) -> TextLanguages:
        return TextLanguages(
            options=[
                Language(
                    is_default=option["is_default"],
                    value=option["value"],
                    title=option["title"],
                )
                for option in data["options"]
            ]
        )
