# Ren'Py Project Template
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT) [![License](https://img.shields.io/badge/License-BSD%200--Clause-orange.svg?style=flat-square)](https://opensource.org/licenses/0BSD) ![GitHub repo size](https://img.shields.io/github/repo-size/plasterbrain/RenpyTemplate?style=flat-square) ![Twitter Follow](https://img.shields.io/twitter/follow/plasterbrain?style=flat-square&logo=twitter)

This is a blank Ren'Py project template for people with more robust visual novel needs. It's mostly geared towards non-mobile games, though the mobile features haven't been gutted entirely.

## Features
### Utilities & QOL Enhancements
- An icon shows when the game is auto-saving
- Pause screen opens to the last used submenu
- Screenshots saved with timestamp to a nameable folder
- **User-customizable key bindings!!!!**
- Most config variables are included and documented for total customization of the engine
- "Player" object you can save inventory and other rollback-averse user variables to
- Completion rate and playtime functions
- Delete data and reset preferences functions
- Basic persistent data merging functions

### Screen/Screen Language Features
- Custom "Increment" screen action lets you change a bar value or look through items in a list using a button
- Checkbox-style buttons
- Web Updater screen included
- Basic Music Room setup
- Scene Replay screen included
- Exception and Performance Warning screens have custom styling
- **Feature-rich preferences menu**
  - Additional built-in preferences: Language, stop AFM after clicks, AFM wait for voice clips, self-voicing mode, mute individual channels, test sound buttons, emphasize audio, voice sustain, in-game font, text size, line spacing, graphics renderer, FPS, screen tearing, powersaving mode, run performance test on startup
  - New preferences: Text box opacity, subtitles, screen resolution
  - Accessibility and graphics options are included here and their built-in Ren'Py screens are disabled

### Third-Party Integrations
- Detect if game is using Steam or Itch app
- Fetch itch.io devlog RSS data
- Check for and notify user of new itch.io version on startup
- Disable screenshots in Steam version

### Help Manual
- Robust HTML5 template for a user-friendly manual
- Includes basic troubleshooting and license info
- Pretty HTML pages for every Ren'Py license you need, with customizable values using URL parameters
- Extra license pages for Creative Commons, Pixabay, and others

### Developer Tools
- Manifest/config file templates for Itch, Steam, and Discord Dispatch
- Batch/Powershell scripts to launch project, delete dev save data, convert image formats, and upload builds to itch.io and Steam
- Debug room
- "Auto play" command

## Todo List
- Game Jolt API integration with login screen and achievements. This is totally doable but also a huge waste of time except as a proof-of-concept.
- A tooltip for the text speed preference that appears at the chosen text speed.
- Ability to remap gamepad controls. I don't have a controller so I can't really work this out right now.
- Steam-like achievement popup for itch.io, Game Jolt, etc.
- Upload scripts for Discord/Dispatch, which is currently indefinitely unavailable.

### Testing
- Build scripts, including Discord Dispatch configuration whenever that becomes a thing again.
- Running a Ren'Py game from the Itch app and getting the `"ITCHIO_API_KEY"` environment variable
- Validate entitlements example using plutil

## Changelog
0.0.0 - Initial commit

0.1.0
- Cleaned up tab/space formatting, typos, extra numbers, and some inaccuracies in license files
  - Notably the BSD-3 endorsement clause has been fixed to say "may *not* be used." I copypasted a typo stating the opposite from the version of the license included with GLEW, where it remains. At least... I think it's a typo?
- License file CSS is now a separate file and not inline, so they'll all match if you change it.
- New *license.js* file to handle dynamically populating license fields with query parameters. Just include it in any dynamic licenses.
  - MIT, BSD-3, and SIL-OFL pages now have dynamic copyright lines which can be changed using URL parameters, to better suit their "above copyright notice" wording.
- Updated Ren'Py dependency copyright list
  - Fixes to various copyright names/years.
  - Extra trademark information where applicable.
  - Scripts used by the manual now include the MIT/copyright notice in their source code so they don't clutter the manual text.
  - Removed py2exe, as I believe it is included with Ren'Py to make the distributables of your game and used when building the engine, but not actually distributed with the game itself.
  - Removed pyobjc, as I can't actually find it anywhere in the Ren'Py/desktop dependency source except as an outdated dependency for TTS system and getting Ren'Py to run on non-Windows systems.
- Project template license simplified to MIT-0 (formerly dual-licensed under BSD-0 and MIT)

## License
All *original* code/text created for this project template is licensed under MIT-0. Some files, e.g. the CSS and JS dependencies of the help manual template, are the copyright of their respective authors, and will have their license information included.

- The texts of the various licenses included here are also the property of their respective owners.
- The Patreon logo is a registered trademark of Patreon, Inc. included in the help manual for the purpose of creating a button to link to your Patreon. I do not own it, and it is included under the vague legal "Font Awesome" standard of redistributing social media icons for creator convenience.

### Warranty
Four out of five doctors agree I'm perfect, but I can't promise the same of my code, which probably kinda sucks actually. This template comes with no warranty of fitness for any particular purpose.
