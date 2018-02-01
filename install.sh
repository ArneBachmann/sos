#! /bin/bash
echo NOMYPY=$NOMYPY

python -m pip install -U pip
if [ "x$NOMYPY" == "x" ]
then
	pip install -U appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut[mypy]
else
	pip install -U appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut
fi
