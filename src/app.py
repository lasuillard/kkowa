import atexit
import multiprocessing as mp
import sys
from tempfile import gettempdir

import grpc
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from _generated.grpc import helloworld_pb2, helloworld_pb2_grpc
from src import ipc
from src.utils import random_string


class MainWindow(QMainWindow):
    """Main window of application."""

    def __init__(self, grpc_target: str) -> None:
        """Create app."""
        super().__init__()

        self.setWindowTitle("kkowa")
        label = QLabel("Hello, World!")
        label.setMargin(10)
        self.setCentralWidget(label)

        # TODO(lasuillard): gRPC used for IPC between mitmproxy and api-server; using it here to check behavior
        self._grpc_channel = grpc.insecure_channel(grpc_target)
        stub = helloworld_pb2_grpc.GreeterStub(self._grpc_channel)
        atexit.register(self._grpc_channel.close)

        button = QPushButton(self)
        button.setText("Check IPC")
        button.clicked.connect(
            lambda: print(  # noqa: T201
                "Greeter client received:",
                stub.SayHello(helloworld_pb2.HelloRequest(name="lasuillard")),
            ),
        )

        self.show()


def run(grpc_endpoint: str | None = None) -> None:
    """Launch GUI application."""
    if not grpc_endpoint:
        grpc_endpoint = random_string(prefix=f"unix://{gettempdir()}/kkowa-", suffix=".sock")

    app = QApplication(sys.argv)  # NOTE: Using separate CLI via Typer
    _w = MainWindow(grpc_endpoint)

    grpc_server = mp.Process(target=ipc.run, args=(grpc_endpoint,))
    grpc_server.start()

    app.exec()


if __name__ == "__main__":
    run()
