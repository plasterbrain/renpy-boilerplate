################################################################################
## Utilities
################################################################################
## Game-agnostic functions.

## -- Competion Percentage -----------------------------------------------------

init python:

    def get_completion_rate():
        total = renpy.count_dialogue_blocks()
        seen = renpy.count_seen_dialogue_blocks()
        return "{0:.0%}".format(float(seen)/float(total))

    def accumulate_runtime(statement):
        """
        Regularly adds runtime of the current session to a persistent total.
        """
        if not persistent._runtime:
            persistent._runtime = 0
        persistent._runtime += renpy.get_game_runtime()
        renpy.clear_game_runtime()

    #TODO too often?
    config.statement_callbacks.append(accumulate_runtime)

## -- Compare Versions ---------------------------------------------------------

init python:

    def semver_str_to_tuple(string):
        return tuple(int(n) for n in string.split("."))

## -- Natural Sort

init python:

    import re
    def sort_naturally(element):
        """
        Use this function as a key with `sort()` to use natural sorting rather
        than ASCII (e.g. "1, 2, 10, 11" instead of "1, 10, 11, 2").

        https://nedbatchelder.com/blog/200712/human_sorting.html
        https://stackoverflow.com/a/5967539

        Parameters
        ----------
        element: str
            The element to sort through. Rather than each digit being processed
            separately, the function will process entire groups of consecutive
            digits as one number.

        Returns
        -------
        str or int
            The single character or atomic number to be used for sorting.
        """
        return [int(c) if c.isdigit() else c for c in re.split('(\d+)', str(element))]

## -- Hyperlink File Handler ---------------------------------------------------

init python:

    def file_handler(value):
        """
        Handles the given value as a file to be opened in the web browser.
        Based on Ren'Py's `_help` function invoked by the F1 key.

        Parameters
        -----------
        value : string
            The name of the file to open; a path relative to the game's base
            directory. Ren'Py won't do anything if it doesn't exist.
        """
        try:
            import webbrowser
            import os

            file_path = os.path.join(config.basedir, value)

            if not os.path.isfile(file_path):
                if config.developer:
                    print(_("ERR: Opening hyperlink file %s failed. File does not exist.") % value )
                return

            webbrowser.open_new("file:///" + file_path)
        except Exception as e:
            if config.developer:
                print(dir(e))
            else:
                pass

    config.hyperlink_handlers["file"] = file_handler

## -- XML/RSS Feed -------------------------------------------------------------

init python:
    def fetch_rss(url, field, entries=1):
        """
        Grabs one or more posts from an RSS feed and stores them as a dictionary
        in a persistent variable.

        Parameters
        ----------
        url : str
            The RSS/XML feed to parse.
        field : str
            The persistent field to edit, a string. (ex: for persistent.thing,
            field should be "thing")
        entries : int
            The number of entries to store in the dictionary. Default 1.
        """
        import urllib
        import socket
        import xml.etree.ElementTree
        from xml.etree.ElementTree import parse

        ## Give up after this many seconds.
        socket.setdefaulttimeout(3)

        try:
            rss = urllib.urlopen(url)
            devlog = parse(rss)
        except IOError:
            print(_("Urllib error: %s is an invalid URL.") % url)
            return
        except socket.timeout:
            print(_("Timed out fetching RSS. Check your internet connection."))
            return
        except Exception as e:
            print(repr(e))
            return

        setattr(persistent, field, [])

        i = 1
        for post in devlog.iterfind("channel/item"):
            getattr(persistent, field).append({
                "title": post.findtext("title"),
                "link": post.findtext("link"),
                "date": post.findtext("pubDate"),
                "category": post.findtext("category"),
                "excerpt": ''.join(xml.etree.ElementTree.fromstring(post.findtext("description")).itertext()), ## C L A S S Y
            })
            if i == entries:
                break
            i += 1

## -- Custom Choice Menu -------------------------------------------------------
# Allows the user to randomize options on the choice menu.

# Hooks up the custom function with Ren'Py.
define menu = _custom_menu

