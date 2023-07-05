<# .SYNOPSIS Removes a game's persistent data without using the Ren'Py launcher.
.DESCRIPTION A script using Ren'Py to remove both persistent data files from the command line. This is useful if you need to delete persistent data but only want to click two times instead of like seven.
#>

# Change "ProjectName" to the name of your game folder.
renpy "ProjectName" rmpersistent
