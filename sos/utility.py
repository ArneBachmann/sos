#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x97594c27

# Compiled with Coconut version 1.4.3 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get("__coconut__")
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules["__coconut__"]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import *
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_back_pipe, _coconut_star_pipe, _coconut_back_star_pipe, _coconut_dubstar_pipe, _coconut_back_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert, _coconut_mark_as_match
_coconut_sys.path.pop(0)

# Compiled Coconut: -----------------------------------------------------------

# Copyright Arne Bachmann
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import hashlib  # early time tracking  # line 4
import itertools  # early time tracking  # line 4
import logging  # early time tracking  # line 4
import os  # early time tracking  # line 4
import shutil  # early time tracking  # line 4
sys = _coconut_sys  # early time tracking  # line 4
import time  # early time tracking  # line 4
START_TIME = time.time()  # early time tracking  # line 4

if TYPE_CHECKING:  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
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

from sos import pure  # line 8
from sos.values import *  # line 9
from sos import usage  # line 10


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
    def __init__(_, mapping: 'Dict[str, Any]'={}) -> 'None':  # line 35
        dict.__init__(_, mapping)  # line 35
    __getattr__ = dict.__getitem__  # line 36
    def __setattr__(_, name: 'str', value: 'Any') -> 'None':  # line 37
        _[name] = value  # line 37
    @_coconut_tco  # line 38
    def __bool__(_) -> 'bool':  # line 38
        return _coconut_tail_call(bool, int(_[None]))  # line 38
    @_coconut_tco  # line 39
    def __str__(_) -> 'str':  # line 39
        return _coconut_tail_call(str, _[None])  # line 39
    def __add__(_, b: 'Any') -> 'str':  # line 40
        return _.value + b  # line 40

useColor = [None]  # type: List[_coconut.typing.Optional[bool]]  # line 42
def enableColor(enable: 'bool'=True, force: 'bool'=False):  # line 43
    ''' This piece of code only became necessary to enable enabling/disabling of the colored terminal output after initialization.
      enable: target state
      force: for testing only
  '''  # line 47
    if not force and (useColor[0] if enable else not useColor[0]):  # nothing to do since already set  # line 48
        return  # nothing to do since already set  # line 48
    MARKER.value = MARKER_COLOR if enable and sys.platform != "win32" else usage.MARKER_TEXT  # HINT because it doesn't work with the loggers yet  # line 49
    try:  # line 50
        if useColor[0] is None:  # very initial, do some monkey-patching  # line 51
            colorama.init(wrap=False)  # line 52
            sys.stdout = colorama.AnsiToWin32(sys.stdout).stream  # TODO replace by "better-exceptions" code  # line 53
            sys.stderr = colorama.AnsiToWin32(sys.stderr).stream  # line 54
    except:  # line 55
        pass  # line 55
    useColor[0] = enable  # line 56

# fallbacks in case there is no colorama library present
Fore = Accessor({k: "" for k in ["RESET", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "YELLOW", "WHITE"]})  # type: Dict[str, str]  # line 59
Style = Accessor({k: "" for k in ["NORMAL", "BRIGHT", "RESET_ALL"]})  # type: Dict[str, str]  # line 60
Back = Fore  # type: Dict[str, str]  # line 61
MARKER = Accessor({"value": usage.MARKER_TEXT})  # type: str  # assume default text-only  # line 62
try:  # line 63
    import colorama  # line 64
    import colorama.ansitowin32  # line 64
    if sys.stderr.isatty:  # list of ansi codes: http://bluesock.org/~willkg/dev/ansi.html  # line 65
        from colorama import Back  # line 66
        from colorama import Fore  # line 66
        from colorama import Style  # line 66
        MARKER_COLOR = Fore.WHITE + usage.MARKER_TEXT + Fore.RESET  # type: str  # line 67
        if sys.platform == "win32":  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 68
            Style.BRIGHT = ""  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 68
        enableColor()  # line 69
