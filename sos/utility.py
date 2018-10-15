#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x2b4660dd

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
def enableColor(enable: 'bool'=True, force: 'bool'=False):  # line 52
    ''' This piece of code only became necessary to enable enabling/disabling of the colored terminal output after initialization. '''  # line 53
    global useColor  # line 54
    if not force and (useColor[0] if enable else not useColor[0]):  # nothing to do since already set  # line 55
        return  # nothing to do since already set  # line 55
    MARKER.value = MARKER_COLOR if enable and sys.platform != "win32" else usage.MARKER_TEXT  # HINT because it doesn't work with the loggers yet  # line 56
    if enable:  # line 57
        try:  # line 58
            colorama.init(wrap=False)  # line 59
            if useColor[0] is None:  # very initial, do some monkey-patching  # line 60
                sys.stdout = colorama.AnsiToWin32(sys.stdout).stream  # TODO replace by "better-exceptions" code  # line 61
                sys.stderr = colorama.AnsiToWin32(sys.stderr).stream  # line 62
        except:  # line 63
            pass  # line 63
    else:  # line 64
        try:  # line 65
            colorama.deinit()  # line 65
        except:  # line 66
            pass  # line 66
    useColor[0] = enable  # line 67

# fallbacks in case there is no colorama library present
Fore = Accessor({k: "" for k in ["RESET", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "YELLOW"]})  # type: Dict[str, str]  # line 70
Back = Fore  # type: Dict[str, str]  # line 71
Style = Accessor({k: "" for k in ["NORMAL", "BRIGHT", "RESET_ALL"]})  # type: Dict[str, str]  # line 72
MARKER = Accessor({"value": usage.MARKER_TEXT})  # type: str  # assume default text-only  # line 73
try:  # line 74
    import pdb  # line 75
    pdb.set_trace()  # line 75
    import colorama  # line 76
    import colorama.ansitowin32  # line 76
    if colorama.ansitowin32.is_a_tty(sys.stderr):  # list of ansi codes: http://bluesock.org/~willkg/dev/ansi.html  # line 77
        from colorama import Back  # line 78
        from colorama import Fore  # line 78
        from colorama import Style  # line 78
        MARKER_COLOR = Fore.WHITE + usage.MARKER_TEXT + Fore.RESET  # type: str  # line 79
        if sys.platform == "win32":  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 80
            Style.BRIGHT = ""  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 80
        enableColor()  # line 81
except:  # if library not installed, use fallback even for colored texts  # line 82
    MARKER_COLOR = usage.MARKER_TEXT  # if library not installed, use fallback even for colored texts  # line 82

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 84
    Number = TypeVar("Number", int, float)  # line 85
    class Counter(Generic[Number]):  # line 86
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 87
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 88
            _.value = initial  # type: Number  # line 88
        def inc(_, by: 'Number'=1) -> 'Number':  # line 89
            _.value += by  # line 89
            return _.value  # line 89
else:  # line 90
    class Counter:  # line 91
        def __init__(_, initial=0) -> 'None':  # line 92
            _.value = initial  # line 92
        def inc(_, by=1):  # line 93
            _.value += by  # line 93
            return _.value  # line 93

class ProgressIndicator(Counter):  # line 95
    ''' Manages a rotating progress indicator. '''  # line 96
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 97
        super(ProgressIndicator, _).__init__(-1)  # line 97
        _.symbols = symbols  # line 97
        _.timer = time.time()  # type: float  # line 97
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 97
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 98
        ''' Returns a value only if a certain time has passed. '''  # line 99
        newtime = time.time()  # type: float  # line 100
        if newtime - _.timer < .1:  # line 101
            return None  # line 101
        _.timer = newtime  # line 102
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 103
        if _.callback:  # line 104
            _.callback(sign)  # line 104
        return sign  # line 105

class Logger:  # line 107
    ''' Logger that supports joining many items. '''  # line 108
    def __init__(_, log) -> 'None':  # line 109
        _._log = log  # line 109
    def debug(_, *s):  # line 110
        _._log.debug(pure.sjoin(*s))  # line 110
    def info(_, *s):  # line 111
        _._log.info(pure.sjoin(*s))  # line 111
    def warn(_, *s):  # line 112
        _._log.warning(pure.sjoin(*s))  # line 112
    def error(_, *s):  # line 113
        _._log.error(pure.sjoin(*s))  # line 113


