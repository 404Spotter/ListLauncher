import os
import tomllib
from pathlib import Path
import tomli_w

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
