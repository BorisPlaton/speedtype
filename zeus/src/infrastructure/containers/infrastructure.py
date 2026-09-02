from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Provider, Singleton
from pymongo import AsyncMongoClient

from domain.repository.config import (
    SpecialSymbolsConfigRepository,
    TextLanguagesConfigRepository,
    TimeLimitsConfigRepository,
    WordsLengthConfigRepository,
)
from domain.repository.special_symbols import SpecialSymbolsRepository
from domain.repository.word import WordsRepository
from infrastructure.migrations.runner import MigrationRunner
from infrastructure.migrations.versions.v1 import MigrationV1
from infrastructure.migrations.versions.v2 import MigrationV2
from infrastructure.repository.migrations import MigrationsRepository
from infrastructure.repository.special_symbols import SpecialSymbolsMongoDBRepository
from infrastructure.repository.special_symbols_config import SpecialSymbolsConfigMongoDBRepository
from infrastructure.repository.text_languages_config import TextLanguagesConfigMongoDBRepository
from infrastructure.repository.time_limits_config import TimeLimitsConfigMongoDBRepository
from infrastructure.repository.word import WordsMongoDBRepository
from infrastructure.repository.words_length_config import WordsLengthConfigMongoDBRepository


class InfrastructureContainer(DeclarativeContainer):
    config = Configuration()

    mongo_client: Provider[AsyncMongoClient] = Singleton(
        AsyncMongoClient,
        host=config.mongodb.URI,
        timeoutMS=config.mongodb.TIMEOUT,
    )

    special_symbols_config_repository: Provider[SpecialSymbolsConfigRepository] = Singleton(
        SpecialSymbolsConfigMongoDBRepository,
        mongo_client=mongo_client,
    )
    text_languages_config_repository: Provider[TextLanguagesConfigRepository] = Singleton(
        TextLanguagesConfigMongoDBRepository,
        mongo_client=mongo_client,
    )
    time_limits_config_repository: Provider[TimeLimitsConfigRepository] = Singleton(
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

    migration_v1: Provider[MigrationV1] = Singleton(
        MigrationV1,
        time_limits_config_repository=time_limits_config_repository,
        words_length_config_repository=words_length_config_repository,
        text_languages_config_repository=text_languages_config_repository,
        special_symbols_config_repository=special_symbols_config_repository,
    )
    migration_v2: Provider[MigrationV2] = Singleton(
        MigrationV2,
        words_length_config_repository=words_length_config_repository,
        text_languages_config_repository=text_languages_config_repository,
        special_symbols_config_repository=special_symbols_config_repository,
        words_repository=words_repository,
        special_symbols_repository=special_symbols_repository,
    )
    migrations_repository: Provider[MigrationsRepository] = Singleton(
        MigrationsRepository,
        migration_v1=migration_v1,
        migration_v2=migration_v2,
    )
    migrations_runner: Provider[MigrationRunner] = Singleton(
        MigrationRunner,
        migrations_repository=migrations_repository,
    )
