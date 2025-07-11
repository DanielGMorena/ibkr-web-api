from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
@patch("app.api.hist_mkt_data.IBClientManager")
async def test_get_hist_market_data_success(mock_ib_client_manager, async_client):
    # Setup mock IB client
    mock_ib = MagicMock()
    mock_contract = MagicMock()
    mock_ib.reqContractDetailsAsync = AsyncMock(
        return_value=[MagicMock(contract=mock_contract)]
    )
    mock_ib.qualifyContractsAsync = AsyncMock(return_value=[mock_contract])

    bar = MagicMock()
    bar.date = "2024-07-10"
    bar.open = 100
    bar.close = 110
    bar.__dict__ = {"date": "2024-07-10", "open": 100, "close": 110}

    mock_ib.reqHistoricalDataAsync = AsyncMock(return_value=[bar])
    mock_ib_client_manager.return_value.__aenter__.return_value = mock_ib

    response = await async_client.get("/histMktData/", params={"symbol": "AAPL"})
    assert response.status_code == 200
    assert response.json() == [{"date": "2024-07-10", "open": 100, "close": 110}]


@pytest.mark.asyncio
@patch("app.api.hist_mkt_data.IBClientManager")
async def test_get_hist_market_data_not_found(mock_ib_client_manager, async_client):
    # No contracts found
    mock_ib = MagicMock()
    mock_ib.reqContractDetailsAsync = AsyncMock(return_value=[])
    mock_ib_client_manager.return_value.__aenter__.return_value = mock_ib

    response = await async_client.get("/histMktData/", params={"symbol": "INVALID"})
    assert response.status_code == 404
    assert response.json()["detail"] == "No contract found for symbol 'INVALID'"


@pytest.mark.asyncio
@patch("app.api.hist_mkt_data.IBClientManager")
async def test_get_hist_market_data_internal_error(
    mock_ib_client_manager, async_client
):
    # Simulate unexpected error
    mock_ib = MagicMock()
    mock_ib.reqContractDetailsAsync = AsyncMock(side_effect=RuntimeError("Boom!"))
    mock_ib_client_manager.return_value.__aenter__.return_value = mock_ib

    response = await async_client.get("/histMktData/", params={"symbol": "FAIL"})
    assert response.status_code == 500
    assert "Boom!" in response.json()["detail"]


@pytest.mark.asyncio
@patch("app.api.hist_mkt_data.IBClientManager")
async def test_get_hist_market_data_with_end_datetime(
    mock_ib_client_manager, async_client
):
    # Test with end_datetime explicitly provided
    mock_ib = MagicMock()
    mock_contract = MagicMock()
    mock_ib.reqContractDetailsAsync = AsyncMock(
        return_value=[MagicMock(contract=mock_contract)]
    )
    mock_ib.qualifyContractsAsync = AsyncMock(return_value=[mock_contract])

    bar = MagicMock()
    bar.__dict__ = {"date": "2024-07-11", "open": 200, "close": 210}
    mock_ib.reqHistoricalDataAsync = AsyncMock(return_value=[bar])

    mock_ib_client_manager.return_value.__aenter__.return_value = mock_ib

    response = await async_client.get(
        "/histMktData/",
        params={
            "symbol": "MSFT",
            "duration": "5 D",
            "bar_size": "5 mins",
            "what_to_show": "MIDPOINT",
            "use_rth": 0,
            "end_datetime": "20240710 14:00:00",
        },
    )
    assert response.status_code == 200
    assert response.json()[0]["open"] == 200
    assert response.json()[0]["close"] == 210
