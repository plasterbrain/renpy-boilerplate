################################################################################
## GUI: Error Screens
################################################################################
## For the complete white label experience, you can customize these built-in
## Ren'Py error screens to match the look of your game.

init 1 python:

    ## --- Custom Exception Handler (7.3.5)
    ## Function used in place of Ren'Py's default error handler. It takes three
    ## arguments: the shortened traceback (showing only your game's files in the
    ## stack trace), a string; the full traceback (showing files from your game
    ## and Ren'Py core in the stack trace), a string; and the path to a file
    ## containing a traceback method.
    ##
    ## Accepts a function or None to use Ren'Py's built-in handler.
    ##
    ## If the function returns True, the exception is ignored and control is
    ## transferred to the next statement. If it returns False, the built-in
    ## exception handler is used. This function may also call renpy.jump() to
    ## transfer control to some other label.
    def call_custom_exception_screen(screen_name, **kwargs):
        try:
            old_quit = renpy.config.quit_action
            renpy.config.quit_action = renpy.exports.quit
            persistent._error_screencap = _custom_screenshot(error=True)
            persistent._error_screencap = persistent._error_screencap.replace("\\", "/")

            for i in renpy.config.layers:
                renpy.game.context().scene_lists.clear(i)

            renpy.show_screen(screen_name, _transient=True, **kwargs)
            return renpy.ui.interact(mouse="screen", type="screen", suppress_overlay=True, suppress_underlay=True)
        finally:
            try:
                import os
                os.remove(persistent._error_screencap)
            except:
                pass
            renpy.config.quit_action = old_quit

    def custom_report_exception(short, full, traceback_fn):
        """
        Reports an exception to the user. Returns True if the exception should
        be raised by the normal reporting mechanisms. Otherwise, should raise
        the appropriate exception to cause a reload or quit or rollback.
        """
        global error_handled
        global _autosave
        error_handled = True
        _autosave = False

        renpy.display.error.error_dump()

        if renpy.game.args.command != "run":  # @UndefinedVariable
            return True

        if "RENPY_SIMPLE_EXCEPTIONS" in os.environ:
            return True

        try:
            renpy.display.error.init_display()
        except:
            return True

        if renpy.display.draw is None:
            return True

        ignore_action = None
        rollback_action = None
        reload_action = None

        try:
            if not renpy.game.context().init_phase:

                if renpy.config.rollback_enabled:
                    rollback_action = renpy.display.error.rollback_action

                reload_action = renpy.exports.curried_call_in_new_context("_save_reload_game")

            else:
                reload_action = renpy.exports.utter_restart

            if renpy.game.context(-1).next_node is not None:
                ignore_action = renpy.ui.returns(False)
        except:
            print("5")
            pass

        try:
            renpy.game.invoke_in_new_context(
                call_custom_exception_screen,
                "error",
                short=short, full=full,
                rollback_action=rollback_action,
                reload_action=reload_action,
                ignore_action=ignore_action,
                traceback_fn=traceback_fn,
                )

            _autosave = True

            if renpy.store._ignore_action is not None:
                renpy.display.behavior.run(renpy.store._ignore_action)
            return True

        except renpy.game.CONTROL_EXCEPTIONS:
            raise

        except:
            renpy.display.log.write("While handling exception:")
            renpy.display.log.exception()
            raise

    config.exception_handler = custom_report_exception


screen error(short, full, traceback_fn, rollback_action, reload_action, ignore_action):
    modal True
    zorder 102 ## Behind confirm windows, above everything else.

    style_prefix "error"

    python:
        tt = GetTooltip()
        tt = tt if tt else ""
        try:
            platform = renpy._platform.platform()
            platform = platform.replace("-", " ")
        except:
            platform = renpy.platform.replace("-", " ")

        bigger = increments.prefs_resolution_list.index(persistent.prefs_resolution) + 1
        if bigger >= len(increments.prefs_resolution_list):
            bigger = len(increments.prefs_resolution_list) - 1

    add im.Blur(persistent._error_screencap, .5) size increments.prefs_resolution_list[bigger]

    frame: ## Background and padding.

        vbox: ## Content goes here.
            xalign 0.5
            yalign 0.5
            spacing 10

            hbox: ## Title
                xfill True
                label gui.warning_symbol + " " + _("An error has occurred.")
                vbox: ## Some diagnostic info unrelated to the specific error
                    xalign 1.0
                    yalign 0.5
                    text _("Version [config.version]") text_align 1.0 xalign 1.0
                    text platform

            viewport:
                draggable True
                mousewheel True
                pagekeys True
                scrollbars "vertical"
                ysize gui._scale(250)
                vbox:
                    yalign 0.5
                    text short
                    if config.developer:
                        text full

            ## Action buttons
            side "l r":
                xfill True
                hbox:
                    spacing 10
                    textbutton _("Copy as Markdown"):
                        action _CopyFile(traceback_fn, u"```\n{}```\n")
                        tooltip _("Copy the traceback text in markdown format.")
                    #textbutton _("Copy as BBCode"):
                    #   action _CopyFile(traceback_fn, u"[code]\n{}[/code]\n")
                    #   tooltip _("Copy the traceback text in BBCode format.")
                hbox:
                    spacing 10
                    if config.rollback_enabled:
                        textbutton _("Rollback"):
                            action rollback_action
                            tooltip _("Try rolling back one statement.")
                    textbutton _("Ignore"):
                        action ignore_action
                        tooltip _("Try to ignore the error and continue. The game may not function as intended.")
                    textbutton _("Quit"):
                        action Function(renpy.quit, status=1)
                        tooltip _("Quit the game.")

            text tt color gui.tt1_color

style error_frame:
    background Solid("#000000CC")
    padding(40, 20)
    xfill True
    yfill True

style error_label_text:
    size gui._scale(40)

## Traceback text.
style error_text:
    color gui.tt2_color
    line_spacing 4
    size 16

## -- Performance Warning ------------------------------------------------------
#TODO: Updates in 7.4.0 and likely will get more updates going forward
## This screen is sometimes shown if the program determines there's a display
## issue during the init phrase OpenGL performance test.
##
## It accesses the variable `problem`, which may be "sw" if the system is
## forcibly using software rendering. Historically it could also be "fixed" if
## the computer wasn't using shaders or "slow" if display performance was slow.

screen _performance_warning(problem=""):

    style_prefix "error"

    frame:
        background Solid("#000")

        vbox:
            align (0.5, 0.45)
            xysize (0.5, 0.5)
            spacing 10
            label gui.warning_symbol + " " + _("Performance Warning")

            if problem == "sw":
                text _("This computer is using software rendering.")
            elif problem == "fixed":
                text _("This computer is not using shaders.")
            elif problem == "slow":
                text _("This computer is displaying graphics slowly.")
            else:
                text _("This computer has a problem displaying graphics: [problem].") substitute True

            text _("If you experience performance issues during the game, you may need to update your graphics card drivers.")

            use checkbox(_preferences, "performance_test", label_text=_("Show this warning again"))

            textbutton _("Continue"):
                xalign 1.0
                action Return(_preferences.performance_test)
