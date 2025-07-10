import os
from unittest.mock import MagicMock, patch

import pytest

from app.ib.ib_client_manager import IBClientManager, _generate_client_id


def test_generate_client_id_uniqueness():
    base = os.getpid() * 100
    ids = {_generate_client_id() for _ in range(100)}
    assert all(base < cid < base + 100 for cid in ids)
    assert len(ids) == len(set(ids))  # all unique


@patch("app.ib.ib_client_manager.get_settings")
def test_ib_client_manager_defaults_used_when_config_missing(mock_get_settings):
    mock_get_settings.return_value.get.return_value = None

    with patch("app.ib.ib_client_manager.IB", autospec=True):
        manager = IBClientManager()

    assert manager.host == "127.0.0.1"
    assert manager.port == 7497
    assert isinstance(manager.client_id, int)


@patch("app.ib.ib_client_manager.get_settings")
def test_ib_client_manager_uses_config(mock_get_settings):
    mock_get_settings.return_value.get.return_value = {
        "host": "testhost",
        "port": 12345,
        "client_id": 99,
    }

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
    mock_get_settings.return_value.get.return_value = {}
    mock_ib_instance = MagicMock()
    mock_ib_instance.isConnected.return_value = True
    mock_ib_class.return_value = mock_ib_instance

    manager = IBClientManager()

    await manager.connect()
    mock_ib_instance.connectAsync.assert_awaited_once()

    manager.disconnect()
    mock_ib_instance.disconnect.assert_called_once()


@patch("app.ib.ib_client_manager.IB")
@patch("app.ib.ib_client_manager.get_settings")
@pytest.mark.asyncio
async def test_ib_client_manager_async_context(mock_get_settings, mock_ib_class):
    mock_get_settings.return_value.get.return_value = {}
    mock_ib_instance = MagicMock()
    mock_ib_instance.connectAsync.return_value = mock_ib_instance
    mock_ib_instance.isConnected.return_value = True
    mock_ib_class.return_value = mock_ib_instance

    async with IBClientManager() as ib:
        assert ib is mock_ib_instance
        mock_ib_instance.connectAsync.assert_awaited_once()

    mock_ib_instance.disconnect.assert_called_once()
