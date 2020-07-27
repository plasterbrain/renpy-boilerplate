################################################################################
## API: Discord
################################################################################
## https://discordapp.com/developers/docs/rich-presence/how-to#updating-presence

init python:

    DISCORD_API_KEY = "12345"

    #---------------------------------------------------------------------------
    import time
    try:
        import discord_rpc
    except ImportError:
        pass

    discord_starttime = time.time()
    def discord_connected(current_user):
        print("Connected to Discord as %s" % current_user)

    def discord_disconnected(codeno, codemsg):
        print("Discord disconnected with code %s: %s" % (codeno, codemsg))

    def discord_error(errno, errmsg):
        print("Discord connection closed with error code %s: %s" % (errno, errmsg))

    discord_callbacks = {
        "ready": discord_connected,
        "disconnected": discord_disconnected,
        "error": discord_error}

    def discord_init():
        try:
            discord_rpc.initialize(DISCORD_API_KEY, callbacks=discord_callbacks, log=False)
        except Exception as e:
            print(repr(e))

    def discord_update(details=None, state=None, icon=""):
        update_data = {
            "start_timestamp": discord_starttime,
            "details": details,
            "state": state,
            "large_image_key": icon}

        discord_rpc.update_presence(**update_data)
        discord_rpc.update_connection()
        discord_rpc.run_callbacks()

    #config.start_callbacks.append(discord_init)
