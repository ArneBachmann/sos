#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xbc5dacb5

# Compiled with Coconut version 1.4.0-post_dev8 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get("__coconut__")
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules["__coconut__"]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_addpattern, _coconut_sentinel
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# Copyright Arne Bachmann
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import math  # line 4
if TYPE_CHECKING:  # line 5
    from typing import Any  # line 5
    from typing import FrozenSet  # line 5
    from typing import List  # line 5
    from typing import Tuple  # line 5

try:  # line 7
    import wcwidth  # optional dependency for unicode support  # line 8
    def wcswidth(string: 'str') -> 'int':  # line 9
        l = wcwidth.wcswidth(string)  # type: int  # line 10
        return len(string) if l < 0 else l  # line 11
except:  # line 12
    wcswidth = len  # type: _coconut.typing.Callable[[str], int]  # line 12

KIBI = 1 << 10  # type: int  # line 14
MEBI = 1 << 20  # type: int  # line 15
GIBI = 1 << 30  # type: int  # line 16

_SECOND = 1000  # type: int  # line 18
_MINUTE = _SECOND * 60  # type: int  # line 19
_HOUR = _MINUTE * 60  # type: int  # line 20
_DAY = _HOUR * 24  # type: int  # line 21
_WEEK = _DAY * 7  # type: int  # line 22


# "Pure" functions
@_coconut_tco  # line 26
def unzip(lizt: 'List[Tuple[Any]]') -> 'Tuple[List[Any]]':  # line 26
    return _coconut_tail_call(zip, *lizt)  # line 27

@_coconut_tco  # line 29
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 29
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 29

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl: 'str'="", first: 'bool'=True) -> 'str':  # line 31
    return ((sep if first else "") + (nl + sep).join(seq)) if seq else ""  # line 31

def requiredDecimalDigits(number: 'int') -> 'int':  # line 33
    return 1 if number <= 0 else int(math.floor(round(math.log(number, 10), 6)) + 1)  # line 34

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # Used to match only arguments, or use only stored patterns  # line 36
    return a & b if a else b  # Used to match only arguments, or use only stored patterns  # line 36

def getTermWidth() -> 'int':  # line 38
    try:  # line 39
        import termwidth  # line 39
    except:  # HINT could be factored out, or even increased for most modern systems  # line 40
        return 80  # HINT could be factored out, or even increased for most modern systems  # line 40
    return termwidth.getTermWidth()[0]  # line 41

# Global variable
termWidth = getTermWidth() - 1  # uses curses or returns conservative default of 80  # line 44

def ljust(string: 'str'="", width: 'int'=termWidth) -> 'str':  # line 46
    assert width > 0  # line 47
    return string + " " * max(0, width - wcswidth(string))  # line 48

def splitStrip(string: 'str') -> 'List[str]':  # line 50
    return [_.strip() for _ in string.replace("\r", "").split("\n")]  # line 50

def signedNumber(number: 'int', filled: 'bool'=False) -> 'str':  # line 52
    ''' Always returns the sign. '''  # line 53
    return "+" if number > 0 else ("-" if number < 0 else (" " if filled else ""))  # line 54

def siSize(size: 'int') -> 'str':  # line 56
    ''' Returns formatted number with SI unit. '''  # line 57
    return "%.2f MiB" % (float(size) / MEBI) if size > 1.25 * MEBI else ("%.2f KiB" % (float(size) / KIBI) if size > 1.25 * KIBI else ("%d bytes" % size))  # line 58

def timeString(timeMs: 'int') -> 'str':  # line 60
    ''' Returns formatted time with unit. '''  # line 61
    return "%.1f weeks" % (float(timeMs) / _WEEK) if timeMs > 8. * _WEEK / 7 else ("%.1f days" % (float(timeMs) / _DAY) if timeMs > 1.125 * _DAY else ("%.1f hours" % (float(timeMs) / _HOUR) if timeMs > 1.5 * _HOUR else ("%.1f minutes" % (float(timeMs) / _MINUTE) if timeMs > 1.5 * _MINUTE else ("%.1f seconds" % (float(timeMs) / _SECOND) if timeMs > 1.5 * _SECOND else ("%d ms" % timeMs)))))  # line 62

def median(values: 'List[Union[int, float]]', inplace: 'bool'=False):  # line 69
    ''' TODO Use doctest here.
  >>> print(median([1, 2, 3]))
  2
  >>> print(median([1, 2]))
  1.5
  '''  # line 75
    assert isinstance(values, list)  # line 76
    n = len(values)  # type: int  # line 77
    assert n > 0  # line 78
    if n == 1:  # line 79
        return values[0]  # line 79
    if inplace:  # line 80
        values.sort()  # line 80
    else:  # get copy  # line 81
        values = list(sorted(values))  # get copy  # line 81
    return values[n >> 1] if (n >> 1) << 1 != n else (values[(n >> 1) - 1] + values[(n >> 1)]) / 2.0  # line 82

def appendEndmarkerIterator(i: 'Iterable', end: 'Any'=lambda count, value: (count, value), endValue: 'Any'=None):  # line 84
    '''
  >>> print(list(appendEndmarkerIterator(enumerate(iter(range(3))))))
  [(0, 0), (1, 1), (2, 2), (3, None)]
  '''  # line 88
    count = 0  # type: int  # line 89
    try:  # line 90
        while True:  # line 90
            yield next(i)  # line 90
            count += 1  # line 90
    except:  # line 91
        yield end(count, endValue)  # line 91
