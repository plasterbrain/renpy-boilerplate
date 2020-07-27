################################################################################
## Module: Keymap
################################################################################
## Functions and classes to handle keymap bindings, remapping keys in-game, and
## dynamically generating human-readable names for key combinations.
#TODO Gamepad rebinding? I don't know how KeyInput would handle that and more importantly whether Ren'Py has a cache clearing function like with keymap, or if it just works for both? idk

init 1 python:

    ## ---! (Keymap) "Enter" Action Group
    ## Group of keymap actions which all traditionally use the enter key.

    km_dismiss = KeymapAction("dismiss",
        nice_name=_("Advance the text"),
        slot_group="enter")
    km_dismiss.add_frozen("mouseup_1")
    km_dismiss.add_frozen("K_SPACE")
    km_btn_select = KeymapAction("button_select",
        nice_name=_("Select"),
        slot_group="enter", shown=False)
    km_btn_select.add_frozen("mouseup_1")
    km_bar_activate = KeymapAction("bar_activate",
        nice_name=_("Edit bar value"),
        slot_group="enter", shown=False)
    km_bar_activate.add_frozen("mousedown_1")
    km_bar_deactivate = KeymapAction("bar_deactivate",
        nice_name=_("Finish editing bar value"),
        slot_group="enter", shown=False)
    km_bar_deactivate.add_frozen("mouseup_1")

    ## "Enter" group keys
    km_dismiss.add_frozen("K_RETURN", for_group=True)
    km_dismiss.add_frozen("pad_a_press", for_group=True)
    km_dismiss.add_frozen("pad_righttrigger_pos", for_group=True)
    km_dismiss.add_slot("K_z")

    ## ---! (Keymap) Button Alternate Select
    km_btn_alt_select = KeymapAction("button_alternate",
        nice_name=_("Alt Select"), shown=False)
    km_btn_alt_select.add_frozen("mouseup_3")
    km_btn_alt_select.add_frozen("pad_b_press")

    ## --- (Keymap) Input Controls
    #TODO test if input consumes these events first if they're bound to something else!

    config.keymap["input_enter"] = ["K_RETURN"]
    config.keymap["input_backspace"] = ["K_BACKSPACE", "repeat_K_BACKSPACE"]
    config.keymap["input_delete"] = ["K_DELETE", "repeat_K_DELETE"]
    config.keymap["input_home"] = ["K_HOME"]
    config.keymap["input_end"] = ["K_END"]
    config.keymap["input_copy"] = ["ctrl_K_INSERT", "ctrl_K_c"]
    config.keymap["input_paste"] = ["shift_K_INSERT", "ctrl_K_v"]

    ## ---! (Keymap) VN Controls

    km_afm = KeymapAction("toggle_afm", nice_name=_("Auto-forward mode"))
    km_afm.add_slot()

    km_skip = KeymapAction("toggle_skip", nice_name=_("Skip"))
    km_skip.add_slot("K_TAB")

    km_skip_hold = KeymapAction("skip",
        nice_name=_("Hold to skip"), shown=False)
    km_skip_hold.add_slot("K_LCTRL")

    km_rollback = KeymapAction("rollback",
        nice_name=_("Rollback"))
    km_rollback.add_frozen("mousedown_4")
    km_rollback.add_frozen("K_AC_BACK")
    km_rollback.add_frozen("pad_leftshoulder_press")
    km_rollback.add_frozen("pad_lefttrigger_pos")
    km_rollback.add_frozen("pad_back_press")
    km_rollback.add_slot("K_PAGEUP", use_repeat=True)

    km_rollforward = KeymapAction("rollforward",
        nice_name=_("Rollforward"), shown=False)
    km_rollforward.add_frozen("mousedown_5")
    km_rollforward.add_frozen("pad_rightshoulder_press")
    km_rollforward.add_slot("K_PAGEDOWN", use_repeat=True)

    ## --- (Keymap) Extraneous VN Controls

    ## Dismiss `renpy.pause(hard=True)` events.
    config.keymap["dismiss_hard_pause"] = []
    ## (6.99.12) Dismiss the current dialogue even if that window isn't focused.
    config.keymap["dismiss_unfocused"] = []
    ## ! Only works outside developer mode if `config.fast_skipping` = True.
    #TODO remove fast skip alt action from quick menu
    config.keymap["fast_skip"] = [] # [">"]
    config.keymap["stop_skipping"] = []

    ## ---! (Keymap) Screen Controls
    km_hide = KeymapAction("hide_windows", nice_name=_("Hide windows"))
    km_hide.add_frozen("mouseup_2")
    km_hide.add_frozen("pad_y_press")
    km_hide.add_slot("K_h")

    #TODO does game menu override renpy.input
    km_game_menu = KeymapAction("game_menu", nice_name=_("Pause"))
    km_game_menu.add_frozen("mouseup_3")
    km_game_menu.add_frozen("pad_guide_press")
    km_game_menu.add_frozen("pad_start_press")
    km_game_menu.add_frozen("K_ESCAPE")
    km_game_menu.add_slot()

    km_help = KeymapAction("help", nice_name=_("Help"))
    km_help.add_slot("K_F1")

    config.keymap["progress_screen"] = None # ["K_F2"]
    config.keymap["accessibility"] = None # ["K_a"]
    config.keymap["choose_renderer"] = None # ["K_g", "alt_shift_K_g"]

    km_save_delete = KeymapAction("save_delete",
        nice_name=_("Delete save file"))
    km_save_delete.add_slot("K_DELETE")

    ## ---! (Keymap) Program Controls

    km_iconify = KeymapAction("iconify", nice_name=_("Minimize window"))
    km_iconify.add_slot()

    km_quit = KeymapAction("quit", nice_name=_("Quit"))
    km_quit.add_slot()

    km_fullscreen = KeymapAction("toggle_fullscreen",
        nice_name=_("Fullscreen"))
    km_fullscreen.add_slot("f")
    km_fullscreen.add_frozen("K_F11")
    km_fullscreen.add_frozen("alt_K_RETURN")

    km_screenshot = KeymapAction("screenshot",
        nice_name=_("Take a screenshot"))
    km_screenshot.add_slot("K_F12")

    km_sv_tts = KeymapAction("self_voicing",
        nice_name=_("Text-to-speech"), shown=False)
    km_sv_tts.add_slot("shift_K_v")

    km_sv_clipboard = KeymapAction("clipboard_voicing",
        nice_name=_("Text to clipboard"), shown=False)
    km_sv_clipboard.add_slot("shift_K_c")

    config.keymap["debug_voicing"] = [] ## End users don't need this lol

    ## ---! (Keymap) "Left" Action Group

    km_f_left = KeymapAction("focus_left",
        nice_name=_("Left"),
        slot_group="left")
    km_in_left = KeymapAction("input_left",
        nice_name=_("Input caret left"),
        slot_group="left", shown=False)
    km_vp_left = KeymapAction("viewport_leftarrow",
        nice_name=_("Scroll left"),
        slot_group="left", shown=False)
    km_bar_left = KeymapAction("bar_left",
        nice_name=_("Decrease bar"),
        slot_group="left", shown=False)

    km_f_left.add_frozen("pad_dpleft_press", for_group=True)
    km_f_left.add_frozen("pad_leftx_neg", for_group=True)
    km_f_left.add_frozen("pad_rightx_neg", for_group=True)
    km_f_left.add_slot("K_LEFT", use_repeat=True)

    ## ---! (Keymap) "Right" Action Group

    km_f_right = KeymapAction("focus_right",
        nice_name=_("Right"),
        slot_group="right")
    km_in_right = KeymapAction("input_right",
        nice_name=_("Input caret right"),
        slot_group="right", shown=False)
    km_vp_right = KeymapAction("viewport_rightarrow",
        nice_name=_("Scroll right"),
        slot_group="right", shown=False)
    km_bar_right = KeymapAction("bar_right",
        nice_name=_("Increase bar"),
        slot_group="right", shown=False)

    km_f_right.add_frozen("pad_dpright_press", for_group=True)
    km_f_right.add_frozen("pad_leftx_pos", for_group=True)
    km_f_right.add_frozen("pad_rightx_pos", for_group=True)
    km_f_right.add_slot("K_RIGHT", use_repeat=True)

    ## ---! (Keymap) "Up" Action Group

    km_f_up = KeymapAction("focus_up",
        nice_name=_("Up"),
        slot_group="up")
    km_in_up = KeymapAction("input_up",
        nice_name=_("Input caret up"),
        slot_group="up", shown=False)
    km_vp_up = KeymapAction("viewport_uparrow",
        nice_name=_("Scroll up"),
        slot_group="up", shown=False)
    km_bar_up = KeymapAction("bar_up",
        nice_name=_("Increase bar"),
        slot_group="up", shown=False)

    km_f_up.add_frozen("pad_dpup_press", for_group=True)
    km_f_up.add_frozen("pad_lefty_neg", for_group=True)
    km_f_up.add_frozen("pad_righty_neg", for_group=True)
    km_f_up.add_slot("K_UP", use_repeat=True)

    ## ---! (Keymap) "Down" Action Grodown

    km_f_down = KeymapAction("focus_down",
        nice_name=_("Down"),
        slot_group="down")
    km_in_down = KeymapAction("input_down",
        nice_name=_("Input caret down"),
        slot_group="down", shown=False)
    km_vp_down = KeymapAction("viewport_downarrow",
        nice_name=_("Scroll down"),
        slot_group="down", shown=False)
    km_bar_down = KeymapAction("bar_down",
        nice_name=_("Increase bar"),
        slot_group="down", shown=False)

    km_f_down.add_frozen("pad_dpdown_press", for_group=True)
    km_f_down.add_frozen("pad_lefty_pos", for_group=True)
    km_f_down.add_frozen("pad_righty_pos", for_group=True)
    km_f_down.add_slot("K_DOWN", use_repeat=True)

    ## --- (Keymap) Mouse-Only Controls
    #TODO are mousedowns 4/5 like swipes on mobile or what...?

    config.keymap["viewport_wheelup"] = ["mousedown_4"]
    config.keymap["viewport_wheeldown"] = ["mousedown_5"]
    config.keymap["viewport_drag_start"] = ["mousedown_1"]
    config.keymap["viewport_drag_end"] = ["mouseup_1"]
    config.keymap["button_ignore"] = ["mousedown_1"]
    config.keymap["button_alternate_ignore"] = ["mousedown_3"]

    ## --- (Mobile) Gestures
    ## https://www.renpy.org/doc/html/gesture.html
    ## Dictionary mapping gestures to events they activate, used if
    ## `config.dispatch_gesture` is None.
    config.gestures = {}

