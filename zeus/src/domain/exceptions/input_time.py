from domain.exceptions.base import DomainError


class InputTimeMustBeGreaterThanZero(DomainError):
    def __init__(
        self,
        *,
        actual_time: int,
    ) -> None:
        super().__init__(f"Input time must be greater than zero. Got: {actual_time}.")
