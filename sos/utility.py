#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xe8788664

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
PARENT = ".."  # type: str  # line 128
DOT_SYMBOL = "\u00b7"  # type: str  # line 129
MULT_SYMBOL = "\u00d7"  # type: str  # line 130
CROSS_SYMBOL = "\u2716"  # type: str  # line 131
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 132
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 133
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in "this revision"  # line 134
MOVE_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 135
METADATA_FORMAT = 2  # type: int  # counter for (partially incompatible) consecutive formats (was undefined, "1" is the first numbered format version after that)  # line 136
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 137
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 138
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS, RCS have probably different per-file operation  # line 139
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 140
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[_coconut.typing.Optional[bytes], str]  # line 141
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[_coconut.typing.Optional[str], int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 142
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "useColorOutput": True, "diffLines": 2, "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 143


# Functions
def siSize(size: 'int') -> 'str':  # line 160
    ''' Returns number and unit. '''  # line 161
    return "%.2f MiB" % (float(size) / MEBI) if size > 1.25 * MEBI else ("%.2f KiB" % (float(size) / KIBI) if size > 1.25 * KIBI else ("%d bytes" % size))  # line 162

def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 164
    color = useColor and color or ""  # line 165
    reset = Fore.RESET if useColor and color else ""  # line 166
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 167
    sys.stdout.flush()  # PEP528 compatibility  # line 167
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 169
    color = useColor and color or ""  # line 170
    reset = Fore.RESET if useColor and color else ""  # line 171
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 172
    sys.stderr.flush()  # line 172
@_coconut_tco  # line 173
def encode(s: 'str') -> 'bytes':  # line 173
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 174
@_coconut_tco  # for os->py access of reading filenames  # line 175
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 175
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 175
try:  # line 176
    import chardet  # https://github.com/chardet/chardet  # line 177
    def detectEncoding(binary: 'bytes') -> 'str':  # line 178
        return chardet.detect(binary)["encoding"]  # line 178
except:  # Guess the encoding  # line 179
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 179
        ''' Fallback if chardet library missing. '''  # line 180
        try:  # line 181
            binary.decode(UTF8)  # line 181
            return UTF8  # line 181
        except UnicodeError:  # line 182
            pass  # line 182
        try:  # line 183
            binary.decode("utf_16")  # line 183
            return "utf_16"  # line 183
        except UnicodeError:  # line 184
            pass  # line 184
        try:  # line 185
            binary.decode("cp1252")  # line 185
            return "cp1252"  # line 185
        except UnicodeError:  # line 186
            pass  # line 186
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 187

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 189
    try:  # line 190
        return func()  # line 190
    except:  # line 191
        return default  # line 191

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 193
    try:  # line 194
        return func()  # line 194
    except Exception as E:  # line 195
        onError(E)  # line 195

def removePath(key: 'str', value: 'str') -> 'str':  # line 197
    ''' Cleanup of user-specified global file patterns, used in config. '''  # TODO improve  # line 198
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 199

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 201
    ''' Updates a dictionary by another one, returning a new copy without touching any of the passed dictionaries. '''  # line 202
    d = dict(dikt)  # type: Dict[Any, Any]  # line 203
    d.update(by)  # line 203
    return d  # line 203

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # line 205
    ''' Abstraction for opening both compressed and plain files. '''  # line 206
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # line 207

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 209
    ''' Determine EOL style from a binary string. '''  # line 210
    lf = file.count(b"\n")  # type: int  # line 211
    cr = file.count(b"\r")  # type: int  # line 212
    crlf = file.count(b"\r\n")  # type: int  # line 213
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 214
        if lf != crlf or cr != crlf:  # line 215
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 215
        return b"\r\n"  # line 216
    if lf != 0 and cr != 0:  # line 217
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 217
    if lf > cr:  # Linux/Unix  # line 218
        return b"\n"  # Linux/Unix  # line 218
    if cr > lf:  # older 8-bit machines  # line 219
        return b"\r"  # older 8-bit machines  # line 219
    return None  # no new line contained, cannot determine  # line 220

if TYPE_CHECKING:  # line 222
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 223
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 223
else:  # line 224
    def safeSplit(s, d=None):  # line 225
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 225

@_coconut_tco  # line 227
def hashStr(datas: 'str') -> 'str':  # line 227
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 227

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 229
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 229

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 231
    return lizt[index:].index(what) + index  # line 231

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 233
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 233

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 235
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 235

def Exit(message: 'str'="", code=1):  # line 237
    lines = message.split("\n")  # type: List[str]  # line 238
    printe("[", nl="")  # line 239
    printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN, nl="")  # line 240
    printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + lines[0] + ".") if lines[0] != "" else ""))  # line 241
    if len(lines) > 1:  # line 242
        printe("\n".join(lines[1:]))  # line 245
    sys.exit(code)  # line 246

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 248
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 249
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 250
        raise Exception("Cannot possibly strings pack into specified length")  # line 250
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 251
        prefix += separator + ((process)(strings.pop(0)))  # line 251
    return prefix  # line 252