## -- Keymap Rebinding ---------------------------------------------------------

init python:

    #TODO test this offset
    ## Init offset -1: Lets us create KeymapActions in other files reliably

    import pygame_sdl2 as pygame

    ## Action names mapped to their currently "slotted" key, used to adjust the
    ## keymap to match user preferences the next time the game is run.
    if not persistent._keymap_slotted:
        persistent._keymap_slotted = {}

    ## Event strings created by `renpy.display.behavior.compile_event()` for
    ## any bindable keys that have been used at least once, mapped to their
    ## current action. This is used to check if a desired key is already taken.
    if not persistent._keymap_reverse:
        persistent._keymap_reverse = {}

    ## Keys that are "frozen" and can't be used for rebinding or by slots.
    _keymap_reserved = []

    ## List of all the KeymapAction objects available.
    _keymap_action_list = []

    ## Map of KeymapAction name attributes to their corresponding object 'cause
    ## Ren'Py doesn't like saving objects themselves to persistent, tee hee!
    _keymap_action_map = {}

    ## Map of slot group names to a list of actions whose "slots" they update.
    _keymap_group_map = {}

    ## Internally used reverse lookup mapping Pygame key integers to keysyms.
    KEYMAP_INT_MAP = {const_int: const_str for const_str, const_int in pygame.__dict__.iteritems() if const_str.startswith("K_")}

    def get_keysym_from_keycode(keysym):
        """
        Attempts to convert an "easy" Ren'Py keycode (like "S") into a more
        Pygame-friendly equivalent (like "shift_K_s").

        Parameters
        ----------
        keysym : str
            The Ren'Py-style keysym to convert.

        Returns
        -------
        str
            A keysym string using Ren'Py's string modifiers (e.g. "shift_"), if
            necessary, and key constants instead of unicode characters.
        """
        keycode = keysym.split("_")
        if len(keycode) != 1:
            ## Key is probably already formatted with Pygame keysym.
            return keysym

        keycode = keycode[0]
        if len(keycode) != 1:
            raise Exception("Invalid key specifier %s. See the `config.keymap` documentation for examples of how to format key specifiers." % keysym)

        shift = "shift_"
        try:
            ## Get an unshifted version of this key
            keyint = ord(KEYMAP_SHIFTED_MAP[keycode])
        except KeyError:
            if keycode.isalpha() and keycode.isupper():
                ## Same but for a letter
                keyint = ord(keycode.lower())
            else:
                keyint = ord(keycode)
                shift = ""
        return shift + KEYMAP_INT_MAP[keyint]

    class KeymapAction():
        """
        This class creates an interpretive layer between our desired bindings
        and the final `config.keymap` configuration.

        Attributes
        ----------
        has_slot : bool
            Whether `add_slot` has been called for this action. You can use this
            attribute to filter `_keymap_actions` to get only bindable actions.
        slot_repeat : bool
            Whether the bindable key for this action should be added twice, once
            as itself and once with a "repeat_" modifier. This is used if the
            action should be triggered by holding a key.
        slot_key : str or None
            The keysym currently assigned to this action's bindable slot. It's
            passed to `config.keymap`.
        frozen_keys : list
            The list of keysyms assigned to this action that cannot be remapped
            anywhere else.
        frozen_types : dict
            A dictionary mapping the various input categories ("mouse",
            "mobile", etc.) to a list of frozen keys for this action. This can
            be used by screens to list e.g. only the mouse controls.
        """

        def __init__(self, name, nice_name=None, shown=True, slot_group=None):
            """
            Initializes the class. It's really great.

            Parameters
            ----------
            name : str
                Name of the `config.keymap` action this maps to.
            nice_name : str, optional
                Human-readable name to show on keyboard settings screens.
            shown : bool, optional
                Set and refer to this attribute to selectively hide redundant
                actions from screens. This is good for actions that implicitly
                take values from a shown member of their group.
            slot_group : str, optional
                The name of a group this action belongs to. All the actions in
                this group share a single bindable key for their slots, though
                they may have unique frozen keys.
            """
            self.name = name
            self.nice_name = nice_name
            if not self.nice_name:
                self.nice_name = self.name.capitalize().replace("_", " ")

            self.shown = shown

            self.slot_group = slot_group
            if self.slot_group:
                global _keymap_group_map
                try:
                    _keymap_group_map[self.slot_group].add(self)
                except:
                    _keymap_group_map[self.slot_group] = set([self])

            self.has_slot = False
            self.slot_repeat = False
            self.slot_key = None

            self.frozen_keys = []
            self.frozen_types = {"mouse":[],"kb":[],"gp":[],"joy":[],"mobile":[]}

            self.gesture = None

            global _keymap_action_list
            global _keymap_action_map
            _keymap_action_list.append(self)
            _keymap_action_map[self.name] = self

        def __eq__(self, other):
            if not isinstance(other, KeymapAction):
                return False

            return self.name is other.name

        def add_slot(self, keysym=None, event=None, use_repeat=False, group_leader=True):
            """
            Adds or updates a slot. An action can have up to one bindable slot.
            Only keyboard input actions can be used in a remappable slot.

            Parameters
            ----------
            keysym : str or None
                The keysym to set in the rebindable slot, or None to give this
                action a rebindable slot without setting a default key.
            event : str, optional
                The Ren'Py compiled event string for this object. `bind_key()`
                generates one as it goes so we pass it here to save time.
            use_repeat : bool, optional
                Whether this keysym should be added alongside a copy of itself
                with the "repeat" modifier -- that is, whether holding down this
                key will also trigger this action.
            group_leader : bool, optional
                Recursive loop buster!
            """
            if keysym:
                if any(["keyup_" in keysym,"mouse" in keysym,"_AC_" in keysym]):
                    raise Exception("You can't map a mouse, Android, or keyup event to a rebindable slot.")
                elif keysym.startswith("pad_"):
                    raise Exception("I might add a gamepad slot action later, but for now, GET OUT!!! *gordon ramsay throws fish*")

            self.has_slot = True

            ## Save these values if True, but don't overwrite with default False
            if use_repeat:
                self.slot_repeat = True

            if renpy.is_init_phase():
                saved_keysym = persistent._keymap_slotted.get(self.name)
                if saved_keysym:
                    keysym = saved_keysym
                elif keysym:
                    ## Possibly fix dev-defined default value
                    keysym = get_keysym_from_keycode(keysym)

            if keysym: ## Turn keysym into a more consistent event string
                if not event:
                    event = renpy.display.behavior.compile_event(keysym, True)

            ## Check if this key is used by a frozen slot somewhere.
            if event in _keymap_reserved:
                if config.developer:
                    raise Exception("%s is being used by another action as a non-rebindable key." % keysym)
                else:
                    ## Just unset this key I guesss!
                    keysym = None

            ## Remove any outdated reverse keymap entries (ex. if dev changed
            ## default key without clearing persistent data).
            fixed_reverse = {k: v for k, v in persistent._keymap_reverse.iteritems()}
            for ev, action in persistent._keymap_reverse.iteritems():
                if action == self.name:
                    if ev != event:
                        fixed_reverse.pop(ev)
            persistent._keymap_reverse = fixed_reverse

            old_slot_key = self.slot_key
            self.slot_key = keysym

            if self.slot_group and group_leader:
                if not _keymap_group_map[self.slot_group]:
                    print("Heads up: {0} might not get added correctly to the {0}")
                ## Set this key for all actions in a slot group, if requested.
                for action in _keymap_group_map[self.slot_group]:
                    if action.slot_key != keysym:
                        action.add_slot(keysym, event, use_repeat, False)

            if keysym and event != "(False)":
                persistent._keymap_reverse[event] = self.name
            ## Update dict with this action's bindable key.
            persistent._keymap_slotted[self.name] = self.slot_key
            self.save_to_config()

            ## Used to swap out keys during binding.
            return old_slot_key

        def add_frozen(self, keysym, event=None, for_group=False):
            """
            Adds a non-rebindable keysym. Should only be called on init.

            Parameters
            ----------
            keysym : str
                The non-rebindable keysym to add.
            event : obj, optional
                The Pygame event object for this keysym. If none is provided, it
                will be calculated from `keysym` on the fly.
            fo_group : bool, optional
                Whether to apply this frozen key to all members of the action's
                slot group, default False.
            """
            if not event:
                event = renpy.display.behavior.compile_event(keysym, True)

            self.add_key_to_groups(keysym)

            if not event in _keymap_reserved:
                global _keymap_reserved
                _keymap_reserved.append(event)

            self.frozen_keys.append(keysym)

            if for_group and self.slot_group:
                for action in _keymap_group_map.get(self.slot_group, []):
                    if keysym not in action.frozen_keys:
                        action.add_frozen(keysym, event)

            self.save_to_config()

        def add_key_to_groups(self, keysym, kind="frozen"):
            """
            Adds the key to the appropriate group lists in `self.frozen_types`.

            Parameters
            ----------
            kind : str
                Whether we're adding to the frozen or slot key types dict. This
                might be used in the future to set up a similar list for slot
                keys, but right now slot keys are only for the keyboard.
            """
            key_types = self.frozen_types
            if "mouse" in keysym:
                if keysym == "mouseup_1":
                    ## Add left click to mobile, since it's the same as a tap
                    if keysym not in key_types["mobile"]:
                        key_types["mobile"].append(keysym)
                ## Mouse events
                if keysym not in key_types["mouse"]:
                    key_types["mouse"].append(keysym)
            elif "_AC_" in keysym:
                ## Weird Android buttons
                if keysym not in key_types["mobile"]:
                    key_types["mobile"].append(keysym)
            elif keysym.startswith("pad_"):
                if keysym not in key_types["gp"]:
                    key_types["gp"].append(keysym)
            elif keysym not in key_types["kb"]:
                key_types["kb"].append(keysym)

        def add_gesture(self, gesture):
            """
            Maps the requested gesture in `config.gestures` to the name of this
            action, and sets `self.gesture`.

            Parameters
            ----------
            gesture : str
                A mobile gesture string representing a series of cardinal
                directions, e.g., "n_s_w_e_w_e".
            """
            gesture = gesture.lower()
            lint_gesture = gesture.split("_")
            for part in lint_gesture:
                if part not in ["n", "ne", "e", "se", "s", "sw", "w", "nw"]:
                    raise Exception("Invalid gesture specifier %s" % s)

            self.gesture = gesture
            config.gestures[self.gesture] = self.name

        def save_to_config(self):
            """
            Saves all the stored keys to `config.keymap` and the persistent
            keymap preference variable. This does not clear keymap cache or
            restart the interaction by itself.
            """
            gp_keys = [k for k in self.frozen_keys if k.startswith("pad_")]
            non_gp_keys = [k for k in self.frozen_keys if not k.startswith("pad_")]

            if self.slot_key:
                if self.slot_repeat:
                    slot_keys = [self.slot_key, "repeat_" + self.slot_key]
                    non_gp_keys += slot_keys
                else:
                    non_gp_keys.append(self.slot_key)
            non_gp_keys = list(set(non_gp_keys))
            config.keymap[self.name] = non_gp_keys

            for key in gp_keys:
                if key not in config.pad_bindings:
                    raise Exception("Invalid gamepad specifier %s" % key)
                config.pad_bindings[key].append(self.name)
                config.pad_bindings[key] = list(set(config.pad_bindings[key]))
            #TODO maybe gamepad slot function here.

            #TODO unset when ready to test!
            #persistent.prefs_keymap[self.name] = all_keys

    def bind_key(keysym, new_action, event=None):
        """
        Associates the requested keycode with the requested setting. If the
        requested keycode is being used for another setting, that setting will
        inherit the keycode being replaced here.

        Parameters
        ----------
        keysym : str
            The keysym to bind to an action slot.
        new_action : object
            The new action to bind this key to, a KeymapAction instance.
        event : object
            The Pygame event object for this keysym.
        """
        #TODO reset prefs function needs to clear keymap cache

        if not event:
            event = renpy.display.behavior.compile_event(keysym, True)

        ## Check if our desired key is already mapped to an action.
        old_action = persistent._keymap_reverse.get(event)

        ## Check if this key belongs to `new_action` already!
        if old_action == new_action.name:
            return

        ## Cough up the discarded key if we're replacing an old mapping
        old_key = new_action.add_slot(keysym, event)
        if old_action:
            ## Give the discarded key to the action we just stole a key from
            old_action = _keymap_action_map[old_action]
            old_action.add_slot(old_key)
        else:
            ## Remove the discarded key
            old_event = renpy.display.behavior.compile_event(old_key, True)
            persistent._keymap_reverse[old_event] = None

        renpy.clear_keymap_cache()
        renpy.restart_interaction()

    ## Pygame keysym to Ren'Py keycode prefix for all allowed modifier keys.
    KEYMAP_MODS = {"K_RSHIFT": "shift_", "K_LSHIFT": "shift_",
        "K_RCTRL": "ctrl_", "K_LCTRL": "ctrl_",
        "K_RALT": "alt_", "K_LALT": "alt_",
        "K_LGUI": "meta_", "K_RGUI": "meta_",}

    ## Used to "catch" modifier keys.
    _stored_mods = set()

    ## Displayable class for catching key input.
    class KeyInput(renpy.Displayable):
        def __init__(self, action):
            """
            Parameters
            ----------
            action : object
                The `KeymapAction()` object to bind this key to.
            """
            renpy.Displayable.__init__(self)

            self.action = action
            self.ignorelist = _keymap_reserved

        def render(self, width, height, st, at):
            return renpy.Render(0, 0)

        def event(self, ev, x, y, st):
            """
            Parameters
            ----------
            ev : obj
                `Pygame.event.Event()` object, a unit of user input.
            """
            ## Only bind keyboard events (not gamepad or mouse).
            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.end()
            if ev.type not in [pygame.KEYDOWN, pygame.KEYUP]:
                self.end(False)

            try:
                #TODO ask Nekkowe to test. hopefully this fixes keyerror he got
                keysym = KEYMAP_INT_MAP[ev.key]
            except KeyError as e:
                ## Some international keys don't exist in the dictionary.
                print(repr(e))
                self.end()

            global _stored_mods
            final_keysym = ""
            if ev.type == pygame.KEYUP:
                if _stored_mods:
                    for modkey in _stored_mods:
                        if modkey != keysym:
                            final_keysym += KEYMAP_MODS.get(modkey, "")
                    _stored_mods = set()
                final_keysym += keysym
            elif keysym in KEYMAP_MODS:
                _stored_mods.add(keysym)

            if not final_keysym:
                self.end(False)

            event = renpy.display.behavior.compile_event(final_keysym, True)

            ## Don't rebind reserved keys.
            if event in self.ignorelist:
                self.end(False)

            bind_key(final_keysym, self.action, event)
            self.end()

        def end(self, final=True):
            """
            Parameters
            ----------
            final : bool
                Whether we're actually ending the input (True, default) or just
                looping around to catch multiple simultaneous key presses.
            """
            renpy.restart_interaction()

            if final:
                global _keymap_current
                _keymap_current = None

            raise renpy.IgnoreEvent()

