from domain.exceptions.base import DomainError


class DefaultOptionAlreadyExists(DomainError):
    def __init__(
        self,
        *,
        name: str,
        default_value: object,
    ) -> None:
        super().__init__(f"Default option of '{name}' already exists: '{default_value}'.")


class OptionWithValueDoesntExist(DomainError):
    def __init__(
        self,
        *,
        name: str,
        value: object,
    ) -> None:
        super().__init__(f"Unable to find the '{name}' option with '{value}' value.")
