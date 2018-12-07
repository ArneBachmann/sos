#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xbaeb5495

# Compiled with Coconut version 1.4.0-post_dev2 [Ernest Scribbler]

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

import hashlib  # early time tracking  # line 4
import logging  # early time tracking  # line 4
import os  # early time tracking  # line 4
import shutil  # early time tracking  # line 4
sys = _coconut_sys  # early time tracking  # line 4
import time  # early time tracking  # line 4
START_TIME = time.time()  # early time tracking  # line 4

try:  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Any  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import AnyStr  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Dict  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import FrozenSet  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Generic  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import IO  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Iterable  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Iterator  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import NoReturn  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import List  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Optional  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Sequence  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Set  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Tuple  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Type  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import TypeVar  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Union  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
except:  # line 7
    pass  # line 7

try:  # line 9
    from sos import pure  # line 9
    from sos.values import *  # line 9
    from sos import usage  # line 9
except:  # line 10
    import pure  # line 10
    from values import *  # line 10
    import usage  # line 10


# Lazy imports for quicker initialization TODO make mypy accept this
bz2 = None  # type: Any  # line 14
codecs = None  # type: Any  # line 14
difflib = None  # type: Any  # line 14
class bz2:  # line 15
    @_coconut_tco  # line 15
    def __getattribute__(_, key):  # line 15
        global bz2  # line 16
        import bz2  # line 16
        return _coconut_tail_call(bz2.__getattribute__, key)  # line 16
bz2 = bz2()  # type: object  # line 17

class codecs:  # line 19
    @_coconut_tco  # line 19
    def __getattribute__(_, key):  # line 19
        global codecs  # line 20
        import codecs  # line 20
        return _coconut_tail_call(codecs.__getattribute__, key)  # line 20
codecs = codecs()  # type: object  # line 21

class difflib:  # line 23
    @_coconut_tco  # line 23
    def __getattribute__(_, key):  # line 23
        global difflib  # line 24
        import difflib  # line 24
        return _coconut_tail_call(difflib.__getattribute__, key)  # line 24
difflib = difflib()  # type: object  # line 25


verbose = [None] if '--verbose' in sys.argv or '-v' in sys.argv else []  # type: List[None]  # line 28
debug_ = [None] if os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv else []  # type: List[None]  # line 29


# Classes
class Accessor(dict):  # line 33
    ''' Dictionary with attribute access. '''  # line 34
    def __init__(_, mapping: 'Dict[str, Any]'={}) -> 'None':  # TODO remove -> None when fixed in Coconut stub  # line 35
        dict.__init__(_, mapping)  # TODO remove -> None when fixed in Coconut stub  # line 35
    @_coconut_tco  # or simply class C(dict): __getattr__ = dict.__getitem__  # line 36
    def __getattribute__(_, name: 'str') -> 'Any':  # or simply class C(dict): __getattr__ = dict.__getitem__  # line 36
        try:  # line 37
            return _[name]  # line 37
        except:  # line 38
            return _coconut_tail_call(dict.__getattribute__, _, name)  # line 38
    def __setattr__(_, name: 'str', value: 'Any') -> 'None':  # line 39
        _[name] = value  # line 39
    @_coconut_tco  # line 40
    def __bool__(_) -> 'bool':  # line 40
        return _coconut_tail_call(bool, int(_[None]))  # line 40
    @_coconut_tco  # line 41
    def __str__(_) -> 'str':  # line 41
        return _coconut_tail_call(str, _[None])  # line 41
    def __add__(_, b: 'Any') -> 'str':  # line 42
        return _.value + b  # line 42

