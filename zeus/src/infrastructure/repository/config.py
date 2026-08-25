from abc import ABC, abstractmethod

from domain.entities.config import Config
from domain.repository.config import ConfigRepository
from infrastructure.repository.base import BaseMongoDBRepository


class ConfigMongoDBRepository[Entity: Config](
    ConfigRepository[Entity],
    BaseMongoDBRepository,
    ABC,
):
    async def get(self) -> Entity | None:
        result = await self._collection.find_one()

        if not result:
            return None

        return self._from_json(data=result)

    async def upsert(
        self,
        *,
        config: Entity,
    ) -> None:
        data = self._to_json(entity=config)
        await self._collection.replace_one(
            filter={},
            replacement=data,
            upsert=True,
        )

    @abstractmethod
    def _to_json(
        self,
        *,
        entity: Entity,
    ) -> dict[str, object]: ...

    @abstractmethod
    def _from_json(
        self,
        *,
        data: dict[str, object],
    ) -> Entity: ...