def exception(E):  # line 254
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 255
    printo(str(E))  # line 256
    import traceback  # line 257
    traceback.print_exc()  # line 258
    traceback.print_stack()  # line 259

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 261
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 262
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 263
    _hash = hashlib.sha256()  # line 264
    wsize = 0  # type: int  # line 265
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 266
        Exit("Hash collision detected. Leaving repository in inconsistent state", 1)  # HINT this exits immediately  # line 267
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 268
    with open(encode(path), "rb") as fd:  # line 269
        while True:  # line 270
            buffer = fd.read(bufSize)  # type: bytes  # line 271
            _hash.update(buffer)  # line 272
            if to:  # line 273
                to.write(buffer)  # line 273
            if len(buffer) < bufSize:  # line 274
                break  # line 274
            if indicator:  # line 275
                indicator.getIndicator()  # line 275
        if to:  # line 276
            to.close()  # line 277
            wsize = os.stat(encode(saveTo[0])).st_size  # line 278
            for remote in saveTo[1:]:  # line 279
                tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 279
    return (_hash.hexdigest(), wsize)  # line 280

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 282
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 283
    for k, v in map.items():  # line 284
        if k in params:  # line 284
            return v  # line 284
    return default  # line 285

@_coconut_tco  # line 287
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 287
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 287

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 289
    lines = []  # type: List[str]  # line 290
    if filename is not None:  # line 291
        with open(encode(filename), "rb") as fd:  # line 291
            content = fd.read()  # line 291
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 292
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 293
    if filename is not None:  # line 294
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 294
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 294
    elif content is not None:  # line 295
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 295
    else:  # line 296
        return (sys.getdefaultencoding(), b"\n", [])  # line 296
    if ignoreWhitespace:  # line 297
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 297
    return (encoding, eol, lines)  # line 298

if TYPE_CHECKING:  # line 300
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 301
    @_coconut_tco  # line 302
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 302
        ''' A better makedata() version. '''  # line 303
        r = _old._asdict()  # type: Dict[str, Any]  # line 304
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 305
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 306
else:  # line 307
    @_coconut_tco  # line 308
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 308
        ''' A better makedata() version. '''  # line 309
        r = _old._asdict()  # line 310
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 311
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 312

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 314
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 315
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 316
    for path, info in changes.additions.items():  # line 317
        for dpath, dinfo in changes.deletions.items():  # line 317
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 318
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 319
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 320
                break  # deletions loop, continue with next addition  # line 321
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 322

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 324
    ''' Default can be a selection from choice and allows empty input. '''  # line 325
    while True:  # line 326
        selection = input(text).strip().lower()  # line 327
        if selection != "" and selection in choices:  # line 328
            break  # line 328
        if selection == "" and default is not None:  # line 329
            selection = default  # line 329
            break  # line 329
    return selection  # line 330

