################################################################################
## GUI: Navigation Menus
################################################################################
## Main menu, game menu, and the stuff they rely on.

init python:

    ## --- (Transition) Game Menu to Main Menu
    # When returning to the main menu from the game menu
    config.game_main_transition = None

    ## --- (Transition) Main Menu to Game Menu
    ## Transition from Main Menu into Game Menu, such as when choosing "Load
    ## Game" or "Preferences" in a default Ren'Py setup.
    config.main_game_transition = None

## -- (Subscreen) Navigation ---------------------------------------------------
## Used to provide navigation between related screens.

## nav: Used to create different "lists" of menu buttons while still relying on
## navigation's structure and styles.
screen navigation(nav="pause"):
    vbox:
        style_prefix "navigation"
        spacing 4
        xpos 40
        yalign 0.3

        if nav == "pause":
            ## History
            if config.history_length and not main_menu:
                #TODO test disabling history screen
                textbutton _("History") action ShowMenu("history")

            ## File Select
            textbutton _("File Select") action ShowMenu("save")

            ## (Developer Only) Scene Select
            if config.developer:
                textbutton _("Scene Select") action ShowMenu("scenes")

            ## Settings (and various submenus)
            textbutton _("Settings") action ShowMenu("preferences")
            for s in gui.prefs_submenu_list:
                textbutton gui.prefs_submenu_names[s]:
                    action [ShowMenu("preferences"), SetVariable("_prefs_submenu", s)]
                    style "navigation_subbutton"
                    selected game_menu_screen == "preferences" and _prefs_submenu == s
        elif nav == "extras":
            textbutton _("Scene Select") action ShowMenu("scenes")
            textbutton _("Gallery") action ShowMenu("gallery")
            textbutton _("Music Room") action ShowMenu("musicroom")

    vbox: ## The "exit menu" buttons
        xpos 40
        yalign .9
        yoffset -30
        ## Close game menu
        textbutton _("Return"):
            action Return()

        ## Exit Replay
        if _in_replay:
            textbutton _("Exit Replay") action EndReplay(confirm=True)

        ## Exit to Main Menu/Dekstop
        if not main_menu:
            if renpy.variant("pc"):
                textbutton _("Quit") action Show("game_menu_quit")
            else:
                textbutton _("Main Menu") action LoadMainMenu()

style navigation_button is gui_button
style navigation_button:
    size_group "navigation"

style navigation_button_text is gui_button_text

style navigation_subbutton is navigation_button:
    xoffset 30

style navigation_subbutton_text is navigation_button_text:
    selected_color gui.selected_insensitive_color
    size 16

## -- Main Menu ----------------------------------------------------------------
## https://www.renpy.org/doc/html/screen_special.html#main-menu

init python:
    
    ## --- Main Menu Music
    config.main_menu_music = None
    
    config.main_menu_music_fadein = 0.0

    gui.main_menu_background = Solid("#252525")

screen main_menu():
    tag menu
    on "show" action Hide("loading")

    style_prefix "main_menu"

    add gui.main_menu_background

    frame:
        vbox:
            textbutton _("Start") action Start()
            textbutton _("Continue") action LoadMostRecent()
            textbutton _("Settings") action ShowMenu("preferences")
            textbutton _("Extras") action ShowMenu("scenes")
            if not renpy.mobile and not persistent.steam:
                textbutton _("Update"):
                    action updater.Update("", base=None, force=False, public_key=None, simulate=UPDATE_SIMULATE, add=[], restart=False, confirm=True)
            if renpy.variant("pc"):
                textbutton _("Quit") action Quit(confirm=not main_menu)

## -- (Subscreen) Game Menu ----------------------------------------------------
## This screen is a wrapper used to structure various submenus.

init python:

    ## --- (Transition) Opening Game Menu
    config.enter_transition = None
    config.enter_sound = None

    ## Layers that are cleared when entering the game menu.
    config.menu_clear_layers = []

    ## Music that plays on the game menu.
    config.game_menu_music = None

    ## ---! Game Menu Screen
    ## This is used instead of _game_menu_screen so the variable can be updated
    ## by screen language.
    game_menu_screen = "save"
    config.replay_scope["game_menu_screen"] = "preferences"

    ## --- ShowMenu Sensitivity
    ## A dictionary mapping the name of a ShowMenu screen argument to an
    ## expression used to evaluate whether the user can show that screen.
    config.show_menu_enable = {
        "save" : "(not main_menu) and (not _in_replay)",
        "load" : "(not _in_replay)",}

    ## --- (Transition) Between Game Menu Screens
    config.intra_transition = None

    ## --- (Transition) Closing Game Menu
    config.exit_transition = None
    config.exit_sound = None

    #---------------------------------------------------------------------------
    class InvokeGameMenu(Action):
        def __call__(self):
            return renpy.call_in_new_context("_game_menu", _game_menu_screen=game_menu_screen)

    config.game_menu_action = InvokeGameMenu()


## title: The title of the currently displayed submenu.
## scroll: Whether and how the content needs to scroll.
## yinitial: The initial placement of the scrollbar, if there is one.
screen game_menu(title=_("Paused"), nav="pause", scroll=None, yinitial=0.0):
    style_prefix "game_menu"

    #TODO?
    on "show" action Stop(blips_channel)

    if main_menu:
        add gui.main_menu_background
    else:
        add Solid("#222")

    frame:
        style "game_menu_outer_frame"

        hbox:
            frame: ## Navigation menu goes here.
                style "game_menu_navigation_frame"
            frame: ## Submenu content goes here
                style "game_menu_content_frame"

                if scroll == "viewport":
                    viewport:
                        draggable True
                        mousewheel True
                        pagekeys True
                        scrollbars "vertical"
                        side_yfill True
                        yinitial yinitial
                        vbox:
                            transclude
                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        draggable True
                        mousewheel True
                        pagekeys True
                        scrollbars "vertical"
                        side_yfill True
                        yinitial yinitial
                        transclude
                else:
                    transclude

    use navigation(nav)

    label title

    # if main_menu:
    #    key "game_menu" action ShowMenu("main_menu")

style game_menu_outer_frame is empty
style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120

style game_menu_navigation_frame is empty
style game_menu_navigation_frame:
    xsize 280 ## mobile: 340
    yfill True

style game_menu_content_frame is empty
style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10 ## mobile: 0

style game_menu_viewport is gui_viewport
style game_menu_viewport:
    xsize 920

style game_menu_scrollbar is gui_vscrollbar
style game_menu_vscrollbar:
    unscrollable "hide"

style game_menu_side is gui_side
style game_menu_side:
    spacing 10

style game_menu_label is gui_label
style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text is gui_label_text
style game_menu_label_text:
    size 50
    color gui.h1_color
    yalign 0.5
