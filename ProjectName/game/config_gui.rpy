################################################################################
## Configuration: GUI, Screens, and Styles
################################################################################
init offset = -1 #TODO ?

init python:

    gui.init(1440, 810)

    ## --- Cursors
    ## A dictionary mapping mouse types ("default", "say", "with", "menu",
    ## "prompt", "imagemap", "pause", "mainmenu", and "gamemenu" by default) to
    ## a tuple containing the cursor image, the cursor xoffset, and he cursor
    ## yoffset. The "default" key should always be present, as it is used when
    ## a more specific key is absent. If None, the system mouse is used.
    config.mouse = None

    ## The mouse is hidden after this number of seconds has elapsed without any
    ## mouse input. If None, the mouse will never be hidden.
    config.mouse_hide_time = 30

    #---------------------------------------------------------------------------
    gui.arrow_left = u"\u25C0"
    gui.arrow_right = u"\u25B6"
    gui.warning_symbol = u"\u26A0"

    gui.glyph_font = "DejaVuSans.ttf"

## -- Program Images -----------------------------------------------------------

init python:

    ## ---! Window Icon
    ## The icon shown in the taskbar/dock and on the application window. Accepts
    ## a string with the icon filename or None.
    config.window_icon = None

    ## --- OpenGL Clear Color
    ## The color that the window is cleared to before images are drawn.
    ## This is mainly seen as the color of the letterbox or pillarbox edges if
    ## the game's aspect ratio is different than what's being displayed.
    config.gl_clear_color = "#000"

    ## --- Performance Test Image
    ## If `config.performance_test` and `_preferences.performance_test` are both
    ## true, this image will be used when running the OpenGL performance test on
    ## startup, for 5 frames (.25 seconds).
    config.gl_test_image = "black"

## -- Screen Language Settings -------------------------------------------------

init python:

    ## Whether the order of Side positions determines their render order.
    config.keep_side_render_order = True

    ## --- Hyperlink Style Inheritance (6.99.13)
    ## Whether hyperlinks inherit size from the surrounding text.
    config.hyperlink_inherit_size = True

    ## The maximum size of xfit, yfit, first_fit, etc.
    config.max_fit_size = 8192

## -- Screen Settings ----------------------------------------------------------

init python:

    ## --- Variants
    ## List of screen variants that are searched when choosing a screen to
    ## display to the user. This should always end with None, to ensure that the
    ## default screens are chosen.
    # config.variants = [None]

    ## --- (Callbacks) Screen Redraw
    ## Functions called, without arguments, to determine if Ren'Py needs to
    ## redraw the screen.
    # config.needs_redraw_callbacks.append()

    ## List of names of screens that should be updated once per frame, rather
    ## than once per interaction.
    # config.per_frame_screens.append()

    ## Whether a "with None" statement will be performed after interactions
    ## caused by dialogue, menus, input, and imagemaps. This ensures that old
    ## screens will not show up in transitions.
    config.implicit_with_none = True

    ## --- Overlay Functions
    ## List of overlay functions called when the window is shown. This is used
    ## to show the FPS and the skip indicators, for example.
    # config.window_overlay_functions.append()

    ## Whether overlays are shown during "with" statements.
    config.overlay_during_with = True

    ## --- Remove Screens on Copy
    ## Screens to remove when the game state is stored for rollback or saving.
    config.context_copy_remove_screens = ["notify"]

    ## Whether screens participate in transitions, dissolving from the old state
    ## of the screen to the new state of the screen. If False, only the latest
    ## state of the screen will be shown.
    config.transition_screens = True

## -- Style Settings -----------------------------------------------------------

init python:

    ## --- (Callbacks) Rebuilding Styles
    ## List of functions, called without arguments, just before rebuilding
    ## styles, for example if the user changes style preferences.
    # config.build_styles_callbacks.append()

    ## (6.99.13) Whether to apply position properties to the side of a viewport.
    config.position_viewport_side = True

    ## --- Hyperlink Styler
    ## Function called with a single argument to get the style object to use for
    ## a hyperlink. It's called with the argument of the hyperlink.
    config.hyperlink_styler = None

    ## --- Hyperlink Focus
    ## Function called with a single argument when a hyperlink gains or loses
    ## focus. It is called with either the argument of the hyperlink or None,
    ## respectively. If it returns a value other than None, the interaction
    ## returns that value.
    config.hyperlink_focus = None

    ## --- (Callback) Hyperlink Clicked
    ## Function is called, with a single argument, when a hyperlink is clicked.
    ## It is called with the argument of the hyperlink. If it returns a value
    ## other than None, the interaction returns that value.
    config.hyperlink_callback = None

    ## Protocol used for hyperlinks that do not have a protocol assigned.
    config.hyperlink_protocol = "call_in_new_context"

