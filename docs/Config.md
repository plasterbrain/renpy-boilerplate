# Configuring your game, part 1 (*config.rpy*)
When setting up a new Ren'Py game, this file is a great place to get started. It essentially takes the place of the Ren'Py project template's *options.rpy*, and holds a lot of config variables.

## How to use this file
If you want to add a config variable you believe is missing, first do a Ctrl + F search across the entire project folder to make sure it's not being defined somewhere else. Config variables are located across various files depending on their purpose. Seriously, they're everywhere.

### Setting up project info
Here are some very easy steps you can do to start customizing your game.
1. Set `config.name` to the name of your project.
1. To set the game's version, open *game/version.txt*. The default, 0.0.0, is just an example using semantic versioning, but you can use anything you want. The version number is just for reference on logs and error screens and when pushing updates for your players.
1. Update `config.help` to the name of your readme file, if you have one.
1. You can give your game window a custom title using `config.window_title`. For some reason, you can add a subtitle to this when in the game and main menus using `config.menu_window_subtitle`.

### Intermediate steps
#### Custom game folders
##### Save folder
`config.save_directory` can be used to name your game's save folder. When set to a string, Ren'Py will store your game's save data in a folder under Ren'Py user app data (*{User}/AppData/Roaming/RenPy/* on Windows, *~/Library/RenPy/* on Mac, and *~/.renpy/* on Linux).

In default Ren'Py projects, this is set to a folder with your project name and a numerical ID (e.g., *BROKEN_MINDS-1443979110*). This is likely to prevent inadvertently conflicting with save data from other, identically named Ren'Py games.

You can also set `config.save_directory` to None. In this case, save files will be stored only in the game's *game/saves* directory. Ren'Py documentation discourages this, as it prevents games from being shared between system users, especially those with different access permissions.

This <u>needs</u> to be set in a `python early` block. To make sure it's working as intended, when you launch your game, open the console and type `config.savedir` to make sure it's the correct value.

##### Asset folders
Ren'Py looks for audio and image files to use in your game in the *audio* and *images* folders, respectively. Assets in these folders get added to the list of files it knows about, so you can use statements like `show eileen happy` instead of `show "images/eileen/eileen happy.png"`.

To change these folder names, rename the actual folder(s), and then update `config.audio_directory` (and/or `config.images_directory`) to match the new folder name(s).

(You can also set these to None to disable Ren'Py's automatic audio or image scanning, but... don't!)

The `gui` directory is <u>not</u> automatically scanned, so you can rename this folder to whatever you want. Just make sure to update any screens using images to match the new folder path.

##### Screenshots folder
By default, when a user takes a screenshot, Ren'Py saves the resulting file to your project's base folder. (While in development and running your game from the launcher, they'll end up in the folder of your Ren'Py installation.)

The custom variable `screenshot_folder` has been created to circumvent this. You can change it to choose your own subfolder name or remove it to restore Ren'Py's original functionality.

The name is translateable right now, under the assumption that the user would set the game to a language they can actually read before taking any screenshots, but you may want to change this to keep the same folder regardless of in-game language.

##### Translations folder
This is where the files containing translations of all in-game texts would be stored. It defaults to *tl* in the game directory. To change this, rename the actual *tl* folder and then change `config.tl_directory` to match the new name.

##### Audio file patterns
@TODO THIS

##### Imagemap file patterns
If you have a particular file structure for your GUI images and want to change the way the [imagemap `auto` property](https://www.renpy.org/doc/html/screens.html?highlight=imagemap#imagemap) retrieves them, you can point `config.imagemap_auto_function` to a custom function.

The function should accept two parameters, the value given to `auto` and the desired image variant, and return the appropriate displayable (like an image name). By default, the `auto` property takes a value like "gui/imagemap_%s.png" and formats it with imagemap state variants. For example, that value would retrieve "gui/imagemap_idle.png", "gui/imagemap_hover.png", and so on.

##### Voice file pattern
If your game does <u>not</u> have full voice acting, or you want to manually specify a `voice "file.mp3"` statement above every line, you can skip this section, and delete `config.auto_voice` (and its related in-line comments) entirely.

Games with full voice acting may benefit from [Ren'Py's Automatic Voice system](https://www.renpy.org/doc/html/voice.html#automatic-voice). This will automatically load the right voice file to play if one exists for the given line.

Accordingly, you should customize `config.auto_voice` to match your preferred file/directory structure (maybe something like "audio/voice/{id}.mp3"). Your file pattern needs "{id}", which stands for the dialogue identifier. Every line of dialogue has an ID which is a combination of its parent label and some hexadecimal garbage (e.g., "start_e809cd95").

However, if you don't want to keep all your voice files in the same folder, `config.auto_voice` can also be a function. Your function should accept the dialogue ID as its sole argument and return a string with the name of the file to use. For example, if you wanted to organize files into subfolders according to their label (like "audio/voice/start/e809cd95.mp3"), you might do something like this:
```python
def get_voice_clip(id):
  label = id.split("_")
  dialogue_id = label.pop(-1)
  path = "audio/voice"
  for part in label:
    path = path + part + "/"
  return path + dialogue_id + ".mp3"

define config.auto_voice = get_voice_clip
```
When you're <u>done</u> writing your game dialogue, you can use the Ren'Py launcher to Extract Dialogue (it's a button) as a tab-delimited spreadsheet. Open the resulting file, *dialogue.tab*, in any text editor, and you'll be able to see the dialogue identifiers for every line. You can name and organize your voice files based on these identifiers. Good luck, bye!

### Advanced users only

#### Compatibility garbage:
The following variables are not included in this project template. However, you may want to include them to restore old Ren'Py behavior.

- `config.script_version` - Set to a tuple of the Ren'Py script version you want to emulate to automatically adjust compatibility settings. The default, None, uses the latest Ren'Py version.
- `config.late_images_scan` (7.0.0) - Set to False to automatically define images at init offset 1900, instead of 0. This should be in a block with an init offset of at least -1.
- `config.new_translate_order` (6.99.11) - Set to False to use the old execution order for translating styles/fonts. Note the old order may not work with modern Ren'Py GUI and screen language.
  - The new order works as follows:
    1. The stores in `config.translate_clean_stores` are reverted to their state at the end if init.
    1. All `translate {language} python:` statements are run.
    1. All deferred style statements are run.
    1. All `translate {language} style:` statements are run.
    1. The callbacks in `config.change_language_callbacks` are called.
  - The old order worked like this:
    1. All `translate {language} style:` statements are run.
    1. All `translate {language} python:` statements are run.
    1. The callbacks in `config.change_language_callbacks` are called.
- `config.new_substitutions` (6.13) - Set to False to disable Ren'Py's new-style text string subtitution, where variables are represented in square brackets ([]).
- `config.old_subtitutions` (6.13) - Set to True to enable Ren'Py's old-style text string subtitution, which resembles Python string formatting (using %).
