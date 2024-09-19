# MINITO

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Potential Developments](#potential-developments)
- [Dependencies](#dependencies)

## Description
**Minito** is a **Mini**malist **to**do app written in Python. It was inspired by command-line tools, Linux installers, and basic notepad todo lists. Minito is an incredibly simple yet capable todo app designed to be as minimal as possible while maintaining functionality. Although Minito is meant to hold a temporary todo list while you work on something, you can easily save your list for later.

## Installation
To download Minito, simply locate the latest release in the "Releases" section of the GitHub repository and download the exe file.

## Usage
To begin using Minito, simply run the installed exe by either double-clicking it or by using the command line as shown below:
```cmd
C:\Minito\Location> Minito_vX.X.X.exe
```

### Default Keybindings
| Keybinding | Usage |
|------------|-------|
| TAB | Switch between the main panel and the input box |
| ENTER | Toggles a checkbox and used to enter information in the input box |
| CTRL + E | Edit a task |
| BACKSPACE | Delete a task |
| CTRL + X | Exit the file with prompt to save |
| Q | Exit file with no prompt (only works when in the tasks window) |

### Opening a File
The following is the syntax to open a .minito file using the command line:
```cmd
C:\Minito\Location> Minito_vX.X.X.exe C:\example\path\example_file.minito
```
A .minito file can also be opened using the Windows File Explorer by performing the "Open with" operation and choosing the Minito exe that you have downloaded.

## Configuration
The Minito configuration file is located at `%USERPROFILE%\AppData\Local\Minito`. Insert that path into the Windows run dialog and it will open up the Minito configuration directory where the `configuration.yaml` file will be. The structure of a setting within the configuration file looks like this:
```yaml
# This is a comment explaining what the setting is for
setting: "value"
```
Here are some rules to follow when configuring settings:
- Keep the values lowercase unless required for a specific keybinding such as `SHIFT + H` which would be `"H"`
- See the table within the "Keyboard Input" section of the [User Input](https://urwid.org/manual/userinput.html) part of the Urwid manual for examples on how keybind syntax should look like
- Don't change, comment-out, or delete any of the settings

## Potential Developments
Please note that just because a feature is present here does not mean that it will be implemented.

Empty for now...

## Main Dependency
Minito was built using the [Urwid](https://urwid.org/index.html) Python library. This library is what gives Minito its console-like UI.