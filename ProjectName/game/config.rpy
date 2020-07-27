################################################################################
## Configuration
################################################################################
## https://www.renpy.org/doc/html/config.html
##
## Configuration variables control default Ren'Py behavior. These should
## generally not be changed after init phase and are not part of the save data.

## -- Basic Settings -----------------------------------------------------------

init python:

    ## ---! Project Name
    config.name = __("Project Name")

    ## ---! Version
    config.version = renpy.file("version.txt").read().strip()

    ## --- Window Title
    ## The static portion of the game's window title. If None, the default, this
    ## defaults to the value of `config.name`.
    config.window_title = None

    ## ---! Window Subtitle
    ## The _window_subtitle value, added when entering the main or game menus.
    config.menu_window_subtitle = ""

## -- Engine Settings ----------------------------------------------------------
## Settings for how Ren'Py interprets scripts, text tags, and more.

init -2 python:

    ## Init offset -2 to let dev_tools.rpy change this.

    ## Setting this manually lets us avoid including `script_version.txt`.
    config.developer = False

init python:

    ## --- (Callback) Auto-Forward Check
    ## Function called, without arguments, to determine if it is safe to auto
    ## forward. The intent is that this can be used by a voice system to disable
    ## auto-forwarding when a voice is playing.
    config.afm_callback = None

    ## --- Custom Text Tags
    config.custom_text_tags = {}
    config.self_closing_custom_text_tags = {}

    ## --- Define/Default Namespaces
    ## Map of special namespaces (for define/default statements) to objects.
    # config.special_namespaces[] = None

    ## ---! (Callback) Dismiss Check
    ## Function called, without arguments, when the user attempts to dismiss a
    ## say statement. Use this to prevent advancing the text in certain cases.
    can_dismiss = True ## Whether the user can advance the text.
    config.say_allow_dismiss = lambda : can_dismiss

    ## Whether clicking while in rollback at a checkpoint will keep the roll
    ## forward buffer if the data has not changed.
    config.keep_rollback_data = False

    ## --- (Callbacks) Python Block
    ## List of callbacks that are called after each non-init-phase python block.
    # confg.python_callbacks = []

    ## --- SL2 Keyword
    ## Whether Ren'Py allows the SL2 keyword after a Python statement.
    config.keyword_after_python = False

    ## --- Text Substitutions
    ## A function to substitute certain text strings. It accepts one string
    ## parameter with the full text to be shown and should return a string with
    ## the newly updated text.
    def replace_text(s):
        s = s.replace("--", u"\u2014") ## em dash
        return s
    config.replace_text = replace_text

    ## --- (Callbacks) Text Sustain
    ## Functions called, without arguments, before the second and later
    ## interactions caused by a line of dialogue with pauses in it.
    # config.say_sustain_callbacks.append()

    ## --- TTS Filter Tags (7.4.0)
    ## A list of text tag names. The text wrapped by these tags will be
    ## displayed only if self-voicing is not activated.
    # config.tts_filter_tags = ["noalt", "rt", "art"]

    ## --- Wait for Voicing (6.99.13)
    # Whether {nw} tags waits until voice clips and self-voicing finish.
    config.nw_voice = True

## -- Folder/File Structure ----------------------------------------------------
## Settings for how the engine stores, searches for, and loads game files.

python early:

    ## ---! Save Directory
    ## Directory (under the Ren'Py app data folder) in which games and
    ## persistent information are saved. This will be run before any other
    ## statement, and so it should be set to a string, not an expression.
    config.save_directory = "ProjectName"

init -1 python:

    ## Init offset -1: Audio/image directories are scanned at init offset 0.

    ## --- Audio Directory (7.3.3)
    # TODO test if this works since it's not documented
    ## The name of the directory to recursively search when automatically
    ## defining sound files, or None to disable this feature.
    config.audio_directory = "audio"

    ## --- Images Directory (6.99.2)
    # TODO test if subfolder works?
    ## The name of the directory to recursively search when automatically
    ## defining story images, or None to disable this feature.
    config.images_directory = "images"

init python:

    ## ---! Screenshot Directory
    ## Name of the folder in the base directory where screenshots are saved.
    screenshot_folder = __("screenshots")

    ## ---! Screenshot File Pattern
    ## The pattern used to generate a screenshot file name. When using
    ## `_custom_screenshot`, this should include "{0}", representing the time
    ## the screenshot was taken, and "{1}", representing a numerical ID.
    config.screenshot_pattern = "{0}_{1}.png"

    ## --- Translation Directory
    ## Name of the languages directory in the game folder.
    config.tl_directory = "tl"

    ## --- Audio File Format
    ## Map of default audio channels to a tuple containing: the mixer used by
    ## this channel, a channel file prefix, and a channel file suffix.
    config.auto_channels = {"audio": ("sfx", "", "")}

    ## --- Imagemap File Formats (6.12.0)
    ## A function returning a formatted file name for the various image states
    ## used with an imagemap ("insensitive", "idle", "hover", "selected_idle",
    ## "selected_hover", and "ground"). It receives two arguments, the string
    ## given to the the auto property (like "imagemap_%s.png") and the desired
    ## image variant. It should return a displayable or None.
    config.imagemap_auto_function = _imagemap_auto_function

    ## --- Voice File Format (6.16)
    ## The file pattern to use when searching for a voice clip to play with a
    ## line of dialogue. If this is a string, it should use the `{id}` variable
    ## to represent the dialogue line identifier. If this is a function, it
    ## should accept the current dialogue line ID (a string) as an argument,
    ## and return a string with the filename to use. If None, the automatic
    ## voice feature is disabled.
    # TODO test function in documentation
    config.auto_voice = None

    ## Formatted string used by the voice statement to select a voice file.
    # TODO test how this interacts with config.auto_channels
    config.voice_filename_format = "{filename}"

    #--- Search Path
    # List of directories that are searched for images, music, archives, and
    # other media, but not scripts. This is initialized to a list containing
    # "common" and "game," the name of the game directory.
    #
    # config.searchpath.append()

    ## --- Search Prefxies (6.99.5)
    # List of prefixes added to filenames when Ren'Py searches for a file.
    config.search_prefixes = ["", "images/"]

    ## ---! (Callback) Screenshot Taken (6.12.0)
    # Function called after a screenshot is taken. It is called with a single
    # argument, the full filename of the screenshot.
    config.screenshot_callback = _custom_screenshot_callback

    ## List of archive files Ren'Py searches for images and other data. At
    ## startup, Ren'Py will populate this variable with the names of any
    ## archives found in the game directory, sorted in reverse ascii order.
    ## Accepts a list of strings giving the base archive file names.
    # config.archives = []

    # Screenshots are cropped to this rectangle before being saved.
    # Accepts a (x, y, height, width) tuple or None.
    config.screenshot_crop = None

## -- i18n ---------------------------------------------------------------------
## Settings to make the game translatable.

init python:

    ## --- (Callback) Change Language
    ## List of functions called, with no arguments, when changing the language.
    # config.change_language_callbacks = []

    ## --- RTL Support
    ## Whether right-to-left languages are supported.
    config.rtl = False

    ## List of named stores that are reverted to their state at the end of the
    ## init phase when the language is changed in-game. This only occurs if
    ## `config.new_translate_order` is True (the default).
    config.translate_clean_stores = ["gui"]

    ## List of additional script files that should be translated.
    # config.translate_files = []

    ## List of files where "##<space>" comment sequences should be translated.
    # config.translate_comments = []
