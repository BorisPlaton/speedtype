from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Provider, Singleton
from pymongo import AsyncMongoClient

from domain.repository.special_symbols import SpecialSymbolsRepository
from domain.repository.text_languages import TextLanguagesRepository
from domain.repository.time_limits import TimeLimitsRepository
from domain.repository.words_length import WordsLengthRepository
from infrastructure.repository.special_symbols import SpecialSymbolsMongoDBRepository
from infrastructure.repository.text_languages import TextLanguagesMongoDBRepository
from infrastructure.repository.time_limits import TimeLimitsMongoDBRepository
from infrastructure.repository.words_length import WordsLengthMongoDBRepository


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

    special_symbols_repository: Provider[SpecialSymbolsRepository] = Singleton(
        SpecialSymbolsMongoDBRepository,
        mongo_client=mongo_client,
    )
    text_languages_repository: Provider[TextLanguagesRepository] = Singleton(
        TextLanguagesMongoDBRepository,
        mongo_client=mongo_client,
    )
    time_limits_repository: Provider[TimeLimitsRepository] = Singleton(
        TimeLimitsMongoDBRepository,
        mongo_client=mongo_client,
    )
    words_length_repository: Provider[WordsLengthRepository] = Singleton(
        WordsLengthMongoDBRepository,
        mongo_client=mongo_client,
    )
