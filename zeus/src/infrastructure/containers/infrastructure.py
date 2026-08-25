from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Provider, Singleton
from pymongo import AsyncMongoClient

from domain.repository.config import (
    SpecialSymbolsConfigRepository,
    TextLanguagesConfigRepository,
    TimeLimitsConfigRepository,
    WordsLengthConfigRepository,
)
from domain.repository.special_symbol import SpecialSymbolsRepository
from domain.repository.word import WordsRepository
from infrastructure.repository.special_symbol import SpecialSymbolsMongoDBRepository
from infrastructure.repository.special_symbols_config import SpecialSymbolsConfigMongoDBRepository
from infrastructure.repository.text_languages_config import TextLanguagesConfigMongoDBRepository
from infrastructure.repository.time_limits_config import TimeLimitsConfigMongoDBRepository
from infrastructure.repository.word import WordsMongoDBRepository
from infrastructure.repository.words_length_config import WordsLengthConfigMongoDBRepository


class InfrastructureContainer(DeclarativeContainer):
    config = Configuration()

    mongo_client: Provider[AsyncMongoClient] = Singleton(
        AsyncMongoClient,
        host=config.mongodb.uri,
        username=config.mongodb.USERNAME,
        password=config.mongodb.PASSWORD,
        timeoutMS=config.mongodb.TIMEOUT,
        authSource=config.mongodb.AUTH_SOURCE,
    )

    special_symbols_config_repository: Provider[SpecialSymbolsConfigRepository] = Singleton(
        SpecialSymbolsConfigMongoDBRepository,
        mongo_client=mongo_client,
    )
    text_languages_config_repository: Provider[TextLanguagesConfigRepository] = Singleton(
        TextLanguagesConfigMongoDBRepository,
        mongo_client=mongo_client,
    )
    time_limits_repository: Provider[TimeLimitsConfigRepository] = Singleton(
        TimeLimitsConfigMongoDBRepository,
        mongo_client=mongo_client,
    )
    words_length_config_repository: Provider[WordsLengthConfigRepository] = Singleton(
        WordsLengthConfigMongoDBRepository,
        mongo_client=mongo_client,
    )
    words_repository: Provider[WordsRepository] = Singleton(
        WordsMongoDBRepository,
        mongo_client=mongo_client,
    )
    special_symbols_repository: Provider[SpecialSymbolsRepository] = Singleton(
        SpecialSymbolsMongoDBRepository,
        mongo_client=mongo_client,
    )
