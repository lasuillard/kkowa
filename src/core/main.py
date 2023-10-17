from logging import getLogger

from . import ipc
from .migrate import migrate_db

logger = getLogger(__name__)


def run(*, ipc_address: str) -> None:
    """Run core application."""
    # Migrate database
    logger.info("Migrating database")
    migrate_db()

    # Run IPC server
    logger.info("Starting IPC server")
    ipc_server = ipc.Server(address=ipc_address)
    ipc_server.start(blocking=True)
