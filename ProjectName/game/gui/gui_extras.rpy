################################################################################
## GUI: Extras
################################################################################

## -- About/Help ---------------------------------------------------------------
## You can add information about your game here.

init python:

    ## ---! Help Location
    ## The name of a screen to open when the player presses the "help" key.
    config.help_screen = None

    ## If `config.help_screen` is None, Ren'Py will try to open `config.help`,
    ## either the name of a file or a label to jump to.
    config.help = "help.html"

screen help():
    tag menu

    style_prefix "help"

    use game_menu(_("Help"), scroll="viewport"):
        vbox:
            label config.name
            text config.version

style help_button is gui_button
style help_button:
    xmargin 8

style help_button_text is gui_button_text

style help_label is gui_label
style help_label:
    xsize 250
    right_padding 20

style help_label_text is gui_label_text
style help_label_text:
    size 30
    xalign 1.0
    text_align 1.0

style help_text is gui_text

## -- Replays ------------------------------------------------------------------
## https://www.renpy.org/doc/html/rooms.html#replay
##
## Ren'Py includes the ability to replay a scene from a menu. This can be used
## to create a "scene gallery", or memory gallery that allows the player to
## repeat important scenes. After the scene finishes, Ren'Py returns to the menu
## screen that launched the replay.

init python:
    ## --- (Transition) Enter Replay
    config.enter_replay_transition = None

    ## --- (Transition) Exit Replay
    config.exit_replay_transition = None

    ## A dictionary mapping variables in the default store to the values the
    ## variables will be given when entering a replay.
    config.replay_scope = { "_game_menu_screen" : "preferences" }

    ## Function called, with no arguments, after a replay completes.
    config.after_replay_callback = None

    ## --- Scene Names
    ## Map of label names to human readable ones, e.g. "chapter_1": "Beginning".
    ## If a label is not listed here but is used in scene select, the displayed
    ## name will just be the label name, capitalized, with underscores removed.
    scene_names = {}

    _scene_list = []

    def setup_scene_list():
        global _scene_list

        scenes = [x for x in renpy.get_all_labels() if "_screen" not in x and not x.startswith("_")]

        ## Non-story labels that have no common sematic feature.
        specials_list = ["start", "quit", "after_load", "splashscreen", "before_main_menu", "main_menu", "after_warp"]
        if not config.developer:
            specials_list.append("debug_room")

        for l in specials_list:
            true_name = config.label_overrides.get(l, l)
            try:
                scenes.remove(true_name)
            except ValueError:
                pass

        ## This sorts scenes in the list by their label name.
        scenes.sort(key=sort_naturally)

        _scene_list = []
        for l in scenes:
            name = scene_names.get(l)
            if not name:
                name = l.replace("_", " ")
                name = name.capitalize()
            _scene_list.append((name, l))

        ## Uncomment this to sort scenes by their display name.
        # _scene_list.sort(key=sort_naturally)

screen scenes():
    tag menu
    $ nav = "extras" if main_menu else "pause"
    $ setup_scene_list()
    use game_menu(_("Scene Select"), nav=nav):
        vbox:
            for l in _scene_list:
                ## Remove the `config.developer` check to test unlocking labels.
                if renpy.seen_label(l[1]) or config.developer:
                    textbutton l[0] action Replay(l[1], locked=False)
                else:
                    textbutton _("???") action NullAction

## -- Music Room ---------------------------------------------------------------
## A screen where players can listen to songs they've encountered in-game.

init python:

    ## ---! Music Room Channel
    ## The volume channel Music Room tracks will play on.
    mr_channel = "music"

    ## ---! Music Room Order
    ## Song name slugs in the order they should be listed in the music room.
    mr_order = [
        "bumper_silly",
        "scorpion",
        "museum",
        "punks-recess",
    ]

    ## ---! Music Folder
    ## The folder where music files are located. This should be a subfolder
    ## under `config.audio_directory` ("audio" by default).
    music_directory = "music"

    #---------------------------------------------------------------------------

    ## Internally used to map audio file names to display names.
    _music_fn_dict = {}

    mr = MusicRoom(channel=mr_channel)

    #TODO test no _mr_order
    #TODO punks-recess should break on playing?
    #TODO test that resetting data locks songs in here except always_unlocked
    def setup_music_room():
        global _music_fn_dict

        songs = []
        try: ## Check if _mr_order exists and is not None
            songs = mr_order
            songs[0]
        except: ## Auto-populate song list from music_directory folder
            if not config.audio_directory or not music_directory:
                return

            prefix = config.audio_directory.rstrip("/") + "/"
            prefix += music_directory.rstrip("/") + "/"

            for fn in renpy.list_files(prefix):
                if not fn.startswith(confg.prefix):
                    continue

                basename = os.path.basename(fn)
                base, ext = os.path.splitext(basename)
                songs.append(base)

        for song in songs:
            song_fn = audio.__dict__.get(song)
            song_info = music_map.get(song)
            if song_fn and song_info:
                try:
                    unlocked = song_info.get("unlocked")
                    song_info = song_info.get("name")
                except:
                    unlocked = False
                mr.add(song_fn, unlocked, SetScreenVariable("mr_playing", song_info))
                _music_fn_dict[song_fn] = song_info
    #TODO uncomment
    #setup_music_room()

screen musicroom():
    tag menu

    default mr_playing = "" #TODO test screen variable

    use game_menu(_("Music Room")):
        style_prefix "mr"
        vbox:
            label mr_playing
            bar value AudioPositionValue(mr_channel) xmaximum 500

            python:
                playing = renpy.music.get_playing(mr_channel)
                playpause = u"\u25FC" if renpy.music.get_playing(mr_channel) else u"\u25B6"
                unlocked = mr.unlocked_playlist()
                try:
                    mr_is_first = playing != unlocked[0]
                    mr_is_last = playing != unlocked[-1]
                except IndexError:
                    mr_is_first = False
                    mr_is_last = False

            hbox:
                textbutton u"\u00AB":
                    action mr.Previous()
                    sensitive mr_is_first
                textbutton playpause:
                    action mr.TogglePlay()
                    sensitive unlocked
                textbutton u"\u00BB":
                    action mr.Next()
                    sensitive mr_is_last
            $ i = 1 ## Track number.
            for fn in mr.playlist:
                if mr.is_unlocked(fn):
                    $ track_name = _("%d. %s") % (i, _music_fn_dict.get(fn, fn))
                else:
                    $ track_name = _("?????") ## Locked track name.

                textbutton track_name:
                    action If(renpy.music.get_playing(mr_channel) != fn, mr.Play(fn), mr.Stop())

                $ i += 1

style mr_button_nextprev is mr_button
