#! /bin/bash
echo NOMYPY=$NOMYPY

if [ "x$NOMYPY" == "x" ]
then
	python setup.py clean build --mypy
else
	python setup.py clean build
fi
python setup.py test

if [ $? -eq 0 ]; then
  coverage run --branch --debug=sys --source=sos sos/tests.py --verbose && coverage html && coverage annotate sos/tests.py
  exit 0
else
  echo Python test exited with an error
  exit 1
fi
