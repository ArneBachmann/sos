#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xbaab8345

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


verbose = [None] if '--verbose' in sys.argv or '-v' in sys.argv else []  # type: List[None]  # line 35
debug_ = [None] if os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv else []  # type: List[None]  # line 36


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
    ''' This piece of code only became necessary to enable enabling/disabling of the colored terminal output after initialization.
      enable: target state
      force: for testing only
  '''  # line 56
    if not force and (useColor[0] if enable else not useColor[0]):  # nothing to do since already set  # line 57
        return  # nothing to do since already set  # line 57
    MARKER.value = MARKER_COLOR if enable and sys.platform != "win32" else usage.MARKER_TEXT  # HINT because it doesn't work with the loggers yet  # line 58
    try:  # line 59
        if useColor[0] is None:  # very initial, do some monkey-patching  # line 60
            colorama.init(wrap=False)  # line 61
            sys.stdout = colorama.AnsiToWin32(sys.stdout).stream  # TODO replace by "better-exceptions" code  # line 62
            sys.stderr = colorama.AnsiToWin32(sys.stderr).stream  # line 63
    except:  # line 64
        pass  # line 64
    useColor[0] = enable  # line 65

# fallbacks in case there is no colorama library present
Fore = Accessor({k: "" for k in ["RESET", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "YELLOW", "WHITE"]})  # type: Dict[str, str]  # line 68
Style = Accessor({k: "" for k in ["NORMAL", "BRIGHT", "RESET_ALL"]})  # type: Dict[str, str]  # line 69
Back = Fore  # type: Dict[str, str]  # line 70
MARKER = Accessor({"value": usage.MARKER_TEXT})  # type: str  # assume default text-only  # line 71
try:  # line 72
    import colorama  # line 73
    import colorama.ansitowin32  # line 73
    if colorama.ansitowin32.is_a_tty(sys.stderr):  # list of ansi codes: http://bluesock.org/~willkg/dev/ansi.html  # line 74
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
ONLY_GLOBAL_FLAGS = ["strict", "track", "picky", "compress"]  # type: List[str]  # line 115
CONFIGURABLE_FLAGS = ["useChangesCommand", "useUnicodeFont", "useColorOutput"]  # type: List[str]  # line 116
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 117
CONFIGURABLE_INTS = ["logLines", "diffLines"]  # type: List[str]  # line 118
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 119
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 120
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 121
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 122
BACKUP_SUFFIX = "_last"  # type: str  # line 123
metaFolder = ".sos"  # type: str  # line 124
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 125
metaFile = ".meta"  # type: str  # line 126
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 127
bufSize = pure.MEBI  # type: int  # line 128
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
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "useColorOutput": True, "diffLines": 2, "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth", "*.ps1"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 147
RETRY_NUM = 3  # type: int  # line 161
RETRY_WAIT = 1.5  # type: int  # line 162


# Functions
def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 166
    color = useColor[0] and color or ""  # line 167
    reset = Fore.RESET if useColor[0] and color else ""  # line 168
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 169
    sys.stdout.flush()  # PEP528 compatibility  # line 169
def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 171
    color = useColor[0] and color or ""  # line 172
    reset = Fore.RESET if useColor[0] and color else ""  # line 173
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 174
    sys.stderr.flush()  # line 174
@_coconut_tco  # line 175
def encode(s: 'str') -> 'bytes':  # line 175
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 176
@_coconut_tco  # for os->py access of reading filenames  # line 177
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 177
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 177
try:  # line 178
    import chardet  # https://github.com/chardet/chardet  # line 179
    def detectEncoding(binary: 'bytes') -> 'str':  # line 180
        return chardet.detect(binary)["encoding"]  # line 180
