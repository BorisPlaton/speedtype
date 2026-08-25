from abc import ABC, abstractmethod

from pymongo import AsyncMongoClient


class BaseMongoDBRepository(ABC):
    def __init__(
        self,
        *,
        mongo_client: AsyncMongoClient,
    ) -> None:
        self._collection = mongo_client.get_default_database()[self._collection_name]

    @property
    @abstractmethod
    def _collection_name(self) -> str: ...
