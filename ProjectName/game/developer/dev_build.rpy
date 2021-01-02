################################################################################
## Developer: Build Settings
################################################################################
## Ren'Py includes support for building game distributions.

#-- Build Settings -------------------------------------------------------------

init python:

    ## ---! Build Name
    ## Used in case some of the below values are missing. No special characters.
    build.name = "ProjectName"

    ## ---! Executable Name
    ## Name of the executable file. No special characters. If not set, this will default to `build.name`. `CFBundleExecutable` is set to this value.
    build.executable_name = "ProjectName"

    ## ---! Directory Name
    ## Name for the final dist package zip/directory. If not set, this will
    ## default to something like "projectname-1.0.0". No special characters.
    ## The package name gets appended to it, e.g. "projectname-1.0.0-win."
    build.directory_name = "ProjectName"

    ## ---! Version
    ## The version of your game. If you are distributing to Mac, this must be
    ## semver format (e.g., "1.2.3").
    build.version = config.version

## -- Mac/iOS ------------------------------------------------------------------

init python:

    ## ---! Mac PLIST CFBundleDisplayName
    ## Visible to users and used by Siri. `CFBundleDisplayName` and
    ## `CFBundleName` are set to this value.
    build.display_name = config.name

    ## --- Mac Automatic Graphics Switching
    ## Whether the program should use the integrated GPU. Sets
    ## `NSSupportsAutomaticGraphicsSwitching` to True.
    build.allow_integrated_gpu = True
	
	build.mac_info_plist = {
		"CFBundleDisplayName": build.display_name,
		#"CFBundleSpokenName": "",
		#"CFBundleIdentifier": "com.you.game",
        "CFBundleShortVersionString": build.version,
		"CFBundleDevelopmentRegion": "en-US",
		"LSMinimumSystemVersion": "10.6.0",
        "LSApplicationCategoryType": "public.app-category.simulation-games",
		"NSHumanReadableCopyright": __("All rights reserved."),
	}

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
## 5. "steam" (zip) for all platforms, (hidden, deprecated in 6.99.13)
##
## 6. "android" (directory) for Android/Chrome OS (hidden, DLC)
## 7. "ios" (directory) for iPhones/iPads (hidden, DLC)
##
## 8. "web" (zip) HTML5 for websites/Newgrounds/itch.io (DLC)

init python:

    ## Change "PC" package to directory
    build.packages[0]["formats"] = ["directory"]
	## Change "Mac" package to directory
    build.packages[2]["formats"] = ["app-directory"]
