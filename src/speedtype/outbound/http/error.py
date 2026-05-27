from typing import Any


class APIError(Exception):
    def __init__(
        self,
        *,
        reason: str,
        details: Any = None,
    ) -> None:
        self._reason = reason
        self._details = details

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def details(self) -> Any:
        return self._details


class FailedRequest(APIError):
    pass


class InvalidResponse(APIError):
    pass
