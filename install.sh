#! /bin/bash
echo NOMYPY=$NOMYPY

python -m pip install -U pip
if [ "x$NOMYPY" == "x" ]
then
    pip install -U appdirs chardet configr termwidth python-coveralls "typing >= '3.5', python_version < '3.5'" "enum34, python_version < '3.4'"
    # "setuptools >= 20.8.1" coconut-develop[mypy,cPyparsing,jobs]
else
    pip install -U appdirs chardet configr termwidth python-coveralls "typing >= '3.5', python_version < '3.5'" "enum34, python_version < '3.4'"
    # "setuptools >= 20.8.1" coconut-develop[cPyparsing,jobs]
fi
