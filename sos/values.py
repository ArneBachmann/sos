#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x48fe486d

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

class BranchInfo(_coconut_NamedTuple("BranchInfo", [("number", 'int'), ("ctime", 'int'), ("name", '_coconut.typing.Optional[str]'), ("inSync", 'bool'), ("tracked", 'List[str]'), ("untracked", 'List[str]'), ("parent", '_coconut.typing.Optional[int]'), ("revision", '_coconut.typing.Optional[int]')])):  # line 4
    __slots__ = ()  # line 4
    __ne__ = _coconut.object.__ne__  # line 4
    def __eq__(self, other):  # line 4
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # line 4
    def __new__(_cls, number, ctime, name=None, inSync=False, tracked=[], untracked=[], parent=None, revision=None):  # line 4
        return _coconut.tuple.__new__(_cls, (number, ctime, name, inSync, tracked, untracked, parent, revision))  # line 4


class CommitInfo(_coconut_NamedTuple("CommitInfo", [("number", 'int'), ("ctime", 'int'), ("message", '_coconut.typing.Optional[str]')])):  # line 15
    __slots__ = ()  # line 15
    __ne__ = _coconut.object.__ne__  # line 15
    def __eq__(self, other):  # line 15
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # line 15
    def __new__(_cls, number, ctime, message=None):  # line 15
        return _coconut.tuple.__new__(_cls, (number, ctime, message))  # line 15


class PathInfo(_coconut_NamedTuple("PathInfo", [("nameHash", 'str'), ("size", '_coconut.typing.Optional[int]'), ("mtime", 'int'), ("hash", '_coconut.typing.Optional[str]')])):  # size == None means deleted in this revision  # line 21
    __slots__ = ()  # size == None means deleted in this revision  # line 21
    __ne__ = _coconut.object.__ne__  # size == None means deleted in this revision  # line 21
    def __eq__(self, other):  # size == None means deleted in this revision  # line 21
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # size == None means deleted in this revision  # line 21
# size == None means deleted in this revision
class ChangeSet(_coconut_NamedTuple("ChangeSet", [("additions", 'Dict[str, PathInfo]'), ("deletions", 'Dict[str, PathInfo]'), ("modifications", 'Dict[str, PathInfo]'), ("moves", 'Dict[str, Tuple[str, PathInfo]]')])):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 22
    __slots__ = ()  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 22
    __ne__ = _coconut.object.__ne__  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 22
    def __eq__(self, other):  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 22
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)  # line 22
# avoid default assignment of {} as it leads to runtime errors (contains data on init for unknown reason)
class Range(_coconut_NamedTuple("Range", [("tipe", 'MergeBlockType'), ("indexes", '_coconut.typing.Sequence[int]')])):  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 23
    __slots__ = ()  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 23
    __ne__ = _coconut.object.__ne__  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 23
    def __eq__(self, other):  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 23
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # MergeBlockType[1,2,4], line number, length  # TODO use enum  # line 23
# MergeBlockType[1,2,4], line number, length  # TODO use enum
class MergeBlock(_coconut_NamedTuple("MergeBlock", [("tipe", 'MergeBlockType'), ("lines", 'List[str]'), ("line", 'int'), ("replaces", '_coconut.typing.Optional[MergeBlock]'), ("changes", '_coconut.typing.Optional[Range]')])):  # line 24
    __slots__ = ()  # line 24
    __ne__ = _coconut.object.__ne__  # line 24
    def __eq__(self, other):  # line 24
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # line 24
    def __new__(_cls, tipe, lines, line, replaces=None, changes=None):  # line 24
        return _coconut.tuple.__new__(_cls, (tipe, lines, line, replaces, changes))  # line 24

class GlobBlock(_coconut_NamedTuple("GlobBlock", [("isLiteral", 'bool'), ("content", 'str'), ("index", 'int')])):  # for file pattern rename/move matching  # line 25
    __slots__ = ()  # for file pattern rename/move matching  # line 25
    __ne__ = _coconut.object.__ne__  # for file pattern rename/move matching  # line 25
    def __eq__(self, other):  # for file pattern rename/move matching  # line 25
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # for file pattern rename/move matching  # line 25
# for file pattern rename/move matching
class GlobBlock2(_coconut_NamedTuple("GlobBlock2", [("isLiteral", 'bool'), ("content", 'str'), ("matches", 'str')])):  # matching file pattern and input filename for translation  # line 26
    __slots__ = ()  # matching file pattern and input filename for translation  # line 26
    __ne__ = _coconut.object.__ne__  # matching file pattern and input filename for translation  # line 26
    def __eq__(self, other):  # matching file pattern and input filename for translation  # line 26
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # matching file pattern and input filename for translation  # line 26
# matching file pattern and input filename for translation
