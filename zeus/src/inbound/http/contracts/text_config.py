from pydantic import Field

from domain.entities.config import Config
from domain.use_cases.types.text_config import TextConfig
from inbound.http.contracts.base import BaseResponse
from inbound.http.utils import load_example


class GetTextConfigResponseContract(BaseResponse):
    """
    The text configuration the user can use to customize the input text.
    """

    special_symbols: ConfigResponseContract[str] = Field(
        description="Special symbol types, that will be mixed with regular words.",
    )
    text_languages: ConfigResponseContract[str] = Field(
        description="Languages, in which user can type words.",
    )
    time_limits: ConfigResponseContract[int] = Field(
        description="Time of the single typing session.",
    )
    words_length: ConfigResponseContract[str] = Field(
        description="Words' length that will appear in the input text.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                load_example(name="get_text_config_response.json"),
            ]
        }
    }

    @classmethod
    def from_use_case(
        cls,
        *,
        data: TextConfig,
    ) -> GetTextConfigResponseContract:
        return GetTextConfigResponseContract(
            **{
                "special_symbols": cls._serialize_config(config=data.special_symbols),
                "text_languages": cls._serialize_config(config=data.text_languages),
                "time_limits": cls._serialize_config(config=data.time_limits),
                "words_length": cls._serialize_config(config=data.words_length),
            }
        )

    @classmethod
    def _serialize_config(
        cls,
        *,
        config: Config,
    ) -> dict[str, object]:
        return {
            "name": config.name,
            "options": [
                {
                    "value": option.value,
                    "title": option.get_display_text(),
                    "is_default": option.is_default,
                }
                for option in config.options
            ],
            "is_required": config.is_required,
        }


class ConfigResponseContract[OptionValue](BaseResponse):
    """
    Specific configuration details.
    """

    name: str = Field(
        description="The human-readable name of the configuration.",
    )
    options: list[ConfigOptionResponseContract[OptionValue]] = Field(
        description="The available options for this configuration.",
    )
    is_required: bool = Field(
        description="Flag that indicates whether one of the configuration options has to be selected by the user.",
    )


class ConfigOptionResponseContract[Value](BaseResponse):
    """
    Option details of the specific configuration.
    """

    value: Value = Field(
        description="The actual value of the option. Should be used when referencing this option.",
    )
    title: str = Field(
        description="The human-readable name of the option.",
    )
    is_default: bool = Field(
        description="Is this option selected by default or not.",
    )
