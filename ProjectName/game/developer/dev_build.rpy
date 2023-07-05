################################################################################
## Developer: Build Settings
################################################################################
## Ren'Py includes support for building game distributions.

#-- Build Settings -------------------------------------------------------------

init python:

    ## ---! Build Name*
    ## The program-readable name of your game.
    ## This is used if some of the below values are missing.
    ## (No spaces, punctuation, or special characters.)
    build.name = "ProjectName"

    ## ---! Executable Name
    ## Name for the .exe/.app/.sh file. No special characters.
    build.executable_name = "ProjectName"

    ## ---! Version
    ## Ignore; please update `version.txt` file to set this value.
    build.version = config.version

    ## --- Directory Name
    ## Name of your output folder if you're building your game through the
    ## Ren'Py launcher wizard. The version and platform (e.g. "win" or "mac")
    ## will be added to it automatically.
    #build.directory_name = "ProjectName"

    ## --- Build Destination
    ## Path of your output folder if you're building your game through the
    ## Ren'Py launcher wizard.
    ## @see https://www.renpy.org/doc/html/build.html#var-build.destination
    #build.destination = "dists"

## -- Mac/iOS ------------------------------------------------------------------

init python:

    ## ---! Mac PLIST CFBundleDisplayName
    ## Visible to users and used by Siri.
    build.display_name = config.name

    ## --- Mac Automatic Graphics Switching
    ## Whether the program should use the integrated GPU.
    build.allow_integrated_gpu = True

    ## @TODO ?
    #build.mac_info_plist

## -- Android/Chrome OS --------------------------------------------------------

# init python:

    ## --- Google Play Public App License Key
    ## This key can be found on the Google Play developer console Services &
    ## APIs page. It should not contain any spaces or newlines.
    # define build.google_play_key = "..."

    ## --- Google Play Salt
    ## The salt used to encrypt license information returned from Google Play.
    ## Accepts a 20-byte tuple, where each byte is an integer between -128 and
    ## 127. Don't use this default one; it's just an example!
    # build.google_play_salt = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)

## -- File Classification ------------------------------------------------------

init python:

    ## ---! Mac Documentation Files
    ## In Mac builds, documentation files are stored twice, once inside the app
    ## package, and once outside of it.

    build.documentation("help.html")
    build.documentation("help/**")

    ## ---! Ignored Files

    build.exclude_empty_directories = True ## Remove empty folders from build

    build.classify("help/licenses/template.html", None)

    build.classify(".git**", None) ## Git versioning
    build.classify("**desktop.ini", None) ## Google Drive Sharing

    build.classify("**.bak", None) ## Auto-generated script backups
    # build.classify("game/**.rpy", None) ## Non-compiled scripts

    build.script_version = False ## File that says e.g. "(7, 3, 5)"

    ## ---! Archives

    ## Don't include these in any archives
    build.classify("game/developer/**", "all")
    build.classify("game/version.txt", "all")

    # build.classify("game/**", "game") ## Throw everything else in an archive
    # build.archive("game", "all") ## `game/game.rpa`

    ## --- (6.99.9) Old Ren'Py Themes
    ## Ignored if you use `gui.init()` elsewhere in this project.
    #build.include_old_themes

## -- Build Packages -----------------------------------------------------------
## Each package should contain a) your game files, b) files for the package's
## intended platforms, and for non-mobile packages, c) the Ren'Py engine files.
##
## Here are Ren'Py's built-in package types and what they contain:
##
## 0. "pc" (zip) for Windows 32-bit and Linux 32-/64-bit
## 1. "linux" (tar.bz2) for Linux 32-/64-bit
## 2. "mac" (app-zip, app-dmg) for Macintosh 64-bit
## 3. "win" (zip) for Windows 32-bit
##
## 4. "market" (zip) for Windows, Mac, and Linux
## 5. "steam" (zip) for all platforms, (deprecated in 6.99.13)
##
## 6. "android" (directory) for Android/Chrome OS (hidden, DLC)
## 7. "ios" (directory) for iPhones/iPads (hidden, DLC)
##
## 8. "web" (zip) HTML5 for websites/Newgrounds/itch.io (DLC)

init python:

    build.packages[0]["formats"] = ["directory"]
    build.packages[2]["formats"] = ["app-directory"]

    ## --- x86 Files
    ## Whether to include libraries to run on 32-bit processors for Linux/Mac.
    build.include_i686 = True
