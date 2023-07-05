################################################################################
## Developer: Tools and Settings
################################################################################
## https://www.renpy.org/doc/html/developer_tools.html
##
## Tools and configuration for development and debugging.

init -1 python:

    ## Init offset -1: config.developer is used to set up an `increments` list
    ## and unsets the False value set in an init offset -2 block.

    ## ---! Developer Mode
    ## Enables various tools, like the console, and changes how certain errors
    ## are handled.
    config.developer = True

init 0 python:

    ## --- Missing Backgrounds (7.4.0)
    ## What to show when developer mode is active and an undefined image is used
    ## in a scene statement. Accepts an image name as a string.
    # config.missing_background = "black"

    ## --- Missing Fonts
    ## Whether to search for missing fonts on the user's system even in
    ## developer mode. For non-developers, this happens regardless.
    config.allow_sysfonts = False

    ## --- Report Extraneous Image Attributes
    ## Whether to raise an exception when images are given unused attributes.
    config.report_extraneous_attributes = True

    ## --- Show Patterned Tiles
    ## Whether to show patterned tiles instead of transparency in Dev Mode.
    config.transparent_tile = True

    ## --- Simulate Joystick
    ## Whether to show the joystick menu even when no joystick is connected.
    config.always_has_joystick = True

    ## --- Debug Mode
    # Whether to throw a fatal error for missing files, among other things.
    config.debug = True

    ## Whether to raise exceptions encountered by DictEquality and FieldEquality
    ## classes, which many built-in action objects inherit from.
    config.debug_equality = False

    ## Whether to raise exceptions when sound playback fails.
    config.debug_sound = True

    ## (7.4.0) Whether to draw the text alignment pattern.
    # config.debug_text_alignment = False

    def print_labels():
        """
        Prints all labels in the game.
        """
        namemap = renpy.get_all_labels()
        for label in namemap:
            print(label)

## -- Keymap -------------------------------------------------------------------
## Let's not take these keys away from the list of available keys in the
## compiled build of the game.

init 1 python:

    ## Init offset 1: Overrides this key being unset in the non-dev keymap
    config.keymap["debug_voicing"] = ["alt_K_v"] ## Debug self-voicing

init python:

    ## --- Keymap
    config.keymap["developer"] = ["shift_K_d"] ## Show ceveloper menu
    config.keymap["director"] = ["K_d"] ## Start director mode
    config.keymap["console"] = ["shift_K_o"] ## Show console
    config.keymap["console_older"] = ["K_UP", "repeat_K_UP"]
    config.keymap["console_newer"] = ["K_DOWN", "repeat_K_DOWN"]
    config.keymap["image_load_log"] = ["K_F4"]
    config.keymap['launch_editor'] = ["shift_K_e"] ## Open current script file
    config.keymap["performance"] = ["K_F3"] ## Show FPS and performance mode
    config.keymap["profile_once"] = ["K_F8"] ## Enable frame profiling

    ## --- (Keymap) Memory Profile
    ## If renpy.experimental is True or RENPY_EXPERIMENTAL is true in
    ## Environment variables, this key will print a report of memory usage, in
    ## bytes, of all the game components, to memory.txt. (It's pretty slow.)
    config.keymap["memory_profile"] = ["K_F7"]

    ## --- (Keymap) Auto-Reload
    ## The key to trigger auto-reload mode or reload the game.
    config.keymap["reload_game"] = ["shift_K_r", "alt_shift_K_r"]

    ## --- (Keymap) Simple Style Inspector
    config.keymap["inspector"] = ["shift_K_i"]

    ## --- (Keymap) Full Style Inspector
    config.keymap["full_inspector"] = ["alt_shift_K_i"]

    ## --- (Keymap) Dump to Styles.txt
    config.keymap["dump_styles"] = ["shift_K_y"]


## -- Auto-Play ----------------------------------------------------------------

init python:

    ## Time to wait before randomly selecting a choice from a choice menu.
    config.auto_choice_delay = None

    ## Whether to end renpy.input() immediately and return its default argument.
    config.disable_input = False

    def auto_command():
        """
        Adds a function to launch the game in "auto" mode, for testing or
        demonstration purposes. Auto mode removes or most in-game pauses and
        progresses through choices and interactive elements without user input.
        """
        global is_automode

        ap = renpy.arguments.ArgumentParser(
            description=__("Runs the given project in auto mode."), require_command=False)
        ap.add_argument("--testing", default=True,
            help=__("Whether we're running auto mode to debug. Default True."))
        ap.add_argument('--variant', dest="variant", default=None,
            help=__("The screen variant to test, if any."))
        # ap.add_argument("--route", dest="route", default=False,
        #   help=__("The route to run."))
        args = ap.parse_args()

        args.testing = bool(args.testing)
        args.variant = str(args.variant).lower()

        _preferences.afm_enable = True
        config.disable_input = True
        config.auto_choice_delay = 5.0

        os.environ["RENPY_SKIP_SPLASHSCREEN"] = "1"
        os.environ["RENPY_SKIP_MAIN_MENU"] = "1"
        os.environ["RENPY_LESS_PAUSES"] = "1" ## Skip {w} and {p} tags

        if args.testing:
            config.log = "log-%s.txt" % args.variant.replace(" ", "_")
            config.profile = True
            _preferences.afm_time = 0.0001
            preferences.wait_voice = False
            preferences.text_cps = 300
            config.auto_choice_delay = 0.1

            os.environ["RENPY_TIMEWARP"] = "2.0"

        ## This will cause the game to shut down if it encounters an error
        ## instead of showing a graphical exception screen.
        # os.environ["RENPY_SIMPLE_EXCEPTIONS"] = "1"

        return True

    renpy.arguments.register_command("auto", auto_command)

