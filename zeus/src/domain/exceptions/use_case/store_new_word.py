from domain.exceptions.base import DomainError


class WordAlreadyExist(DomainError):
    def __init__(
        self,
        *,
        word: str,
    ) -> None:
        super().__init__(f"Word '{word}' already exist, those it can't be created again.")


class NonExistingOption(DomainError):
    def __init__(self, *, option: str, option_name: str) -> None:
        super().__init__(f"Option '{option}' doesn't exist in the '{option_name}' options.")
