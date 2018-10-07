#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x85204790

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
        try:  # line 58
            init(wrap=False)  # line 59
            if useColor[0] is None:  # very initial  # line 60
                sys.stdout = AnsiToWin32(sys.stdout).stream  # TODO replace by "better exceptions" code  # line 61
                sys.stderr = AnsiToWin32(sys.stderr).stream  # line 62
        except:  # line 63
            pass  # line 63
    else:  # line 64
        try:  # line 65
            deinit()  # line 65
        except:  # line 66
            pass  # line 66
    useColor[0] = enable  # line 67

Fore = Accessor({k: "" for k in ["RESET", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "YELLOW"]})  # type: Dict[str, str]  # line 69
Back = Fore  # type: Dict[str, str]  # line 69
Style = Accessor({k: "" for k in ["NORMAL", "BRIGHT", "RESET_ALL"]})  # type: Dict[str, str]  # line 70
MARKER = Accessor({"value": usage.MARKER_TEXT})  # type: str  # assume default text-only  # line 71
try:  # line 72
    import colorama.ansitowin32  # line 73
    if colorama.ansitowin32.is_a_tty(sys.stderr):  # list of ansi codes: http://bluesock.org/~willkg/dev/ansi.html  # line 74
        from colorama import init  # line 75
        from colorama import deinit  # line 75
        from colorama import AnsiToWin32  # line 75
        from colorama import Back  # line 75
        from colorama import Fore  # line 75
        from colorama import Style  # line 75
        MARKER_COLOR = Fore.WHITE + usage.MARKER_TEXT + Fore.RESET  # type: str  # line 76
        if sys.platform == "win32":  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 77
            Style.BRIGHT = ""  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 77
        enableColor()  # line 78
except:  # if library not installed, use fallback even for colored texts  # line 79
    MARKER_COLOR = usage.MARKER_TEXT  # if library not installed, use fallback even for colored texts  # line 79

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 81
    Number = TypeVar("Number", int, float)  # line 82
    class Counter(Generic[Number]):  # line 83
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 84
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 85
            _.value = initial  # type: Number  # line 85
        def inc(_, by: 'Number'=1) -> 'Number':  # line 86
            _.value += by  # line 86
            return _.value  # line 86
else:  # line 87
    class Counter:  # line 88
        def __init__(_, initial=0) -> 'None':  # line 89
            _.value = initial  # line 89
        def inc(_, by=1):  # line 90
            _.value += by  # line 90
            return _.value  # line 90

class ProgressIndicator(Counter):  # line 92
    ''' Manages a rotating progress indicator. '''  # line 93
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 94
        super(ProgressIndicator, _).__init__(-1)  # line 94
        _.symbols = symbols  # line 94
        _.timer = time.time()  # type: float  # line 94
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 94
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 95
        ''' Returns a value only if a certain time has passed. '''  # line 96
        newtime = time.time()  # type: float  # line 97
        if newtime - _.timer < .1:  # line 98
            return None  # line 98
        _.timer = newtime  # line 99
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 100
        if _.callback:  # line 101
            _.callback(sign)  # line 101
        return sign  # line 102

class Logger:  # line 104
    ''' Logger that supports joining many items. '''  # line 105
    def __init__(_, log) -> 'None':  # line 106
        _._log = log  # line 106
    def debug(_, *s):  # line 107
        _._log.debug(pure.sjoin(*s))  # line 107
    def info(_, *s):  # line 108
        _._log.info(pure.sjoin(*s))  # line 108
    def warn(_, *s):  # line 109
        _._log.warning(pure.sjoin(*s))  # line 109
    def error(_, *s):  # line 110
        _._log.error(pure.sjoin(*s))  # line 110


