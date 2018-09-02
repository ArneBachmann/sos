#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xd04e45e8

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
    from sos import usage  # line 10
except:  # line 11
    import pure  # line 11
    from values import *  # line 11
    import usage  # line 11


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
    def __init__(_, mapping: 'Dict[str, Any]'={}) -> 'None':  # TODO remove -> None when fixed in Coconut stub  # line 42
        dict.__init__(_, mapping)  # TODO remove -> None when fixed in Coconut stub  # line 42
    @_coconut_tco  # or simply class C(dict): __getattr__ = dict.__getitem__  # line 43
    def __getattribute__(_, name: 'str') -> 'Any':  # or simply class C(dict): __getattr__ = dict.__getitem__  # line 43
        try:  # line 44
            return _[name]  # line 44
        except:  # line 45
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 45
    def __setattr__(_, name: 'str', value: 'Any') -> 'None':  # line 46
        _[name] = value  # line 46
    @_coconut_tco  # line 47
    def __bool__(_) -> 'bool':  # line 47
        return _coconut_tail_call(bool, int(_[None]))  # line 47
    @_coconut_tco  # line 48
    def __str__(_) -> 'str':  # line 48
        return _coconut_tail_call(str, _[None])  # line 48
    def __add__(_, b: 'Any') -> 'str':  # line 49
        return _.value + b  # line 49

useColor = [None]  # type: List[_coconut.typing.Optional[bool]]  # line 51
def enableColor(enable=True):  # line 52
    ''' This piece of code only became necessary to enable run-time en-/disabling of the colored terminal output. '''  # line 53
    global useColor  # line 54
    if (useColor[0] and enable) or (not enable and not useColor[0]):  # nothing to do  # line 55
        return  # nothing to do  # line 55
    MARKER.value = MARKER_COLOR if enable and sys.platform != "win32" else usage.MARKER_TEXT  # HINT because it doesn't work with the loggers yet  # line 56
    if enable:  # line 57
        init(wrap=False)  # line 58
        if useColor[0] is None:  # very initial  # line 59
            sys.stdout = AnsiToWin32(sys.stdout).stream  # TODO replace by "better exceptions" code  # line 60
            sys.stderr = AnsiToWin32(sys.stderr).stream  # line 61
    else:  # line 62
        deinit()  # line 62
    useColor[0] = enable  # line 63

Fore = Accessor({k: "" for k in ["RESET", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "YELLOW"]})  # type: Dict[str, str]  # line 65
Back = Fore  # type: Dict[str, str]  # line 65
Style = Accessor({k: "" for k in ["NORMAL", "BRIGHT", "RESET_ALL"]})  # type: Dict[str, str]  # line 66
MARKER = Accessor({"value": usage.MARKER_TEXT})  # type: str  # assume default text-only  # line 67
try:  # line 68
    import colorama.ansitowin32  # line 69
    if colorama.ansitowin32.is_a_tty(sys.stderr):  # list of ansi codes: http://bluesock.org/~willkg/dev/ansi.html  # line 70
        from colorama import init  # line 71
        from colorama import deinit  # line 71
        from colorama import AnsiToWin32  # line 71
        from colorama import Back  # line 71
        from colorama import Fore  # line 71
        from colorama import Style  # line 71
        MARKER_COLOR = Fore.WHITE + usage.MARKER_TEXT + Fore.RESET  # type: str  # line 72
        if sys.platform == "win32":  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 73
            Style.BRIGHT = ""  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 73
        enableColor()  # line 74
except:  # if library not installed, use fallback even for colored texts  # line 75
    MARKER_COLOR = usage.MARKER_TEXT  # if library not installed, use fallback even for colored texts  # line 75

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 77
    Number = TypeVar("Number", int, float)  # line 78
    class Counter(Generic[Number]):  # line 79
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 80
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 81
            _.value = initial  # type: Number  # line 81
        def inc(_, by: 'Number'=1) -> 'Number':  # line 82
            _.value += by  # line 82
            return _.value  # line 82
else:  # line 83
    class Counter:  # line 84
        def __init__(_, initial=0) -> 'None':  # line 85
            _.value = initial  # line 85
        def inc(_, by=1):  # line 86
            _.value += by  # line 86
            return _.value  # line 86

