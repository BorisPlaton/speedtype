class APIError(Exception):
    def __init__(
        self,
        *,
        reason: str,
        details: object | None = None,
    ) -> None:
        self._reason = reason
        self._details = details

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def details(self) -> object | None:
        return self._details


class FailedRequest(APIError):
    def __init__(
        self,
        *,
        reason: str = "Failed to make request to the zeus.",
        details: object | None = None,
    ) -> None:
        super().__init__(reason=reason, details=details)


class InvalidResponse(APIError):
    pass
