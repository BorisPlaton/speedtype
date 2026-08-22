from pydantic import Field

from domain.use_cases.types.text_words import TextWords
from inbound.http.contracts.base import BaseRequest, BaseResponse


class GetTextWordsRequestContract(BaseRequest):
    language: str
    words_length: str
    special_symbol_types: list[str] | None = Field(default=None)


class GetTextWordsResponseContract(BaseResponse):
    words: list[str]
    special_symbols: list[str] | None = Field(default=None)

    @classmethod
    def from_use_case(cls, *, data: TextWords) -> dict[str, object]:
        response = {
            "words": [word.value for word in data.words],
        }

        if data.special_symbols:
            response["special_symbols"] = [symbol.value for symbol in data.special_symbols]

        return response
