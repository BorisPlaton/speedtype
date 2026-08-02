from abc import ABC, abstractmethod


class UseCase[Result](ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Result: ...