## -- Auto-Reload --------------------------------------------------------------

init python:

    ## Whether pressing the auto-reload key enables auto-reload mode. If True,
    ## the game will reload on press, and also every time the script files are
    ## saved, until you press the auto-reload key again. If False, the game will
    ## only reload when you press the auto-reload key.
    config.autoreload = True

    ## Whether to attempt to return to the same menu after a reload.
    config.reload_menu = True

    ## ---! Auto-Reload Ignore List
    ## Auto-reload will not be triggered by changing game files if they have any
    ## of the extensions in this blacklist. Here we're ignoring error-generated
    ## screenshots, which are deleted when the screen is closed.
    config.autoreload_blacklist.append("_error.png")
    config.autoreload_blacklist.append("_error.jpeg")
    config.autoreload_blacklist.append("_error.bmp")
    config.autoreload_blacklist.append("_error.tga")

    ## --- Auto-Reload Functions (7.4.0)
    ## List of (regex, autoreload function) tuples to run before an auto-reload.
    ## By default, Ren'Py uses this to flushe the cache for images and audio.
    # config.autoreload_functions = []

    ## List of Python module names to reload whenever the game is reloaded.
    config.reload_modules = []

## -- Linting ------------------------------------------------------------------

init python:

    ## --- (Callbacks) Linting
    ## List of functions that are called, with no arguments, when lint is run.
    ## The functions should check the script data and report any errors using
    ## standard output or the  Python print statement.
    # config.lint_hooks = []

    ## --- (Callbacks) Lint Stats
    ## List of functions called, without arguments, to generate stats at the end
    ## of a lint file. This can be done using print().
    # config.lint_stats_callbacks = []

    ## A list of built-in Python names that can be replaced without lint
    ## reporting an error.
    # config.lint_ignore_replaces.append()

    ## Whether to report an error for screens defined without a parameter list.
    config.lint_screens_without_parameters = True

## -- Logging ------------------------------------------------------------------

init python:

    ## Log width in number of characters.
    config.log_width = 80

    ## (Callbacks) Logging a Line
    ## List of functions called when creating a line entry in a log. These are
    ## called with one argument, the current line log entry (lle) object.
    # config.line_log_callbacks = []

    ## --- Garbage Collection Log
    ## Whether to log info about the objects that trigger garbage collection.
    config.gc_print_unreachable = False

    ## --- Image Cache Log
    ## Whether to log information about the image cache to image_cache.txt.
    config.debug_image_cache = False

    ## --- Statement Log
    ## Name of the file to log text to from say or menu statements, or None
    ## to disable the statement log.
    config.log = None

    ## --- Save Log
    ## Whether to write a file called save_dump.txt whenever a game is saved.
    ## This file contains information about the objects that have been saved.
    ## Each line contains the object's approximate size, the path to the object,
    ## whether the object is an alias, and a representation of the object.
    config.save_dump = False

    ## Whether to use cPickle module to save the game. If False, Ren'Py will use
    ## the pickle module instead. This makes the game slower, but is better for
    ## reporting save file errors.
    config.use_cpickle = True

    ## --- Text Overflow Log
    ## Whether to log instances of dialogue box overflow to text_overflow.txt.
    config.debug_text_overflow = False

## -- Profiling ----------------------------------------------------------------

init python:

    ## --- Profiling
    # Whether to show profile data as stdout when the game is launched from the
    # command line.
    config.profile = False

    ## Name of the event to check to see if the profile needs to be printed.
    config.profile_to_event = "flip"

    ## --- Profiled Screens
    ## List of screens for which screen profiling should be enabled. Screen
    ## profile data is logged to profile_screen.txt in the game directory.
    config.profile_screens = []

    ## --- Init Block Profiling (7.4.0)
    ## Init blocks taking longer than this are logged to log.txt.
    # config.profile_init = 0.25

    ## How long frames have to take (to the event) to trigger profiling.
    config.profile_time = 1.0 / 50.0

    ## --- Reload Profiling
    config.profile_reload = False

## -- Style Inspector ----------------------------------------------------------
## https://www.renpy.org/doc/html/style.html#style-inspector

#init python:

    ## Custom function to call as the style inspector.
    # config.inspector = None