useColor = [None]  # type: List[_coconut.typing.Optional[bool]]  # line 44
def enableColor(enable: 'bool'=True, force: 'bool'=False):  # line 45
    ''' This piece of code only became necessary to enable enabling/disabling of the colored terminal output after initialization.
      enable: target state
      force: for testing only
  '''  # line 49
    if not force and (useColor[0] if enable else not useColor[0]):  # nothing to do since already set  # line 50
        return  # nothing to do since already set  # line 50
    MARKER.value = MARKER_COLOR if enable and sys.platform != "win32" else usage.MARKER_TEXT  # HINT because it doesn't work with the loggers yet  # line 51
    try:  # line 52
        if useColor[0] is None:  # very initial, do some monkey-patching  # line 53
            colorama.init(wrap=False)  # line 54
            sys.stdout = colorama.AnsiToWin32(sys.stdout).stream  # TODO replace by "better-exceptions" code  # line 55
            sys.stderr = colorama.AnsiToWin32(sys.stderr).stream  # line 56
    except:  # line 57
        pass  # line 57
    useColor[0] = enable  # line 58

# fallbacks in case there is no colorama library present
Fore = Accessor({k: "" for k in ["RESET", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "YELLOW", "WHITE"]})  # type: Dict[str, str]  # line 61
Style = Accessor({k: "" for k in ["NORMAL", "BRIGHT", "RESET_ALL"]})  # type: Dict[str, str]  # line 62
Back = Fore  # type: Dict[str, str]  # line 63
MARKER = Accessor({"value": usage.MARKER_TEXT})  # type: str  # assume default text-only  # line 64
try:  # line 65
    import colorama  # line 66
    import colorama.ansitowin32  # line 66
    if sys.stderr.isatty:  # list of ansi codes: http://bluesock.org/~willkg/dev/ansi.html  # line 67
        from colorama import Back  # line 68
        from colorama import Fore  # line 68
        from colorama import Style  # line 68
        MARKER_COLOR = Fore.WHITE + usage.MARKER_TEXT + Fore.RESET  # type: str  # line 69
        if sys.platform == "win32":  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 70
            Style.BRIGHT = ""  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 70
        enableColor()  # line 71
except:  # if library not installed, use fallback even for colored texts  # line 72
    MARKER_COLOR = usage.MARKER_TEXT  # if library not installed, use fallback even for colored texts  # line 72

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 74
    Number = TypeVar("Number", int, float)  # line 75
    class Counter(Generic[Number]):  # line 76
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 77
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 78
            _.value = initial  # type: Number  # line 78
        def inc(_, by: 'Number'=1) -> 'Number':  # line 79
            _.value += by  # line 79
            return _.value  # line 79
else:  # line 80
    class Counter:  # line 81
        def __init__(_, initial=0) -> 'None':  # line 82
            _.value = initial  # line 82
        def inc(_, by=1):  # line 83
            _.value += by  # line 83
            return _.value  # line 83

class ProgressIndicator(Counter):  # line 85
    ''' Manages a rotating progress indicator. '''  # line 86
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 87
        super(ProgressIndicator, _).__init__(-1)  # line 87
        _.symbols = symbols  # line 87
        _.timer = time.time()  # type: float  # line 87
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 87
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 88
        ''' Returns a value only if a certain time has passed. '''  # line 89
        newtime = time.time()  # type: float  # line 90
        if newtime - _.timer < .1:  # line 91
            return None  # line 91
        _.timer = newtime  # line 92
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 93
        if _.callback:  # line 94
            _.callback(sign)  # line 94
        return sign  # line 95

class Logger:  # line 97
    ''' Logger that supports joining many items. '''  # line 98
    def __init__(_, log) -> 'None':  # line 99
        _._log = log  # line 99
    def debug(_, *s):  # line 100
        _._log.debug(pure.sjoin(*s))  # line 100
    def info(_, *s):  # line 101
        _._log.info(pure.sjoin(*s))  # line 101
    def warn(_, *s):  # line 102
        _._log.warning(pure.sjoin(*s))  # line 102
    def error(_, *s):  # line 103
        _._log.error(pure.sjoin(*s))  # line 103