## -- Font Settings ------------------------------------------------------------

init python:

    ## ---! Font Directory
    font_directory = "gui/fonts/"

    ## ---! Font Replacement
    ## Dictionary mapping (font, bold, italics) to (font, bold, italics), used
    ## to replace fonts with specialized bold/italic versions.
    config.font_replacement_map = {
        (font_directory + "Lato.ttf", True, False):
            (font_directory + "Lato-bold.ttf", False, False)}

    ## --- Font Transforms (7.2.2)
    ## Dictionary mapping font names to font transform functions. It's used by
    ## the accessibility module to configure OpenDyslexic.
    # config.font_transforms[] = None

    ## --- Font Scaling (7.2.2)
    ## Dictionary mapping truetype font names to their scaling factor. It's used
    ## by the accessibility module to scale OpenDyslexic.
    # config.ftfont_scale[] = None

    ## Dictionary mapping truetype font names to their ascent/descent scaling
    ## factor. It's used for scaling OpenDyslexic.
    # config.ftfont_vertical_extent_scale[] = None

## -- Default Styles -----------------------------------------------------------

init python:

    gui.h1_color = "#0099cc"
    gui.h2_color = "#8d9fb3"
    gui.h3_color = "#5b6a77"
    gui.tt1_color = "#535353"
    gui.tt2_color = "#919191"

    gui.idle_color = "#888888"
    gui.idle_small_color = "#aaaaaa"
    gui.hover_color = "#66c1e0"
    gui.selected_color = "#ffffff"
    gui.selected_insensitive_color = "#46525e"
    gui.insensitive_color = "#8888887f"

    ## Colors used for the portions of bars that are not filled in. These are
    ## not used directly, but are used when re-generating bar image files.
    gui.muted_color = "#003d51"
    gui.hover_muted_color = "#005b7a"

    gui.text_font = "DejaVuSans.ttf"

style default:
    language "unicode"
    size 22 ## mobile: 30

style input:
    adjust_spacing False

style hyperlink_text:
    hover_underline True

style gui_text:
    color "#ffffff"
    font gui.text_font
    size 22 ## mobile: 30

style button:
    padding (4, 4)
    xsize None
    ysize None

style button_text is gui_text:
    color gui.idle_color
    hover_color gui.hover_color
    insensitive_color gui.insensitive_color
    selected_color gui.selected_color
    text_align 0.0
    xalign 0.0
    yalign 0.5

style label_text is gui_text

style prompt_text is gui_text

## -- (Default Styles) Bars ----------------------------------------------------
## Used to show or adjust an amount out of 100% (ex. volume sliders).

init python:

    gui.bar_width = 25
    gui.bar_tile = False
    gui.bar_borders = Borders(4, 4, 4, 4)

image bar_full = Solid("#66C1E0")
image bar_empty = Solid("#003D51")

style bar:
    ysize gui.bar_width
    left_bar Frame("bar_full", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("bar_empty", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_width
    top_bar Frame("bar_empty", gui.bar_borders, tile=gui.bar_tile)
    bottom_bar Frame("bar_full", gui.bar_borders, tile=gui.bar_tile)

## -- (Default Styles) Scrollbars ----------------------------------------------
## Used to indicate current position in a viewport.

init python:

    gui.scrollbar_width = 20

image idle_scrollbar = Solid("#1a1a1a")
image hover_scrollbar = Solid("#1a1a1a")
image idle_scrollbar_thumb = Solid("#696969")
image hover_scrollbar_thumb = Solid("#888")

style scrollbar:
    ysize gui.scrollbar_width
    base_bar Frame("[prefix_]scrollbar", Borders(4, 4, 4, 4), tile=False)
    thumb Frame("[prefix_]scrollbar_thumb", Borders(4, 4, 4, 4), tile=False)
    unscrollable "hide"

style vscrollbar is scrollbar:
    xsize gui.scrollbar_width
    ysize None

## -- (Default Styles) Sliders -------------------------------------------------
## Not the hamburger kind. Used for setting a numerical amount out of an
## arbitrary range (ex. text speed).

init python:

    gui.slider_width = 25 ## mobile: 36

image idle_slider = Solid("#003D51")
image hover_slider = Solid("#005B7A")

## The draggable part on an option slider.
image idle_slider_thumb = Solid("#919191")
image hover_slider_thumb = Solid("#bebebe")

style slider:
    ysize gui.slider_width
    base_bar Frame("[prefix_]slider", Borders(4, 4, 4, 4), tile=False)
    thumb "[prefix_]slider_thumb"

style vslider is slider:
    xsize gui.slider_width
    ysize None
