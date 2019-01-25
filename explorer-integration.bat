@echo off

rem Folder interactions
reg delete "HKCR\Directory\shell\SOS Offline" /f /va
reg delete "HKCR\Directory\shell\SOS Changes" /f /va
reg delete "HKCR\Directory\shell\SOS Commit" /f /va
reg delete "HKCR\Directory\shell\SOS Diff" /f /va
reg delete "HKCR\Directory\shell\SOS Log" /f /va
reg delete "HKCR\Directory\shell\SOS Status" /f /va
reg add "HKCR\Directory\shell\SOS Changes\command" /t REG_SZ /d "cmd.exe /C echo SOS changes \"%%1\" & cd \"%%1\" & sos changes & pause" /f
reg add "HKCR\Directory\shell\SOS Changes" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\shell\SOS Changes" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\shell\SOS Commit\command" /t REG_SZ /d "cmd.exe /C echo SOS commit \"%%1\" & cd \"%%1\" & echo CTRL+C to abort. & timeout /t 10 && sos commit & pause" /f
reg add "HKCR\Directory\shell\SOS Commit" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\shell\SOS Commit" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & cd \"%%1\" & sos diff & pause" /f
reg add "HKCR\Directory\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\shell\SOS Log\command" /t REG_SZ /d "cmd.exe /C echo SOS log \"%%1\" & cd \"%%1\" & sos log --changes -n 5 & pause" /f
reg add "HKCR\Directory\shell\SOS Log" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\shell\SOS Log" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\shell\SOS Offline\command" /t REG_SZ /d "cmd /C echo SOS offline \"%%1\" & cd \"%%1\" && sos offline --strict --progress && sos config set useChangesCommand on --quiet & pause" /f
reg add "HKCR\Directory\shell\SOS Offline" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\shell\SOS Offline" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\shell\SOS Status\command" /t REG_SZ /d "cmd.exe /C echo SOS status \"%%1\" & cd \"%%1\" & sos status & pause" /f
reg add "HKCR\Directory\shell\SOS Status" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\shell\SOS Status" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f


rem Explorer window empty area interactions
reg delete "HKCR\Directory\Background\shell\SOS Offline" /f /va
reg delete "HKCR\Directory\Background\shell\SOS Changes" /f /va
reg delete "HKCR\Directory\Background\shell\SOS Commit" /f /va
reg delete "HKCR\Directory\Background\shell\SOS Diff" /f /va
reg delete "HKCR\Directory\Background\shell\SOS Log" /f /va
reg delete "HKCR\Directory\Background\shell\SOS Status" /f /va
reg add "HKCR\Directory\Background\shell\SOS Changes\command" /t REG_SZ /d "cmd.exe /C echo SOS changes \"%%1\" & cd \"%%1\" & sos changes & pause" /f
reg add "HKCR\Directory\Background\shell\SOS Changes" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\Background\shell\SOS Changes" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\Background\shell\SOS Commit\command" /t REG_SZ /d "cmd.exe /C echo SOS commit \"%%1\" & cd \"%%1\" & echo CTRL+C to abort. & timeout /t 10 && sos commit & pause" /f
reg add "HKCR\Directory\Background\shell\SOS Commit" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\Background\shell\SOS Commit" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\Background\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & cd \"%%1\" & sos diff & pause" /f
reg add "HKCR\Directory\Background\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\Background\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\Background\shell\SOS Log\command" /t REG_SZ /d "cmd.exe /C echo SOS log \"%%1\" & cd \"%%1\" & sos log --changes -n 5 & pause" /f
reg add "HKCR\Directory\Background\shell\SOS Log" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\Background\shell\SOS Log" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\Background\shell\SOS Offline\command" /t REG_SZ /d "cmd /C echo SOS offline \"%%1\" & cd \"%%1\" && sos offline --strict --progress && sos config set useChangesCommand on --quiet & pause" /f
reg add "HKCR\Directory\Background\shell\SOS Offline" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\Background\shell\SOS Offline" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\Directory\Background\shell\SOS Status\command" /t REG_SZ /d "cmd.exe /C echo SOS status \"%%1\" & cd \"%%1\" & sos status --verbose & pause" /f
reg add "HKCR\Directory\Background\shell\SOS Status" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\Directory\Background\shell\SOS Status" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f


rem Desktop background interactions
rem %[HKEY_CLASSES_ROOT\DesktopBackground\shell\SOS Offline\command]
rem %[HKEY_CLASSES_ROOT\DesktopBackground\shell\SOS Commit\command]
rem %[HKEY_CLASSES_ROOT\DesktopBackground\shell\SOS Log\command]
rem %[HKEY_CLASSES_ROOT\DesktopBackground\shell\SOS Diff\command]


rem Single file commands
reg delete "HKCR\*\shell\SOS Diff" /f /va
reg delete "HKCR\*\shell\SOS Ignore" /f /va
rem add "HKCR\*\shell\SOS Commit File\command" /t REG_SZ /d "cmd.exe /C sos commit --only ""%1"" & pause" /f
reg add "HKCR\*\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & sos diff --classic --only \"%%1\" | TortoiseUDiff /p /title:\"%%1\"" /f
reg add "HKCR\*\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\*\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
reg add "HKCR\*\shell\SOS Ignore\command" /t REG_SZ /d "cmd.exe /C echo SOS ignore \"%%1\" & sos config add ignores \"%%1\" & pause" /f
reg add "HKCR\*\shell\SOS Ignore" /v Position /t REG_SZ /d Bottom /f
reg add "HKCR\*\shell\SOS Ignore" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f


rem Checking
rem reg query "HKCR\Directory\shell\SOS Offline\command"
