################################################################################
## GUI: ADV/NVL Mode
################################################################################
## This file contains screens used to display dialogue and choice menus.

init python:
    #TODO Newer Ren'Py may have made this obsolete
    def say_get_alt(what):
        """
        Strips out Ren'Py text tags from a string.

        Parameters
        ----------
        what : str
            The dialogue to search and remove tags from.

        Returns
        -------
        str
            The "what" text, sanitized for TTS.
        """
        ## Replace {a=[...]} with line indicating there's a link.
        what = re.sub(r"(\{\{)|(?:\{(?:\/?)(?:a|\#)(?:\=(?:[^}]*))?\})", ", " + _("Linked text:") + " ", what, 1)

        ## Remove all tags except {fast}.
        what = re.sub(r"(\{\{)|(?:\{(?:\/?)(?:a|alpha|art|b|clear|color|cps|font|i|image|k|nw|outlinecolor|p|plain|rb|rt|s|size|space|u|vspace|w|\#)(?:\=(?:[^}]*))?\})", "", what)
        while "{fast}" in what:
            # Don't reread the whole text if line is extended.
            parts = what.partition("{fast}")
            what = parts[2]
        return what

## -- Say screen ---------------------------------------------------------------
## https://www.renpy.org/doc/html/screen_special.html#say
## https://www.renpy.org/doc/html/side_image.html
##
## Thsi screen displays dialogue to the player. It needs a text displayable
## with id "what", as Ren'Py uses this to manage text display. It can also
## create displayables with id "who" and id "window" to apply style properties.

## who: The name of the speaking character, or None if no name is given.
## what: The text to be "spoken."
screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what" alt say_get_alt(what)

        # if _preferences.afm_enable:
            #TODO auto mode graphics

    if not renpy.variant("small"): ## The side image does not show up on mobile.
        add SideImage() xalign 0.0 yalign 1.0

style window is default:
    background Solid((0, 0, 0, gui.say_alpha))
    xalign 0.5
    xfill True
    yalign 1.0
    ysize 185 ## mobile: 240

style namebox is default
style namebox:
    padding (5, 5)
    xpos 240 ## mobile: 80
    xanchor 0.0
    xsize None ## None sizes automatically
    ypos 0
    ysize None ## None sizes automatically

style say_label is default
style say_label:
    xalign 0.0
    yalign 0.5

style say_label_text:
    size 30 ## mobile: 36

style say_dialogue is default
style say_dialogue:
    xalign 0.0
    xpos 268
    xsize 744
    ypos 50

style say_thought is say_dialogue

## -- Choice Menu --------------------------------------------------------------
## https://www.renpy.org/doc/html/screen_special.html#choice
##
## This screen is used to display the in-game choice menus.

init python:
    ## Whether to shuffle the menu choices.
    menu_shuffled = False

    ## Whether show give menu captions as text spoken by the narrator.
    config.narrator_menu = False
    
    ## Whether to show unavailable choices as disabled buttons
    config.menu_include_disabled

## items: A list of choice objects, each with caption and action fields.
screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox is vbox

style choice_vbox:
    spacing 22
    xalign 0.5
    ypos 270
    yanchor 0.5

style choice_button is button #TODO ?
style choice_button is default:
    padding (100, 5, 100, 5)
    xsize 790 ## mobile: 1240
    # ysize None
    # tile False

style choice_button_text is button_text #TODO ?
style choice_button_text is default:
    color "#cccccc"
    hover_color "#ffffff"
    insensitive_color "#444444"
    size 30 ## default.text_size
    text_align 0.5
    xalign 0.5 ## choice_button_text.xalign

## -- (Subscreen) Timed Menu ---------------------------------------------------
## Showing this screen at the same time as a choice menu will give it a time
## limit, jumping to the specified label if the user doesn't answer in time.

screen menu_timer(amount, target):
    timer amount action [Jump(target), Hide("menu_timer")]

## -- NVL Screen ---------------------------------------------------------------
## https://www.renpy.org/doc/html/screen_special.html#nvl
##
## This screen is used for NVL-mode dialogue and choice menus.

init python:

    ## --- NVL Entry Height
    ## The height of each NVL mode dialogue entry.
    gui.nvl_height = 115 ## mobile: 170

    ## --- NVL List Length
    ## The max number of dialogue entries to show at a time in NVL mode. If
    ## None, dialogue should have a fixed height and the window should scroll.
    config.nvl_list_length = 6

    ## --- NVL Mode CTC
    ## The click-to-continue indicator that is used for NVL mode characters that
    ## are at the end of a page. (That is, immediately followed by an nvl clear
    ## statement.) This replaces the ctc parameter of Character().
    config.nvl_page_ctc = None

    ## This replaces the ctc_position parameter of Character().
    config.nvl_page_ctc_position = "nestled"

    ## --- NVL Mode Rollback
    ## Whether NVL mode rollback goes by pages (True) or lines of dialogue.
    config.nvl_paged_rollback = False

    ## --- NVL Screen Layer
    config.nvl_layer = "screens"

