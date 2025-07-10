import httpx
import pytest
from fastapi import FastAPI

from app.main import create_app
from app.settings import get_settings

TEST_CONFIG_PATH = "tests/test_config.yml"


@pytest.fixture
def test_app(monkeypatch) -> FastAPI:
    monkeypatch.setenv("APP_CONFIG", TEST_CONFIG_PATH)
    from app.settings import get_settings

    get_settings.cache_clear()
    return create_app()


@pytest.mark.asyncio
async def test_app_starts_and_responds(test_app: FastAPI):
    """
    Test that the FastAPI app starts and returns a successful response from a built-in route.
    """
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/docs")
        assert response.status_code == 200


def test_app_metadata(test_app: FastAPI):
    """
    Test that app metadata (title, description) matches settings.
    """
    settings = get_settings()
    assert test_app.title == settings.fastapi.title
    assert test_app.description == settings.fastapi.description
