from unittest.mock import MagicMock, patch

from httpx2 import AsyncClient


async def test_non_existing_endpoint(
    zeus_client: AsyncClient,
    snapshot: dict[str, object],
) -> None:
    response = await zeus_client.get("/non/existing/endpoint")

    assert response.status_code == 404, response.text
    assert response.json() == snapshot


@patch("domain.use_cases.get_text_config.GetTextConfig.execute", MagicMock(side_effect=Exception()))
async def test_internal_server_error(
    zeus_client: AsyncClient,
    snapshot: dict[str, object],
) -> None:
    response = await zeus_client.get("/text/config")

    assert response.status_code == 500, response.text
    assert response.json() == snapshot
