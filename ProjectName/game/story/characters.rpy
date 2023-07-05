################################################################################
## Story: Characters
################################################################################
## This file defines character objects, settings, and callbacks.

init python:

    ## The default value of the callback parameter of Character.
    config.character_callback = None

    ## --- (Callbacks) All Characters
    ## A list of callbacks that are called by all characters. This list is
    ## prepended to the list of character-specific callbacks.
    config.all_character_callbacks = []

    ## --- (Callback) Character Say Arguments
    ## Function used to process say arguments associated with characters.
    # config.say_arguments_callback = None

    ## --- (Callback) Character Voice Tag
    ## Function called with the character's voice tag.
    # config.voice_tag_callback = None

    ## --- Character Style Prefixes
    ## Style property prefixes that can be given to a Character object. For
    ## example: adding "namebox" to this list allows you to define a character
    ## with style properties:
    ##
    ##     define e = Character("Eileen", namebox_background="pink",
    ##     namebox_color="#000")
    ##
    ## When the character is speaking, the displayable on the Say screen with
    ## the id "namebox" will use the "pink" background and black text color.
    config.character_id_prefixes = ["namebox"]

    ## --- Descriptive Text
    ## The character used to display the descriptive text when self-voicing mode
    ## is enabled. This character can be invoked in a descriptive context using
    ## "sv". If set to None, Ren'Py will use the narrator for this purpose.
    # config.descriptive_text_character = None

    def say_callback(file, event, **kwargs):
        """
        Handles functions that occur during say statements. Right now, it clears certain variables based on accessibility settings, plays a
        unique beeping sound whenever a character is talking, and sets a custom
        last_say_who flag to the current character when the statement ends for
        TTS purposes.

        Parameters:
            file (str):  The file to play for talking beeps.
            event (str): The current part of the say interaction.
        """
        try:
            if event == "show":
                renpy.music.play(file, channel=blips_channel)
            elif event == "slow_done":
                renpy.music.stop(channel=blips_channel)
        except:
            pass

    curried_say_callback = renpy.curry(say_callback)

    def GameCharacter(name, talk="talk", **properties):
        """
        Wrapper for Character object with a default callback for character
        talk sounds etc. and the sidebar image set to show Kiane.

        Parameters:
            name (str, None): The character's name.
            talk (str): The character's talk sound, i.e., "[talk].ogg".
            **properties: Other properties passed to Character object.

        Returns:
            Character object with the given properties.
        """

        talk = "sounds/talk/" + talk + ".ogg"

        return Character(name, callback=curried_say_callback(talk), **properties)

## Example characters; feel free to change or delete them.
define e = Character(_("Eileen"))
define l = Character(_("Lucy"))
define en = Character(_("Eileen"), kind=nvl)

## Subtitles character, used to provide captions for important sounds.
define alt = Character(None, who_alt=_("Caption"), condition="getattr(persistent, 'prefs_subtitles')", window_style="say_none")