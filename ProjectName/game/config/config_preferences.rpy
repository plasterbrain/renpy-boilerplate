################################################################################
## Config: Preferences
################################################################################
## Settings for preferences and how the player interacts with the game.

## -- Preferences: General -----------------------------------------------------
## Visual novel gameplay and other basic settings.

init python:

    ## Default translation language. None defaults to the game's native
    ## language or the user's preference, if they set one.
    config.language = None
    config.default_language = None

    ## --- Language Autodetect (7.1.2)
    ## Try to set game language based on the user's system locale.
    config.enable_language_autodetect = False

    ## A function that determines what language to use based on system locale.
    ## It accepts two string parameters, the ISO code of the system locale and
    ## the ISO code of the system region. It should return a string naming the
    ## translation to use, or None to use the default translation.
    config.locale_to_language_function = _locale_to_language_function

    ## --- Rollback
    ## Allow the user to roll back (i.e., "rewind" the game).
    config.rollback_enabled = False

    ## --- Allow Skipping
    ## Allow the user to skip (i.e., "fast-forward" the game).
    #TODO (!) Only skip text after beating the game once.
    config.allow_skipping = True

    #TODO stop when thoughts appear option
    #TODO notification the first time you try to skip that u may miss thoughts

    ## Approximate amount of time that dialogue will be shown for, when skipping
    ## statements using the ctrl key, in milliseconds.
    config.skip_delay = 75

    ## --- Allow Fast Skipping
    ## Whether players can skip to the next choice (or other stopping point)
    ## using the fast skip key or on-screen button
    config.fast_skipping = False

    ## --- Auto-Forward Mode (AFM)
    ## Number of bonus characters added to every string in AFM.
    config.afm_bonus = 25

    ## Number of characters in a string it takes to trigger AFM delay.
    config.afm_characters = 250

## ---! Text Speed
## Text display speed in characters per second (an integer). If set to 0, text
## will display all at once, without a "typewriter" effect.
default preferences.text_cps = 50

## ---! Skip Mode
## Whether to skip all text (True) or only text the player has seen (False).
default preferences.skip_unseen = False
## Whether to continue skipping after a choice menu.
default preferences.skip_after_choices = False

## ---! Auto-Forward Mode
default preferences.afm_enable = False
## Time to wait for auto-forward mode. Bigger numbers are slower.
default preferences.afm_time = 15
## Whether AFM continues after the user clicks.
default preferences.afm_after_click = False
## Whether AFM should wait for voice files and self-voicing to finish.
default preferences.wait_voice = True

## ---! Self-Voicing
default preferences.self_voicing = False
## When self-voicing is playing, the other channels drop to this volume.
default preferences.self_voicing_volume_drop = 0.5

## -- Audio --------------------------------------------------------------------

init python:

    ## ---! Volumes
    ## Mixer volume, a float value from 0.0 (muted) to 1.0 (full volume).
    config.default_music_volume = 1.0
    config.default_sfx_volume = 1.0
    config.default_voice_volume = 1.0

    ## --- Sample Sounds
    ## Sounds used for the "Test" button in Preferences, to test audio levels.
    config.sample_sound = None
    config.sample_voice = None

## ---! Emphasize Audio
## Whether to emphasize the channels in `config.emphasize_audio_channels` while
## they're playing by reducing the volume of the other channels.
default preferences.emphasize_audio = False

## ---! Subtitles
## Whether to show text said by the subtitle character.
default persistent.prefs_subtitles = False

## ---! Voice Sustain
## Whether a voice clip plays until it is finished or replaced by another clip.
## If False, the voice line ends when the line of dialogue advances.
default preferences.voice_sustain = False

## -- Display ------------------------------------------------------------------

init python:

    ## ---! Window Resizing
    # Whether the user is allowed to resize an OpenGL-drawn window.
    config.gl_resize = False

    ## Store the physical window size as part of save data.
    config.save_physical_size = True

    #---------------------------------------------------------------------------
    def _set_prefs_resolution():
        """
        Sets the screen resolution based on `persistent.prefs_resolution`. If
        not a valid size, it will reset the screen size to the program default.
        """
        if persistent.prefs_resolution not in increments.prefs_resolution_list:
            persistent.prefs_resolution = (config.screen_width, config.screen_height)
        if persistent.prefs_resolution and not preferences.fullscreen:
            SetResolution(persistent.prefs_resolution)
    _set_prefs_resolution()

## ---! Font Family
## This option allows users to change the in-game font.
default preferences.font_transform = increments.font_transform_list[0]

## ---! Font Size
## Scales the font size.
default preferences.font_size = 1.0

