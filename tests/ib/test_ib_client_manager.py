import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.ib.ib_client_manager import IBClientManager, _generate_client_id


def test_generate_client_id(monkeypatch):
    """Test that the client ID is based on PID times multiplier."""
    monkeypatch.setattr(os, "getpid", lambda: 123)
    assert _generate_client_id() == 12300
    assert _generate_client_id(multiplier=5) == 615


@patch("app.ib.ib_client_manager.IB", autospec=True)
@patch("app.ib.ib_client_manager.get_settings")
def test_ib_client_manager_init_defaults(mock_get_settings, mock_ib_class):
    """Test initialization with default config values."""
    mock_get_settings.return_value = MagicMock(IB_HOST="localhost", IB_PORT=4001)

    manager = IBClientManager()

    assert manager.host == "localhost"
    assert manager.port == 4001
    assert isinstance(manager.client_id, int)
    assert manager.ib is mock_ib_class.return_value


@pytest.mark.asyncio
@patch("app.ib.ib_client_manager.IB", autospec=True)
async def test_ib_client_manager_connect(mock_ib_class):
    mock_ib = mock_ib_class.return_value
    mock_ib.connectAsync = AsyncMock()

    manager = IBClientManager("localhost", 4001, 123)
    await manager.connect()

    mock_ib.connectAsync.assert_awaited_once_with("localhost", 4001, 123)


@patch("app.ib.ib_client_manager.IB", autospec=True)
def test_ib_client_manager_disconnect(mock_ib_class):
    """Test the disconnect() method is called only if connected."""
    mock_ib = mock_ib_class.return_value

    # Case 1: isConnected = True
    mock_ib.isConnected.return_value = True
    manager = IBClientManager()
    manager.disconnect()
    mock_ib.disconnect.assert_called_once()

    # Reset and test Case 2: isConnected = False
    mock_ib.disconnect.reset_mock()
    mock_ib.isConnected.return_value = False
    manager.disconnect()
    mock_ib.disconnect.assert_not_called()


@pytest.mark.asyncio
@patch("app.ib.ib_client_manager.IB", autospec=True)
async def test_ib_client_manager_async_context(mock_ib_class):
    mock_ib = mock_ib_class.return_value
    mock_ib.isConnected.return_value = True
    mock_ib.connectAsync = AsyncMock()

    async with IBClientManager("localhost", 4001, 123) as ib:
        mock_ib.connectAsync.assert_awaited_once_with("localhost", 4001, 123)
        assert ib is mock_ib

    mock_ib.disconnect.assert_called_once()
