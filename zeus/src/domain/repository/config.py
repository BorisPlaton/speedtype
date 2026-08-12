from abc import ABC, abstractmethod

from domain.entities.config import Config, SpecialSymbols, TextLanguages, TimeLimits, WordsLength


class ConfigRepository[Entity: Config](ABC):
    @abstractmethod
    async def get(self) -> Entity: ...

    @abstractmethod
    async def upsert(self, *, config: Entity) -> None: ...


class TextLanguagesRepository(ConfigRepository[TextLanguages], ABC):
    pass


class SpecialSymbolsRepository(ConfigRepository[SpecialSymbols], ABC):
    pass


class TimeLimitsRepository(ConfigRepository[TimeLimits], ABC):
    pass


class WordsLengthRepository(ConfigRepository[WordsLength], ABC):
    pass