# Constants
_log = Logger(logging.getLogger(__name__))  # line 117
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 117
CONFIGURABLE_FLAGS = ["strict", "track", "picky", "compress", "useChangesCommand", "useUnicodeFont", "useColorOutput"]  # type: List[str]  # line 118
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 119
CONFIGURABLE_INTS = ["logLines", "diffLines"]  # type: List[str]  # line 120
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 121
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 122
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 123
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 124
BACKUP_SUFFIX = "_last"  # type: str  # line 125
metaFolder = ".sos"  # type: str  # line 126
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 127
metaFile = ".meta"  # type: str  # line 128
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 129
KIBI = 1 << 10  # type: int  # line 130
MEBI = 1 << 20  # type: int  # line 130
GIBI = 1 << 30  # type: int  # line 130
bufSize = MEBI  # type: int  # line 131
UTF8 = "utf_8"  # type: str  # early used constant, not defined in standard library  # line 132
SVN = "svn"  # type: str  # line 133
SLASH = "/"  # type: str  # line 134
PARENT = ".."  # type: str  # line 135
DOT_SYMBOL = "\u00b7"  # type: str  # line 136
MULT_SYMBOL = "\u00d7"  # type: str  # line 137
CROSS_SYMBOL = "\u2716"  # type: str  # line 138
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 139
PLUSMINUS_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 140
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in "this revision"  # line 141
MOVE_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 142
METADATA_FORMAT = 2  # type: int  # counter for (partially incompatible) consecutive formats (was undefined, "1" is the first numbered format version after that)  # line 143
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 144
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 145
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # bool: tracked? (otherwise picky), str:arguments to "commit" TODO CVS, RCS have probably different per-file operation  # line 146
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 147
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[_coconut.typing.Optional[bytes], str]  # line 148
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[_coconut.typing.Optional[str], int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 149
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "useColorOutput": True, "diffLines": 2, "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 150


# Functions
def siSize(size: 'int') -> 'str':  # line 167
    ''' Returns number and unit. '''  # line 168
    return "%.2f MiB" % (float(size) / MEBI) if size > 1.25 * MEBI else ("%.2f KiB" % (float(size) / KIBI) if size > 1.25 * KIBI else ("%d bytes" % size))  # line 169

def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 171
    color = useColor and color or ""  # line 172
    reset = Fore.RESET if useColor and color else ""  # line 173
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 174
    sys.stdout.flush()  # PEP528 compatibility  # line 174
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 176
    color = useColor and color or ""  # line 177
    reset = Fore.RESET if useColor and color else ""  # line 178
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 179
    sys.stderr.flush()  # line 179
@_coconut_tco  # line 180
def encode(s: 'str') -> 'bytes':  # line 180
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 181
@_coconut_tco  # for os->py access of reading filenames  # line 182
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 182
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 182
try:  # line 183
    import chardet  # https://github.com/chardet/chardet  # line 184
    def detectEncoding(binary: 'bytes') -> 'str':  # line 185
        return chardet.detect(binary)["encoding"]  # line 185
except:  # Guess the encoding  # line 186
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 186
        ''' Fallback if chardet library missing. '''  # line 187
        try:  # line 188
            binary.decode(UTF8)  # line 188
            return UTF8  # line 188
        except UnicodeError:  # line 189
            pass  # line 189
        try:  # line 190
            binary.decode("utf_16")  # line 190
            return "utf_16"  # line 190
        except UnicodeError:  # line 191
            pass  # line 191
        try:  # line 192
            binary.decode("cp1252")  # line 192
            return "cp1252"  # line 192
        except UnicodeError:  # line 193
            pass  # line 193
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 194

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 196
    try:  # line 197
        return func()  # line 197
    except:  # line 198
        return default  # line 198

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 200
    try:  # line 201
        return func()  # line 201
    except Exception as E:  # line 202
        onError(E)  # line 202

def removePath(key: 'str', value: 'str') -> 'str':  # line 204
    ''' Cleanup of user-specified global file patterns, used in config. '''  # TODO improve  # line 205
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 206

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 208
    ''' Updates a dictionary by another one, returning a new copy without touching any of the passed dictionaries. '''  # line 209
    d = dict(dikt)  # type: Dict[Any, Any]  # line 210
    d.update(by)  # line 210
    return d  # line 210

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # line 212
    ''' Abstraction for opening both compressed and plain files. '''  # line 213
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # line 214

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 216
    ''' Determine EOL style from a binary string. '''  # line 217
    lf = file.count(b"\n")  # type: int  # line 218
    cr = file.count(b"\r")  # type: int  # line 219
    crlf = file.count(b"\r\n")  # type: int  # line 220
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 221
        if lf != crlf or cr != crlf:  # line 222
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 222
        return b"\r\n"  # line 223
    if lf != 0 and cr != 0:  # line 224
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 224
    if lf > cr:  # Linux/Unix  # line 225
        return b"\n"  # Linux/Unix  # line 225
    if cr > lf:  # older 8-bit machines  # line 226
        return b"\r"  # older 8-bit machines  # line 226
    return None  # no new line contained, cannot determine  # line 227

if TYPE_CHECKING:  # line 229
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 230
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 230
else:  # line 231
    def safeSplit(s, d=None):  # line 232
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 232

@_coconut_tco  # line 234
def hashStr(datas: 'str') -> 'str':  # line 234
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 234

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 236
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 236

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 238
    return lizt[index:].index(what) + index  # line 238

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 240
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 240

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 242
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 242

def Exit(message: 'str'="", code=1):  # line 244
    lines = message.split("\n")  # type: List[str]  # line 245
    printe("[", nl="")  # line 246
    printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN, nl="")  # line 247
    printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + lines[0] + ".") if lines[0] != "" else ""))  # line 248
    if len(lines) > 1:  # line 249
        printe("\n".join(lines[1:]))  # line 252
    sys.exit(code)  # line 253

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 255
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 256
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 257
        raise Exception("Cannot possibly strings pack into specified length")  # line 257
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 258
        prefix += separator + ((process)(strings.pop(0)))  # line 258
    return prefix  # line 259

