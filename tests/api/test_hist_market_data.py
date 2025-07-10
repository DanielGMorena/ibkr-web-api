from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastapi import FastAPI

from app.main import create_app


@pytest.fixture
def test_app(monkeypatch) -> FastAPI:
    monkeypatch.setenv("APP_CONFIG", "tests/test_config.yml")
    from app.settings import get_settings

    get_settings.cache_clear()
    return create_app()


@pytest.mark.asyncio
@patch("app.api.hist_mkt_data.IBClientManager")
async def test_get_hist_market_data_success(mock_ib_client_manager, test_app):
    # Mock the IB client
    mock_ib = MagicMock()

    # Create fake contract and bar
    mock_contract = MagicMock()
    mock_ib.reqContractDetailsAsync = AsyncMock(
        return_value=[MagicMock(contract=mock_contract)]
    )
    mock_ib.qualifyContractsAsync = AsyncMock(return_value=[mock_contract])

    # ✅ Correct way to mock a "bar" with attributes
    bar_mock = MagicMock()
    bar_mock.date = "2024-07-10"
    bar_mock.open = 100
    bar_mock.close = 110
    mock_ib.reqHistoricalDataAsync = AsyncMock(return_value=[bar_mock])

    mock_ib_client_manager.return_value.__aenter__.return_value = mock_ib

    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/histMktData/", params={"symbol": "AAPL"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["open"] == 100
        assert data[0]["close"] == 110


@pytest.mark.asyncio
@patch("app.api.hist_mkt_data.IBClientManager")
async def test_get_hist_market_data_internal_error(mock_ib_client_manager, test_app):
    mock_ib = MagicMock()
    # Simulate an exception during contract request
    mock_ib.reqContractDetailsAsync = AsyncMock(side_effect=RuntimeError("IB failure"))
    mock_ib_client_manager.return_value.__aenter__.return_value = mock_ib

    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/histMktData/", params={"symbol": "AAPL"})
        assert response.status_code == 500
        assert "IB failure" in response.text