except:  # if library not installed, use fallback even for colored texts  # line 70
    MARKER_COLOR = usage.MARKER_TEXT  # if library not installed, use fallback even for colored texts  # line 70

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 72
    Number = TypeVar("Number", int, float)  # line 73
    class Counter(Generic[Number]):  # line 74
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 75
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 76
            _.value = initial  # type: Number  # line 76
        def inc(_, by: 'Number'=1) -> 'Number':  # line 77
            _.value += by  # line 77
            return _.value  # line 77
else:  # line 78
    class Counter:  # line 79
        def __init__(_, initial=0) -> 'None':  # line 80
            _.value = initial  # line 80
        def inc(_, by=1):  # line 81
            _.value += by  # line 81
            return _.value  # line 81

class ProgressIndicator(Counter):  # line 83
    ''' Manages a rotating progress indicator. '''  # line 84
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 85
        super(ProgressIndicator, _).__init__(-1)  # line 85
        _.symbols = symbols  # line 85
        _.timer = time.time()  # type: float  # line 85
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 85
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 86
        ''' Returns a value only if a certain time has passed. '''  # line 87
        newtime = time.time()  # type: float  # line 88
        if newtime - _.timer < .1:  # line 89
            return None  # line 89
        _.timer = newtime  # line 90
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 91
        if _.callback:  # line 92
            _.callback(sign)  # line 92
        return sign  # line 93

class Logger:  # line 95
    ''' Logger that supports joining many items. '''  # line 96
    def __init__(_, log) -> 'None':  # line 97
        _._log = log  # line 97
    def debug(_, *s):  # line 98
        _._log.debug(pure.sjoin(*s))  # line 98
    def info(_, *s):  # line 99
        _._log.info(pure.sjoin(*s))  # line 99
    def warn(_, *s):  # line 100
        _._log.warning(pure.sjoin(*s))  # line 100
    def error(_, *s):  # line 101
        _._log.error(pure.sjoin(*s))  # line 101


