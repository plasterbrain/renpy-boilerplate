################################################################################
## GUI: Preferences Screen
################################################################################
## https://www.renpy.org/doc/html/screen_special.html#preferences
##
## The preferences UI comprises one main wrapper screen and various subpages,
## which list the actual user options.

#TODO toggle autosaving, maybe?
#TODO quit save slot option?
#TODO confirm before fast skipping

## -- Preferences Screen -------------------------------------------------------

init python:

    ## ---! Preference Submenus
    ## Used by `prefs()`
    gui.prefs_submenu_list = ["basic", "audio", "ctrl", "disp", "data"]
    ## Map of human-readable submenu names to their Python identifiers.
    gui.prefs_submenu_names = {
        "basic": _("General"),
        "ctrl": _("Controls"),
        "audio": _("Audio"),
        "disp": _("Graphics"),
        "data": _("Data")}

    gui.prefs_bar_width = gui._scale(350)

    #---------------------------------------------------------------------------
    ## The currently shown submenu.
    _prefs_submenu = gui.prefs_submenu_list[0]

    PREFS_SPACER = Null(height=15)

screen preferences():
    tag menu
    style_prefix "prefs"

    $ menu_name = "preferences"
    on "show" action SetVariable("game_menu_screen", menu_name)
    on "replace" action SetVariable("game_menu_screen", menu_name)

    ## Main content
    use game_menu(title=_("Preferences"), scroll="viewport"):
        vbox:
            text gui.prefs_submenu_names[_prefs_submenu] size 40
            $ renpy.use_screen("prefs_" + _prefs_submenu)

    ## Tooltip/hint area
    vbox:
        style_prefix "prefs_tooltips"
        $ tt = GetTooltip()
        $ tt = tt if tt else ""
        text tt color gui.tt2_color size 18
        if persistent._changed_renderer:
            hbox:
                spacing 8
                xalign 1.0
                text u"\u26A0"
                text _("Restart the game for changes to take effect.")

style prefs_tooltips_vbox:
    spacing 8
    xalign 1.0
    xoffset -25
    ypos .072

style prefs_tooltips_text:
    color gui.tt1_color
    size 14
    text_align 1.0
    xalign 1.0

style prefs_h2:
    color gui.h2_color

style prefs_label:
    xsize 250

style prefs_label_text:
    color gui.h3_color

style prefs_button:
    clear ## Remove default assigned styles
    padding (0,0)

style prefs_hbox:
    box_wrap True
    spacing 15

style prefs_vbox:
    spacing 10
    # xsize 450 ## mobile: 400

style prefs_slider:
    xsize gui.prefs_bar_width

style prefs_bar:
    xsize gui.prefs_bar_width

style prefs_submenu_hbox:
    spacing 20

style prefs_submenu_button_text:
    size 18

## -- Preferences: General -----------------------------------------------------
## Visual novel gameplay and other basic settings.

screen prefs_basic():
    style_prefix "prefs"

    $ translations = scan_translations()

    if len(translations) > 1:
        hbox:
            label _("Language")
            for lang in translations: ## (ex. _("English"), None)
                textbutton lang[0] action Language(lang[1])
    hbox:
        label _("Text Speed")
        bar value Preference("text speed"):
            tooltip _("Text display speed in characters per second.")
    hbox:
        label _("Text box opacity")
        bar value StyleValue("say_alpha", 255)

    add PREFS_SPACER

    text _("Skip mode") style "prefs_h2"
    hbox:
        label _("Text to skip")
        textbutton _("All text"):
            action Preference("skip", "all")
            tooltip _("Skip mode will skip everything.")
        textbutton _("Seen text only"):
            action Preference("skip", "seen")
            tooltip _("Skip mode will stop when you encounter unseen text.")
    hbox:
        label _("After choices")
        textbutton _("Keep skipping"):
            action Preference("after choices", "skip")
            tooltip _("Skip mode will continue after making choices.")
        textbutton _("Stop"):
            action Preference("after choices", "stop")
            tooltip _("Skip mode will stop when you reach a choice menu.")

    add PREFS_SPACER

    text _("Auto-forward mode") style "prefs_h2"
    hbox:
        label _("Speed")
        bar value Preference("auto-forward time"):
            tooltip _("How long AFM waits before advancing to the next line of dialogue.")
    hbox:
        label _("After clicks")
        textbutton _("Continue"):
            action Preference("auto-forward after click", "enable")
            tooltip _("Auto-forward mode will ignore clicks.")
        textbutton _("Stop"):
            action Preference("auto-forward after click", "disable")
            tooltip _("Auto-forward mode will stop when you click the screen.")
    if config.has_voice:
        hbox:
            label _("Voice clips")
            textbutton _("Wait for voice"):
                action Preference("wait for voice", "enable")
                tooltip _("Auto-forward mode will wait for voice clips to finish before proceeding.")
            textbutton _("Ignore voice"):
                action Preference("wait for voice", "disable")
                tooltip _("Auto-forward mode will ignore voice clips.")

    add PREFS_SPACER

    use increment(_("Self-voicing"), "self_voicing")

