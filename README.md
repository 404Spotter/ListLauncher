# ListLauncher

    Launch a saved list of files, folders, and shell commands from the command line. Build a "playlist" for a complex project and launch everything needed with one command.

    Works on Linux desktop distros (requires xdg-utils and Python 3.13)

## Usage

'''bash
Create New List:
    $ listlauncher new-list "list_name" 
Add PDF or File to Launch with Default:
    $ listlauncher "list_name" add ~/Documents/notes.pdf
Run Project or File with Program like VSCode:
    $ listlauncher "list_name" add "code ~/projectsmy-project"
View Saved Lists
    $ listlauncher list
View Executions Saved to List:
    $ listlauncher view "list_name"
Launch List:
    $ listlauncher "list_name" 
'''





