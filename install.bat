
echo NOMYPY=%NOMYPY%
echo BACKPORT=%BACKPORT%

python -m pip install -U pip

if "%NOMYPY%" == "" (
    pip install -U appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls "coconut-develop[mypy,cPyparsing] <= 1.3.1.post0.dev20"
) else (
    pip install -U appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls "coconut-develop[cPyparsing] <= 1.3.1.post0.dev20"
)

if "%BACKPORT%" == "true" (
    pip install -U enum34
)
