import pytest
from test_auth import test_login

@pytest.mark.asyncio
async def test_add_part(client):
    token = await test_login(client)  # Передаём client!
    response = await client.post("/parts", json={
        "car_id": 1,
        "name": "Масляный фильтр"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Масляный фильтр"

@pytest.mark.asyncio
async def test_get_parts(client):
    token = await test_login(client)  # Передаём client!
    response = await client.get("/parts/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
