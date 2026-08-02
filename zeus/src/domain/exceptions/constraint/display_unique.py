from domain.exceptions.base import DomainError


class ItemValueMustBeUnique(DomainError):
    def __init__(
        self,
        *,
        name: str,
    ) -> None:
        super().__init__(f"Entries of '{name}' have duplicated values")


class ItemDisplayTextMustBeUnique(DomainError):
    def __init__(
        self,
        *,
        name: str,
    ) -> None:
        super().__init__(f"Entries of '{name}' have duplicated values")
