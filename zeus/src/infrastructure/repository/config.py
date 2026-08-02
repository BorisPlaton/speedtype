from abc import ABC, abstractmethod

from pymongo import AsyncMongoClient

from domain.entities.config import Config
from domain.repository.config import ConfigRepository


class ConfigMongoDBRepository[Entity: Config](ConfigRepository[Entity], ABC):
    def __init__(
        self,
        *,
        mongo_client: AsyncMongoClient,
    ) -> None:
        self._collection = mongo_client.get_default_database()[self.collection_name]

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

    @property
    @abstractmethod
    def collection_name(self) -> str: ...

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
