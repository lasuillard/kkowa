from concurrent import futures
from logging import getLogger

import grpc
from grpc._server import _Context
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

from _generated.grpc import helloworld_pb2, helloworld_pb2_grpc

logger = getLogger(__name__)


class Greeter(helloworld_pb2_grpc.GreeterServicer):  # noqa: D101
    def SayHello(  # noqa: N802, D102
        self,
        request: helloworld_pb2.HelloRequest,
        context: _Context,  # noqa: ARG002
    ) -> helloworld_pb2.HelloResponse:
        return helloworld_pb2.HelloResponse(message=f"Hello, {request.name}!")


def run(address: str) -> None:
    """Run gRPC server.

    Args:
        address: Address to listen to.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # Health check
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)

    # Reflection
    service_names = (
        helloworld_pb2.DESCRIPTOR.services_by_name["Greeter"].full_name,
        health_pb2.DESCRIPTOR.services_by_name["Health"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port(address)  # It returns 1 if UDS
    server.start()
    logger.info("Server started, listening on %s", address)
    server.wait_for_termination()
