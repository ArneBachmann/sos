
echo NOMYPY=%NOMYPY%

python -m pip install -U pip

if "%NOMYPY%" == "" (
    pip install -U appdirs chardet configr termwidth "coverage == 4.0.3" python-coveralls "typing >= '3.5' ; python_version < '3.5'" "enum34 ; python_version < '3.4'"
    rem "setuptools >= 20.8.1" coconut-develop[mypy,cPyparsing]
) else (
    pip install -U appdirs chardet configr termwidth "coverage == 4.0.3" python-coveralls "typing >= '3.5' ; python_version < '3.5'" "enum34 ; python_version < '3.4'"
    rem "setuptools >= 20.8.1" coconut-develop[cPyparsing]
)
