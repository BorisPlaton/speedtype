from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from domain.use_cases.get_text_config import GetTextConfig
from domain.use_cases.get_text_words import GetTextWords


class DomainContainer(DeclarativeContainer):
    deps = providers.DependenciesContainer()

    get_text_config = providers.Singleton(
        GetTextConfig,
        words_length_config_repository=deps.words_length_config_repository,
        time_limits_config_repository=deps.time_limits_repository,
        text_languages_config_repository=deps.text_languages_config_repository,
        special_symbols_config_repository=deps.special_symbols_config_repository,
    )
    get_text_words = providers.Singleton(
        GetTextWords,
        words_repository=deps.words_repository,
        special_symbols_repository=deps.special_symbols_repository,
        words_length_config_repository=deps.words_length_config_repository,
        text_languages_config_repository=deps.text_languages_config_repository,
        special_symbols_config_repository=deps.special_symbols_config_repository,
    )
