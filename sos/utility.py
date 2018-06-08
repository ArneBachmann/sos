#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xfff19d7d

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
    from sos import pure  # line 10
    from sos.values import *  # line 10
except:  # line 11
    import pure  # line 11
    from values import *  # line 11


# Lazy imports for quicker initialization TODO make mypy pass
bz2 = None  # type: Any  # line 15
codecs = None  # type: Any  # line 15
difflib = None  # type: Any  # line 15
class bz2:  # line 16
    @_coconut_tco  # line 16
    def __getattribute__(_, key):  # line 16
        global bz2  # line 17
        import bz2  # line 18
        return _coconut_tail_call(bz2.__getattribute__, key)  # line 19
bz2 = bz2()  # type: object  # line 20

class codecs:  # line 22
    @_coconut_tco  # line 22
    def __getattribute__(_, key):  # line 22
        global codecs  # line 23
        import codecs  # line 24
        return _coconut_tail_call(codecs.__getattribute__, key)  # line 25
codecs = codecs()  # type: object  # line 26

class difflib:  # line 28
    @_coconut_tco  # line 28
    def __getattribute__(_, key):  # line 28
        global difflib  # line 29
        import difflib  # line 30
        return _coconut_tail_call(difflib.__getattribute__, key)  # line 31
difflib = difflib()  # type: object  # line 32


verbose = '--verbose' in sys.argv or '-v' in sys.argv  # type: bool  # line 35
debug_ = os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv  # type: bool  # line 36


# Classes
class Accessor(dict):  # line 40
    ''' Dictionary with attribute access. Writing only supported via dictionary access. '''  # line 41
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # TODO remove -> None when fixed in Coconut stub  # line 42
        dict.__init__(_, mapping)  # TODO remove -> None when fixed in Coconut stub  # line 42
    @_coconut_tco  # or simply class C(dict): __getattr__ = dict.__getitem__  # line 43
    def __getattribute__(_, name: 'str') -> 'Any':  # or simply class C(dict): __getattr__ = dict.__getitem__  # line 43
        try:  # line 44
            return _[name]  # line 44
        except:  # line 45
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 45

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 47
    Number = TypeVar("Number", int, float)  # line 48
    class Counter(Generic[Number]):  # line 49
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 50
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 51
            _.value = initial  # type: Number  # line 51
        def inc(_, by: 'Number'=1) -> 'Number':  # line 52
            _.value += by  # line 52
            return _.value  # line 52
else:  # line 53
    class Counter:  # line 54
        def __init__(_, initial=0) -> 'None':  # line 55
            _.value = initial  # line 55
        def inc(_, by=1):  # line 56
            _.value += by  # line 56
            return _.value  # line 56

class ProgressIndicator(Counter):  # line 58
    ''' Manages a rotating progress indicator. '''  # line 59
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 60
        super(ProgressIndicator, _).__init__(-1)  # line 60
        _.symbols = symbols  # line 60
        _.timer = time.time()  # type: float  # line 60
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 60
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 61
        ''' Returns a value only if a certain time has passed. '''  # line 62
        newtime = time.time()  # type: float  # line 63
        if newtime - _.timer < .1:  # line 64
            return None  # line 64
        _.timer = newtime  # line 65
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 66
        if _.callback:  # line 67
            _.callback(sign)  # line 67
        return sign  # line 68

class Logger:  # line 70
    ''' Logger that supports joining many items. '''  # line 71
    def __init__(_, log) -> 'None':  # line 72
        _._log = log  # line 72
    def debug(_, *s):  # line 73
        _._log.debug(pure.sjoin(*s))  # line 73
    def info(_, *s):  # line 74
        _._log.info(pure.sjoin(*s))  # line 74
    def warn(_, *s):  # line 75
        _._log.warning(pure.sjoin(*s))  # line 75
    def error(_, *s):  # line 76
        _._log.error(pure.sjoin(*s))  # line 76


