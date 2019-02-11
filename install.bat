
echo NOMYPY=%NOMYPY%

rem Requirement for Python 3.4 compatibility is to use pip < 19.0 as 19.0+ will raise a deprecation warning
python -m pip install -U "pip < 19.0"

rem Workaround for conda problems with pip 19.0 vs. Python 3.4
set PIP_NO_BUILD_ISOLATION=False
set PIP_USE_PEP517=False

if "%NOMYPY%" == "" (
    pip install -U appdirs chardet configr termwidth "coverage == 4.0.3" python-coveralls "typing >= '3.5'; python_version < '3.5'" "enum34; python_version < '3.4'" "setuptools == 30.1.0; python_version == '3.4'"
    rem "setuptools >= 20.8.1" coconut-develop[mypy,cPyparsing]
) else (
    pip install -U appdirs chardet configr termwidth "coverage == 4.0.3" python-coveralls "typing >= '3.5'; python_version < '3.5'" "enum34; python_version < '3.4'" "setuptools == 30.1.0; python_version == '3.4'"
    rem "setuptools >= 20.8.1" coconut-develop[cPyparsing]
)
exit /b 0