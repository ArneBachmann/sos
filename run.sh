#! /bin/bash
echo NOMYPY=$NOMYPY
if [ "x$NOMYPY" == "x" ]
then
	python setup.py clean build test
else
	python setup.py clean build test --mypy
fi
coverage run --branch --debug=sys --source=sos sos/tests.py && coverage html && coverage annotate sos/tests.py