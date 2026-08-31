import pytest
from httpx2 import AsyncClient


@pytest.mark.parametrize(
    "language, word_length, special_symbols",
    [
        (language, word_length, special_symbols)
        for language in ("ua", "en", "ru")
        for word_length in ("short", "long", "regular")
        for special_symbols in (None, ["special_symbols"], ["punctuation"], ["special_symbols", "punctuation"])
    ],
)
async def test_endpoint_returns_words_and_special_symbols(
    zeus_client: AsyncClient,
    snapshot: dict[str, object],
    language: str,
    word_length: str,
    special_symbols: list[str],
) -> None:
    response = await zeus_client.post(
        "/text/words",
        json={
            "language": language,
            "words_length": word_length,
            "special_symbol_types": special_symbols,
        },
    )

    assert response.status_code == 200, response.text
    assert response.json() == snapshot


@pytest.mark.parametrize(
    "language, word_length, special_symbols",
    [
        ("en", "short", ["qwerty"]),
        ("qwerty", "long", None),
        ("ua", "qwerty", ["punctuation"]),
    ],
)
async def test_endpoint_rejects_values(
    zeus_client: AsyncClient,
    snapshot: dict[str, object],
    language: str,
    word_length: str,
    special_symbols: list[str],
) -> None:
    response = await zeus_client.post(
        "/text/words",
        json={
            "language": language,
            "words_length": word_length,
            "special_symbol_types": special_symbols,
        },
    )

    assert response.status_code == 400, response.text
    assert response.json() == snapshot
