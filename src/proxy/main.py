from collections.abc import Callable, Sequence
from typing import Any

from mitmproxy.http import HTTPFlow
from mitmproxy.tools import cmdline, main
from mitmproxy.tools.dump import DumpMaster


class Counter:
    """Simple addon for demonstration."""

    def __init__(self) -> None:  # noqa: D107
        self.num = 0

    def request(self, flow: HTTPFlow) -> None:  # noqa: D102
        self.num = self.num + 1
        print("Count %d" % self.num, flow.request.url)  # noqa: T201


addons = [Counter()]


# https://github.com/mitmproxy/mitmproxy/blob/main/mitmproxy/tools/main.py
class Master(DumpMaster):
    """Customized DumpMaster with addons."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D107
        super().__init__(*args, **kwargs)

        self.addons.add(*addons)


def run(args: Sequence[str] | None = None, extra: Callable[[Any], dict] | None = None) -> None:
    """Run mitmproxy app."""
    main.run(Master, cmdline.mitmdump, args or [], extra)