# Constants
_log = Logger(logging.getLogger(__name__))  # line 80
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 80
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress", "useChangesCommand", "useUnicodeFont"]  # type: List[str]  # line 81
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 82
CONFIGURABLE_INTS = ["logLines"]  # type: List[str]  # line 83
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 84
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 85
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 86
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 87
BACKUP_SUFFIX = "_last"  # type: str  # line 88
metaFolder = ".sos"  # type: str  # line 89
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 90
metaFile = ".meta"  # type: str  # line 91
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 92
KIBI = 1 << 10  # type: int  # line 93
MEBI = 1 << 20  # type: int  # line 93
GIBI = 1 << 30  # type: int  # line 93
bufSize = MEBI  # type: int  # line 94
UTF8 = "utf_8"  # type: str  # early used constant, not defined in standard library  # line 95
SVN = "svn"  # type: str  # line 96
SLASH = "/"  # type: str  # line 97
DOT_SYMBOL = "\u00b7"  # type: str  # line 98
MULT_SYMBOL = "\u00d7"  # type: str  # line 99
CROSS_SYMBOL = "\u2716"  # type: str  # line 100
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 101
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 102
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in "this revision"  # line 103
MOVE_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 104
METADATA_FORMAT = 1  # type: int  # counter for incompatible consecutive formats (was undefined, "1" is the first versioned version after that)  # line 105
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 106
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 107
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS, RCS have probably different per-file operation  # line 108
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 109
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[bytes, str]  # line 110
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[str, int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 111
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE], "ignoresWhitelist": []})  # type: Accessor  # line 112


