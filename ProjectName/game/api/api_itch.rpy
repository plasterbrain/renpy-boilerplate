################################################################################
## API: itch.io
################################################################################
## Tools for connecting with the game's itch.io page.

init python:

    ## ---! (itch.io) Username
    ## Lowercase itch.io username, used in URLs.
    itch_user = ""

    ## --- (itch.io) Project Name
    ## Lowercase itch.io project name or slug, used in URLs.
    itch_project = ""

    ## ---! (itch.io) Channel Names
    ## The names of the game's channels corresponding with each platform.
    if renpy.windows:
        itch_channel = "win-mac-linux"
    elif renpy.macintosh:
        itch_channel = "mac"
    elif renpy.linux:
        itch_channel = "linux"
    elif renpy.android:
        itch_channel = "android"
    else: ## iOS or web version
        itch_channel = ""

## Whether the game should check for newer versions on itch.io on startup.
default persistent.prefs_itch_update = False

init python:

    #---------------------------------------------------------------------------
    ## Whether we're using an itch.io build and/or the Itch app.
    persistent.itch = True
    persistent.itch_app = os.environ.get("ITCHIO_API_KEY")

    ## Dictionary of devlog RSS meta, populated by `itch_fetch_devlog()`
    if not persistent.itch_devlog:
        persistent.itch_devlog = []

    gui.itch_orange_color = "#fa5c5c" ## Itch logo
    gui.itch_red_color = "#8B2E36" ## Itch app button
    gui.itch_bg_color = "#141414" ## Itch app popup background
    gui.itch_bg_border_color = "#383434" ## Itch app popup border
    gui.itch_text_color = "#DDD" ## Itch app dark UI text

    #---------------------------------------------------------------------------
    build.itch_project = itch_user + "/" + itch_project
    itch_project_url = "https://" + itch_user + ".itch.io/" + itch_project
    itch_update_url = "https://itch.io/api/1/x/wharf/latest?target=" + build.itch_project + "&channel_name=" + itch_channel

    ## If a newer version is available on itch.io, this is set to the version
    ## number as a string. Otherwise, it's False.
    persistent._itch_update_ver = False

    ## Whether the user has seen the update prompt already.
    persistent._itch_update_shown = False

    def itch_fetch_devlog(number=1):
        """
        Wrapper for `fetch_rss()` to parse the game's itch.io devlog.
        """
        fetch_rss(itch_project_url + "/devlog.rss", "itch_devlog", number)

    def itch_notify_update():
        """
        Shows an update notification if a new version is available on itch.io.
        The "okay" button on this screen opens your game's itch.io page.
        """
        if persistent._itch_update_ver and not persistent._itch_update_shown:
            persistent._itch_update_shown = True

            renpy.show_screen("itch_update_prompt")
            renpy.restart_interaction()

            ## Use the generic confirmation screen
            # layout.yesno_screen( _("A new version (%s) is available for download!") % persistent._itch_update_ver, OpenURL(itch_project_url))

    def itch_fetch_update():
        """
        Attempts to fetch the latest version of your game from Itch.io's API and
        compare it to the current game version. It will only work once per
        session, or if `persistent._itch_update_ver` is set to False.

        Returns
        -------
        tuple
            A tuple containing the version returned from Itch and whether it is
            newer than the current version (a boolean). If there was an error
            fetching a version from Itch, it will return the current version
            (from `config.version`) and False.
        """
        if not itch_channel:
            return (config.version, False)

        if persistent._itch_update_ver:
            return (persistent._itch_update_ver, True)

        # import os
        import socket
        import urllib
        import json

        ##
        socket.setdefaulttimeout(10)
        fn = "_latest.json"
        itch_ver = config.version
        update_available = False

        try:
            urllib.urlretrieve(itch_update_url, fn)
            with open(fn, "rb") as f:
                itch_info = json.loads(f.read())
            itch_ver = itch_info["latest"]
            # os.remove(fn) ## Delete the downloaded file.
        except IOError:
            print(_("Urllib error: %s is an invalid URL.") % itch_update_url)
        except socket.timeout:
            print(_("Timed out fetching version from Itch. Check your internet connection."))
        except KeyError:
            try:
                print(_("Itch URL error: %s") % itch_info["errors"][0])
            except Exception as e:
                print(repr(e))

        if itch_ver:
            itch_tuple = semver_str_to_tuple(itch_ver)
            current_tuple = semver_str_to_tuple(config.version)
            update_available = itch_tuple > current_tuple
            if update_available:
                persistent._itch_update_ver = itch_ver

        return (itch_ver, update_available)

    if persistent.prefs_itch_update and not persistent.itch_app:
        config.start_callbacks.append(itch_fetch_update)

    def itch_hyperlink_styler(target):
        """
        Returns the style object to use for hyperlinks in itch.io text.
        """
        return style.itch_hyperlink

