import multiprocessing as mp
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

from src import mitmproxy


class MainWindow(QMainWindow):
    """Main window of application."""

    def __init__(self) -> None:
        """Create app."""
        super().__init__()

        self.setWindowTitle("kkowa")
        label = QLabel("Hello, World!")
        label.setMargin(10)
        self.setCentralWidget(label)

        # Start background processes
        # TODO(lasuillard): Each process should sink logs to files, only GUI app logs to terminal
        self._mitmproxy = mp.Process(target=mitmproxy.run, args=())
        self._mitmproxy.start()

        # TODO(lasuillard): Wait until all ready

        self.show()


def run() -> None:
    """Launch GUI application."""
    app = QApplication(sys.argv)  # NOTE: Using separate CLI via Typer
    _w = MainWindow()
    app.exec()
