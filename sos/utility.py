#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xd23d24ac

# Compiled with Coconut version 1.4.0-post_dev8 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get("__coconut__")
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules["__coconut__"]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_addpattern, _coconut_sentinel
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

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
CODEC_FUNCTIONS = ['utf_32_be', 'utf_32_le', 'utf_32', 'utf_16_be', 'utf_16_le', 'utf_16', 'utf_7', 'utf_8_sig', 'utf_8']  # type: List[str]  # line 156


# Functions
def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 160
    color = useColor[0] and color or ""  # line 161
    reset = Fore.RESET if useColor[0] and color else ""  # line 162
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 163
    sys.stdout.flush()  # PEP528 compatibility  # line 163

def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 166
    color = useColor[0] and color or ""  # line 167
    reset = Fore.RESET if useColor[0] and color else ""  # line 168
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 169
    sys.stderr.flush()  # line 169

@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 172
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 172
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 172

@_coconut_tco  # for os->py access of reading filenames  # line 174
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 174
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 174

def guessEncoding(binary: 'bytes') -> 'List[str]':  # line 176
    ''' If encoding cannot be determined automatically, attempt a guess. Usually it's not unambiguous, though.
  >>> print(guessEncoding(b"abcd0234"))
  ['ascii']
  >>> print(guessEncoding(bytes([0b00100100, 0b11000010, 0b10100010, 0b11100010, 0b10000010, 0b10101100, 0b11110000, 0b10011010, 0b10110011, 0b10011001])))  # utf_8  1:$ 2:cent 3:€, 4:? -> gives 5 options, but it's UTF-8
  ['utf_16_be', 'utf_16_le', 'utf_8']
  >>> print(guessEncoding(bytes([0b00000000, 0b00100100, 0b11011000, 0b01010010, 0b11011111, 0b01100010])))  # utf_16 $ ? -> gives 3 options, on is correct
  ['utf_16_be', 'utf_16_le']
  >>> print(guessEncoding(bytes([0b00100100, 0b11000010, 0b10100010])))  # utf_8  1:$ 2:cent 3:€, 4:? -> gives 2 UTF-8 options
  ['utf_8']
  '''  # line 186
    if all((bite < 128 for bite in binary)):  # TODO move as first detection step  # line 187
        return ["ascii"]  # TODO move as first detection step  # line 187
    decoded = list(filter(lambda _=None: tryOrDefault(lambda: codecs.encode(codecs.decode(binary, _), _) == binary, None), CODEC_FUNCTIONS))  # type: List[str]  # line 188
    if (len(binary) >> 1) << 1 != len(binary):  # only utf-8 variants possible here  # line 189
        decoded[:] = list(filter(lambda _=None: "8" in _, decoded))  # only utf-8 variants possible here  # line 189
    return decoded  # line 190

# Optional dependency: https://github.com/chardet/chardet
try:  # line 193
    import chardet  # line 194
    def detectEncoding(binary: 'bytes') -> '_coconut.typing.Optional[str]':  # returns None if nothing useful detected  # line 195
        return chardet.detect(binary)["encoding"]  # returns None if nothing useful detected  # line 195
except:  # line 196
    def detectEncoding(binary: 'bytes') -> '_coconut.typing.Optional[str]':  # line 197
        ''' Fallback function definition if no chardet library installed. '''  # line 198
        encodings = guessEncoding(binary)  # type: List[str]  # line 199
        if len(encodings) == 1:  # line 200
            return encodings[0]  # line 200
        if len(encodings) == 0:  # or cp1252 or cp850  # line 201
            return None  # or cp1252 or cp850  # line 201
        return encodings[-1]  # line 202

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 204
    try:  # line 205
        return func()  # line 205
    except:  # line 206
        return default  # line 206

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 208
    try:  # line 209
        return func()  # line 209
    except Exception as E:  # line 210
        onError(E)  # line 210