# Constants
_log = Logger(logging.getLogger(__name__))  # line 114
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 114
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress", "useChangesCommand", "useUnicodeFont", "useColorOutput"]  # type: List[str]  # line 115
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 116
CONFIGURABLE_INTS = ["logLines", "diffLines"]  # type: List[str]  # line 117
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 118
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 119
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 120
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 121
BACKUP_SUFFIX = "_last"  # type: str  # line 122
metaFolder = ".sos"  # type: str  # line 123
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 124
metaFile = ".meta"  # type: str  # line 125
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 126
KIBI = 1 << 10  # type: int  # line 127
MEBI = 1 << 20  # type: int  # line 127
GIBI = 1 << 30  # type: int  # line 127
bufSize = MEBI  # type: int  # line 128
UTF8 = "utf_8"  # type: str  # early used constant, not defined in standard library  # line 129
SVN = "svn"  # type: str  # line 130
SLASH = "/"  # type: str  # line 131
PARENT = ".."  # type: str  # line 132
DOT_SYMBOL = "\u00b7"  # type: str  # line 133
MULT_SYMBOL = "\u00d7"  # type: str  # line 134
CROSS_SYMBOL = "\u2716"  # type: str  # line 135
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 136
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 137
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in "this revision"  # line 138
MOVE_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 139
METADATA_FORMAT = 2  # type: int  # counter for (partially incompatible) consecutive formats (was undefined, "1" is the first numbered format version after that)  # line 140
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 141
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 142
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS, RCS have probably different per-file operation  # line 143
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 144
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[_coconut.typing.Optional[bytes], str]  # line 145
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[_coconut.typing.Optional[str], int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 146
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "useColorOutput": True, "diffLines": 2, "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 147


# Functions
def siSize(size: 'int') -> 'str':  # line 164
    ''' Returns number and unit. '''  # line 165
    return "%.2f MiB" % (float(size) / MEBI) if size > 1.25 * MEBI else ("%.2f KiB" % (float(size) / KIBI) if size > 1.25 * KIBI else ("%d bytes" % size))  # line 166

def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 168
    color = useColor and color or ""  # line 169
    reset = Fore.RESET if useColor and color else ""  # line 170
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 171
    sys.stdout.flush()  # PEP528 compatibility  # line 171
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 173
    color = useColor and color or ""  # line 174
    reset = Fore.RESET if useColor and color else ""  # line 175
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 176
    sys.stderr.flush()  # line 176
@_coconut_tco  # line 177
def encode(s: 'str') -> 'bytes':  # line 177
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 178
@_coconut_tco  # for os->py access of reading filenames  # line 179
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 179
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 179
try:  # line 180
    import chardet  # https://github.com/chardet/chardet  # line 181
    def detectEncoding(binary: 'bytes') -> 'str':  # line 182
        return chardet.detect(binary)["encoding"]  # line 182
except:  # Guess the encoding  # line 183
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 183
        ''' Fallback if chardet library missing. '''  # line 184
        try:  # line 185
            binary.decode(UTF8)  # line 185
            return UTF8  # line 185
        except UnicodeError:  # line 186
            pass  # line 186
        try:  # line 187
            binary.decode("utf_16")  # line 187
            return "utf_16"  # line 187
        except UnicodeError:  # line 188
            pass  # line 188
        try:  # line 189
            binary.decode("cp1252")  # line 189
            return "cp1252"  # line 189
        except UnicodeError:  # line 190
            pass  # line 190
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 191

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 193
    try:  # line 194
        return func()  # line 194
    except:  # line 195
        return default  # line 195

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 197
    try:  # line 198
        return func()  # line 198
    except Exception as E:  # line 199
        onError(E)  # line 199

def removePath(key: 'str', value: 'str') -> 'str':  # line 201
    ''' Cleanup of user-specified global file patterns, used in config. '''  # TODO improve  # line 202
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 203

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 205
    ''' Updates a dictionary by another one, returning a new copy without touching any of the passed dictionaries. '''  # line 206
    d = dict(dikt)  # type: Dict[Any, Any]  # line 207
    d.update(by)  # line 207
    return d  # line 207

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # line 209
    ''' Abstraction for opening both compressed and plain files. '''  # line 210
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # line 211

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 213
    ''' Determine EOL style from a binary string. '''  # line 214
    lf = file.count(b"\n")  # type: int  # line 215
    cr = file.count(b"\r")  # type: int  # line 216
    crlf = file.count(b"\r\n")  # type: int  # line 217
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 218
        if lf != crlf or cr != crlf:  # line 219
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 219
        return b"\r\n"  # line 220
    if lf != 0 and cr != 0:  # line 221
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 221
    if lf > cr:  # Linux/Unix  # line 222
        return b"\n"  # Linux/Unix  # line 222
    if cr > lf:  # older 8-bit machines  # line 223
        return b"\r"  # older 8-bit machines  # line 223
    return None  # no new line contained, cannot determine  # line 224

if TYPE_CHECKING:  # line 226
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 227
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 227
else:  # line 228
    def safeSplit(s, d=None):  # line 229
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 229

@_coconut_tco  # line 231
def hashStr(datas: 'str') -> 'str':  # line 231
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 231

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 233
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 233

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 235
    return lizt[index:].index(what) + index  # line 235

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 237
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 237

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 239
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 239

def Exit(message: 'str'="", code=1):  # line 241
    lines = message.split("\n")  # type: List[str]  # line 242
    printe("[", nl="")  # line 243
    printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN, nl="")  # line 244
    printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + lines[0] + ".") if lines[0] != "" else ""))  # line 245
    if len(lines) > 1:  # line 246
        printe("\n".join(lines[1:]))  # line 249
    sys.exit(code)  # line 250

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 252
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 253
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 254
        raise Exception("Cannot possibly strings pack into specified length")  # line 254
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 255
        prefix += separator + ((process)(strings.pop(0)))  # line 255
    return prefix  # line 256

