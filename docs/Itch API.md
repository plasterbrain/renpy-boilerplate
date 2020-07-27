# itch.io Integration

- `persistent.itch` Whether this is the itch.io version of the game. True if the *api_itch.rpy* file exists.
`persistent.itch_app` Whether the game is being run from the Itch app. True if the app manifest caused Itch to set a `ITCHIO_API_KEY` environment variable.
- Various itch.io brand and app UI colors in the `gui` store.

## Update notification (*api_itch.rpy*)
You can request the latest version of your game for the player's platform available on Itch. If it's newer than the current version, a window will pop up over the main menu indicating that a new version is available for download. This functionality is disabled by default, but is enabled if the user turns on "check for new versions" in the options menu.

```python
config.start_callbacks.append(itch_fetch_update)
```
You can customize the `itch_update_prompt()` screen however you want. By default, it shows your project name/thumbnail, the new version number, and a preview of the latest devlog.

It's a good idea then to have your newest devlog pertain to the latest release, at least for a little while. There's no way to show only the newest "changelog" style post. Itch.io devlogs have various categories (to differentiate changelogs from "behind-the-scenes" posts), but <u>all</u> of them are marked under the devlog category on the RSS. Shame on you, itch!

The script does not have a way to download your game thumbnail from Itch, so you'll have to add your own. `itch_thumbnail` is set to a grey square of the approximate thumbnail size, but you should overwrite it to point to an image file representing your game. The thumbnail is 125 x 96 pixels by default.

Note

## itch.io devlog
Use `itch_fetch_devlog()` to fetch data from the RSS feed of your itch.io devlog, located at https://{USER}.io/{PROJECT}/devlog.rss. The title, date, excerpt, and link for each entry are saved as a dictionary, then added to a list in `persistent.itch_devlog`. By default, it fetches only the newest entry, but you can supply any number to the function or None to fetch all entries.

Note any fancy HTML in the excerpt (like italics or links) will probably appear as plaintext.

## Itch App manifest (*.itch.toml*)
This [Itch app config file](https://itch.io/docs/itch/integrating/manifest.html) gives players launch options for Itch app users playing your game. You can use this file to pass platform-specific arguments to executables, change the [default launch option text](https://itch.io/docs/itch/integrating/manifest-actions.html#names), and add an option to open the manual or a web link.

Using the `scope` parameter in this file also creates a game- and session-specific JWT saved to the `ITCHIO_API_KEY` environment variable. You could use this value to verify whether the Itch app user has legitimately purchased your game.

This file is totally optional to have, so you can remove it if you don't need special Itch desktop app launch features.

### Instructions
You may want to read up on TOML formatting to understand how this file is structured.

#### Required steps
1. Set the `path` value for each platform to match `build.executable_name` (*build.rpy*). For example, if your executable name is "start," change `path` to "start.exe" for Windows, "start.app" for Mac, and so on.

#### Maybe required steps
1. Remove the "play" action entries for any platforms you're not distributing on.

#### Optional steps
1. The names used in the file by default ("play," "manual," and "forums") are a few of the labels which have automatic translations in the Itch app. If you want to use custom names for your actions, and your game is available in other locales, use the following format, underneath the appropriate action, to provide your own translations:
```
[[actions.locales.es]]
name = "Bailar"
[[actions.locales.it]]
name = "Ballare"
```
1. If you want users to be able to open your game's manual/readme file from the Itch app, uncomment the "manual" action and set the value of `path` to match `config.help` (*config.rpy*), the name of your readme file in the base game folder.
1. If you want users to be able to open a web link from the Itch app, uncomment the "forums" action. To use a label other than "forums," see the above entry on translating action names.
1. The `sandbox` parameter will force your game to launch in [sandbox mode](https://itch.io/docs/itch/using/sandbox.html), protecting the user from potentially malicious software. You can remove this line if you want, though the documentation says it may be required in the future.

## Removing this feature

1. (*.itch.toml*) the entire file
