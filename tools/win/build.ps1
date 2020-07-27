<# .SYNOPSIS Tells Ren'Py to create PC/Mac builds and reorganizes the output.
.DESCRIPTION
.NOTES The resulting files are moved to one folder, build.directory_name.
#>

$Steamworks = "c://steamworks/tools/ContentBuilder/Content"
$Renpy = "c://Program Files/RenPy/launcher"
$ProjectDir = "../../ProjectName"
$BuildDir = "ProjectName"
$BuildExe = "ProjectName"

Write-Host "Building your game...";
renpy $Renpy distribute $ProjectDir --dest $Steamworks --package "pc" --no-update | Out-String

renpy $Renpy distribute $ProjectDir --dest $Steamworks --package "mac" --no-update | Out-String

Rename-Item "$Steamworks/$BuildDir-pc" "$Steamworks/$BuildDir" | Out-String

Move-Item -Path "$Steamworks/$BuildDir-mac-app/$BuildExe.app" -Destination "$Steamworks/$BuildDir" | Out-String
Remove-Item "$Steamworks/$BuildDir-mac-app" -Recurse | Out-String

ii $Steamworks
pause;
