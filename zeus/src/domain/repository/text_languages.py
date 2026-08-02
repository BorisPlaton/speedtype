from abc import ABC

from domain.entities.text_languages import TextLanguages
from domain.repository.config import ConfigRepository


class TextLanguagesRepository(ConfigRepository[TextLanguages], ABC):
    pass
