from funcy import first

from domain.constraints.base import Constraint
from domain.exceptions.constraint.display_unique import ItemDisplayTextMustBeUnique, ItemValueMustBeUnique
from domain.value_objects.base import ConfigEntry


class DisplayUniqueConstraint(Constraint):
    def __init__(
        self,
        *,
        items: list[ConfigEntry],
    ) -> None:
        self._items = items
        self._name = first(items).name

    def check(self) -> None:
        items_amount = len(self._items)

        item_values = {item.value for item in self._items}
        if len(item_values) != items_amount:
            raise ItemValueMustBeUnique(name=self._name)

        display_values = {item.get_display_text() for item in self._items}
        if len(display_values) != items_amount:
            raise ItemDisplayTextMustBeUnique(name=self._name)
