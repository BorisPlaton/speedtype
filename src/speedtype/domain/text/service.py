from speedtype.domain.text.value_objects import TextConfig
from speedtype.outbound.zeus.client import ZeusClient


class TextService:
    def __init__(
        self,
        *,
        zeus_client: ZeusClient,
    ) -> None:
        self._zeus_client = zeus_client

    async def get_text_config(self) -> TextConfig:
        pass
