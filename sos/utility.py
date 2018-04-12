#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x75637492

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
    from typing import AnyStr  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Dict  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import FrozenSet  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Generic  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import IO  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
    from typing import Iterable  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
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


# Lazy imports for quicker initialization TODO make mypy pass
bz2 = None  # type: Any  # line 17
codecs = None  # type: Any  # line 17
difflib = None  # type: Any  # line 17
class bz2:  # line 18
    @_coconut_tco  # line 18
    def __getattribute__(_, key):  # line 18
        global bz2  # line 19
        import bz2  # line 20
        return _coconut_tail_call(bz2.__getattribute__, key)  # line 21
bz2 = bz2()  # type: object  # line 22

class codecs:  # line 24
    @_coconut_tco  # line 24
    def __getattribute__(_, key):  # line 24
        global codecs  # line 25
        import codecs  # line 26
        return _coconut_tail_call(codecs.__getattribute__, key)  # line 27
codecs = codecs()  # type: object  # line 28

class difflib:  # line 30
    @_coconut_tco  # line 30
    def __getattribute__(_, key):  # line 30
        global difflib  # line 31
        import difflib  # line 32
        return _coconut_tail_call(difflib.__getattribute__, key)  # line 33
difflib = difflib()  # type: object  # line 34


verbose = '--verbose' in sys.argv or '-v' in sys.argv  # type: bool  # line 37
debug_ = os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv  # type: bool  # line 38


# Classes
class Accessor(dict):  # line 42
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 43
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # TODO remove -> None when fixed in Coconut stub  # line 44
        dict.__init__(_, mapping)  # TODO remove -> None when fixed in Coconut stub  # line 44
    @_coconut_tco  # line 45
    def __getattribute__(_, name: 'str') -> 'Any':  # line 45
        try:  # line 46
            return _[name]  # line 46
        except:  # line 47
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 47

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 49
    Number = TypeVar("Number", int, float)  # line 50
    class Counter(Generic[Number]):  # line 51
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 52
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 53
            _.value = initial  # type: Number  # line 53
        def inc(_, by: 'Number'=1) -> 'Number':  # line 54
            _.value += by  # line 54
            return _.value  # line 54
else:  # line 55
    class Counter:  # line 56
        def __init__(_, initial=0) -> 'None':  # line 57
            _.value = initial  # line 57
        def inc(_, by=1):  # line 58
            _.value += by  # line 58
            return _.value  # line 58

class ProgressIndicator(Counter):  # line 60
    ''' Manages a rotating progress indicator. '''  # line 61
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 62
        super(ProgressIndicator, _).__init__(-1)  # line 62
        _.symbols = symbols  # line 62
        _.timer = time.time()  # type: float  # line 62
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 62
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 63
        ''' Returns a value only if a certain time has passed. '''  # line 64
        newtime = time.time()  # type: float  # line 65
        if newtime - _.timer < .1:  # line 66
            return None  # line 66
        _.timer = newtime  # line 67
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 68
        if _.callback:  # line 69
            _.callback(sign)  # line 69
        return sign  # line 70

class Logger:  # line 72
    ''' Logger that supports joining many items. '''  # line 73
    def __init__(_, log) -> 'None':  # line 74
        _._log = log  # line 74
    def debug(_, *s):  # line 75
        _._log.debug(pure.sjoin(*s))  # line 75
    def info(_, *s):  # line 76
        _._log.info(pure.sjoin(*s))  # line 76
    def warn(_, *s):  # line 77
        _._log.warning(pure.sjoin(*s))  # line 77
    def error(_, *s):  # line 78
        _._log.error(pure.sjoin(*s))  # line 78