init -1 python:
    #TODO test this
    def _custom_menu(items):
        """
        A substitution for the default renpy.display_menu, which is used to pass
        choices in the script to a choice screen. Currently, this custom function randomizes the items in a choice menu if menu_shuffled is True.

        This code is adapted from the "shuffling choice" tutorial by Pytom:
        https://www.patreon.com/posts/shuffling-choice-13572006

        Parameters
        ----------
            items : list
                The list of menu choice tuples, as they're ordered in the
                script. Each tuple contains the label (what's shown to the user)
                and the return value if that choice is selected. Menu captions
                have a return value of None.

        Other Parameters
        ----------------
            screen : str, optional
                The name of the screen to use, default "choice"
            window_style : str, optional
                Name of the style to use for the window, default "menu_window"
            caption_style : str, optional
                Style of the menu caption, default "menu_caption"
            choice_style : str, optional
                Style of the choices on the menu, default "menu_choice"
            choice_chosen_style : str, optional
                Style of choices that have been previously selected, default
                "menu_choice_chosen".
            choice_chosen_button_style : str, optional
                Choice of the button element of a previously selected choice,
                default "menu_choice_chosen_button"
            interact : bool, optional
                Whether an interaction is performed, default True.
            with_none : bool or None, optional
                If True, performs a with None to after the screen is shown. If
                None, takes the value from config.implicit_with_none. The
                default is None.
            scope, widget_properties : dict
                These are passed to the choice screen, but I have no idea what
                they do! Wow, what a mystery!!

        Returns
        -------
            items : list
                The list of menu choice objects, either as they were or in a new, random order.
        """
        items = items[:]

        if menu_shuffled:
            renpy.random.shuffle(items)

        return renpy.display_menu(items)

## -- Delete Data Functions ----------------------------------------------------

default persistent.test = "butter"

init python:
    def _delete_progress():
        """
        Deletes all save files, persistent data, and seen elements, resetting
        game progress to zero. Note that this function does not call a
        confirmation prompt or run renpy.full_restart(). Ideally, you should
        use DeleteData() to call this function.
        """
        ## Delete save files
        for slot in renpy.list_saved_games(fast=True):
            renpy.unlink_save(slot)

        ## Delete seen data
        renpy.game.seen_translates_count = 0

        ## For games with achievements NOT synced to an external API
        # achievement.clear_all()

        ## Names, as strings, of persistent variables to keep.
        keep_persistent = [
            "_keynames",
            "_reverse_keymap",
            "_changed_renderer",
            "_custom_prefs_default",
            "default_keymap",
            "prefs_keymap",
            "prefs_resolution",
            "_itch_update_shown",
            "_itch_update_available",
        ]
        kept_persistent = {}
        for field in keep_persistent:
            kept_persistent[field] = getattr(persistent, field)

        ## Delete the rest of the persistent data
        persistent._clear(progress=True)

        ## Restore desired persistent variables
        for field, data in kept_persistent.iteritems():
            setattr(persistent, field, data)

        ## Clear cache. Why not?
        renpy.free_memory()

        print("Save data and progress deleted.")

    def _delete_prefs():
        """
        Restores all preferences to their defaults. It supports built-in
        and GUI preferences natively, but not support style preferences.

        It does not reset language.
        """
        ## Built-in Preferences
        for name, value in persistent._preference_default.iteritems():
            setattr(_preferences, name, value)
            setattr(preferences, name, value)

        ## Built-in Preferences (old style)
        for name, value in config.__dict__.iteritems():
            if not name.startswith("default_"):
                continue
            config_pref = name.split("default_")[1]
            if value is not None:
                try:
                    ## voice_sustain, mouse_move, afm_enable,
                    ## show_empty_window, emphasize_audio
                    _preferences.__dict__[config_pref] = value
                except:
                    if config_pref == "wait_for_voice":
                        ## config.wait_for_voice = _preferences.wait_voice
                        _preferences.wait_voice = value
                    elif "_volume" in config_pref:
                        ## Default mixer volumes
                        config_pref = config_pref.split("_")[0]
                        _preferences.set_volume(config_pref, value)

        ## GUI Preferences
        for name, value in persistent._gui_preference_default.iteritems():
            try:
                persistent._gui_preference_default[name] = value
            except:
                pass
        persistent._changed_style = True

        ## Custom Preferences
        for name, value in persistent._custom_prefs_default.iteritems():
            setattr(persistent, name, value)

        print("Preferences restored to factory settings.")

    #TODO test removing screenshot folder
    #TODO test removing screenshots from basedir
    #TODO test removing save folder (appdata) - PERMISSIONS ERROR?
    #TODO test removing save folder (in game folder)
    def _delete_folder(type="screenshots"):
        """
        Deletes an ancillary game storage folder. If "screenshots" is specified
        and no custom screenshot_folder exists, it will try to remove any
        screenshots in the base game directory.

        Parameters
        ----------
        type : str
            The type of folder to delete. Accepts "screenshots" (the default)
            to try wiping the custom screenshots folder or screenshots in the
            base directory, or "save" to delete the save data folder.
        """
        import os
        import shutil
        import glob

        if type is "save":
            folder = config.savedir
        else:
            try:
                if steam_handles_screenshots:
                    return
                folder = os.path.join(config.basedir, screenshot_folder)
            except:
                print("Custom screenshot folder not set.")
                try:
                    # Delete all the screenshots in the base directory. Why not?
                    while True:
                        fn = os.path.join(dest, config.screenshot_pattern % i)
                        if not os.path.exists(fn):
                            break
                        os.remove(fn)
                        i += 1
                    print("Screenshots in %s successfully deleted." % config.basedir)
                except:
                    print("Error deleting screenshots.")
                return

        if os.path.isdir(folder):
            try:
                shutil.rmtree(dest)
            except OSError as e:
                print(str(e))
                return
        print("Successfully deleted %s." % folder)

