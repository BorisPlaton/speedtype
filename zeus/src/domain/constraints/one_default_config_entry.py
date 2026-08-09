from funcy import ilen

from domain.constraints.base import Constraint
from domain.exceptions.constraint.one_default import OneDefaultItemMustExist
from domain.value_objects.base import ConfigEntry


class NotMoreThanOneDefaultConfigEntryConstraint(Constraint):
    def __init__(self, *, items: list[ConfigEntry], exact_one: bool, name: str) -> None:
        self._items = items
        self._name = name
        self._exact_one = exact_one

    def check(self) -> None:
        defaults_amount = ilen(filter(lambda item: item.is_default, self._items))

        if not defaults_amount and self._exact_one:
            raise OneDefaultItemMustExist(name=self._name, actual_amount=defaults_amount)

        if defaults_amount > 1:
            raise OneDefaultItemMustExist(name=self._name, actual_amount=defaults_amount)