def exception(E):  # line 261
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 262
    printo(str(E))  # line 263
    import traceback  # line 264
    traceback.print_exc()  # line 265
    traceback.print_stack()  # line 266

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 268
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 269
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 270
    _hash = hashlib.sha256()  # line 271
    wsize = 0  # type: int  # line 272
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 273
        Exit("Hash collision detected. Leaving repository in inconsistent state", 1)  # HINT this exits immediately  # line 274
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 275
    with open(encode(path), "rb") as fd:  # line 276
        while True:  # line 277
            buffer = fd.read(bufSize)  # type: bytes  # line 278
            _hash.update(buffer)  # line 279
            if to:  # line 280
                to.write(buffer)  # line 280
            if len(buffer) < bufSize:  # line 281
                break  # line 281
            if indicator:  # line 282
                indicator.getIndicator()  # line 282
        if to:  # line 283
            to.close()  # line 284
            wsize = os.stat(encode(saveTo[0])).st_size  # line 285
            for remote in saveTo[1:]:  # line 286
                tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 286
    return (_hash.hexdigest(), wsize)  # line 287

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 289
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 290
    for k, v in map.items():  # line 291
        if k in params:  # line 291
            return v  # line 291
    return default  # line 292

@_coconut_tco  # line 294
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 294
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 294

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 296
    lines = []  # type: List[str]  # line 297
    if filename is not None:  # line 298
        with open(encode(filename), "rb") as fd:  # line 298
            content = fd.read()  # line 298
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 299
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 300
    if filename is not None:  # line 301
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 301
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 301
    elif content is not None:  # line 302
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 302
    else:  # line 303
        return (sys.getdefaultencoding(), b"\n", [])  # line 303
    if ignoreWhitespace:  # line 304
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 304
    return (encoding, eol, lines)  # line 305

