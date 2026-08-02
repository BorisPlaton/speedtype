from domain.entities.config import Config
from domain.use_cases.types.text_config import TextConfig
from inbound.http.contracts.base import BaseResponse


class TextConfigResponseContract(BaseResponse):
    special_symbols: ConfigResponseContract[str]
    text_languages: ConfigResponseContract[str]
    time_limits: ConfigResponseContract[int]
    words_length: ConfigResponseContract[str]

    @classmethod
    def from_use_case(
        cls,
        *,
        data: TextConfig,
    ) -> TextConfigResponseContract:
        return TextConfigResponseContract(
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
    name: str
    options: list[ConfigOptionResponseContract[OptionValue]]
    is_required: bool


class ConfigOptionResponseContract[Value](BaseResponse):
    value: Value
    title: str
    is_default: bool
