
echo NOMYPY=%NOMYPY%

python -m pip install -U pip

if "%NOMYPY%" == "" (
	pip install --upgrade appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut[mypy]
) else (
	pip install --upgrade appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut
)
