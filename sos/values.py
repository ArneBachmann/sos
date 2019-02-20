#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x2d2eecfd

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

if TYPE_CHECKING:  # line 4
    from typing import Dict  # line 4
    from typing import List  # line 4
    from typing import Tuple  # line 4
try:  # line 5
    import enum  # line 5
except:  # line 6
    raise Exception("SOS requires the enum module (Python 3.4+). You may try to manually install it via 'pip install enum34' or use 'pip install -U sos-vcs[backport]'")  # line 6


# Enums
MergeOperation = enum.Enum("MergeOperation", {"INSERT": 1, "REMOVE": 2, "BOTH": 3, "ASK": 4})  # insert remote changes into current, remove remote deletions from current, do both (replicates remote state), or ask per block  # line 10
MergeBlockType = enum.Enum("MergeBlockType", "KEEP INSERT REMOVE REPLACE MOVE")  # modify = intra-line changes, replace = full block replacement  # line 11


# Value types
class BranchInfo(_coconut.typing.NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("inSync", 'bool'), ("tracked", 'List[str]'), ("untracked", 'List[str]'), ("parent", '_coconut.typing.Optional[int]'), ("revision", '_coconut.typing.Optional[int]')])):  # line 15
    __slots__ = ()  # line 15
    __ne__ = _coconut.object.__ne__  # line 15
    def __eq__(self, other):  # line 15
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # line 15
    def __hash__(self):  # line 15
        return _coconut.tuple.__hash__(self) ^ hash(self.__class__)  # line 15
    def __new__(_cls, number, ctime, name=None, inSync=False, tracked=[], untracked=[], parent=None, revision=None):  # line 15
        return _coconut.tuple.__new__(_cls, (number, ctime, name, inSync, tracked, untracked, parent, revision))  # line 15


class CommitInfo(_coconut.typing.NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 26
    __slots__ = ()  # line 26
    __ne__ = _coconut.object.__ne__  # line 26
    def __eq__(self, other):  # line 26
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # line 26
    def __hash__(self):  # line 26
        return _coconut.tuple.__hash__(self) ^ hash(self.__class__)  # line 26
    def __new__(_cls, number, ctime, message=None):  # line 26
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 26


class PathInfo(_coconut.typing.NamedTuple("PathInfo", [("nameHash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", '_coconut.typing.Optional[str]')])):  # size == None means deleted in this revision; mtime = int(1000 * epoch)  # line 32
    __slots__ = ()  # size == None means deleted in this revision; mtime = int(1000 * epoch)  # line 32
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision; mtime = int(1000 * epoch)  # line 32
    def __eq__(self, other):  # size == None means deleted in this revision; mtime = int(1000 * epoch)  # line 32
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # size == None means deleted in this revision; mtime = int(1000 * epoch)  # line 32
    def __hash__(self):  # size == None means deleted in this revision; mtime = int(1000 * epoch)  # line 32
        return _coconut.tuple.__hash__(self) ^ hash(self.__class__)  # size == None means deleted in this revision; mtime = int(1000 * epoch)  # line 32
# size == None means deleted in this revision; mtime = int(1000 * epoch)
class ChangeSet(_coconut.typing.NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]'), ("moves", 'Dict[str, Tuple[str, PathInfo]]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 33
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 33
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 33
    def __eq__(self, other):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 33
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 33
    def __hash__(self):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 33
        return _coconut.tuple.__hash__(self) ^ hash(self.__class__)  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 33
# avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)
class Range(_coconut.typing.NamedTuple("Range", [("tipe", 'MergeBlockType'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 34
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 34
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 34
    def __eq__(self, other):  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 34
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 34
    def __hash__(self):  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 34
        return _coconut.tuple.__hash__(self) ^ hash(self.__class__)  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 34
# MergeBlockType[1,2,4], line number, length  # TODO use enum
class MergeBlock(_coconut.typing.NamedTuple("MergeBlock", [("tipe", 'MergeBlockType'), ("lines", 'List[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 35
    __slots__ = ()  # line 35
    __ne__ = _coconut.object.__ne__  # line 35
    def __eq__(self, other):  # line 35
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # line 35
    def __hash__(self):  # line 35
        return _coconut.tuple.__hash__(self) ^ hash(self.__class__)  # line 35
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 35
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 35

class GlobBlock(_coconut.typing.NamedTuple("GlobBlock", [("isLiteral", 'bool'), ("content", 'str'), ("index", 'int')])):  # for file pattern rename/move matching  # line 36
    __slots__ = ()  # for file pattern rename/move matching  # line 36
    __ne__ = _coconut.object.__ne__  # for file pattern rename/move matching  # line 36
    def __eq__(self, other):  # for file pattern rename/move matching  # line 36
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # for file pattern rename/move matching  # line 36
    def __hash__(self):  # for file pattern rename/move matching  # line 36
        return _coconut.tuple.__hash__(self) ^ hash(self.__class__)  # for file pattern rename/move matching  # line 36
# for file pattern rename/move matching
class GlobBlock2(_coconut.typing.NamedTuple("GlobBlock2", [("isLiteral", 'bool'), ("content", 'str'), ("matches", 'str')])):  # matching file pattern and input filename for translation  # line 37
    __slots__ = ()  # matching file pattern and input filename for translation  # line 37
    __ne__ = _coconut.object.__ne__  # matching file pattern and input filename for translation  # line 37
    def __eq__(self, other):  # matching file pattern and input filename for translation  # line 37
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # matching file pattern and input filename for translation  # line 37
    def __hash__(self):  # matching file pattern and input filename for translation  # line 37
        return _coconut.tuple.__hash__(self) ^ hash(self.__class__)  # matching file pattern and input filename for translation  # line 37
# matching file pattern and input filename for translation