def user_block_input(output: 'List[str]'):  # line 332
    ''' Side-effect appending to input list. '''  # line 333
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 334
    line = sep  # type: str  # line 334
    while True:  # line 335
        line = input("> ")  # line 336
        if line == sep:  # line 337
            break  # line 337
        output.append(line)  # writes to caller-provided list reference  # line 338

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 340
    encoding = None  # type: str  # line 341
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 341
    othr = None  # type: _coconut.typing.Sequence[str]  # line 341
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 341
    curr = None  # type: _coconut.typing.Sequence[str]  # line 341
    try:  # line 342
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 343
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 344
    except Exception as E:  # line 345
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname), E))  # line 345
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 346
        printo(line)  # from generator expression  # line 346

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 348
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 363
    encoding = None  # type: str  # line 364
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 364
    othr = None  # type: _coconut.typing.Sequence[str]  # line 364
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 364
    curr = None  # type: _coconut.typing.Sequence[str]  # line 364
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 365
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 366
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 367
    except Exception as E:  # line 368
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname), E))  # line 368
    if None not in [othreol, curreol] and othreol != curreol:  # line 369
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 369
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 370
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 371
    tmp = []  # type: List[str]  # block lines  # line 372
    last = " "  # type: str  # "into"-file offset for remark lines  # line 373
    no = None  # type: int  # "into"-file offset for remark lines  # line 373
    line = None  # type: str  # "into"-file offset for remark lines  # line 373
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 373
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 374
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 375
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 375
            continue  # continue filling current block, no matter what type of block it is  # line 375
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 376
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 376
        if last == " ":  # block is same in both files  # line 377
            if len(tmp) > 0:  # avoid adding empty keep block  # line 378
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 378
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 379
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 380
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 381
                offset += len(blocks[-2].lines)  # line 382
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 383
                blocks.pop()  # line 384
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 385
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 386
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 387
                offset += len(blocks[-1].lines)  # line 388
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 389
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 390
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 391
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 391
        last = line[0]  # line 392
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 393
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 395
    debug("Diff blocks: " + repr(blocks))  # line 396
    if diffOnly:  # line 397
        return (blocks, nl)  # line 397

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 400
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 400
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 400
    selection = ""  # type: str  # clean list of strings  # line 400
    for block in blocks:  # line 401
        if block.tipe == MergeBlockType.KEEP:  # line 402
            output.extend(block.lines)  # line 402
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 403
            output.extend(block.lines)  # line 405
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 406
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 407
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 408
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 409
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 410
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 411
                while True:  # line 412
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 413
                    if op in "tb":  # line 414
                        output.extend(block.lines)  # line 414
                    if op in "ib":  # line 415
                        output.extend(block.replaces.lines)  # line 415
                    if op == "u":  # line 416
                        user_block_input(output)  # line 416
                    if op in "tbiu":  # line 417
                        break  # line 417
            else:  # more than one line and not ask  # line 418
                if mergeOperation == MergeOperation.REMOVE:  # line 419
                    pass  # line 419
                elif mergeOperation == MergeOperation.BOTH:  # line 420
                    output.extend(block.lines)  # line 420
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 421
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 421
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 422
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 423
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 425
                if selection in "ao":  # line 426
                    if block.tipe == MergeBlockType.INSERT:  # line 427
                        add_all = "y" if selection == "a" else "n"  # line 427
                        selection = add_all  # line 427
                    else:  # REMOVE case  # line 428
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 428
                        selection = del_all  # REMOVE case  # line 428
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 429
                output.extend(block.lines)  # line 431
    debug("Merge output: " + "; ".join(output))  # line 432
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 433
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 436
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 436
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 439
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 440
    blocks = []  # type: List[MergeBlock]  # line 441
    for i, line in enumerate(out):  # line 442
        if line[0] == "+":  # line 443
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 444
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 445
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 446
                else:  # first + in block  # line 447
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 448
            else:  # last line of + block  # line 449
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 450
                    blocks[-1].lines.append(line[2])  # line 451
                else:  # single line  # line 452
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 453
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 454
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 455
                    blocks.pop()  # line 455
        elif line[0] == "-":  # line 456
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 457
                blocks[-1].lines.append(line[2])  # line 458
            else:  # first in block  # line 459
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 460
        elif line[0] == " ":  # line 461
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 462
                blocks[-1].lines.append(line[2])  # line 463
            else:  # first in block  # line 464
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 465
        else:  # line 466
            raise Exception("Cannot parse diff line %r" % line)  # line 466
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 467
    if diffOnly:  # line 468
        return blocks  # line 468
    out[:] = []  # line 469
    for i, block in enumerate(blocks):  # line 470
        if block.tipe == MergeBlockType.KEEP:  # line 471
            out.extend(block.lines)  # line 471
        elif block.tipe == MergeBlockType.REPLACE:  # line 472
            if mergeOperation == MergeOperation.ASK:  # line 473
                printo(pure.ajoin("- ", othr))  # line 474
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 475
                printo("+ " + (" " * i) + block.lines[0])  # line 476
                printo(pure.ajoin("+ ", into))  # line 477
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 478
                if op in "tb":  # line 479
                    out.extend(block.lines)  # line 479
                    break  # line 479
                if op in "ib":  # line 480
                    out.extend(block.replaces.lines)  # line 480
                    break  # line 480
                if op == "m":  # line 481
                    user_block_input(out)  # line 481
                    break  # line 481
            else:  # non-interactive  # line 482
                if mergeOperation == MergeOperation.REMOVE:  # line 483
                    pass  # line 483
                elif mergeOperation == MergeOperation.BOTH:  # line 484
                    out.extend(block.lines)  # line 484
                elif mergeOperation == MergeOperation.INSERT:  # line 485
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 485
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 486
            out.extend(block.lines)  # line 486
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 487
            out.extend(block.lines)  # line 487
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 489

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 491
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 494
    debug("Detecting root folders...")  # line 495
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 496
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 497
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 498
        contents = set(os.listdir(path))  # type: Set[str]  # line 499
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 500
        choice = None  # type: _coconut.typing.Optional[str]  # line 501
        if len(vcss) > 1:  # line 502
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 503
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 504
        elif len(vcss) > 0:  # line 505
            choice = vcss[0]  # line 505
        if not vcs[0] and choice:  # memorize current repo root  # line 506
            vcs = (path, choice)  # memorize current repo root  # line 506
        new = os.path.dirname(path)  # get parent path  # line 507
        if new == path:  # avoid infinite loop  # line 508
            break  # avoid infinite loop  # line 508
        path = new  # line 509
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 510
        if vcs[0]:  # already detected vcs base and command  # line 511
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 511
        sos = path  # line 512
        while True:  # continue search for VCS base  # line 513
            contents = set(os.listdir(path))  # line 514
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 515
            choice = None  # line 516
            if len(vcss) > 1:  # line 517
                choice = SVN if SVN in vcss else vcss[0]  # line 518
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 519
            elif len(vcss) > 0:  # line 520
                choice = vcss[0]  # line 520
            if choice:  # line 521
                return (sos, path, choice)  # line 521
            new = os.path.dirname(path)  # get parent path  # line 522
            if new == path:  # no VCS folder found  # line 523
                return (sos, None, None)  # no VCS folder found  # line 523
            path = new  # line 524
    return (None, vcs[0], vcs[1])  # line 525

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 527
    index = 0  # type: int  # line 528
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 529
    while index < len(pattern):  # line 530
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 531
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 531
            continue  # line 531
        if pattern[index] in "*?":  # line 532
            count = 1  # type: int  # line 533
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 534
                count += 1  # line 534
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 535
            index += count  # line 535
            continue  # line 535
        if pattern[index:index + 2] == "[!":  # line 536
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 536
            index += len(out[-1][1])  # line 536
            continue  # line 536
        count = 1  # line 537
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 538
            count += 1  # line 538
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 539
        index += count  # line 539
    return out  # line 540

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 542
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 543
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 544
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 546
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 546
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 547
        Exit("Source and target file patterns differ in semantics")  # line 547
    return (ot, nt)  # line 548

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 550
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 551
    pairs = []  # type: List[Tuple[str, str]]  # line 552
    for filename in filenames:  # line 553
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 554
        nextliteral = 0  # type: int  # line 555
        index = 0  # type: int  # line 555
        parsedOld = []  # type: List[GlobBlock2]  # line 556
        for part in oldPattern:  # match everything in the old filename  # line 557
            if part.isLiteral:  # line 558
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 558
                index += len(part.content)  # line 558
                nextliteral += 1  # line 558
            elif part.content.startswith("?"):  # line 559
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 559
                index += len(part.content)  # line 559
            elif part.content.startswith("["):  # line 560
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 560
                index += 1  # line 560
            elif part.content == "*":  # line 561
                if nextliteral >= len(literals):  # line 562
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 562
                    break  # line 562
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 563
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 564
                index = nxt  # line 564
            else:  # line 565
                Exit("Invalid file pattern specified for move/rename")  # line 565
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 566
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 567
        nextliteral = 0  # line 568
        nextglob = 0  # type: int  # line 568
        outname = []  # type: List[str]  # line 569
        for part in newPattern:  # generate new filename  # line 570
            if part.isLiteral:  # line 571
                outname.append(literals[nextliteral].content)  # line 571
                nextliteral += 1  # line 571
            else:  # line 572
                outname.append(globs[nextglob].matches)  # line 572
                nextglob += 1  # line 572
        pairs.append((filename, "".join(outname)))  # line 573
    return pairs  # line 574

