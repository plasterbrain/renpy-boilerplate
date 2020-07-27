# Tools
NOTE: The scripts in the *tools/win* folder and the example configuration files are based on scripts I have used successfully in the past, but haven't tested in their current form (i.e. with everything abstracted to variables and a new relative folder structure).

### Config Files
The *tools* folder has some starting config files to help you build and upload your game.

#### *.vdf* files
These are configuration files for uploading games to Steam, using Valve's ad-hoc "KeyValue" format. There's one for your overall game ("app") and one for each of your platform-specific file lists ("depots").

You should edit these and replace stuff marked in braces with the appropriate text. For example, "{build.directory_name}" should be replaced with "ProjectName", or probably whatever your build directory is actually called.

#### *entitlements.plist*
Not tested. A starter entitlements configuration if you're notarizing your game on Mac. It contains some security allowances you'll probably need:
- `disable-library-validation` and `allow-dyld-environment-variables` are required by Steamworks SDK.
- `allow-unsigned-executable-memory` is required by Python.

### Windows Scripts

The template comes with some scripts to aid in the development, testing, and build process on Windows by calling Ren'Py and other programs from the command line.

Some of the batch scripts have corresponding Powershell files. On my system Ren'Py throws a missing lib error when launched from the Command Prompt, but nto from Powershell. The *bat* scripts are required though because, for security reasons, *.ps1* scripts can't be launched with a double-click.

For most of these you'll need Ren'Py [added to your PATH variable](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/), or you'll have to change where it says "renpy" to point to the Ren'Py executable on your computer.

#### *launch*
Launches the uncompiled game. Normally this is only possible if your project folder is in the Ren'Py launcher's chosen "projects" directory. You should keep this script on the same level as the *ProjectName* folder.

Edit *launch.ps1* to match the name of your base project directory, since by default it points to "ProjectName."

#### *reset*
Deletes the game's persistent data from both *game/saves* and the app data save location. Normally this is only possible if your project folder is in the Ren'Py launcher's chosen "projects" directory. You should keep this script on the same level as the *ProjectName* folder.

Edit *reset.ps1* to match the name of your base project directory, since by default it points to "ProjectName."

#### *tools/../debug*
Lints the game, then launches it in "auto" mode (using a command created in *dev_tools.rpy*). The lint results should be saved to *lint.txt* and outputted in the console window.

Edit *debug.ps1* to match the relative path of your base project directory, since by default it points to "ProjectName."

#### *tools/../build*
Builds the "pc" and "mac" packages for your game using Ren'Py. By default these are thrown into the Steamworks Content Builder "content" folder. Then it renames the output directories for your builds and moves files around so that they are all available in one directory, `build.directory_name`. This effectively mimics the output of building the "market" package but includes a copy of the necessary game files in the Mac app's *autorun* folder, allowing you to distribute the *.app* file by itself.

Edit the variables at the top of *build.ps1* to match your project configuration and point to the correct folders on your machine.

#### *tools/../upload.bat*
Attempts to upload the game to itch.io and Steam. By default, the script will perform a dry run on all of these, meaning it will show you what files would be uploaded without actually doing anything. Once you've done  a test run of this script, you can change `itchdry` to an empty string (and set "preview" to "0" in *app.vdf*) to upload your files for real. On Steam they will not be pushed live to the main download branch until you manually approve the upload online, but on itch.io your changes will be live immediately, so be careful!

Edit the variables at the top of *upload.bat* to match your project configuration and Steam/itch.io information, and point to the correct folders on your machine.

This script assumes you have Steamworks SDK downloaded and Itch's upload utility, [butler](https://itch.io/docs/butler/installing.html), installed and added to your PATH.

### Linux Scripts
If you have Linux installed as a substytem on Windows, you can open the Linux shell in this directory and run these scripts.

#### *tools/../convert-png.sh*
Converts images in the current directory and sub-directories from *.png* to *.webp* format. Use this to drastically cut down on your game's size! The newly converted images will initially appear as *{filename}.png.webp*, Once the script is done converting them all, it will fix the names to just be *{filename}.webp*.

Finally, you'll be prompted to confirm whether you want to delete your old images. Remember to look through the new images to make sure you're happy with them. Alternatively, you may want to copy your images to a backup before running the conversion script.

This script assumes you have [cwebp](https://developers.google.com/speed/webp/download) installed. Then drop it in your images folder, give the script execute permission (`chmod +x ./convert-png.sh`), run it, and then grab a cup of coffee while you wait.

#### *tools/../convert-jpg.sh*
Same as the above, but with *.jpg* files and using lossy conversion.
