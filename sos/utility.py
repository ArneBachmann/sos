#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xc27d121e

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
import shutil  # early time tracking  # line 5
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
Back = Fore  # type: Dict[str, str]  # line 50
Style = Accessor({k: "" for k in ["NORMAL", "BRIGHT", "RESET_ALL"]})  # type: Dict[str, str]  # line 51
try:  # http://bluesock.org/~willkg/dev/ansi.html  # line 52
    if hasattr(sys.stderr, "isatty") and sys.stderr.isatty():  # http://bluesock.org/~willkg/dev/ansi.html  # line 52
        from colorama import init  # line 53
        from colorama import AnsiToWin32  # line 53
        from colorama import Back  # line 53
        from colorama import Fore  # line 53
        from colorama import Style  # line 53
        init(wrap=False)  # line 54
        sys.stdout = AnsiToWin32(sys.stdout).stream  # wrap the color conversion manually  # line 55
        sys.stderr = AnsiToWin32(sys.stderr).stream  # line 56
        if sys.platform == "win32":  # sadly this changes background color as well  # line 57
            Style.BRIGHT = ""  # sadly this changes background color as well  # line 57
except:  # line 58
    pass  # line 58

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 60
    Number = TypeVar("Number", int, float)  # line 61
    class Counter(Generic[Number]):  # line 62
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 63
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 64
            _.value = initial  # type: Number  # line 64
        def inc(_, by: 'Number'=1) -> 'Number':  # line 65
            _.value += by  # line 65
            return _.value  # line 65
else:  # line 66
    class Counter:  # line 67
        def __init__(_, initial=0) -> 'None':  # line 68
            _.value = initial  # line 68
        def inc(_, by=1):  # line 69
            _.value += by  # line 69
            return _.value  # line 69

class ProgressIndicator(Counter):  # line 71
    ''' Manages a rotating progress indicator. '''  # line 72
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 73
        super(ProgressIndicator, _).__init__(-1)  # line 73
        _.symbols = symbols  # line 73
        _.timer = time.time()  # type: float  # line 73
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 73
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 74
        ''' Returns a value only if a certain time has passed. '''  # line 75
        newtime = time.time()  # type: float  # line 76
        if newtime - _.timer < .1:  # line 77
            return None  # line 77
        _.timer = newtime  # line 78
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 79
        if _.callback:  # line 80
            _.callback(sign)  # line 80
        return sign  # line 81

class Logger:  # line 83
    ''' Logger that supports joining many items. '''  # line 84
    def __init__(_, log) -> 'None':  # line 85
        _._log = log  # line 85
    def debug(_, *s):  # line 86
        _._log.debug(pure.sjoin(*s))  # line 86
    def info(_, *s):  # line 87
        _._log.info(pure.sjoin(*s))  # line 87
    def warn(_, *s):  # line 88
        _._log.warning(pure.sjoin(*s))  # line 88
    def error(_, *s):  # line 89
        _._log.error(pure.sjoin(*s))  # line 89


