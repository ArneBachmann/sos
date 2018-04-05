#! /bin/bash
echo NOMYPY=$NOMYPY

python -m pip install -U pip
if [ "x$NOMYPY" == "x" ]
then
    pip install -U appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut-develop[mypy,cPyparsing,jobs]
else
    pip install -U appdirs chardet configr "setuptools >= 20.8.1" termwidth coverage python-coveralls coconut-develop[cPyparsing,jobs]
fi

if [ "x$BACKPORT" == "xtrue" ]
then
    pip install -U enum34
fi