except:  # Guess the encoding  # line 181
    def detectEncoding(binary: 'bytes') -> 'str':  # Guess the encoding  # line 181
        ''' Fallback if chardet library missing. '''  # line 182
        try:  # line 183
            binary.decode(UTF8)  # line 183
            return UTF8  # line 183
        except UnicodeError:  # line 184
            pass  # line 184
        try:  # line 185
            binary.decode("utf_16")  # line 185
            return "utf_16"  # line 185
        except UnicodeError:  # line 186
            pass  # line 186
        try:  # line 187
            binary.decode("cp1252")  # line 187
            return "cp1252"  # line 187
        except UnicodeError:  # line 188
            pass  # line 188
        return "ascii"  # this code will never be reached, as above is an 8-bit charset that always matches  # line 189

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 191
    try:  # line 192
        return func()  # line 192
    except:  # line 193
        return default  # line 193

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 195
    try:  # line 196
        return func()  # line 196
    except Exception as E:  # line 197
        onError(E)  # line 197

def removePath(key: 'str', value: 'str') -> 'str':  # line 199
    ''' Cleanup of user-specified global file patterns, used in config. '''  # TODO improve  # line 200
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 201

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 203
    ''' Updates a dictionary by another one, returning a new copy without touching any of the passed dictionaries. '''  # line 204
    d = dict(dikt)  # type: Dict[Any, Any]  # line 205
    d.update(by)  # line 205
    return d  # line 205

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # line 207
    ''' Abstraction for opening both compressed and plain files. '''  # line 208
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # line 209

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 211
    ''' Determine EOL style from a binary string. '''  # line 212
    lf = file.count(b"\n")  # type: int  # line 213
    cr = file.count(b"\r")  # type: int  # line 214
    crlf = file.count(b"\r\n")  # type: int  # line 215
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 216
        if lf != crlf or cr != crlf:  # line 217
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 217
        return b"\r\n"  # line 218
    if lf != 0 and cr != 0:  # line 219
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 219
    if lf > cr:  # Linux/Unix  # line 220
        return b"\n"  # Linux/Unix  # line 220
    if cr > lf:  # older 8-bit machines  # line 221
        return b"\r"  # older 8-bit machines  # line 221
    return None  # no new line contained, cannot determine  # line 222

if TYPE_CHECKING:  # line 224
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 225
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 225
else:  # line 226
    def safeSplit(s, d=None):  # line 227
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 227

@_coconut_tco  # line 229
def hashStr(datas: 'str') -> 'str':  # line 229
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 229

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 231
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 231

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 233
    return lizt[index:].index(what) + index  # line 233

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 235
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 235

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 237
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 237

def Exit(message: 'str'="", code=1):  # line 239
    lines = message.split("\n")  # type: List[str]  # line 240
    printe("[", nl="")  # line 241
    printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN, nl="")  # line 242
    printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + lines[0] + ".") if lines[0] != "" else ""))  # line 243
    if len(lines) > 1:  # line 244
        printe("\n".join(lines[1:]))  # line 247
    sys.exit(code)  # line 248

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 250
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 251
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 252
        raise Exception("Cannot possibly strings pack into specified length")  # line 252
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 253
        prefix += separator + ((process)(strings.pop(0)))  # line 253
    return prefix  # line 254

def exception(E):  # line 256
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 257
    printo(str(E))  # line 258
    import traceback  # line 259
    traceback.print_exc()  # line 260
    traceback.print_stack()  # line 261

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 263
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 264
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 265
    _hash = hashlib.sha256()  # line 266
    wsize = 0  # type: int  # line 267
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 268
        Exit("Hash collision detected. Leaving repository in inconsistent state", 1)  # HINT this exits immediately  # line 269
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 270
    retry = RETRY_NUM  # type: int  # line 271
    while True:  # line 272
        try:  # line 273
            with open(encode(path), "rb") as fd:  # line 274
                while True:  # line 275
                    buffer = fd.read(bufSize)  # type: bytes  # line 276
                    _hash.update(buffer)  # line 277
                    if to:  # line 278
                        to.write(buffer)  # line 278
                    if len(buffer) < bufSize:  # line 279
                        break  # line 279
                    if indicator:  # line 280
                        indicator.getIndicator()  # line 280
                if to:  # line 281
                    to.close()  # line 282
                    wsize = os.stat(encode(saveTo[0])).st_size  # line 283
                    for remote in saveTo[1:]:  # line 284
                        tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 284
            break  # line 285
        except WinError as E:  # line 286
            retry -= 1  # line 287
            if retry == 0:  # line 288
                raise E  # line 288
            error("Cannot open %r - retrying %d more times in %.1d seconds" % (path, RETRY_WAIT))  # line 289
            time.sleep(RETRY_WAIT)  # line 290
    return (_hash.hexdigest(), wsize)  # line 291

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 293
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 294
    for k, v in map.items():  # line 295
        if k in params:  # line 295
            return v  # line 295
    return default  # line 296

