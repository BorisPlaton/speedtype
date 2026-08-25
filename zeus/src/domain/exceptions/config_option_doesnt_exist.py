from domain.exceptions.base import DomainError


class ConfigOptionDoesntExist(DomainError):
    def __init__(
        self,
        *,
        config_name: str,
        non_existed_option: str,
    ) -> None:
        super().__init__(f"Option '{non_existed_option}' doesn't exist in config '{config_name}'.")
