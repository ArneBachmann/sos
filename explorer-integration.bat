@echo off
rem TODO add nested menu https://www.askvg.com/add-cascading-menus-for-your-favorite-programs-in-windows-7-desktop-context-menu/
rem TODO add script option for nested menu https://stackoverflow.com/questions/20449316/how-add-context-menu-item-to-windows-explorer-for-folders
rem HINT replace Directory with LibraryFolder to make this work in libraries

set remove=false
if "%1" == "uninstall" (
  set remove=true
)
if "%1" == "remove" (
  set remove=true
)
if "%1" == "install" (
  set install=true
)

set admin=false
if "%1" == "--admin" (
  set admin=true
) else (
  if "%2" == "--admin" (
    set admin=true
  ))

if "%remove%" == "true" (
	if "%admin%" == "true" (
		echo Remove for admin
		reg delete "HKCR\Directory\shell\SOS Offline" /f
		reg delete "HKCR\Directory\shell\SOS Changes" /f
		reg delete "HKCR\Directory\shell\SOS Commit" /f
		reg delete "HKCR\Directory\shell\SOS Diff" /f
		reg delete "HKCR\Directory\shell\SOS Log" /f
		reg delete "HKCR\Directory\shell\SOS Status" /f
		reg delete "HKCR\Directory\Background\shell\SOS Offline" /f
		reg delete "HKCR\Directory\Background\shell\SOS Changes" /f
		reg delete "HKCR\Directory\Background\shell\SOS Commit" /f
		reg delete "HKCR\Directory\Background\shell\SOS Diff" /f
		reg delete "HKCR\Directory\Background\shell\SOS Log" /f
		reg delete "HKCR\Directory\Background\shell\SOS Status" /f
		reg delete "HKCR\*\shell\SOS Diff" /f
		reg delete "HKCR\*\shell\SOS Ignore" /f
) else (
		echo Remove for user
		reg delete "HKCU\Software\Classes\Directory\shell\SOS Offline" /f
		reg delete "HKCU\Software\Classes\Directory\shell\SOS Changes" /f
		reg delete "HKCU\Software\Classes\Directory\shell\SOS Commit" /f
		reg delete "HKCU\Software\Classes\Directory\shell\SOS Diff" /f
		reg delete "HKCU\Software\Classes\Directory\shell\SOS Log" /f
		reg delete "HKCU\Software\Classes\Directory\shell\SOS Status" /f
		reg delete "HKCU\Software\Classes\Directory\Background\shell\SOS Offline" /f
		reg delete "HKCU\Software\Classes\Directory\Background\shell\SOS Changes" /f
		reg delete "HKCU\Software\Classes\Directory\Background\shell\SOS Commit" /f
		reg delete "HKCU\Software\Classes\Directory\Background\shell\SOS Diff" /f
		reg delete "HKCU\Software\Classes\Directory\Background\shell\SOS Log" /f
		reg delete "HKCU\Software\Classes\Directory\Background\shell\SOS Status" /f
		reg delete "HKCU\Software\Classes\*\shell\SOS Diff" /f
		reg delete "HKCU\Software\Classes\*\shell\SOS Ignore" /f
	)
)

