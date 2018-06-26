#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x7bece705

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


# Lazy imports for quicker initialization TODO make mypy accept this
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
    ''' Dictionary with attribute access. '''  # line 41
    def __init__(_, mapping: 'Dict[str, Any]') -> 'None':  # TODO remove -> None when fixed in Coconut stub  # line 42
        dict.__init__(_, mapping)  # TODO remove -> None when fixed in Coconut stub  # line 42
    @_coconut_tco  # or simply class C(dict): __getattr__ = dict.__getitem__  # line 43
    def __getattribute__(_, name: 'str') -> 'Any':  # or simply class C(dict): __getattr__ = dict.__getitem__  # line 43
        try:  # line 44
            return _[name]  # line 44
        except:  # line 45
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 45
    def __setattribute__(_, name: 'str', value: 'Any') -> 'None':  # line 46
        try:  # line 47
            _[name] = value  # line 47
        except:  # line 48
            dict.__setattribute__(_, name, value)  # line 48

Fore = Accessor({k: "" for k in ["RESET", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "YELLOW"]})  # type: Dict[str, str]  # line 50
try:  # http://bluesock.org/~willkg/dev/ansi.html  # line 51
    if hasattr(sys.stderr, "isatty") and sys.stderr.isatty():  # http://bluesock.org/~willkg/dev/ansi.html  # line 51
        from colorama import init  # line 52
        from colorama import AnsiToWin32  # line 52
        from colorama import Back  # line 52
        from colorama import Fore  # line 52
        init(wrap=False)  # line 53
        sys.stdout = AnsiToWin32(sys.stdout).stream  # wrap the color conversion manually  # line 54
        sys.stderr = AnsiToWin32(sys.stderr).stream  # line 55
except:  # line 56
    pass  # line 56

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 58
    Number = TypeVar("Number", int, float)  # line 59
    class Counter(Generic[Number]):  # line 60
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 61
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 62
            _.value = initial  # type: Number  # line 62
        def inc(_, by: 'Number'=1) -> 'Number':  # line 63
            _.value += by  # line 63
            return _.value  # line 63
else:  # line 64
    class Counter:  # line 65
        def __init__(_, initial=0) -> 'None':  # line 66
            _.value = initial  # line 66
        def inc(_, by=1):  # line 67
            _.value += by  # line 67
            return _.value  # line 67

class ProgressIndicator(Counter):  # line 69
    ''' Manages a rotating progress indicator. '''  # line 70
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 71
        super(ProgressIndicator, _).__init__(-1)  # line 71
        _.symbols = symbols  # line 71
        _.timer = time.time()  # type: float  # line 71
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 71
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 72
        ''' Returns a value only if a certain time has passed. '''  # line 73
        newtime = time.time()  # type: float  # line 74
        if newtime - _.timer < .1:  # line 75
            return None  # line 75
        _.timer = newtime  # line 76
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 77
        if _.callback:  # line 78
            _.callback(sign)  # line 78
        return sign  # line 79

class Logger:  # line 81
    ''' Logger that supports joining many items. '''  # line 82
    def __init__(_, log) -> 'None':  # line 83
        _._log = log  # line 83
    def debug(_, *s):  # line 84
        _._log.debug(pure.sjoin(*s))  # line 84
    def info(_, *s):  # line 85
        _._log.info(pure.sjoin(*s))  # line 85
    def warn(_, *s):  # line 86
        _._log.warning(pure.sjoin(*s))  # line 86
    def error(_, *s):  # line 87
        _._log.error(pure.sjoin(*s))  # line 87


