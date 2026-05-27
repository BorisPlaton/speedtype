from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class APIResult[Ok, Error]:
    ok: Ok | None
    error: Error | None

    @classmethod
    def new(
        cls,
        *,
        ok: Ok | None = None,
        error: Error | None = None,
    ) -> APIResult:
        return APIResult(
            ok=ok,
            error=error,
        )

    def ok(self) -> Ok | None:
        return self.ok

    def error(self) -> Error | None:
        return self.error
