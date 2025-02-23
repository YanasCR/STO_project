import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture(scope="module")
async def client():
    """Фикстура для тестового клиента FastAPI"""
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        yield ac
