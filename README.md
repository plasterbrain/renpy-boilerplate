# Ren'Py Project Template
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT) [![License](https://img.shields.io/badge/License-BSD%200--Clause-orange.svg?style=flat-square)](https://opensource.org/licenses/0BSD) ![GitHub repo size](https://img.shields.io/github/repo-size/plasterbrain/Renpy-Template?style=flat-square) ![Twitter Follow](https://img.shields.io/twitter/follow/plasterbrain?style=flat-square&logo=twitter)

This is a blank Ren'Py project template for people with more robust visual novel needs. It's mostly geared towards non-mobile games, though the mobile features haven't been gutted entirely.

## Features
- QOL additions
  - An icon shows when the game is auto-saving
  - Pause screen opens to the last used submenu
  - Screenshots saved with timestamp to a nameable folder
  - User key bindings
- Screen additions
  - Web Updater screen
  - Music Room
  - Scene/Replay Select
  - Removes the built-in Ren'Py "blue screens"
    - Exception and performance warning screens have custom styling
    - Accessibility and graphics settings menus are disabled and their options are included in the in-game preferences
  - Robust preferences screen
    - Additional built-in preferences: Language, stop AFM after clicks, AFM wait for voice clips, self-voicing mode, mute individual channels, test sound buttons, emphasize audio, voice sustain, in-game font, text size, line spacing, graphics renderer, FPS, screen tearing, powersaving mode, run performance test on startup
    - New preferences: Text box opacity, subtitles, screen resolution
  - Custom "Increment" action lets you change a bar value or look through items in a list using a button
  - Basic checkbox-style buttons
- Utilities
  - A treasure trove of config variables!
  - "Player" object you can save inventory and other user variables to
  - Get game completion rate and time spent playing
  - Delete save data/reset preferences
  - Some basic persistent data merging functions
- Game manual HTML template
  - Includes basic troubleshooting and license info
  - Pretty HTML pages for every Ren'Py license
  - Extra license pages for Creative Commons, Pixabay, and others
- Third-party integrations
  - Check for/notify user of new itch.io version on startup
  - Fetch itch.io devlog RSS data
  - Disable screenshots in Steam version
  - Discord RPC
  - Detect if game is using Steam or Itch app
- Developer tools
  - Debug room
  - "Auto play" command
  - Manifest/config file templates for Itch, Steam, and Discord Dispatch
  - Batch/Powershell scripts to upload builds to itch.io and Steam

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

## License
This project template is dual-licensed under the BSD 0-Clause License if you want to avoid including a copyright notice, and the MIT License if you hate crayon licenses.

Four out of five doctors agree I'm perfect, but I can't promise the same of my code, which probably kinda sucks actually. This template comes with no warranty of fitness for any particular purpose.