if TYPE_CHECKING:  # line 307
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 308
    @_coconut_tco  # line 309
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 309
        ''' A better makedata() version. '''  # line 310
        r = _old._asdict()  # type: Dict[str, Any]  # line 311
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 312
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 313
else:  # line 314
    @_coconut_tco  # line 315
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 315
        ''' A better makedata() version. '''  # line 316
        r = _old._asdict()  # line 317
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 318
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 319

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 321
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 322
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 323
    for path, info in changes.additions.items():  # line 324
        for dpath, dinfo in changes.deletions.items():  # line 324
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 325
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 326
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 327
                break  # deletions loop, continue with next addition  # line 328
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 329

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 331
    ''' Default can be a selection from choice and allows empty input. '''  # line 332
    while True:  # line 333
        selection = input(text).strip().lower()  # line 334
        if selection != "" and selection in choices:  # line 335
            break  # line 335
        if selection == "" and default is not None:  # line 336
            selection = default  # line 336
            break  # line 336
    return selection  # line 337

def user_block_input(output: 'List[str]'):  # line 339
    ''' Side-effect appending to input list. '''  # line 340
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 341
    line = sep  # type: str  # line 341
    while True:  # line 342
        line = input("> ")  # line 343
        if line == sep:  # line 344
            break  # line 344
        output.append(line)  # writes to caller-provided list reference  # line 345

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 347
    encoding = None  # type: str  # line 348
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 348
    othr = None  # type: _coconut.typing.Sequence[str]  # line 348
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 348
    curr = None  # type: _coconut.typing.Sequence[str]  # line 348
    try:  # line 349
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 350
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 351
    except Exception as E:  # line 352
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname), E))  # line 352
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 353
        printo(line)  # from generator expression  # line 353

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 355
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 370
    encoding = None  # type: str  # line 371
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 371
    othr = None  # type: _coconut.typing.Sequence[str]  # line 371
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 371
    curr = None  # type: _coconut.typing.Sequence[str]  # line 371
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 372
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 373
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 374
    except Exception as E:  # line 375
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname), E))  # line 375
    if None not in [othreol, curreol] and othreol != curreol:  # line 376
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 376
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 377
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 378
    tmp = []  # type: List[str]  # block lines  # line 379
    last = " "  # type: str  # "into"-file offset for remark lines  # line 380
    no = None  # type: int  # "into"-file offset for remark lines  # line 380
    line = None  # type: str  # "into"-file offset for remark lines  # line 380
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 380
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 381
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 382
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 382
            continue  # continue filling current block, no matter what type of block it is  # line 382
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 383
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 383
        if last == " ":  # block is same in both files  # line 384
            if len(tmp) > 0:  # avoid adding empty keep block  # line 385
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 385
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 386
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 387
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 388
                offset += len(blocks[-2].lines)  # line 389
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 390
                blocks.pop()  # line 391
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 392
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 393
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 394
                offset += len(blocks[-1].lines)  # line 395
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 396
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 397
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 398
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 398
        last = line[0]  # line 399
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 400
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 402
    debug("Diff blocks: " + repr(blocks))  # line 403
    if diffOnly:  # line 404
        return (blocks, nl)  # line 404

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 407
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 407
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 407
    selection = ""  # type: str  # clean list of strings  # line 407
    for block in blocks:  # line 408
        if block.tipe == MergeBlockType.KEEP:  # line 409
            output.extend(block.lines)  # line 409
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 410
            output.extend(block.lines)  # line 412
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 413
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 414
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 415
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 416
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 417
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 418
                while True:  # line 419
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 420
                    if op in "tb":  # line 421
                        output.extend(block.lines)  # line 421
                    if op in "ib":  # line 422
                        output.extend(block.replaces.lines)  # line 422
                    if op == "u":  # line 423
                        user_block_input(output)  # line 423
                    if op in "tbiu":  # line 424
                        break  # line 424
            else:  # more than one line and not ask  # line 425
                if mergeOperation == MergeOperation.REMOVE:  # line 426
                    pass  # line 426
                elif mergeOperation == MergeOperation.BOTH:  # line 427
                    output.extend(block.lines)  # line 427
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 428
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 428
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 429
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 430
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 432
                if selection in "ao":  # line 433
                    if block.tipe == MergeBlockType.INSERT:  # line 434
                        add_all = "y" if selection == "a" else "n"  # line 434
                        selection = add_all  # line 434
                    else:  # REMOVE case  # line 435
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 435
                        selection = del_all  # REMOVE case  # line 435
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 436
                output.extend(block.lines)  # line 438
    debug("Merge output: " + "; ".join(output))  # line 439
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 440
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 443
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 443
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 446
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 447
    blocks = []  # type: List[MergeBlock]  # line 448
    for i, line in enumerate(out):  # line 449
        if line[0] == "+":  # line 450
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 451
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 452
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 453
                else:  # first + in block  # line 454
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 455
            else:  # last line of + block  # line 456
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 457
                    blocks[-1].lines.append(line[2])  # line 458
                else:  # single line  # line 459
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 460
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 461
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 462
                    blocks.pop()  # line 462
        elif line[0] == "-":  # line 463
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 464
                blocks[-1].lines.append(line[2])  # line 465
            else:  # first in block  # line 466
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 467
        elif line[0] == " ":  # line 468
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 469
                blocks[-1].lines.append(line[2])  # line 470
            else:  # first in block  # line 471
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 472
        else:  # line 473
            raise Exception("Cannot parse diff line %r" % line)  # line 473
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 474
    if diffOnly:  # line 475
        return blocks  # line 475
    out[:] = []  # line 476
    for i, block in enumerate(blocks):  # line 477
        if block.tipe == MergeBlockType.KEEP:  # line 478
            out.extend(block.lines)  # line 478
        elif block.tipe == MergeBlockType.REPLACE:  # line 479
            if mergeOperation == MergeOperation.ASK:  # line 480
                printo(pure.ajoin("- ", othr))  # line 481
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 482
                printo("+ " + (" " * i) + block.lines[0])  # line 483
                printo(pure.ajoin("+ ", into))  # line 484
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 485
                if op in "tb":  # line 486
                    out.extend(block.lines)  # line 486
                    break  # line 486
                if op in "ib":  # line 487
                    out.extend(block.replaces.lines)  # line 487
                    break  # line 487
                if op == "m":  # line 488
                    user_block_input(out)  # line 488
                    break  # line 488
            else:  # non-interactive  # line 489
                if mergeOperation == MergeOperation.REMOVE:  # line 490
                    pass  # line 490
                elif mergeOperation == MergeOperation.BOTH:  # line 491
                    out.extend(block.lines)  # line 491
                elif mergeOperation == MergeOperation.INSERT:  # line 492
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 492
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 493
            out.extend(block.lines)  # line 493
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 494
            out.extend(block.lines)  # line 494
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 496

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 498
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 501
    debug("Detecting root folders...")  # line 502
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 503
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 504
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 505
        contents = set(os.listdir(path))  # type: Set[str]  # line 506
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 507
        choice = None  # type: _coconut.typing.Optional[str]  # line 508
        if len(vcss) > 1:  # line 509
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 510
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 511
        elif len(vcss) > 0:  # line 512
            choice = vcss[0]  # line 512
        if not vcs[0] and choice:  # memorize current repo root  # line 513
            vcs = (path, choice)  # memorize current repo root  # line 513
        new = os.path.dirname(path)  # get parent path  # line 514
        if new == path:  # avoid infinite loop  # line 515
            break  # avoid infinite loop  # line 515
        path = new  # line 516
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 517
        if vcs[0]:  # already detected vcs base and command  # line 518
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 518
        sos = path  # line 519
        while True:  # continue search for VCS base  # line 520
            contents = set(os.listdir(path))  # line 521
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 522
            choice = None  # line 523
            if len(vcss) > 1:  # line 524
                choice = SVN if SVN in vcss else vcss[0]  # line 525
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 526
            elif len(vcss) > 0:  # line 527
                choice = vcss[0]  # line 527
            if choice:  # line 528
                return (sos, path, choice)  # line 528
            new = os.path.dirname(path)  # get parent path  # line 529
            if new == path:  # no VCS folder found  # line 530
                return (sos, None, None)  # no VCS folder found  # line 530
            path = new  # line 531
    return (None, vcs[0], vcs[1])  # line 532

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 534
    index = 0  # type: int  # line 535
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 536
    while index < len(pattern):  # line 537
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 538
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 538
            continue  # line 538
        if pattern[index] in "*?":  # line 539
            count = 1  # type: int  # line 540
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 541
                count += 1  # line 541
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 542
            index += count  # line 542
            continue  # line 542
        if pattern[index:index + 2] == "[!":  # line 543
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 543
            index += len(out[-1][1])  # line 543
            continue  # line 543
        count = 1  # line 544
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 545
            count += 1  # line 545
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 546
        index += count  # line 546
    return out  # line 547

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 549
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 550
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 551
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 553
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 553
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 554
        Exit("Source and target file patterns differ in semantics")  # line 554
    return (ot, nt)  # line 555

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 557
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 558
    pairs = []  # type: List[Tuple[str, str]]  # line 559
    for filename in filenames:  # line 560
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 561
        nextliteral = 0  # type: int  # line 562
        index = 0  # type: int  # line 562
        parsedOld = []  # type: List[GlobBlock2]  # line 563
        for part in oldPattern:  # match everything in the old filename  # line 564
            if part.isLiteral:  # line 565
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 565
                index += len(part.content)  # line 565
                nextliteral += 1  # line 565
            elif part.content.startswith("?"):  # line 566
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 566
                index += len(part.content)  # line 566
            elif part.content.startswith("["):  # line 567
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 567
                index += 1  # line 567
            elif part.content == "*":  # line 568
                if nextliteral >= len(literals):  # line 569
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 569
                    break  # line 569
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 570
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 571
                index = nxt  # line 571
            else:  # line 572
                Exit("Invalid file pattern specified for move/rename")  # line 572
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 573
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 574
        nextliteral = 0  # line 575
        nextglob = 0  # type: int  # line 575
        outname = []  # type: List[str]  # line 576
        for part in newPattern:  # generate new filename  # line 577
            if part.isLiteral:  # line 578
                outname.append(literals[nextliteral].content)  # line 578
                nextliteral += 1  # line 578
            else:  # line 579
                outname.append(globs[nextglob].matches)  # line 579
                nextglob += 1  # line 579
        pairs.append((filename, "".join(outname)))  # line 580
    return pairs  # line 581