# Constants
_log = Logger(logging.getLogger(__name__))  # line 107
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 107
ONLY_GLOBAL_FLAGS = ["strict", "track", "picky", "compress"]  # type: List[str]  # line 108
CONFIGURABLE_FLAGS = ["useChangesCommand", "useUnicodeFont", "useColorOutput"]  # type: List[str]  # line 109
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 110
CONFIGURABLE_INTS = ["logLines", "diffLines"]  # type: List[str]  # line 111
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # lists that don't allow folders with their file patterns  # line 112
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 113
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 114
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 115
BACKUP_SUFFIX = "_last"  # type: str  # line 116
metaFolder = ".sos"  # type: str  # line 117
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 118
metaFile = ".meta"  # type: str  # line 119
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 120
bufSize = pure.MEBI  # type: int  # line 121
UTF8 = "utf-8"  # type: str  # early used constant, not defined in standard library  # line 122
SVN = "svn"  # type: str  # line 123
SLASH = "/"  # type: str  # line 124
PARENT = ".."  # type: str  # line 125
DOT_SYMBOL = "\u00b7"  # type: str  # line 126
MULT_SYMBOL = "\u00d7"  # type: str  # line 127
CROSS_SYMBOL = "\u2716"  # type: str  # line 128
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 129
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 130
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in "this revision"  # line 131
MOVE_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 132
METADATA_FORMAT = 2  # type: int  # counter for (partially incompatible) consecutive formats (was undefined, "1" is the first numbered format version after that)  # line 133
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 134
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 135
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # 2-tuple(is_tracked? (otherwise picky), str-arguments to "commit") TODO CVS, RCS have probably different per-file operation  # line 136
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 137
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[_coconut.typing.Optional[bytes], str]  # line 138
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[_coconut.typing.Optional[str], int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 139
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "useColorOutput": True, "diffLines": 2, "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth", "*.ps1", "*.bat"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 140
RETRY_NUM = 3  # type: int  # line 154
RETRY_WAIT = 1.5  # type: int  # line 155


# Functions
def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 159
    color = useColor[0] and color or ""  # line 160
    reset = Fore.RESET if useColor[0] and color else ""  # line 161
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 162
    sys.stdout.flush()  # PEP528 compatibility  # line 162
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 164
    color = useColor[0] and color or ""  # line 165
    reset = Fore.RESET if useColor[0] and color else ""  # line 166
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 167
    sys.stderr.flush()  # line 167
@_coconut_tco  # line 168
def encode(s: 'str') -> 'bytes':  # line 168
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 169
@_coconut_tco  # for os->py access of reading filenames  # line 170
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 170
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 170
try:  # line 171
    import chardet  # https://github.com/chardet/chardet  # line 172
    def detectEncoding(binary: 'bytes') -> '_coconut.typing.Optional[str]':  # None if nothing useful detected (=binary)  # line 173
        return chardet.detect(binary)["encoding"]  # None if nothing useful detected (=binary)  # line 173
except:  # Guess the encoding  # line 174
    def detectEncoding(binary: 'bytes') -> '_coconut.typing.Optional[str]':  # Guess the encoding  # line 174
        ''' Fallback if chardet library missing. '''  # line 175
        try:  # line 176
            binary.decode(UTF8)  # line 176
            return UTF8  # line 176
        except UnicodeError:  # line 177
            pass  # line 177
        try:  # line 178
            binary.decode("UTF-8-SIG")  # line 178
            return UTF8  # line 178
        except UnicodeError:  # line 179
            pass  # line 179
        try:  # line 180
            binary.decode("utf_16")  # line 180
            return "utf_16"  # line 180
        except UnicodeError:  # line 181
            pass  # line 181
        try:  # HINT: can still contain whitespace which is hard to diff  # line 182
            binary.decode("ascii")  # HINT: can still contain whitespace which is hard to diff  # line 182
            return "ascii"  # HINT: can still contain whitespace which is hard to diff  # line 182
        except UnicodeError:  # line 183
            pass  # line 183
        try:  # line 184
            binary.decode("cp1252")  # line 184
            return "cp1252"  # line 184
        except UnicodeError:  # line 185
            pass  # line 185
        return None  # line 186

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
    ''' Cleanup of user-specified *global* file patterns, used in config. '''  # line 197
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

def Exit(message: 'str'="", code: 'int'=1, excp: 'Any'=None):  # line 236
    lines = (message + ("" if excp is None else ("\n" + exception(excp)))).replace("\r", "\n").split("\n")  # type: List[str]  # line 237
    printe("[", nl="")  # line 238
    printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN, nl="")  # line 239
    printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + lines[0] + ".") if lines[0] != "" else ""))  # line 240
    if len(lines) > 1:  # line 241
        printe("\n".join(lines[1:]))  # line 244
    sys.exit(code)  # line 245

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 247
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 248
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 249
        raise Exception("Cannot possibly strings pack into specified length")  # line 249
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 250
        prefix += separator + ((process)(strings.pop(0)))  # line 250
    return prefix  # line 251

