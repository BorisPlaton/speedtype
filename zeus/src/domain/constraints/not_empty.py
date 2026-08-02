from domain.constraints.base import Constraint
from domain.exceptions.constraint.not_empty import StringCannotBeEmpty


class NotEmptyStringConstraint(Constraint):
    def __init__(self, *, value: str, name: str) -> None:
        self._value = value
        self._name = name

    def check(self) -> None:
        if not self._value:
            raise StringCannotBeEmpty(name=self._name)
