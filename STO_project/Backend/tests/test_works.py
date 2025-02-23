import pytest
from test_auth import test_login

@pytest.mark.asyncio
async def test_add_work(client):
    token = await test_login(client)  # Передаём client!
    response = await client.post("/works", json={
        "car_id": 1,
        "name": "Замена масла",
        "status": "pending"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Замена масла"

@pytest.mark.asyncio
async def test_update_work(client):
    token = await test_login(client)  # Передаём client!
    response = await client.put("/works/1", json={
        "status": "completed"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

@pytest.mark.asyncio
async def test_get_works(client):
    token = await test_login(client)  # Передаём client!
    response = await client.get("/works", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
