from functools import partial

import typer


def _mitmproxy(ctx: typer.Context) -> None:
    """Run Django's management commands.

    This command is wrapper for Django CLI and any given arguments will be passed to it.
    """
    if "--help" in ctx.args:
        print(ctx.get_help())
        print("---")

    # TODO(lasuillard): Run mitmproxy CLI


def register(app: typer.Typer) -> None:
    """Register commands in current module to given `Typer` app."""
    # Command preset for "redirect" commands, which just wraps existing CLIs for re-export
    redirector = partial(
        app.command,
        context_settings={
            # Allow passing arbitrary arguments
            "allow_extra_args": True,
            "ignore_unknown_options": True,
            # Disable default `--help` to pass it to instead of showing help for wrapper command
            "help_option_names": [],
        },
    )
    redirector(name="mitmproxy", no_args_is_help=False)(_mitmproxy)
