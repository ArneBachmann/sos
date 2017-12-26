#! /bin/bash
echo NOMYPY=$NOMYPY
if [ "x$NOMYPY" == "x" ]
then
	pip install appdirs chardet configr wcwidth coverage python-coveralls coconut 
else
	pip install appdirs chardet configr wcwidth coverage python-coveralls coconut[mypy]
fi