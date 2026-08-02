from domain.exceptions.base import DomainError


class StringCannotBeEmpty(DomainError):
    def __init__(
        self,
        *,
        name: str,
    ) -> None:
        super().__init__(f"Value of '{name}' string cannot be empty")
