from abc import ABC, abstractmethod


class Constraint(ABC):
    @abstractmethod
    def check(self) -> None: ...
