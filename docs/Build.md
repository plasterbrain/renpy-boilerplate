# Building your game (*devtools/dev_build.rpy*)
Hi, sorry, this step is surprisingly difficult. Much of the content in this section comes from my own experience. For reference, this project template and documentation only covers distributing PC/Linux builds and builds for pre-Catalina Mac, as this is what I actually have experience with.

## Setting up distribution builds for fun and profit
The game will be separated into various depots (components), which can be selectively uploaded and downloaded via itch.io/Steam to provide players with the right content.

First, we will be building the game with the *developer* folder in-tact, so that you'll have access to those tools when testing a compiled version of the game.

Second, we'll build two packages, the "PC" and "Mac" ones Ren'Py has already made. While "Markets" includes the files for all three platforms, building this way causes the Mac app not to have a *Contents/Resources/autorun* directory, instead relying on the directories at the same level as the executable, like the Windows/Linux versions do. This is a little awkward for Mac users and also I'm not sure if it works with notarization.

We'll then classify the platform-specific content in various depots to reduce the overall download size. (Excluding the Python libs for other platforms saves like 40mb.)

If you receive email newsletters from any form of indie software company, you probably already know that the latest version of Mac OS, Catalina (10.15) will only run apps that are [notarized](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution). Notarization is a tedious and programmy process that requires a Mac as well as a $99 annual Apple Developer subscription.

"That sucks! How do I get around it?!" you may ask. On itch.io, you are welcome to ignore this requirement and put up a non-notarized Mac version for Mojave (10.14) and earlier. However, this isn't possible on Steam, which as of mid-October 2019 requires Catalina-compatiblity for games to be listed as available on Mac.

