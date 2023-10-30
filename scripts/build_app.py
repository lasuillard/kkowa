import sys
from itertools import chain, product

from PyInstaller.__main__ import run


def _repeat_option(option: str, args: list[str]) -> list[str]:
    """Helper function to repeat a CLI option for multiple items.

    >>> _repeat_option("--copy-metadata", ["opentelemetry_api", "opentelemetry_sdk", "grpcio"])
    ['--copy-metadata', 'opentelemetry_api', '--copy-metadata', 'opentelemetry_sdk', '--copy-metadata', 'grpcio']

    """
    return list(chain(*product([option], args)))


if __name__ == "__main__":
    # Build arguments
    args = [
        "main.py",
        "--onefile",
        *_repeat_option("--copy-metadata", ["opentelemetry_api", "opentelemetry_sdk", "grpcio"]),
        *_repeat_option("--collect-submodules", ["opentelemetry_exporter_otlp_proto_grpc", "opentelemetry"]),
        "--exclude-module",
        "tkinter",
        *sys.argv[1:],  # Allow additional arguments from CLI
    ]
    print(f"Running PyInstaller with args: {args!r}")

    # Run PyInstaller CLI
    run(args)
