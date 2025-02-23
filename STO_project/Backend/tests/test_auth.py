import pytest

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "role": "admin"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login(client):
    response = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_get_profile(client):
    token = await test_login(client)  # Передаём client!
    response = await client.get("/auth/profile", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
