from concurrent import futures
from logging import getLogger

import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

from _generated.grpc import helloworld_pb2, helloworld_pb2_grpc

from .services.greeter import Greeter

logger = getLogger(__name__)


class Server:
    """IPC server."""

    def __init__(self, address: str) -> None:
        """Init IPC server.

        Args:
            address: Bind address to listen IPC requests for.
        """
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # IPC services
        helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), self._server)

        # Health check
        health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), self._server)

        # Reflection
        service_names = (
            helloworld_pb2.DESCRIPTOR.services_by_name["Greeter"].full_name,
            health_pb2.DESCRIPTOR.services_by_name["Health"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(service_names, self._server)

        self._server.add_insecure_port(address)  # It returns 1 if UDS
        self._address = address

    @property
    def address(self) -> str:
        """Return server listen address."""
        return self._address

    def start(self, *, blocking: bool = False) -> None:
        """Start IPC server."""
        self._server.start()
        logger.info("IPC server listening on %s", self._address)
        if blocking:
            self._server.wait_for_termination()

    def stop(self, grace: float | None) -> None:
        """Stop server.

        Args:
            grace: Graceful shutdown period. If `None`, abort all RPCs immediately.
        """
        self._server.stop(grace)
