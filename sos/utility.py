#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1c05f476

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

# Utiliy functions
import hashlib  # early time tracking  # line 5
import logging  # early time tracking  # line 5
import os  # early time tracking  # line 5
sys = _coconut_sys  # early time tracking  # line 5
import time  # early time tracking  # line 5
START_TIME = time.time()  # early time tracking  # line 5

try:  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Any  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Dict  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import FrozenSet  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Generic  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import IO  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Iterator  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import List  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Optional  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Sequence  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Set  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Tuple  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Type  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import TypeVar  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Union  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
except:  # line 8
    pass  # line 8

try:  # line 10
    import enum  # line 10
except:  # line 11
    raise Exception("SOS requires the enum module (Python 3.4+). You may try to manually install it via 'pip install enum34' or use 'pip install -U sos-vcs[backport]'")  # line 11
try:  # line 12
    from sos import pure  # line 12
    from sos.values import *  # line 12
except:  # line 13
    import pure  # line 13
    from values import *  # line 13


# Lazy imports for quicker initialization
class bz2:  # line 17
    @_coconut_tco  # line 18
    def __getattribute__(_, key):  # line 18
        global bz2  # line 19
        import bz2  # overrides global reference  # line 20
        return _coconut_tail_call(bz2.__getattribute__, key)  # line 21
bz2 = bz2()  # line 22

class codecs:  # line 24
    @_coconut_tco  # line 25
    def __getattribute__(_, key):  # line 25
        global codecs  # line 26
        import codecs  # overrides global reference  # line 27
        return _coconut_tail_call(codecs.__getattribute__, key)  # line 28
codecs = codecs()  # line 29

class difflib:  # line 31
    @_coconut_tco  # line 32
    def __getattribute__(_, key):  # line 32
        global difflib  # line 33
        import difflib  # overrides global reference  # line 34
        return _coconut_tail_call(difflib.__getattribute__, key)  # line 35
difflib = difflib()  # line 36


verbose = '--verbose' in sys.argv or '-v' in sys.argv  # type: bool  # line 39
debug_ = os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv  # type: bool  # line 40


# Classes
class Accessor(dict):  # line 44
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 45
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # TODO remove -> None when fixed in Coconut stub  # line 46
        dict.__init__(_, mapping)  # TODO remove -> None when fixed in Coconut stub  # line 46
    @_coconut_tco  # line 47
    def __getattribute__(_, name: 'str') -> 'Any':  # line 47
        try:  # line 48
            return _[name]  # line 48
        except:  # line 49
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 49

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 51
    Number = TypeVar("Number", int, float)  # line 52
    class Counter(Generic[Number]):  # line 53
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 54
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 55
            _.value = initial  # type: Number  # line 55
        def inc(_, by: 'Number'=1) -> 'Number':  # line 56
            _.value += by  # line 56
            return _.value  # line 56
else:  # line 57
    class Counter:  # line 58
        def __init__(_, initial=0) -> 'None':  # line 59
            _.value = initial  # line 59
        def inc(_, by=1):  # line 60
            _.value += by  # line 60
            return _.value  # line 60

class ProgressIndicator(Counter):  # line 62
    ''' Manages a rotating progress indicator. '''  # line 63
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 64
        super(ProgressIndicator, _).__init__(-1)  # line 64
        _.symbols = symbols  # line 64
        _.timer = time.time()  # type: float  # line 64
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 64
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 65
        ''' Returns a value only if a certain time has passed. '''  # line 66
        newtime = time.time()  # type: float  # line 67
        if newtime - _.timer < .1:  # line 68
            return None  # line 68
        _.timer = newtime  # line 69
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 70
        if _.callback:  # line 71
            _.callback(sign)  # line 71
        return sign  # line 72

class Logger:  # line 74
    ''' Logger that supports joining many items. '''  # line 75
    def __init__(_, log) -> 'None':  # line 76
        _._log = log  # line 76
    def debug(_, *s):  # line 77
        _._log.debug(pure.sjoin(*s))  # line 77
    def info(_, *s):  # line 78
        _._log.info(pure.sjoin(*s))  # line 78
    def warn(_, *s):  # line 79
        _._log.warning(pure.sjoin(*s))  # line 79
    def error(_, *s):  # line 80
        _._log.error(pure.sjoin(*s))  # line 80


