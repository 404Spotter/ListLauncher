import typer
import sys
from listlauncher import core

app = typer.Typer(
    help="Launch saved lists of files, folders, and commands.",
    no_args_is_help=True,
)
def fail(error):
    typer.secho(f"Error: {error}", fg="red", err=True)
    raise typer.Exit(1)

@app.command()
def new_list(
    name: str,
):
    """Create an empty list."""
    try:
        core.new_list(name)
    except core.ListLauncherError as error:
        fail(error)
    typer.echo(f"Created list '{name}'")


@app.command()
def add(name: str, target: str):
    """Add a file, folder, or command (in quotes) to a list."""
    try:
        item = core.add_item(name, target)
    except core.ListLauncherError as error:
        fail(error)
    typer.echo(f"Added {item['type']} to '{name}'")

@app.command()
def run(name: str):
    """Open everything in a list."""
    try:
        failed = core.run_list(name)
    except core.ListLauncherError as error:
        fail(error)

    for item, reason in failed:
        typer.secho(f"Failed to launch {item}: {reason}", fg="yellow", err=True)


def main():
    # Treat `listlauncher list1` as `listlauncher run list1`
    commands = typer.main.get_command(app).commands
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-") and sys.argv[1] not in commands:
        sys.argv.insert(1, "run")
    app()