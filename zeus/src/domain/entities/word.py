import uuid
from abc import ABC
from dataclasses import dataclass
from uuid import UUID

from domain.constraints.not_empty_string import NotEmptyStringConstraint
from domain.value_objects.language import Language
from domain.value_objects.special_symbol import SpecialSymbol
from domain.value_objects.word_length import WordLength


@dataclass(kw_only=True, slots=True)
class Word(ABC):
    id: UUID
    value: str
    language_value: str
    word_length_value: str
    special_symbol_type: str | None

    @classmethod
    def new(
        cls,
        *,
        value: str,
        language: Language,
        word_length: WordLength,
        special_symbol: SpecialSymbol | None,
    ) -> Word:
        NotEmptyStringConstraint(value=value, name="Word's value").check()
        return cls(
            id=uuid.uuid4(),
            value=value,
            language_value=language.value,
            word_length_value=word_length.value,
            special_symbol_type=special_symbol.value if special_symbol else None,
        )
