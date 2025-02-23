import pytest
from test_auth import test_login

@pytest.mark.asyncio
async def test_add_car(client):
    token = await test_login(client)  # Передаём client!
    response = await client.post("/cars", json={
        "brand": "Toyota",
        "model": "Camry",
        "year": 2020,
        "vin": "1234567890ABCDEFG"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["brand"] == "Toyota"

@pytest.mark.asyncio
async def test_get_cars(client):
    token = await test_login(client)  # Передаём client!
    response = await client.get("/cars", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_delete_car(client):
    token = await test_login(client)  # Передаём client!
    response = await client.delete("/cars/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
