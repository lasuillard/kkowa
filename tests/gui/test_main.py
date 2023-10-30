from pytestqt.qtbot import QtBot

from src.gui.main import MainWindow


def test_widget(qtbot: QtBot) -> None:
    window = MainWindow("")
    qtbot.add_widget(window)
    assert window.label.text() == "Hello, World!"
