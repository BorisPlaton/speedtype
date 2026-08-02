from domain.exceptions.base import DomainError


class OneDefaultItemMustExist(DomainError):
    def __init__(
        self,
        *,
        name: str,
        actual_amount: int,
    ) -> None:
        super().__init__(f"Expected one default item of '{name}'. Got {actual_amount}.")
