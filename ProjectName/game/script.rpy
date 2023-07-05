################################################################################
## Program Flow
################################################################################
## This file handles how the game launches, runs, and exits.

init -1 python:

	#---------------------------------------------------------------------------
	## Init offset -1 so this can be overriden by the auto_command().
	is_automode = False

	def errorping(message, type="error"):
		if config.developer:
			renpy.notify(message)
		print(message)

## -- Launch -------------------------------------------------------------------

init python:

	## --- (Callbacks) Start
	## List of functions called, with no arguments, after the init phase, but
	## before the splashscreen starts. This is intended for frameworks to
	## initialize variables that will be saved. The default value includes
	## callbacks that Ren'Py uses to implement features like nvl mode.
	# config.start_callbacks.append()

	## --- Auto-Load
	## Name of the save slot to load when launching the game.
	#TODO test if this foregoes splashscreen etc.
	config.auto_load = None

	## --- (Mobile) Minimum Splash Time
	## The minimum amount of time, in seconds, a presplash, Android presplash,
	## or iOS LaunchImage is displayed for. If Ren'Py initializes before this
	## amount of time has been reached, it will sleep to ensure the image is
	## shown for at least this amount of time.
	config.minimum_presplash_time = 0.0

	## --- (Transition) Splashscreen to Main Menu
	config.end_splash_transition = None

	## ---! Persistent Data
	## By default, when merging conflicting persistent data files, Ren'Py will
	## use the more recently saved value. Custom functions can override this.
	def psnt_combine_data(old, new, current):
		current.update(old)
		current.update(new)
		return current

	def psnt_use_true(old, new, current):
		return old or new

	#renpy.register_persistent('seen_endings', psnt_combine_data)

label _choose_renderer:
	## Ren'Py jumps to this label if the user holds shift on startup. Normally
	## it shows the "choose renderer" screen. Note that getting this to work
	## requires either allowing duplicate labels or suppressing duplicate label
	## errors with `config.ignore_duplicate_labels`.
	#TODO If some funky behavior comes up it's probably this.

	# scene expression "#000"
	# $ renpy.shown_window()
	# $ renpy.show_screen("_choose_renderer",  _transient=True)
	# $ ui.interact(suppress_overlay=True, suppress_underlay=True)

	return

# label splashscreen:
	## If it exists, this label is called when the game is first run, before
	## showing the main menu.

label before_main_menu:
	## If it exists, this label is called before the main menu. It is used in
	## rare cases to set up the main menu, for example by starting a movie
	## playing in the background.
	$ itch_notify_update()
	show screen loading
	jump main_menu_screen

# label main_menu:
	## If it exists, this label is called instead of the main menu. If it
	## returns, Ren'Py will start the game at the start label.

## -- Game ---------------------------------------------------------------------

init python:

	## --- (Transition) End Game to Main Menu
	config.end_game_transition = None

## Initialize a player object to save info to.
default player = Player()

label start:
	## Add the parts of your story here.
	call chapter_1
	## call chapter_2
	## call chapter 3
	## ...
	return

## -- Jump/Warp ----------------------------------------------------------------
## Settings for jumping around the script in large chunks.

# init python:

	## --- (Callbacks) Fast Skipping
	## List of functions called, without arguments, when fast skipping happens.
	# config.fast_skipping_callbacks.append()

## -- Load Game ----------------------------------------------------------------
## If you release significant updates for your game, this is where you can
## specify how to handle any outdated save data.

init python:

	## --- (Callback) After Load (6.99.11)
	## A list of functions called, with no arguments, when a load occurs.
	# config.after_load_callbacks = []

	## --- Load Failed Label (7.3.0)
	## Label to jump to when Ren'Py fails to load a game because it can no
	## longer find the current statement. Accepts either a string with the label
	## to jump to, a function, or None to raise an error. The function is called
	## with no arguments and should return a string giving the label to jump to.
	config.load_failed_label = None

	## --- (Transition) Menu to Loaded Game
	config.after_load_transition = None

# label after_load:
	## This label is called when a game is loaded. It can be use to fix data
	## when the game is updated.

## -- Quit ---------------------------------------------------------------------

init python:

	##  --- Autosave on Quit (6.14)
	config.autosave_on_quit = True

	## --- (Callback) Quit Game (6.99.11)
	## Action called when the user clicks the quit button on the game window.
	## The default action prompts the user to see if he wants to quit the game.
	config.quit_action = Quit()

	## --- (Mobile) Background Quit
	## If True, the mobile app will quit when it loses focus.
	config.quit_on_mobile_background = False

	## --- (Mobile) Background Save
	## If True, the mobile app will save its state when it loses focus, so the
	## game can resume its place when the app starts again.
	config.save_on_mobile_background = True

label quit:
	python:
		try:
			discord_rpc.shutdown()
		except:
			pass

## -- Label/Context Settings ---------------------------------------------------

init python:

	## --- Label Overrides
	## A dictionary of label redirections. For example, if you map the label
	## "start" to "mystart", any calls to "start" will go to "mystart" instead.
	# config.label_overrides = {}

	## --- Duplicate Labels (7.2.0)
	## Whether multiple labels with the same name are allowed.
	config.allow_duplicate_labels = False

	## ---! Suppress Duplicate Label Errors
	config.ignore_duplicate_labels = True

	## --- Missing Return Label (7.4.0)
	## Label to jump to when "return" statement fails.
	config.return_not_found_label = None

	## --- (Callbacks) Interaction Start
	## List of functions that are called, with no arguments, when an interaction
	## is started, but not when it is restarted.
	# config.start_interact_callbacks = []

	## --- (Callbacks) Interaction Start/Restart
	## A list of functions that are called, without any arguments, when an
	## interaction is started or restarted.
	# config.interact_callbacks = []

	## --- (Callback) Missing Label
	## It is called with one argument, the name of the missing label,
	## and should return either the name of a label to use as a replacement, or
	## None, to raise an exception.
	config.missing_label_callback = None

	## --- (Callbacks) New Context
	## Called when Ren'Py enters a new context, such as a menu context.
	config.context_callback = None

	## --- (Callback) Periodical
	## Called, with no arguments, at around 20Hz.
	config.periodic_callback = None

	## --- (Callback) Reaching a Label
	## A function called whenever the game reaches a new label. It is called
	## with two parameters, the name of the label, and whether the label was
	## reached abnormally (by jumping, calling, or creating a new context).
	# config.label_callback = None

	## ---! (Callbacks) Statement
	## List of callbacks called before each statement. They are called with one
	## argument, the name of the statement. Ren'Py uses this to automatically
	## show/hide the text window.
	# config.statement_callbacks.append()
