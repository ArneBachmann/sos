#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x290e87d4

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
    from typing import NoReturn  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 7
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
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[_coconut.typing.Optional[bytes], str]  # line 123
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[_coconut.typing.Optional[str], int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 124
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 125


# Functions
def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # PEP528 compatibility  # line 138
    tryOrIgnore(lambda: sys.stdout.write((("" if color is None else color)) + s + (Fore.RESET if color else "") + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 138
    sys.stdout.flush()  # PEP528 compatibility  # line 138
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 139
    tryOrIgnore(lambda: sys.stderr.write((("" if color is None else color)) + s + (Fore.RESET if color else "") + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 139
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

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 155
    try:  # line 156
        return func()  # line 156
    except:  # line 157
        return default  # line 157

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 159
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
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 185
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 185
else:  # line 186
    def safeSplit(s, d=None):  # line 187
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 187

@_coconut_tco  # line 189
def hashStr(datas: 'str') -> 'str':  # line 189
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 189

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 191
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 191

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 193
    return lizt[index:].index(what) + index  # line 193

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 195
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 195

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 197
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 197

def Exit(message: 'str'="", code=1):  # line 199
    printe("[%sEXIT%s%s%s]" % (Fore.YELLOW if code else Fore.GREEN, Fore.RESET, " %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + message + "." if message != "" else "")))  # line 199
    sys.exit(code)  # line 199

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 205
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 206
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 207
        raise Exception("Cannot possibly strings pack into specified length")  # line 207
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 208
        prefix += separator + ((process)(strings.pop(0)))  # line 208
    return prefix  # line 209

def exception(E):  # line 211
    ''' Report an exception to the user to enable useful bug reporting. '''  # line 212
    printo(str(E))  # line 213
    import traceback  # line 214
    traceback.print_exc()  # line 215
    traceback.print_stack()  # line 216

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 218
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 219
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 220
    _hash = hashlib.sha256()  # line 221
    wsize = 0  # type: int  # line 222
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 223
        Exit("Hash collision detected. Leaving repository in inconsistent state.", 1)  # HINT this exits immediately  # line 224
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 225
    with open(encode(path), "rb") as fd:  # line 226
        while True:  # line 227
            buffer = fd.read(bufSize)  # type: bytes  # line 228
            _hash.update(buffer)  # line 229
            if to:  # line 230
                to.write(buffer)  # line 230
            if len(buffer) < bufSize:  # line 231
                break  # line 231
            if indicator:  # line 232
                indicator.getIndicator()  # line 232
        if to:  # line 233
            to.close()  # line 234
            wsize = os.stat(encode(saveTo[0])).st_size  # line 235
            for remote in saveTo[1:]:  # line 236
                tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 236
    return (_hash.hexdigest(), wsize)  # line 237

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 239
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 240
    for k, v in map.items():  # line 241
        if k in params:  # line 241
            return v  # line 241
    return default  # line 242

@_coconut_tco  # line 244
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 244
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 244

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 246
    lines = []  # type: List[str]  # line 247
    if filename is not None:  # line 248
        with open(encode(filename), "rb") as fd:  # line 248
            content = fd.read()  # line 248
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 249
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 250
    if filename is not None:  # line 251
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 251
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 251
    elif content is not None:  # line 252
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 252
    else:  # line 253
        return (sys.getdefaultencoding(), b"\n", [])  # line 253
    if ignoreWhitespace:  # line 254
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 254
    return (encoding, eol, lines)  # line 255

if TYPE_CHECKING:  # line 257
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 258
    @_coconut_tco  # line 259
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 259
        ''' A better makedata() version. '''  # line 260
        r = _old._asdict()  # type: Dict[str, Any]  # line 261
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 262
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 263
else:  # line 264
    @_coconut_tco  # line 265
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 265
        ''' A better makedata() version. '''  # line 266
        r = _old._asdict()  # line 267
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 268
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 269

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 271
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 272
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 273
    for path, info in changes.additions.items():  # line 274
        for dpath, dinfo in changes.deletions.items():  # line 274
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 275
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 276
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 277
                break  # deletions loop, continue with next addition  # line 278
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 279

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 281
    ''' Default can be a selection from choice and allows empty input. '''  # line 282
    while True:  # line 283
        selection = input(text).strip().lower()  # line 284
        if selection != "" and selection in choices:  # line 285
            break  # line 285
        if selection == "" and default is not None:  # line 286
            selection = default  # line 286
            break  # line 286
    return selection  # line 287

def user_block_input(output: 'List[str]'):  # line 289
    ''' Side-effect appending to input list. '''  # line 290
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 291
    line = sep  # type: str  # line 291
    while True:  # line 292
        line = input("> ")  # line 293
        if line == sep:  # line 294
            break  # line 294
        output.append(line)  # writes to caller-provided list reference  # line 295

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 297
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 312
    encoding = None  # type: str  # line 313
    othr = None  # type: _coconut.typing.Sequence[str]  # line 313
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 313
    curr = None  # type: _coconut.typing.Sequence[str]  # line 313
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 313
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 314
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 315
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 316
    except Exception as E:  # line 317
        Exit("Cannot merge '%s' into '%s': %r" % (filename, intoname, E))  # line 317
    if None not in [othreol, curreol] and othreol != curreol:  # line 318
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 318
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 319
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 320
    tmp = []  # type: List[str]  # block lines  # line 321
    last = " "  # type: str  # "into"-file offset for remark lines  # line 322
    no = None  # type: int  # "into"-file offset for remark lines  # line 322
    line = None  # type: str  # "into"-file offset for remark lines  # line 322
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 322
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 323
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 324
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 324
            continue  # continue filling current block, no matter what type of block it is  # line 324
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 325
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 325
        if last == " ":  # block is same in both files  # line 326
            if len(tmp) > 0:  # avoid adding empty keep block  # line 327
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 327
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 328
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 329
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 330
                offset += len(blocks[-2].lines)  # line 331
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 332
                blocks.pop()  # line 333
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 334
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 335
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 336
                offset += len(blocks[-1].lines)  # line 337
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 338
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 339
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 340
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 340
        last = line[0]  # line 341
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 342
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 344
    debug("Diff blocks: " + repr(blocks))  # line 345
    if diffOnly:  # line 346
        return (blocks, nl)  # line 346

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 349
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 349
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 349
    selection = ""  # type: str  # clean list of strings  # line 349
    for block in blocks:  # line 350
        if block.tipe == MergeBlockType.KEEP:  # line 351
            output.extend(block.lines)  # line 351
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 352
            output.extend(block.lines)  # line 354
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 355
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 356
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 357
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 358
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 359
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 360
                while True:  # line 361
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 362
                    if op in "tb":  # line 363
                        output.extend(block.lines)  # line 363
                    if op in "ib":  # line 364
                        output.extend(block.replaces.lines)  # line 364
                    if op == "u":  # line 365
                        user_block_input(output)  # line 365
                    if op in "tbiu":  # line 366
                        break  # line 366
            else:  # more than one line and not ask  # line 367
                if mergeOperation == MergeOperation.REMOVE:  # line 368
                    pass  # line 368
                elif mergeOperation == MergeOperation.BOTH:  # line 369
                    output.extend(block.lines)  # line 369
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 370
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 370
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 371
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 372
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 374
                if selection in "ao":  # line 375
                    if block.tipe == MergeBlockType.INSERT:  # line 376
                        add_all = "y" if selection == "a" else "n"  # line 376
                        selection = add_all  # line 376
                    else:  # REMOVE case  # line 377
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 377
                        selection = del_all  # REMOVE case  # line 377
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 378
                output.extend(block.lines)  # line 380
    debug("Merge output: " + "; ".join(output))  # line 381
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 382
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 385
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 385
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 388
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 389
    blocks = []  # type: List[MergeBlock]  # line 390
    for i, line in enumerate(out):  # line 391
        if line[0] == "+":  # line 392
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 393
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 394
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 395
                else:  # first + in block  # line 396
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 397
            else:  # last line of + block  # line 398
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 399
                    blocks[-1].lines.append(line[2])  # line 400
                else:  # single line  # line 401
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 402
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 403
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 404
                    blocks.pop()  # line 404
        elif line[0] == "-":  # line 405
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 406
                blocks[-1].lines.append(line[2])  # line 407
            else:  # first in block  # line 408
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 409
        elif line[0] == " ":  # line 410
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 411
                blocks[-1].lines.append(line[2])  # line 412
            else:  # first in block  # line 413
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 414
        else:  # line 415
            raise Exception("Cannot parse diff line %r" % line)  # line 415
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 416
    if diffOnly:  # line 417
        return blocks  # line 417
    out[:] = []  # line 418
    for i, block in enumerate(blocks):  # line 419
        if block.tipe == MergeBlockType.KEEP:  # line 420
            out.extend(block.lines)  # line 420
        elif block.tipe == MergeBlockType.REPLACE:  # line 421
            if mergeOperation == MergeOperation.ASK:  # line 422
                printo(pure.ajoin("- ", othr))  # line 423
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 424
                printo("+ " + (" " * i) + block.lines[0])  # line 425
                printo(pure.ajoin("+ ", into))  # line 426
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 427
                if op in "tb":  # line 428
                    out.extend(block.lines)  # line 428
                    break  # line 428
                if op in "ib":  # line 429
                    out.extend(block.replaces.lines)  # line 429
                    break  # line 429
                if op == "m":  # line 430
                    user_block_input(out)  # line 430
                    break  # line 430
            else:  # non-interactive  # line 431
                if mergeOperation == MergeOperation.REMOVE:  # line 432
                    pass  # line 432
                elif mergeOperation == MergeOperation.BOTH:  # line 433
                    out.extend(block.lines)  # line 433
                elif mergeOperation == MergeOperation.INSERT:  # line 434
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 434
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 435
            out.extend(block.lines)  # line 435
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 436
            out.extend(block.lines)  # line 436
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 438

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 440
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 443
    debug("Detecting root folders...")  # line 444
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 445
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 446
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 447
        contents = set(os.listdir(path))  # type: Set[str]  # line 448
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 449
        choice = None  # type: _coconut.typing.Optional[str]  # line 450
        if len(vcss) > 1:  # line 451
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 452
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 453
        elif len(vcss) > 0:  # line 454
            choice = vcss[0]  # line 454
        if not vcs[0] and choice:  # memorize current repo root  # line 455
            vcs = (path, choice)  # memorize current repo root  # line 455
        new = os.path.dirname(path)  # get parent path  # line 456
        if new == path:  # avoid infinite loop  # line 457
            break  # avoid infinite loop  # line 457
        path = new  # line 458
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 459
        if vcs[0]:  # already detected vcs base and command  # line 460
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 460
        sos = path  # line 461
        while True:  # continue search for VCS base  # line 462
            contents = set(os.listdir(path))  # line 463
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 464
            choice = None  # line 465
            if len(vcss) > 1:  # line 466
                choice = SVN if SVN in vcss else vcss[0]  # line 467
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 468
            elif len(vcss) > 0:  # line 469
                choice = vcss[0]  # line 469
            if choice:  # line 470
                return (sos, path, choice)  # line 470
            new = os.path.dirname(path)  # get parent path  # line 471
            if new == path:  # no VCS folder found  # line 472
                return (sos, None, None)  # no VCS folder found  # line 472
            path = new  # line 473
    return (None, vcs[0], vcs[1])  # line 474

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 476
    index = 0  # type: int  # line 477
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 478
    while index < len(pattern):  # line 479
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 480
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 480
            continue  # line 480
        if pattern[index] in "*?":  # line 481
            count = 1  # type: int  # line 482
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 483
                count += 1  # line 483
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 484
            index += count  # line 484
            continue  # line 484
        if pattern[index:index + 2] == "[!":  # line 485
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 485
            index += len(out[-1][1])  # line 485
            continue  # line 485
        count = 1  # line 486
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 487
            count += 1  # line 487
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 488
        index += count  # line 488
    return out  # line 489

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 491
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 492
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 493
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 495
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 495
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 496
        Exit("Source and target file patterns differ in semantics")  # line 496
    return (ot, nt)  # line 497

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 499
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 500
    pairs = []  # type: List[Tuple[str, str]]  # line 501
    for filename in filenames:  # line 502
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 503
        nextliteral = 0  # type: int  # line 504
        index = 0  # type: int  # line 504
        parsedOld = []  # type: List[GlobBlock2]  # line 505
        for part in oldPattern:  # match everything in the old filename  # line 506
            if part.isLiteral:  # line 507
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 507
                index += len(part.content)  # line 507
                nextliteral += 1  # line 507
            elif part.content.startswith("?"):  # line 508
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 508
                index += len(part.content)  # line 508
            elif part.content.startswith("["):  # line 509
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 509
                index += 1  # line 509
            elif part.content == "*":  # line 510
                if nextliteral >= len(literals):  # line 511
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 511
                    break  # line 511
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 512
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 513
                index = nxt  # line 513
            else:  # line 514
                Exit("Invalid file pattern specified for move/rename")  # line 514
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 515
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 516
        nextliteral = 0  # line 517
        nextglob = 0  # type: int  # line 517
        outname = []  # type: List[str]  # line 518
        for part in newPattern:  # generate new filename  # line 519
            if part.isLiteral:  # line 520
                outname.append(literals[nextliteral].content)  # line 520
                nextliteral += 1  # line 520
            else:  # line 521
                outname.append(globs[nextglob].matches)  # line 521
                nextglob += 1  # line 521
        pairs.append((filename, "".join(outname)))  # line 522
    return pairs  # line 523

@_coconut_tco  # line 525
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 525
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 529
    if not actions:  # line 530
        return []  # line 530
    sources = None  # type: List[str]  # line 531
    targets = None  # type: List[str]  # line 531
    sources, targets = [list(l) for l in zip(*actions)]  # line 532
    last = len(actions)  # type: int  # line 533
    while last > 1:  # line 534
        clean = True  # type: bool  # line 535
        for i in range(1, last):  # line 536
            try:  # line 537
                index = targets[:i].index(sources[i])  # type: int  # line 538
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 539
                targets.insert(index, targets.pop(i))  # line 540
                clean = False  # line 541
            except:  # target not found in sources: good!  # line 542
                continue  # target not found in sources: good!  # line 542
        if clean:  # line 543
            break  # line 543
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 544
    if exitOnConflict:  # line 545
        for i in range(1, len(actions)):  # line 545
            if sources[i] in targets[:i]:  # line 545
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 545
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 546

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 548
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 549
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 550
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 551

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str]]':  # line 553
    ''' Returns (root-normalized) set of --only arguments, and set or --except arguments. '''  # line 554
    root = os.getcwd()  # type: str  # zero necessary as marker for last start position  # line 555
    index = 0  # type: int  # zero necessary as marker for last start position  # line 555
    onlys = []  # type: List[str]  # line 556
    excps = []  # type: List[str]  # line 556
    remotes = []  # type: List[str]  # line 556
    for key, container in [("--only", onlys), ("--except", excps), ("--remote", remotes)]:  # line 557
        while True:  # line 558
            try:  # line 559
                index = 1 + listindex(options, key, index)  # line 560
                container.append(options[index])  # line 561
                del options[index]  # line 562
                del options[index - 1]  # line 563
            except:  # no more found  # line 564
                break  # no more found  # line 564
        index = 0  # line 565
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(".." + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(".." + SLASH))) if excps else None, remotes)  # line 566