@_coconut_tco  # line 298
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 298
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 298

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 300
    lines = []  # type: List[str]  # line 301
    if filename is not None:  # line 302
        with open(encode(filename), "rb") as fd:  # line 302
            content = fd.read()  # line 302
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 303
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 304
    if filename is not None:  # line 305
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 305
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 305
    elif content is not None:  # line 306
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 306
    else:  # line 307
        return (sys.getdefaultencoding(), b"\n", [])  # line 307
    if ignoreWhitespace:  # line 308
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 308
    return (encoding, eol, lines)  # line 309

if TYPE_CHECKING:  # line 311
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 312
    @_coconut_tco  # line 313
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 313
        ''' A better makedata() version. '''  # line 314
        r = _old._asdict()  # type: Dict[str, Any]  # line 315
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 316
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 317
else:  # line 318
    @_coconut_tco  # line 319
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 319
        ''' A better makedata() version. '''  # line 320
        r = _old._asdict()  # line 321
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 322
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 323

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 325
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 326
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 327
    for path, info in changes.additions.items():  # line 328
        for dpath, dinfo in changes.deletions.items():  # line 328
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 329
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 330
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 331
                break  # deletions loop, continue with next addition  # line 332
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 333

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 335
    ''' Default can be a selection from choice and allows empty input. '''  # line 336
    while True:  # line 337
        selection = input(text).strip().lower()  # line 338
        if selection != "" and selection in choices:  # line 339
            break  # line 339
        if selection == "" and default is not None:  # line 340
            selection = default  # line 340
            break  # line 340
    return selection  # line 341

def user_block_input(output: 'List[str]'):  # line 343
    ''' Side-effect appending to input list. '''  # line 344
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 345
    line = sep  # type: str  # line 345
    while True:  # line 346
        line = input("> ")  # line 347
        if line == sep:  # line 348
            break  # line 348
        output.append(line)  # writes to caller-provided list reference  # line 349

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 351
    encoding = None  # type: str  # line 352
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 352
    othr = None  # type: _coconut.typing.Sequence[str]  # line 352
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 352
    curr = None  # type: _coconut.typing.Sequence[str]  # line 352
    try:  # line 353
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 354
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 355
    except Exception as E:  # line 356
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname), E))  # line 356
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 357
        printo(line)  # from generator expression  # line 357

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 359
    ''' Merges other binary text contents 'file' (or reads file 'filename') into current text contents 'into' (or reads file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, no actual text merging
      eol: if True, will use the other file's EOL marks
      in case of replace block and INSERT strategy, the change will be added **behind** the original. HINT could be configurable
  '''  # line 374
    encoding = None  # type: str  # line 375
    othreol = None  # type: _coconut.typing.Optional[bytes]  # line 375
    othr = None  # type: _coconut.typing.Sequence[str]  # line 375
    curreol = None  # type: _coconut.typing.Optional[bytes]  # line 375
    curr = None  # type: _coconut.typing.Sequence[str]  # line 375
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 376
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 377
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 378
    except Exception as E:  # line 379
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname), E))  # line 379
    if None not in [othreol, curreol] and othreol != curreol:  # line 380
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 380
    output = list(difflib.Differ().compare(othr, curr))  # type: List[str]  # from generator expression  # line 381
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 382
    tmp = []  # type: List[str]  # block lines  # line 383
    last = " "  # type: str  # "into"-file offset for remark lines  # line 384
    no = None  # type: int  # "into"-file offset for remark lines  # line 384
    line = None  # type: str  # "into"-file offset for remark lines  # line 384
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 384
    for no, line in enumerate(output + ["X"]):  # EOF marker (difflib's output will never be "X" alone)  # line 385
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 386
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 386
            continue  # continue filling current block, no matter what type of block it is  # line 386
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 387
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 387
        if last == " ":  # block is same in both files  # line 388
            if len(tmp) > 0:  # avoid adding empty keep block  # line 389
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # avoid adding empty keep block  # line 389
        elif last == "-":  # may be a pure deletion or part of a replacement (with next block being "+")  # line 390
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 391
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # line 392
                offset += len(blocks[-2].lines)  # line 393
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 394
                blocks.pop()  # line 395
        elif last == "+":  # may be insertion or replacement (with previous - block)  # line 396
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # first, assume simple insertion, then check for replacement  # line 397
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 398
                offset += len(blocks[-1].lines)  # line 399
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 400
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 401
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 402
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 402
        last = line[0]  # line 403
        tmp[:] = [line[2:]]  # only keep current line for next block  # line 404