# Constants
_log = Logger(logging.getLogger(__name__))  # line 105
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 105
ONLY_GLOBAL_FLAGS = ["strict", "track", "picky", "compress"]  # type: List[str]  # line 106
CONFIGURABLE_FLAGS = ["useChangesCommand", "useUnicodeFont", "useColorOutput"]  # type: List[str]  # line 107
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 108
CONFIGURABLE_INTS = ["logLines", "diffLines"]  # type: List[str]  # line 109
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # lists that don't allow folders with their file patterns  # line 110
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 111
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 112
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 113
BACKUP_SUFFIX = "_last"  # type: str  # line 114
metaFolder = ".sos"  # type: str  # line 115
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 116
metaFile = ".meta"  # type: str  # line 117
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 118
bufSize = pure.MEBI  # type: int  # line 119
UTF8 = "utf-8"  # type: str  # early used constant, not defined in standard library  # line 120
SVN = "svn"  # type: str  # line 121
SLASH = "/"  # type: str  # line 122
PARENT = ".."  # type: str  # line 123
DOT_SYMBOL = "\u00b7"  # type: str  # line 124
MULT_SYMBOL = "\u00d7"  # type: str  # line 125
CROSS_SYMBOL = "\u2716"  # type: str  # line 126
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 127
CHANGED_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 128
MOVED_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 129
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in pointing to "this revision"  # line 130
METADATA_FORMAT = 2  # type: int  # counter for (partially incompatible) consecutive formats (was undefined, "1" is the first numbered format version after that)  # line 131
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 132
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 133
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # 2-tuple(is_tracked? (otherwise picky), str-arguments to "commit") TODO CVS, RCS have probably different per-file operation  # line 134
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 135
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[_coconut.typing.Optional[bytes], str]  # line 136
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[_coconut.typing.Optional[str], int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 137
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "useColorOutput": True, "diffLines": 2, "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth", "*.ps1", "*.bat"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 138
RETRY_NUM = 3  # type: int  # line 152
RETRY_WAIT = 1.5  # type: int  # line 153
CODEC_FUNCTIONS = ['utf_32_be', 'utf_32_le', 'utf_32', 'utf_16_be', 'utf_16_le', 'utf_16', 'utf_7', 'utf_8_sig', 'utf_8']  # type: List[str]  # line 154


# Functions
def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 158
    color = useColor[0] and color or ""  # line 159
    reset = Fore.RESET if useColor[0] and color else ""  # line 160
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 161
    sys.stdout.flush()  # PEP528 compatibility  # line 161

def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 164
    color = useColor[0] and color or ""  # line 165
    reset = Fore.RESET if useColor[0] and color else ""  # line 166
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 167
    sys.stderr.flush()  # line 167

@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 170
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 170
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 170

@_coconut_tco  # for os->py access of reading filenames  # line 172
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 172
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 172

def guessEncoding(binary: 'bytes') -> 'List[str]':  # line 174
    ''' If encoding cannot be determined automatically, attempt a guess. Usually it's not unambiguous, though.
  >>> print(guessEncoding(b"abcd0234"))
  ['ascii']
  >>> print(guessEncoding(bytes([0b00100100, 0b11000010, 0b10100010, 0b11100010, 0b10000010, 0b10101100, 0b11110000, 0b10011010, 0b10110011, 0b10011001])))  # utf_8  1:$ 2:cent 3:€, 4:? -> gives 5 options, but it's UTF-8
  ['utf_16_be', 'utf_16_le', 'utf_8']
  >>> print(guessEncoding(bytes([0b00000000, 0b00100100, 0b11011000, 0b01010010, 0b11011111, 0b01100010])))  # utf_16 $ ? -> gives 3 options, on is correct
  ['utf_16_be', 'utf_16_le']
  >>> print(guessEncoding(bytes([0b00100100, 0b11000010, 0b10100010])))  # utf_8  1:$ 2:cent 3:€, 4:? -> gives 2 UTF-8 options
  ['utf_8']
  '''  # line 184
    if all((bite < 128 for bite in binary)):  # TODO move as first detection step  # line 185
        return ["ascii"]  # TODO move as first detection step  # line 185
    decoded = list(filter(lambda _=None: tryOrDefault(lambda: codecs.encode(codecs.decode(binary, _), _) == binary, None), CODEC_FUNCTIONS))  # type: List[str]  # line 186
    if (len(binary) >> 1) << 1 != len(binary):  # only utf-8 variants possible here  # line 187
        decoded[:] = list(filter(lambda _=None: "8" in _, decoded))  # only utf-8 variants possible here  # line 187
    return decoded  # line 188

# Optional dependency: https://github.com/chardet/chardet
try:  # line 191
    import chardet  # line 192
    def detectEncoding(binary: 'bytes') -> '_coconut.typing.Optional[str]':  # returns None if nothing useful detected  # line 193
        return chardet.detect(binary)["encoding"]  # returns None if nothing useful detected  # line 193
except:  # line 194
    def detectEncoding(binary: 'bytes') -> '_coconut.typing.Optional[str]':  # line 195
        ''' Fallback function definition if no chardet library installed. '''  # line 196
        encodings = guessEncoding(binary)  # type: List[str]  # line 197
        if len(encodings) == 1:  # line 198
            return encodings[0]  # line 198
        if len(encodings) == 0:  # or cp1252 or cp850  # line 199
            return None  # or cp1252 or cp850  # line 199
        return encodings[-1]  # line 200

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 202
    try:  # line 203
        return func()  # line 203
    except:  # line 204
        return default  # line 204

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 206
    try:  # line 207
        return func()  # line 207
    except Exception as E:  # line 208
        onError(E)  # line 208

def removePath(key: 'str', value: 'str') -> 'str':  # line 210
    ''' Cleanup of user-specified *global* file patterns, used in config. '''  # line 211
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 212

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 214
    ''' Updates a dictionary by another one, returning a new copy without touching any of the passed dictionaries. '''  # line 215
    d = dict(dikt)  # type: Dict[Any, Any]  # line 216
    d.update(by)  # line 216
    return d  # line 216

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # line 218
    ''' Abstraction for opening both compressed and plain files. '''  # line 219
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # line 220

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 222
    ''' Determine EOL style from a binary string. '''  # line 223
    lf = file.count(b"\n")  # type: int  # line 224
    cr = file.count(b"\r")  # type: int  # line 225
    crlf = file.count(b"\r\n")  # type: int  # line 226
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 227
        if lf != crlf or cr != crlf:  # line 228
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 228
        return b"\r\n"  # line 229
    if lf != 0 and cr != 0:  # line 230
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 230
    if lf > cr:  # Linux/Unix  # line 231
        return b"\n"  # Linux/Unix  # line 231
    if cr > lf:  # older 8-bit machines  # line 232
        return b"\r"  # older 8-bit machines  # line 232
    return None  # no new line contained, cannot determine  # line 233

if TYPE_CHECKING:  # line 235
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 236
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 236
else:  # line 237
    def safeSplit(s, d=None):  # line 238
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 238

@_coconut_tco  # line 240
def hashStr(datas: 'str') -> 'str':  # line 240
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 240

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 242
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 242

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 244
    return lizt[index:].index(what) + index  # line 244

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 246
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 246

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 248
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 248

def Exit(message: 'str'="", code: 'int'=1, excp: 'Any'=None):  # line 250
    if not '--quiet' in sys.argv:  # line 251
        lines = (message + ("" if excp is None else ("\n" + exception(excp)))).replace("\r", "\n").split("\n")  # type: List[str]  # line 252
        printe("[", nl="")  # line 253
        printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN, nl="")  # line 254
        printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + lines[0] + ".") if lines[0] != "" else ""))  # line 255
        if len(lines) > 1:  # line 256
            printe("\n".join(lines[1:]))  # line 259
    if '--wait' in sys.argv:  # line 260
        input("Hit Enter to finish." if not '--quiet' in sys.argv else "")  # line 260
    sys.exit(code)  # line 261

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 263
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 264
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 265
        raise Exception("Cannot possibly strings pack into specified length")  # line 265
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 266
        prefix += separator + ((process)(strings.pop(0)))  # line 266
    return prefix  # line 267