Resources
- [Steam hardware survey](https://store.steampowered.com/hwsurvey)
- [Notarizing Mac Applications](https://www.patreon.com/posts/30297261)
- [Ren'Py Distribution Tools (RDT)](https://github.com/UnscriptedVN/rdt)
- [Notarizing your Flash/AIR applications for macOS](https://www.molleindustria.org/blog/notarizing-your-flashair-applications-for-macos/) (the information is pretty generalized)
- [Ren'Py docs: Android](https://www.renpy.org/doc/html/android.html)
- [Ren'Py docs: ChromeOS](https://www.renpy.org/doc/html/chromeos.html)
- [Itch Uploading GUI](https://blendogames.itch.io/blendo-itch-uploader)
- [Itch brand assets and guidelines](https://itch.io/press-kit)
- [Apple branding guidelines](https://developer.apple.com/app-store/marketing/guidelines/) for games releasing on the App Store

### Distributing to the Google Play Store
To add Google Play in-app purchases or if the size of your build exceeds 100MB, you'll need a [Google Play publisher account](https://support.google.com/googleplay/android-developer/answer/6112435). Registration is $25, and you must be at least 18 years old.

## Preparing to build
### Step 1. Project cleanup

The only things that should be in your base project directory are:
- Files actually needed for your game.
  - (Ren'Py will add its own engine files when you compile a build.)
- Files used for your manual.
- Launch configuration files (*.itch.toml*, *steam_appid.txt*, etc.)

Everything else should be either moved out of the project directory or ignored in the Ren'Py build file classification, as explained below.

### Step 2. Build settings
- `build.name` is the name of your project, without spaces.
- `build.executable_name` will be used to set the name of the *.app*, *.exe*, and *.sh* files that launch your game on various platforms.
- `build.directory_name` is the name of your build folder, defualt  "{build.name}-{build.version}-{build.package}."
- `build.version` is set to config.version by default. This is used as part of the folder name if build.directory_name is not set, for generating the *Info.plist* file on Mac builds, and for building updates for the web updater.
  - If you are distributing on Mac, `build.version` is used for *Info.plist*'s **CFBundleShortVersionString**, and is visible to users. It needs to be in semantic version format (e.g., 1.2.3).
  - In either case, this variable probably should not have spaces or special characters in it.

These guidelines assume you're compiling builds using Ren'Py from the command line (which has a **--dest** flag to set the build destination). If you want to use the Ren'Py launcher instead, and to specify the name of the folder where the builds go, use `build.destination`.

#### Mac-exclusive build settings
- `build.display_name` is the app display name on Mac. You can remove it if you're not building for Mac.
- `build.allow_integrated_gpu` sets the value of **NSSupportsAutomaticGraphicsSwitching** in the *Info.plist* file.

### Step 3. Classifying files
To decide what to build and what to leave behind, we need to use `build.classify()`.

#### Platform-exclusive files
If you have script files of some kind that pertain only to certain platforms or operating systems, you can classify those files into the "mac", "windows", "linux", and "android" lists.

You can also make your own lists, in addition to these, but if you're doing this to exclude, say, Itch- and Steam-specific files, it's much easier to make one game build including everything and then tell the Itch and Steam upload tools to ignore the irrelevant files.

An exception to this would be cases where your only way of pushing builds for distribution is by uploading a zip folder. But, like, that shouldn't be the case, because that sucks.

##### What about DLC?
If you are uploading somewhere using *zip* files like a lame-o, you'll need to classify DLC-exclusive files into their own list, like "bonus_episode".

For products that are not entirely separate games (like episodes or DLC routes), Steam is your best distribution option. Itch and the like don't really have built-in systems for managing DLC.

Fortunately, with Steam, you can forego making separate file lists and packages for DLC entirely. Once configured, this approach may be simpler when it comes to organizing distribution files on your computer. (The downside is you will have to rebuild the entire game even if you only update the DLC. :) )

1. Put all your DLC content in one or more subfolders.
1. Configure the command line tools (as shown later on) to exclude the DLC subfolder(s) from your main game package.
1. Configure a depot for the DLC that points to the DLC subfolder.

Itch could theoretically work this way too, but you'll probably need to give your users installation instructions.

#### Ignored files
If there are any files you want in your project directory but do not want in the distributed version of the game, you can classify their file patterns as None. A good example is *game/embarrassing-porn-collection-i-use-to-destress-after-spending-hours-programming.tar.bz*. You definitely don't want that file in the compiled build.

The current build file is set to ignore Git versioning stuff, OS-generated files, and unused template stuff.

1. There's a commented out line there to ignore uncompiled *.rpy* scripts. Once you do a test build to make sure your file patterns are working properly, you may want to uncomment it. Ignoring *.rpy* files means users won't be able to poke around and edit the files of your compiled build without first using a tool like unrpyc.
1. Ren'Py has various file patterns it ignores by default, including all the various error and log *txt* files it may have generated for you during development.
1. Remember, we're keeping *devtools* and *testers* for now, to a) double-check that the compiled build runs okay and b) give beta testers console access.
1. Do not exclude *version.txt* if you are reading it to populate `config.version`.

#### Archives (.rpa)
Archives keep your files sort of secret by packing lots of files and folders into one *something.rpa*. They are an optional feature.

To archive files, first classify them into a custom list -- not one of Ren'Py's built-in file lists. This will appear as the name of your archive. Second, use `build.archive()` to determine what file lists that archive appears on. This will usually be "all", but if you wanted to, for example, package *bonus.rpa* in your Windows builds, you could write:
```python
## Step 1
build.classify("game/images/windows_memes/**", "win_bonus")
## Step 2
build.archive("win_bonus", "windows")
```

Try it out!
1. Right now, the lines to archive all game files under *game.rpa* are there, but commented. This is because you may want to try a test build first, without archives, to see if your file patterns worked as intended.
1. Do not archive the *devtools* or *testers* folders themselves, if you are following my super-cool build plan. The Steam/Itch upload scripts will be pattern matching based on the existence of those folders. The content inside them can be archived, though there's not really a reason to do it.
1. If you are using the [game manual and license pages](/Manual) included in this project template, <u>do not</u> archive any of these files, or anything in the *help* folder, or your manual <u>will not work</u>. (#BeenThere.)

### Step 4. Defining packages
Build packages associate file lists and build properties with platforms.

@TODO I don't know if notarizing Mac apps requires them to be zipped and/or to not have any of that Windows/Linux nonsense sitting in the same directory.

For distribution on Steam, Itch, and the like via command line, your game build should be a regular folder, and [not a zipped archive](https://itch.io/docs/butler/single-files.html).

If you're not using a command line tool to exclude DLC content, you can make a DLC package like this:

```python
build.package("bonus", "", "bonus_scripts bonus_media", "Bonus Episode", dlc=True)
```
1. "bonus" is the Pythonic name of the package.
1. The second parameter (package format) should be empty for DLC.
1. "bonus_episode" is a string of all the file lists that make up this DLC, separated by space.
1. "Bonus Episode" is the name of the package in the launcher, for your reference.

## Building the game
Use *tools/build.bat* to build from the command line.

## Uploading your game

If you run the game after building, the usual log, persistent, and cache files will be generated. The various build scripts are set to ignore these, just in case.

1. Set both instances of `BUILD_DIRECTORY` to point to your compiled build directory.
1. Update `USERNAME` and `PROJECT` to match your username and project slug on Itch.
1. Edit `CHANNEL` as appropriate, using [Itch's channel name formatting](https://itch.io/docs/butler/pushing.html#channel-names). For example, if you're pushing the demo version of your game for Windows, you could use "win-demo". Setting the right channel allows Itch to mark your build for the appropriate platforms automatically.
1. To [ignore files](https://itch.io/docs/butler/pushing.html#appendix-c-ignoring-files), add `--ignore "*.txt"` to this code, where the part in brackets is a file pattern to ignore. You'll need to add a new flag like this for every file pattern you want to exclude. Add the `--dry-run` flag to do a test push, which shows you what files would be uploaded to Itch.

### Steampipe
WELCOME TO HELL WORLD

- (APP ID) For your game.
- (WINDOWS DEPOT ID) Windows build
- (LINUX DEPOT ID) Linux build
- (MAC DEPOT ID) Notarized Mac build
- Steamworks SDK downloaded

Move the scripts in *tools* to *{STEAMWORKS}/ContentBuilder/scripts*.

Your first time pushing to Steam, you should run these scripts once with "preview" (that's in *app_example.vdf*) set to "1" so you can double check which files will actually be uploaded. Set it to "0" to push the build for real. The script will set the build live on the *beta* branch right away.
