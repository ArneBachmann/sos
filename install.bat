
echo NOMYPY=%NOMYPY%
echo BACKPORT=%BACKPORT%

python -m pip install -U pip

if "%NOMYPY%" == "" (
    pip install -U appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut-develop[mypy,cPyparsing]
) else (
    pip install -U appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut-develop[cPyparsing]
)

if "%BACKPORT%" == "true" (
    pip install -U enum34
)
