import pytest
from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_root():
    response = client.get("/")
    assert response.status_code == 200