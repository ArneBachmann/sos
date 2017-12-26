echo NOMYPY=%NOMYPY%
if "%NOMYPY%" == "" (
	pip install --upgrade appdirs chardet configr wcwidth coverage python-coveralls coconut[mypy]
) else (
	pip install --upgrade appdirs chardet configr wcwidth coverage python-coveralls coconut 
)