################################################################################
## GUI: File Save/Load Screens
################################################################################

init python:

    ## --- File Pages
    ## Add the names of custom file pages here. By default, Ren'Py adds "quick"
    ## and "auto" to this list. The rest of the page names are just numbers.
    # config.file_page_names.append()

    ## --- Save Thumbnails
    config.thumbnail_height = 144
    config.thumbnail_width = 256

    ## --- Quicksaves
    config.quicksave_slots = 3

    ## --- Auto-saves
    config.has_autosave = True
    config.autosave_slots = 3
    config.autosave_frequency = 200
    config.autosave_on_choice = True

    ## Name of the slot to save to when quitting the game.
    _quit_slot = None

    ## --- (Callbacks) Save File JSON
    ## List of callback functions that are used to create the json object that
    ## is stored with each save.
    ##
    ## Each callback is called with a Python dictionary that will eventually be
    ## saved. Callbacks should modify that dictionary by adding JSON-compatible
    ## Python types, such as numbers, strings, lists, and dicts. The dictionary
    ## at the end of the last callback is then saved as part of the save slot.
    ##
    ## The dictionary passed to the callbacks may have already have keys
    ## beginning with an underscore _. These keys are used by Ren'Py, and should
    ## not be changed.
    config.save_json_callbacks = []

    ## Function called, without arguments, to get the extra_info value for an
    ## auto-save file.
    # config.auto_save_extra_info = None

    ## Whether to clear the screenshot used by saved games when creating a
    ## rollback checkpoint.
    config.auto_clear_screenshot = True

## title: The name of the file page, usually "Save" or "Load."
screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    on "show" action SetVariable("game_menu_screen", "save")
    on "replace" action SetVariable("game_menu_screen", "save")

    use game_menu(title):

        fixed:

            ## Give the input the "enter" key event before the buttons.
            order_reverse True

            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            grid 2 2:
                style_prefix "slot"

                spacing 10
                xalign 0.5
                yalign 0.5

                for i in range(4):
                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %I:%M %p"), empty=_("empty slot")).lstrip("0").replace(" 0", " "):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        ## To show custom save JSON data, use FileJson().

                        key "save_delete" action FileDelete(slot)

            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing 0

                textbutton _("<") alt _("Previous page") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                for page in range(1, 6):
                    textbutton "[page]" alt _("Page %d") % page action FilePage(page)

                textbutton _(">") alt _("Next page") action FilePageNext()

screen save():
    tag menu

    use file_slots(_("Save"))

screen load():
    tag menu

    use file_slots(_("Load"))

style page_label is gui_label
style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button is gui_button
style page_button:
    padding (10, 4)

style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button:
    padding (10, 10)
    xsize 276
    ysize 206

style slot_button_text is gui_button_text
style slot_button_text:
    color gui.idle_small_color
    selected_idle_color gui.selected_color
    selected_hover_color gui.hover_color
    size 14
    text_align 0.5
    xalign 0.5

style slot_time_text is slot_button_text
style slot_name_text is slot_button_text
