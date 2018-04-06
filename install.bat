
echo NOMYPY=%NOMYPY%
echo BACKPORT=%BACKPORT%

python -m pip install -U pip

if "%NOMYPY%" == "" (
    pip install -U appdirs chardet configr termwidth coverage python-coveralls "typing >= '3.5' ; python_version < '3.5'"
	rem "setuptools >= 20.8.1" coconut-develop[mypy,cPyparsing]
) else (
    pip install -U appdirs chardet configr  termwidth coverage python-coveralls "typing >= '3.5' ; python_version < '3.5'"
    rem "setuptools >= 20.8.1" coconut-develop[cPyparsing]
)

if "%BACKPORT%" == "true" (
    pip install -U enum34
)
