################################################################################
## Module: Custom GUI Actions
################################################################################
## Classes offering additional action functionality to your screens.

## -- Delete All Data ----------------------------------------------------------

init python:
    #TODO test that canceling confirm will cancel operation.
    #TODO test double confirm
    #TODO test all
    #TODO test that style prefs reset
    class DeleteData(Action):
        def __init__(self, type="progress", confirm=True):
            """
            Parameters
            ----------
            type : str
                The type of data to delete. Accepts "progress" (the default) to
                remove save files and persistent data, "prefs" to restore
                preferences to default, "screenshots" to remove the custom
                screenshots folder, or "all" to do all three.
            confirm : bool or str, optional
                Whether to prompt the user for confirmation before going ham.
                Default True. If set to "twice," you can prompt two confirmation
                messages, to ask if the player is really, really sure.
            """
            self.type = type
            self.confirm = confirm

            if self.type == "all":
                self.message = _("Reset all game data? This will remove save files, screenshots, and your saved preferences.")
            if self.type == "prefs":
                self.message = _("Reset game settings to their defaults?")
            elif self.type is "screenshots":
                self.message = _("Delete all screenshots?")
            else:
                self.type = "progress"
                if self.confirm is "twice":
                    self.message = _("Delete save data?")
                else:
                    self.message = _("Are you sure you want to delete your game progress? This cannot be undone.")
            self.message2 = _("Are you sure? This cannot be undone.")

        def __call__(self):
            """
            Shows a confirmation popup if necessary and then deletes the
            selected data, or cancels if the player selects "no."
            """
            if self.confirm == "twice":
                # Prompt the first of two confirmation messages and send a
                # parameter that says we did this.
                layout.yesno_screen(self.message, DeleteData(self.type, "second"))
            elif self.confirm == "second":
                # Prompt confirmation with self.message2.
                layout.yesno_screen(self.message2, DeleteData(self.type, False))
            elif self.confirm:
                # Prompt confirmation with self.message.
                layout.yesno_screen(self.message, DeleteData(self.type, False))
            else:
                if self.type in ["prefs", "all"]:
                    _delete_prefs()
                if self.type in ["screenshots", "all"]:
                    _delete_folder("screenshots")
                if self.type in ["progress", "all"]:
                    _delete_progress()
                    renpy.full_restart()

## -- Load Most Recent Save ----------------------------------------------------
## Adds the ability to "continue" the game from the most recent save file.

init python:
    class LoadMostRecent(Action):
        def __init__(self):
            self.slot = renpy.newest_slot(r"\d+")

        def __call__(self):
            renpy.load(self.slot)

        def get_sensitive(self):
            return self.slot is not None

## -- Open Directory -----------------------------------------------------------
## Adds the ability to open the folder from a button.

    import os

    class OpenFolder(Action):
        """
        Opens the given folder in the system file browser. This code is adapted
        from Ren'Py's OpenDirectory() (front_page.rpy).

        Attributes
        ----------
        alt : str
            The default alt text for the displayable with this action.
        """

        alt = _("Open [text] in file browser.")

        def __init__(self, directory):
            """
            Sets the directory to open.

            Parameters
            ----------
            directory : str
                The name of the folder to open, relative to the project root.
            """
            self.directory = os.path.join(config.basedir, directory)

        def get_sensitive(self):
            """
            Shows the button with his action as selectable if the requested
            folder exists.
            """
            return os.path.exists(self.directory)

        def __call__(self):
            """
            Attempts to open the requested folder in the file browser. If
            unsuccessful, it will print a message and do nothing else.
            """
            try:
                directory = renpy.fsencode(self.directory)

                if renpy.windows:
                    os.startfile(directory)
                elif renpy.macintosh:
                    subprocess.Popen([ "open", directory ])
                else:
                    subprocess.Popen([ "xdg-open", directory ])
            except:
                print("Failed to open %s." % directory)

## -- Set Graphics Renderer ----------------------------------------------------
## An action that changes the renderer but also sets a persistent variable if
## the new selection differs from the current renderer. This can be used to show
## text prompting the user to restart.

