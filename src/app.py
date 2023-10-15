import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    """Main window of application."""

    def __init__(self) -> None:
        """Create app."""
        super().__init__()

        self.setWindowTitle("kkowa")
        label = QLabel("Hello, World!")
        label.setMargin(10)
        self.setCentralWidget(label)
        self.show()


def run() -> None:
    """Launch GUI application."""
    app = QApplication(sys.argv)  # NOTE: Using separate CLI via Typer
    _w = MainWindow()
    app.exec()


if __name__ == "__main__":
    run()
