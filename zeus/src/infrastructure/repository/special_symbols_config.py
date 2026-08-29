from typing import TypedDict

from domain.entities.config import SpecialSymbols
from domain.value_objects.special_symbol_type import SpecialSymbolType
from infrastructure.repository.config import ConfigMongoDBRepository


class SpecialSymbolsConfigMongoDBRepository(ConfigMongoDBRepository[SpecialSymbols]):
    class SpecialSymbolsRecord(TypedDict):
        config_name: str
        options: list[SpecialSymbolsConfigMongoDBRepository.SpecialSymbolRecordOption]

    class SpecialSymbolRecordOption(TypedDict):
        title: str
        value: str
        is_default: bool

    def _to_json(
        self,
        *,
        entity: SpecialSymbols,
    ) -> SpecialSymbolsRecord:
        return {
            "config_name": SpecialSymbols.name,
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
        data: SpecialSymbolsRecord,
    ) -> SpecialSymbols:
        return SpecialSymbols(
            options=[
                SpecialSymbolType(
                    is_default=option["is_default"],
                    value=option["value"],
                    title=option["title"],
                )
                for option in data["options"]
            ]
        )

    @property
    def _config_class(self) -> type[SpecialSymbols]:
        return SpecialSymbols
