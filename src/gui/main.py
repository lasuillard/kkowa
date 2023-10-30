from logging import getLogger

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from _generated.grpc import helloworld_pb2
from src.ipc import ClientFactory

logger = getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window of application."""

    def __init__(self, ipc_address: str) -> None:
        """Create app."""
        super().__init__()

        self.setWindowTitle("kkowa")
        self.label = QLabel("Hello, World!")
        self.label.setMargin(10)
        self.setCentralWidget(self.label)

        self._client_factory = ClientFactory(address=ipc_address)

        button = QPushButton(self)
        button.setText("Check gRPC")
        button.clicked.connect(self._check_ipc_connectivity)

        self.show()

    def _check_ipc_connectivity(self) -> None:
        with self._client_factory.get_client() as ipc:
            logger.debug(
                "IPC greeter received: %r",
                ipc.greeter.SayHello(helloworld_pb2.HelloRequest(name="lasuillard")),
            )


def run(*, ipc_address: str) -> None:
    """Run GUI app."""
    app = QApplication([])  # NOTE: Using separate CLI via Typer
    _w = MainWindow(ipc_address)
    app.exec()
