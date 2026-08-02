from abc import ABC

from domain.entities.special_symbols import SpecialSymbols
from domain.repository.config import ConfigRepository


class SpecialSymbolsRepository(ConfigRepository[SpecialSymbols], ABC):
    pass
