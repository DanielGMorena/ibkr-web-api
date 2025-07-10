import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.ib.ib_client_manager import IBClientManager, _generate_client_id


def test_generate_client_id_uniqueness():
    base = os.getpid() * 100
    ids = {_generate_client_id() for _ in range(100)}
    assert all(base < cid < base + 100 for cid in ids)
    assert len(ids) == len(set(ids))  # all unique


@patch("app.ib.ib_client_manager.get_settings")
def test_ib_client_manager_defaults_used_when_config_missing(mock_get_settings):
    # Simulate missing settings (ib.host and ib.port are None)
    mock_settings = MagicMock()
    mock_settings.ib.host = None
    mock_settings.ib.port = None
    mock_get_settings.return_value = mock_settings

    with patch("app.ib.ib_client_manager.IB", autospec=True):
        manager = IBClientManager()

    assert manager.host == "127.0.0.1"
    assert manager.port == 7497
    assert isinstance(manager.client_id, int)


@patch("app.ib.ib_client_manager.get_settings")
def test_ib_client_manager_uses_config(mock_get_settings):
    # Simulate valid IB settings
    mock_settings = MagicMock()
    mock_settings.ib.host = "testhost"
    mock_settings.ib.port = 12345
    mock_get_settings.return_value = mock_settings

    with patch("app.ib.ib_client_manager.IB", autospec=True):
        manager = IBClientManager()

    assert manager.host == "testhost"
    assert manager.port == 12345
    assert isinstance(manager.client_id, int)  # still random


@patch("app.ib.ib_client_manager.IB")
@patch("app.ib.ib_client_manager.get_settings")
@pytest.mark.asyncio
async def test_ib_client_manager_connect_and_disconnect(
    mock_get_settings, mock_ib_class
):
    # Mock settings
    mock_settings = MagicMock()
    mock_settings.ib.host = "localhost"
    mock_settings.ib.port = 4001
    mock_get_settings.return_value = mock_settings

    # Mock IB instance with awaitable connectAsync
    mock_ib_instance = MagicMock()
    mock_ib_instance.connectAsync = AsyncMock()
    mock_ib_instance.isConnected.return_value = True
    mock_ib_instance.disconnect = MagicMock()
    mock_ib_class.return_value = mock_ib_instance

    manager = IBClientManager()

    # Test connect
    await manager.connect()
    mock_ib_instance.connectAsync.assert_awaited_once_with(
        manager.host, manager.port, manager.client_id
    )

    # Test disconnect
    manager.disconnect()
    mock_ib_instance.disconnect.assert_called_once()


@patch("app.ib.ib_client_manager.IB")
@patch("app.ib.ib_client_manager.get_settings")
@pytest.mark.asyncio
async def test_ib_client_manager_async_context(mock_get_settings, mock_ib_class):
    # Mock settings object
    mock_settings = MagicMock()
    mock_settings.ib.host = "localhost"
    mock_settings.ib.port = 4001
    mock_get_settings.return_value = mock_settings

    # Create IB mock instance with proper async and sync methods
    mock_ib_instance = MagicMock()
    mock_ib_instance.connectAsync = AsyncMock(
        return_value=mock_ib_instance
    )  # ✅ critical fix
    mock_ib_instance.isConnected.return_value = True
    mock_ib_instance.disconnect = MagicMock()
    mock_ib_class.return_value = mock_ib_instance

    # Run test using async context manager
    async with IBClientManager() as ib:
        assert ib is mock_ib_instance
        mock_ib_instance.connectAsync.assert_awaited_once()

    mock_ib_instance.disconnect.assert_called_once()
