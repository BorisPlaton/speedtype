from abc import ABC, abstractmethod

from domain.entities.config import Config, SpecialSymbols, TextLanguages, TimeLimits, WordsLength


class ConfigRepository[Entity: Config](ABC):
    @abstractmethod
    async def get(self) -> Entity: ...

    @abstractmethod
    async def upsert(self, *, config: Entity) -> None: ...


class TextLanguagesConfigRepository(ConfigRepository[TextLanguages], ABC):
    pass


class SpecialSymbolsConfigRepository(ConfigRepository[SpecialSymbols], ABC):
    pass


class TimeLimitsConfigRepository(ConfigRepository[TimeLimits], ABC):
    pass


class WordsLengthConfigRepository(ConfigRepository[WordsLength], ABC):
    pass
