from contextlib import AbstractContextManager
from logging import getLogger
from types import TracebackType
from typing import Self

import grpc
from grpc_health.v1 import health_pb2_grpc

from _generated.grpc import helloworld_pb2_grpc

logger = getLogger(__name__)


class Client(AbstractContextManager):
    """IPC client."""

    def __init__(self, address: str) -> None:
        """Initialize IPC client.

        Args:
            address: Target IPC address.
        """
        logger.debug("Establishing gRPC connection to %s", address)
        self._channel = grpc.insecure_channel(address)

        # Init stubs to use it conveniently
        self.health = health_pb2_grpc.HealthStub(self._channel)
        self.greeter = helloworld_pb2_grpc.GreeterStub(self._channel)

    def close(self) -> None:
        """Shutdown client, cleaning up all resources."""
        logger.debug("Closing gRPC channel")
        self._channel.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> bool | None:
        self.close()
        return None


class ClientFactory:
    """IPC client factory."""

    def __init__(self, address: str) -> None:
        """Initialize IPC client factory.

        Args:
            address: Target IPC address.
        """
        self._address = address

    def get_client(self) -> Client:
        """Return new client."""
        return Client(address=self._address)