def exception(E) -> 'str':  # line 253
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 254
    import traceback  # line 255
    return str(E) + "\n" + traceback.format_exc() + "\n" + traceback.format_list(traceback.extract_stack())  # line 256

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 258
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 259
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 260
    _hash = hashlib.sha256()  # line 261
    wsize = 0  # type: int  # line 262
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 263
        Exit("Hash collision detected. Leaving repository in inconsistent state", 1)  # HINT this exits immediately  # line 264
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 265
    retry = RETRY_NUM  # type: int  # line 266
    while True:  # line 267
        try:  # line 268
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
            break  # line 280
        except Exception as E:  # (IsADirectoryError, PermissionError)  # line 281
            retry -= 1  # line 282
            if retry == 0:  # line 283
                raise E  # line 283
            error("Cannot open %r - retrying %d more times in %.1d seconds" % (path, RETRY_WAIT))  # line 284
            time.sleep(RETRY_WAIT)  # line 285
    return (_hash.hexdigest(), wsize)  # line 286

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 288
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 289
    for k, v in map.items():  # line 290
        if k in params:  # line 290
            return v  # line 290
    return default  # line 291

@_coconut_tco  # line 293
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 293
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 293

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 295
    ''' Detects a (text) file's encoding, detects the end of line markers, loads the file and splits it into lines.
      returns: 3-tuple (encoding-string, end-of-line bytes, [lines])
  '''  # line 298
    lines = []  # type: List[str]  # line 299
    if filename is not None:  # line 300
        with open(encode(filename), "rb") as fd:  # line 300
            content = fd.read()  # line 300
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 301
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 302
    if filename is not None:  # line 303
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 303
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 303
    elif content is not None:  # line 304
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 304
    else:  # line 305
        return (sys.getdefaultencoding(), b"\n", [])  # line 305
    if ignoreWhitespace:  # line 306
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 306
    return (encoding, eol, lines)  # line 307

if TYPE_CHECKING:  # line 309
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 310
    @_coconut_tco  # line 311
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 311
        ''' A better makedata() version. '''  # line 312
        r = _old._asdict()  # type: Dict[str, Any]  # line 313
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 314
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 315
else:  # line 316
    @_coconut_tco  # line 317
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 317
        ''' A better makedata() version. '''  # line 318
        r = _old._asdict()  # line 319
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 320
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 321

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 323
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 324
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 325
    for path, info in changes.additions.items():  # line 326
        for dpath, dinfo in changes.deletions.items():  # line 326
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 327
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 328
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 329
                break  # deletions loop, continue with next addition  # line 330
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 331

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 333
    ''' Default can be a selection from choice and allows empty input. '''  # line 334
    while True:  # line 335
        selection = input(text).strip().lower()  # line 336
        if selection != "" and selection in choices:  # line 337
            break  # line 337
        if selection == "" and default is not None:  # line 338
            selection = default  # line 338
            break  # line 338
    return selection  # line 339