def exception(E):  # line 258
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 259
    printo(str(E))  # line 260
    import traceback  # line 261
    traceback.print_exc()  # line 262
    traceback.print_stack()  # line 263

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 265
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 266
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 267
    _hash = hashlib.sha256()  # line 268
    wsize = 0  # type: int  # line 269
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 270
        Exit("Hash collision detected. Leaving repository in inconsistent state", 1)  # HINT this exits immediately  # line 271
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 272
    with open(encode(path), "rb") as fd:  # line 273
        while True:  # line 274
            buffer = fd.read(bufSize)  # type: bytes  # line 275
            _hash.update(buffer)  # line 276
            if to:  # line 277
                to.write(buffer)  # line 277
            if len(buffer) < bufSize:  # line 278
                break  # line 278
            if indicator:  # line 279
                indicator.getIndicator()  # line 279
        if to:  # line 280
            to.close()  # line 281
            wsize = os.stat(encode(saveTo[0])).st_size  # line 282
            for remote in saveTo[1:]:  # line 283
                tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 283
    return (_hash.hexdigest(), wsize)  # line 284

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 286
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 287
    for k, v in map.items():  # line 288
        if k in params:  # line 288
            return v  # line 288
    return default  # line 289

@_coconut_tco  # line 291
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 291
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 291

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 293
    lines = []  # type: List[str]  # line 294
    if filename is not None:  # line 295
        with open(encode(filename), "rb") as fd:  # line 295
            content = fd.read()  # line 295
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 296
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 297
    if filename is not None:  # line 298
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 298
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 298
    elif content is not None:  # line 299
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 299
    else:  # line 300
        return (sys.getdefaultencoding(), b"\n", [])  # line 300
    if ignoreWhitespace:  # line 301
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 301
    return (encoding, eol, lines)  # line 302

if TYPE_CHECKING:  # line 304
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 305
    @_coconut_tco  # line 306
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 306
        ''' A better makedata() version. '''  # line 307
        r = _old._asdict()  # type: Dict[str, Any]  # line 308
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 309
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 310
else:  # line 311
    @_coconut_tco  # line 312
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 312
        ''' A better makedata() version. '''  # line 313
        r = _old._asdict()  # line 314
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 315
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 316

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 318
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 319
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 320
    for path, info in changes.additions.items():  # line 321
        for dpath, dinfo in changes.deletions.items():  # line 321
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 322
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 323
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 324
                break  # deletions loop, continue with next addition  # line 325
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 326

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 328
    ''' Default can be a selection from choice and allows empty input. '''  # line 329
    while True:  # line 330
        selection = input(text).strip().lower()  # line 331
        if selection != "" and selection in choices:  # line 332
            break  # line 332
        if selection == "" and default is not None:  # line 333
            selection = default  # line 333
            break  # line 333
    return selection  # line 334

