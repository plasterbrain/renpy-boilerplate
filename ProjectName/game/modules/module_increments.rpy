################################################################################
## Module: Increments
################################################################################
## A custom action used to allow the user to press a button to either select an
## adjacent value in a list or change a number by a certain value.

init -1 python:

    ## Init offset -1: Values needed for defaults and `_set_prefs_resolution()`

    ## ---! (Increments) Font Transforms
    increments.font_transform_list = ["dejavusans", "opendyslexic"]
    increments.font_transform_names = {
        "dejavusans": _("DejaVu Sans"),
        "opendyslexic": "OpenDyslexic"}

    ## ---! (Increments) FPS
    increments.gl_framerate_list = [30, 60, None]
    increments.gl_framerate_names = {
        30: _("30 FPS"),
        60: _("60 FPS"),
        None: _("Max")}

    ## ---! (Increments) Performance Mode
    increments.gl_powersave_list = ["auto", True, False]
    increments.gl_powersave_names = {
        "auto": _("Auto"),
        True: _("Powersaving"),
        False: _("Performance")}

    ## ---! (Increments) Tearing Mode
    increments.gl_tearing_list = [False, True]
    increments.gl_tearing_names = {
        False: _("Frameskip"),
        True: _("Tearing")}
    increments.gl_tearing_tt = {
        False: _("Compensate for graphics issues by skipping frames."),
        True: _("Compensate for graphics issues by screen tearing.")}

    ## ---! (Increments) Self-Voicing
    increments.self_voicing_list = [False, True, "clipboard"]
    if config.developer: ## Add debug voicing for developers.
        increments.self_voicing_list.append("debug")
    increments.self_voicing_names = {
        False: _("Disabled"),
        True: _("Text-to-speech"),
        "clipboard": _("Clipboard"),
        "debug": _("Debug Mode")}
    increments.self_voicing_tt = {
        False: _("Self-voicing will be disabled."),
        True: _("Game text will be read aloud using text-to-speech."),
        "clipboard": _("Game text will be copied to the clipboard."),
        "debug": _("Self-voicing text will be shown in a notification window.")}

    ## ---! (Increments) Resolution
    ## List of screen size options as tuples (width, height).
    increments.prefs_resolution_list = [(1280,720), (1440,810), (1600,900), (1920, 1080)]
    increments.prefs_resolution_names = {x: _("%d x %d") % x for x in increments.prefs_resolution_list}

    ## ---! (Increments) Graphics Renderer
    ## A list of tuples pairing the renderer option with conditions required
    ## for it to be available. Note that choosing the "sw" renderer may cause
    ## Ren'Py to show the performance warning screen on next launch.
    increments.renderer_list = [
        ("auto", True),
        ("gl", not config.gl2),
        ("gl2", config.gl2),
        ("angle", renpy.windows and not config.gl2),
        ("angle2", renpy.windows and config.gl2),
        ("gles", not config.gl2),
        ("gles2", config.gl2),
        ("sw", True)]
    increments.renderer_names = {
        "angle2": "ANGLE2/DirectX",
        "gl2": "OpenGL 2.0",
        "gles2": "GLES2",
        "angle": "ANGLE/DirectX",
        "gl": "OpenGL",
        "gles": "GLES",
        "auto": _("Auto"),
        "sw": _("Software")}

    #---------------------------------------------------------------------------
    increments.renderer_list = [x[0] for x in increments.renderer_list if x[1]]

    def increment_tt(variable, store=_preferences):
        """
        Searches `increments` for a tooltips dictionary for `variable`.
        """
        try:
            tt_list = getattr(increments, variable + "_tt")
            inc_value = getattr(store, variable)
            return tt_list.get(inc_value, "")
        except:
            return ""

    def increment_name(variable, store=_preferences):
        """
        Searches `increments` for a dictionary of display names for `variable`.
        """
        try:
            name_list = getattr(increments, variable + "_names")
            inc_value = getattr(store, variable)
            return name_list.get(inc_value, "")
        except:
            return ""

    class Increment(Action):
        """
        A button action that increases or decreases a value.
        """
        def __init__(self, variable, title="", decrease=False, store=None, step=1, max=100, list=None, tt="", action=None):
            """
            Initializes the class, setting the proper store object to use and
            making adjustments if a list variable was supplied.

            Parameters
            ----------
            variable : str
                The name of the variable/field to adjust, a string.
            title : str
                Accessible title for this control.
            decrease : bool, optional
                Whether this action decreases the value. Default False.
            store : obj, optional
                The object whose field we want to adjust with this action.
                Default _preference if the field exists, or else persistent.
            step : int, optional
                How much is added or subtracted from the value when you call
                this action. Default 1, or .25 for volume controls.
            max : int, optional
                The max value for this variable, default 100. If a list is
                supplied, this is set to the length of the list, minus 1.
            list : list or None, optional
                If supplied, increment adjusts the selected index of this list.
            tt : str, optional
                A string to use as the tooltip.
            action : obj or None, optional
                An action to run after Implement() is called.
            """
            self.variable = variable
            self.title = title
            self.decrease = decrease
            self.store = store
            self.step = step
            self.max = max
            self.list = list
            self.tooltip = tt
            self.action = action

            ## Whether this is adjusting a mixer's volume
            self.volume = False
            if self.variable in _preferences.volumes:
                self.volume = True
                self.value = _preferences.get_volume(self.variable)
                self.step = .25
                self.max = 1.0
                self.list = None

            if not self.store: ## Find the store if we didn't get one
                if self.variable in _preferences.__dict__ or self.variable in preferences.__dict__:
                    self.store = _preferences
                else:
                    self.store = persistent

            self.alt =  _("Decrease") if self.decrease else _("Increase")
            ## e.g., "SFX Volume: Increase."
            self.alt = _("{0}: {1}").format(self.title, self.alt)

            if not self.volume:
                self.value = getattr(self.store, self.variable)

            if self.list:
                ## The list index is found using reverse lookup, so all items
                ## in the list should be unique.
                if len(self.list) is not len(set(self.list)):
                    raise Exception("List items need to be unique.")
                try:
                    self.value = self.list.index(self.value)
                except ValueError:
                    ## Default to first item in the list.
                    setattr(self.store, self.variable, self.list[0])
                    self.value = 0
                except IndexError:
                    raise Exception("Increment() needs a non-empty list.")

                self.step = 1
                self.max = len(list) - 1
                self.alt = _("View previous option") if self.decrease else _("View next option")
                ## e.g., Framerate: 30 FPS selected. View next option.
                self.alt = _("{0}: {1}. {2}").format(self.title, increment_name(self.variable, self.store), self.alt)
            elif not self.value:
                self.value = self.max

        def __call__(self):
            #if self.get_selected():
            #    return
            if self.decrease:
                self.value -= self.step
                if self.value < 0:
                    self.value = 0.0
                    if self.volume:
                        _preferences.mute[self.variable] = True
            else:
                if self.volume:
                    self.value = _preferences.get_volume(self.variable)
                self.value += self.step
                if self.value > self.max:
                    self.value = self.max

            if self.list:
                setattr(self.store, self.variable, self.list[self.value])
            elif self.volume:
                _preferences.set_volume(self.variable, self.value)
            else:
                setattr(self.store, self.variable, self.value)

            if self.action:
                # ;D
                self.action.__init__()
                self.action.__call__()
            else:
                renpy.restart_interaction()

        def get_tooltip(self):
            return self.tooltip

        def get_sensitive(self):
            if self.decrease:
                if self.volume:
                    return _preferences.get_volume(self.variable) > 0.0
                return self.value
            else:
                if self.volume:
                    return _preferences.get_volume(self.variable) < self.max
                return self.value < self.max

        #def get_selected(self):
        #    if self.decrease:
        #        if self.volume:
        #            return _preferences.get_volume(self.variable) == 0.0
        #        return self.value == 0
        #    else:
        #        if self.volume:
        #            return _preferences.get_volume(self.variable) == self.max
        #        return self.value == self.max

    def IncrementList(variable, list=None, title="", decrease=False, store=None, tt="", action=None):
        """
        A wrapper for Increment() where list is a non-optional parameter. If
        not supplied, the function will look for "{VARIABLE}_list" in the
        increments store, and raise an exception if nothing is found.
        """
        try:
            list = getattr(increments, variable + "_list")
        except Exception as e:
            if not list:
                raise e
        return Increment(variable, decrease=decrease, store=store, list=list, title=title, tt=tt, action=action)

init -2 python in increments:

    #---------------------------------------------------------------------------
    ## Init offset -2: Create namespace used by the rest of the file.
    pass
