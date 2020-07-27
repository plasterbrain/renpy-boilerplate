################################################################################
## Audio
################################################################################
## This file defines how the game processes audio data.

init python:

    ## --- Sample Rate
    config.sound_sample_rate = 48000

    ## --- Equal Mono (7.3.0)
    ## If true, Ren'Py distributes mono to both stereo channels. If false,
    ## Ren'Py splits the audio 50/50.
    config.equal_mono = True

## -- Channels -----------------------------------------------------------------

init python:

    ## --- Channel Emphasis
    ## List of channels that are emphasized over others.
    config.emphasize_audio_channels = ["voice"]

    ## How long to lower volume for on non-emphasized channels.
    config.emphasize_audio_time = 0.5

    ## How low to set the volume on non-emphasized channels.
    config.emphasize_audio_volume = 0.5

## -- Sound --------------------------------------------------------------------

init python:

    ## --- Sound
    config.has_sound = True

    ## (6.99.9) Channel used for `hover_sound`, and `activate_sound`.
    config.play_channel = "audio"

    ## (6.17.4) Whether sound loops by default.
    config.default_sound_loop = False

    ## Whether to play non-looping sounds during skip mode.
    config.skip_sounds = False

init -1 python:

    ## Init offset -1: `blips_channel` used by general character callback

    blips_channel = "talk"
    renpy.music.register_channel(blips_channel, mixer="sfx", loop=False, stop_on_mute=True, tight=True, file_prefix="", file_suffix="")

## -- Voice --------------------------------------------------------------------

init python:

    ## Whether the game has voice acting.
    config.has_voice = True

    ## Number of seconds after a voice clip ends before AFM can advance text.
    config.afm_voice_delay = .5

## -- Movies -------------------------------------------------------------------

init python:

    ## --- Movie Channels
    ## Should movie displayables be given their own channels?
    config.auto_movie_channel = True

    ## Default mixer used for automatically defined video playback channels.
    config.movie_mixer = "music"

## -- Music --------------------------------------------------------------------

init python:

    ## --- Music
    config.has_music = True

    ## Crossfade time between music tracks.
    config.fade_music = 0.0

    ## Whether to continue the fadeout if Ren'Py reaches the end of a track.
    config.tight_loop_default = True

init -1 python:

    ## Init offset -1: Used by `setup_music_room()` at init 0.

    ## ---! Music Map
    ## A dictionary mapping in-game song names to either a string with their
    ## human-readable name. or a dictionary with "name" and "unlocked" keys.
    music_map = {
        "bumper_silly": {"name": _("Bumper In: Silly"), "unlocked": True},
        "museum": _("Sunny Museum"),
        "punks-recess": _("Punks at Recess"),}
