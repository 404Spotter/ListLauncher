# ListLauncher

    Launch a saved list of files, folders, and shell commands from the command line. Build a "playlist" for a complex project and launch everything needed with one command.

    Works on Linux desktop distros (requires xdg-utils and Python 3.13)

## Usage

```bash
  # Create a list
  listlauncher new-list work

  # Add a file or folder (opens in its default app)
  listlauncher add work ~/Documents/notes.pdf

  # Add a command (wrap it in quotes)
  listlauncher add work "code ~/projects/my-project"

  # See what's in a list
  listlauncher view work

  # Launch everything in the list
  listlauncher work

  # Remove an Entry from A List
  listlauncher list_name rm "_"

  # Delete a List
  listlauncher rm-list list_name

  # View All Saved Lists
  listlauncher lists
```



