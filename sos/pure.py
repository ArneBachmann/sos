#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x330c1448

# Compiled with Coconut version 1.4.0-post_dev2 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get("__coconut__")
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules["__coconut__"]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# Copyright Arne Bachmann
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import math  # line 4
from typing import Any  # line 5
from typing import FrozenSet  # line 5
from typing import List  # line 5
from typing import Tuple  # line 5
try:  # line 6
    import wcwidth  # optional dependency for unicode support  # line 7
    def wcswidth(string: 'str') -> 'int':  # line 8
        l = wcwidth.wcswidth(string)  # type: int  # line 9
        return len(string) if l < 0 else l  # line 10
except:  # line 11
    wcswidth = len  # type: _coconut.typing.Callable[[str], int]  # line 11

KIBI = 1 << 10  # type: int  # line 13
MEBI = 1 << 20  # type: int  # line 14
GIBI = 1 << 30  # type: int  # line 15

_SECOND = 1000  # type: int  # line 17
_MINUTE = _SECOND * 60  # type: int  # line 18
_HOUR = _MINUTE * 60  # type: int  # line 19
_DAY = _HOUR * 24  # type: int  # line 20
_WEEK = _DAY * 7  # type: int  # line 21


# "Pure" functions
@_coconut_tco  # line 25
def unzip(lizt: 'List[Tuple[Any]]') -> 'Tuple[List[Any]]':  # line 25
    return _coconut_tail_call(zip, *lizt)  # line 26

@_coconut_tco  # line 28
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 28
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 28

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl: 'str'="", first: 'bool'=True) -> 'str':  # line 30
    return ((sep if first else "") + (nl + sep).join(seq)) if seq else ""  # line 30

def requiredDecimalDigits(number: 'int') -> 'int':  # line 32
    return 1 if number <= 0 else int(math.floor(round(math.log(number, 10), 6)) + 1)  # line 33

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # Used to match only arguments, or use only stored patterns  # line 35
    return a & b if a else b  # Used to match only arguments, or use only stored patterns  # line 35

def getTermWidth() -> 'int':  # line 37
    try:  # line 38
        import termwidth  # line 38
    except:  # HINT could be factored out, or even increased for most modern systems  # line 39
        return 80  # HINT could be factored out, or even increased for most modern systems  # line 39
    return termwidth.getTermWidth()[0]  # line 40

# Global variable
termWidth = getTermWidth() - 1  # uses curses or returns conservative default of 80  # line 43

def ljust(string: 'str'="", width: 'int'=termWidth) -> 'str':  # line 45
    assert width > 0  # line 46
    return string + " " * max(0, width - wcswidth(string))  # line 47

def splitStrip(string: 'str') -> 'List[str]':  # line 49
    return [_.strip() for _ in string.replace("\r", "").split("\n")]  # line 49

def signedNumber(number: 'int', filled: 'bool'=False) -> 'str':  # line 51
    ''' Always returns the sign. '''  # line 52
    return "+" if number > 0 else ("-" if number < 0 else (" " if filled else ""))  # line 53

def siSize(size: 'int') -> 'str':  # line 55
    ''' Returns formatted number with SI unit. '''  # line 56
    return "%.2f MiB" % (float(size) / MEBI) if size > 1.25 * MEBI else ("%.2f KiB" % (float(size) / KIBI) if size > 1.25 * KIBI else ("%d bytes" % size))  # line 57

def timeString(timeMs: 'int') -> 'str':  # line 59
    ''' Returns formatted time with unit. '''  # line 60
    return "%.1f weeks" % (float(timeMs) / _WEEK) if timeMs > 8. * _WEEK / 7 else ("%.1f days" % (float(timeMs) / _DAY) if timeMs > 1.125 * _DAY else ("%.1f hours" % (float(timeMs) / _HOUR) if timeMs > 1.5 * _HOUR else ("%.1f minutes" % (float(timeMs) / _MINUTE) if timeMs > 1.5 * _MINUTE else ("%.0f seconds" % (float(timeMs) / _SECOND) if timeMs > 1.5 * _SECOND else ("%d ms" % timeMs)))))  # line 61
