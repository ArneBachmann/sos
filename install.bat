echo NOMYPY=%NOMYPY%
echo BACKPORT=%BACKPORT%

if "%BACKPORT%" == "true" (
	set BP=backport,
) else (
    set BP=
)

if "%NOMYPY%" == "" (
	pip install --upgrade appdirs chardet configr termwidth coverage python-coveralls coconut[%BP%mypy]
) else (
	pip install --upgrade appdirs chardet configr termwidth coverage python-coveralls coconut[%BP%]
)
