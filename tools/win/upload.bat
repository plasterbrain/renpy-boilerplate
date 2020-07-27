:: Name:      upload.bat
:: Purpose:   Runs commands to push your game to Itch and Steam.
:: Author:    Plasterbrain, unless it doesn't work, then it wasn't me
:: Version:   0.0.0
Title "Pushing to itch.io and Steam"

set steamworks=C:\\steamworks\ContentBuilder
set steamlogin=username
set steampass=password
set appscript=app.vdf
set builddir=ProjectName
set buildexe=ProjectName
set itchdry=--dry-run
set itchname=Username/ProjectName

:: (Steam) All Builds
%steamworks%\builder\steamcmd.exe +login %steamlogin "%steampass%" +run_app_build "%steamworks%\scripts\%appscript%"

:: (Itch) Windows Build
butler push %itchdry% "%steamworks%\content\%builddir%" --ignore "%buildexe%.app" --ignore "linux-i686" --ignore "linux-x86_64" --ignore "%buildexe%.sh" --ignore "steam_appid.txt" --ignore "developer" %itchname%:win

:: (Itch) Linux Build
butler push %itchdry% "%steamworks%\content\%builddir" --fix-permissions --ignore --ignore "windows-i686" --ignore "%buildexe%.exe" --ignore "steam_appid.txt" --ignore "developer" %itchname%:linux

:: (Itch) Mac OS Build
butler push %itchdry% "%steamworks%\content\%builddir%\%buildexe%.app" --fix-permissions --ignore "steam_appid.txt" %itchname%:osx