# Constants
_log = Logger(logging.getLogger(__name__))  # line 82
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 82
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress", "useChangesCommand", "useUnicodeFont"]  # type: List[str]  # line 83
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 84
CONFIGURABLE_INTS = ["logLines"]  # type: List[str]  # line 85
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 86
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 87
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 88
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 89
BACKUP_SUFFIX = "_last"  # type: str  # line 90
metaFolder = ".sos"  # type: str  # line 91
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 92
metaFile = ".meta"  # type: str  # line 93
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 94
KIBI = 1 << 10  # type: int  # line 95
MEBI = 1 << 20  # type: int  # line 95
GIBI = 1 << 30  # type: int  # line 95
bufSize = MEBI  # type: int  # line 96
UTF8 = "utf_8"  # type: str  # early used constant, not defined in standard library  # line 97
SVN = "svn"  # type: str  # line 98
SLASH = "/"  # type: str  # line 99
DOT_SYMBOL = "\u00b7"  # type: str  # line 100
MULT_SYMBOL = "\u00d7"  # type: str  # line 101
CROSS_SYMBOL = "\u2716"  # type: str  # line 102
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 103
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # line 104
MOVE_SYMBOL = "\u21cc"  # type: str  # \U0001F5C0"  # HINT second one is very unlikely to be in any console font  # line 105
METADATA_FORMAT = 1  # type: int  # counter for incompatible consecutive formats (was undefined, "1" is the first versioned version after that)  # line 106
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 107
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 108
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "csv": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS has different per-file operation  # line 109
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[bytes, str]  # line 110
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[str, int]  # https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 111
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE], "ignoresWhitelist": []})  # type: Accessor  # line 112


# Enums
MergeOperation = enum.Enum("MergeOperation", {"INSERT": 1, "REMOVE": 2, "BOTH": 3, "ASK": 4})  # insert remote changes into current, remove remote deletions from current, do both (replicates remote state), or ask per block  # line 125
MergeBlockType = enum.Enum("MergeBlockType", "KEEP INSERT REMOVE REPLACE MOVE")  # modify = intra-line changes, replace = full block replacement  # line 126


