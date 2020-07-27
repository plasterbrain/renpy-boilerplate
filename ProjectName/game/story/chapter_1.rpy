################################################################################
## Story: Chapter 1
################################################################################
## The actual script of the game! Wow!! I bet it's really good!

label chapter_1:
    e "Alpha Team, you search uptown."
    e "Gold Team, you search downtown."
    e "Any questions?"
    ## If config.descriptive_text_character is not explicitly set, this will
    ## show up if the player has self-voicing turned on.
    sv "Eileen turns to Lucy, a buff fish wearing a Speedo."
    l "..."
    ## This is a subtitle, which shows up if persistent.prefs_subtitles is True.
    alt "Eileen's phone goes off. Her ringtone is \"Toxic\" by Brittney Spears."
    l "GOLD TEAM RULES!"
    return
