import os
from typing import Optional

from ib_insync import IB

from app.settings import get_settings


def _generate_client_id(multiplier: int = 100) -> int:
    """
    Generate a unique client ID based on the process ID.

    Args:
        multiplier (int): Multiplier to ensure distinct client ID space.

    Returns:
        int: A unique client ID.
    """
    return os.getpid() * multiplier


class IBClientManager:
    """
    A managed IB client with automatic connect/disconnect logic.

    Supports use as a context manager:
        with IBClientManager() as ib:
            ib.positions()

    Attributes:
        ib (IB): The managed ib_insync.IB instance.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        client_id: Optional[int] = None,
    ) -> None:
        """
        Initialize the client manager.

        Args:
            host (Optional[str]): IB host. Defaults to settings.
            port (Optional[int]): IB port. Defaults to settings.
            client_id (Optional[int]): Client ID. Defaults to PID-based generator.
        """
        settings = get_settings()
        self.host = host or settings.IB_HOST
        self.port = port or settings.IB_PORT
        self.client_id = client_id or _generate_client_id()
        self.ib = IB()

    async def connect(self) -> IB:
        """
        Asynchronously connect to the IB server and return the client.

        Returns:
            IB: The connected IB client instance.
        """
        await self.ib.connectAsync(self.host, self.port, self.client_id)
        return self.ib

    def disconnect(self) -> None:
        """Disconnect from IB server if connected."""
        if self.ib.isConnected():
            self.ib.disconnect()

    async def __aenter__(self) -> IB:
        """Enter the context manager, returning the connected IB client."""
        return await self.connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager and clean up."""
        self.disconnect()
