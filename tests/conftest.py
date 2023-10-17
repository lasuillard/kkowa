from collections.abc import Generator

import pytest

from src.core.ipc import Server
from src.ipc import Client
from src.utils import random_uds


@pytest.fixture(scope="session")
def ipc_server() -> Generator[Server, None, None]:
    server = Server(address=random_uds())
    server.start()
    yield server
    server.stop(None)


@pytest.fixture(scope="session")
def ipc_client(ipc_server: Server) -> Generator[Client, None, None]:
    with Client(ipc_server.address) as client:
        yield client