def removePath(key: 'str', value: 'str') -> 'str':  # line 212
    ''' Cleanup of user-specified *global* file patterns, used in config. '''  # line 213
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 214

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 216
    ''' Updates a dictionary by another one, returning a new copy without touching any of the passed dictionaries. '''  # line 217
    d = dict(dikt)  # type: Dict[Any, Any]  # line 218
    d.update(by)  # line 218
    return d  # line 218

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # line 220
    ''' Abstraction for opening both compressed and plain files. '''  # line 221
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # line 222

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 224
    ''' Determine EOL style from a binary string. '''  # line 225
    lf = file.count(b"\n")  # type: int  # line 226
    cr = file.count(b"\r")  # type: int  # line 227
    crlf = file.count(b"\r\n")  # type: int  # line 228
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 229
        if lf != crlf or cr != crlf:  # line 230
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 230
        return b"\r\n"  # line 231
    if lf != 0 and cr != 0:  # line 232
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 232
    if lf > cr:  # Linux/Unix  # line 233
        return b"\n"  # Linux/Unix  # line 233
    if cr > lf:  # older 8-bit machines  # line 234
        return b"\r"  # older 8-bit machines  # line 234
    return None  # no new line contained, cannot determine  # line 235

if TYPE_CHECKING:  # line 237
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 238
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 238
else:  # line 239
    def safeSplit(s, d=None):  # line 240
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 240

@_coconut_tco  # line 242
def hashStr(datas: 'str') -> 'str':  # line 242
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 242

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 244
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 244

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 246
    return lizt[index:].index(what) + index  # line 246

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 248
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 248

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 250
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 250

def Exit(message: 'str'="", code: 'int'=1, excp: 'Any'=None):  # line 252
    if not '--quiet' in sys.argv:  # line 253
        lines = (message + ("" if excp is None else ("\n" + exception(excp)))).replace("\r", "\n").split("\n")  # type: List[str]  # line 254
        printe("[", nl="")  # line 255
        printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN, nl="")  # line 256
        printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + lines[0] + ".") if lines[0] != "" else ""))  # line 257
        if len(lines) > 1:  # line 258
            printe("\n".join(lines[1:]))  # line 261
    if '--wait' in sys.argv:  # line 262
        input("Hit Enter to finish." if not '--quiet' in sys.argv else "")  # line 262
    sys.exit(code)  # line 263

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 265
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 266
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 267
        raise Exception("Cannot possibly strings pack into specified length")  # line 267
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 268
        prefix += separator + ((process)(strings.pop(0)))  # line 268
    return prefix  # line 269

def exception(E) -> 'str':  # line 271
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 272
    import traceback  # line 273
    return str(E) + "\n" + traceback.format_exc() + "\n" + "".join(traceback.format_list(traceback.extract_stack()))  # line 274

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 276
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 277
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 278
    _hash = hashlib.sha256()  # line 279
    wsize = 0  # type: int  # line 280
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 281
        Exit("Hash collision detected. Leaving repository in inconsistent state", 1)  # HINT this exits immediately  # line 282
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 283
    retry = RETRY_NUM  # type: int  # line 284
    while True:  # line 285
        try:  # line 286
            with open(encode(path), "rb") as fd:  # line 287
                while True:  # line 288
                    buffer = fd.read(bufSize)  # type: bytes  # line 289
                    _hash.update(buffer)  # line 290
                    if to:  # line 291
                        to.write(buffer)  # line 291
                    if len(buffer) < bufSize:  # line 292
                        break  # line 292
                    if indicator:  # line 293
                        indicator.getIndicator()  # line 293
                if to:  # line 294
                    to.close()  # line 295
                    wsize = os.stat(encode(saveTo[0])).st_size  # line 296
                    for remote in saveTo[1:]:  # line 297
                        tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 297
            break  # line 298
        except Exception as E:  # (IsADirectoryError, PermissionError)  # line 299
            retry -= 1  # line 300
            if retry == 0:  # line 301
                raise E  # line 301
            error("Cannot open %r - retrying %d more times in %.1d seconds" % (path, RETRY_WAIT))  # line 302
            time.sleep(RETRY_WAIT)  # line 303
    return (_hash.hexdigest(), wsize)  # line 304

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 306
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 307
    for k, v in map.items():  # line 308
        if k in params:  # line 308
            return v  # line 308
    return default  # line 309

