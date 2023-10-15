from logging import getLogger

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