## ---! Line Spacing
## Scales the spacing between lines.
default preferences.font_line_spacing = 1.0

## ---! Fullscreen
default preferences.fullscreen = False

## ---! Resolution
default persistent.prefs_resolution = (config.screen_width,config.screen_height)

## ---! Renderer
## Graphics renderer.
default preferences.renderer = "auto"

## ---! Show Transitions
## Which transitions should be shown. Accepts 2 for all transitions, or 0 for no
## transitions. (1 is reserved.)
default preferences.transitions = 2

## ---! Show Video Sprites
## Whether to show images instead of videosprites.
default preferences.video_image_fallback = False

## ---! Framerate
## Target framerate. Accepts an integer, or None to attempt to draw at the
## monitor's full framerate.
default preferences.gl_framerate = None

## ---! Refresh Rate
## How often to draw an unchanging screen. Accepts True to draw the screen 5
## times a second, False to draw at the full framerate, or "auto" to draw at 5hz
## when the device is using battery power.
default preferences.gl_powersave = "auto"

## ---! GL Tearing
## Whether to use tearing (True) or frameskip (False) when the game can't keep
# up with its intended framerate.
default preferences.gl_tearing = False

## -- Controls -----------------------------------------------------------------
## https://www.renpy.org/doc/html/keymap.html

init python:

    ## --- Pygame Events
    ## https://www.pygame.org/docs/ref/event.html
    ## List of additional PyGame events the game accepts.
    config.pygame_events = []

    ## ---! Underlay
    ## Extra keymap functions.
    config.underlay.append(renpy.Keymap(thought1 = NullAction()))
    config.underlay.append(renpy.Keymap(thought2 = NullAction()))
    config.underlay.append(renpy.Keymap(thought3 = NullAction()))
    config.underlay.append(renpy.Keymap(history = Call("history")))
    config.underlay.append(renpy.Keymap(phone = ShowMenu("phone")))
    config.underlay.append(renpy.Keymap(preferences =
        If(renpy.get_screen("preferences"),
        Hide("preferences"), Show("preferences"))))

    ## --- Keyboard Repeat
    ## Rate of keyboard repeat, in seconds, a tuple containing the delay
    ## before the first repeat and the delay between subsequent repeats. If
    ## None, keyboard repeat is disabled.
    config.key_repeat = (.3, .03)

    ## Amount of penalty to apply to moves perpendicular to the selected
    ## direction of motion, when moving focus with the keyboard.
    config.focus_crossrange_penalty = 1024

    ## --- (Mobile) Gesture Dispatch Function
    ## Function used to dispatch gestures. It is called with one argument, a
    ## raw gesture string to dispatch as an event.
    config.dispatch_gesture = None

    ## --- (Mobile) Gesture Size
    ## Size of gesture components, as a fraction of screen_width.
    config.gesture_component_size = .05
    ## Size of gesture strokes, as a fraction of screen_width.
    config.gesture_stroke_size = .2

    ## --- (Mobile) Longpress
    ## How long the screen must be pressed for it to register as a longpress.
    config.longpress_duration = 0.5
    ## The range the press must remain in to register as a longpress.
    config.longpress_radius = 15
    ## The amount of time the device will vibrate for after a longpress.
    config.longpress_vibrate = .1

    ## ---! (Mobile/Mouse) Rollback Side
    ## Tapping or clicking the side of the screen causes the game to roll back.
    config.enable_rollback_side = False

## --- Automatic Mouse Move
# Whether the mouse should automatically move to the selected button.
default preferences.mouse_move = False

## -- Data Settings ------------------------------------------------------------

init python:

    ## --- Performance Test
    ## Whether to run a short OpenGL performance test on startup (desktop
    ## only). If errors are found, the user will be shown a warning (the
    ## `_performance_warning` screen) where they can then choose whether they
    ## want the warning to pop up in the future.
    config.performance_test = True

## ---! Performance Test
## Whether Ren'Py should do a performance test and warn the user if there are
## display issues on startup.
default preferences.performance_test = True

init 1 python:

    #---------------------------------------------------------------------------
    ## Init offset 1: Needs custom persistent-based preference defaults set
    def set_persistent_pref_defaults():
        """
        Adds any persistent fields beginning with "prefs_" and their original
        values to a preferences dictionary, which we can use if the user wants
        to reset their preferences.
        """
        if persistent._custom_prefs_default:
            return
        persistent._custom_prefs_default = {}

        for name, value in persistent.__dict__.iteritems():
            if not name.startswith("prefs_"):
                continue

            persistent._custom_prefs_default[name] = value
    set_persistent_pref_defaults()