def user_block_input(output: 'List[str]'):  # line 336
    ''' Side-effect appending to input list. '''  # line 337
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 338
    line = sep  # type: str  # line 338
    while True:  # line 339
        line = input("> ")  # line 340
        if line == sep:  # line 341
            break  # line 341
        output.append(line)  # writes to caller-provided list reference  # line 342

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 344
    encoding = None  # type: str  # line 345
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 345
    othr = None  # type: _coconut.typing.Sequence[str]  # line 345
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 345
    curr = None  # type: _coconut.typing.Sequence[str]  # line 345
    try:  # line 346
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 347
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 348
    except Exception as E:  # line 349
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname), E))  # line 349
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 350
        printo(line)  # from generator expression  # line 350

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 352
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 367
    encoding = None  # type: str  # line 368
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 368
    othr = None  # type: _coconut.typing.Sequence[str]  # line 368
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 368
    curr = None  # type: _coconut.typing.Sequence[str]  # line 368
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 369
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 370
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 371
    except Exception as E:  # line 372
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname), E))  # line 372
    if None not in [othreol, curreol] and othreol != curreol:  # line 373
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 373
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 374
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 375
    tmp = []  # type: List[str]  # block lines  # line 376
    last = " "  # type: str  # "into"-file offset for remark lines  # line 377
    no = None  # type: int  # "into"-file offset for remark lines  # line 377
    line = None  # type: str  # "into"-file offset for remark lines  # line 377
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 377
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 378
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 379
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 379
            continue  # continue filling current block, no matter what type of block it is  # line 379
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 380
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 380
        if last == " ":  # block is same in both files  # line 381
            if len(tmp) > 0:  # avoid adding empty keep block  # line 382
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 382
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 383
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 384
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 385
                offset += len(blocks[-2].lines)  # line 386
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 387
                blocks.pop()  # line 388
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 389
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 390
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 391
                offset += len(blocks[-1].lines)  # line 392
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 393
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 394
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 395
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 395
        last = line[0]  # line 396
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 397
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 399
    debug("Diff blocks: " + repr(blocks))  # line 400
    if diffOnly:  # line 401
        return (blocks, nl)  # line 401

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 404
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 404
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 404
    selection = ""  # type: str  # clean list of strings  # line 404
    for block in blocks:  # line 405
        if block.tipe == MergeBlockType.KEEP:  # line 406
            output.extend(block.lines)  # line 406
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 407
            output.extend(block.lines)  # line 409
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 410
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 411
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 412
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 413
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 414
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 415
                while True:  # line 416
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 417
                    if op in "tb":  # line 418
                        output.extend(block.lines)  # line 418
                    if op in "ib":  # line 419
                        output.extend(block.replaces.lines)  # line 419
                    if op == "u":  # line 420
                        user_block_input(output)  # line 420
                    if op in "tbiu":  # line 421
                        break  # line 421
            else:  # more than one line and not ask  # line 422
                if mergeOperation == MergeOperation.REMOVE:  # line 423
                    pass  # line 423
                elif mergeOperation == MergeOperation.BOTH:  # line 424
                    output.extend(block.lines)  # line 424
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 425
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 425
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 426
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 427
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 429
                if selection in "ao":  # line 430
                    if block.tipe == MergeBlockType.INSERT:  # line 431
                        add_all = "y" if selection == "a" else "n"  # line 431
                        selection = add_all  # line 431
                    else:  # REMOVE case  # line 432
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 432
                        selection = del_all  # REMOVE case  # line 432
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 433
                output.extend(block.lines)  # line 435
    debug("Merge output: " + "; ".join(output))  # line 436
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 437
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 440
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 440
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 443
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 444
    blocks = []  # type: List[MergeBlock]  # line 445
    for i, line in enumerate(out):  # line 446
        if line[0] == "+":  # line 447
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 448
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 449
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 450
                else:  # first + in block  # line 451
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 452
            else:  # last line of + block  # line 453
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 454
                    blocks[-1].lines.append(line[2])  # line 455
                else:  # single line  # line 456
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 457
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 458
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 459
                    blocks.pop()  # line 459
        elif line[0] == "-":  # line 460
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 461
                blocks[-1].lines.append(line[2])  # line 462
            else:  # first in block  # line 463
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 464
        elif line[0] == " ":  # line 465
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 466
                blocks[-1].lines.append(line[2])  # line 467
            else:  # first in block  # line 468
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 469
        else:  # line 470
            raise Exception("Cannot parse diff line %r" % line)  # line 470
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 471
    if diffOnly:  # line 472
        return blocks  # line 472
    out[:] = []  # line 473
    for i, block in enumerate(blocks):  # line 474
        if block.tipe == MergeBlockType.KEEP:  # line 475
            out.extend(block.lines)  # line 475
        elif block.tipe == MergeBlockType.REPLACE:  # line 476
            if mergeOperation == MergeOperation.ASK:  # line 477
                printo(pure.ajoin("- ", othr))  # line 478
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 479
                printo("+ " + (" " * i) + block.lines[0])  # line 480
                printo(pure.ajoin("+ ", into))  # line 481
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 482
                if op in "tb":  # line 483
                    out.extend(block.lines)  # line 483
                    break  # line 483
                if op in "ib":  # line 484
                    out.extend(block.replaces.lines)  # line 484
                    break  # line 484
                if op == "m":  # line 485
                    user_block_input(out)  # line 485
                    break  # line 485
            else:  # non-interactive  # line 486
                if mergeOperation == MergeOperation.REMOVE:  # line 487
                    pass  # line 487
                elif mergeOperation == MergeOperation.BOTH:  # line 488
                    out.extend(block.lines)  # line 488
                elif mergeOperation == MergeOperation.INSERT:  # line 489
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 489
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 490
            out.extend(block.lines)  # line 490
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 491
            out.extend(block.lines)  # line 491
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 493

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 495
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 498
    debug("Detecting root folders...")  # line 499
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 500
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 501
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 502
        contents = set(os.listdir(path))  # type: Set[str]  # line 503
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 504
        choice = None  # type: _coconut.typing.Optional[str]  # line 505
        if len(vcss) > 1:  # line 506
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 507
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 508
        elif len(vcss) > 0:  # line 509
            choice = vcss[0]  # line 509
        if not vcs[0] and choice:  # memorize current repo root  # line 510
            vcs = (path, choice)  # memorize current repo root  # line 510
        new = os.path.dirname(path)  # get parent path  # line 511
        if new == path:  # avoid infinite loop  # line 512
            break  # avoid infinite loop  # line 512
        path = new  # line 513
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 514
        if vcs[0]:  # already detected vcs base and command  # line 515
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 515
        sos = path  # line 516
        while True:  # continue search for VCS base  # line 517
            contents = set(os.listdir(path))  # line 518
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 519
            choice = None  # line 520
            if len(vcss) > 1:  # line 521
                choice = SVN if SVN in vcss else vcss[0]  # line 522
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 523
            elif len(vcss) > 0:  # line 524
                choice = vcss[0]  # line 524
            if choice:  # line 525
                return (sos, path, choice)  # line 525
            new = os.path.dirname(path)  # get parent path  # line 526
            if new == path:  # no VCS folder found  # line 527
                return (sos, None, None)  # no VCS folder found  # line 527
            path = new  # line 528
    return (None, vcs[0], vcs[1])  # line 529

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 531
    index = 0  # type: int  # line 532
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 533
    while index < len(pattern):  # line 534
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 535
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 535
            continue  # line 535
        if pattern[index] in "*?":  # line 536
            count = 1  # type: int  # line 537
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 538
                count += 1  # line 538
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 539
            index += count  # line 539
            continue  # line 539
        if pattern[index:index + 2] == "[!":  # line 540
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 540
            index += len(out[-1][1])  # line 540
            continue  # line 540
        count = 1  # line 541
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 542
            count += 1  # line 542
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 543
        index += count  # line 543
    return out  # line 544

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 546
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 547
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 548
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 550
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 550
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 551
        Exit("Source and target file patterns differ in semantics")  # line 551
    return (ot, nt)  # line 552

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 554
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 555
    pairs = []  # type: List[Tuple[str, str]]  # line 556
    for filename in filenames:  # line 557
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 558
        nextliteral = 0  # type: int  # line 559
        index = 0  # type: int  # line 559
        parsedOld = []  # type: List[GlobBlock2]  # line 560
        for part in oldPattern:  # match everything in the old filename  # line 561
            if part.isLiteral:  # line 562
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 562
                index += len(part.content)  # line 562
                nextliteral += 1  # line 562
            elif part.content.startswith("?"):  # line 563
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 563
                index += len(part.content)  # line 563
            elif part.content.startswith("["):  # line 564
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 564
                index += 1  # line 564
            elif part.content == "*":  # line 565
                if nextliteral >= len(literals):  # line 566
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 566
                    break  # line 566
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 567
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 568
                index = nxt  # line 568
            else:  # line 569
                Exit("Invalid file pattern specified for move/rename")  # line 569
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 570
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 571
        nextliteral = 0  # line 572
        nextglob = 0  # type: int  # line 572
        outname = []  # type: List[str]  # line 573
        for part in newPattern:  # generate new filename  # line 574
            if part.isLiteral:  # line 575
                outname.append(literals[nextliteral].content)  # line 575
                nextliteral += 1  # line 575
            else:  # line 576
                outname.append(globs[nextglob].matches)  # line 576
                nextglob += 1  # line 576
        pairs.append((filename, "".join(outname)))  # line 577
    return pairs  # line 578

