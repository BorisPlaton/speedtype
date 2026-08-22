from dataclasses import dataclass

from domain.constraints.not_empty_string import NotEmptyStringConstraint
from domain.value_objects.language_option import LanguageOption
from domain.value_objects.word_length_option import WordLengthOption


@dataclass(kw_only=True, slots=True)
class Word:
    value: str
    language_value: str
    word_length_value: str

    @classmethod
    def new(
        cls,
        *,
        word: str,
        language: LanguageOption,
        word_length: WordLengthOption,
    ) -> Word:
        NotEmptyStringConstraint(value=word, name="Word's value").check()
        return cls(
            value=word,
            language_value=language.value,
            word_length_value=word_length.value,
        )
