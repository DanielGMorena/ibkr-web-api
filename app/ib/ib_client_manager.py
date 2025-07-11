import logging
import os
import random
from typing import Optional, Type

from ib_insync import IB

from app.settings import get_settings

logger = logging.getLogger(__name__)


def _generate_client_id(multiplier: int = 100, offset_range: int = 50) -> int:
    """
    Generate a unique client ID based on the process ID and a random offset.

    Args:
        multiplier (int): Base multiplier for PID.
        offset_range (int): Range of random offset to avoid collisions in same process.

    Returns:
        int: A pseudo-unique client ID.
    """
    base = os.getpid() * multiplier
    offset = random.randint(1, offset_range)
    client_id = base + offset
    logger.debug(f"Generated client ID: {client_id} (base={base}, offset={offset})")
    return client_id


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
    ) -> None:
        """
        Initialize the client manager.

        Args:
            host (Optional[str]): IB host. Defaults to settings.
            port (Optional[int]): IB port. Defaults to settings.
        """
        settings = get_settings()

        ib_config = settings.ib
        self.host = host or ib_config.host
        if self.host is None:
            self.host = "127.0.0.1"
            logger.warning("No IB host specified; using default '127.0.0.1'")

        self.port = port or ib_config.port
        if self.port is None:
            self.port = 7497
            logger.warning("No IB port specified; using default 7497")

        self.client_id = _generate_client_id()
        self.ib = IB()  # type: ignore

        logger.info(
            f"IBClientManager initialized with host={self.host}, port={self.port}, client_id={self.client_id}"
        )

    async def connect(self) -> IB:
        """
        Asynchronously connect to the IB server and return the client.

        Returns:
            IB: The connected IB client instance.
        """
        logger.info(
            f"Connecting to IB server at {self.host}:{self.port} with client_id={self.client_id}"
        )
        await self.ib.connectAsync(self.host, self.port, self.client_id)
        logger.info("Connected to IB server")
        return self.ib

    def disconnect(self) -> None:
        """Disconnect from IB server if connected."""
        if self.ib.isConnected():
            logger.info("Disconnecting from IB server")
            self.ib.disconnect()  # type: ignore
            logger.info("Disconnected from IB server")
        else:
            logger.debug("IB client already disconnected")

    async def __aenter__(self) -> IB:
        """Enter the context manager, returning the connected IB client."""
        logger.debug("Entering IBClientManager context")
        return await self.connect()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """Exit the context manager and clean up."""
        logger.debug("Exiting IBClientManager context")
        self.disconnect()