@_coconut_tco  # line 311
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 311
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 311

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 313
    ''' Detects a (text) file's encoding, detects the end of line markers, loads the file and splits it into lines.
      returns: 3-tuple (encoding-string, end-of-line bytes, [lines])
  '''  # line 316
    lines = []  # type: List[str]  # line 317
    if filename is not None:  # line 318
        with open(encode(filename), "rb") as fd:  # line 318
            content = fd.read()  # line 318
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 319
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 320
    if filename is not None:  # line 321
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 321
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 321
    elif content is not None:  # line 322
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 322
    else:  # line 323
        return (sys.getdefaultencoding(), b"\n", [])  # line 323
    if ignoreWhitespace:  # line 324
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 324
    return (encoding, eol, lines)  # line 325

if TYPE_CHECKING:  # line 327
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 328
    @_coconut_tco  # line 329
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 329
        ''' A better makedata() version. '''  # line 330
        r = _old._asdict()  # type: Dict[str, Any]  # line 331
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 332
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 333
else:  # line 334
    @_coconut_tco  # line 335
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 335
        ''' A better makedata() version. '''  # line 336
        r = _old._asdict()  # line 337
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 338
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 339

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 341
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 342
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 343
    for path, info in changes.additions.items():  # line 344
        for dpath, dinfo in changes.deletions.items():  # line 344
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 345
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 346
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 347
                break  # deletions loop, continue with next addition  # line 348
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 349

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 351
    ''' Default can be a selection from choice and allows empty input. '''  # line 352
    while True:  # line 353
        selection = input(text).strip().lower()  # line 354
        if selection != "" and selection in choices:  # line 355
            break  # line 355
        if selection == "" and default is not None:  # line 356
            selection = default  # line 356
            break  # line 356
    return selection  # line 357

def user_block_input(output: 'List[str]'):  # line 359
    ''' Side-effect appending to input list. '''  # line 360
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 361
    line = sep  # type: str  # line 361
    while True:  # line 362
        line = input("> ")  # line 363
        if line == sep:  # line 364
            break  # line 364
        output.append(line)  # writes to caller-provided list reference  # line 365

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 367
    encoding = None  # type: str  # typing  # line 368
    othreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 368
    othr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 368
    curreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 368
    curr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 368
    try:  # line 369
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 370
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 371
    except Exception as E:  # in case of binary files  # line 372
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname)), excp=E)  # in case of binary files  # line 372
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 373
        printo(line)  # from generator expression  # line 373

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 375
    ''' Merges other binary text contents in 'file' (or reads from file 'filename') into current text contents 'into' (or reads from file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, don't perform the actual text merging
      eol: if True, will use the other file's EOL marks instead of current file's
      in case of a replace block and INSERT strategy, the change will be added **behind** the original. HINT this could be made configurable
  '''  # line 390
    encoding = None  # type: str  # typing  # line 391
    othreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 391
    othr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 391
    curreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 391
    curr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 391
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 392
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 393
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 394
    except Exception as E:  # line 395
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname)), excp=E)  # line 395
    if None not in (othreol, curreol) and othreol != curreol:  # line 396
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 396
    output = difflib.Differ().compare(othr, curr)  # type: Union[Iterable[str], List[str]]  # line 397
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 398
    tmp = []  # type: List[str]  # block of consecutive lines  # line 399
    last = " "  # type: str  # "into"-file offset for remark lines  # line 400
    no = None  # type: int  # "into"-file offset for remark lines  # line 400
    line = None  # type: str  # "into"-file offset for remark lines  # line 400
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 400

    for no, line in pure.appendEndmarkerIterator(enumerate(output), endValue="X"):  # EOF marker (difflib's output will never be "X" alone)  # line 402
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 403
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 403
            continue  # continue filling current block, no matter what type of block it is  # line 403
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 404
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 404
        if last == " " and len(tmp) > 0:  # same in both files. avoid adding empty keep block  # line 405
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # same in both files. avoid adding empty keep block  # line 405
        elif last == "-":  # may be a pure deletion or part of a replacement (with previous or next block being "+")  # line 406
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 407
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # is a +/- replacement  # line 408
                offset += len(blocks[-2].lines)  # line 409
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to insert merge block TODO why -1 necessary?  # line 410
                blocks.pop()  # line 411
        elif last == "+":  # may be a pure insertion or part of a replacement (with previous or next block being "-")  # line 412
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # line 413
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 414
                offset += len(blocks[-1].lines)  # line 415
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 416
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 417
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 418
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 418
        last = line[0]  # remember for comparison once next block comes around  # line 419
        tmp[:] = [line[2:]]  # only remember current line as fresh next block  # line 420
