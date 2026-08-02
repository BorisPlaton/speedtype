from speedtype.outbound.http.contracts import BaseResponse


class TextConfigResponseContract(BaseResponse):
    special_symbols: ConfigResponseContract[str]
    text_languages: ConfigResponseContract[str]
    time_limits: ConfigResponseContract[int]
    words_length: ConfigResponseContract[str]


class ConfigResponseContract[OptionValue](BaseResponse):
    name: str
    options: list[ConfigOptionResponseContract[OptionValue]]
    is_required: bool


class ConfigOptionResponseContract[Value](BaseResponse):
    value: Value
    title: str
    is_default: bool