## -- Preferences: Audio -------------------------------------------------------
## Volume and other audio settings.

#TODO test with custom mixer
#TODO test sample sound/voice
screen prefs_audio():
    style_prefix "prefs"

    text "Volume" style "prefs_h2"
    for mixer in ["music", "sound", "voice"]:
        $ has_mixer = getattr(config, "has_" + mixer, "custom")
        $ mixer_name = "mixer " + mixer if has_mixer is "custom" else mixer
        $ special_name = "sfx" if mixer == "sound" else mixer
        $ sample_sound = config.__dict__.get("sample_" + mixer)
        if has_mixer or has_mixer is "custom":
            if _preferences.get_mute(special_name):
                $ mute_text = _("Unmute")
                $ mute_alt = _("Unmute %s") % mixer
            else:
                $ mute_text = _("Mute")
                $ mute_alt = _("Mute %s") % mixer

            hbox:
                label _("%s volume") % mixer.capitalize()
                textbutton "-":
                    action Increment(special_name, decrease=True)
                bar value Preference(special_name + " volume") style "prefs_bar"
                textbutton "+":
                    action Increment(special_name)
                textbutton mute_text:
                    alt mute_alt
                    action Preference(mixer_name + " mute", "toggle")
                if sample_sound: ## Add a button to play the test sound.
                    textbutton _("Test") action Play(mixer, sample_sound)
    if config.has_music or config.has_sound or config.has_voice:
        textbutton _("Mute All"):
            action Preference("all mute", "toggle")
            xalign 1.0
    if config.emphasize_audio_channels:
        hbox:
            label _("Emphasize Audio")
            textbutton _("On"):
                action Preference("emphasize audio", "enable")
                tooltip _("Adjust volume to emphasize important sounds.")
            textbutton _("Off"):
                action Preference("emphasize audio", "disable")
                tooltip _("Don't adjust channel volumes automatically.")

    hbox:
        label _("Subtitles")
        textbutton _("On"):
            alt _("Enable subtitles")
            action SetField(persistent, "prefs_subtitles", True)
        textbutton _("Off"):
            alt _("Turn off subtitles")
            action SetField(persistent, "prefs_subtitles", False)
    if config.has_voice:
        hbox:
            label _("Voice sustain")
            textbutton _("On"):
                action Preference("voice sustain", "enable")
                tooltip _("Voice clips will play for their full duration even if you advance the text.")
            textbutton _("Off"):
                action Preference("voice sustain", "disable")
                tooltip _("Voice clips will be cut off if you advance the text early.")

## -- Preferences: Display -----------------------------------------------------
## Graphics, performance, and font settings.

