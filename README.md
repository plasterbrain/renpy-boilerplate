# Ren'Py Project Template
[![License: MIT](https://img.shields.io/badge/License-MIT0-grey.svg?style=flat-square)](https://opensource.org/licenses/MIT-0) ![GitHub repo size](https://img.shields.io/github/repo-size/plasterbrain/RenpyTemplate?style=flat-square)

A Ren'Py project starter template based on tricks I learned while making *Pizza Game*. This is for developers who like to get the most out of the Ren'Py engine and is geared towards desktop (rather than mobile) visual novels.

## Features
- "Player" object to track inventory and other rollback-averse variables
- Web-based game manual with basic troubleshooting and license info (including customizable pages showing all license text)
- Subtitles character for describing story-critical sounds
- Manifest/config files for uploading to itch and Steam
- Batch/Powershell scripts to launch project, delete dev save data, convert image formats, and upload builds to itch.io and Steam
- Debug room to separate basic testing from your story files
- All built-in config variables defined with compatibility notes

### New/enhanced screens
- Music Room
- Scene Gallery/Scene Select
- Custom Exception and "Performance Warning" screens
- Pause screen that always opens to the last used submenu
- Expanded Preferences screen with 5 submenus:
  - General options (language select, text box opacity, accessibility settings)
  - Controls (keyboard/mobile/gamepad input lists, custom key bindings)
  - Graphics (replaces Ren'Py's hidden Performance Settings menu)
  - Audio (mute individual channels, test sound volume, emphasize audio)
  - Data (privacy settings, delete save data option, reset preferences, completion stats)
- Web Updater
- Spin buttons
- Checkbox buttons

### New/updated functions
- Detect if user is in itch.io/Steam
- Show if a new game version is available on itch
- Show a HUD icon when the game auto-saves
- Customize screenshot desintation folder and include a timestamp in screenshot filename
- Merge persistent data
- Disable built-in Ren'Py screenshots when running on Steam
- Run the game automatically (for basic testing)
- Fetch RSS (e.g. to include game news on the game menu)


## Todo List
- [Audio panning](https://www.renpy.org/doc/html/audio.html?highlight=audio#renpy.music.set_pan)/monophonic option for unilateral deafness 
- Self-voicing confirmation popup window allowing users to cancel if accidentally toggled
- Replicate Steam achievement HUD for other platforms
- Some rudimentary example for calling to a custom server API which then could ping Discord to avoid exposing API keys
- Game Jolt API integration with login screen and achievements. Totally doable but also a huge waste of time due to low player adoption rate (except as a proof-of-concept for periodic API callbacks)
- Demonstration text for text speed preference
- Gamepad control remapping
- Entitlements file location?
- "Unit testing" scripts
- Related: some system for keeping pace with Ren'Py updates re: compatibility changes, new/removed dependencies, new config variables etc.
- LayeredImage example?
- `.gitignore` template and basic instructions on how to set up Git for your project, bearing in mind that this template is meant to be customized to smithereens and thus can't really be treated as an isolated dependency...

### Testing
- Validate build scripts
- Validate entitlements example using plutil
- Getting `"ITCHIO_API_KEY"` environment variable when running from itch app
- CFAppleHelpAnchor pointing to `help` (or does Ren'Py puts it somewhere incompatible during the build process?)
- Notarizing Mac apps requiring them to be zipped and/or to not have any Windows/Linux nonsense sitting in the same directory

## Changelog
### 0.0.0
- Initial commit

### 0.1.0
- Cleaned up tab/space formatting, typos, extra numbers, and some inaccuracies in license files. BSD-3 endorsement clause has been fixed to say "may *not* be used." I copypasted a typo stating the opposite from the version of the license included with GLEW, where it remains. At least... I think it's a typo? :thonk:
- License file CSS is now a separate file and not inline, so they'll all match if you change it. Durr.
- New *license.js* file to handle dynamically populating license fields with query parameters. Just include it in any dynamic licenses.
  - MIT, BSD-3, and SIL-OFL pages now have dynamic copyright lines which can be changed using URL parameters, to better suit their "above copyright notice" wording.
- Updated Ren'Py dependency copyright list
  - Fixes to various copyright names/years.
  - Extra trademark information where applicable.
  - Scripts used by the manual now include the MIT/copyright notice in their source code so they don't clutter the manual text.
  - Removed py2exe, as I believe it is included with Ren'Py to make the distributables of your game and used when building the engine, but not actually distributed with the game itself.
  - Removed pyobjc, as I can't actually find it anywhere in the Ren'Py/desktop dependency source except as an outdated dependency for TTS and getting Ren'Py to run on non-Windows systems.
- Project template license simplified to MIT-0 (formerly dual-licensed under BSD-0 and MIT)

### 0.2.0
- Added copyright info for libraries included in Ren'Py 7.4.x to the template
- New Apache license template file
- New LICENSE-3RD-PARTY file for comfort and convenience
- New 7.4 Ren'Py variables added

### 0.3.0
- Reformatted README for clarity

## License
@TODO text here!