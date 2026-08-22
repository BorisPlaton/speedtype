from pydantic import Field

from speedtype.outbound.http.contracts import BaseResponse


class GetTextWordsResponseContract(BaseResponse):
    words: list[str]
    special_symbols: list[str] | None = Field(default=None)
