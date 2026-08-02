from abc import ABC, abstractmethod

from domain.entities.config import Config


class ConfigRepository[Entity: Config](ABC):
    @abstractmethod
    async def get(self) -> Entity: ...

    @abstractmethod
    async def upsert(self, *, config: Entity) -> None: ...