init python:

    ## ---! Renderer Setting
    ## Whether a new renderer has been selected and the game should be restarted.
    persistent._changed_renderer = False
    persistent.old_renderer = _preferences.renderer

    class SetRenderer(Action):
        """
        Sets the graphics renderer. Identical to Ren'Py's `_SetRenderer`, but it
        also changes `persistent._changed_renderer` to true, so that the screen
        can display a message warning users to restart.

        This code is adapted from Ren'Py's `_SetRenderer` action (00gltest.rpy).

        Attributes
        ----------
        alt : str
            The alt text supplied to the UI element that calls this action.
        """

        alt = _("Set graphics renderer to [text].")

        def __init__(self, renderer=None):
            """
            Initializes the class. If an invalid renderer is requested, the
            action will raise an error for devs and set the renderer to "auto"
            (the default) for players.

            Parameters
            ----------
            renderer : str
                The string representing the new renderer to use, one of "auto",
                "gl", "gl2", "angle", "angle2", "gles", or "gles2".
            """
            if not renderer:
                renderer = _preferences.renderer

            if renderer not in ["auto", "gl", "gl2", "angle", "angle2", "gles", "gles2"]:
                if config.developer:
					if renderer is "sw":
						raise Exception("The software renderer has been removed as of Ren'Py 7.4.")
					else:
                    	raise Exception("Invalid renderer %s" % s)
                else:
                    renderer = "auto"
            self.renderer = renderer

        def __call__(self):
            """
            Sets the value of _preferences.renderer to the requested renderer,
            and then sets `persistent._changed_renderer` to True.
            """
            _preferences.renderer = self.renderer
            if self.renderer == persistent.old_renderer:
                ## Remove the "restart" message if we switch back to the
                ## original renderer setting without restarting the program.
                persistent._changed_renderer = False
            else:
                persistent._changed_renderer = True

            renpy.restart_interaction()

        def get_selected(self):
            """
            Renders the button as already selected if the requested renderer is
            already being used.
            """
            return _preferences.renderer == self.renderer


init -1 python:
    #TODO test with button sensitivity
    class SetResolution(Action):
        def __init__(self, size=None):
            if not size:
                size = persistent.prefs_resolution
            self.size = size

        def __call__(self):
            if renpy.mobile:
                return
            renpy.set_physical_size(self.size)
            renpy.restart_interaction()

        def get_selected(self):
            return self.size == renpy.get_physical_size()

## -- Style Value --------------------------------------------------------------
## Allows you to update an integer GUI preference, such as RGB color or opacity,
## using a slider.

init python:

    ## Interally used to check if `style.rebuild()` should be run.
    persistent._changed_style = False

    class StyleValue(FieldValue):
        def __init__(self, field, range, style="slider", action=None, offset=0):
            """
            Initializes the value class.

            Parameters
            ----------
            field : str
                The GUI preference to update. This is the first parameter given
                to `gui.preference()` when defining a GUI preference variable.
            range : int
                The max value of this preference.
            style : str, optional
                The style this bar should use. Default "slider".
            action : obj or None, optional
                An action to run after updating the preference. Default None.
            offset : int, optional
                The minimum value of the slider. Default 0. If offest is
                negative or a larger number than range, it will be reset to 0.
            """
            self.field = field
            self.range = range

            self.style = style
            self.action = action

            self.offset = offset
            if self.offset < 0 or self.offset > self.range:
                self.offset = 0

        def get_adjustment(self):
            """
            Updates the visible bar value using the persistent _gui_preference
            dictionary rather than the gui namespace.
            """
            value = persistent._gui_preference.get(self.field)

            range = self.range - self.offset
            value -= self.offset
            return ui.adjustment(
                range=range,
                value=value,
                changed=self.changed,
                step=10,
                force_step=False,
            )

        def changed(self, value):
            """
            Updates the bar value sets `persistent._changed_style` to True, and
            runs the appropriate style-adjusting function. This method tries to
            evaluate a function called `_change_PREF(value)`, where PREF is the
            name of the style preference. It takes one argument, the new value
            of the style preference.

            Parameters
            ----------
            value : int
                The bar's new value.
            """
            new_value = value + self.offset
            if new_value > self.range:
                new_value = self.range
            value = new_value

            if not persistent._changed_style:
                persistent._changed_style = True

            persistent._gui_preference[self.field] = value

            try:
                eval("_change_" + self.field + "(" + str(value) + ")")
            except:
                pass
            renpy.restart_interaction()

    def maybe_update_styles(statement):
        """
        Tells Ren'Py to rebuild styles if a style preference has been updated
        through a bar using StyleValue. It checks for persistent._changed_style,
        as style.rebuild() is too slow to run as part of StyleValue's changed()
        method. This function is appended to config.statement_callbacks.

        Parameters
        ----------
        statement : str
            The type of statement being run.
        """
        if persistent._changed_style:
            persistent._changed_style = False
            style.rebuild()

    config.statement_callbacks.append(maybe_update_styles)