# Functions
def printo(s: 'str'="", nl: 'str'="\n"):  # PEP528 compatibility  # line 125
    tryOrDefault(lambda _=None: (lambda _coconut_none_coalesce_item: sys.stdout if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(sys.stdout.buffer), sys.stdout).write((s + nl).encode(sys.stdout.encoding, 'backslashreplace'))  # PEP528 compatibility  # line 125
    sys.stdout.flush()  # PEP528 compatibility  # line 125
def printe(s: 'str'="", nl: 'str'="\n"):  # line 126
    tryOrDefault(lambda _=None: (lambda _coconut_none_coalesce_item: sys.stderr if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(sys.stderr.buffer), sys.stderr).write((s + nl).encode(sys.stderr.encoding, 'backslashreplace'))  # line 126
    sys.stderr.flush()  # line 126
@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 127
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 127
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 127
@_coconut_tco  # for os->py access of reading filenames  # line 128
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 128
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 128
try:  # line 129
    import chardet  # https://github.com/chardet/chardet  # line 130
    def detectEncoding(binary: 'bytes') -> 'str':  # line 131
        return chardet.detect(binary)["encoding"]  # line 131
except:  # Guess the encoding  # line 132
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 132
        ''' Fallback if chardet library missing. '''  # line 133
        try:  # line 134
            binary.decode(UTF8)  # line 134
            return UTF8  # line 134
        except UnicodeError:  # line 135
            pass  # line 135
        try:  # line 136
            binary.decode("utf_16")  # line 136
            return "utf_16"  # line 136
        except UnicodeError:  # line 137
            pass  # line 137
        try:  # line 138
            binary.decode("cp1252")  # line 138
            return "cp1252"  # line 138
        except UnicodeError:  # line 139
            pass  # line 139
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 140

def tryOrDefault(func: '_coconut.typing.Callable[..., Any]', default: 'Any') -> 'Any':  # line 142
    try:  # line 143
        return func()  # line 143
    except:  # line 144
        return default  # line 144

def tryOrIgnore(func: '_coconut.typing.Callable[..., Any]', onError: '_coconut.typing.Callable[[Exception], None]'=lambda _=None: None) -> 'Any':  # line 146
    try:  # line 147
        return func()  # line 147
    except Exception as E:  # line 148
        onError(E)  # line 148

def removePath(key: 'str', value: 'str') -> 'str':  # line 150
    ''' Cleanup of user-specified global file patterns. '''  # TODO improve  # line 151
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 152

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 154
    d = {}  # type: Dict[Any, Any]  # line 154
    d.update(dikt)  # line 154
    d.update(by)  # line 154
    return d  # line 154

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # Abstraction for opening both compressed and plain files  # line 156
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # Abstraction for opening both compressed and plain files  # line 156

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 158
    ''' Determine EOL style from a binary string. '''  # line 159
    lf = file.count(b"\n")  # type: int  # line 160
    cr = file.count(b"\r")  # type: int  # line 161
    crlf = file.count(b"\r\n")  # type: int  # line 162
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 163
        if lf != crlf or cr != crlf:  # line 164
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 164
        return b"\r\n"  # line 165
    if lf != 0 and cr != 0:  # line 166
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 166
    if lf > cr:  # Linux/Unix  # line 167
        return b"\n"  # Linux/Unix  # line 167
    if cr > lf:  # older 8-bit machines  # line 168
        return b"\r"  # older 8-bit machines  # line 168
    return None  # no new line contained, cannot determine  # line 169

if TYPE_CHECKING:  # line 171
    Splittable = TypeVar("Splittable", AnyStr)  # line 172
    def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> 'List[Splittable]':  # line 173
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 173
else:  # line 174
    def safeSplit(s, d=None):  # line 175
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 175

@_coconut_tco  # line 177
def hashStr(datas: 'str') -> 'str':  # line 177
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 177

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 179
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 179

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 181
    return lizt[index:].index(what) + index  # line 181

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 183
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 183

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 185
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 185

def Exit(message: 'str'="", code=1):  # line 187
    printe("[EXIT%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "") + (" " + message + "." if message != "" else ""))  # line 187
    sys.exit(code)  # line 187

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 189
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 190
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 191
        raise Exception("Cannot possibly strings pack into specified length")  # line 191
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 192
        prefix += separator + ((process)(strings.pop(0)))  # line 192
    return prefix  # line 193

def exception(E):  # line 195
    ''' Report an exception to the user to enable useful bug reporting. '''  # line 196
    printo(str(E))  # line 197
    import traceback  # line 198
    traceback.print_exc()  # line 199
    traceback.print_stack()  # line 200

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None, callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 202
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 203
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 204
    _hash = hashlib.sha256()  # line 205
    wsize = 0  # type: int  # line 206
    if saveTo and os.path.exists(encode(saveTo)):  # line 207
        Exit("Hash conflict. Leaving revision in inconsistent state. This should happen only once in a lifetime")  # line 207
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 208
    with open(encode(path), "rb") as fd:  # line 209
        while True:  # line 210
            buffer = fd.read(bufSize)  # type: bytes  # line 211
            _hash.update(buffer)  # line 212
            if to:  # line 213
                to.write(buffer)  # line 213
            if len(buffer) < bufSize:  # line 214
                break  # line 214
            if indicator:  # line 215
                indicator.getIndicator()  # line 215
        if to:  # line 216
            to.close()  # line 217
            wsize = os.stat(encode(saveTo)).st_size  # line 218
    return (_hash.hexdigest(), wsize)  # line 219

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 221
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 222
    for k, v in map.items():  # line 223
        if k in params:  # line 223
            return v  # line 223
    return default  # line 224

@_coconut_tco  # line 226
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 226
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 226

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 228
    lines = []  # type: _coconut.typing.Sequence[str]  # line 229
    if filename is not None:  # line 230
        with open(encode(filename), "rb") as fd:  # line 230
            content = fd.read()  # line 230
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 231
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 232
    if filename is not None:  # line 233
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 233
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 233
    elif content is not None:  # line 234
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 234
    else:  # line 235
        return (sys.getdefaultencoding(), b"\n", [])  # line 235
    if ignoreWhitespace:  # line 236
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 236
    return (encoding, eol, lines)  # line 237

if TYPE_CHECKING:  # line 239
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 240
    @_coconut_tco  # line 241
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 241
        ''' A better makedata() version. '''  # line 242
        r = _old._asdict()  # type: Dict[str, Any]  # line 243
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 244
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 245
else:  # line 246
    @_coconut_tco  # line 247
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 247
        ''' A better makedata() version. '''  # line 248
        r = _old._asdict()  # line 249
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 250
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 251

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 253
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 254
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 255
    for path, info in changes.additions.items():  # line 256
        for dpath, dinfo in changes.deletions.items():  # line 256
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 257
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 258
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 259
                break  # deletions loop, continue with next addition  # line 260
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 261

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 263
    ''' Default can be a selection from choice and allows empty input. '''  # line 264
    while True:  # line 265
        selection = input(text).strip().lower()  # line 266
        if selection != "" and selection in choices:  # line 267
            break  # line 267
        if selection == "" and default is not None:  # line 268
            selection = default  # line 268
            break  # line 268
    return selection  # line 269

def user_block_input(output: 'List[str]'):  # line 271
    ''' Side-effect appending to input list. '''  # line 272
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 273
    line = sep  # type: str  # line 273
    while True:  # line 274
        line = input("> ")  # line 275
        if line == sep:  # line 276
            break  # line 276
        output.append(line)  # writes to caller-provided list reference  # line 277

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 279
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 294
    encoding = None  # type: str  # line 295
    othr = None  # type: _coconut.typing.Sequence[str]  # line 295
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 295
    curr = None  # type: _coconut.typing.Sequence[str]  # line 295
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 295
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 296
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 297
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 298
    except Exception as E:  # line 299
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 299
    if None not in [othreol, curreol] and othreol != curreol:  # line 300
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 300
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 301
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 302
    tmp = []  # type: List[str]  # block lines  # line 303
    last = " "  # type: str  # "into"-file offset for remark lines  # line 304
    no = None  # type: int  # "into"-file offset for remark lines  # line 304
    line = None  # type: str  # "into"-file offset for remark lines  # line 304
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 304
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 305
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 306
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 306
            continue  # continue filling current block, no matter what type of block it is  # line 306
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 307
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 307
        if last == " ":  # block is same in both files  # line 308
            if len(tmp) > 0:  # avoid adding empty keep block  # line 309
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 309
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 310
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 311
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 312
                offset += len(blocks[-2].lines)  # line 313
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 314
                blocks.pop()  # line 315
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 316
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 317
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 318
                offset += len(blocks[-1].lines)  # line 319
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 320
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 321
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 322
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 322
        last = line[0]  # line 323
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 324
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 326
    debug("Diff blocks: " + repr(blocks))  # line 327
    if diffOnly:  # line 328
        return (blocks, nl)  # line 328

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 331
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 331
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 331
    selection = None  # type: str  # clean list of strings  # line 331
    for block in blocks:  # line 332
        if block.tipe == MergeBlockType.KEEP:  # line 333
            output.extend(block.lines)  # line 333
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 334
            output.extend(block.lines)  # line 336
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 337
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 338
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 339
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 340
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 341
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 342
                while True:  # line 343
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 344
                    if op in "tb":  # line 345
                        output.extend(block.lines)  # line 345
                    if op in "ib":  # line 346
                        output.extend(block.replaces.lines)  # line 346
                    if op == "u":  # line 347
                        user_block_input(output)  # line 347
                    if op in "tbiu":  # line 348
                        break  # line 348
            else:  # more than one line and not ask  # line 349
                if mergeOperation == MergeOperation.REMOVE:  # line 350
                    pass  # line 350
                elif mergeOperation == MergeOperation.BOTH:  # line 351
                    output.extend(block.lines)  # line 351
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 352
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 352
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 353
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 354
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 356
                if selection in "ao":  # line 357
                    if block.tipe == MergeBlockType.INSERT:  # line 358
                        add_all = "y" if selection == "a" else "n"  # line 358
                        selection = add_all  # line 358
                    else:  # REMOVE case  # line 359
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 359
                        selection = del_all  # REMOVE case  # line 359
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 360
                output.extend(block.lines)  # line 362
    debug("Merge output: " + "; ".join(output))  # line 363
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 364
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 367
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 367
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 370
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 371
    blocks = []  # type: List[MergeBlock]  # line 372
    for i, line in enumerate(out):  # line 373
        if line[0] == "+":  # line 374
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 375
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 376
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 377
                else:  # first + in block  # line 378
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 379
            else:  # last line of + block  # line 380
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 381
                    blocks[-1].lines.append(line[2])  # line 382
                else:  # single line  # line 383
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 384
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 385
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 386
                    blocks.pop()  # line 386
        elif line[0] == "-":  # line 387
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 388
                blocks[-1].lines.append(line[2])  # line 389
            else:  # first in block  # line 390
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 391
        elif line[0] == " ":  # line 392
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 393
                blocks[-1].lines.append(line[2])  # line 394
            else:  # first in block  # line 395
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 396
        else:  # line 397
            raise Exception("Cannot parse diff line %r" % line)  # line 397
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 398
    if diffOnly:  # line 399
        return blocks  # line 399
    out[:] = []  # line 400
    for i, block in enumerate(blocks):  # line 401
        if block.tipe == MergeBlockType.KEEP:  # line 402
            out.extend(block.lines)  # line 402
        elif block.tipe == MergeBlockType.REPLACE:  # line 403
            if mergeOperation == MergeOperation.ASK:  # line 404
                printo(pure.ajoin("- ", othr))  # line 405
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 406
                printo("+ " + (" " * i) + block.lines[0])  # line 407
                printo(pure.ajoin("+ ", into))  # line 408
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 409
                if op in "tb":  # line 410
                    out.extend(block.lines)  # line 410
                    break  # line 410
                if op in "ib":  # line 411
                    out.extend(block.replaces.lines)  # line 411
                    break  # line 411
                if op == "m":  # line 412
                    user_block_input(out)  # line 412
                    break  # line 412
            else:  # non-interactive  # line 413
                if mergeOperation == MergeOperation.REMOVE:  # line 414
                    pass  # line 414
                elif mergeOperation == MergeOperation.BOTH:  # line 415
                    out.extend(block.lines)  # line 415
                elif mergeOperation == MergeOperation.INSERT:  # line 416
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 416
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 417
            out.extend(block.lines)  # line 417
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 418
            out.extend(block.lines)  # line 418
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 420

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 422
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 425
    debug("Detecting root folders...")  # line 426
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 427
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 428
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 429
        contents = set(os.listdir(path))  # type: Set[str]  # line 430
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder  # line 431
        choice = None  # type: _coconut.typing.Optional[str]  # line 432
        if len(vcss) > 1:  # line 433
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 434
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 435
        elif len(vcss) > 0:  # line 436
            choice = vcss[0]  # line 436
        if not vcs[0] and choice:  # memorize current repo root  # line 437
            vcs = (path, choice)  # memorize current repo root  # line 437
        new = os.path.dirname(path)  # get parent path  # line 438
        if new == path:  # avoid infinite loop  # line 439
            break  # avoid infinite loop  # line 439
        path = new  # line 440
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 441
        if vcs[0]:  # already detected vcs base and command  # line 442
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 442
        sos = path  # line 443
        while True:  # continue search for VCS base  # line 444
            contents = set(os.listdir(path))  # line 445
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 446
            choice = None  # line 447
            if len(vcss) > 1:  # line 448
                choice = SVN if SVN in vcss else vcss[0]  # line 449
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 450
            elif len(vcss) > 0:  # line 451
                choice = vcss[0]  # line 451
            if choice:  # line 452
                return (sos, path, choice)  # line 452
            new = os.path.dirname(path)  # get parent path  # line 453
            if new == path:  # no VCS folder found  # line 454
                return (sos, None, None)  # no VCS folder found  # line 454
            path = new  # line 455
    return (None, vcs[0], vcs[1])  # line 456

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 458
    index = 0  # type: int  # line 459
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 460
    while index < len(pattern):  # line 461
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 462
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 462
            continue  # line 462
        if pattern[index] in "*?":  # line 463
            count = 1  # type: int  # line 464
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 465
                count += 1  # line 465
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 466
            index += count  # line 466
            continue  # line 466
        if pattern[index:index + 2] == "[!":  # line 467
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 467
            index += len(out[-1][1])  # line 467
            continue  # line 467
        count = 1  # line 468
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 469
            count += 1  # line 469
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 470
        index += count  # line 470
    return out  # line 471

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 473
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 474
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 475
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 477
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 477
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 478
        Exit("Source and target file patterns differ in semantics")  # line 478
    return (ot, nt)  # line 479

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 481
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 482
    pairs = []  # type: List[Tuple[str, str]]  # line 483
    for filename in filenames:  # line 484
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 485
        nextliteral = 0  # type: int  # line 486
        index = 0  # type: int  # line 486
        parsedOld = []  # type: List[GlobBlock2]  # line 487
        for part in oldPattern:  # match everything in the old filename  # line 488
            if part.isLiteral:  # line 489
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 489
                index += len(part.content)  # line 489
                nextliteral += 1  # line 489
            elif part.content.startswith("?"):  # line 490
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 490
                index += len(part.content)  # line 490
            elif part.content.startswith("["):  # line 491
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 491
                index += 1  # line 491
            elif part.content == "*":  # line 492
                if nextliteral >= len(literals):  # line 493
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 493
                    break  # line 493
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 494
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 495
                index = nxt  # line 495
            else:  # line 496
                Exit("Invalid file pattern specified for move/rename")  # line 496
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 497
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 498
        nextliteral = 0  # line 499
        nextglob = 0  # type: int  # line 499
        outname = []  # type: List[str]  # line 500
        for part in newPattern:  # generate new filename  # line 501
            if part.isLiteral:  # line 502
                outname.append(literals[nextliteral].content)  # line 502
                nextliteral += 1  # line 502
            else:  # line 503
                outname.append(globs[nextglob].matches)  # line 503
                nextglob += 1  # line 503
        pairs.append((filename, "".join(outname)))  # line 504
    return pairs  # line 505

@_coconut_tco  # line 507
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 507
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 511
    if not actions:  # line 512
        return []  # line 512
    sources = None  # type: List[str]  # line 513
    targets = None  # type: List[str]  # line 513
    sources, targets = [list(l) for l in zip(*actions)]  # line 514
    last = len(actions)  # type: int  # line 515
    while last > 1:  # line 516
        clean = True  # type: bool  # line 517
        for i in range(1, last):  # line 518
            try:  # line 519
                index = targets[:i].index(sources[i])  # type: int  # line 520
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 521
                targets.insert(index, targets.pop(i))  # line 522
                clean = False  # line 523
            except:  # target not found in sources: good!  # line 524
                continue  # target not found in sources: good!  # line 524
        if clean:  # line 525
            break  # line 525
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 526
    if exitOnConflict:  # line 527
        for i in range(1, len(actions)):  # line 527
            if sources[i] in targets[:i]:  # line 527
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 527
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 528

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 530
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 531
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 532
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 533

def parseOnlyOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 535
    ''' Returns (root-normalized) set of --only arguments, and set or --except arguments. '''  # line 536
    root = os.getcwd()  # type: str  # line 537
    onlys = []  # type: List[str]  # zero necessary as last start position  # line 538
    excps = []  # type: List[str]  # zero necessary as last start position  # line 538
    index = 0  # type: int  # zero necessary as last start position  # line 538
    while True:  # line 539
        try:  # line 540
            index = 1 + listindex(options, "--only", index)  # line 541
            onlys.append(options[index])  # line 542
            del options[index]  # line 543
            del options[index - 1]  # line 544
        except:  # line 545
            break  # line 545
    index = 0  # line 546
    while True:  # line 547
        try:  # line 548
            index = 1 + listindex(options, "--except", index)  # line 549
            excps.append(options[index])  # line 550
            del options[index]  # line 551
            del options[index - 1]  # line 552
        except:  # line 553
            break  # line 553
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(".." + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(".." + SLASH))) if excps else None)  # avoids out-of-repo paths  # line 554