@_coconut_tco  # line 576
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 576
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 580
    if not actions:  # line 581
        return []  # line 581
    sources = None  # type: List[str]  # line 582
    targets = None  # type: List[str]  # line 582
    sources, targets = [list(l) for l in zip(*actions)]  # line 583
    last = len(actions)  # type: int  # line 584
    while last > 1:  # line 585
        clean = True  # type: bool  # line 586
        for i in range(1, last):  # line 587
            try:  # line 588
                index = targets[:i].index(sources[i])  # type: int  # line 589
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 590
                targets.insert(index, targets.pop(i))  # line 591
                clean = False  # line 592
            except:  # target not found in sources: good!  # line 593
                continue  # target not found in sources: good!  # line 593
        if clean:  # line 594
            break  # line 594
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 595
    if exitOnConflict:  # line 596
        for i in range(1, len(actions)):  # line 596
            if sources[i] in targets[:i]:  # line 596
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 596
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 597

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 599
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 600
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 601
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 602

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str]]':  # line 604
    ''' Returns (root-normalized) set of --only and --except arguments. '''  # line 605
    root = os.getcwd()  # type: str  # line 606
    onlys = []  # type: List[str]  # line 607
    excps = []  # type: List[str]  # line 607
    remotes = []  # type: List[str]  # line 607
    for keys, container in [(("--only", "--include"), onlys), (("--except", "--exclude"), excps), (("--remote",), remotes)]:  # line 608
        founds = [i for i in range(len(options)) if any([options[i].startswith(key) for key in keys])]  # assuming no more than one = in the string  # line 609
        for i in reversed(founds):  # line 610
            if "=" in options[i]:  # line 611
                container.append(options[i].split("=")[1])  # line 612
            elif i + 1 < len(options):  # in case last --only has no argument  # line 613
                container.append(options[i + 1])  # line 614
                del options[i + 1]  # line 615
            del options[i]  # reverse removal  # line 616
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(PARENT + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(PARENT + SLASH))) if excps else None, remotes)  # line 617