# TODO add code to detect moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 406
    debug("Diff blocks: " + repr(blocks))  # line 407
    if diffOnly:  # line 408
        return (blocks, nl)  # line 408

# now perform merge operations depending on detected blocks
    output[:] = []  # clean list of strings  # line 411
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 411
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 411
    selection = ""  # type: str  # clean list of strings  # line 411
    for block in blocks:  # line 412
        if block.tipe == MergeBlockType.KEEP:  # line 413
            output.extend(block.lines)  # line 413
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 414
            output.extend(block.lines)  # line 416
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 417
            if len(block.lines) == len(block.replaces.lines) == 1:  # one-liner  # line 418
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 419
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 420
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 421
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 422
                while True:  # line 423
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 424
                    if op in "tb":  # line 425
                        output.extend(block.lines)  # line 425
                    if op in "ib":  # line 426
                        output.extend(block.replaces.lines)  # line 426
                    if op == "u":  # line 427
                        user_block_input(output)  # line 427
                    if op in "tbiu":  # line 428
                        break  # line 428
            else:  # more than one line and not ask  # line 429
                if mergeOperation == MergeOperation.REMOVE:  # line 430
                    pass  # line 430
                elif mergeOperation == MergeOperation.BOTH:  # line 431
                    output.extend(block.lines)  # line 431
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 432
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 432
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 433
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 434
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 436
                if selection in "ao":  # line 437
                    if block.tipe == MergeBlockType.INSERT:  # line 438
                        add_all = "y" if selection == "a" else "n"  # line 438
                        selection = add_all  # line 438
                    else:  # REMOVE case  # line 439
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 439
                        selection = del_all  # REMOVE case  # line 439
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 440
                output.extend(block.lines)  # line 442
    debug("Merge output: " + "; ".join(output))  # line 443
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 444
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 447
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 447
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
  '''  # line 450
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 451
    blocks = []  # type: List[MergeBlock]  # line 452
    for i, line in enumerate(out):  # line 453
        if line[0] == "+":  # line 454
            if i + 1 < len(out) and out[i + 1][0] == "+":  # block will continue  # line 455
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 456
                    blocks[-1].lines.append(line[2])  # add one more character to the accumulating list  # line 457
                else:  # first + in block  # line 458
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 459
            else:  # last line of + block  # line 460
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 461
                    blocks[-1].lines.append(line[2])  # line 462
                else:  # single line  # line 463
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [line[2]], i))  # line 464
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 465
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 466
                    blocks.pop()  # line 466
        elif line[0] == "-":  # line 467
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 468
                blocks[-1].lines.append(line[2])  # line 469
            else:  # first in block  # line 470
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [line[2]], i))  # line 471
        elif line[0] == " ":  # line 472
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 473
                blocks[-1].lines.append(line[2])  # line 474
            else:  # first in block  # line 475
                blocks.append(MergeBlock(MergeBlockType.KEEP, [line[2]], i))  # line 476
        else:  # line 477
            raise Exception("Cannot parse diff line %r" % line)  # line 477
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # line 478
    if diffOnly:  # line 479
        return blocks  # line 479
    out[:] = []  # line 480
    for i, block in enumerate(blocks):  # line 481
        if block.tipe == MergeBlockType.KEEP:  # line 482
            out.extend(block.lines)  # line 482
        elif block.tipe == MergeBlockType.REPLACE:  # line 483
            if mergeOperation == MergeOperation.ASK:  # line 484
                printo(pure.ajoin("- ", othr))  # line 485
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 486
                printo("+ " + (" " * i) + block.lines[0])  # line 487
                printo(pure.ajoin("+ ", into))  # line 488
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 489
                if op in "tb":  # line 490
                    out.extend(block.lines)  # line 490
                    break  # line 490
                if op in "ib":  # line 491
                    out.extend(block.replaces.lines)  # line 491
                    break  # line 491
                if op == "m":  # line 492
                    user_block_input(out)  # line 492
                    break  # line 492
            else:  # non-interactive  # line 493
                if mergeOperation == MergeOperation.REMOVE:  # line 494
                    pass  # line 494
                elif mergeOperation == MergeOperation.BOTH:  # line 495
                    out.extend(block.lines)  # line 495
                elif mergeOperation == MergeOperation.INSERT:  # line 496
                    out.extend(list(block.replaces.lines) + list(block.lines))  # line 496
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 497
            out.extend(block.lines)  # line 497
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 498
            out.extend(block.lines)  # line 498
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 500

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 502
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 505
    debug("Detecting root folders...")  # line 506
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 507
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 508
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 509
        contents = set(os.listdir(path))  # type: Set[str]  # line 510
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 511
        choice = None  # type: _coconut.typing.Optional[str]  # line 512
        if len(vcss) > 1:  # line 513
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 514
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 515
        elif len(vcss) > 0:  # line 516
            choice = vcss[0]  # line 516
        if not vcs[0] and choice:  # memorize current repo root  # line 517
            vcs = (path, choice)  # memorize current repo root  # line 517
        new = os.path.dirname(path)  # get parent path  # line 518
        if new == path:  # avoid infinite loop  # line 519
            break  # avoid infinite loop  # line 519
        path = new  # line 520
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 521
        if vcs[0]:  # already detected vcs base and command  # line 522
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 522
        sos = path  # line 523
        while True:  # continue search for VCS base  # line 524
            contents = set(os.listdir(path))  # line 525
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 526
            choice = None  # line 527
            if len(vcss) > 1:  # line 528
                choice = SVN if SVN in vcss else vcss[0]  # line 529
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 530
            elif len(vcss) > 0:  # line 531
                choice = vcss[0]  # line 531
            if choice:  # line 532
                return (sos, path, choice)  # line 532
            new = os.path.dirname(path)  # get parent path  # line 533
            if new == path:  # no VCS folder found  # line 534
                return (sos, None, None)  # no VCS folder found  # line 534
            path = new  # line 535
    return (None, vcs[0], vcs[1])  # line 536

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 538
    index = 0  # type: int  # line 539
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 540
    while index < len(pattern):  # line 541
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 542
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 542
            continue  # line 542
        if pattern[index] in "*?":  # line 543
            count = 1  # type: int  # line 544
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 545
                count += 1  # line 545
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 546
            index += count  # line 546
            continue  # line 546
        if pattern[index:index + 2] == "[!":  # line 547
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 547
            index += len(out[-1][1])  # line 547
            continue  # line 547
        count = 1  # line 548
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 549
            count += 1  # line 549
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 550
        index += count  # line 550
    return out  # line 551

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 553
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 554
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 555
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 557
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 557
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 558
        Exit("Source and target file patterns differ in semantics")  # line 558
    return (ot, nt)  # line 559

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 561
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 562
    pairs = []  # type: List[Tuple[str, str]]  # line 563
    for filename in filenames:  # line 564
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 565
        nextliteral = 0  # type: int  # line 566
        index = 0  # type: int  # line 566
        parsedOld = []  # type: List[GlobBlock2]  # line 567
        for part in oldPattern:  # match everything in the old filename  # line 568
            if part.isLiteral:  # line 569
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 569
                index += len(part.content)  # line 569
                nextliteral += 1  # line 569
            elif part.content.startswith("?"):  # line 570
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 570
                index += len(part.content)  # line 570
            elif part.content.startswith("["):  # line 571
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 571
                index += 1  # line 571
            elif part.content == "*":  # line 572
                if nextliteral >= len(literals):  # line 573
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 573
                    break  # line 573
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 574
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 575
                index = nxt  # line 575
            else:  # line 576
                Exit("Invalid file pattern specified for move/rename")  # line 576
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 577
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 578
        nextliteral = 0  # line 579
        nextglob = 0  # type: int  # line 579
        outname = []  # type: List[str]  # line 580
        for part in newPattern:  # generate new filename  # line 581
            if part.isLiteral:  # line 582
                outname.append(literals[nextliteral].content)  # line 582
                nextliteral += 1  # line 582
            else:  # line 583
                outname.append(globs[nextglob].matches)  # line 583
                nextglob += 1  # line 583
        pairs.append((filename, "".join(outname)))  # line 584
    return pairs  # line 585

@_coconut_tco  # line 587
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 587
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 591
    if not actions:  # line 592
        return []  # line 592
    sources = None  # type: List[str]  # line 593
    targets = None  # type: List[str]  # line 593
    sources, targets = [list(l) for l in zip(*actions)]  # line 594
    last = len(actions)  # type: int  # line 595
    while last > 1:  # line 596
        clean = True  # type: bool  # line 597
        for i in range(1, last):  # line 598
            try:  # line 599
                index = targets[:i].index(sources[i])  # type: int  # line 600
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 601
                targets.insert(index, targets.pop(i))  # line 602
                clean = False  # line 603
            except:  # target not found in sources: good!  # line 604
                continue  # target not found in sources: good!  # line 604
        if clean:  # line 605
            break  # line 605
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 606
    if exitOnConflict:  # line 607
        for i in range(1, len(actions)):  # line 607
            if sources[i] in targets[:i]:  # line 607
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 607
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 608

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 610
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 611
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 612
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 613

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str]]':  # line 615
    ''' Returns (root-normalized) set of --only and --except arguments. '''  # line 616
    root = os.getcwd()  # type: str  # line 617
    onlys = []  # type: List[str]  # line 618
    excps = []  # type: List[str]  # line 618
    remotes = []  # type: List[str]  # line 618
    for keys, container in [(("--only", "--include"), onlys), (("--except", "--exclude"), excps), (("--remote",), remotes)]:  # line 619
        founds = [i for i in range(len(options)) if any([options[i].startswith(key) for key in keys])]  # assuming no more than one = in the string  # line 620
        for i in reversed(founds):  # line 621
            if "=" in options[i]:  # line 622
                container.append(options[i].split("=")[1])  # line 623
            elif i + 1 < len(options):  # in case last --only has no argument  # line 624
                container.append(options[i + 1])  # line 625
                del options[i + 1]  # line 626
            del options[i]  # reverse removal  # line 627
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(PARENT + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(PARENT + SLASH))) if excps else None, remotes)  # line 628
