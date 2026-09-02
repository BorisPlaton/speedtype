from abc import ABC, abstractmethod


class Migration(ABC):
    @abstractmethod
    async def execute(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