screen prefs_disp():
    style_prefix "prefs"

    text _("Text Settings") style "prefs_h2"
    if increments.font_transform_list:
        use increment(_("Font family"), "font_transform")
    hbox:
        label _("Text Size")
        hbox:
            bar value Preference("font size")
            textbutton _("Reset"):
                alt _("Reset font size")
                action Preference("font size", 1.0)
    hbox:
        label _("Line Spacing")
        hbox:
            bar value Preference("font line spacing")
            textbutton _("Reset"):
                alt _("Reset font line spacing")
                action Preference("font line spacing", 1.0)

    add PREFS_SPACER

    text _("Display") style "prefs_h2"
    ## Window/Fullscreen
    if renpy.variant("pc") or renpy.variant("web"):
        hbox:
            label _("Window Mode")
            textbutton _("Windowed"):
                action Preference("display", "any window")
            textbutton _("Fullscreen"):
                action Preference("display", "fullscreen")
    ## Screen Resolution
    if renpy.variant("pc") and increments.prefs_resolution_list:
        use increment(_("Resolution"), "prefs_resolution", store=persistent, action=SetResolution())

    ## Graphics Renderer
    use increment(_("Renderer"), "renderer", action=SetRenderer())

    add PREFS_SPACER

    text _("Performance") style "prefs_h2"
    hbox:
        label _("Transitions")
        textbutton _("On"):
            action Preference("transitions", "all")
        textbutton _("Off"):
            action Preference("transitions", "none")
    hbox:
        label _("Videos")
        textbutton _("On"):
            action Preference("video sprites", "show")
        textbutton _("Off"):
            action Preference("video sprites", "hide")
            tooltip _("Replace videos with still images.")
    use increment(_("Framerate"), "gl_framerate")
    use increment(_("Refresh rate"), "gl_powersave")
    use increment(_("Handle issues"), "gl_tearing")

## -- Preferences: Controls ----------------------------------------------------
## Control bindings, mouse settings, and gamepad calibration.

screen prefs_ctrl():
    style_prefix "prefs"

    $ actn_list = [a for a in _keymap_action_list if a.shown]
    $ actn_list_gp = [a for a in actn_list if a not in [km_f_left, km_f_right, km_f_up, km_f_down]]

    if renpy.variant("pc"):
        text _("Keyboard") style "prefs_h2"
        for actn in actn_list:
            if actn.has_slot or actn.frozen_types["kb"]:
                hbox:
                    label actn.nice_name
                    if actn.has_slot:
                        use keyboard_input(actn)
                    for k in actn.frozen_types["kb"]:
                        textbutton persistent._keysym_names.get(k, get_keyname_from_keycode(k))

        add PREFS_SPACER

        text _("Mouse") style "prefs_h2"
        if config.enable_rollback_side:
            hbox:
                label _("Rollback Side")
                textbutton _("Left") action Preference("rollback side", "left")
                textbutton _("Right") action Preference("rollback side", "right")
                textbutton _("Off") action Preference("rollback side", "disable")
        hbox:
            label _("Auto Mouse")
            textbutton "On":
                action Preference("automatic move", "enable")
                tooltip _("The mouse will move towards selected buttons.")
            textbutton "Off":
                action Preference("automatic move", "disable")
                tooltip _("The mouse will not be automatically moved.")
        for actn in actn_list:
            if actn.frozen_types["mouse"]:
                hbox:
                    label actn.nice_name
                    for k in actn.frozen_types["mouse"]:
                        ## There probably won't be more than one, but ¯\_(ツ)_/¯
                        text persistent._keysym_names.get(k, k)
    elif renpy.variant("android") or renpy.variant("ios"):
        if config.enable_rollback_side:
            hbox:
                label _("Rollback Side")
                textbutton _("Left"):
                    action Preference("rollback side", "left")
                textbutton _("Right"):
                    action Preference("rollback side", "right")
                textbutton _("Off"):
                    action Preference("rollback side", "disable")
        for actn in actn_list:
            if actn.frozen_types["mobile"] or actn.gesture:
                hbox:
                    label actn.nice_name
                    for k in actn.frozen_types["mobile"]:
                        text persistent._keysym_names.get("mobile_" + k, k)
                    if actn.gesture:
                        #TODO test gestures showing up
                        text actn.gesture.upper().replace("_", " ")

    add PREFS_SPACER

    hbox:
        text _("Gamepad") style "prefs_h2"
        textbutton _("On") action SetField(_preferences, "pad_enabled", True)
        textbutton _("Off") action SetField(_preferences, "pad_enabled", False)
        textbutton _("Calibrate") action GamepadCalibrate()
    for actn in actn_list_gp:
        if actn.frozen_types["gp"]:
            hbox:
                label actn.nice_name
                for k in actn.frozen_types["gp"]:
                    text persistent._keysym_names.get(k, k)

