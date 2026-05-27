from abc import ABC, abstractmethod

from speedtype.outbound.http.session import HTTPSessionManager


class HTTPClient(ABC):
    def __init__(
        self,
        *,
        url: str,
    ) -> None:
        self._http_session = HTTPSessionManager().get(
            name=self.name,
            session_kwargs={
                "base_url": url,
            },
        )

    @property
    @abstractmethod
    def name(self) -> str: ...
