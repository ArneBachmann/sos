#! /bin/bash
echo NOMYPY=$NOMYPY

python -m pip install -U pip
if [ "x$NOMYPY" == "x" ]
then
	pip install --upgrade appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut[mypy]
else
	pip install --upgrade appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut
fi
