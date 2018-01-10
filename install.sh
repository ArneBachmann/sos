#! /bin/bash
echo NOMYPY=$NOMYPY
if [ "x$NOMYPY" == "x" ]
then
	pip install --upgrade appdirs chardet configr wcwidth coverage python-coveralls coconut[mypy]
else
	pip install --upgrade appdirs chardet configr wcwidth coverage python-coveralls coconut
fi