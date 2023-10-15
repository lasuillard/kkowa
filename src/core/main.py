from .ipc import Server


def run(*, ipc_address: str) -> None:
    """Run IPC server."""
    server = Server(address=ipc_address)
    server.start()