def user_block_input(output: 'List[str]'):  # line 341
    ''' Side-effect appending to input list. '''  # line 342
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 343
    line = sep  # type: str  # line 343
    while True:  # line 344
        line = input("> ")  # line 345
        if line == sep:  # line 346
            break  # line 346
        output.append(line)  # writes to caller-provided list reference  # line 347

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 349
    encoding = None  # type: str  # line 350
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 350
    othr = None  # type: _coconut.typing.Sequence[str]  # line 350
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 350
    curr = None  # type: _coconut.typing.Sequence[str]  # line 350
    try:  # line 351
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 352
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 353
    except Exception as E:  # in case of binary files  # line 354
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname)), exception=E)  # in case of binary files  # line 354
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 355
        printo(line)  # from generator expression  # line 355

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 357
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 372
    encoding = None  # type: str  # line 373
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 373
    othr = None  # type: _coconut.typing.Sequence[str]  # line 373
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 373
    curr = None  # type: _coconut.typing.Sequence[str]  # line 373
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 374
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 375
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 376
    except Exception as E:  # line 377
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname)), exception=E)  # line 377
    if None not in [othreol, curreol] and othreol != curreol:  # line 378
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 378
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 379
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 380
    tmp = []  # type: List[str]  # block lines  # line 381
    last = " "  # type: str  # "into"-file offset for remark lines  # line 382
    no = None  # type: int  # "into"-file offset for remark lines  # line 382
    line = None  # type: str  # "into"-file offset for remark lines  # line 382
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 382
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 383
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 384
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 384
            continue  # continue filling current block, no matter what type of block it is  # line 384
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 385
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 385
        if last == " ":  # block is same in both files  # line 386
            if len(tmp) > 0:  # avoid adding empty keep block  # line 387
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 387
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 388
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 389
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 390
                offset += len(blocks[-2].lines)  # line 391
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 392
                blocks.pop()  # line 393
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 394
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 395
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 396
                offset += len(blocks[-1].lines)  # line 397
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 398
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 399
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 400
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 400
        last = line[0]  # line 401
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 402
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 404
    debug("Diff blocks: " + repr(blocks))  # line 405
    if diffOnly:  # line 406
        return (blocks, nl)  # line 406

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 409
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 409
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 409
    selection = ""  # type: str  # clean list of strings  # line 409
    for block in blocks:  # line 410
        if block.tipe == MergeBlockType.KEEP:  # line 411
            output.extend(block.lines)  # line 411
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 412
            output.extend(block.lines)  # line 414
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 415
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 416
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 417
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 418
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 419
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 420
                while True:  # line 421
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 422
                    if op in "tb":  # line 423
                        output.extend(block.lines)  # line 423
                    if op in "ib":  # line 424
                        output.extend(block.replaces.lines)  # line 424
                    if op == "u":  # line 425
                        user_block_input(output)  # line 425
                    if op in "tbiu":  # line 426
                        break  # line 426
            else:  # more than one line and not ask  # line 427
                if mergeOperation == MergeOperation.REMOVE:  # line 428
                    pass  # line 428
                elif mergeOperation == MergeOperation.BOTH:  # line 429
                    output.extend(block.lines)  # line 429
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 430
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 430
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 431
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 432
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 434
                if selection in "ao":  # line 435
                    if block.tipe == MergeBlockType.INSERT:  # line 436
                        add_all = "y" if selection == "a" else "n"  # line 436
                        selection = add_all  # line 436
                    else:  # REMOVE case  # line 437
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 437
                        selection = del_all  # REMOVE case  # line 437
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 438
                output.extend(block.lines)  # line 440
    debug("Merge output: " + "; ".join(output))  # line 441
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 442
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 445
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 445
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 448
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 449
    blocks = []  # type: List[MergeBlock]  # line 450
    for i, line in enumerate(out):  # line 451
        if line[0] == "+":  # line 452
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 453
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 454
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 455
                else:  # first + in block  # line 456
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 457
            else:  # last line of + block  # line 458
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 459
                    blocks[-1].lines.append(line[2])  # line 460
                else:  # single line  # line 461
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 462
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 463
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 464
                    blocks.pop()  # line 464
        elif line[0] == "-":  # line 465
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 466
                blocks[-1].lines.append(line[2])  # line 467
            else:  # first in block  # line 468
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 469
        elif line[0] == " ":  # line 470
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 471
                blocks[-1].lines.append(line[2])  # line 472
            else:  # first in block  # line 473
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 474
        else:  # line 475
            raise Exception("Cannot parse diff line %r" % line)  # line 475
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 476
    if diffOnly:  # line 477
        return blocks  # line 477
    out[:] = []  # line 478
    for i, block in enumerate(blocks):  # line 479
        if block.tipe == MergeBlockType.KEEP:  # line 480
            out.extend(block.lines)  # line 480
        elif block.tipe == MergeBlockType.REPLACE:  # line 481
            if mergeOperation == MergeOperation.ASK:  # line 482
                printo(pure.ajoin("- ", othr))  # line 483
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 484
                printo("+ " + (" " * i) + block.lines[0])  # line 485
                printo(pure.ajoin("+ ", into))  # line 486
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 487
                if op in "tb":  # line 488
                    out.extend(block.lines)  # line 488
                    break  # line 488
                if op in "ib":  # line 489
                    out.extend(block.replaces.lines)  # line 489
                    break  # line 489
                if op == "m":  # line 490
                    user_block_input(out)  # line 490
                    break  # line 490
            else:  # non-interactive  # line 491
                if mergeOperation == MergeOperation.REMOVE:  # line 492
                    pass  # line 492
                elif mergeOperation == MergeOperation.BOTH:  # line 493
                    out.extend(block.lines)  # line 493
                elif mergeOperation == MergeOperation.INSERT:  # line 494
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 494
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 495
            out.extend(block.lines)  # line 495
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 496
            out.extend(block.lines)  # line 496
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 498

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 500
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 503
    debug("Detecting root folders...")  # line 504
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 505
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 506
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 507
        contents = set(os.listdir(path))  # type: Set[str]  # line 508
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 509
        choice = None  # type: _coconut.typing.Optional[str]  # line 510
        if len(vcss) > 1:  # line 511
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 512
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 513
        elif len(vcss) > 0:  # line 514
            choice = vcss[0]  # line 514
        if not vcs[0] and choice:  # memorize current repo root  # line 515
            vcs = (path, choice)  # memorize current repo root  # line 515
        new = os.path.dirname(path)  # get parent path  # line 516
        if new == path:  # avoid infinite loop  # line 517
            break  # avoid infinite loop  # line 517
        path = new  # line 518
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 519
        if vcs[0]:  # already detected vcs base and command  # line 520
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 520
        sos = path  # line 521
        while True:  # continue search for VCS base  # line 522
            contents = set(os.listdir(path))  # line 523
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 524
            choice = None  # line 525
            if len(vcss) > 1:  # line 526
                choice = SVN if SVN in vcss else vcss[0]  # line 527
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 528
            elif len(vcss) > 0:  # line 529
                choice = vcss[0]  # line 529
            if choice:  # line 530
                return (sos, path, choice)  # line 530
            new = os.path.dirname(path)  # get parent path  # line 531
            if new == path:  # no VCS folder found  # line 532
                return (sos, None, None)  # no VCS folder found  # line 532
            path = new  # line 533
    return (None, vcs[0], vcs[1])  # line 534

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 536
    index = 0  # type: int  # line 537
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 538
    while index < len(pattern):  # line 539
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 540
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 540
            continue  # line 540
        if pattern[index] in "*?":  # line 541
            count = 1  # type: int  # line 542
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 543
                count += 1  # line 543
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 544
            index += count  # line 544
            continue  # line 544
        if pattern[index:index + 2] == "[!":  # line 545
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 545
            index += len(out[-1][1])  # line 545
            continue  # line 545
        count = 1  # line 546
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 547
            count += 1  # line 547
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 548
        index += count  # line 548
    return out  # line 549

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 551
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 552
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 553
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 555
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 555
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 556
        Exit("Source and target file patterns differ in semantics")  # line 556
    return (ot, nt)  # line 557

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 559
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 560
    pairs = []  # type: List[Tuple[str, str]]  # line 561
    for filename in filenames:  # line 562
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 563
        nextliteral = 0  # type: int  # line 564
        index = 0  # type: int  # line 564
        parsedOld = []  # type: List[GlobBlock2]  # line 565
        for part in oldPattern:  # match everything in the old filename  # line 566
            if part.isLiteral:  # line 567
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 567
                index += len(part.content)  # line 567
                nextliteral += 1  # line 567
            elif part.content.startswith("?"):  # line 568
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 568
                index += len(part.content)  # line 568
            elif part.content.startswith("["):  # line 569
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 569
                index += 1  # line 569
            elif part.content == "*":  # line 570
                if nextliteral >= len(literals):  # line 571
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 571
                    break  # line 571
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 572
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 573
                index = nxt  # line 573
            else:  # line 574
                Exit("Invalid file pattern specified for move/rename")  # line 574
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 575
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 576
        nextliteral = 0  # line 577
        nextglob = 0  # type: int  # line 577
        outname = []  # type: List[str]  # line 578
        for part in newPattern:  # generate new filename  # line 579
            if part.isLiteral:  # line 580
                outname.append(literals[nextliteral].content)  # line 580
                nextliteral += 1  # line 580
            else:  # line 581
                outname.append(globs[nextglob].matches)  # line 581
                nextglob += 1  # line 581
        pairs.append((filename, "".join(outname)))  # line 582
    return pairs  # line 583

