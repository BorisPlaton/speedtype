from abc import ABC, abstractmethod

from domain.entities.special_symbol import SpecialSymbol
from domain.value_objects.special_symbol_type import SpecialSymbolType


class SpecialSymbolsRepository(ABC):
    @abstractmethod
    async def upsert_many(
        self,
        *,
        entries: list[SpecialSymbol],
    ) -> None: ...

    @abstractmethod
    async def get_by_types(
        self,
        *,
        special_symbol_types: list[SpecialSymbolType],
    ) -> list[SpecialSymbol]: ...