# Constants
_log = Logger(logging.getLogger(__name__))  # line 91
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 91
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress", "useChangesCommand", "useUnicodeFont"]  # type: List[str]  # line 92
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 93
CONFIGURABLE_INTS = ["logLines"]  # type: List[str]  # line 94
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 95
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 96
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 97
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 98
BACKUP_SUFFIX = "_last"  # type: str  # line 99
metaFolder = ".sos"  # type: str  # line 100
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 101
metaFile = ".meta"  # type: str  # line 102
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 103
KIBI = 1 << 10  # type: int  # line 104
MEBI = 1 << 20  # type: int  # line 104
GIBI = 1 << 30  # type: int  # line 104
bufSize = MEBI  # type: int  # line 105
UTF8 = "utf_8"  # type: str  # early used constant, not defined in standard library  # line 106
SVN = "svn"  # type: str  # line 107
SLASH = "/"  # type: str  # line 108
DOT_SYMBOL = "\u00b7"  # type: str  # line 109
MULT_SYMBOL = "\u00d7"  # type: str  # line 110
CROSS_SYMBOL = "\u2716"  # type: str  # line 111
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 112
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 113
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in "this revision"  # line 114
MOVE_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 115
METADATA_FORMAT = 1  # type: int  # counter for incompatible consecutive formats (was undefined, "1" is the first versioned version after that)  # line 116
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 117
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 118
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS, RCS have probably different per-file operation  # line 119
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 120
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[bytes, str]  # line 121
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[str, int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 122
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 123


# Functions
def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # PEP528 compatibility  # line 136
    tryOrIgnore(lambda _=None: sys.stdout.write((("" if color is None else color)) + s + (Fore.RESET if color else "") + nl), lambda _=None: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')))  # PEP528 compatibility  # line 136
    sys.stdout.flush()  # PEP528 compatibility  # line 136
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 137
    tryOrIgnore(lambda _=None: sys.stderr.write((("" if color is None else color)) + s + (Fore.RESET if color else "") + nl), lambda _=None: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')))  # line 137
    sys.stderr.flush()  # line 137
@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 138
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 138
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 138
@_coconut_tco  # for os->py access of reading filenames  # line 139
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 139
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 139
try:  # line 140
    import chardet  # https://github.com/chardet/chardet  # line 141
    def detectEncoding(binary: 'bytes') -> 'str':  # line 142
        return chardet.detect(binary)["encoding"]  # line 142
except:  # Guess the encoding  # line 143
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 143
        ''' Fallback if chardet library missing. '''  # line 144
        try:  # line 145
            binary.decode(UTF8)  # line 145
            return UTF8  # line 145
        except UnicodeError:  # line 146
            pass  # line 146
        try:  # line 147
            binary.decode("utf_16")  # line 147
            return "utf_16"  # line 147
        except UnicodeError:  # line 148
            pass  # line 148
        try:  # line 149
            binary.decode("cp1252")  # line 149
            return "cp1252"  # line 149
        except UnicodeError:  # line 150
            pass  # line 150
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 151

def tryOrDefault(func: '_coconut.typing.Callable[..., Any]', default: 'Any') -> 'Any':  # line 153
    try:  # line 154
        return func()  # line 154
    except:  # line 155
        return default  # line 155

def tryOrIgnore(func: '_coconut.typing.Callable[..., Any]', onError: '_coconut.typing.Callable[[Exception], None]'=lambda _=None: None) -> 'Any':  # line 157
    try:  # line 158
        return func()  # line 158
    except Exception as E:  # line 159
        onError(E)  # line 159

def removePath(key: 'str', value: 'str') -> 'str':  # line 161
    ''' Cleanup of user-specified global file patterns. '''  # TODO improve  # line 162
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 163

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 165
    d = {}  # type: Dict[Any, Any]  # line 165
    d.update(dikt)  # line 165
    d.update(by)  # line 165
    return d  # line 165

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # Abstraction for opening both compressed and plain files  # line 167
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # Abstraction for opening both compressed and plain files  # line 167

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 169
    ''' Determine EOL style from a binary string. '''  # line 170
    lf = file.count(b"\n")  # type: int  # line 171
    cr = file.count(b"\r")  # type: int  # line 172
    crlf = file.count(b"\r\n")  # type: int  # line 173
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 174
        if lf != crlf or cr != crlf:  # line 175
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 175
        return b"\r\n"  # line 176
    if lf != 0 and cr != 0:  # line 177
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 177
    if lf > cr:  # Linux/Unix  # line 178
        return b"\n"  # Linux/Unix  # line 178
    if cr > lf:  # older 8-bit machines  # line 179
        return b"\r"  # older 8-bit machines  # line 179
    return None  # no new line contained, cannot determine  # line 180

if TYPE_CHECKING:  # line 182
    Splittable = TypeVar("Splittable", AnyStr)  # line 183
    def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> 'List[Splittable]':  # line 184
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 184
else:  # line 185
    def safeSplit(s, d=None):  # line 186
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 186

@_coconut_tco  # line 188
def hashStr(datas: 'str') -> 'str':  # line 188
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 188

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 190
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 190

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 192
    return lizt[index:].index(what) + index  # line 192

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 194
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 194

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 196
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 196

def Exit(message: 'str'="", code=1):  # line 198
    printe("[%sEXIT%s%s%s]" % (Fore.RED if code else Fore.GREEN, Fore.RESET, " %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + message + "." if message != "" else "")))  # line 198
    sys.exit(code)  # line 198

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 204
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 205
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 206
        raise Exception("Cannot possibly strings pack into specified length")  # line 206
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 207
        prefix += separator + ((process)(strings.pop(0)))  # line 207
    return prefix  # line 208

def exception(E):  # line 210
    ''' Report an exception to the user to enable useful bug reporting. '''  # line 211
    printo(str(E))  # line 212
    import traceback  # line 213
    traceback.print_exc()  # line 214
    traceback.print_stack()  # line 215

def hashFile(path: 'str', compress: 'bool', saveTo: '_coconut.typing.Optional[str]'=None, callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 217
    ''' Calculate hash of file contents, and return compressed sized, if in write mode, or zero. '''  # line 218
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 219
    _hash = hashlib.sha256()  # line 220
    wsize = 0  # type: int  # line 221
    if saveTo and os.path.exists(encode(saveTo)):  # line 222
        Exit("Hash collision detected. Leaving repository in inconsistent state.", 1)  # HINT this exits immediately  # line 223
    to = openIt(saveTo, "w", compress) if saveTo else None  # line 224
    with open(encode(path), "rb") as fd:  # line 225
        while True:  # line 226
            buffer = fd.read(bufSize)  # type: bytes  # line 227
            _hash.update(buffer)  # line 228
            if to:  # line 229
                to.write(buffer)  # line 229
            if len(buffer) < bufSize:  # line 230
                break  # line 230
            if indicator:  # line 231
                indicator.getIndicator()  # line 231
        if to:  # line 232
            to.close()  # line 233
            wsize = os.stat(encode(saveTo)).st_size  # line 234
    return (_hash.hexdigest(), wsize)  # line 235

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 237
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 238
    for k, v in map.items():  # line 239
        if k in params:  # line 239
            return v  # line 239
    return default  # line 240

@_coconut_tco  # line 242
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 242
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 242

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 244
    lines = []  # type: _coconut.typing.Sequence[str]  # line 245
    if filename is not None:  # line 246
        with open(encode(filename), "rb") as fd:  # line 246
            content = fd.read()  # line 246
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 247
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 248
    if filename is not None:  # line 249
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 249
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 249
    elif content is not None:  # line 250
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 250
    else:  # line 251
        return (sys.getdefaultencoding(), b"\n", [])  # line 251
    if ignoreWhitespace:  # line 252
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 252
    return (encoding, eol, lines)  # line 253

if TYPE_CHECKING:  # line 255
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 256
    @_coconut_tco  # line 257
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 257
        ''' A better makedata() version. '''  # line 258
        r = _old._asdict()  # type: Dict[str, Any]  # line 259
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 260
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 261
else:  # line 262
    @_coconut_tco  # line 263
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 263
        ''' A better makedata() version. '''  # line 264
        r = _old._asdict()  # line 265
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 266
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 267

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 269
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 270
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 271
    for path, info in changes.additions.items():  # line 272
        for dpath, dinfo in changes.deletions.items():  # line 272
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 273
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 274
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 275
                break  # deletions loop, continue with next addition  # line 276
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 277

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 279
    ''' Default can be a selection from choice and allows empty input. '''  # line 280
    while True:  # line 281
        selection = input(text).strip().lower()  # line 282
        if selection != "" and selection in choices:  # line 283
            break  # line 283
        if selection == "" and default is not None:  # line 284
            selection = default  # line 284
            break  # line 284
    return selection  # line 285

def user_block_input(output: 'List[str]'):  # line 287
    ''' Side-effect appending to input list. '''  # line 288
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 289
    line = sep  # type: str  # line 289
    while True:  # line 290
        line = input("> ")  # line 291
        if line == sep:  # line 292
            break  # line 292
        output.append(line)  # writes to caller-provided list reference  # line 293

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 295
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 310
    encoding = None  # type: str  # line 311
    othr = None  # type: _coconut.typing.Sequence[str]  # line 311
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 311
    curr = None  # type: _coconut.typing.Sequence[str]  # line 311
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 311
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 312
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 313
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 314
    except Exception as E:  # line 315
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 315
    if None not in [othreol, curreol] and othreol != curreol:  # line 316
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 316
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 317
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 318
    tmp = []  # type: List[str]  # block lines  # line 319
    last = " "  # type: str  # "into"-file offset for remark lines  # line 320
    no = None  # type: int  # "into"-file offset for remark lines  # line 320
    line = None  # type: str  # "into"-file offset for remark lines  # line 320
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 320
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 321
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 322
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 322
            continue  # continue filling current block, no matter what type of block it is  # line 322
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 323
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 323
        if last == " ":  # block is same in both files  # line 324
            if len(tmp) > 0:  # avoid adding empty keep block  # line 325
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 325
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 326
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 327
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 328
                offset += len(blocks[-2].lines)  # line 329
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 330
                blocks.pop()  # line 331
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 332
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 333
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 334
                offset += len(blocks[-1].lines)  # line 335
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 336
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 337
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 338
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 338
        last = line[0]  # line 339
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 340
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 342
    debug("Diff blocks: " + repr(blocks))  # line 343
    if diffOnly:  # line 344
        return (blocks, nl)  # line 344

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 347
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 347
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 347
    selection = None  # type: str  # clean list of strings  # line 347
    for block in blocks:  # line 348
        if block.tipe == MergeBlockType.KEEP:  # line 349
            output.extend(block.lines)  # line 349
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 350
            output.extend(block.lines)  # line 352
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 353
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 354
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 355
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 356
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 357
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 358
                while True:  # line 359
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 360
                    if op in "tb":  # line 361
                        output.extend(block.lines)  # line 361
                    if op in "ib":  # line 362
                        output.extend(block.replaces.lines)  # line 362
                    if op == "u":  # line 363
                        user_block_input(output)  # line 363
                    if op in "tbiu":  # line 364
                        break  # line 364
            else:  # more than one line and not ask  # line 365
                if mergeOperation == MergeOperation.REMOVE:  # line 366
                    pass  # line 366
                elif mergeOperation == MergeOperation.BOTH:  # line 367
                    output.extend(block.lines)  # line 367
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 368
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 368
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 369
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 370
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 372
                if selection in "ao":  # line 373
                    if block.tipe == MergeBlockType.INSERT:  # line 374
                        add_all = "y" if selection == "a" else "n"  # line 374
                        selection = add_all  # line 374
                    else:  # REMOVE case  # line 375
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 375
                        selection = del_all  # REMOVE case  # line 375
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 376
                output.extend(block.lines)  # line 378
    debug("Merge output: " + "; ".join(output))  # line 379
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 380
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 383
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 383
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 386
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 387
    blocks = []  # type: List[MergeBlock]  # line 388
    for i, line in enumerate(out):  # line 389
        if line[0] == "+":  # line 390
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 391
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 392
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 393
                else:  # first + in block  # line 394
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 395
            else:  # last line of + block  # line 396
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 397
                    blocks[-1].lines.append(line[2])  # line 398
                else:  # single line  # line 399
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 400
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 401
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 402
                    blocks.pop()  # line 402
        elif line[0] == "-":  # line 403
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 404
                blocks[-1].lines.append(line[2])  # line 405
            else:  # first in block  # line 406
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 407
        elif line[0] == " ":  # line 408
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 409
                blocks[-1].lines.append(line[2])  # line 410
            else:  # first in block  # line 411
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 412
        else:  # line 413
            raise Exception("Cannot parse diff line %r" % line)  # line 413
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 414
    if diffOnly:  # line 415
        return blocks  # line 415
    out[:] = []  # line 416
    for i, block in enumerate(blocks):  # line 417
        if block.tipe == MergeBlockType.KEEP:  # line 418
            out.extend(block.lines)  # line 418
        elif block.tipe == MergeBlockType.REPLACE:  # line 419
            if mergeOperation == MergeOperation.ASK:  # line 420
                printo(pure.ajoin("- ", othr))  # line 421
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 422
                printo("+ " + (" " * i) + block.lines[0])  # line 423
                printo(pure.ajoin("+ ", into))  # line 424
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 425
                if op in "tb":  # line 426
                    out.extend(block.lines)  # line 426
                    break  # line 426
                if op in "ib":  # line 427
                    out.extend(block.replaces.lines)  # line 427
                    break  # line 427
                if op == "m":  # line 428
                    user_block_input(out)  # line 428
                    break  # line 428
            else:  # non-interactive  # line 429
                if mergeOperation == MergeOperation.REMOVE:  # line 430
                    pass  # line 430
                elif mergeOperation == MergeOperation.BOTH:  # line 431
                    out.extend(block.lines)  # line 431
                elif mergeOperation == MergeOperation.INSERT:  # line 432
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 432
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 433
            out.extend(block.lines)  # line 433
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 434
            out.extend(block.lines)  # line 434
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 436

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 438
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 441
    debug("Detecting root folders...")  # line 442
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 443
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 444
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 445
        contents = set(os.listdir(path))  # type: Set[str]  # line 446
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 447
        choice = None  # type: _coconut.typing.Optional[str]  # line 448
        if len(vcss) > 1:  # line 449
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 450
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 451
        elif len(vcss) > 0:  # line 452
            choice = vcss[0]  # line 452
        if not vcs[0] and choice:  # memorize current repo root  # line 453
            vcs = (path, choice)  # memorize current repo root  # line 453
        new = os.path.dirname(path)  # get parent path  # line 454
        if new == path:  # avoid infinite loop  # line 455
            break  # avoid infinite loop  # line 455
        path = new  # line 456
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 457
        if vcs[0]:  # already detected vcs base and command  # line 458
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 458
        sos = path  # line 459
        while True:  # continue search for VCS base  # line 460
            contents = set(os.listdir(path))  # line 461
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 462
            choice = None  # line 463
            if len(vcss) > 1:  # line 464
                choice = SVN if SVN in vcss else vcss[0]  # line 465
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 466
            elif len(vcss) > 0:  # line 467
                choice = vcss[0]  # line 467
            if choice:  # line 468
                return (sos, path, choice)  # line 468
            new = os.path.dirname(path)  # get parent path  # line 469
            if new == path:  # no VCS folder found  # line 470
                return (sos, None, None)  # no VCS folder found  # line 470
            path = new  # line 471
    return (None, vcs[0], vcs[1])  # line 472

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 474
    index = 0  # type: int  # line 475
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 476
    while index < len(pattern):  # line 477
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 478
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 478
            continue  # line 478
        if pattern[index] in "*?":  # line 479
            count = 1  # type: int  # line 480
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 481
                count += 1  # line 481
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 482
            index += count  # line 482
            continue  # line 482
        if pattern[index:index + 2] == "[!":  # line 483
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 483
            index += len(out[-1][1])  # line 483
            continue  # line 483
        count = 1  # line 484
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 485
            count += 1  # line 485
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 486
        index += count  # line 486
    return out  # line 487

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 489
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 490
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 491
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 493
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 493
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 494
        Exit("Source and target file patterns differ in semantics")  # line 494
    return (ot, nt)  # line 495

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 497
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 498
    pairs = []  # type: List[Tuple[str, str]]  # line 499
    for filename in filenames:  # line 500
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 501
        nextliteral = 0  # type: int  # line 502
        index = 0  # type: int  # line 502
        parsedOld = []  # type: List[GlobBlock2]  # line 503
        for part in oldPattern:  # match everything in the old filename  # line 504
            if part.isLiteral:  # line 505
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 505
                index += len(part.content)  # line 505
                nextliteral += 1  # line 505
            elif part.content.startswith("?"):  # line 506
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 506
                index += len(part.content)  # line 506
            elif part.content.startswith("["):  # line 507
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 507
                index += 1  # line 507
            elif part.content == "*":  # line 508
                if nextliteral >= len(literals):  # line 509
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 509
                    break  # line 509
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 510
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 511
                index = nxt  # line 511
            else:  # line 512
                Exit("Invalid file pattern specified for move/rename")  # line 512
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 513
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 514
        nextliteral = 0  # line 515
        nextglob = 0  # type: int  # line 515
        outname = []  # type: List[str]  # line 516
        for part in newPattern:  # generate new filename  # line 517
            if part.isLiteral:  # line 518
                outname.append(literals[nextliteral].content)  # line 518
                nextliteral += 1  # line 518
            else:  # line 519
                outname.append(globs[nextglob].matches)  # line 519
                nextglob += 1  # line 519
        pairs.append((filename, "".join(outname)))  # line 520
    return pairs  # line 521

@_coconut_tco  # line 523
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 523
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 527
    if not actions:  # line 528
        return []  # line 528
    sources = None  # type: List[str]  # line 529
    targets = None  # type: List[str]  # line 529
    sources, targets = [list(l) for l in zip(*actions)]  # line 530
    last = len(actions)  # type: int  # line 531
    while last > 1:  # line 532
        clean = True  # type: bool  # line 533
        for i in range(1, last):  # line 534
            try:  # line 535
                index = targets[:i].index(sources[i])  # type: int  # line 536
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 537
                targets.insert(index, targets.pop(i))  # line 538
                clean = False  # line 539
            except:  # target not found in sources: good!  # line 540
                continue  # target not found in sources: good!  # line 540
        if clean:  # line 541
            break  # line 541
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 542
    if exitOnConflict:  # line 543
        for i in range(1, len(actions)):  # line 543
            if sources[i] in targets[:i]:  # line 543
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 543
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 544

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 546
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 547
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 548
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 549

def parseOnlyOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]]]':  # line 551
    ''' Returns (root-normalized) set of --only arguments, and set or --except arguments. '''  # line 552
    root = os.getcwd()  # type: str  # line 553
    onlys = []  # type: List[str]  # zero necessary as last start position  # line 554
    excps = []  # type: List[str]  # zero necessary as last start position  # line 554
    index = 0  # type: int  # zero necessary as last start position  # line 554
    while True:  # line 555
        try:  # line 556
            index = 1 + listindex(options, "--only", index)  # line 557
            onlys.append(options[index])  # line 558
            del options[index]  # line 559
            del options[index - 1]  # line 560
        except:  # line 561
            break  # line 561
    index = 0  # line 562
    while True:  # line 563
        try:  # line 564
            index = 1 + listindex(options, "--except", index)  # line 565
            excps.append(options[index])  # line 566
            del options[index]  # line 567
            del options[index - 1]  # line 568
        except:  # line 569
            break  # line 569
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(".." + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(".." + SLASH))) if excps else None)  # avoids out-of-repo paths  # line 570