class ProgressIndicator(Counter):  # line 88
    ''' Manages a rotating progress indicator. '''  # line 89
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 90
        super(ProgressIndicator, _).__init__(-1)  # line 90
        _.symbols = symbols  # line 90
        _.timer = time.time()  # type: float  # line 90
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 90
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 91
        ''' Returns a value only if a certain time has passed. '''  # line 92
        newtime = time.time()  # type: float  # line 93
        if newtime - _.timer < .1:  # line 94
            return None  # line 94
        _.timer = newtime  # line 95
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 96
        if _.callback:  # line 97
            _.callback(sign)  # line 97
        return sign  # line 98

class Logger:  # line 100
    ''' Logger that supports joining many items. '''  # line 101
    def __init__(_, log) -> 'None':  # line 102
        _._log = log  # line 102
    def debug(_, *s):  # line 103
        _._log.debug(pure.sjoin(*s))  # line 103
    def info(_, *s):  # line 104
        _._log.info(pure.sjoin(*s))  # line 104
    def warn(_, *s):  # line 105
        _._log.warning(pure.sjoin(*s))  # line 105
    def error(_, *s):  # line 106
        _._log.error(pure.sjoin(*s))  # line 106


# Constants
_log = Logger(logging.getLogger(__name__))  # line 110
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 110
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress", "useChangesCommand", "useUnicodeFont", "useColorOutput"]  # type: List[str]  # line 111
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 112
CONFIGURABLE_INTS = ["logLines", "diffLines"]  # type: List[str]  # line 113
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 114
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 115
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 116
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 117
BACKUP_SUFFIX = "_last"  # type: str  # line 118
metaFolder = ".sos"  # type: str  # line 119
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 120
metaFile = ".meta"  # type: str  # line 121
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 122
KIBI = 1 << 10  # type: int  # line 123
MEBI = 1 << 20  # type: int  # line 123
GIBI = 1 << 30  # type: int  # line 123
bufSize = MEBI  # type: int  # line 124
UTF8 = "utf_8"  # type: str  # early used constant, not defined in standard library  # line 125
SVN = "svn"  # type: str  # line 126
SLASH = "/"  # type: str  # line 127
DOT_SYMBOL = "\u00b7"  # type: str  # line 128
MULT_SYMBOL = "\u00d7"  # type: str  # line 129
CROSS_SYMBOL = "\u2716"  # type: str  # line 130
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 131
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 132
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in "this revision"  # line 133
MOVE_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 134
METADATA_FORMAT = 2  # type: int  # counter for (partially incompatible) consecutive formats (was undefined, "1" is the first numbered format version after that)  # line 135
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 136
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 137
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS, RCS have probably different per-file operation  # line 138
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 139
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[_coconut.typing.Optional[bytes], str]  # line 140
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[_coconut.typing.Optional[str], int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 141
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "useColorOutput": True, "diffLines": 2, "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 142


# Functions
def siSize(size: 'int') -> 'str':  # line 159
    ''' Returns number and unit. '''  # line 160
    return "%.2f MiB" % (float(size) / MEBI) if size > 1.25 * MEBI else ("%.2f KiB" % (float(size) / KIBI) if size > 1.25 * KIBI else ("%d bytes" % size))  # line 161

def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 163
    color = useColor and color or ""  # line 164
    reset = Fore.RESET if useColor and color else ""  # line 165
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 166
    sys.stdout.flush()  # PEP528 compatibility  # line 166
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 168
    color = useColor and color or ""  # line 169
    reset = Fore.RESET if useColor and color else ""  # line 170
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 171
    sys.stderr.flush()  # line 171
@_coconut_tco  # line 172
def encode(s: 'str') -> 'bytes':  # line 172
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 173
@_coconut_tco  # for os->py access of reading filenames  # line 174
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 174
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 174
try:  # line 175
    import chardet  # https://github.com/chardet/chardet  # line 176
    def detectEncoding(binary: 'bytes') -> 'str':  # line 177
        return chardet.detect(binary)["encoding"]  # line 177
except:  # Guess the encoding  # line 178
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 178
        ''' Fallback if chardet library missing. '''  # line 179
        try:  # line 180
            binary.decode(UTF8)  # line 180
            return UTF8  # line 180
        except UnicodeError:  # line 181
            pass  # line 181
        try:  # line 182
            binary.decode("utf_16")  # line 182
            return "utf_16"  # line 182
        except UnicodeError:  # line 183
            pass  # line 183
        try:  # line 184
            binary.decode("cp1252")  # line 184
            return "cp1252"  # line 184
        except UnicodeError:  # line 185
            pass  # line 185
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 186

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 188
    try:  # line 189
        return func()  # line 189
    except:  # line 190
        return default  # line 190

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 192
    try:  # line 193
        return func()  # line 193
    except Exception as E:  # line 194
        onError(E)  # line 194

def removePath(key: 'str', value: 'str') -> 'str':  # line 196
    ''' Cleanup of user-specified global file patterns, used in config. '''  # TODO improve  # line 197
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 198

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 200
    ''' Updates a dictionary by another one, returning a new copy without touching any of the passed dictionaries. '''  # line 201
    d = dict(dikt)  # type: Dict[Any, Any]  # line 202
    d.update(by)  # line 202
    return d  # line 202

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # line 204
    ''' Abstraction for opening both compressed and plain files. '''  # line 205
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # line 206

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 208
    ''' Determine EOL style from a binary string. '''  # line 209
    lf = file.count(b"\n")  # type: int  # line 210
    cr = file.count(b"\r")  # type: int  # line 211
    crlf = file.count(b"\r\n")  # type: int  # line 212
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 213
        if lf != crlf or cr != crlf:  # line 214
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 214
        return b"\r\n"  # line 215
    if lf != 0 and cr != 0:  # line 216
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 216
    if lf > cr:  # Linux/Unix  # line 217
        return b"\n"  # Linux/Unix  # line 217
    if cr > lf:  # older 8-bit machines  # line 218
        return b"\r"  # older 8-bit machines  # line 218
    return None  # no new line contained, cannot determine  # line 219

if TYPE_CHECKING:  # line 221
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 222
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 222
else:  # line 223
    def safeSplit(s, d=None):  # line 224
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 224

@_coconut_tco  # line 226
def hashStr(datas: 'str') -> 'str':  # line 226
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 226

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 228
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 228

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 230
    return lizt[index:].index(what) + index  # line 230

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 232
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 232

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 234
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 234

def Exit(message: 'str'="", code=1):  # line 236
    printe("[")  # line 237
    printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN)  # line 238
    printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + message + ".") if message != "" else ""))  # line 239
    sys.exit(code)  # line 243

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 245
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 246
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 247
        raise Exception("Cannot possibly strings pack into specified length")  # line 247
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 248
        prefix += separator + ((process)(strings.pop(0)))  # line 248
    return prefix  # line 249