# Constants
_log = Logger(logging.getLogger(__name__))  # line 93
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 93
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress", "useChangesCommand", "useUnicodeFont"]  # type: List[str]  # line 94
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 95
CONFIGURABLE_INTS = ["logLines"]  # type: List[str]  # line 96
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 97
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 98
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 99
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 100
BACKUP_SUFFIX = "_last"  # type: str  # line 101
metaFolder = ".sos"  # type: str  # line 102
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 103
metaFile = ".meta"  # type: str  # line 104
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 105
KIBI = 1 << 10  # type: int  # line 106
MEBI = 1 << 20  # type: int  # line 106
GIBI = 1 << 30  # type: int  # line 106
bufSize = MEBI  # type: int  # line 107
UTF8 = "utf_8"  # type: str  # early used constant, not defined in standard library  # line 108
SVN = "svn"  # type: str  # line 109
SLASH = "/"  # type: str  # line 110
DOT_SYMBOL = "\u00b7"  # type: str  # line 111
MULT_SYMBOL = "\u00d7"  # type: str  # line 112
CROSS_SYMBOL = "\u2716"  # type: str  # line 113
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 114
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 115
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in "this revision"  # line 116
MOVE_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 117
METADATA_FORMAT = 2  # type: int  # counter for (partially incompatible) consecutive formats (was undefined, "1" is the first numbered format version after that)  # line 118
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 119
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 120
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS, RCS have probably different per-file operation  # line 121
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 122
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[bytes, str]  # line 123
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[str, int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 124
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 125


# Functions
def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # PEP528 compatibility  # line 138
    tryOrIgnore(lambda _=None: sys.stdout.write((("" if color is None else color)) + s + (Fore.RESET if color else "") + nl), lambda _=None: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')))  # PEP528 compatibility  # line 138
    sys.stdout.flush()  # PEP528 compatibility  # line 138
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 139
    tryOrIgnore(lambda _=None: sys.stderr.write((("" if color is None else color)) + s + (Fore.RESET if color else "") + nl), lambda _=None: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')))  # line 139
    sys.stderr.flush()  # line 139
@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 140
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 140
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 140
@_coconut_tco  # for os->py access of reading filenames  # line 141
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 141
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 141
try:  # line 142
    import chardet  # https://github.com/chardet/chardet  # line 143
    def detectEncoding(binary: 'bytes') -> 'str':  # line 144
        return chardet.detect(binary)["encoding"]  # line 144
except:  # Guess the encoding  # line 145
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 145
        ''' Fallback if chardet library missing. '''  # line 146
        try:  # line 147
            binary.decode(UTF8)  # line 147
            return UTF8  # line 147
        except UnicodeError:  # line 148
            pass  # line 148
        try:  # line 149
            binary.decode("utf_16")  # line 149
            return "utf_16"  # line 149
        except UnicodeError:  # line 150
            pass  # line 150
        try:  # line 151
            binary.decode("cp1252")  # line 151
            return "cp1252"  # line 151
        except UnicodeError:  # line 152
            pass  # line 152
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 153

def tryOrDefault(func: '_coconut.typing.Callable[..., Any]', default: 'Any') -> 'Any':  # line 155
    try:  # line 156
        return func()  # line 156
    except:  # line 157
        return default  # line 157

def tryOrIgnore(func: '_coconut.typing.Callable[..., Any]', onError: '_coconut.typing.Callable[[Exception], None]'=lambda _=None: None) -> 'Any':  # line 159
    try:  # line 160
        return func()  # line 160
    except Exception as E:  # line 161
        onError(E)  # line 161

def removePath(key: 'str', value: 'str') -> 'str':  # line 163
    ''' Cleanup of user-specified global file patterns. '''  # TODO improve  # line 164
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 165

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 167
    d = {}  # type: Dict[Any, Any]  # line 167
    d.update(dikt)  # line 167
    d.update(by)  # line 167
    return d  # line 167

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # Abstraction for opening both compressed and plain files  # line 169
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # Abstraction for opening both compressed and plain files  # line 169

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 171
    ''' Determine EOL style from a binary string. '''  # line 172
    lf = file.count(b"\n")  # type: int  # line 173
    cr = file.count(b"\r")  # type: int  # line 174
    crlf = file.count(b"\r\n")  # type: int  # line 175
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 176
        if lf != crlf or cr != crlf:  # line 177
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 177
        return b"\r\n"  # line 178
    if lf != 0 and cr != 0:  # line 179
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 179
    if lf > cr:  # Linux/Unix  # line 180
        return b"\n"  # Linux/Unix  # line 180
    if cr > lf:  # older 8-bit machines  # line 181
        return b"\r"  # older 8-bit machines  # line 181
    return None  # no new line contained, cannot determine  # line 182

if TYPE_CHECKING:  # line 184
    Splittable = TypeVar("Splittable", AnyStr)  # line 185
    def safeSplit(s: 'Splittable', d: '_coconut.typing.Optional[Splittable]'=None) -> 'List[Splittable]':  # line 186
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 186
else:  # line 187
    def safeSplit(s, d=None):  # line 188
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 188

@_coconut_tco  # line 190
def hashStr(datas: 'str') -> 'str':  # line 190
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 190

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 192
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 192

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 194
    return lizt[index:].index(what) + index  # line 194

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 196
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 196

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 198
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 198

def Exit(message: 'str'="", code=1):  # line 200
    printe("[%sEXIT%s%s%s]" % (Fore.YELLOW if code else Fore.GREEN, Fore.RESET, " %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + message + "." if message != "" else "")))  # line 200
    sys.exit(code)  # line 200

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 206
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 207
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 208
        raise Exception("Cannot possibly strings pack into specified length")  # line 208
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 209
        prefix += separator + ((process)(strings.pop(0)))  # line 209
    return prefix  # line 210

def exception(E):  # line 212
    ''' Report an exception to the user to enable useful bug reporting. '''  # line 213
    printo(str(E))  # line 214
    import traceback  # line 215
    traceback.print_exc()  # line 216
    traceback.print_stack()  # line 217

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 219
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 220
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 221
    _hash = hashlib.sha256()  # line 222
    wsize = 0  # type: int  # line 223
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 224
        Exit("Hash collision detected. Leaving repository in inconsistent state.", 1)  # HINT this exits immediately  # line 225
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 226
    with open(encode(path), "rb") as fd:  # line 227
        while True:  # line 228
            buffer = fd.read(bufSize)  # type: bytes  # line 229
            _hash.update(buffer)  # line 230
            if to:  # line 231
                to.write(buffer)  # line 231
            if len(buffer) < bufSize:  # line 232
                break  # line 232
            if indicator:  # line 233
                indicator.getIndicator()  # line 233
        if to:  # line 234
            to.close()  # line 235
            wsize = os.stat(encode(saveTo[0])).st_size  # line 236
            for remote in saveTo[1:]:  # line 237
                shutil.copy2(encode(saveTo[0]), encode(remote))  # line 237
    return (_hash.hexdigest(), wsize)  # line 238

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 240
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 241
    for k, v in map.items():  # line 242
        if k in params:  # line 242
            return v  # line 242
    return default  # line 243

@_coconut_tco  # line 245
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 245
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 245

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, bytes, _coconut.typing.Sequence[str]]':  # line 247
    lines = []  # type: _coconut.typing.Sequence[str]  # line 248
    if filename is not None:  # line 249
        with open(encode(filename), "rb") as fd:  # line 249
            content = fd.read()  # line 249
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 250
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 251
    if filename is not None:  # line 252
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 252
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 252
    elif content is not None:  # line 253
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 253
    else:  # line 254
        return (sys.getdefaultencoding(), b"\n", [])  # line 254
    if ignoreWhitespace:  # line 255
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 255
    return (encoding, eol, lines)  # line 256

if TYPE_CHECKING:  # line 258
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 259
    @_coconut_tco  # line 260
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 260
        ''' A better makedata() version. '''  # line 261
        r = _old._asdict()  # type: Dict[str, Any]  # line 262
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 263
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 264
else:  # line 265
    @_coconut_tco  # line 266
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 266
        ''' A better makedata() version. '''  # line 267
        r = _old._asdict()  # line 268
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 269
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 270

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 272
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 273
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 274
    for path, info in changes.additions.items():  # line 275
        for dpath, dinfo in changes.deletions.items():  # line 275
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 276
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 277
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 278
                break  # deletions loop, continue with next addition  # line 279
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 280

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 282
    ''' Default can be a selection from choice and allows empty input. '''  # line 283
    while True:  # line 284
        selection = input(text).strip().lower()  # line 285
        if selection != "" and selection in choices:  # line 286
            break  # line 286
        if selection == "" and default is not None:  # line 287
            selection = default  # line 287
            break  # line 287
    return selection  # line 288

def user_block_input(output: 'List[str]'):  # line 290
    ''' Side-effect appending to input list. '''  # line 291
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 292
    line = sep  # type: str  # line 292
    while True:  # line 293
        line = input("> ")  # line 294
        if line == sep:  # line 295
            break  # line 295
        output.append(line)  # writes to caller-provided list reference  # line 296

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 298
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 313
    encoding = None  # type: str  # line 314
    othr = None  # type: _coconut.typing.Sequence[str]  # line 314
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 314
    curr = None  # type: _coconut.typing.Sequence[str]  # line 314
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 314
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 315
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 316
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 317
    except Exception as E:  # line 318
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 318
    if None not in [othreol, curreol] and othreol != curreol:  # line 319
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 319
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 320
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 321
    tmp = []  # type: List[str]  # block lines  # line 322
    last = " "  # type: str  # "into"-file offset for remark lines  # line 323
    no = None  # type: int  # "into"-file offset for remark lines  # line 323
    line = None  # type: str  # "into"-file offset for remark lines  # line 323
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 323
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 324
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 325
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 325
            continue  # continue filling current block, no matter what type of block it is  # line 325
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 326
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 326
        if last == " ":  # block is same in both files  # line 327
            if len(tmp) > 0:  # avoid adding empty keep block  # line 328
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 328
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 329
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 330
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 331
                offset += len(blocks[-2].lines)  # line 332
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 333
                blocks.pop()  # line 334
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 335
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 336
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 337
                offset += len(blocks[-1].lines)  # line 338
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 339
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 340
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 341
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 341
        last = line[0]  # line 342
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 343
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 345
    debug("Diff blocks: " + repr(blocks))  # line 346
    if diffOnly:  # line 347
        return (blocks, nl)  # line 347

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 350
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 350
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 350
    selection = None  # type: str  # clean list of strings  # line 350
    for block in blocks:  # line 351
        if block.tipe == MergeBlockType.KEEP:  # line 352
            output.extend(block.lines)  # line 352
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 353
            output.extend(block.lines)  # line 355
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 356
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 357
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 358
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 359
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 360
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 361
                while True:  # line 362
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 363
                    if op in "tb":  # line 364
                        output.extend(block.lines)  # line 364
                    if op in "ib":  # line 365
                        output.extend(block.replaces.lines)  # line 365
                    if op == "u":  # line 366
                        user_block_input(output)  # line 366
                    if op in "tbiu":  # line 367
                        break  # line 367
            else:  # more than one line and not ask  # line 368
                if mergeOperation == MergeOperation.REMOVE:  # line 369
                    pass  # line 369
                elif mergeOperation == MergeOperation.BOTH:  # line 370
                    output.extend(block.lines)  # line 370
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 371
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 371
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 372
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 373
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 375
                if selection in "ao":  # line 376
                    if block.tipe == MergeBlockType.INSERT:  # line 377
                        add_all = "y" if selection == "a" else "n"  # line 377
                        selection = add_all  # line 377
                    else:  # REMOVE case  # line 378
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 378
                        selection = del_all  # REMOVE case  # line 378
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 379
                output.extend(block.lines)  # line 381
    debug("Merge output: " + "; ".join(output))  # line 382
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 383
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 386
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 386
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 389
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 390
    blocks = []  # type: List[MergeBlock]  # line 391
    for i, line in enumerate(out):  # line 392
        if line[0] == "+":  # line 393
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 394
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 395
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 396
                else:  # first + in block  # line 397
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 398
            else:  # last line of + block  # line 399
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 400
                    blocks[-1].lines.append(line[2])  # line 401
                else:  # single line  # line 402
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 403
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 404
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 405
                    blocks.pop()  # line 405
        elif line[0] == "-":  # line 406
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 407
                blocks[-1].lines.append(line[2])  # line 408
            else:  # first in block  # line 409
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 410
        elif line[0] == " ":  # line 411
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 412
                blocks[-1].lines.append(line[2])  # line 413
            else:  # first in block  # line 414
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 415
        else:  # line 416
            raise Exception("Cannot parse diff line %r" % line)  # line 416
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 417
    if diffOnly:  # line 418
        return blocks  # line 418
    out[:] = []  # line 419
    for i, block in enumerate(blocks):  # line 420
        if block.tipe == MergeBlockType.KEEP:  # line 421
            out.extend(block.lines)  # line 421
        elif block.tipe == MergeBlockType.REPLACE:  # line 422
            if mergeOperation == MergeOperation.ASK:  # line 423
                printo(pure.ajoin("- ", othr))  # line 424
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 425
                printo("+ " + (" " * i) + block.lines[0])  # line 426
                printo(pure.ajoin("+ ", into))  # line 427
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 428
                if op in "tb":  # line 429
                    out.extend(block.lines)  # line 429
                    break  # line 429
                if op in "ib":  # line 430
                    out.extend(block.replaces.lines)  # line 430
                    break  # line 430
                if op == "m":  # line 431
                    user_block_input(out)  # line 431
                    break  # line 431
            else:  # non-interactive  # line 432
                if mergeOperation == MergeOperation.REMOVE:  # line 433
                    pass  # line 433
                elif mergeOperation == MergeOperation.BOTH:  # line 434
                    out.extend(block.lines)  # line 434
                elif mergeOperation == MergeOperation.INSERT:  # line 435
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 435
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 436
            out.extend(block.lines)  # line 436
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 437
            out.extend(block.lines)  # line 437
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 439

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 441
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 444
    debug("Detecting root folders...")  # line 445
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 446
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 447
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 448
        contents = set(os.listdir(path))  # type: Set[str]  # line 449
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 450
        choice = None  # type: _coconut.typing.Optional[str]  # line 451
        if len(vcss) > 1:  # line 452
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 453
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 454
        elif len(vcss) > 0:  # line 455
            choice = vcss[0]  # line 455
        if not vcs[0] and choice:  # memorize current repo root  # line 456
            vcs = (path, choice)  # memorize current repo root  # line 456
        new = os.path.dirname(path)  # get parent path  # line 457
        if new == path:  # avoid infinite loop  # line 458
            break  # avoid infinite loop  # line 458
        path = new  # line 459
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 460
        if vcs[0]:  # already detected vcs base and command  # line 461
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 461
        sos = path  # line 462
        while True:  # continue search for VCS base  # line 463
            contents = set(os.listdir(path))  # line 464
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 465
            choice = None  # line 466
            if len(vcss) > 1:  # line 467
                choice = SVN if SVN in vcss else vcss[0]  # line 468
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 469
            elif len(vcss) > 0:  # line 470
                choice = vcss[0]  # line 470
            if choice:  # line 471
                return (sos, path, choice)  # line 471
            new = os.path.dirname(path)  # get parent path  # line 472
            if new == path:  # no VCS folder found  # line 473
                return (sos, None, None)  # no VCS folder found  # line 473
            path = new  # line 474
    return (None, vcs[0], vcs[1])  # line 475

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 477
    index = 0  # type: int  # line 478
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 479
    while index < len(pattern):  # line 480
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 481
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 481
            continue  # line 481
        if pattern[index] in "*?":  # line 482
            count = 1  # type: int  # line 483
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 484
                count += 1  # line 484
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 485
            index += count  # line 485
            continue  # line 485
        if pattern[index:index + 2] == "[!":  # line 486
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 486
            index += len(out[-1][1])  # line 486
            continue  # line 486
        count = 1  # line 487
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 488
            count += 1  # line 488
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 489
        index += count  # line 489
    return out  # line 490

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 492
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 493
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 494
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 496
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 496
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 497
        Exit("Source and target file patterns differ in semantics")  # line 497
    return (ot, nt)  # line 498

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 500
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 501
    pairs = []  # type: List[Tuple[str, str]]  # line 502
    for filename in filenames:  # line 503
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 504
        nextliteral = 0  # type: int  # line 505
        index = 0  # type: int  # line 505
        parsedOld = []  # type: List[GlobBlock2]  # line 506
        for part in oldPattern:  # match everything in the old filename  # line 507
            if part.isLiteral:  # line 508
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 508
                index += len(part.content)  # line 508
                nextliteral += 1  # line 508
            elif part.content.startswith("?"):  # line 509
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 509
                index += len(part.content)  # line 509
            elif part.content.startswith("["):  # line 510
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 510
                index += 1  # line 510
            elif part.content == "*":  # line 511
                if nextliteral >= len(literals):  # line 512
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 512
                    break  # line 512
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 513
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 514
                index = nxt  # line 514
            else:  # line 515
                Exit("Invalid file pattern specified for move/rename")  # line 515
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 516
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 517
        nextliteral = 0  # line 518
        nextglob = 0  # type: int  # line 518
        outname = []  # type: List[str]  # line 519
        for part in newPattern:  # generate new filename  # line 520
            if part.isLiteral:  # line 521
                outname.append(literals[nextliteral].content)  # line 521
                nextliteral += 1  # line 521
            else:  # line 522
                outname.append(globs[nextglob].matches)  # line 522
                nextglob += 1  # line 522
        pairs.append((filename, "".join(outname)))  # line 523
    return pairs  # line 524

@_coconut_tco  # line 526
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 526
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 530
    if not actions:  # line 531
        return []  # line 531
    sources = None  # type: List[str]  # line 532
    targets = None  # type: List[str]  # line 532
    sources, targets = [list(l) for l in zip(*actions)]  # line 533
    last = len(actions)  # type: int  # line 534
    while last > 1:  # line 535
        clean = True  # type: bool  # line 536
        for i in range(1, last):  # line 537
            try:  # line 538
                index = targets[:i].index(sources[i])  # type: int  # line 539
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 540
                targets.insert(index, targets.pop(i))  # line 541
                clean = False  # line 542
            except:  # target not found in sources: good!  # line 543
                continue  # target not found in sources: good!  # line 543
        if clean:  # line 544
            break  # line 544
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 545
    if exitOnConflict:  # line 546
        for i in range(1, len(actions)):  # line 546
            if sources[i] in targets[:i]:  # line 546
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 546
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 547

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 549
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 550
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 551
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 552

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str]]':  # line 554
    ''' Returns (root-normalized) set of --only arguments, and set or --except arguments. '''  # line 555
    root = os.getcwd()  # type: str  # zero necessary as marker for last start position  # line 556
    index = 0  # type: int  # zero necessary as marker for last start position  # line 556
    onlys = []  # type: List[str]  # line 557
    excps = []  # type: List[str]  # line 557
    remotes = []  # type: List[str]  # line 557
    for key, container in [("--only", onlys), ("--except", excps), ("--remote", remotes)]:  # line 558
        while True:  # line 559
            try:  # line 560
                index = 1 + listindex(options, key, index)  # line 561
                container.append(options[index])  # line 562
                del options[index]  # line 563
                del options[index - 1]  # line 564
            except:  # no more found  # line 565
                break  # no more found  # line 565
        index = 0  # line 566
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(".." + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(".." + SLASH))) if excps else None, remotes)  # line 567