def exception(E) -> 'str':  # line 269
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 270
    import traceback  # line 271
    return str(E) + "\n" + traceback.format_exc() + "\n" + "".join(traceback.format_list(traceback.extract_stack()))  # line 272

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 274
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 275
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 276
    _hash = hashlib.sha256()  # line 277
    wsize = 0  # type: int  # line 278
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 279
        Exit("Hash collision detected. Leaving repository in inconsistent state", 1)  # HINT this exits immediately  # line 280
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 281
    retry = RETRY_NUM  # type: int  # line 282
    while True:  # line 283
        try:  # line 284
            with open(encode(path), "rb") as fd:  # line 285
                while True:  # line 286
                    buffer = fd.read(bufSize)  # type: bytes  # line 287
                    _hash.update(buffer)  # line 288
                    if to:  # line 289
                        to.write(buffer)  # line 289
                    if len(buffer) < bufSize:  # line 290
                        break  # line 290
                    if indicator:  # line 291
                        indicator.getIndicator()  # line 291
                if to:  # line 292
                    to.close()  # line 293
                    wsize = os.stat(encode(saveTo[0])).st_size  # line 294
                    for remote in saveTo[1:]:  # line 295
                        tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 295
            break  # line 296
        except Exception as E:  # (IsADirectoryError, PermissionError)  # line 297
            retry -= 1  # line 298
            if retry == 0:  # line 299
                raise E  # line 299
            error("Cannot open %r - retrying %d more times in %.1d seconds" % (path, retry, RETRY_WAIT))  # line 300
            time.sleep(RETRY_WAIT)  # line 301
    return (_hash.hexdigest(), wsize)  # line 302

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 304
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 305
    for k, v in map.items():  # line 306
        if k in params:  # line 306
            return v  # line 306
    return default  # line 307

