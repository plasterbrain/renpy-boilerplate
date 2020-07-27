# Discord Integration


## Dispatch Config (*config.json*)
If you plan to create a Discord server for your game for testing or distribution, you'll need to use Discord's command line uploading utility, Dispatch. This [config file](https://discordapp.com/developers/docs/dispatch/branches-and-builds#setting-up-our-first-build) tells Dispatch how to bundle and distribute your game.

### Instructions

#### Required steps
1. Set the `id` to your game's application ID. To get an application ID, create an app for your game on the [Discord Developer Portal](https://discord.com/developers/applications). Copy the value listed on the app settings page under "client ID."
1. Under `storage`, replace the part of each `path` value where it says "ProjectName" to match the value of `config.save_directory` (*config.rpy*). For example, if your `config.save_directory` value is "CoolSaveFolder," the `path` for Windows should be "${DATA}/RenPy/CoolSaveFolder".
 - You can delete any platforms in this section if they don't apply to your game, or delete this entire section if you don't want Discord to handle cloud saves for whatever reason.
 - If you are <u>not</u> setting a custom value for `config.save_directory`, Ren'Py will use your project name followed by a hyphen and a 10-digit ID. You'll have to go to your user app data folder to find the exact folder name. Set the `path` to match this value.
 - If you set `config.save_directory` to *None*, Ren'Py is only storing game data in the *game/saves* folder. You can set the `path` value for all three platforms to "${INSTALLDIR}/game/saves", though I don't know how this interacts with the *user_data* property yet.

#### Maybe required steps
1. The `manifests` array contains the settings for your game's manifests, which are comparable to Ren'Py build packages. By default, Ren'Py's "marketplace" package includes compatibility files for Windows, Mac, and Linux, so you shouldn't need more than one manifest in the array. However, if you have multiple unique build packages you want to distribute via Discord, you'll need multiple manifests. For example, Here's how you might structure separate manifests if you have windows- and linux-specific build packages.
```
{
  "application": {
    "id": 12345,
    "manifests": [
      {
        "label": "game-windows",
        "platforms": ["win32", "win64"]
        // ...
        // Windows-specific storage info...
        // Windows-specific launch options...
        // ...
      },
      {
        "label": "game-linux",
        "platforms": ["linux"],
        // ...
        // Linux-specific storage info...
        // Linux-specific launch options...
        // ...
      }
    ]
  }
}
```
One advantage of separating by platform is that your launch options don't need unique names across the separate manifests. As is, the launch options have names like "Game (Windows)" to keep them unique. With separate manifests, they could just be "Game."
1. Adjust `platforms` to only include the platforms relevant to the current manifest.
1. If you want to move *config.json* somewhere else, you should update `local_root` so it points to the game's base project folder.
1. Add any files to `exclusions` section that appear in your distribution build that should be excluded when a Discord user downloads your game. Use this format for every new file pattern to exclude, like this:
```
  {
    "local_path": "filetoexclude.txt"
  },
  {
    "local_path": "dlc/**.*"
  }
```
1. Under `launch_options`, edit each `executable` value to mach `build.executable_name` (*build.rpy*).
 - Remove any platforms here that don't apply to your game.

#### Optional steps
1. Each manifest `label` can be whatever you want, but should be unique across manifests. You will need this label name when setting up Discord store channels.
1. Similarly, the `id` under key can be set to anything, but should never be changed after you publish a live build of your game.

#### Removing this file
If you don't plan to distribute your game on Discord, you can delete this.

1. (*config.json*) the entire file
