################################################################################
## GUI: HUD Elements & Popups
################################################################################
## This file contains screens that appear on top of regular gameplay interface
## to provide quick actions or show the player a message.

init python:
    ## Sure, let's assume there could be 99 other things on screen.
    gui.quickmenu_zorder = 100
    gui.notify_zorder = 101
    gui.confirm_zorder = 103

## -- Loading Icon -------------------------------------------------------------
## Shows the user that something is occurring in the background.

init python:

    def check_autosave():
        """
        Shows the load icon overlay with the text "Saving..." for 1 second
        whenever the game saves automatically.
        """
        if not renpy.loadsave.autosave_not_running.isSet():
            renpy.hide_screen("loading")
            renpy.show_screen("loading")

    config.start_interact_callbacks.append(check_autosave)

## type: The purpose of this loading icon, either "save" (for saving a file) or
## "load" (for loading something).
screen loading(type="save"):
    zorder gui.notify_zorder
    $ load_text = _("Saving...") if type == "save" else _("Loading...")
    text load_text xpos .88 ypos .94
    add "load_icon" xpos 1.0 ypos 1.0 xoffset -64 yoffset -64
    if type == "save":
        timer 1 action Hide("loading")
    transclude

## -- Quick Menu ---------------------------------------------------------------
## The quick menu is displayed in-game near the dialogue box to provide easy
## access to various visual novel and game menu functions.

init python:

    ## Use this to temporarily hide the quick menu during the game.
    quick_menu = True

    ## --- Overlay Screens
    config.overlay_screens.append("quick_menu")

screen quick_menu():
    zorder gui.quickmenu_zorder

    if quick_menu:
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign .99

            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu("history")
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Q.Save") action QuickSave()
            textbutton _("Q.Load") action QuickLoad()
            if config.has_voice and not renpy.sound.is_playing("voice"):
                #TODO test voice replay button.
                textbutton _("Replay") action Play("voice", _last_voice_play)

## --- Mobile Version
screen quick_menu():
    variant "touch"
    zorder gui.quickmenu_zorder

    if quick_menu:
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign .99

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()

style quick_button is default

style quick_button:
    padding (10, 4, 10, 0) ## mobile: (40, 14, 40, 0)

style quick_button_text is button_text
style quick_button_text:
    color gui.idle_small_color
    selected_color gui.selected_color
    size 14 ## mobile: 20

## -- Confirm screen -----------------------------------------------------------
## https://www.renpy.org/doc/html/screen_special.html#confirm

init python:
    #TODO test editing these
    gui.ARE_YOU_SURE = _("Are you sure?")
    gui.DELETE_SAVE = _("Are you sure you want to delete this save?")
    gui.OVERWRITE_SAVE = _("Are you sure you want to overwrite your save?")
    gui.LOADING = _("Loading will lose unsaved progress.\nAre you sure you want to do this?")
    gui.QUIT = _("Are you sure you want to quit?")
    gui.MAIN_MENU = _("Are you sure you want to return to the main menu?\nThis will lose unsaved progress.")
    gui.END_REPLAY = _("Are you sure you want to end the replay?")
    gui.SLOW_SKIP = _("Are you sure you want to begin skipping?")
    gui.FAST_SKIP_SEEN = _("Are you sure you want to skip to the next choice?")
    gui.FAST_SKIP_UNSEEN = _("Are you sure you want to skip unseen dialogue to the next choice?")

## message: The message to show the user, as a string.
## yes_action: The action to take if the user selects "Yes."
## no_action: The action to take if the user selects "No."
screen confirm(message, yes_action, no_action):
    modal True
    zorder gui.confirm_zorder

    style_prefix "confirm"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action

style confirm_frame is gui_frame #TODO ?
style confirm_frame:
    background Frame(Solid("#00000099"), Borders(40, 40, 40, 40), False)
    padding (40, 40)
    xalign 0.5
    yalign 0.5

style confirm_button is gui_medium_button #TODO ?

style confirm_button_text is gui_medium_button_text #TODO ?
style confirm_button_text:
    text_align 0.5
    xalign 0.5


style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text

## -- Confirm: Quit ------------------------------------------------------------
## A specific form of the quit prompt which shows the options vertically and
## includes three actions: MainMenu(), Quit() and cancel.

screen game_menu_quit():
    modal True
    zorder gui.confirm_zorder

    style_prefix "confirm"

    frame:
        vbox:
            xalign .5
            yalign .5

            label _("Are you sure you want to quit? You will lose all unsaved progress."):
                style "confirm_prompt"
                xalign 0.5

            textbutton _("Exit to Main Menu"):
                action MainMenu()
            textbutton _("Exit to Desktop"):
                action Quit(False)
            textbutton _("Cancel"):
                action Hide("game_menu_quit")
                keysym "game_menu"

## -- Skip Indicator -----------------------------------------------------------
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():
    zorder gui.notify_zorder

    style_prefix "skip"

    frame:
        hbox:
            spacing 6

            text _("Skipping")
            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"

## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat

style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    padding (16, 5, 50, 5)
    ypos 10

style skip_text:
    size 16 ## mobile: 25

style skip_triangle:
    ## This font has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it.
    font "DejaVuSans.ttf"

## -- Notify Screen ------------------------------------------------------------
## https://www.renpy.org/doc/html/screen_special.html#notify-screen
##
## The notify screen is used to show the player a message, for example, when
## the game is quicksaved or a screenshot has been taken.

## message: The message to show the player, as a string.
screen notify(message):
    zorder gui.notify_zorder

    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    background Frame(Solid("#000000BB"), Borders(16, 5, 40, 5), tile=False)
    padding (16, 5, 40, 5)
    ypos 45

style notify_text:
    size 16 ## mobile: 25

## -- Progress Screen ----------------------------------------------------------
## This screen depicts the number of dialogue blocks the player has seen out of
## the total number of dialogue blocks.

screen _progress:
    $ new = renpy.count_newly_seen_dialogue_blocks()
    $ seen = renpy.count_seen_dialogue_blocks()
    $ total = renpy.count_dialogue_blocks()

    drag:
        draggable True
        focus_mask None
        xpos 0
        ypos 0

        text "[new] [seen]/[total]":
            size 14
            color "#fff"
            outlines [(1, "#000", 0, 0)]
            alt ""