@_coconut_tco  # line 309
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 309
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 309

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 311
    ''' Detects a (text) file's encoding, detects the end of line markers, loads the file and splits it into lines.
      returns: 3-tuple (encoding-string, end-of-line bytes, [lines])
  '''  # line 314
    lines = []  # type: List[str]  # line 315
    if filename is not None:  # line 316
        with open(encode(filename), "rb") as fd:  # line 316
            content = fd.read()  # line 316
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 317
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 318
    if filename is not None:  # line 319
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 319
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 319
    elif content is not None:  # line 320
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 320
    else:  # line 321
        return (sys.getdefaultencoding(), b"\n", [])  # line 321
    if ignoreWhitespace:  # line 322
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 322
    return (encoding, eol, lines)  # line 323

if TYPE_CHECKING:  # line 325
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 326
    @_coconut_tco  # line 327
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 327
        ''' A better makedata() version. '''  # line 328
        r = _old._asdict()  # type: Dict[str, Any]  # line 329
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 330
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 331
else:  # line 332
    @_coconut_tco  # line 333
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 333
        ''' A better makedata() version. '''  # line 334
        r = _old._asdict()  # line 335
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 336
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 337

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 339
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 340
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 341
    for path, info in changes.additions.items():  # line 342
        for dpath, dinfo in changes.deletions.items():  # line 342
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 343
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 344
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 345
                break  # deletions loop, continue with next addition  # line 346
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 347

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 349
    ''' Default can be a selection from choice and allows empty input. '''  # line 350
    while True:  # line 351
        selection = input(text).strip().lower()  # line 352
        if selection != "" and selection in choices:  # line 353
            break  # line 353
        if selection == "" and default is not None:  # line 354
            selection = default  # line 354
            break  # line 354
    return selection  # line 355

def user_block_input(output: 'List[str]'):  # line 357
    ''' Side-effect appending to input list. '''  # line 358
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 359
    line = sep  # type: str  # line 359
    while True:  # line 360
        line = input("> ")  # line 361
        if line == sep:  # line 362
            break  # line 362
        output.append(line)  # writes to caller-provided list reference  # line 363

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 365
    encoding = None  # type: str  # typing  # line 366
    othreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 366
    othr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 366
    curreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 366
    curr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 366
    try:  # line 367
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 368
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 369
    except Exception as E:  # in case of binary files  # line 370
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname)), excp=E)  # in case of binary files  # line 370
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 371
        printo(line)  # from generator expression  # line 371

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 373
    ''' Merges other binary text contents in 'file' (or reads from file 'filename') into current text contents 'into' (or reads from file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, don't perform the actual text merging
      eol: if True, will use the other file's EOL marks instead of current file's
      in case of a replace block and INSERT strategy, the change will be added **behind** the original. HINT this could be made configurable
  '''  # line 388
    encoding = None  # type: str  # typing  # line 389
    othreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 389
    othr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 389
    curreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 389
    curr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 389
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 390
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 391
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 392
    except Exception as E:  # line 393
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname)), excp=E)  # line 393
    if None not in (othreol, curreol) and othreol != curreol:  # line 394
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 394
    output = difflib.Differ().compare(othr, curr)  # type: Union[Iterable[str], List[str]]  # line 395
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 396
    tmp = []  # type: List[str]  # block of consecutive lines  # line 397
    last = " "  # type: str  # "into"-file offset for remark lines  # line 398
    no = None  # type: int  # "into"-file offset for remark lines  # line 398
    line = None  # type: str  # "into"-file offset for remark lines  # line 398
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 398

    for no, line in pure.appendEndmarkerIterator(enumerate(output), endValue="X"):  # EOF marker (difflib's output will never be "X" alone)  # line 400
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 401
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 401
            continue  # continue filling current block, no matter what type of block it is  # line 401
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 402
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 402
        if last == " " and len(tmp) > 0:  # same in both files. avoid adding empty keep block  # line 403
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # same in both files. avoid adding empty keep block  # line 403
        elif last == "-":  # may be a pure deletion or part of a replacement (with previous or next block being "+")  # line 404
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 405
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # is a +/- replacement  # line 406
                offset += len(blocks[-2].lines)  # line 407
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to insert merge block TODO why -1 necessary?  # line 408
                blocks.pop()  # line 409
        elif last == "+":  # may be a pure insertion or part of a replacement (with previous or next block being "-")  # line 410
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # line 411
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 412
                offset += len(blocks[-1].lines)  # line 413
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 414
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 415
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 416
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 416
        last = line[0]  # remember for comparison once next block comes around  # line 417
        tmp[:] = [line[2:]]  # only remember current line as fresh next block  # line 418
