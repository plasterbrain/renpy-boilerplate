<# .SYNOPSIS Tells Ren'Py to lint the game, then launches it in auto mode.
.DESCRIPTION
.NOTES Lint results are outputted to console and saved to lint.txt.
#>

$ProjectDir = "../../ProjectName"

Write-Host "Checking script for potential problems...";
renpy $ProjectDir lint "lint.txt" | Out-String

Get-Content -Path "lint.txt"; pause;

Write-Host "Auto-running the game.";
renpy $ProjectDir auto;
pause;