@_coconut_tco  # line 580
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 580
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 584
    if not actions:  # line 585
        return []  # line 585
    sources = None  # type: List[str]  # line 586
    targets = None  # type: List[str]  # line 586
    sources, targets = [list(l) for l in zip(*actions)]  # line 587
    last = len(actions)  # type: int  # line 588
    while last > 1:  # line 589
        clean = True  # type: bool  # line 590
        for i in range(1, last):  # line 591
            try:  # line 592
                index = targets[:i].index(sources[i])  # type: int  # line 593
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 594
                targets.insert(index, targets.pop(i))  # line 595
                clean = False  # line 596
            except:  # target not found in sources: good!  # line 597
                continue  # target not found in sources: good!  # line 597
        if clean:  # line 598
            break  # line 598
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 599
    if exitOnConflict:  # line 600
        for i in range(1, len(actions)):  # line 600
            if sources[i] in targets[:i]:  # line 600
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 600
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 601

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 603
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 604
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 605
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 606

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str]]':  # line 608
    ''' Returns (root-normalized) set of --only and --except arguments. '''  # line 609
    root = os.getcwd()  # type: str  # line 610
    onlys = []  # type: List[str]  # line 611
    excps = []  # type: List[str]  # line 611
    remotes = []  # type: List[str]  # line 611
    for keys, container in [(("--only", "--include"), onlys), (("--except", "--exclude"), excps), (("--remote",), remotes)]:  # line 612
        founds = [i for i in range(len(options)) if any([options[i].startswith(key) for key in keys])]  # assuming no more than one = in the string  # line 613
        for i in reversed(founds):  # line 614
            if "=" in options[i]:  # line 615
                container.append(options[i].split("=")[1])  # line 616
            elif i + 1 < len(options):  # in case last --only has no argument  # line 617
                container.append(options[i + 1])  # line 618
                del options[i + 1]  # line 619
            del options[i]  # reverse removal  # line 620
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(PARENT + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(PARENT + SLASH))) if excps else None, remotes)  # line 621