# Functions
def printo(s: 'str'="", nl: 'str'="\n"):  # PEP528 compatibility  # line 130
    tryOrDefault(lambda _=None: (lambda _coconut_none_coalesce_item: sys.stdout if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(sys.stdout.buffer), sys.stdout).write((s + nl).encode(sys.stdout.encoding, 'backslashreplace'))  # PEP528 compatibility  # line 130
    sys.stdout.flush()  # PEP528 compatibility  # line 130
def printe(s: 'str'="", nl: 'str'="\n"):  # line 131
    tryOrDefault(lambda _=None: (lambda _coconut_none_coalesce_item: sys.stderr if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(sys.stderr.buffer), sys.stderr).write((s + nl).encode(sys.stderr.encoding, 'backslashreplace'))  # line 131
    sys.stderr.flush()  # line 131
@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 132
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 132
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 132
@_coconut_tco  # for os->py access of reading filenames  # line 133
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 133
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 133
try:  # line 134
    import chardet  # https://github.com/chardet/chardet  # line 135
    def detectEncoding(binary: 'bytes') -> 'str':  # line 136
        return chardet.detect(binary)["encoding"]  # line 136
except:  # Guess the encoding  # line 137
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 137
        ''' Fallback if chardet library missing. '''  # line 138
        try:  # line 139
            binary.decode(UTF8)  # line 139
            return UTF8  # line 139
        except UnicodeError:  # line 140
            pass  # line 140
        try:  # line 141
            binary.decode("utf_16")  # line 141
            return "utf_16"  # line 141
        except UnicodeError:  # line 142
            pass  # line 142
        try:  # line 143
            binary.decode("cp1252")  # line 143
            return "cp1252"  # line 143
        except UnicodeError:  # line 144
            pass  # line 144
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 145

def tryOrDefault(func: '_coconut.typing.Callable[..., Any]', default: 'Any') -> 'Any':  # line 147
    try:  # line 148
        return func()  # line 148
    except:  # line 149
        return default  # line 149

def tryOrIgnore(func: '_coconut.typing.Callable[..., Any]', onError: '_coconut.typing.Callable[[Exception], None]'=lambda _: None) -> 'Any':  # handle with care!  # line 151
    try:  # line 152
        return func()  # line 152
    except Exception as E:  # line 153
        onError(E)  # line 153

def removePath(key: 'str', value: 'str') -> 'str':  # line 155
    ''' Cleanup of user-specified global file patterns. '''  # TODO improve  # line 156
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 157

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 159
    d = {}  # type: Dict[Any, Any]  # line 159
    d.update(dikt)  # line 159
    d.update(by)  # line 159
    return d  # line 159

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # Abstraction for opening both compressed and plain files  # line 161
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # Abstraction for opening both compressed and plain files  # line 161

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 163
    ''' Determine EOL style from a binary string. '''  # line 164
    lf = file.count(b"\n")  # type: int  # line 165
    cr = file.count(b"\r")  # type: int  # line 166
    crlf = file.count(b"\r\n")  # type: int  # line 167
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 168
        if lf != crlf or cr != crlf:  # line 169
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 169
        return b"\r\n"  # line 170
    if lf != 0 and cr != 0:  # line 171
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 171
    if lf > cr:  # Linux/Unix  # line 172
        return b"\n"  # Linux/Unix  # line 172
    if cr > lf:  # older 8-bit machines  # line 173
        return b"\r"  # older 8-bit machines  # line 173
    return None  # no new line contained, cannot determine  # line 174

if TYPE_CHECKING:  # line 176
    Splittable = TypeVar("Splittable", AnyStr)  # line 177
    def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> 'List[Splittable]':  # line 178
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 178
else:  # line 179
    def safeSplit(s, d=None):  # line 180
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 180

@_coconut_tco  # line 182
def hashStr(datas: 'str') -> 'str':  # line 182
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 182

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 184
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 184

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 186
    return lizt[index:].index(what) + index  # line 186

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 188
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 188

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 190
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 190

def Exit(message: 'str'="", code=1):  # line 192
    printe("[EXIT%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "") + (" " + message + "." if message != "" else ""))  # line 192
    sys.exit(code)  # line 192

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 194
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar to xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 195
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 196
        raise Exception("Cannot possibly strings pack into specified length")  # line 196
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 197
        prefix += separator + ((process)(strings.pop(0)))  # line 197
    return prefix  # line 198

def exception(E):  # line 200
    ''' Report an exception to the user to enable useful bug reporting. '''  # line 201
    printo(str(E))  # line 202
    import traceback  # line 203
    traceback.print_exc()  # line 204
    traceback.print_stack()  # line 205

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None, callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 207
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 208
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 209
    _hash = hashlib.sha256()  # line 210
    wsize = 0  # type: int  # line 211
    if saveTo and os.path.exists(encode(saveTo)):  # line 212
        Exit("Hash conflict. Leaving revision in inconsistent state. This should happen only once in a lifetime")  # line 212
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 213
    with open(encode(path), "rb") as fd:  # line 214
        while True:  # line 215
            buffer = fd.read(bufSize)  # type: bytes  # line 216
            _hash.update(buffer)  # line 217
            if to:  # line 218
                to.write(buffer)  # line 218
            if len(buffer) < bufSize:  # line 219
                break  # line 219
            if indicator:  # line 220
                indicator.getIndicator()  # line 220
        if to:  # line 221
            to.close()  # line 222
            wsize = os.stat(encode(saveTo)).st_size  # line 223
    return (_hash.hexdigest(), wsize)  # line 224

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 226
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 227
    for k, v in map.items():  # line 228
        if k in params:  # line 228
            return v  # line 228
    return default  # line 229

@_coconut_tco  # line 231
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 231
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 231

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 233
    lines = []  # type: _coconut.typing.Sequence[str]  # line 234
    if filename is not None:  # line 235
        with open(encode(filename), "rb") as fd:  # line 235
            content = fd.read()  # line 235
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 236
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 237
    if filename is not None:  # line 238
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 238
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 238
    elif content is not None:  # line 239
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 239
    else:  # line 240
        return (sys.getdefaultencoding(), b"\n", [])  # line 240
    if ignoreWhitespace:  # line 241
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 241
    return (encoding, eol, lines)  # line 242

if TYPE_CHECKING:  # line 244
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 245
    @_coconut_tco  # line 246
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 246
        ''' A better makedata() version. '''  # line 247
        r = _old._asdict()  # type: Dict[str, Any]  # line 248
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 249
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 250
else:  # line 251
    @_coconut_tco  # line 252
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 252
        ''' A better makedata() version. '''  # line 253
        r = _old._asdict()  # line 254
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 255
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 256

def detectMoves(changes: 'ChangeSet') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 258
    ''' Compute renames/removes for a changeset. '''  # line 259
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 260
    for path, info in changes.additions.items():  # line 261
        for dpath, dinfo in changes.deletions.items():  # line 261
            if info.size == dinfo.size and info.mtime == dinfo.mtime and info.hash == dinfo.hash:  # was moved TODO check either mtime or hash?  # line 262
                moves[path] = (dpath, info)  # store new data and original name, but don't remove add/del  # line 263
                break  # deletions loop, continue with next addition  # line 264
    return moves  # line 265

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 267
    ''' Default can be a selection from choice and allows empty input. '''  # line 268
    while True:  # line 269
        selection = input(text).strip().lower()  # line 270
        if selection != "" and selection in choices:  # line 271
            break  # line 271
        if selection == "" and default is not None:  # line 272
            selection = default  # line 272
            break  # line 272
    return selection  # line 273

def user_block_input(output: 'List[str]'):  # line 275
    ''' Side-effect appending to input list. '''  # line 276
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 277
    line = sep  # type: str  # line 277
    while True:  # line 278
        line = input("> ")  # line 279
        if line == sep:  # line 280
            break  # line 280
        output.append(line)  # writes to caller-provided list reference  # line 281

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 283
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For update, the other version is assumed to be the "new/added" one, while for diff, the current changes are the ones "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly returns detected change blocks only, no text merging
      eol flag will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original
  '''  # line 298
    encoding = None  # type: str  # line 299
    othr = None  # type: _coconut.typing.Sequence[str]  # line 299
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 299
    curr = None  # type: _coconut.typing.Sequence[str]  # line 299
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 299
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 300
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 301
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 302
    except Exception as E:  # line 303
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 303
    if None not in [othreol, curreol] and othreol != curreol:  # line 304
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 304
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 305
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 306
    tmp = []  # type: List[str]  # block lines  # line 307
    last = " "  # type: str  # "into"-file offset for remark lines  # line 308
    no = None  # type: int  # "into"-file offset for remark lines  # line 308
    line = None  # type: str  # "into"-file offset for remark lines  # line 308
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 308
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 309
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 310
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 310
            continue  # continue filling current block, no matter what type of block it is  # line 310
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 311
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 311
        if last == " ":  # block is same in both files  # line 312
            if len(tmp) > 0:  # avoid adding empty keep block  # line 313
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 313
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 314
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 315
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 316
                offset += len(blocks[-2].lines)  # line 317
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 318
                blocks.pop()  # line 319
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 320
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 321
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 322
                offset += len(blocks[-1].lines)  # line 323
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 324
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 325
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 326
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 326
        last = line[0]  # line 327
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 328
# TODO add code to detect block moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 330
    debug("Diff blocks: " + repr(blocks))  # line 331
    if diffOnly:  # line 332
        return (blocks, nl)  # line 332

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 335
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 335
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 335
    selection = None  # type: str  # clean list of strings  # line 335
    for block in blocks:  # line 336
        if block.tipe == MergeBlockType.KEEP:  # line 337
            output.extend(block.lines)  # line 337
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 338
            output.extend(block.lines)  # line 340
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 341
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 342
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 343
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 344
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 345
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 346
                while True:  # line 347
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 348
                    if op in "tb":  # line 349
                        output.extend(block.lines)  # line 349
                    if op in "ib":  # line 350
                        output.extend(block.replaces.lines)  # line 350
                    if op == "u":  # line 351
                        user_block_input(output)  # line 351
                    if op in "tbiu":  # line 352
                        break  # line 352
            else:  # more than one line and not ask  # line 353
                if mergeOperation == MergeOperation.REMOVE:  # line 354
                    pass  # line 354
                elif mergeOperation == MergeOperation.BOTH:  # line 355
                    output.extend(block.lines)  # line 355
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 356
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 356
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 357
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 358
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 360
                if selection in "ao":  # line 361
                    if block.tipe == MergeBlockType.INSERT:  # line 362
                        add_all = "y" if selection == "a" else "n"  # line 362
                        selection = add_all  # line 362
                    else:  # REMOVE case  # line 363
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 363
                        selection = del_all  # REMOVE case  # line 363
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 364
                output.extend(block.lines)  # line 366
    debug("Merge output: " + "; ".join(output))  # line 367
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 368
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 371
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 371
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 374
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 375
    blocks = []  # type: List[MergeBlock]  # line 376
    for i, line in enumerate(out):  # line 377
        if line[0] == "+":  # line 378
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 379
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 380
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 381
                else:  # first + in block  # line 382
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 383
            else:  # last line of + block  # line 384
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 385
                    blocks[-1].lines.append(line[2])  # line 386
                else:  # single line  # line 387
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 388
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 389
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 390
                    blocks.pop()  # line 390
        elif line[0] == "-":  # line 391
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 392
                blocks[-1].lines.append(line[2])  # line 393
            else:  # first in block  # line 394
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 395
        elif line[0] == " ":  # line 396
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 397
                blocks[-1].lines.append(line[2])  # line 398
            else:  # first in block  # line 399
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 400
        else:  # line 401
            raise Exception("Cannot parse diff line %r" % line)  # line 401
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 402
    if diffOnly:  # line 403
        return blocks  # line 403
    out[:] = []  # line 404
    for i, block in enumerate(blocks):  # line 405
        if block.tipe == MergeBlockType.KEEP:  # line 406
            out.extend(block.lines)  # line 406
        elif block.tipe == MergeBlockType.REPLACE:  # line 407
            if mergeOperation == MergeOperation.ASK:  # line 408
                printo(pure.ajoin("- ", othr))  # line 409
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 410
                printo("+ " + (" " * i) + block.lines[0])  # line 411
                printo(pure.ajoin("+ ", into))  # line 412
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 413
                if op in "tb":  # line 414
                    out.extend(block.lines)  # line 414
                    break  # line 414
                if op in "ib":  # line 415
                    out.extend(block.replaces.lines)  # line 415
                    break  # line 415
                if op == "m":  # line 416
                    user_block_input(out)  # line 416
                    break  # line 416
            else:  # non-interactive  # line 417
                if mergeOperation == MergeOperation.REMOVE:  # line 418
                    pass  # line 418
                elif mergeOperation == MergeOperation.BOTH:  # line 419
                    out.extend(block.lines)  # line 419
                elif mergeOperation == MergeOperation.INSERT:  # line 420
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 420
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 421
            out.extend(block.lines)  # line 421
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 422
            out.extend(block.lines)  # line 422
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 424

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 426
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 429
    debug("Detecting root folders...")  # line 430
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 431
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 432
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 433
        contents = set(os.listdir(path))  # type: Set[str]  # line 434
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder  # line 435
        choice = None  # type: _coconut.typing.Optional[str]  # line 436
        if len(vcss) > 1:  # line 437
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 438
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 439
        elif len(vcss) > 0:  # line 440
            choice = vcss[0]  # line 440
        if not vcs[0] and choice:  # memorize current repo root  # line 441
            vcs = (path, choice)  # memorize current repo root  # line 441
        new = os.path.dirname(path)  # get parent path  # line 442
        if new == path:  # avoid infinite loop  # line 443
            break  # avoid infinite loop  # line 443
        path = new  # line 444
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 445
        if vcs[0]:  # already detected vcs base and command  # line 446
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 446
        sos = path  # line 447
        while True:  # continue search for VCS base  # line 448
            new = os.path.dirname(path)  # get parent path  # line 449
            if new == path:  # no VCS folder found  # line 450
                return (sos, None, None)  # no VCS folder found  # line 450
            path = new  # line 451
            contents = set(os.listdir(path))  # line 452
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 453
            choice = None  # line 454
            if len(vcss) > 1:  # line 455
                choice = SVN if SVN in vcss else vcss[0]  # line 456
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 457
            elif len(vcss) > 0:  # line 458
                choice = vcss[0]  # line 458
            if choice:  # line 459
                return (sos, path, choice)  # line 459
    return (None, vcs[0], vcs[1])  # line 460

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 462
    index = 0  # type: int  # line 463
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 464
    while index < len(pattern):  # line 465
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 466
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 466
            continue  # line 466
        if pattern[index] in "*?":  # line 467
            count = 1  # type: int  # line 468
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 469
                count += 1  # line 469
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 470
            index += count  # line 470
            continue  # line 470
        if pattern[index:index + 2] == "[!":  # line 471
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 471
            index += len(out[-1][1])  # line 471
            continue  # line 471
        count = 1  # line 472
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 473
            count += 1  # line 473
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 474
        index += count  # line 474
    return out  # line 475

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 477
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 478
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 479
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 481
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 481
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 482
        Exit("Source and target file patterns differ in semantics")  # line 482
    return (ot, nt)  # line 483

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 485
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 486
    pairs = []  # type: List[Tuple[str, str]]  # line 487
    for filename in filenames:  # line 488
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 489
        nextliteral = 0  # type: int  # line 490
        index = 0  # type: int  # line 490
        parsedOld = []  # type: List[GlobBlock2]  # line 491
        for part in oldPattern:  # match everything in the old filename  # line 492
            if part.isLiteral:  # line 493
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 493
                index += len(part.content)  # line 493
                nextliteral += 1  # line 493
            elif part.content.startswith("?"):  # line 494
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 494
                index += len(part.content)  # line 494
            elif part.content.startswith("["):  # line 495
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 495
                index += 1  # line 495
            elif part.content == "*":  # line 496
                if nextliteral >= len(literals):  # line 497
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 497
                    break  # line 497
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 498
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 499
                index = nxt  # line 499
            else:  # line 500
                Exit("Invalid file pattern specified for move/rename")  # line 500
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 501
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 502
        nextliteral = 0  # line 503
        nextglob = 0  # type: int  # line 503
        outname = []  # type: List[str]  # line 504
        for part in newPattern:  # generate new filename  # line 505
            if part.isLiteral:  # line 506
                outname.append(literals[nextliteral].content)  # line 506
                nextliteral += 1  # line 506
            else:  # line 507
                outname.append(globs[nextglob].matches)  # line 507
                nextglob += 1  # line 507
        pairs.append((filename, "".join(outname)))  # line 508
    return pairs  # line 509

@_coconut_tco  # line 511
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 511
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 515
    if not actions:  # line 516
        return []  # line 516
    sources = None  # type: List[str]  # line 517
    targets = None  # type: List[str]  # line 517
    sources, targets = [list(l) for l in zip(*actions)]  # line 518
    last = len(actions)  # type: int  # line 519
    while last > 1:  # line 520
        clean = True  # type: bool  # line 521
        for i in range(1, last):  # line 522
            try:  # line 523
                index = targets[:i].index(sources[i])  # type: int  # line 524
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 525
                targets.insert(index, targets.pop(i))  # line 526
                clean = False  # line 527
            except:  # target not found in sources: good!  # line 528
                continue  # target not found in sources: good!  # line 528
        if clean:  # line 529
            break  # line 529
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 530
    if exitOnConflict:  # line 531
        for i in range(1, len(actions)):  # line 531
            if sources[i] in targets[:i]:  # line 531
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 531
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 532

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 534
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 535
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 536
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 537

def parseOnlyOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 539
    ''' Returns (root-normalized) set of --only arguments, and set or --except arguments. '''  # line 540
    root = os.getcwd()  # type: str  # line 541
    onlys = []  # type: List[str]  # zero necessary as last start position  # line 542
    excps = []  # type: List[str]  # zero necessary as last start position  # line 542
    index = 0  # type: int  # zero necessary as last start position  # line 542
    while True:  # line 543
        try:  # line 544
            index = 1 + listindex(options, "--only", index)  # line 545
            onlys.append(options[index])  # line 546
            del options[index]  # line 547
            del options[index - 1]  # line 548
        except:  # line 549
            break  # line 549
    index = 0  # line 550
    while True:  # line 551
        try:  # line 552
            index = 1 + listindex(options, "--except", index)  # line 553
            excps.append(options[index])  # line 554
            del options[index]  # line 555
            del options[index - 1]  # line 556
        except:  # line 557
            break  # line 557
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(".." + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(".." + SLASH))) if excps else None)  # avoids out-of-repo paths  # line 558
