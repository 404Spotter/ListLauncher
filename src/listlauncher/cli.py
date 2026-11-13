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
    """Add a file, folder, or command (in quotes) to a list.""" # Text in cli.
    try:
        entry = core.add_entry(name, target)
    except core.ListLauncherError as error:
        fail(error)
    typer.echo(f"Added {entry['type']} to '{name}'")

@app.command()
def run(name: str):
    """Open everything in a list."""
    try:
        failed = core.run_list(name)
    except core.ListLauncherError as error:
        fail(error)

    for entry, reason in failed:
        typer.secho(f"Failed to launch {entry}: {reason}", fg="yellow", err=True)

@app.command()
def view(name: str):
    """View everything saved to a list."""
    try:
        entries = core.get_entries(name)
    except core.ListLauncherError as error:
        fail(error)

    if not entries:
        typer.echo(f"'{name}' is empty. Add entries with `listlauncher add {name} TARGET`")
        return

    typer.secho(name, bold=True)
    for number, entry in enumerate(entries, start=1):
        typer.echo(f"  {number}. [{entry['type']}] {core.describe_entry(entry)}")

@app.command()
def rm(name: str, target: str):
    """Remove an entry from a list by its position in the view list or by its full entry"""
    try:
        entry = core.remove_entry(name, target)
    except core.ListLauncherError as error:
        fail(error)
    typer.echo(f"Removed {core.describe_entry(entry)} from '{name}'")

@app.command()
def rm_list(name: str):
    """Remove list"""
    try:
        core.delete_list(name)
    except core.ListLauncherError as error:
        fail(error)
    typer.echo(f"Deleted List: '{name}'")

@app.command()
def lists():
    """List all Lists"""
    names = core.get_list_names()
    if not names:
        typer.echo("No lists yet.")
        return
    for name in names:
        typer.echo(name)
def main():
    commands = typer.main.get_command(app).commands
    args = sys.argv[1:]
    if args and not args[0].startswith("-") and args[0] not in commands:
        if len(args) > 1 and args[1] in commands:
            # `listlauncher list1 add X` -> `listlauncher add list1 X`
            sys.argv[1], sys.argv[2] = sys.argv[2], sys.argv[1]
        else:
            # `listlauncher list1` -> `listlauncher run list1`
            sys.argv.insert(1, "run")
    app()

