from pydantic import Field

from domain.use_cases.types.text_words import TextWords
from inbound.http.contracts.base import BaseRequest, BaseResponse
from inbound.http.contracts.utils import load_example


class GetTextWordsRequestContract(BaseRequest):
    language: str = Field(
        description="The language of the words.",
    )
    words_length: str = Field(
        description="Expected length of the words.",
    )
    special_symbol_types: list[str] | None = Field(
        default=None,
        description="""
        If present, the response will also contain special symbols of the specified types in this field.
        """,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                load_example(name="get_text_words_request.json"),
            ]
        }
    }


class GetTextWordsResponseContract(BaseResponse):
    words: list[str] = Field(
        description="""
        Words for the input text. Words are in the language and size that were specified in the request.
        """
    )
    special_symbols: list[str] | None = Field(
        default=None,
        description="""
        Contains a list of all special symbols from the special symbol types that were requested by the user.
        """,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                load_example(name="get_text_words_response.json"),
            ]
        }
    }

    @classmethod
    def from_use_case(cls, *, data: TextWords) -> dict[str, object]:
        response = {
            "words": [word.value for word in data.words],
        }

        if data.special_symbols:
            response["special_symbols"] = [symbol.value for symbol in data.special_symbols]

        return response