@_coconut_tco  # line 583
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 583
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 587
    if not actions:  # line 588
        return []  # line 588
    sources = None  # type: List[str]  # line 589
    targets = None  # type: List[str]  # line 589
    sources, targets = [list(l) for l in zip(*actions)]  # line 590
    last = len(actions)  # type: int  # line 591
    while last > 1:  # line 592
        clean = True  # type: bool  # line 593
        for i in range(1, last):  # line 594
            try:  # line 595
                index = targets[:i].index(sources[i])  # type: int  # line 596
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 597
                targets.insert(index, targets.pop(i))  # line 598
                clean = False  # line 599
            except:  # target not found in sources: good!  # line 600
                continue  # target not found in sources: good!  # line 600
        if clean:  # line 601
            break  # line 601
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 602
    if exitOnConflict:  # line 603
        for i in range(1, len(actions)):  # line 603
            if sources[i] in targets[:i]:  # line 603
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 603
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 604

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 606
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 607
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 608
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 609

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str]]':  # line 611
    ''' Returns (root-normalized) set of --only and --except arguments. '''  # line 612
    root = os.getcwd()  # type: str  # line 613
    onlys = []  # type: List[str]  # line 614
    excps = []  # type: List[str]  # line 614
    remotes = []  # type: List[str]  # line 614
    for keys, container in [(("--only", "--include"), onlys), (("--except", "--exclude"), excps), (("--remote",), remotes)]:  # line 615
        founds = [i for i in range(len(options)) if any([options[i].startswith(key) for key in keys])]  # assuming no more than one = in the string  # line 616
        for i in reversed(founds):  # line 617
            if "=" in options[i]:  # line 618
                container.append(options[i].split("=")[1])  # line 619
            elif i + 1 < len(options):  # in case last --only has no argument  # line 620
                container.append(options[i + 1])  # line 621
                del options[i + 1]  # line 622
            del options[i]  # reverse removal  # line 623
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(PARENT + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(PARENT + SLASH))) if excps else None, remotes)  # line 624