@_coconut_tco  # line 585
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 585
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 589
    if not actions:  # line 590
        return []  # line 590
    sources = None  # type: List[str]  # line 591
    targets = None  # type: List[str]  # line 591
    sources, targets = [list(l) for l in zip(*actions)]  # line 592
    last = len(actions)  # type: int  # line 593
    while last > 1:  # line 594
        clean = True  # type: bool  # line 595
        for i in range(1, last):  # line 596
            try:  # line 597
                index = targets[:i].index(sources[i])  # type: int  # line 598
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 599
                targets.insert(index, targets.pop(i))  # line 600
                clean = False  # line 601
            except:  # target not found in sources: good!  # line 602
                continue  # target not found in sources: good!  # line 602
        if clean:  # line 603
            break  # line 603
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 604
    if exitOnConflict:  # line 605
        for i in range(1, len(actions)):  # line 605
            if sources[i] in targets[:i]:  # line 605
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 605
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 606

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 608
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 609
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 610
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 611

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str]]':  # line 613
    ''' Returns (root-normalized) set of --only and --except arguments. '''  # line 614
    root = os.getcwd()  # type: str  # line 615
    onlys = []  # type: List[str]  # line 616
    excps = []  # type: List[str]  # line 616
    remotes = []  # type: List[str]  # line 616
    for keys, container in [(("--only", "--include"), onlys), (("--except", "--exclude"), excps), (("--remote",), remotes)]:  # line 617
        founds = [i for i in range(len(options)) if any([options[i].startswith(key) for key in keys])]  # assuming no more than one = in the string  # line 618
        for i in reversed(founds):  # line 619
            if "=" in options[i]:  # line 620
                container.append(options[i].split("=")[1])  # line 621
            elif i + 1 < len(options):  # in case last --only has no argument  # line 622
                container.append(options[i + 1])  # line 623
                del options[i + 1]  # line 624
            del options[i]  # reverse removal  # line 625
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(PARENT + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(PARENT + SLASH))) if excps else None, remotes)  # line 626