# TODO add code to detect and mark moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 420
    debug("Diff blocks: " + repr(blocks))  # line 421
    if diffOnly:  # line 422
        return (blocks, nl)  # line 422

# now perform merge operations depending on detected blocks and selected merge options
    output = []  # clean list of strings  # line 425
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 425
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 425
    selection = ""  # type: str  # clean list of strings  # line 425
    for block in blocks:  # line 426
        if block.tipe == MergeBlockType.KEEP:  # line 427
            output.extend(block.lines)  # line 427
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 428
            output.extend(block.lines)  # line 430
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 431
            if len(block.lines) == len(block.replaces.lines) == 1:  # both sides are one-liners: apply next sub-level merge  # line 432
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 433
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 434
#      if mergeOperation == MergeOperation.ASK:  # more than one line: needs user input
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 436
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 437
                while True:  # line 438
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 439
                    if op in "tb":  # order for both determined here - TODO make configurable  # line 440
                        output.extend(block.lines)  # order for both determined here - TODO make configurable  # line 440
                    if op in "ib":  # line 441
                        output.extend(block.replaces.lines)  # line 441
                    if op == "u":  # line 442
                        user_block_input(output)  # line 442
                    if op in "tbiu":  # was valid user input  # line 443
                        break  # was valid user input  # line 443
            else:  # more than one line and not ask  # line 444
                if mergeOperation == MergeOperation.REMOVE:  # line 445
                    pass  # line 445
                elif mergeOperation == MergeOperation.BOTH:  # line 446
                    output.extend(block.lines)  # line 446
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 447
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 447
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 448
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 449
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 451
                if selection in "ao":  # line 452
                    if block.tipe == MergeBlockType.INSERT:  # line 453
                        add_all = "y" if selection == "a" else "n"  # line 453
                        selection = add_all  # line 453
                    else:  # REMOVE case  # line 454
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 454
                        selection = del_all  # REMOVE case  # line 454
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 455
                output.extend(block.lines)  # line 457
    debug("Merge output: " + "\n".join(output))  # line 458
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 459
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 462
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 462
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
      returns: merged line
      raises: Exception in case of unparseable marker
  '''  # line 467
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 468
    blocks = []  # type: List[MergeBlock]  # line 469
    for i, charline in enumerate(out):  # line 470
        if charline[0] == "+":  # line 471
            if i + 1 < len(out) and out[i + 1][0] == "+":  # look-ahead: block will continue  # line 472
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 473
                    blocks[-1].lines.append(charline[2])  # add one more character to the accumulating list  # line 474
                else:  # first + in block  # line 475
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [charline[2]], i))  # line 476
            else:  # last charline of + block  # line 477
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 478
                    blocks[-1].lines.append(charline[2])  # line 479
                else:  # single charline  # line 480
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [charline[2]], i))  # line 481
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 482
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 483
                    blocks.pop()  # line 483
        elif charline[0] == "-":  # line 484
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 485
                blocks[-1].lines.append(charline[2])  # line 486
            else:  # first in block  # line 487
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [charline[2]], i))  # line 488
        elif charline[0] == " ":  # keep area  # line 489
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 490
                blocks[-1].lines.append(charline[2])  # line 491
            else:  # first in block  # line 492
                blocks.append(MergeBlock(MergeBlockType.KEEP, [charline[2]], i))  # line 493
        else:  # line 494
            raise Exception("Cannot parse diff charline %r" % charline)  # line 494
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # update blocks  # line 495
    if diffOnly:  # debug interrupt - only return blocks  # line 496
        return blocks  # debug interrupt - only return blocks  # line 496

    out = []  # line 498
    for i, block in enumerate(blocks):  # line 499
        if block.tipe == MergeBlockType.KEEP:  # line 500
            out.extend(block.lines)  # line 500
        elif block.tipe == MergeBlockType.REPLACE:  # line 501
            if mergeOperation == MergeOperation.ASK:  # TODO add loop here like in merge  # line 502
                printo(pure.ajoin("- ", othr))  # line 503
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 504
                printo("+ " + (" " * i) + block.lines[0])  # line 505
                printo(pure.ajoin("+ ", into))  # line 506
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 507
                if op in "tb":  # line 508
                    out.extend(block.lines)  # line 508
                    break  # line 508
                if op in "ib":  # line 509
                    out.extend(block.replaces.lines)  # line 509
                    break  # line 509
                if op == "m":  # line 510
                    user_block_input(out)  # line 510
                    break  # line 510
            else:  # non-interactive  # line 511
                if mergeOperation == MergeOperation.REMOVE:  # neither keep old nor insert new  # line 512
                    pass  # neither keep old nor insert new  # line 512
                elif mergeOperation == MergeOperation.BOTH:  # remove old and insert new  # line 513
                    out.extend(block.lines)  # remove old and insert new  # line 513
                elif mergeOperation == MergeOperation.INSERT:  # keep old an insert new  # line 514
                    out.extend(block.replaces.lines + block.lines)  # keep old an insert new  # line 514
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 515
            out.extend(block.lines)  # line 515
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 516
            out.extend(block.lines)  # line 516
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 518

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 520
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 523
    debug("Detecting root folders...")  # line 524
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 525
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 526
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 527
        contents = set(os.listdir(path))  # type: Set[str]  # line 528
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 529
        choice = None  # type: _coconut.typing.Optional[str]  # line 530
        if len(vcss) > 1:  # line 531
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 532
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 533
        elif len(vcss) > 0:  # line 534
            choice = vcss[0]  # line 534
        if not vcs[0] and choice:  # memorize current repo root  # line 535
            vcs = (path, choice)  # memorize current repo root  # line 535
        new = os.path.dirname(path)  # get parent path  # line 536
        if new == path:  # avoid infinite loop  # line 537
            break  # avoid infinite loop  # line 537
        path = new  # line 538
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 539
        if vcs[0]:  # already detected vcs base and command  # line 540
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 540
        sos = path  # line 541
        while True:  # continue search for VCS base  # line 542
            contents = set(os.listdir(path))  # line 543
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 544
            choice = None  # line 545
            if len(vcss) > 1:  # line 546
                choice = SVN if SVN in vcss else vcss[0]  # line 547
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 548
            elif len(vcss) > 0:  # line 549
                choice = vcss[0]  # line 549
            if choice:  # line 550
                return (sos, path, choice)  # line 550
            new = os.path.dirname(path)  # get parent path  # line 551
            if new == path:  # no VCS folder found  # line 552
                return (sos, None, None)  # no VCS folder found  # line 552
            path = new  # line 553
    return (None, vcs[0], vcs[1])  # line 554

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 556
    index = 0  # type: int  # line 557
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 558
    while index < len(pattern):  # line 559
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 560
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 560
            continue  # line 560
        if pattern[index] in "*?":  # line 561
            count = 1  # type: int  # line 562
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 563
                count += 1  # line 563
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 564
            index += count  # line 564
            continue  # line 564
        if pattern[index:index + 2] == "[!":  # line 565
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 565
            index += len(out[-1][1])  # line 565
            continue  # line 565
        count = 1  # line 566
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 567
            count += 1  # line 567
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 568
        index += count  # line 568
    return out  # line 569

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 571
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 572
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 573
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 575
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 575
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 576
        Exit("Source and target file patterns differ in semantics")  # line 576
    return (ot, nt)  # line 577

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 579
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 580
    pairs = []  # type: List[Tuple[str, str]]  # line 581
    for filename in filenames:  # line 582
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 583
        nextliteral = 0  # type: int  # line 584
        index = 0  # type: int  # line 584
        parsedOld = []  # type: List[GlobBlock2]  # line 585
        for part in oldPattern:  # match everything in the old filename  # line 586
            if part.isLiteral:  # line 587
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 587
                index += len(part.content)  # line 587
                nextliteral += 1  # line 587
            elif part.content.startswith("?"):  # line 588
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 588
                index += len(part.content)  # line 588
            elif part.content.startswith("["):  # line 589
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 589
                index += 1  # line 589
            elif part.content == "*":  # line 590
                if nextliteral >= len(literals):  # line 591
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 591
                    break  # line 591
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 592
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 593
                index = nxt  # line 593
            else:  # line 594
                Exit("Invalid file pattern specified for move/rename")  # line 594
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 595
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 596
        nextliteral = 0  # line 597
        nextglob = 0  # type: int  # line 597
        outname = []  # type: List[str]  # line 598
        for part in newPattern:  # generate new filename  # line 599
            if part.isLiteral:  # line 600
                outname.append(literals[nextliteral].content)  # line 600
                nextliteral += 1  # line 600
            else:  # line 601
                outname.append(globs[nextglob].matches)  # line 601
                nextglob += 1  # line 601
        pairs.append((filename, "".join(outname)))  # line 602
    return pairs  # line 603

@_coconut_tco  # line 605
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 605
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 609
    if not actions:  # line 610
        return []  # line 610
    sources = None  # type: List[str]  # line 611
    targets = None  # type: List[str]  # line 611
    sources, targets = [list(l) for l in zip(*actions)]  # line 612
    last = len(actions)  # type: int  # line 613
    while last > 1:  # line 614
        clean = True  # type: bool  # line 615
        for i in range(1, last):  # line 616
            try:  # line 617
                index = targets[:i].index(sources[i])  # type: int  # line 618
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 619
                targets.insert(index, targets.pop(i))  # line 620
                clean = False  # line 621
            except:  # target not found in sources: good!  # line 622
                continue  # target not found in sources: good!  # line 622
        if clean:  # line 623
            break  # line 623
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 624
    if exitOnConflict:  # line 625
        for i in range(1, len(actions)):  # line 625
            if sources[i] in targets[:i]:  # line 625
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 625
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 626

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 628
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 629
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 630
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 631

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str], List[str]]':  # line 633
    ''' Returns (root-normalized) Tuple with set of [f{--only], f{--except}, [remotes], [noremotes]] arguments. '''  # line 634
    root = os.getcwd()  # type: str  # line 635
    onlys = []  # type: List[str]  # line 636
    excps = []  # type: List[str]  # line 636
    remotes = []  # type: List[str]  # line 636
    noremotes = []  # type: List[str]  # line 636
    for keys, container in [(("--only", "--include"), onlys), (("--except", "--exclude"), excps), (("--remote", "--remotes", "--only-remote", "--only-remotes", "--include-remote", "--include-remotes"), remotes), (("--except-remote", "--except-remotes", "--exclude-remote", "--exclude-remotes"), noremotes)]:  # line 637
        founds = [i for i in range(len(options)) if any([options[i].startswith(key + "=") or options[i] == key for key in keys])]  # assuming no more than one = in the string  # line 638
        for i in reversed(founds):  # line 639
            if "=" in options[i]:  # line 640
                container.extend(safeSplit(options[i].split("=")[1], ";"))  # TODO keep semicolon or use comma?  # line 641
            elif i + 1 < len(options):  # in case last --only has no argument  # line 642
                container.extend(safeSplit(options[i + 1], ";"))  # TODO test this  # line 643
                del options[i + 1]  # line 644
            del options[i]  # reverse removal  # line 645
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(PARENT + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(PARENT + SLASH))) if excps else None, [os.path.abspath(os.path.normpath(_)) for _ in remotes], [os.path.abspath(os.path.normpath(_)) for _ in noremotes])  # line 646