if "%install%" == "true" (
	if "%admin%" == "true" (
		echo Install for admin
		reg add "HKCR\Directory\shell\SOS Changes\command" /t REG_SZ /d "cmd.exe /C echo SOS changes \"%%1\" & cd /D \"%%1\" && sos changes & pause" /f
		reg add "HKCR\Directory\shell\SOS Changes" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\shell\SOS Changes" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\shell\SOS Commit\command" /t REG_SZ /d "cmd.exe /C echo SOS commit \"%%1\" & cd /D \"%%1\" && echo CTRL+C to abort. & timeout /t 10 && sos commit & pause" /f
		reg add "HKCR\Directory\shell\SOS Commit" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\shell\SOS Commit" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & cd /D \"%%1\" && sos diff & pause" /f
		reg add "HKCR\Directory\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\shell\SOS Log\command" /t REG_SZ /d "cmd.exe /C echo SOS log \"%%1\" & cd /D \"%%1\" && sos log --changes -n 5 & pause" /f
		reg add "HKCR\Directory\shell\SOS Log" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\shell\SOS Log" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\shell\SOS Offline\command" /t REG_SZ /d "cmd /C echo SOS offline \"%%1\" & cd /D \"%%1\" && sos offline --strict --progress && sos config set useChangesCommand on --quiet & pause" /f
		reg add "HKCR\Directory\shell\SOS Offline" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\shell\SOS Offline" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\shell\SOS Status\command" /t REG_SZ /d "cmd.exe /C echo SOS status \"%%1\" & cd /D \"%%1\" && sos status & pause" /f
		reg add "HKCR\Directory\shell\SOS Status" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\shell\SOS Status" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\Background\shell\SOS Changes\command" /t REG_SZ /d "cmd.exe /C echo SOS changes \"%%1\" & cd /D \"%%1\" && sos changes & pause" /f
		reg add "HKCR\Directory\Background\shell\SOS Changes" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\Background\shell\SOS Changes" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\Background\shell\SOS Commit\command" /t REG_SZ /d "cmd.exe /C echo SOS commit \"%%1\" & cd /D \"%%1\" && echo CTRL+C to abort. & timeout /t 10 && sos commit & pause" /f
		reg add "HKCR\Directory\Background\shell\SOS Commit" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\Background\shell\SOS Commit" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\Background\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & cd /D \"%%1\" && sos diff & pause" /f
		reg add "HKCR\Directory\Background\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\Background\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\Background\shell\SOS Log\command" /t REG_SZ /d "cmd.exe /C echo SOS log \"%%1\" & cd /D \"%%1\" && sos log --changes -n 5 & pause" /f
		reg add "HKCR\Directory\Background\shell\SOS Log" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\Background\shell\SOS Log" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\Background\shell\SOS Offline\command" /t REG_SZ /d "cmd /C echo SOS offline \"%%1\" & cd /D \"%%1\" && sos offline --strict --progress && sos config set useChangesCommand on --quiet & pause" /f
		reg add "HKCR\Directory\Background\shell\SOS Offline" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\Background\shell\SOS Offline" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\Directory\Background\shell\SOS Status\command" /t REG_SZ /d "cmd.exe /C echo SOS status \"%%1\" & cd /D \"%%1\" && sos status --verbose & pause" /f
		reg add "HKCR\Directory\Background\shell\SOS Status" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\Directory\Background\shell\SOS Status" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		rem add "HKCR\*\shell\SOS Commit File\command" /t REG_SZ /d "cmd.exe /C sos commit --only ""%1"" & pause" /f
		reg add "HKCR\*\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & sos diff --classic --only \"%%1\" --quiet | TortoiseUDiff /p /title:\"%%1\"" /f
		reg add "HKCR\*\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\*\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCR\*\shell\SOS Ignore\command" /t REG_SZ /d "cmd.exe /C echo SOS ignore \"%%1\" & sos config add ignores \"%%1\" & pause" /f
		reg add "HKCR\*\shell\SOS Ignore" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCR\*\shell\SOS Ignore" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
	) else (
		echo Install for user
		reg add "HKCU\Software\Classes\Directory\shell\SOS Changes\command" /t REG_SZ /d "cmd.exe /C echo SOS changes \"%%1\" & cd /D \"%%1\" && sos changes & pause" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Changes" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Changes" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Commit\command" /t REG_SZ /d "cmd.exe /C echo SOS commit \"%%1\" & cd /D \"%%1\" && echo CTRL+C to abort. & timeout /t 10 && sos commit & pause" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Commit" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Commit" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & cd /D \"%%1\" && sos diff & pause" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Log\command" /t REG_SZ /d "cmd.exe /C echo SOS log \"%%1\" & cd /D \"%%1\" && sos log --changes -n 5 & pause" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Log" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Log" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Offline\command" /t REG_SZ /d "cmd /C echo SOS offline \"%%1\" & cd /D \"%%1\" && sos offline --strict --progress && sos config set useChangesCommand on --quiet & pause" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Offline" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Offline" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Status\command" /t REG_SZ /d "cmd.exe /C echo SOS status \"%%1\" & cd /D \"%%1\" && sos status & pause" /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Status" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\shell\SOS Status" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f

		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Changes\command" /t REG_SZ /d "cmd.exe /C echo SOS changes \"%%1\" & cd /D \"%%1\" && sos changes & pause" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Changes" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Changes" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Commit\command" /t REG_SZ /d "cmd.exe /C echo SOS commit \"%%1\" & cd /D \"%%1\" && echo CTRL+C to abort. & timeout /t 10 && sos commit & pause" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Commit" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Commit" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & cd /D \"%%1\" && sos diff & pause" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Log\command" /t REG_SZ /d "cmd.exe /C echo SOS log \"%%1\" & cd /D \"%%1\" && sos log --changes -n 5 & pause" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Log" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Log" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Offline\command" /t REG_SZ /d "cmd /C echo SOS offline \"%%1\" & cd /D \"%%1\" && sos offline --strict --progress && sos config set useChangesCommand on --quiet & pause" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Offline" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Offline" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Status\command" /t REG_SZ /d "cmd.exe /C echo SOS status \"%%1\" & cd /D \"%%1\" && sos status --verbose & pause" /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Status" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\Directory\Background\shell\SOS Status" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		rem add "HKCU\Software\Classes\*\shell\SOS Commit File\command" /t REG_SZ /d "cmd.exe /C sos commit --only ""%1"" & pause" /f
		reg add "HKCU\Software\Classes\*\shell\SOS Diff\command" /t REG_SZ /d "cmd.exe /C echo SOS diff \"%%1\" & sos diff --classic --only \"%%1\" --quiet | TortoiseUDiff /p /title:\"%%1\"" /f
		reg add "HKCU\Software\Classes\*\shell\SOS Diff" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\*\shell\SOS Diff" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
		reg add "HKCU\Software\Classes\*\shell\SOS Ignore\command" /t REG_SZ /d "cmd.exe /C echo SOS ignore \"%%1\" & sos config add ignores \"%%1\" & pause" /f
		reg add "HKCU\Software\Classes\*\shell\SOS Ignore" /v Position /t REG_SZ /d Bottom /f
		reg add "HKCU\Software\Classes\*\shell\SOS Ignore" /v Icon /t REG_SZ /d "%CD%\extras\logo.ico" /f
	)
)


rem Desktop background interactions - add later
rem %[HKEY_CLASSES_ROOT\DesktopBackground\shell\SOS Offline\command]
rem %[HKEY_CLASSES_ROOT\DesktopBackground\shell\SOS Commit\command]
rem %[HKEY_CLASSES_ROOT\DesktopBackground\shell\SOS Log\command]
rem %[HKEY_CLASSES_ROOT\DesktopBackground\shell\SOS Diff\command]

echo Finished.
