import pytest
from pymongo import AsyncMongoClient

from infrastructure.containers.application import ApplicationContainer
from infrastructure.migrations.migrations_list import MigrationID


async def test_migrate_command_run_all_migrations(
    container: ApplicationContainer,
    clean_mongodb: None,  # noqa: ARG001
) -> None:
    runner = container.infra.migrations_runner()

    # ruff: disable[SLF001]
    mongo_client: AsyncMongoClient = container.infra.mongo_client()
    words_collection = container.infra.words_repository()._collection_name
    special_symbols_collection = container.infra.special_symbols_repository()._collection_name
    text_config_collection = container.infra.text_languages_config_repository()._collection_name
    # ruff: enable[SLF001]

    assert not await mongo_client.get_default_database()[words_collection].find({}).to_list()
    assert not await mongo_client.get_default_database()[special_symbols_collection].find({}).to_list()
    assert not await mongo_client.get_default_database()[text_config_collection].find({}).to_list()

    await runner.run()

    assert await mongo_client.get_default_database()[words_collection].find({}).to_list()
    assert await mongo_client.get_default_database()[special_symbols_collection].find({}).to_list()
    assert await mongo_client.get_default_database()[text_config_collection].find({}).to_list()


async def test_migrate_command_run_only_specified_migration(
    container: ApplicationContainer,
    clean_mongodb: None,  # noqa: ARG001
) -> None:
    runner = container.infra.migrations_runner()

    # ruff: disable[SLF001]
    mongo_client: AsyncMongoClient = container.infra.mongo_client()
    words_collection = container.infra.words_repository()._collection_name
    special_symbols_collection = container.infra.special_symbols_repository()._collection_name
    text_config_collection = container.infra.text_languages_config_repository()._collection_name
    # ruff: enable[SLF001]

    assert not await mongo_client.get_default_database()[words_collection].find({}).to_list()
    assert not await mongo_client.get_default_database()[special_symbols_collection].find({}).to_list()
    assert not await mongo_client.get_default_database()[text_config_collection].find({}).to_list()

    await runner.run(migration_id=MigrationID.V1)

    assert not await mongo_client.get_default_database()[words_collection].find({}).to_list()
    assert not await mongo_client.get_default_database()[special_symbols_collection].find({}).to_list()
    assert await mongo_client.get_default_database()[text_config_collection].find({}).to_list()


@pytest.mark.parametrize(
    "migration_id",
    [
        "v1-1",
        "qwerty",
        "v0",
    ],
)
async def test_migrate_command_fails_with_invalid_migration_id(
    migration_id: str,
    container: ApplicationContainer,
) -> None:
    runner = container.infra.migrations_runner()

    with pytest.raises(ValueError):
        await runner.run(migration_id=migration_id)
