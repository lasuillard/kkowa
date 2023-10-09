import typer

from . import app, wrapper

cli = typer.Typer(
    help="kkowa app.",
    no_args_is_help=True,
)

# Register commands; if need nested subcommand, use `app.add_typer()`
# https://typer.tiangolo.com/tutorial/subcommands/nested-subcommands/
app.register(cli)
wrapper.register(cli)


# Dummy for exposing single command on CLI help
# https://typer.tiangolo.com/tutorial/commands/one-or-multiple/
@cli.callback()
def callback() -> None:  # noqa: D103
    pass
