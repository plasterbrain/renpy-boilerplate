:: Name:      upload.bat
:: Purpose:   Runs commands to push your game to Itch and Steam.
:: Author:    Plasterbrain, unless it doesn't work, then it wasn't me
:: Version:   0.0.0
Title "Pushing to itch.io and Steam"

set steamworks=C:\\steamworks\ContentBuilder\Content
set steamlogin=username
set steampass=password
set steamscript=app.vdf
set itchbuilddir=ProjectName
set itchbuildexe=ProjectName
set itchdry=--dry-run
set itchname=Username/ProjectName

:: (Steam) All Builds
%steamworks%\builder\steamcmd.exe +login %steamlogin "%steampass%" +run_app_build "%steamworks%\scripts\%steamscript%"

:: (Itch) Windows Build
butler push %itchdry% "%steamworks%\%itchbuilddir%" --ignore "%itchbuildexe%.app" --ignore "linux-i686" --ignore "linux-x86_64" --ignore "%itchbuildexe%.sh" --ignore "steam_appid.txt" --ignore "developer" %itchname%:win

:: (Itch) Linux Build
butler push %itchdry% "%steamworks%\%itchbuilddir" --fix-permissions --ignore --ignore "windows-i686" --ignore "%itchbuildexe%.exe" --ignore "steam_appid.txt" --ignore "developer" %itchname%:linux

:: (Itch) macOS Build
butler push %itchdry% "%steamworks%\%itchbuilddir%\%itchbuildexe%.app" --fix-permissions --ignore "steam_appid.txt" %itchname%:osx
