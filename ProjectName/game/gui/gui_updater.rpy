################################################################################
## GUI: Web Updater
################################################################################
## https://www.renpy.org/doc/html/updater.html

init python:
    ## Enables the "Build Updates" option in the Ren'Py launcher.
    build.include_update = True

    ## --- Update Testing
    ## This can be one of None, "available", "not-available", or "error". It
    ## must be None for a release.
    UPDATE_SIMULATE = config.developer

    gui.updater_labels = {
        "CANCELLED": _("The updates were canceled."),
        "CHECKING": _("Checking for updates..."),
        "DONE": _("The updates have been installed. [config.name] will now restart."),
        "DONE_NO_RESTART": _("The updates have been installed! You should restart the game."),
        "DOWNLOADING": _("Downloading the new version..."),
        "ERROR": _("An error has occured:"),
        "FINISHING": _("Finishing up..."),
        "PREPARING": _("Preparing to download the updates..."),
        "UNPACKING": _("Unpacking the updates..."),
        "UPDATE AVAILABLE": _("Version [u.version] is available! Press \"next\" to download and install it."),
        "UPDATE NOT AVAILABLE": _("[config.name] is already up to date!"),
    }

    gui.updater_width = int(config.screen_width * 0.6)

screen updater(u=u):
    tag menu

    style_prefix "updater"

    add gui.main_menu_background

    vbox:
        vbox:
            style "updater_message_vbox"

            label _("Update")
            text gui.updater_labels.get(u.state)
            if u.message is not None:
                text "[u.message!q]"

        if u.progress is not None:
            hbox:
                style_prefix "updater_progress"
                bar value u.progress range 1.0 style "updater_progress_bar"
                text "{0:.0%}".format(u.progress)

        hbox:
            ## This shows the canceled message and a return button when you
            ## cancel, instead of just returning wordlessly to the main menu.
            if u.state == u.CANCELLED:
                textbutton _("Return") action u.cancel
            elif u.state == u.DONE:
                textbutton _("Continue") action u.proceed
            elif u.state == u.DONE_NO_RESTART:
                textbutton _("Done") action u.proceed
            else:
                textbutton _("Cancel"):
                    action [SetField(u, "state", u.CANCELLED), SetField(u, "cancelled", True)]
                    sensitive u.can_cancel
                textbutton _("Next"):
                    action u.proceed
                    sensitive u.can_proceed

style updater_vbox:
    xalign 0.5
    xmaximum gui.updater_width
    xsize gui.updater_width
    yalign 0.5
    ysize 300

style updater_message_vbox:
    spacing 10

style updater_label_text:
    size 50
    color gui.h1_color

style updater_text:
    line_spacing 8
    xsize gui.updater_width

style updater_progress_hbox:
    xalign 0.0

style updater_progress_bar is _bar:
    xsize (gui.updater_width - 150)
    ysize 25

style updater_progress_text:
    min_width 100
    text_align 1.0
    xalign 1.0

style updater_hbox:
    xalign 1.0
    yalign 1.0
    spacing gui._scale(25)
