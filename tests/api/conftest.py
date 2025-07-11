from collections.abc import AsyncGenerator

import httpx
import pytest

from app.app_factory import create_app


@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator[httpx.AsyncClient, None, None]:
    """
    Pytest fixture that provides a TestClient for the FastAPI app.

    This fixture uses a test-specific config file and yields a reusable
    client instance for sending requests to the app during tests.

    Yields:
        Generator[TestClient, None, None]: The FastAPI test client.
    """
    app = create_app(config_path="tests/test_config.yml")
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