image itchio:
    "gui/itchio.png"
    zoom .5

## The game's thumbnail on itch.io
image itch_thumbnail:
    Solid("#383434")
    size (125, 96)

style itch_frame:
    background Solid(gui.itch_bg_color)
    padding (10, 10)

style itch_vbox:
    spacing 8

style itch_text:
    color Color(gui.itch_text_color).replace_opacity(.5)
    font font_directory + "Lato.ttf"
    hyperlink_functions (itch_hyperlink_styler, hyperlink_function, None)
    line_spacing 8
    size 13

style itch_hyperlink:
    color gui.itch_orange_color
    underline True

style itch_h1 is itch_text:
    color gui.itch_text_color
    line_spacing 0
    size 18

style itch_h2 is itch_text: ## Inherits Lato
    bold True
    color Color(gui.itch_text_color).replace_opacity(.8)
    line_spacing 2
    size 16

style itch_h3 is itch_text: ## Inherits Lato
    color Color(gui.itch_text_color).replace_opacity(.65)
    line_spacing 0
    size 14

style itch_button:
    background Solid(gui.itch_orange_color)
    hover_background Color(gui.itch_orange_color).tint(.9)
    padding (15, 10)

style itch_button_text:
    size 14
    color gui.itch_text_color

## -- Screen: Itch Update Notification -----------------------------------------
## A popup screen styled after the Itch app that notifies users that a new
## version of your game is available.

init python:
    gui.itch_frame_width = 600
    gui.itch_frame_height = 380

screen itch_update_prompt():
    modal True
    zorder gui.notify_zorder

    style_prefix "itch"

    python: ## Grab some RSS data
        if not persistent.itch_devlog:
            itch_fetch_devlog(2)
        try:
            title = persistent.itch_devlog[0]["title"]
            date = persistent.itch_devlog[0]["date"]
            excerpt = persistent.itch_devlog[0]["excerpt"]
            link = persistent.itch_devlog[0]["link"]
            if excerpt and link:
                link = "{a=%s}" % link + _("(Read more)") + "{/a}"
                excerpt = excerpt + " " + link
            cat = persistent.itch_devlog[0]["category"]
        except:
            cat = False

    frame: ## This frame is the border.
        style_suffix "outer_border"
        frame: ## This frame is for the background color.
            style_suffix "outer_frame"

        vbox: ## Actual content goes here!
            align (0.5, 0.5)
            first_spacing 20
            spacing 10

            vbox:
                spacing 8
                xalign 0.5
                yoffset 10
                add "itchio" xalign 0.5
                text _("A new version is available!") style_suffix "h1"

            frame: ## The project name/icon with a download button
                style_suffix "inner_frame"
                hbox:
                    xfill True
                    hbox:
                        spacing 15
                        add "itch_thumbnail"
                        vbox: ## A box designed to look like an itch.io widget.
                            align (0.0, 0.0)
                            text config.name style_suffix "h2"
                            text _("By {b}[itch_user]{/b}") style_suffix "h3"
                            text _("Version [persistent._itch_update_ver]")
                    textbutton _("Download"):
                        style "itch_button"
                        align (1.0, 1.0)
                        action [OpenURL(persistent.itch_update_url), Hide("itch_update_prompt")]

            if cat == "devlog":
                frame: ## A box with a preview of the latest devlog update.
                    style_suffix "inner_frame"
                    vbox:
                        text title style_suffix "h2"
                        text date style_suffix "h3"
                        text excerpt

            textbutton _("No thanks"):
                style "itch_dismiss"
                action Hide("itch_update_prompt")
                keysym "game_menu"

        textbutton "X":
            style "itch_dismiss_x"
            alt _("Dismiss")
            action Hide("itch_update_prompt")

style itch_outer_frame is itch_frame:
    align (0.5, 0.5)
    xysize (gui.itch_frame_width, gui.itch_frame_height)

style itch_outer_border is itch_outer_frame:
    background Solid(gui.itch_bg_border_color)
    xysize (gui.itch_frame_width + 2, gui.itch_frame_height + 2)

## "Inner" frames, for content that should look like it's embedded from itch.io
style itch_inner_frame is itch_frame:
    background Solid(Color(gui.itch_bg_color).shade(.6))
    xfill True

style itch_dismiss:
    xalign 0.5

style itch_dismiss_text is itch_text:
    color Color(gui.itch_text_color).replace_opacity(.3)
    hover_color Color(gui.itch_text_color).replace_opacity(.5)

style itch_dismiss_x:
    align (1.0, 0.0)

style itch_dismiss_x_text is itch_dismiss_text:
    size 18
