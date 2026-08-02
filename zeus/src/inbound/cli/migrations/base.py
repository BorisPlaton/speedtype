from abc import ABC, abstractmethod


class Migration(ABC):
    @abstractmethod
    async def execute(self) -> None: ...
