# Web Updater (included in gui_extras.rpy)
Ren'Py's [web updater feature](https://www.renpy.org/doc/html/updater.html) lets players easily check for, download, and install updates within your game if you have the game files hosted online somewhere.

It uses zsync to only download new or modified files instead of redownloading the entire game for every patch.

The updater can be used to download DLC packages as well, though Ren'Py doesn't have a built-in way to sell this DLC outside of [frameworks on mobile](https://www.renpy.org/doc/html/iap.html?highlight=app).

## How to use this feature
The web updater requires hosting a number of files, including a zipped build of your game, on a web server with direct access to file URLs and HTTP range requests (shared hosting or something like [Fast.io](https://fast.io) may work).

The web updater does not work with mobile or web builds, nor do you need it when distributing on Steam.

For games on itch.io: the Itch app handles automatic patching in much the same way as Steam. However, many (most?) users still download games through the website and launch them directly. For these users, see the [update notification feature in *api_itch.rpy*](/Itch%20API.md).

To include a web updater in your game, use the following steps:
1. Build a distribution of your game with updates. There will now be an updates folder inside your distributed project directory with *current.json* inside. Next to your compiled build you'll find *updates.json* along with various update data files for each package:
  - *{PACKAGE}.sums*
  - *{PACKAGE}.update.gz*
  - *{PACKAGE}.update.json*
  - *{PACKAGE}.zsync*
1. Upload *updates.json* and the various package files to a single directory on your web server.
1. Edit the updater action in *gui_nav.rpy* to point to the location of *updates.json* on your server.

By default, the updater screen runs in simulation mode when `config.developer` is True. It pretends to find, download, and install an update. This is so you can see how the process will look for the end user.

## Removing this feature
The web updater is entirely optional or a Ren'Py game. You should also delete it if your game is *only* going to be on Steam. I also don't think it works with web and mobile Ren'Py distributions.

1. (*gui_updater.rpy*) The entire file
1. (*gui_nav.rpy*) The "Update" textbutton on the main_menu screen.