## dialogue: list of currently shown NVL dialogue entries.
## items: List of NVL menu choices, if any.
screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing 10 ## only used if not gui.nvl_height, or before choices

        if gui.nvl_height:
            vpgrid:
                cols 1
                yinitial 1.0

                use _nvl_dialogue(dialogue)
        else:
            use _nvl_dialogue(dialogue)

        ## Choice Menu
        for i in items:
            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0

## Shows the name and speaker for each line of NVL Mode dialogue.
screen _nvl_dialogue(dialogue):

    for d in dialogue:
        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id

style nvl_window is default
style nvl_window:
    background Solid("#000000cc")
    padding (20, 20)
    xfill True
    yfill True

style nvl_entry is default
style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label is say_label
style nvl_label:
    xpos 430 ## mobile: 325
    xanchor 1.0 ## nvl_label.text_align
    ypos 0
    yanchor 0.0
    xsize 150 ## mobile: 305
    min_width 150 ## nvl_label.xsize
    text_align 1.0

style nvl_dialogue is say_dialogue
style nvl_dialogue:
    xpos 450 ## mobile: 345
    xanchor 0.0 ## nvl_dialogue.text_align
    ypos 8 ## mobile: 5
    xsize 590 ## mobile: 915
    min_width 590 ## nvl_dialogue.xsize
    text_align 0.0
    layout "tex" ## "subtitle" if nvl_dialogue.text_align != 0.0

style nvl_thought:
    xpos 240 ## mobile: 20
    xanchor 0.0 ## nvl_thought.text_align
    ypos 0
    xsize 780 ## mobile: 1240
    min_width 780 ## nvl_thought.xsize
    text_align 0.0
    layout "tex" ## "subtitle" if nvl_thought.text_align != 0.0

style nvl_button is button
style nvl_button:
    xpos 450 ## mobile: 20
    xanchor 0.0
    variant "Small"
    xsize 1240

style nvl_button_text is button_text

## -- Input Screen -------------------------------------------------------------
## https://www.renpy.org/doc/html/screen_special.html#input
##
## This screen is used to display renpy.input. It must create an input
## displayable with id "input", to accept the various input parameters.

## prompt: The text prompt sent by renpy.input(), e.g., "What is your name?"
screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            #TODO this style just inherit from say_dialogue?
            xalign 0.0 ## say_dialogue.xalign
            xpos 268 ## say_dialogue.xpos
            xsize 744 ## say_dialogue.xsize
            ypos 50 ## say_dialogue.ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign 0.0 ## say_dialogue.xalign

style input:
    xalign 0.0 ## say_dialogue.xalign
    xmaximum 744 ## say_dialogue.xsize

## -- History Screen -----------------------------------------------------------
## https://www.renpy.org/doc/html/history.html
##
## This is a screen that displays the dialogue history to the player. It has
## access the dialogue history stored in _history_list.

init python:

    ## --- History List Length
    ## The number of entries of dialogue history Ren'Py keeps. If None, Ren'Py
    ## won't show the History screen.
    config.history_length = 250

    ## --- History List Callback
    ## List of functions called before adding a new object to _history_list. The
    ## callbacks are called with the new HistoryEntry object as the first
    ## argument, and can add new fields to that object.
    # config.history_callbacks.append()

    ## --- Allowed Tags
    ## Which text tags can appear on the history screen.
    gui.history_allow_tags = set()

screen history():
    tag menu

    on "show" action SetVariable("game_menu_screen", "history")
    on "replace" action SetVariable("game_menu_screen", "history")

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll="vpgrid", yinitial=1.0):

        style_prefix "history"

        for h in _history_list:
            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:
                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the character's name color, if set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")

style history_window is empty
style history_window:
    xfill True
    ysize 140 ## mobile: 190. Change scroll to "viewport" if you remove this

style history_name is gui_label
style history_name:
    xpos 155
    xanchor 1.0 ## history_name_text.text_align
    ypos 0
    xsize 155

style history_name_text is gui_label_text
style history_name_text:
    min_width 155
    text_align 1.0

style history_text is gui_text
style history_text:
    xpos 170
    ypos 2
    xanchor 0.0 ## history_text.text_align
    xsize 740 ## mobile: 690
    min_width 740 ## history_text.xsize
    text_align 0.0
    layout "tex" ## "subtitle" if history_text.text_align != 0.0

style history_label is gui_label
style history_label:
    xfill True

style history_label_text is gui_label_text
style history_label_text:
    xalign 0.5