# Constants
_log = Logger(logging.getLogger(__name__))  # line 84
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 84
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress", "useChangesCommand", "useUnicodeFont"]  # type: List[str]  # line 85
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 86
CONFIGURABLE_INTS = ["logLines"]  # type: List[str]  # line 87
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 88
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 89
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 90
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 91
BACKUP_SUFFIX = "_last"  # type: str  # line 92
metaFolder = ".sos"  # type: str  # line 93
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 94
metaFile = ".meta"  # type: str  # line 95
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 96
KIBI = 1 << 10  # type: int  # line 97
MEBI = 1 << 20  # type: int  # line 98
GIBI = 1 << 30  # type: int  # line 99
bufSize = MEBI  # type: int  # line 100
UTF8 = "utf_8"  # type: str  # early used constant, not defined in standard library  # line 101
SVN = "svn"  # type: str  # line 102
SLASH = "/"  # type: str  # line 103
DOT_SYMBOL = "\u00b7"  # type: str  # line 104
MULT_SYMBOL = "\u00d7"  # type: str  # line 105
CROSS_SYMBOL = "\u2716"  # type: str  # line 106
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 107
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # line 108
MOVE_SYMBOL = "\u21cc"  # type: str  # \U0001F5C0"  # HINT second one is very unlikely to be in any console font  # line 109
METADATA_FORMAT = 1  # type: int  # counter for incompatible consecutive formats  # line 110
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 111
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 112
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "csv": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS has different per-file operation  # line 113
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[bytes, str]  # line 114
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[str, int]  # https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 115
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE], "ignoresWhitelist": []})  # type: Accessor  # line 116


# Enums
MergeOperation = enum.Enum("MergeOperation", {"INSERT": 1, "REMOVE": 2, "BOTH": 3, "ASK": 4})  # insert remote changes into current, remove remote deletions from current, do both (replicates remote state), or ask per block  # line 129
MergeBlockType = enum.Enum("MergeBlockType", "KEEP INSERT REMOVE REPLACE MOVE")  # modify = intra-line changes, replace = full block replacement  # line 130


