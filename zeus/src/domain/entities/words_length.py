from dataclasses import dataclass
from typing import ClassVar

from domain.entities.config import Config
from domain.value_objects.word_length import WordLength


@dataclass(kw_only=True, slots=True)
class WordsLength(Config[WordLength]):
    is_required: ClassVar[bool] = True
    name: ClassVar[str] = "Words Length"