def exception(E):  # line 251
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 252
    printo(str(E))  # line 253
    import traceback  # line 254
    traceback.print_exc()  # line 255
    traceback.print_stack()  # line 256

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 258
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 259
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 260
    _hash = hashlib.sha256()  # line 261
    wsize = 0  # type: int  # line 262
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 263
        Exit("Hash collision detected. Leaving repository in inconsistent state.", 1)  # HINT this exits immediately  # line 264
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 265
    with open(encode(path), "rb") as fd:  # line 266
        while True:  # line 267
            buffer = fd.read(bufSize)  # type: bytes  # line 268
            _hash.update(buffer)  # line 269
            if to:  # line 270
                to.write(buffer)  # line 270
            if len(buffer) < bufSize:  # line 271
                break  # line 271
            if indicator:  # line 272
                indicator.getIndicator()  # line 272
        if to:  # line 273
            to.close()  # line 274
            wsize = os.stat(encode(saveTo[0])).st_size  # line 275
            for remote in saveTo[1:]:  # line 276
                tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 276
    return (_hash.hexdigest(), wsize)  # line 277

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 279
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 280
    for k, v in map.items():  # line 281
        if k in params:  # line 281
            return v  # line 281
    return default  # line 282

@_coconut_tco  # line 284
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 284
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 284

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 286
    lines = []  # type: List[str]  # line 287
    if filename is not None:  # line 288
        with open(encode(filename), "rb") as fd:  # line 288
            content = fd.read()  # line 288
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 289
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 290
    if filename is not None:  # line 291
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 291
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 291
    elif content is not None:  # line 292
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 292
    else:  # line 293
        return (sys.getdefaultencoding(), b"\n", [])  # line 293
    if ignoreWhitespace:  # line 294
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 294
    return (encoding, eol, lines)  # line 295