# Functions
def printo(s: 'str'="", nl: 'str'="\n"):  # PEP528 compatibility  # line 134
    tryOrDefault(lambda _=None: (lambda _coconut_none_coalesce_item: sys.stdout if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(sys.stdout.buffer), sys.stdout).write((s + nl).encode(sys.stdout.encoding, 'backslashreplace'))  # PEP528 compatibility  # line 134
    sys.stdout.flush()  # PEP528 compatibility  # line 134
def printe(s: 'str'="", nl: 'str'="\n"):  # line 135
    tryOrDefault(lambda _=None: (lambda _coconut_none_coalesce_item: sys.stderr if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(sys.stderr.buffer), sys.stderr).write((s + nl).encode(sys.stderr.encoding, 'backslashreplace'))  # line 135
    sys.stderr.flush()  # line 135
@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 136
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 136
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 136
@_coconut_tco  # for os->py access of reading filenames  # line 137
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 137
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 137
try:  # line 138
    import chardet  # https://github.com/chardet/chardet  # line 139
    def detectEncoding(binary: 'bytes') -> 'str':  # line 140
        return chardet.detect(binary)["encoding"]  # line 140
except:  # line 141
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 142
        ''' Fallback if chardet library missing. '''  # line 143
        try:  # line 144
            binary.decode(UTF8)  # line 144
            return UTF8  # line 144
        except UnicodeError:  # line 145
            pass  # line 145
        try:  # line 146
            binary.decode("utf_16")  # line 146
            return "utf_16"  # line 146
        except UnicodeError:  # line 147
            pass  # line 147
        try:  # line 148
            binary.decode("cp1252")  # line 148
            return "cp1252"  # line 148
        except UnicodeError:  # line 149
            pass  # line 149
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 150

def tryOrDefault(func: '_coconut.typing.Callable[..., Any]', default: 'Any') -> 'Any':  # line 152
    try:  # line 153
        return func()  # line 153
    except:  # line 154
        return default  # line 154

def tryOrIgnore(func: '_coconut.typing.Callable[..., Any]', onError: '_coconut.typing.Callable[[Exception], None]'=lambda _: None) -> 'None':  # handle with care!  # line 156
    try:  # line 157
        return func()  # line 157
    except Exception as E:  # line 158
        onError(E)  # line 158

def removePath(key: 'str', value: 'str') -> 'str':  # line 160
    ''' Cleanup of user-specified global file patterns. '''  # TODO improve  # line 161
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 162

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 164
    d = {}  # type: Dict[Any, Any]  # line 164
    d.update(dikt)  # line 164
    d.update(by)  # line 164
    return d  # line 164

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # Abstraction for opening both compressed and plain files  # line 166
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # Abstraction for opening both compressed and plain files  # line 166

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 168
    ''' Determine EOL style from a binary string. '''  # line 169
    lf = file.count(b"\n")  # type: int  # line 170
    cr = file.count(b"\r")  # type: int  # line 171
    crlf = file.count(b"\r\n")  # type: int  # line 172
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 173
        if lf != crlf or cr != crlf:  # line 174
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 174
        return b"\r\n"  # line 175
    if lf != 0 and cr != 0:  # line 176
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 176
    if lf > cr:  # Linux/Unix  # line 177
        return b"\n"  # Linux/Unix  # line 177
    if cr > lf:  # older 8-bit machines  # line 178
        return b"\r"  # older 8-bit machines  # line 178
    return None  # no new line contained, cannot determine  # line 179

if TYPE_CHECKING:  # line 181
    Splittable = TypeVar("Splittable", str, bytes)  # TODO isn't that the same as AnyStr?  # line 182
    def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> 'List[Splittable]':  # line 183
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 183
else:  # line 184
    def safeSplit(s, d=None):  # line 185
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 185

@_coconut_tco  # line 187
def hashStr(datas: 'str') -> 'str':  # line 187
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 187

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 189
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 189

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 191
    return lizt[index:].index(what) + index  # line 191

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 193
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 193

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 195
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 195

def Exit(message: 'str'="", code=1):  # line 197
    printe("[EXIT%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "") + (" " + message + "." if message != "" else ""))  # line 197
    sys.exit(code)  # line 197

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 199
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar to xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 200
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 201
        raise Exception("Cannot possibly strings pack into specified length")  # line 201
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 202
        prefix += separator + ((process)(strings.pop(0)))  # line 202
    return prefix  # line 203

def exception(E):  # line 205
    ''' Report an exception to the user to enable useful bug reporting. '''  # line 206
    printo(str(E))  # line 207
    import traceback  # line 208
    traceback.print_exc()  # line 209
    traceback.print_stack()  # line 210

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None, callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 212
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 213
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 214
    _hash = hashlib.sha256()  # line 215
    wsize = 0  # type: int  # line 216
    if saveTo and os.path.exists(encode(saveTo)):  # line 217
        Exit("Hash conflict. Leaving revision in inconsistent state. This should happen only once in a lifetime")  # line 217
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 218
    with open(encode(path), "rb") as fd:  # line 219
        while True:  # line 220
            buffer = fd.read(bufSize)  # type: bytes  # line 221
            _hash.update(buffer)  # line 222
            if to:  # line 223
                to.write(buffer)  # line 223
            if len(buffer) < bufSize:  # line 224
                break  # line 224
            if indicator:  # line 225
                indicator.getIndicator()  # line 225
        if to:  # line 226
            to.close()  # line 227
            wsize = os.stat(encode(saveTo)).st_size  # line 228
    return (_hash.hexdigest(), wsize)  # line 229

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 231
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 232
    for k, v in map.items():  # line 233
        if k in params:  # line 233
            return v  # line 233
    return default  # line 234

@_coconut_tco  # line 236
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 236
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 236

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 238
    lines = []  # type: _coconut.typing.Sequence[str]  # line 239
    if filename is not None:  # line 240
        with open(encode(filename), "rb") as fd:  # line 240
            content = fd.read()  # line 240
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 241
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 242
    if filename is not None:  # line 243
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 243
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 243
    elif content is not None:  # line 244
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 244
    else:  # line 245
        return (sys.getdefaultencoding(), b"\n", [])  # line 245
    if ignoreWhitespace:  # line 246
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 246
    return (encoding, eol, lines)  # line 247

if TYPE_CHECKING:  # line 249
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 250
    @_coconut_tco  # line 251
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 251
        ''' A better makedata() version. '''  # line 252
        r = _old._asdict()  # type: Dict[str, Any]  # line 253
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 254
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 255
else:  # line 256
    @_coconut_tco  # line 257
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 257
        ''' A better makedata() version. '''  # line 258
        r = _old._asdict()  # line 259
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 260
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 261

def detectMoves(changes: 'ChangeSet') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 263
    ''' Compute renames/removes for a changeset. '''  # line 264
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 265
    for path, info in changes.additions.items():  # line 266
        for dpath, dinfo in changes.deletions.items():  # line 267
            if info.size == dinfo.size and info.mtime == dinfo.mtime and info.hash == dinfo.hash:  # was moved TODO check either mtime or hash?  # line 268
                moves[path] = (dpath, info)  # store new data and original name, but don't remove add/del  # line 269
                break  # deletions loop, continue with next addition  # line 270
    return moves  # line 271

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 273
    ''' Default can be a selection from choice and allows empty input. '''  # line 274
    while True:  # line 275
        selection = input(text).strip().lower()  # line 276
        if selection != "" and selection in choices:  # line 277
            break  # line 277
        if selection == "" and default is not None:  # line 278
            selection = default  # line 278
            break  # line 278
    return selection  # line 279

def user_block_input(output: 'List[str]'):  # line 281
    ''' Side-effect appending to input list. '''  # line 282
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 283
    line = sep  # type: str  # line 283
    while True:  # line 284
        line = input("> ")  # line 285
        if line == sep:  # line 286
            break  # line 286
        output.append(line)  # writes to caller-provided list reference  # line 287

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 289
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For update, the other version is assumed to be the "new/added" one, while for diff, the current changes are the ones "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly returns detected change blocks only, no text merging
      eol flag will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original
  '''  # line 304
    encoding = None  # type: str  # line 305
    othr = None  # type: _coconut.typing.Sequence[str]  # line 305
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 305
    curr = None  # type: _coconut.typing.Sequence[str]  # line 305
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 305
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 306
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 307
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 308
    except Exception as E:  # line 309
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 309
    if None not in [othreol, curreol] and othreol != curreol:  # line 310
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 310
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 311
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 312
    tmp = []  # type: List[str]  # block lines  # line 313
    last = " "  # type: str  # line 314
    no = None  # type: int  # line 314
    line = None  # type: str  # line 314
    offset = 0  # type: int  # into file offset for remark lines  # line 315
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 316
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 317
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 317
            continue  # continue filling current block, no matter what type of block it is  # line 317
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 318
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 318
        if last == " ":  # block is same in both files  # line 319
            if len(tmp) > 0:  # avoid adding empty keep block  # line 320
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 320
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 321
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 322
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 323
                offset += len(blocks[-2].lines)  # line 324
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 325
                blocks.pop()  # line 326
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 327
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 328
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 329
                offset += len(blocks[-1].lines)  # line 330
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 331
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 332
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 333
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 333
        last = line[0]  # line 334
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 335
# TODO add code to detect block moves here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 337
    debug("Diff blocks: " + repr(blocks))  # line 338
    if diffOnly:  # line 339
        return (blocks, nl)  # line 339

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 342
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 342
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 342
    selection = None  # type: str  # clean list of strings  # line 342
    for block in blocks:  # line 343
        if block.tipe == MergeBlockType.KEEP:  # line 344
            output.extend(block.lines)  # line 345
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 346
            output.extend(block.lines)  # line 348
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 349
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 350
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 351
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 352
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 353
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 354
                while True:  # line 355
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 356
                    if op in "tb":  # line 357
                        output.extend(block.lines)  # line 357
                    if op in "ib":  # line 358
                        output.extend(block.replaces.lines)  # line 358
                    if op == "u":  # line 359
                        user_block_input(output)  # line 359
                    if op in "tbiu":  # line 360
                        break  # line 360
            else:  # more than one line and not ask  # line 361
                if mergeOperation == MergeOperation.REMOVE:  # line 362
                    pass  # line 362
                elif mergeOperation == MergeOperation.BOTH:  # line 363
                    output.extend(block.lines)  # line 363
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 364
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 364
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 365
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_akk is None):  # condition for asking  # line 366
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 368
                if selection in "ao":  # line 369
                    if block.tipe == MergeBlockType.INSERT:  # line 370
                        add_all = "y" if selection == "a" else "n"  # line 370
                        selection = add_all  # line 370
                    else:  # REMOVE case  # line 371
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 371
                        selection = del_all  # REMOVE case  # line 371
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 372
                output.extend(block.lines)  # line 374
    debug("Merge output: " + "; ".join(output))  # line 375
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 376
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 379
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 379
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 382
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 383
    blocks = []  # type: List[MergeBlock]  # line 384
    for i, line in enumerate(out):  # line 385
        if line[0] == "+":  # line 386
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 387
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 388
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 389
                else:  # first + in block  # line 390
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 391
            else:  # last line of + block  # line 392
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 393
                    blocks[-1].lines.append(line[2])  # line 394
                else:  # single line  # line 395
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 396
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 397
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 398
                    blocks.pop()  # line 398
        elif line[0] == "-":  # line 399
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 400
                blocks[-1].lines.append(line[2])  # line 401
            else:  # first in block  # line 402
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 403
        elif line[0] == " ":  # line 404
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 405
                blocks[-1].lines.append(line[2])  # line 406
            else:  # first in block  # line 407
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 408
        else:  # line 409
            raise Exception("Cannot parse diff line %r" % line)  # line 409
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 410
    if diffOnly:  # line 411
        return blocks  # line 411
    out[:] = []  # line 412
    for i, block in enumerate(blocks):  # line 413
        if block.tipe == MergeBlockType.KEEP:  # line 414
            out.extend(block.lines)  # line 414
        elif block.tipe == MergeBlockType.REPLACE:  # line 415
            if mergeOperation == MergeOperation.ASK:  # line 416
                printo(pure.ajoin("- ", othr))  # line 417
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 418
                printo("+ " + (" " * i) + block.lines[0])  # line 419
                printo(pure.ajoin("+ ", into))  # line 420
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 421
                if op in "tb":  # line 422
                    out.extend(block.lines)  # line 422
                    break  # line 422
                if op in "ib":  # line 423
                    out.extend(block.replaces.lines)  # line 423
                    break  # line 423
                if op == "m":  # line 424
                    user_block_input(out)  # line 424
                    break  # line 424
            else:  # non-interactive  # line 425
                if mergeOperation == MergeOperation.REMOVE:  # line 426
                    pass  # line 426
                elif mergeOperation == MergeOperation.BOTH:  # line 427
                    out.extend(block.lines)  # line 427
                elif mergeOperation == MergeOperation.INSERT:  # line 428
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 428
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 429
            out.extend(block.lines)  # line 429
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 430
            out.extend(block.lines)  # line 430
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 432

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 434
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 437
    debug("Detecting root folders...")  # line 438
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 439
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 440
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 441
        contents = set(os.listdir(path))  # type: Set[str]  # line 442
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder  # line 443
        choice = None  # type: _coconut.typing.Optional[str]  # line 444
        if len(vcss) > 1:  # line 445
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 446
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 447
        elif len(vcss) > 0:  # line 448
            choice = vcss[0]  # line 448
        if not vcs[0] and choice:  # memorize current repo root  # line 449
            vcs = (path, choice)  # memorize current repo root  # line 449
        new = os.path.dirname(path)  # get parent path  # line 450
        if new == path:  # avoid infinite loop  # line 451
            break  # avoid infinite loop  # line 451
        path = new  # line 452
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 453
        if vcs[0]:  # already detected vcs base and command  # line 454
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 454
        sos = path  # line 455
        while True:  # continue search for VCS base  # line 456
            new = os.path.dirname(path)  # get parent path  # line 457
            if new == path:  # no VCS folder found  # line 458
                return (sos, None, None)  # no VCS folder found  # line 458
            path = new  # line 459
            contents = set(os.listdir(path))  # line 460
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 461
            choice = None  # line 462
            if len(vcss) > 1:  # line 463
                choice = SVN if SVN in vcss else vcss[0]  # line 464
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 465
            elif len(vcss) > 0:  # line 466
                choice = vcss[0]  # line 466
            if choice:  # line 467
                return (sos, path, choice)  # line 467
    return (None, vcs[0], vcs[1])  # line 468

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 470
    index = 0  # type: int  # line 471
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 472
    while index < len(pattern):  # line 473
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 474
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 474
            continue  # line 474
        if pattern[index] in "*?":  # line 475
            count = 1  # type: int  # line 476
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 477
                count += 1  # line 477
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 478
            index += count  # line 478
            continue  # line 478
        if pattern[index:index + 2] == "[!":  # line 479
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 479
            index += len(out[-1][1])  # line 479
            continue  # line 479
        count = 1  # line 480
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 481
            count += 1  # line 481
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 482
        index += count  # line 482
    return out  # line 483

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 485
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 486
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 487
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 489
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 489
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 490
        Exit("Source and target file patterns differ in semantics")  # line 490
    return (ot, nt)  # line 491

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 493
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 494
    pairs = []  # type: List[Tuple[str, str]]  # line 495
    for filename in filenames:  # line 496
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 497
        nextliteral = 0  # type: int  # line 498
        parsedOld = []  # type: List[GlobBlock2]  # line 499
        index = 0  # type: int  # line 500
        for part in oldPattern:  # match everything in the old filename  # line 501
            if part.isLiteral:  # line 502
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 502
                index += len(part.content)  # line 502
                nextliteral += 1  # line 502
            elif part.content.startswith("?"):  # line 503
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 503
                index += len(part.content)  # line 503
            elif part.content.startswith("["):  # line 504
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 504
                index += 1  # line 504
            elif part.content == "*":  # line 505
                if nextliteral >= len(literals):  # line 506
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 506
                    break  # line 506
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 507
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 508
                index = nxt  # line 508
            else:  # line 509
                Exit("Invalid file pattern specified for move/rename")  # line 509
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 510
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 511
        nextliteral = 0  # line 512
        nextglob = 0  # type: int  # line 512
        outname = []  # type: List[str]  # line 513
        for part in newPattern:  # generate new filename  # line 514
            if part.isLiteral:  # line 515
                outname.append(literals[nextliteral].content)  # line 515
                nextliteral += 1  # line 515
            else:  # line 516
                outname.append(globs[nextglob].matches)  # line 516
                nextglob += 1  # line 516
        pairs.append((filename, "".join(outname)))  # line 517
    return pairs  # line 518

@_coconut_tco  # line 520
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 520
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 524
    if not actions:  # line 525
        return []  # line 525
    sources = None  # type: List[str]  # line 526
    targets = None  # type: List[str]  # line 526
    sources, targets = [list(l) for l in zip(*actions)]  # line 527
    last = len(actions)  # type: int  # line 528
    while last > 1:  # line 529
        clean = True  # type: bool  # line 530
        for i in range(1, last):  # line 531
            try:  # line 532
                index = targets[:i].index(sources[i])  # type: int  # line 533
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 534
                targets.insert(index, targets.pop(i))  # line 535
                clean = False  # line 536
            except:  # target not found in sources: good!  # line 537
                continue  # target not found in sources: good!  # line 537
        if clean:  # line 538
            break  # line 538
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 539
    if exitOnConflict:  # line 540
        for i in range(1, len(actions)):  # line 540
            if sources[i] in targets[:i]:  # line 540
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 540
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 541

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 543
    ''' Determine OS-independent relative folder path, and relative pattern path. '''  # line 544
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 545
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 546

def parseOnlyOptions(root: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 548
    ''' Returns set of --only arguments, and set or --except arguments. '''  # line 549
    cwd = os.getcwd()  # type: str  # line 550
    onlys = []  # type: List[str]  # zero necessary as last start position  # line 551
    excps = []  # type: List[str]  # zero necessary as last start position  # line 551
    index = 0  # type: int  # zero necessary as last start position  # line 551
    while True:  # line 552
        try:  # line 553
            index = 1 + listindex(options, "--only", index)  # line 554
            onlys.append(options[index])  # line 555
            del options[index]  # line 556
            del options[index - 1]  # line 557
        except:  # line 558
            break  # line 558
    index = 0  # line 559
    while True:  # line 560
        try:  # line 561
            index = 1 + listindex(options, "--except", index)  # line 562
            excps.append(options[index])  # line 563
            del options[index]  # line 564
            del options[index - 1]  # line 565
        except:  # line 566
            break  # line 566
    return (frozenset((relativize(root, o)[1] for o in onlys)) if onlys else None, frozenset((relativize(root, e)[1] for e in excps)) if excps else None)  # line 567
