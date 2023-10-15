from concurrent import futures
from logging import getLogger

import grpc
from grpc._server import _Context

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
    server.add_insecure_port(address)
    server.start()
    print("Server started, listening on %s" % address)  # noqa: T201
    server.wait_for_termination()


if __name__ == "__main__":
    run("localhost:50051")
