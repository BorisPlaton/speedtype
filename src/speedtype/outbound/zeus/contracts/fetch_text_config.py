from speedtype.domain.text.value_objects import (
    TextConfig,
    TextLanguage,
    TextModifier,
    TextOption,
    TimeLimit,
    WordsConfigs,
)
from speedtype.outbound.http.contracts import BaseResponse


class FetchTextConfigResponse(BaseResponse):
    text_languages: list[TextLanguageResponse]
    time_limits: list[TimeLimitResponse]
    word_config: WordConfigResponse

    def to_internal(self) -> TextConfig:
        return TextConfig(
            languages=tuple(
                TextLanguage(
                    title=language.title,
                    code=language.code,
                )
                for language in self.text_languages
            ),
            time_limits=tuple(
                TimeLimit(
                    seconds=time_limit.value_seconds,
                    display_text=time_limit.display_value,
                    is_default=time_limit.is_default,
                )
                for time_limit in self.time_limits
            ),
            words_configs=WordsConfigs(
                word_lengths=TextModifier(
                    is_required=self.word_config.word_lengths.is_required,
                    options=tuple(
                        TextOption(title=option.title, code=option.code, is_default=option.is_default)
                        for option in self.word_config.word_lengths.options
                    ),
                ),
                special_symbols=TextModifier(
                    is_required=self.word_config.special_symbols.is_required,
                    options=tuple(
                        TextOption(title=option.title, code=option.code, is_default=option.is_default)
                        for option in self.word_config.special_symbols.options
                    ),
                ),
            ),
        )


class TextLanguageResponse(BaseResponse):
    title: str
    code: str
    is_default: bool


class TimeLimitResponse(BaseResponse):
    value_seconds: int
    display_value: str
    is_default: bool


class WordConfigResponse(BaseResponse):
    word_lengths: TextModifierResponse
    special_symbols: TextModifierResponse


class TextModifierResponse(BaseResponse):
    options: list[TextOptionResponse]
    is_required: bool


class TextOptionResponse(BaseResponse):
    title: str
    code: str
    is_default: bool