if TYPE_CHECKING:  # line 297
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 298
    @_coconut_tco  # line 299
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 299
        ''' A better makedata() version. '''  # line 300
        r = _old._asdict()  # type: Dict[str, Any]  # line 301
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 302
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 303
else:  # line 304
    @_coconut_tco  # line 305
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 305
        ''' A better makedata() version. '''  # line 306
        r = _old._asdict()  # line 307
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 308
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 309

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 311
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 312
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 313
    for path, info in changes.additions.items():  # line 314
        for dpath, dinfo in changes.deletions.items():  # line 314
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 315
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 316
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 317
                break  # deletions loop, continue with next addition  # line 318
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 319

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 321
    ''' Default can be a selection from choice and allows empty input. '''  # line 322
    while True:  # line 323
        selection = input(text).strip().lower()  # line 324
        if selection != "" and selection in choices:  # line 325
            break  # line 325
        if selection == "" and default is not None:  # line 326
            selection = default  # line 326
            break  # line 326
    return selection  # line 327

def user_block_input(output: 'List[str]'):  # line 329
    ''' Side-effect appending to input list. '''  # line 330
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 331
    line = sep  # type: str  # line 331
    while True:  # line 332
        line = input("> ")  # line 333
        if line == sep:  # line 334
            break  # line 334
        output.append(line)  # writes to caller-provided list reference  # line 335

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 337
    encoding = None  # type: str  # line 338
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 338
    othr = None  # type: _coconut.typing.Sequence[str]  # line 338
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 338
    curr = None  # type: _coconut.typing.Sequence[str]  # line 338
    try:  # line 339
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 340
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 341
    except Exception as E:  # line 342
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname), E))  # line 342
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 343
        printo(line)  # from generator expression  # line 343

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 345
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 360
    encoding = None  # type: str  # line 361
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 361
    othr = None  # type: _coconut.typing.Sequence[str]  # line 361
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 361
    curr = None  # type: _coconut.typing.Sequence[str]  # line 361
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 362
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 363
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 364
    except Exception as E:  # line 365
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname), E))  # line 365
    if None not in [othreol, curreol] and othreol != curreol:  # line 366
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 366
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 367
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 368
    tmp = []  # type: List[str]  # block lines  # line 369
    last = " "  # type: str  # "into"-file offset for remark lines  # line 370
    no = None  # type: int  # "into"-file offset for remark lines  # line 370
    line = None  # type: str  # "into"-file offset for remark lines  # line 370
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 370
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 371
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 372
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 372
            continue  # continue filling current block, no matter what type of block it is  # line 372
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 373
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 373
        if last == " ":  # block is same in both files  # line 374
            if len(tmp) > 0:  # avoid adding empty keep block  # line 375
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 375
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 376
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 377
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 378
                offset += len(blocks[-2].lines)  # line 379
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 380
                blocks.pop()  # line 381
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 382
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 383
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 384
                offset += len(blocks[-1].lines)  # line 385
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 386
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 387
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 388
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 388
        last = line[0]  # line 389
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 390
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 392
    debug("Diff blocks: " + repr(blocks))  # line 393
    if diffOnly:  # line 394
        return (blocks, nl)  # line 394

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 397
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 397
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 397
    selection = ""  # type: str  # clean list of strings  # line 397
    for block in blocks:  # line 398
        if block.tipe == MergeBlockType.KEEP:  # line 399
            output.extend(block.lines)  # line 399
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 400
            output.extend(block.lines)  # line 402
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 403
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 404
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 405
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 406
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 407
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 408
                while True:  # line 409
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 410
                    if op in "tb":  # line 411
                        output.extend(block.lines)  # line 411
                    if op in "ib":  # line 412
                        output.extend(block.replaces.lines)  # line 412
                    if op == "u":  # line 413
                        user_block_input(output)  # line 413
                    if op in "tbiu":  # line 414
                        break  # line 414
            else:  # more than one line and not ask  # line 415
                if mergeOperation == MergeOperation.REMOVE:  # line 416
                    pass  # line 416
                elif mergeOperation == MergeOperation.BOTH:  # line 417
                    output.extend(block.lines)  # line 417
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 418
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 418
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 419
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 420
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 422
                if selection in "ao":  # line 423
                    if block.tipe == MergeBlockType.INSERT:  # line 424
                        add_all = "y" if selection == "a" else "n"  # line 424
                        selection = add_all  # line 424
                    else:  # REMOVE case  # line 425
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 425
                        selection = del_all  # REMOVE case  # line 425
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 426
                output.extend(block.lines)  # line 428
    debug("Merge output: " + "; ".join(output))  # line 429
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 430
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 433
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 433
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 436
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 437
    blocks = []  # type: List[MergeBlock]  # line 438
    for i, line in enumerate(out):  # line 439
        if line[0] == "+":  # line 440
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 441
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 442
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 443
                else:  # first + in block  # line 444
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 445
            else:  # last line of + block  # line 446
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 447
                    blocks[-1].lines.append(line[2])  # line 448
                else:  # single line  # line 449
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 450
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 451
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 452
                    blocks.pop()  # line 452
        elif line[0] == "-":  # line 453
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 454
                blocks[-1].lines.append(line[2])  # line 455
            else:  # first in block  # line 456
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 457
        elif line[0] == " ":  # line 458
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 459
                blocks[-1].lines.append(line[2])  # line 460
            else:  # first in block  # line 461
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 462
        else:  # line 463
            raise Exception("Cannot parse diff line %r" % line)  # line 463
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 464
    if diffOnly:  # line 465
        return blocks  # line 465
    out[:] = []  # line 466
    for i, block in enumerate(blocks):  # line 467
        if block.tipe == MergeBlockType.KEEP:  # line 468
            out.extend(block.lines)  # line 468
        elif block.tipe == MergeBlockType.REPLACE:  # line 469
            if mergeOperation == MergeOperation.ASK:  # line 470
                printo(pure.ajoin("- ", othr))  # line 471
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 472
                printo("+ " + (" " * i) + block.lines[0])  # line 473
                printo(pure.ajoin("+ ", into))  # line 474
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 475
                if op in "tb":  # line 476
                    out.extend(block.lines)  # line 476
                    break  # line 476
                if op in "ib":  # line 477
                    out.extend(block.replaces.lines)  # line 477
                    break  # line 477
                if op == "m":  # line 478
                    user_block_input(out)  # line 478
                    break  # line 478
            else:  # non-interactive  # line 479
                if mergeOperation == MergeOperation.REMOVE:  # line 480
                    pass  # line 480
                elif mergeOperation == MergeOperation.BOTH:  # line 481
                    out.extend(block.lines)  # line 481
                elif mergeOperation == MergeOperation.INSERT:  # line 482
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 482
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 483
            out.extend(block.lines)  # line 483
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 484
            out.extend(block.lines)  # line 484
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 486

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 488
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 491
    debug("Detecting root folders...")  # line 492
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 493
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 494
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 495
        contents = set(os.listdir(path))  # type: Set[str]  # line 496
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 497
        choice = None  # type: _coconut.typing.Optional[str]  # line 498
        if len(vcss) > 1:  # line 499
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 500
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 501
        elif len(vcss) > 0:  # line 502
            choice = vcss[0]  # line 502
        if not vcs[0] and choice:  # memorize current repo root  # line 503
            vcs = (path, choice)  # memorize current repo root  # line 503
        new = os.path.dirname(path)  # get parent path  # line 504
        if new == path:  # avoid infinite loop  # line 505
            break  # avoid infinite loop  # line 505
        path = new  # line 506
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 507
        if vcs[0]:  # already detected vcs base and command  # line 508
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 508
        sos = path  # line 509
        while True:  # continue search for VCS base  # line 510
            contents = set(os.listdir(path))  # line 511
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 512
            choice = None  # line 513
            if len(vcss) > 1:  # line 514
                choice = SVN if SVN in vcss else vcss[0]  # line 515
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 516
            elif len(vcss) > 0:  # line 517
                choice = vcss[0]  # line 517
            if choice:  # line 518
                return (sos, path, choice)  # line 518
            new = os.path.dirname(path)  # get parent path  # line 519
            if new == path:  # no VCS folder found  # line 520
                return (sos, None, None)  # no VCS folder found  # line 520
            path = new  # line 521
    return (None, vcs[0], vcs[1])  # line 522

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 524
    index = 0  # type: int  # line 525
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 526
    while index < len(pattern):  # line 527
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 528
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 528
            continue  # line 528
        if pattern[index] in "*?":  # line 529
            count = 1  # type: int  # line 530
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 531
                count += 1  # line 531
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 532
            index += count  # line 532
            continue  # line 532
        if pattern[index:index + 2] == "[!":  # line 533
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 533
            index += len(out[-1][1])  # line 533
            continue  # line 533
        count = 1  # line 534
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 535
            count += 1  # line 535
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 536
        index += count  # line 536
    return out  # line 537

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 539
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 540
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 541
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 543
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 543
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 544
        Exit("Source and target file patterns differ in semantics")  # line 544
    return (ot, nt)  # line 545

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 547
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 548
    pairs = []  # type: List[Tuple[str, str]]  # line 549
    for filename in filenames:  # line 550
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 551
        nextliteral = 0  # type: int  # line 552
        index = 0  # type: int  # line 552
        parsedOld = []  # type: List[GlobBlock2]  # line 553
        for part in oldPattern:  # match everything in the old filename  # line 554
            if part.isLiteral:  # line 555
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 555
                index += len(part.content)  # line 555
                nextliteral += 1  # line 555
            elif part.content.startswith("?"):  # line 556
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 556
                index += len(part.content)  # line 556
            elif part.content.startswith("["):  # line 557
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 557
                index += 1  # line 557
            elif part.content == "*":  # line 558
                if nextliteral >= len(literals):  # line 559
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 559
                    break  # line 559
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 560
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 561
                index = nxt  # line 561
            else:  # line 562
                Exit("Invalid file pattern specified for move/rename")  # line 562
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 563
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 564
        nextliteral = 0  # line 565
        nextglob = 0  # type: int  # line 565
        outname = []  # type: List[str]  # line 566
        for part in newPattern:  # generate new filename  # line 567
            if part.isLiteral:  # line 568
                outname.append(literals[nextliteral].content)  # line 568
                nextliteral += 1  # line 568
            else:  # line 569
                outname.append(globs[nextglob].matches)  # line 569
                nextglob += 1  # line 569
        pairs.append((filename, "".join(outname)))  # line 570
    return pairs  # line 571

