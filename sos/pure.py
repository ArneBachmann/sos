#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x29c451d5

# Compiled with Coconut version 1.3.1-post_dev28 [Dead Parrot]

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


# "Pure" functions
@_coconut_tco  # line 15
def sjoin(*s: 'Tuple[Any]') -> 'str':  # line 15
    return _coconut_tail_call(" ".join, [str(e) for e in s if e != ''])  # line 15

def ajoin(sep: 'str', seq: '_coconut.typing.Sequence[str]', nl: 'str'="", first: 'bool'=True) -> 'str':  # line 17
    return ((sep if first else "") + (nl + sep).join(seq)) if seq else ""  # line 17

def requiredDecimalDigits(number: 'int') -> 'int':  # line 19
    return 1 if number <= 0 else int(math.floor(round(math.log(number, 10), 6)) + 1)  # line 20

def conditionalIntersection(a: '_coconut.typing.Optional[FrozenSet[str]]', b: 'FrozenSet[str]') -> 'FrozenSet[str]':  # Used to match only arguments, or use only stored patterns  # line 22
    return a & b if a else b  # Used to match only arguments, or use only stored patterns  # line 22

def getTermWidth() -> 'int':  # line 24
    try:  # line 25
        import termwidth  # line 25
    except:  # HINT could be factored out, or even increased for most modern systems  # line 26
        return 80  # HINT could be factored out, or even increased for most modern systems  # line 26
    return termwidth.getTermWidth()[0]  # line 27

# Global variable
termWidth = getTermWidth() - 1  # uses curses or returns conservative default of 80  # line 30

def ljust(string: 'str'="", width: 'int'=termWidth) -> 'str':  # line 32
    assert width > 0  # line 33
    return string + " " * max(0, width - wcswidth(string))  # line 34

def splitStrip(string: 'str') -> 'List[str]':  # line 36
    return [_.strip() for _ in string.replace("\r", "").split("\n")]  # line 36
