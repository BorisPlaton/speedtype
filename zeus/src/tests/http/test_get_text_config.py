from httpx2 import AsyncClient


async def test_endpoint_returns_config(
    zeus_client: AsyncClient,
    snapshot: dict[str, object],
) -> None:
    response = await zeus_client.get("/text/config")

    assert response.status_code == 200, response.text
    assert response.json() == snapshot
