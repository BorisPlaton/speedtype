from abc import ABC

from domain.entities.words_length import WordsLength
from domain.repository.config import ConfigRepository


class WordsLengthRepository(ConfigRepository[WordsLength], ABC):
    pass
