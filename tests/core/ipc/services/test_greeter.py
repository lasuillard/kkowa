from _generated.grpc.helloworld_pb2 import HelloRequest
from src.ipc.client import Client


class TestGreeter:
    def test_SayHello(self, ipc_client: Client) -> None:  # noqa: N802
        assert ipc_client.greeter.SayHello(HelloRequest(name="Cabbage")).message == "Hello, Cabbage!"
