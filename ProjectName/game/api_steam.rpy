################################################################################
## API: Steam
################################################################################

python early:

	## ---! Steam App ID
	## For use when calling Steamworks API in Ren'Py, for example to open the
	## store page for your game in Steam overlay.
	config.steam_appid = ""

init python:

    ## --- Achievement Notification Position
    ## If not None, this sets the position of the steam notification popup, one
    ## of "top left", "top right", "bottom left", or "bottom right".
    achievement.steam_position = None

    ## Whether the Ren'Py screenshot functionality should be disabled in favor
    ## of Steam's screenshot API.
    steam_handles_screenshots = False

    #---------------------------------------------------------------------------
    ## ---! Steam API
    ## Whether the Steam API is initialized. It's set every time the game
    ## initiates. We don't want it "defaulted" in case the user runs a second
    ## non-Steam copy on the same machine.
    try:
        _renpysteam
        persistent.steam = True
    except:
        persistent.steam = False
