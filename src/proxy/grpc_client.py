from logging import getLogger

import grpc

from _generated.grpc import (
    helloworld_pb2,  # noqa: F401; Re-export for convenience
    helloworld_pb2_grpc,
)

logger = getLogger(__name__)


class GrpcClient:
    """gRPC client."""

    def __init__(self, endpoint: str) -> None:  # noqa: D107
        self._channel = grpc.insecure_channel(endpoint)
        self.greeter = helloworld_pb2_grpc.GreeterStub(self._channel)

    def shutdown(self) -> None:
        """Shutdown client, cleaning up all resources."""
        logger.debug("Closing gRPC channel")
        self._channel.close()
