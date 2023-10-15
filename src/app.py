import atexit
import multiprocessing as mp
from logging import getLogger

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from src.api_server import grpc_server
from src.proxy.grpc_client import GrpcClient, helloworld_pb2
from src.utils import random_uds

logger = getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window of application."""

    def __init__(self, grpc_endpoint: str) -> None:
        """Create app."""
        super().__init__()

        self.setWindowTitle("kkowa")
        label = QLabel("Hello, World!")
        label.setMargin(10)
        self.setCentralWidget(label)

        # TODO(lasuillard): gRPC used for IPC between mitmproxy and api-server; using it here to check behavior
        self._grpc_client = GrpcClient(grpc_endpoint)
        atexit.register(self._grpc_client.shutdown)

        button = QPushButton(self)
        button.setText("Check gRPC")
        button.clicked.connect(
            lambda: logger.debug(
                "Greeter client received: %r",
                self._grpc_client.greeter.SayHello(helloworld_pb2.HelloRequest(name="lasuillard")),
            ),
        )

        self.show()


def run(grpc_endpoint: str | None = None) -> None:
    """Launch GUI application."""
    if not grpc_endpoint:
        grpc_endpoint = random_uds()

    # Run API server first
    _grpc_server = mp.Process(target=grpc_server.run, args=(grpc_endpoint,))
    _grpc_server.start()

    # TODO(lasuillard): Wait for all dependent servers are ready, if any fails should exit with non-zero code
    # ...

    # Run GUI application
    app = QApplication([])  # NOTE: Using separate CLI via Typer
    _w = MainWindow(grpc_endpoint)
    app.exec()


if __name__ == "__main__":
    run()
