from typing import TypedDict

from domain.entities.config import TextLanguages
from domain.value_objects.language_option import LanguageOption
from infrastructure.repository.config import ConfigMongoDBRepository


class TextLanguagesConfigMongoDBRepository(ConfigMongoDBRepository[TextLanguages]):
    class TextLanguagesRecord(TypedDict):
        config_name: str
        options: list[TextLanguagesConfigMongoDBRepository.TextLanguagesRecordOption]

    class TextLanguagesRecordOption(TypedDict):
        title: str
        value: str
        is_default: bool

    def _to_json(
        self,
        *,
        entity: TextLanguages,
    ) -> TextLanguagesRecord:
        return {
            "config_name": TextLanguages.name,
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
                LanguageOption(
                    is_default=option["is_default"],
                    value=option["value"],
                    title=option["title"],
                )
                for option in data["options"]
            ]
        )

    @property
    def _config_class(self) -> type[TextLanguages]:
        return TextLanguages
