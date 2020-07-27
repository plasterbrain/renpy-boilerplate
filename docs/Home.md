# Getting started
Hello, and welcome to my downright inexcusably excessive documentation for this project! It's important to read at least some of this, as I would consider fine-tuning a Ren'Py project to be like defusing a bomb.

## How to read these docs
To keep things as clear as possible for those with little background in coding, I've tried to follow some consistent, if arbitrary, formatting rules:

- Variables, keys, and functions are represented as inline code, e.g. `config.version`.
- File names, folders, and extensions are in italics, e.g. *config.rpy*.
- Function parameter names are in bold, e.g. **should_reload**.
- Values are in plain text, e.g. "string" or True.

## How to use this template
### Project file structure
The project template is a folder with various scripts and config files, a sub-directory called *tools* with [some useful development stuff](/Tools.md), and a sub-directory called *ProjectName*, which is your base Ren'Py project folder.

This base project directory contains *game*, the folder where your Ren'Py scripts, images, videos, and sounds go. It also has a *help* folder and a file called *help.html*, which comprise your [game manual](/Manual).

Finally, *steam_appid.txt* and *.itch.toml* are configuration files that will be distributed with your game, as they help Steam and the Itch app respectively to launch it correctly.

The *tools* folder and files outside the *ProjectName* directory are useful for development but will not be compiled or shipped with your game build.

To get started with a new project:
1. Download a copy of this template
1. Rename *ProjectName* to whatever you want.
1. Move *ProjectName* to your Ren'Py projects directory so you can access it from the Ren'Py launcher.
  - Alternatively, on Windows, the two batch scripts in the main template directory will let you launch the game (and clear persistent data) from anywhere, provided you edit them to point to your new *ProjectName* folder and have Ren'Py in your PATH variable.
1. Start editing!

### Code conventions
#### Init blocks and Python statements
Most variables are defined in init blocks. This is mostly so I could indent them, making inline commentary more distinguishable from section headings. However, non-preference variables can also be set using a `define` statement, outside of any blocks. This has the added benefit of declaring the given variable as a constant.

Preference variables are set using `default`. I couldn't really avoid that one since the `default` statement handles setting up "default" preference values in a persistent dictionary.

`init offset = {number}` and `init {number} python:` statements affect the order in which the code underneath is run. In cases where the offset is not 0 (the default), There will be a comment explaining why the offset is needed. Often this can be If you move the code to another file, make sure that init offset comes with it, or Ren'Py will either throw an Exception or ignore the code entirely. Similarly, the `python early:` block is used to specially mark code that needs to run before persistent data is loaded.

#### Inline comments
Comments beginning with two pound signs ("##") are informational. Comments begining with a single pound sign ("#") are disabled code.

Most variables have an inline comment heading describing what they do. If I found out what version of Ren'Py it was added in, the patch number is listed in parentheses. The variables are usually pretty simple, but the code is lengthy because there's lot of settings and I tend to wax poetic on like, stuff I wish I knew when I first started using Ren'Py.

Variables with "## ---!" in their heading (with an exclamation mark) will affect the project if they are deleted from the script, either because they have been set to a non-default value or because they are something custom I added. Variables with a "## ---" heading (no exclamation mark) are redeclarations of default Ren'Py values, there for your reference, so they can be safely deleted from the file if you don't want to change their value.

A long "#--------..." line is sometimes used to separate init blocks into sections: The top-most section contains variables you may want to edit. The bottom-most section is reserved for functions and "automatic" variable declarations (e.g., created using list/dictionary comprehension). You don't need to touch them unless you know what you're doing. Finally, the middle section, if there is one, contains helpful predefined variables you don't need to edit, but may want to reference in your screens, styles, and other code.

#### Variables
There are some pairs of variables that end in "\_list" and "\_names". The "list" variable is a list of code-accessible items (usually represented as text strings) presented in the order they should be read by the script. The "names" variable is a Python dictionary. It has the same items as the list, now mapped to some properties, like human-readable names (like "variable1": \_\_("Cool Variable!")).

The reason we need two is because Python dictionaries don't remember the order of their items. The combined effect is the ability to loop over a list of items (such as screens) in our preferred order while accessing useful information about each one.

Variables ending in "\_map" are also dictionaries.

Screen text, character names, and other string variables may be wrapped in `_()`. That's Python's `gettext` function, and Ren'Py uses it to generate translations. Text outside of story dialogue should use this function to be added to the list of translateable strings. Text enclosed in `_()`, with one underscore, is translated when it is shown. Text enclosed in `__()`, with two underscores, is translated immediately, making this function suitable for more programmatic usage.

Variable names in all caps are constant, defined in that one statement and then used for reference elsewhere -- never actually changed.

#### Functions
Functions are documented using numpydoc inline documentation conventions. I don't know why. But like, why not?

Functions beginning with an underscore are usually intended to be called by other functions rather than directly.