# TODO add code to detect and mark moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 422
    debug("Diff blocks: " + repr(blocks))  # line 423
    if diffOnly:  # line 424
        return (blocks, nl)  # line 424

# now perform merge operations depending on detected blocks and selected merge options
    output = []  # clean list of strings  # line 427
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 427
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 427
    selection = ""  # type: str  # clean list of strings  # line 427
    for block in blocks:  # line 428
        if block.tipe == MergeBlockType.KEEP:  # line 429
            output.extend(block.lines)  # line 429
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 430
            output.extend(block.lines)  # line 432
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 433
            if len(block.lines) == len(block.replaces.lines) == 1:  # both sides are one-liners: apply next sub-level merge  # line 434
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 435
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 436
#      if mergeOperation == MergeOperation.ASK:  # more than one line: needs user input
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 438
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 439
                while True:  # line 440
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 441
                    if op in "tb":  # order for both determined here - TODO make configurable  # line 442
                        output.extend(block.lines)  # order for both determined here - TODO make configurable  # line 442
                    if op in "ib":  # line 443
                        output.extend(block.replaces.lines)  # line 443
                    if op == "u":  # line 444
                        user_block_input(output)  # line 444
                    if op in "tbiu":  # was valid user input  # line 445
                        break  # was valid user input  # line 445
            else:  # more than one line and not ask  # line 446
                if mergeOperation == MergeOperation.REMOVE:  # line 447
                    pass  # line 447
                elif mergeOperation == MergeOperation.BOTH:  # line 448
                    output.extend(block.lines)  # line 448
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 449
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 449
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 450
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 451
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 453
                if selection in "ao":  # line 454
                    if block.tipe == MergeBlockType.INSERT:  # line 455
                        add_all = "y" if selection == "a" else "n"  # line 455
                        selection = add_all  # line 455
                    else:  # REMOVE case  # line 456
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 456
                        selection = del_all  # REMOVE case  # line 456
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 457
                output.extend(block.lines)  # line 459
    debug("Merge output: " + "\n".join(output))  # line 460
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 461
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 464
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 464
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
      returns: merged line
      raises: Exception in case of unparseable marker
  '''  # line 469
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 470
    blocks = []  # type: List[MergeBlock]  # line 471
    for i, charline in enumerate(out):  # line 472
        if charline[0] == "+":  # line 473
            if i + 1 < len(out) and out[i + 1][0] == "+":  # look-ahead: block will continue  # line 474
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 475
                    blocks[-1].lines.append(charline[2])  # add one more character to the accumulating list  # line 476
                else:  # first + in block  # line 477
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [charline[2]], i))  # line 478
            else:  # last charline of + block  # line 479
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 480
                    blocks[-1].lines.append(charline[2])  # line 481
                else:  # single charline  # line 482
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [charline[2]], i))  # line 483
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 484
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 485
                    blocks.pop()  # line 485
        elif charline[0] == "-":  # line 486
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 487
                blocks[-1].lines.append(charline[2])  # line 488
            else:  # first in block  # line 489
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [charline[2]], i))  # line 490
        elif charline[0] == " ":  # keep area  # line 491
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 492
                blocks[-1].lines.append(charline[2])  # line 493
            else:  # first in block  # line 494
                blocks.append(MergeBlock(MergeBlockType.KEEP, [charline[2]], i))  # line 495
        else:  # line 496
            raise Exception("Cannot parse diff charline %r" % charline)  # line 496
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # update blocks  # line 497
    if diffOnly:  # debug interrupt - only return blocks  # line 498
        return blocks  # debug interrupt - only return blocks  # line 498

    out = []  # line 500
    for i, block in enumerate(blocks):  # line 501
        if block.tipe == MergeBlockType.KEEP:  # line 502
            out.extend(block.lines)  # line 502
        elif block.tipe == MergeBlockType.REPLACE:  # line 503
            if mergeOperation == MergeOperation.ASK:  # TODO add loop here like in merge  # line 504
                printo(pure.ajoin("- ", othr))  # line 505
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 506
                printo("+ " + (" " * i) + block.lines[0])  # line 507
                printo(pure.ajoin("+ ", into))  # line 508
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 509
                if op in "tb":  # line 510
                    out.extend(block.lines)  # line 510
                    break  # line 510
                if op in "ib":  # line 511
                    out.extend(block.replaces.lines)  # line 511
                    break  # line 511
                if op == "m":  # line 512
                    user_block_input(out)  # line 512
                    break  # line 512
            else:  # non-interactive  # line 513
                if mergeOperation == MergeOperation.REMOVE:  # neither keep old nor insert new  # line 514
                    pass  # neither keep old nor insert new  # line 514
                elif mergeOperation == MergeOperation.BOTH:  # remove old and insert new  # line 515
                    out.extend(block.lines)  # remove old and insert new  # line 515
                elif mergeOperation == MergeOperation.INSERT:  # keep old an insert new  # line 516
                    out.extend(block.replaces.lines + block.lines)  # keep old an insert new  # line 516
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 517
            out.extend(block.lines)  # line 517
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 518
            out.extend(block.lines)  # line 518
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 520

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 522
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 525
    debug("Detecting root folders...")  # line 526
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 527
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 528
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 529
        contents = set(os.listdir(path))  # type: Set[str]  # line 530
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 531
        choice = None  # type: _coconut.typing.Optional[str]  # line 532
        if len(vcss) > 1:  # line 533
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 534
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 535
        elif len(vcss) > 0:  # line 536
            choice = vcss[0]  # line 536
        if not vcs[0] and choice:  # memorize current repo root  # line 537
            vcs = (path, choice)  # memorize current repo root  # line 537
        new = os.path.dirname(path)  # get parent path  # line 538
        if new == path:  # avoid infinite loop  # line 539
            break  # avoid infinite loop  # line 539
        path = new  # line 540
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 541
        if vcs[0]:  # already detected vcs base and command  # line 542
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 542
        sos = path  # line 543
        while True:  # continue search for VCS base  # line 544
            contents = set(os.listdir(path))  # line 545
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 546
            choice = None  # line 547
            if len(vcss) > 1:  # line 548
                choice = SVN if SVN in vcss else vcss[0]  # line 549
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 550
            elif len(vcss) > 0:  # line 551
                choice = vcss[0]  # line 551
            if choice:  # line 552
                return (sos, path, choice)  # line 552
            new = os.path.dirname(path)  # get parent path  # line 553
            if new == path:  # no VCS folder found  # line 554
                return (sos, None, None)  # no VCS folder found  # line 554
            path = new  # line 555
    return (None, vcs[0], vcs[1])  # line 556

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 558
    index = 0  # type: int  # line 559
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 560
    while index < len(pattern):  # line 561
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 562
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 562
            continue  # line 562
        if pattern[index] in "*?":  # line 563
            count = 1  # type: int  # line 564
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 565
                count += 1  # line 565
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 566
            index += count  # line 566
            continue  # line 566
        if pattern[index:index + 2] == "[!":  # line 567
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 567
            index += len(out[-1][1])  # line 567
            continue  # line 567
        count = 1  # line 568
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 569
            count += 1  # line 569
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 570
        index += count  # line 570
    return out  # line 571

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 573
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 574
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 575
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 577
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 577
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 578
        Exit("Source and target file patterns differ in semantics")  # line 578
    return (ot, nt)  # line 579

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 581
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 582
    pairs = []  # type: List[Tuple[str, str]]  # line 583
    for filename in filenames:  # line 584
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 585
        nextliteral = 0  # type: int  # line 586
        index = 0  # type: int  # line 586
        parsedOld = []  # type: List[GlobBlock2]  # line 587
        for part in oldPattern:  # match everything in the old filename  # line 588
            if part.isLiteral:  # line 589
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 589
                index += len(part.content)  # line 589
                nextliteral += 1  # line 589
            elif part.content.startswith("?"):  # line 590
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 590
                index += len(part.content)  # line 590
            elif part.content.startswith("["):  # line 591
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 591
                index += 1  # line 591
            elif part.content == "*":  # line 592
                if nextliteral >= len(literals):  # line 593
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 593
                    break  # line 593
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 594
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 595
                index = nxt  # line 595
            else:  # line 596
                Exit("Invalid file pattern specified for move/rename")  # line 596
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 597
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 598
        nextliteral = 0  # line 599
        nextglob = 0  # type: int  # line 599
        outname = []  # type: List[str]  # line 600
        for part in newPattern:  # generate new filename  # line 601
            if part.isLiteral:  # line 602
                outname.append(literals[nextliteral].content)  # line 602
                nextliteral += 1  # line 602
            else:  # line 603
                outname.append(globs[nextglob].matches)  # line 603
                nextglob += 1  # line 603
        pairs.append((filename, "".join(outname)))  # line 604
    return pairs  # line 605

@_coconut_tco  # line 607
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 607
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 611
    if not actions:  # line 612
        return []  # line 612
    sources = None  # type: List[str]  # line 613
    targets = None  # type: List[str]  # line 613
    sources, targets = [list(l) for l in zip(*actions)]  # line 614
    last = len(actions)  # type: int  # line 615
    while last > 1:  # line 616
        clean = True  # type: bool  # line 617
        for i in range(1, last):  # line 618
            try:  # line 619
                index = targets[:i].index(sources[i])  # type: int  # line 620
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 621
                targets.insert(index, targets.pop(i))  # line 622
                clean = False  # line 623
            except:  # target not found in sources: good!  # line 624
                continue  # target not found in sources: good!  # line 624
        if clean:  # line 625
            break  # line 625
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 626
    if exitOnConflict:  # line 627
        for i in range(1, len(actions)):  # line 627
            if sources[i] in targets[:i]:  # line 627
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 627
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 628

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 630
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 631
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 632
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 633

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str], List[str]]':  # line 635
    ''' Returns (root-normalized) Tuple with set of [f{--only], f{--except}, [remotes], [noremotes]] arguments. '''  # line 636
    root = os.getcwd()  # type: str  # line 637
    onlys = []  # type: List[str]  # line 638
    excps = []  # type: List[str]  # line 638
    remotes = []  # type: List[str]  # line 638
    noremotes = []  # type: List[str]  # line 638
    for keys, container in [(("--only", "--include"), onlys), (("--except", "--exclude"), excps), (("--remote", "--remotes", "--only-remote", "--only-remotes", "--include-remote", "--include-remotes"), remotes), (("--except-remote", "--except-remotes", "--exclude-remote", "--exclude-remotes"), noremotes)]:  # line 639
        founds = [i for i in range(len(options)) if any([options[i].startswith(key + "=") or options[i] == key for key in keys])]  # assuming no more than one = in the string  # line 640
        for i in reversed(founds):  # line 641
            if "=" in options[i]:  # line 642
                container.extend(safeSplit(options[i].split("=")[1], ";"))  # TODO keep semicolon or use comma?  # line 643
            elif i + 1 < len(options):  # in case last --only has no argument  # line 644
                container.extend(safeSplit(options[i + 1], ";"))  # TODO test this  # line 645
                del options[i + 1]  # line 646
            del options[i]  # reverse removal  # line 647
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(PARENT + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(PARENT + SLASH))) if excps else None, [os.path.abspath(os.path.normpath(_)) for _ in remotes], [os.path.abspath(os.path.normpath(_)) for _ in noremotes])  # line 648