## -- Screenshot Handlers ------------------------------------------------------

init -1 python:

    ## Init offset -1: Used by `config.screenshot_callback`
    def _custom_screenshot_callback(fn):
        """
        Shows the user a notification after a screenshot is taken.

        Parameters
        ----------
        fn : str
            The full file path of the screenshot that was just taken.
        """
        fn_short = fn.rsplit('\\', 1)[-1]
        renpy.notify(_("Saved %s.") % fn)

init 1 python:

    ## Init offset 1: We need config.keymap and config.underlay established
    ## and optionally steam_handles_screenshots set.
    #TODO test if calling this outisde of console with a bad screenshot pattern
    #throws an error or just fails silently
    def _custom_screenshot(pattern=None, notify=False, returns=True, error=False):
        """
        This function adapts code from `_screenshot` (00keymap.rpy).
        """
        import datetime
        import os
        import os.path
        import __main__

        pattern = config.screenshot_pattern if not pattern else str(pattern)
        error = "_error" if error else ""

        time = datetime.datetime.now()
        time_taken = time.strftime("%Y-%m-%d")

        ## Allowed file extensions: https://www.pygame.org/docs/ref/image.html
        for ext in [".bmp", ".tga", ".jpeg", ".png"]:
            if pattern.endswith(ext):
                extension = ext
                break
        try:
            pattern = pattern.replace(extension, error + extension)
        except NameError:
            if config.developer:
                raise Exception("Screenshot file pattern should end with \".png\", \".jpeg\", .\".bmp\" or \".tga\".")
            ## Fr players it will fail silently

        try:
            ## Create screenshot directory if it does not exist.
            dest = os.path.join(config.basedir, screenshot_folder)
            if not os.path.isdir(dest):
                os.mkdir(dest)
        except:
            dest = config.basedir
            if renpy.macapp:
                dest = os.path.expanduser(b"~/Desktop")

        i = 1
        while True:
            fn = os.path.join(dest, pattern.format(time_taken, i))
            if not os.path.exists(fn):
                break
            i += 1

        try:
            if not renpy.screenshot(fn): ## Returning pygame surface failed.
                if notify:
                    renpy.notify(_("Failed to save screenshot as %s.") % fn)
                return
        except: ## Calling the screenshot function apparently failed.
            import traceback
            traceback.print_exc()
            if notify:
                renpy.notify(_("Failed to save screenshot as %s.") % fn)
            return

        # Filename with the path removed.
        if notify and config.screenshot_callback is not None:
            config.screenshot_callback(fn)

        if returns:
            #TODO can we return this anyway and call funct from keymap?
            return fn

    def _custom_keymap_screenshot():
        if steam_handles_screenshots:
            return
        return _custom_screenshot(None, True, False)

    config.underlay[0].__dict__["keymap"]["screenshot"] = _custom_screenshot

## -- Scan Translations --------------------------------------------------------

init python:

    def scan_translations():
        """
        Returns a list of tuples coupling the names of available translation
        languages for this game with Python identifiers.

        This code is borrowed from Ren'Py's Launcher preferences screen
        (preferences.rpy).

        Returns
        -------
        rv : list
            List of tuples containing a human readable language name and a
            Python identifier (or None, for the default language).
        """

        languages = renpy.known_languages()

        rv = [("English", None)]

        for i in languages:
            rv.append((i.replace("_", " ").title(), i))
        return rv
