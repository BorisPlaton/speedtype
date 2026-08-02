from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from domain.use_cases.get_text_config import GetTextConfig


class DomainContainer(DeclarativeContainer):
    deps = providers.DependenciesContainer()

    get_text_config = providers.Singleton(
        GetTextConfig,
        words_length_repository=deps.words_length_repository,
        time_limits_repository=deps.time_limits_repository,
        text_languages_repository=deps.text_languages_repository,
        special_symbols_repository=deps.special_symbols_repository,
    )
