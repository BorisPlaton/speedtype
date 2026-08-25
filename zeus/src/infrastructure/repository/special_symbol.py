from typing import TypedDict

from pymongo import UpdateOne

from domain.entities.special_symbol import SpecialSymbol
from domain.repository.special_symbol import SpecialSymbolsRepository
from domain.value_objects.special_symbol_type import SpecialSymbolType
from infrastructure.repository.base import BaseMongoDBRepository


class SpecialSymbolsMongoDBRepository(BaseMongoDBRepository, SpecialSymbolsRepository):
    class SpecialSymbolRecord(TypedDict):
        value: str
        special_symbol_type: str

    async def upsert_many(
        self,
        *,
        entries: list[SpecialSymbol],
    ) -> None:
        operations = [
            UpdateOne(
                {"value": entry.special_symbol_type},
                {"$set": self._to_json(entity=entry)},
                upsert=True,
            )
            for entry in entries
        ]
        await self._collection.bulk_write(operations)

    async def get_by_types(
        self,
        *,
        special_symbol_types: list[SpecialSymbolType],
    ) -> list[SpecialSymbol]:
        special_symbols = await self._collection.find(
            {
                "special_symbol_type": {"$in": [symbol_type.value for symbol_type in special_symbol_types]},
            }
        ).to_list()

        return [self._from_json(data=record) for record in special_symbols]

    @staticmethod
    def _to_json(
        *,
        entity: SpecialSymbol,
    ) -> SpecialSymbolRecord:
        return {
            "value": entity.value,
            "special_symbol_type": entity.special_symbol_type,
        }

    @staticmethod
    def _from_json(
        *,
        data: SpecialSymbolRecord,
    ) -> SpecialSymbol:
        return SpecialSymbol(
            value=data["value"],
            special_symbol_type=data["special_symbol_type"],
        )

    @property
    def _collection_name(self) -> str:
        return "special_symbols"
