import os
import tomllib
from pathlib import Path
import tomli_w
import re
import shlex
import shutil
import subprocess

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "listlauncher"

def list_path(name):
    return CONFIG_DIR / f"{name}.toml"

def save_list(name, data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with list_path(name).open("wb") as file:
        tomli_w.dump(data, file)

def load_list(name):
    with list_path(name).open("rb") as file:
        return tomllib.load(file)

class ListLauncherError(Exception):
    """ERROR"""

# New List Command (need to add inline add)
def new_list(name):
    if not re.fullmatch(r"[\w-]+", name):
        raise ListLauncherError("List names can only use letters, numbers, - and _")
    if list_path(name).exists():
        raise ListLauncherError(f"A list called '{name}' already exists")
    save_list(name, {"name": name, "entries": []})

# Add an entry to a list
def add_entry(name, target):
    if not list_path(name).exists():
        raise ListLauncherError(f"No list named '{name}'")
    data = load_list(name)
    path = Path(target)
    if path.exists():
        entry = {"type": "path", "path": str(path.resolve())}
    else: 
        args = shlex.split(target)
        if not args or shutil.which(os.path.expanduser(args[0])) is None:
            raise ListLauncherError(
                f"'{target}' isn't an existing file or folder, or a command on your PATH"
            )
        entry = {"type": "command", "run": args}
    data["entries"].append(entry)
    save_list(name, data)
    return entry

# Remove an Entry from a List
def remove_entry(name, target):
    if not list_path(name).exists():
        raise ListLauncherError(f"No list named '{name}'")
    data = load_list(name)
    entries = data["entries"]
    if target.isdecimal():
        index = int(target) - 1
        if not 0 <= index < len(entries):
            raise ListLauncherError(f"'{name}' has no number {target}")
    else:
        as_path = str(Path(target).resolve())
        as_command = shlex.split(target)
        for index, entry in enumerate(entries):
            if entry.get("path") == as_path or entry.get("run") == as_command:
                break
        else:
            raise ListLauncherError(f"'{target}' isnt in '{name}")
        
    removed = entries.pop(index)
    save_list(name, data)
    return removed

# Delete a List
def delete_list(name):
    if not list_path(name).exists():
        raise ListLauncherError(f"No list named '{name}'")
    list_path(name).unlink()
# Executing entries from lists
def launch_entry(entry):
    if entry["type"] == "path":
        command = ["xdg-open", entry["path"]]
    else: 
        command = [os.path.expanduser(arg) for arg in entry["run"]]
    subprocess.Popen(
        command,
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

# Get All List Names
def get_list_names():
        return sorted(path.stem for path in CONFIG_DIR.glob("*.toml"))

def run_list(name):
    if not list_path(name).exists():
        raise ListLauncherError(f"No list called '{name}'")

    entries = load_list(name)["entries"]
    if not entries:
        raise ListLauncherError(f"'{name}' is empty. Add entries with `listlauncher add`")

    failed = []
    for entry in entries:
        try:
            launch_entry(entry)
        except OSError as error:
            failed.append((entry, str(error)))
    return failed

# Get entries from a List
def get_entries(name):
    if not list_path(name).exists():
        raise ListLauncherError(f"No list named '{name}'")
    return load_list(name)["entries"]

def describe_entry(entry):
    if entry["type"] == "path":
        return entry["path"]
    return shlex.join(entry["run"])