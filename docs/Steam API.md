# Steam Integration

## Instructions

1. Paste your app ID into *steam_appid.txt*. There will only be one ID for your game as a whole; don't confuse it with IDs for depots.

## Removing Steam integration
1. (*steam_appid.txt*) delete the entire file
1. (*utilities.rpy*) remove the check for *steam_handles_screenshots* in `_delete_folder()`.
