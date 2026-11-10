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
    save_list(name, {"name": name, "items": []})

# Add Command
def add_item(name, target):
    if not list_path(name).exists():
        raise ListLauncherError(f"No list named '{name}'")
    data = load_list(name)
    path = Path(target)
    if path.exists():
        item = {"type": "path", "path": str(path.resolve())}
    else: 
        args = shlex.split(target)
        if not args or shutil.which(os.path.expanduser(args[0])) is None:
            raise ListLauncherError(
                f"'{target}' isn't an existing file or folder, or a command on your PATH"
            )
        item = {"type": "command", "run": args}
    data["items"].append(item)
    save_list(name, data)
    return item

# Executing Items from lists
def launch_item(item):
    if item["type"] == "path":
        command = ["xdg-open", item["path"]]
    else: 
        command = [os.path.expanduser(arg) for arg in item["run"]]
    subprocess.Popen(
        command,
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def run_list(name):
    if not list_path(name).exists():
        raise ListLauncherError(f"No list called '{name}'")

    items = load_list(name)["items"]
    if not items:
        raise ListLauncherError(f"'{name}' is empty. Add items with `listlauncher add`")

    failed = []
    for item in items:
        try:
            launch_item(item)
        except OSError as error:
            failed.append((item, str(error)))
    return failed

# Get items from a List
def get_items(name):
    if not list_path(name).exists():
        raise ListLauncherError(f"No list named '{name}'")
    return load_list(name)["items"]

def describe_item(item):
    if item["type"] == "path":
        return item["path"]
    return shlex.join(item["run"])