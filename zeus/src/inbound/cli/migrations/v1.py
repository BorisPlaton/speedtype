from inbound.cli.migrations.base import Migration
from infrastructure.containers.application import ApplicationContainer


TIME_LIMITS = {
    "options": [
        {
            "is_default": True,
            "value": 15,
        },
        {
            "is_default": False,
            "value": 30,
        },
        {
            "is_default": False,
            "value": 60,
        },
        {
            "is_default": False,
            "value": 90,
        },
    ],
}
WORDS_LENGTH = {
    "options": [
        {
            "is_default": False,
            "value": "short",
            "title": "SHORT",
        },
        {
            "is_default": True,
            "value": "regular",
            "title": "REGULAR",
        },
        {
            "is_default": False,
            "value": "long",
            "title": "LONG",
        },
    ],
}
TEXT_LANGUAGES = {
    "options": [
        {
            "is_default": True,
            "value": "en",
            "title": "ENGLISH",
        },
        {
            "is_default": False,
            "value": "ua",
            "title": "UKRAINIAN",
        },
        {
            "is_default": False,
            "value": "ru",
            "title": "RUSSIAN",
        },
    ],
}
SPECIAL_SYMBOLS = {
    "options": [
        {
            "is_default": False,
            "value": "special_symbols",
            "title": "SPECIAL SYMBOLS",
        },
        {
            "is_default": False,
            "value": "punctuation",
            "title": "PUNCTUATION",
        },
    ],
}


class MigrationV1(Migration):
    def __init__(
        self,
        container: ApplicationContainer,
    ) -> None:
        mongo_client = container.infra.mongo_client()
        self._time_limits_collection = mongo_client.get_default_database()["time_limits"]
        self._words_length_collection = mongo_client.get_default_database()["words_length"]
        self._text_languages_collection = mongo_client.get_default_database()["text_languages"]
        self._special_symbols_collection = mongo_client.get_default_database()["special_symbols"]

    async def execute(self) -> None:

        if not await self._time_limits_collection.find_one():
            await self._time_limits_collection.insert_one(TIME_LIMITS)

        if not await self._words_length_collection.find_one():
            await self._words_length_collection.insert_one(WORDS_LENGTH)

        if not await self._text_languages_collection.find_one():
            await self._text_languages_collection.insert_one(TEXT_LANGUAGES)

        if not await self._special_symbols_collection.find_one():
            await self._special_symbols_collection.insert_one(SPECIAL_SYMBOLS)