## -- Keymap Names -------------------------------------------------------------
## Functions used to get human readable names for keyboard/mouse input.

init python:

    ## ---! Keysym Names
    ## The options screen looks for a name in this list first. Any keysym names
    ## generated with `get_keyname_from_keycode()` are added to it.
    if not persistent._keysym_names:
        persistent._keysym_names = {
            ## Mouse Event Names
            "mouseup_1": _("Left click"),
            "mouseup_2": _("Middle click"),
            "mouseup_3": _("Right click"),
            "mousedown_1": _("Left click"),
            "mousedown_2": _("Middle click"),
            "mousedown_3": _("Right click"),
            "mousedown_4": _("Mousewheel"),
            "mousedown_5": _("Mousewheel"),
            ## Gamepad Event Names
            "pad_leftshoulder_press": _("L1"),
            "pad_lefttrigger_pos": _("L2"),
            "pad_rightshoulder_press": _("R1"),
            "pad_righttrigger_pos": _("R2"),
            "pad_a_press": _("A"),
            "pad_b_press": _("B"),
            "pad_y_press": _("Y"),
            "pad_back_press": _("Back"),
            "pad_start_press": _("Start"),
            "pad_guide_press": _("Guide"),
            "pad_dpleft_press": _("D-Pad"),
            "pad_dpright_press": _("D-Pad"),
            "pad_dpup_press": _("D-Pad"),
            "pad_dpdown_press": _("D-Pad"),
            "pad_leftx_neg": _("Joystick"),
            "pad_leftx_pos": _("Joystick"),
            "pad_lefty_neg": _("Joystick"),
            "pad_lefty_pos": _("Joystick"),
            "pad_rightx_neg": _("Joystick"),
            "pad_rightx_pos": _("Joystick"),
            "pad_righty_neg": _("Joystick"),
            "pad_righty_pos": _("Joystick"),
            ## Mobile Event Names
            ## Prefixed with "mobile_" to avoid overlapping with mouse names.
            "mobile_mouseup_1": _("Tap"),
            "mobile_K_AC_BACK": _("Back Button")}

    ## ---! Missing Key Text
    ## String to use if we can't find a human-readable key name.
    KEYMAP_MISSING_NAME = _("Unknown")

    ## ---! No Bindings Text
    ## String to use if an action has no controls bound to it.
    KEYMAP_NONE_NAME = _("Not set")

    KEYMAP_MOBILE_NAMES = {
        "mouseup_1": _("Tap")}

    ## ---! Modifier Names
    ## Dictionary mapping Ren'Py keysym modifiers to human-readable names.
    KEYMAP_MOD_NAMES = {
        "repeat": _("Hold"),
        "shift": _("Shift +"),
        "ctrl": _("Ctrl +"),
        "alt": _("Alt +"),
        "meta": _("Cmd +")}

    ## ---! Shifted Key Values
    ## Dicitonary mapping keyboard symbols to their shifted equivalents. This
    ## may need adjusting for international keyboards...
    KEYMAP_UNSHIFTED_MAP = {
        "1": __("!"), "2": __("@"), "3": __("#"),
        "4": __("$"), "5": __("%"), "6": __("^"),
        "7": __("&"), "8": __("*"), "9": __("("),
        "0": __(")"), "-": __("_"), "=": __("+"),
        "`": __("~"), ",": __("<"), ".": __(">"),
        "/": __("?"), ";": __(":"), "'": __("\""),
        "[": __("{"), "]": __("}"), "\\": __("|")}

    #---------------------------------------------------------------------------

    KEYMAP_SHIFTED_MAP = {shift: unshift for unshift, shift in KEYMAP_UNSHIFTED_MAP.iteritems()}

    #TODO AC key names need to be set manually maybe?
    def get_keyname_from_keycode(keycode):
        """
        Given a single Ren'Py keysym string/keycode, this function returns its
        human readable name equivalent. It uses `get_keyname_from_keysym()` to look up any keysyms that are part of the keycode.

        This function will also save the generated name to the `_keysym_names`
        dictionary in persistent for future use.

        Parameters
        ----------
        keycode : str or None
            A single Ren'Py keymap code, where alphanumeric characters may not
            have the "K_" prefix and all mods are added to the name.

        Returns
        -------
        str or None
            The human-readable name for the key combination, or the preset
            missing/unknown keystring if no keycode is found.
        """
        if not keycode:
            return KEYMAP_NONE_NAME

        if not isinstance(keycode, basestring):
            return KEYMAP_MISSING_NAME

        ## Separate the keysym string constant if there is one.
        keysym_part = None
        keycode_parts = keycode.split("K_")
        if "K_" in keycode:
            keysym_part = "K_" + keycode_parts.pop(-1)

        ## Create a list of all the other components of the keycode.
        keycode_parts = keycode_parts[0].split("_")
        keycode_parts = [p for p in keycode_parts if p]

        mod_parts = []
        key_parts = []
        shift_name = KEYMAP_MOD_NAMES.get("shift")
        for part in keycode_parts:
            if part in KEYMAP_MOD_NAMES:
                mod_parts.append(KEYMAP_MOD_NAMES.get(part, ""))
            elif part.isalpha():
                if part.islower():
                    part = part.upper()
                else: ## Add "Shift" to distinguish uppercase
                    if "shift" not in keycode_parts:
                        mod_parts.append(shift_name)
            else:
                if "shift" in keycode_parts:
                    ## ex. "Shift + /" becomes "?"
                    part = KEYMAP_UNSHIFTED_MAP.get(part)
                    if part:
                        try:
                            ## Shift is redundant now.
                            mod_parts.remove(shift_name)
                        except:
                            ## Shift should come before any charcters in
                            ## the keysym and be in `KEYMAP_MOD_NAMES`.
                            print("Heads up: your keycode %s might be formatted incorrectly." % keycode)
                key_parts.append(part)

        keycode_parts = mod_parts + key_parts
        keycode_parts = [p for p in keycode_parts if p]
        if keysym_part:
            keycode_parts.append(get_keyname_from_keysym(keysym_part))

        nice_name = " ".join(keycode_parts)
        if not persistent._keysym_names.get(keycode):
            persistent._keysym_names[keycode] = nice_name
        return nice_name

    def get_keyname_from_keysym(keysym):
        """
        Given a Pygame keysym constant, this function returns its human-readable name equivalent. First it tries using `get_keyname_from_id()`.

        Parameters
        ----------
        keysym : str
            The Pygame key constant, beginning with "K_".

        Returns
        -------
        keyname : str
            Either a human readable name or unicode value supplied by Pygame's
            internal functions to match the key. If an invalid keysym is used,
            the function will attempt some generic formatting.
        """
        keyname = ""

        key_id = pygame.__dict__.get(keysym)
        if key_id:
            keyname = get_keyname_from_id(key_id)

        if not keyname:
            ## Generic formatting if everything else failed.
            keyname = keysym
            keyname = event.replace("_", " ")
            keyname = event.replace("KP", "")
            keyname = event.replace("K", "")
            keyname = event.lower().capitalize()

        return keyname

    def get_keyname_from_id(id):
        """
        Given a Pygame keyboard ID constant, this function returns its built-in
        human-readable name. This is basically a wrapper for pygame.key.name()
        that won't blow up the game on failure.

        Parameters
        ----------
        id : int
            The Pygame key integer ID.

        Returns
        -------
        str
            Pygame's internal, human readable name for this key. If that's a
            blank string, it will try to find the character associated with the
            integer using `chr()`. If this fails, it returns a blank string.
        """
        keyname = ""
        try:
            keyname = pygame.key.name(id)
        except TypeError as e:
            print(repr(e))

        if not keyname:
            try:
                keyname = chr(id)
            except ValueError as e:
                print(repr(e))

        return keyname