@_coconut_tco  # line 573
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 573
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 577
    if not actions:  # line 578
        return []  # line 578
    sources = None  # type: List[str]  # line 579
    targets = None  # type: List[str]  # line 579
    sources, targets = [list(l) for l in zip(*actions)]  # line 580
    last = len(actions)  # type: int  # line 581
    while last > 1:  # line 582
        clean = True  # type: bool  # line 583
        for i in range(1, last):  # line 584
            try:  # line 585
                index = targets[:i].index(sources[i])  # type: int  # line 586
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 587
                targets.insert(index, targets.pop(i))  # line 588
                clean = False  # line 589
            except:  # target not found in sources: good!  # line 590
                continue  # target not found in sources: good!  # line 590
        if clean:  # line 591
            break  # line 591
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 592
    if exitOnConflict:  # line 593
        for i in range(1, len(actions)):  # line 593
            if sources[i] in targets[:i]:  # line 593
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 593
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 594

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 596
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 597
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 598
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 599

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str]]':  # line 601
    ''' Returns (root-normalized) set of --only arguments, and set or --except arguments. '''  # line 602
    root = os.getcwd()  # type: str  # zero necessary as marker for last start position  # line 603
    index = 0  # type: int  # zero necessary as marker for last start position  # line 603
    onlys = []  # type: List[str]  # line 604
    excps = []  # type: List[str]  # line 604
    remotes = []  # type: List[str]  # line 604
    for key, container in [("--only", onlys), ("--except", excps), ("--remote", remotes)]:  # line 605
        while True:  # line 606
            try:  # line 607
                index = 1 + listindex(options, key, index)  # line 608
                container.append(options[index])  # line 609
                del options[index]  # line 610
                del options[index - 1]  # line 611
            except:  # no more found  # line 612
                break  # no more found  # line 612
        index = 0  # line 613
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(".." + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(".." + SLASH))) if excps else None, remotes)  # line 614
