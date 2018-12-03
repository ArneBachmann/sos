echo NOMYPY=%NOMYPY%


if "%NOMYPY%" == "" (

	python setup.py clean build
  python test --mypy
) else (
	python setup.py clean build
  python setup.py test
)
if errorlevel 1 (
  echo Python test exited with an error
  exit 1
) else (
  coverage run --branch --debug=sys --source=sos sos/tests.py --verbose && coverage html && coverage annotate sos/tests.py
  exit 0
)
