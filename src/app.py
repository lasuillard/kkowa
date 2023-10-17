import multiprocessing as mp
from logging import getLogger

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from _generated.grpc import helloworld_pb2
from src import core, mitmproxy
from src.ipc import ClientFactory
from src.utils import random_uds

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


def run(ipc_address: str | None = None) -> None:
    """Launch GUI application."""
    if not ipc_address:
        ipc_address = random_uds()

    # Run core server
    core_app = mp.Process(
        target=core.run,
        kwargs={
            "ipc_address": ipc_address,
        },
    )
    core_app.start()

    # Run mitmproxy
    # TODO(lasuillard): Each process should sink logs to files, only GUI app logs to terminal
    mitmproxy_app = mp.Process(target=mitmproxy.run, args=())
    mitmproxy_app.start()

    # Run GUI application
    app = QApplication([])  # NOTE: Using separate CLI via Typer
    _w = MainWindow(ipc_address)
    app.exec()