# screen joystick_preferences_screen():
# screen _gamepad_select(joysticks):

## -- Preferences: Data --------------------------------------------------------
## Privacy, saving, startup and other data options

screen prefs_data():
    style_prefix "prefs"

    text _("Completed: %s") % get_completion_rate()
    textbutton _("View Screenshots") action OpenFolder(screenshot_folder)

    add PREFS_SPACER

    label _("Startup Settings")
    if persistent.itch and not persistent.itch_app:
        hbox:
            label _("Check for new version") style_suffix "long"
            textbutton _("On"):
                action SetField(persistent, "prefs_itch_update", True)
            textbutton _("Off"):
                action SetField(persistent, "prefs_itch_update", False)
    hbox:
        label _("Performance check") style_suffix "long"
        textbutton _("On"):
            action SetField(_preferences, "performance_test", True)
        textbutton _("Off"):
            action SetField(_preferences, "performance_test", False)

    add PREFS_SPACER

    label _("Danger Zone")
    textbutton _("Delete save data") action DeleteData(confirm="twice")
    textbutton _("Reset Preferences") action DeleteData("prefs")

style prefs_label_long is prefs_label:
    xsize 400

## -- (Subscreen) Incrementer --------------------------------------------------
## A quick way to include list-based increment options.

screen increment(title, variable, store=_preferences, action=None):
    $ incr_tt = increment_tt(variable, store=store)
    hbox:
        label title alt ""
        textbutton gui.arrow_left:
            action IncrementList(variable, title=title, decrease=True, store=store, tt=incr_tt, action=action)
        textbutton increment_name(variable, store=store):
            style "incr_display"
            tooltip incr_tt
            action NullAction()
        textbutton gui.arrow_right:
            action IncrementList(variable, title=title, store=store, tt=incr_tt, action=action)

style incr_display is prefs_button

style incr_display_text:
    font gui.glyph_font
    text_align 0.5
    min_width 180

## -- (Subscreen) Checkbox -----------------------------------------------------

screen checkbox(store, field, true_value=True, false_value=False, label_text="", alt_text=""):
    style_prefix "checkbox"

    $ checked = u"\u2611" if getattr(store, field) == true_value else u"\u2610"

    hbox:
        textbutton checked + " " + label_text:
            action ToggleField(store, field, true_value=true_value, false_value=false_value)
            alt alt_text

style checkbox_button:
    padding (0, 0)

style checkbox_button_text:
    font gui.glyph_font

## -- (Subscreen) Keyboard Input -----------------------------------------------
## A screen element which can be included in options screens. It shows a text
## button that, when pressed, will change to text that reads "Press a key" and
## will enable the KeyInput() action.

init python:

    style.keymap_button["kb"].background = Solid("#ababab")

    #---------------------------------------------------------------------------

    ## The current action being remapped.
    _keymap_current = None

## act: The KeymapAction() object this is setting a key for.
screen keyboard_input(actn):
    style_prefix "keymap"

    python:
        k_name = persistent._keysym_names.get(actn.slot_key, get_keyname_from_keycode(actn.slot_key))
        k_style = "kb"
        if k_name == KEYMAP_NONE_NAME:
            k_style = "None"

    if actn == _keymap_current:
        text _("Press a key")
        add KeyInput(actn)
    else:
        textbutton k_name:
            action SetVariable("_keymap_current", actn)
            style style.keymap_button[k_style]

    key "K_ESCAPE" action SetVariable("_keymap_current", None)

style keymap_button_text:
    color "#000"
    size 14
