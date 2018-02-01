#! /bin/bash
echo NOMYPY=$NOMYPY
echo BACKPORT=$BACKPORT

if [ "x$BACKPORT" == "xtrue" ]
then
    export BP=,backport
else
	export BP=
fi

if [ "x$NOMYPY" == "x" ]
then
	pip install --upgrade appdirs chardet configr termwidth coverage python-coveralls coconut[mypy$BP]
else
	pip install --upgrade appdirs chardet configr termwidth coverage python-coveralls coconut[$BP]
fi
