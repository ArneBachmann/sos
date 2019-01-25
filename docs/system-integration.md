# System integration #

## Windows Explorer ##

Execute the `explorer-integration.bat` file.
If you cannot run `regedit.exe` or `reg.exe` in your company, here is a workaround to make it work:
- Run `cmd.exe` with elevated rights (as admin)
- Run `psexec -i -s -d cmd.exe` in this shell
- In the newly opened shell, run `explore-integration.bat`
- Close shells


## Thunar integration (XFCE on Linux) ##

- Run `python thunar-integration.py`
- Close and reopen all Thunar windows
