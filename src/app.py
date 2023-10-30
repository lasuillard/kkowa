import multiprocessing as mp
from logging import getLogger

from src import core, gui
from src.utils import random_uds

logger = getLogger(__name__)


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

    # Run GUI application
    gui_app = mp.Process(
        target=gui.run,
        kwargs={
            "ipc_address": ipc_address,
        },
    )
    gui_app.start()


if __name__ == "__main__":
    run()
