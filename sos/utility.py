#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xbe778104

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
    @_coconut_tco  # line 43
    def __getattribute__(_, name: 'str') -> 'Any':  # line 43
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
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # line 102
MOVE_SYMBOL = "\u21cc"  # type: str  # \U0001F5C0"  # HINT second one is very unlikely to be in any console font  # line 103
METADATA_FORMAT = 1  # type: int  # counter for incompatible consecutive formats (was undefined, "1" is the first versioned version after that)  # line 104
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 105
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 106
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS, RCS have probably different per-file operation  # line 107
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 108
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[bytes, str]  # line 109
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[str, int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 110
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE], "ignoresWhitelist": []})  # type: Accessor  # line 111


# Functions
def printo(s: 'str'="", nl: 'str'="\n"):  # PEP528 compatibility  # line 124
    tryOrDefault(lambda _=None: (lambda _coconut_none_coalesce_item: sys.stdout if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(sys.stdout.buffer), sys.stdout).write((s + nl).encode(sys.stdout.encoding, 'backslashreplace'))  # PEP528 compatibility  # line 124
    sys.stdout.flush()  # PEP528 compatibility  # line 124
def printe(s: 'str'="", nl: 'str'="\n"):  # line 125
    tryOrDefault(lambda _=None: (lambda _coconut_none_coalesce_item: sys.stderr if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(sys.stderr.buffer), sys.stderr).write((s + nl).encode(sys.stderr.encoding, 'backslashreplace'))  # line 125
    sys.stderr.flush()  # line 125
@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 126
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 126
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 126
@_coconut_tco  # for os->py access of reading filenames  # line 127
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 127
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 127
try:  # line 128
    import chardet  # https://github.com/chardet/chardet  # line 129
    def detectEncoding(binary: 'bytes') -> 'str':  # line 130
        return chardet.detect(binary)["encoding"]  # line 130
except:  # Guess the encoding  # line 131
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 131
        ''' Fallback if chardet library missing. '''  # line 132
        try:  # line 133
            binary.decode(UTF8)  # line 133
            return UTF8  # line 133
        except UnicodeError:  # line 134
            pass  # line 134
        try:  # line 135
            binary.decode("utf_16")  # line 135
            return "utf_16"  # line 135
        except UnicodeError:  # line 136
            pass  # line 136
        try:  # line 137
            binary.decode("cp1252")  # line 137
            return "cp1252"  # line 137
        except UnicodeError:  # line 138
            pass  # line 138
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 139

def tryOrDefault(func: '_coconut.typing.Callable[..., Any]', default: 'Any') -> 'Any':  # line 141
    try:  # line 142
        return func()  # line 142
    except:  # line 143
        return default  # line 143

def tryOrIgnore(func: '_coconut.typing.Callable[..., Any]', onError: '_coconut.typing.Callable[[Exception], None]'=lambda _=None: None) -> 'Any':  # line 145
    try:  # line 146
        return func()  # line 146
    except Exception as E:  # line 147
        onError(E)  # line 147

def removePath(key: 'str', value: 'str') -> 'str':  # line 149
    ''' Cleanup of user-specified global file patterns. '''  # TODO improve  # line 150
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 151

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 153
    d = {}  # type: Dict[Any, Any]  # line 153
    d.update(dikt)  # line 153
    d.update(by)  # line 153
    return d  # line 153

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # Abstraction for opening both compressed and plain files  # line 155
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # Abstraction for opening both compressed and plain files  # line 155

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 157
    ''' Determine EOL style from a binary string. '''  # line 158
    lf = file.count(b"\n")  # type: int  # line 159
    cr = file.count(b"\r")  # type: int  # line 160
    crlf = file.count(b"\r\n")  # type: int  # line 161
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 162
        if lf != crlf or cr != crlf:  # line 163
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 163
        return b"\r\n"  # line 164
    if lf != 0 and cr != 0:  # line 165
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 165
    if lf > cr:  # Linux/Unix  # line 166
        return b"\n"  # Linux/Unix  # line 166
    if cr > lf:  # older 8-bit machines  # line 167
        return b"\r"  # older 8-bit machines  # line 167
    return None  # no new line contained, cannot determine  # line 168

if TYPE_CHECKING:  # line 170
    Splittable = TypeVar("Splittable", AnyStr)  # line 171
    def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> 'List[Splittable]':  # line 172
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 172
else:  # line 173
    def safeSplit(s, d=None):  # line 174
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 174

@_coconut_tco  # line 176
def hashStr(datas: 'str') -> 'str':  # line 176
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 176

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 178
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 178

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 180
    return lizt[index:].index(what) + index  # line 180

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 182
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 182

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 184
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 184

def Exit(message: 'str'="", code=1):  # line 186
    printe("[EXIT%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "") + (" " + message + "." if message != "" else ""))  # line 186
    sys.exit(code)  # line 186

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 188
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar to xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 189
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 190
        raise Exception("Cannot possibly strings pack into specified length")  # line 190
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 191
        prefix += separator + ((process)(strings.pop(0)))  # line 191
    return prefix  # line 192

def exception(E):  # line 194
    ''' Report an exception to the user to enable useful bug reporting. '''  # line 195
    printo(str(E))  # line 196
    import traceback  # line 197
    traceback.print_exc()  # line 198
    traceback.print_stack()  # line 199

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None, callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 201
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 202
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 203
    _hash = hashlib.sha256()  # line 204
    wsize = 0  # type: int  # line 205
    if saveTo and os.path.exists(encode(saveTo)):  # line 206
        Exit("Hash conflict. Leaving revision in inconsistent state. This should happen only once in a lifetime")  # line 206
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 207
    with open(encode(path), "rb") as fd:  # line 208
        while True:  # line 209
            buffer = fd.read(bufSize)  # type: bytes  # line 210
            _hash.update(buffer)  # line 211
            if to:  # line 212
                to.write(buffer)  # line 212
            if len(buffer) < bufSize:  # line 213
                break  # line 213
            if indicator:  # line 214
                indicator.getIndicator()  # line 214
        if to:  # line 215
            to.close()  # line 216
            wsize = os.stat(encode(saveTo)).st_size  # line 217
    return (_hash.hexdigest(), wsize)  # line 218

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 220
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 221
    for k, v in map.items():  # line 222
        if k in params:  # line 222
            return v  # line 222
    return default  # line 223

@_coconut_tco  # line 225
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 225
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 225

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 227
    lines = []  # type: _coconut.typing.Sequence[str]  # line 228
    if filename is not None:  # line 229
        with open(encode(filename), "rb") as fd:  # line 229
            content = fd.read()  # line 229
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 230
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 231
    if filename is not None:  # line 232
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 232
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 232
    elif content is not None:  # line 233
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 233
    else:  # line 234
        return (sys.getdefaultencoding(), b"\n", [])  # line 234
    if ignoreWhitespace:  # line 235
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 235
    return (encoding, eol, lines)  # line 236

if TYPE_CHECKING:  # line 238
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 239
    @_coconut_tco  # line 240
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 240
        ''' A better makedata() version. '''  # line 241
        r = _old._asdict()  # type: Dict[str, Any]  # line 242
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 243
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 244
else:  # line 245
    @_coconut_tco  # line 246
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 246
        ''' A better makedata() version. '''  # line 247
        r = _old._asdict()  # line 248
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 249
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 250

def detectMoves(changes: 'ChangeSet') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 252
    ''' Compute renames/removes for a changeset. '''  # line 253
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 254
    for path, info in changes.additions.items():  # line 255
        for dpath, dinfo in changes.deletions.items():  # line 255
            if info.size == dinfo.size and info.mtime == dinfo.mtime and info.hash == dinfo.hash:  # was moved TODO check either mtime or hash?  # line 256
                moves[path] = (dpath, info)  # store new data and original name, but don't remove add/del  # line 257
                break  # deletions loop, continue with next addition  # line 258
    return moves  # line 259

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 261
    ''' Default can be a selection from choice and allows empty input. '''  # line 262
    while True:  # line 263
        selection = input(text).strip().lower()  # line 264
        if selection != "" and selection in choices:  # line 265
            break  # line 265
        if selection == "" and default is not None:  # line 266
            selection = default  # line 266
            break  # line 266
    return selection  # line 267

def user_block_input(output: 'List[str]'):  # line 269
    ''' Side-effect appending to input list. '''  # line 270
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 271
    line = sep  # type: str  # line 271
    while True:  # line 272
        line = input("> ")  # line 273
        if line == sep:  # line 274
            break  # line 274
        output.append(line)  # writes to caller-provided list reference  # line 275

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 277
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For update, the other version is assumed to be the "new/added" one, while for diff, the current changes are the ones "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly returns detected change blocks only, no text merging
      eol flag will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original
  '''  # line 292
    encoding = None  # type: str  # line 293
    othr = None  # type: _coconut.typing.Sequence[str]  # line 293
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 293
    curr = None  # type: _coconut.typing.Sequence[str]  # line 293
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 293
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 294
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 295
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 296
    except Exception as E:  # line 297
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 297
    if None not in [othreol, curreol] and othreol != curreol:  # line 298
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 298
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 299
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 300
    tmp = []  # type: List[str]  # block lines  # line 301
    last = " "  # type: str  # "into"-file offset for remark lines  # line 302
    no = None  # type: int  # "into"-file offset for remark lines  # line 302
    line = None  # type: str  # "into"-file offset for remark lines  # line 302
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 302
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 303
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 304
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 304
            continue  # continue filling current block, no matter what type of block it is  # line 304
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 305
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 305
        if last == " ":  # block is same in both files  # line 306
            if len(tmp) > 0:  # avoid adding empty keep block  # line 307
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 307
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 308
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 309
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 310
                offset += len(blocks[-2].lines)  # line 311
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 312
                blocks.pop()  # line 313
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 314
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 315
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 316
                offset += len(blocks[-1].lines)  # line 317
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 318
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 319
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 320
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 320
        last = line[0]  # line 321
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 322
# TODO add code to detect block moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 324
    debug("Diff blocks: " + repr(blocks))  # line 325
    if diffOnly:  # line 326
        return (blocks, nl)  # line 326

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 329
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 329
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 329
    selection = None  # type: str  # clean list of strings  # line 329
    for block in blocks:  # line 330
        if block.tipe == MergeBlockType.KEEP:  # line 331
            output.extend(block.lines)  # line 331
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 332
            output.extend(block.lines)  # line 334
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 335
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 336
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 337
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 338
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 339
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 340
                while True:  # line 341
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 342
                    if op in "tb":  # line 343
                        output.extend(block.lines)  # line 343
                    if op in "ib":  # line 344
                        output.extend(block.replaces.lines)  # line 344
                    if op == "u":  # line 345
                        user_block_input(output)  # line 345
                    if op in "tbiu":  # line 346
                        break  # line 346
            else:  # more than one line and not ask  # line 347
                if mergeOperation == MergeOperation.REMOVE:  # line 348
                    pass  # line 348
                elif mergeOperation == MergeOperation.BOTH:  # line 349
                    output.extend(block.lines)  # line 349
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 350
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 350
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 351
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 352
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 354
                if selection in "ao":  # line 355
                    if block.tipe == MergeBlockType.INSERT:  # line 356
                        add_all = "y" if selection == "a" else "n"  # line 356
                        selection = add_all  # line 356
                    else:  # REMOVE case  # line 357
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 357
                        selection = del_all  # REMOVE case  # line 357
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 358
                output.extend(block.lines)  # line 360
    debug("Merge output: " + "; ".join(output))  # line 361
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 362
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 365
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 365
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 368
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 369
    blocks = []  # type: List[MergeBlock]  # line 370
    for i, line in enumerate(out):  # line 371
        if line[0] == "+":  # line 372
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 373
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 374
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 375
                else:  # first + in block  # line 376
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 377
            else:  # last line of + block  # line 378
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 379
                    blocks[-1].lines.append(line[2])  # line 380
                else:  # single line  # line 381
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 382
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 383
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 384
                    blocks.pop()  # line 384
        elif line[0] == "-":  # line 385
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 386
                blocks[-1].lines.append(line[2])  # line 387
            else:  # first in block  # line 388
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 389
        elif line[0] == " ":  # line 390
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 391
                blocks[-1].lines.append(line[2])  # line 392
            else:  # first in block  # line 393
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 394
        else:  # line 395
            raise Exception("Cannot parse diff line %r" % line)  # line 395
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 396
    if diffOnly:  # line 397
        return blocks  # line 397
    out[:] = []  # line 398
    for i, block in enumerate(blocks):  # line 399
        if block.tipe == MergeBlockType.KEEP:  # line 400
            out.extend(block.lines)  # line 400
        elif block.tipe == MergeBlockType.REPLACE:  # line 401
            if mergeOperation == MergeOperation.ASK:  # line 402
                printo(pure.ajoin("- ", othr))  # line 403
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 404
                printo("+ " + (" " * i) + block.lines[0])  # line 405
                printo(pure.ajoin("+ ", into))  # line 406
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 407
                if op in "tb":  # line 408
                    out.extend(block.lines)  # line 408
                    break  # line 408
                if op in "ib":  # line 409
                    out.extend(block.replaces.lines)  # line 409
                    break  # line 409
                if op == "m":  # line 410
                    user_block_input(out)  # line 410
                    break  # line 410
            else:  # non-interactive  # line 411
                if mergeOperation == MergeOperation.REMOVE:  # line 412
                    pass  # line 412
                elif mergeOperation == MergeOperation.BOTH:  # line 413
                    out.extend(block.lines)  # line 413
                elif mergeOperation == MergeOperation.INSERT:  # line 414
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 414
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 415
            out.extend(block.lines)  # line 415
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 416
            out.extend(block.lines)  # line 416
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 418

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 420
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 423
    debug("Detecting root folders...")  # line 424
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 425
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 426
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 427
        contents = set(os.listdir(path))  # type: Set[str]  # line 428
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder  # line 429
        choice = None  # type: _coconut.typing.Optional[str]  # line 430
        if len(vcss) > 1:  # line 431
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 432
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 433
        elif len(vcss) > 0:  # line 434
            choice = vcss[0]  # line 434
        if not vcs[0] and choice:  # memorize current repo root  # line 435
            vcs = (path, choice)  # memorize current repo root  # line 435
        new = os.path.dirname(path)  # get parent path  # line 436
        if new == path:  # avoid infinite loop  # line 437
            break  # avoid infinite loop  # line 437
        path = new  # line 438
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 439
        if vcs[0]:  # already detected vcs base and command  # line 440
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 440
        sos = path  # line 441
        while True:  # continue search for VCS base  # line 442
            new = os.path.dirname(path)  # get parent path  # line 443
            if new == path:  # no VCS folder found  # line 444
                return (sos, None, None)  # no VCS folder found  # line 444
            path = new  # line 445
            contents = set(os.listdir(path))  # line 446
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 447
            choice = None  # line 448
            if len(vcss) > 1:  # line 449
                choice = SVN if SVN in vcss else vcss[0]  # line 450
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 451
            elif len(vcss) > 0:  # line 452
                choice = vcss[0]  # line 452
            if choice:  # line 453
                return (sos, path, choice)  # line 453
    return (None, vcs[0], vcs[1])  # line 454

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 456
    index = 0  # type: int  # line 457
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 458
    while index < len(pattern):  # line 459
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 460
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 460
            continue  # line 460
        if pattern[index] in "*?":  # line 461
            count = 1  # type: int  # line 462
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 463
                count += 1  # line 463
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 464
            index += count  # line 464
            continue  # line 464
        if pattern[index:index + 2] == "[!":  # line 465
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 465
            index += len(out[-1][1])  # line 465
            continue  # line 465
        count = 1  # line 466
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 467
            count += 1  # line 467
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 468
        index += count  # line 468
    return out  # line 469

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 471
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 472
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 473
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 475
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 475
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 476
        Exit("Source and target file patterns differ in semantics")  # line 476
    return (ot, nt)  # line 477

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 479
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 480
    pairs = []  # type: List[Tuple[str, str]]  # line 481
    for filename in filenames:  # line 482
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 483
        nextliteral = 0  # type: int  # line 484
        index = 0  # type: int  # line 484
        parsedOld = []  # type: List[GlobBlock2]  # line 485
        for part in oldPattern:  # match everything in the old filename  # line 486
            if part.isLiteral:  # line 487
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 487
                index += len(part.content)  # line 487
                nextliteral += 1  # line 487
            elif part.content.startswith("?"):  # line 488
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 488
                index += len(part.content)  # line 488
            elif part.content.startswith("["):  # line 489
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 489
                index += 1  # line 489
            elif part.content == "*":  # line 490
                if nextliteral >= len(literals):  # line 491
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 491
                    break  # line 491
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 492
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 493
                index = nxt  # line 493
            else:  # line 494
                Exit("Invalid file pattern specified for move/rename")  # line 494
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 495
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 496
        nextliteral = 0  # line 497
        nextglob = 0  # type: int  # line 497
        outname = []  # type: List[str]  # line 498
        for part in newPattern:  # generate new filename  # line 499
            if part.isLiteral:  # line 500
                outname.append(literals[nextliteral].content)  # line 500
                nextliteral += 1  # line 500
            else:  # line 501
                outname.append(globs[nextglob].matches)  # line 501
                nextglob += 1  # line 501
        pairs.append((filename, "".join(outname)))  # line 502
    return pairs  # line 503

@_coconut_tco  # line 505
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 505
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 509
    if not actions:  # line 510
        return []  # line 510
    sources = None  # type: List[str]  # line 511
    targets = None  # type: List[str]  # line 511
    sources, targets = [list(l) for l in zip(*actions)]  # line 512
    last = len(actions)  # type: int  # line 513
    while last > 1:  # line 514
        clean = True  # type: bool  # line 515
        for i in range(1, last):  # line 516
            try:  # line 517
                index = targets[:i].index(sources[i])  # type: int  # line 518
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 519
                targets.insert(index, targets.pop(i))  # line 520
                clean = False  # line 521
            except:  # target not found in sources: good!  # line 522
                continue  # target not found in sources: good!  # line 522
        if clean:  # line 523
            break  # line 523
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 524
    if exitOnConflict:  # line 525
        for i in range(1, len(actions)):  # line 525
            if sources[i] in targets[:i]:  # line 525
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 525
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 526

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 528
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 529
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 530
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 531

def parseOnlyOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 533
    ''' Returns (root-normalized) set of --only arguments, and set or --except arguments. '''  # line 534
    root = os.getcwd()  # type: str  # line 535
    onlys = []  # type: List[str]  # zero necessary as last start position  # line 536
    excps = []  # type: List[str]  # zero necessary as last start position  # line 536
    index = 0  # type: int  # zero necessary as last start position  # line 536
    while True:  # line 537
        try:  # line 538
            index = 1 + listindex(options, "--only", index)  # line 539
            onlys.append(options[index])  # line 540
            del options[index]  # line 541
            del options[index - 1]  # line 542
        except:  # line 543
            break  # line 543
    index = 0  # line 544
    while True:  # line 545
        try:  # line 546
            index = 1 + listindex(options, "--except", index)  # line 547
            excps.append(options[index])  # line 548
            del options[index]  # line 549
            del options[index - 1]  # line 550
        except:  # line 551
            break  # line 551
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(".." + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(".." + SLASH))) if excps else None)  # avoids out-of-repo paths  # line 552
