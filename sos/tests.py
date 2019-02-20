#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xcf5721e3

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

import codecs  # line 4
import doctest  # line 4
import json  # line 4
import logging  # line 4
import os  # line 4
import shutil  # line 4
sys = _coconut_sys  # line 4
import time  # line 4
import traceback  # line 4
import unittest  # line 4
import uuid  # line 4
from io import BytesIO  # line 5
from io import BufferedRandom  # line 5
from io import TextIOWrapper  # line 5

if TYPE_CHECKING:  # line 7
    from typing import Any  # line 8
    from typing import Dict  # line 8
    from typing import FrozenSet  # line 8
    from typing import List  # line 8
    from typing import Set  # line 8
    from typing import Tuple  # line 8
    from typing import Union  # line 8
    mock = None  # type: Any  # to avoid mypy complaint  # line 9

try:  # Python 3  # line 11
    from unittest import mock  # Python 3  # line 11
except:  # installed via pip  # line 12
    import mock  # installed via pip  # line 12

testFolder = os.path.abspath(os.path.join(os.getcwd(), "test", "repo"))  # this needs to be set before the configr and sos imports TODO explain why  # line 14
rmteFolder = os.path.abspath(os.path.join(os.getcwd(), "test", "remote"))  # line 15
os.environ["TEST"] = testFolder  # needed to mock configr library calls in sos  # line 16

import configr  # line 18
import sos  # import of package, not file (!)  # line 19

sos.defaults["defaultbranch"] = "trunk"  # because sos.main() is never called  # line 21
sos.defaults["useChangesCommand"] = True  # line 22
sos.defaults["useUnicodeFont"] = False  # line 23
sos.defaults["useColorOutput"] = True  # line 24


def determineFilesystemTimeResolution() -> 'float':  # line 27
    name = str(uuid.uuid4())  # type: str  # line 28
    with open(name, "w") as fd:  # create temporary file  # line 29
        fd.write("x")  # create temporary file  # line 29
    mt = os.stat(sos.encode(name)).st_mtime  # type: float  # get current timestamp  # line 30
    while os.stat(sos.encode(name)).st_mtime == mt:  # wait until timestamp modified  # line 31
        time.sleep(0.05)  # to avoid 0.00s bugs (came up some time for unknown reasons)  # line 32
        with open(name, "w") as fd:  # line 33
            fd.write("x")  # line 33
    mt, start, _count = os.stat(sos.encode(name)).st_mtime, time.time(), 0  # line 34
    while os.stat(sos.encode(name)).st_mtime == mt:  # now cound and measure time until modified again  # line 35
        time.sleep(0.05)  # line 36
        _count += 1  # line 37
        with open(name, "w") as fd:  # line 38
            fd.write("x")  # line 38
    os.unlink(name)  # line 39
    fsprecision = round(time.time() - start, 2)  # type: float  # line 40
    print("File system timestamp precision is %s%.2fs; wrote to the file %d times during that time" % ("probably even higher than " if fsprecision == 0.05 else "", fsprecision, _count))  # line 41
    return fsprecision  # line 42


FS_PRECISION = determineFilesystemTimeResolution() * 1.55  # line 45

def sync():  # line 47
    try:  # only Linux  if sys.version_info[:2] >= (3, 3):  # line 48
        os.sync()  # only Linux  if sys.version_info[:2] >= (3, 3):  # line 48
    except:  # Windows testing on AppVeyor  # line 49
        time.sleep(FS_PRECISION)  # Windows testing on AppVeyor  # line 49


@_coconut_tco  # line 52
def debugTestRunner(post_mortem=None):  # line 52
    ''' Unittest runner doing post mortem debugging on failing tests. '''  # line 53
    import pdb  # line 54
    if post_mortem is None:  # line 55
        post_mortem = pdb.post_mortem  # line 55
    class DebugTestResult(unittest.TextTestResult):  # line 56
        def addError(_, test, err):  # called before tearDown()  # line 57
            traceback.print_exception(*err)  # line 58
            post_mortem(err[2])  # line 59
            super(DebugTestResult, _).addError(test, err)  # line 60
        def addFailure(_, test, err):  # line 61
            traceback.print_exception(*err)  # line 62
            post_mortem(err[2])  # line 63
            super(DebugTestResult, _).addFailure(test, err)  # line 64
    return _coconut_tail_call(unittest.TextTestRunner, resultclass=DebugTestResult)  # line 65

@_coconut_tco  # line 67
def wrapChannels(func: '_coconut.typing.Callable[..., Any]') -> 'str':  # line 67
    ''' Wrap function call to capture and return strings emitted on stdout and stderr. '''  # line 68
    oldv, oldso, oldse = sys.argv, sys.stdout, sys.stderr  # line 69
    class StreamCopyWrapper(TextIOWrapper):  # line 70
        def __init__(_):  # line 71
            TextIOWrapper.__init__(_, BufferedRandom(BytesIO(b"")), encoding=sos.UTF8)  # line 71
        def write(_, bla):  # line 72
            oldso.write(bla)  # line 72
            TextIOWrapper.write(_, bla)  # line 72
    buf = StreamCopyWrapper()  # line 73
    handler = logging.StreamHandler(buf)  # TODO doesn't seem to be captured  # line 74
    sys.stdout = sys.stderr = buf  # assignment goes right to left  # line 75
    logging.getLogger().addHandler(handler)  # line 76
    try:  # capture output into buf  # line 77
        func()  # capture output into buf  # line 77
    except Exception as E:  # line 78
        buf.write(str(E) + "\n")  # line 78
        traceback.print_exc(file=buf)  # line 78
    except SystemExit as F:  # line 79
        buf.write("EXIT CODE %s" % F.code + "\n")  # line 79
        traceback.print_exc(file=buf)  # line 79
    logging.getLogger().removeHandler(handler)  # line 80
    sys.argv, sys.stdout, sys.stderr = oldv, oldso, oldse  # TODO when run using pythonw.exe and/or no console, these could be None  # line 81
    buf.seek(0)  # line 82
    return _coconut_tail_call(buf.read)  # line 83

def mockInput(datas: '_coconut.typing.Sequence[str]', func: '_coconut.typing.Callable[[], Any]') -> 'Any':  # line 85
    try:  # via python sos/tests.py  # line 86
        with mock.patch("sos._utility.input", side_effect=datas):  # line 87
            return func()  # line 87
    except:  # via setup.py  # line 88
        with mock.patch("sos.utility.input", side_effect=datas):  # line 89
            return func()  # line 89

def setRepoFlag(name: 'str', value: 'Any', toConfig: 'bool'=False):  # line 91
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 92
        flags, branches, config = json.loads(fd.read())  # line 92
    if not toConfig:  # line 93
        flags[name] = value  # line 93
    else:  # line 94
        config[name] = value  # line 94
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 95
        fd.write(json.dumps((flags, branches, config)))  # line 95

def checkRepoFlag(name: 'str', flag: '_coconut.typing.Optional[bool]'=None, value: '_coconut.typing.Optional[Any]'=None) -> 'bool':  # line 97
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 98
        flags, branches, config = json.loads(fd.read())  # line 98
    return (name in flags and flags[name] == flag) if flag is not None else (name in config and config[name] == value)  # line 99


class Tests(unittest.TestCase):  # line 102
    ''' Entire test suite. '''  # line 103

    def setUp(_):  # line 105
        sos.Metadata.singleton = None  # line 106
        for folder in (testFolder, rmteFolder):  # line 107
            for entry in os.listdir(folder):  # cannot reliably remove testFolder on Windows when using TortoiseSVN as VCS  # line 108
                resource = os.path.join(folder, entry)  # type: str  # line 109
                shutil.rmtree(sos.encode(resource)) if os.path.isdir(sos.encode(resource)) else os.unlink(sos.encode(resource))  # line 110
        os.chdir(testFolder)  # line 111

# Assertion helpers
    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]', only: 'bool'=False):  # line 114
        for w in what:  # line 115
            _.assertIn(w, where)  # line 115
        if only:  # line 116
            _.assertEqual(len(what), len(where))  # line 116

    def assertAllNotIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]'):  # line 118
        for w in what:  # line 119
            _.assertNotIn(w, where)  # line 119

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 121
        for w in where:  # line 122
            _.assertIn(what, w)  # line 122

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 124
        _.assertTrue(any((what in w for w in where)))  # line 124

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 126
        _.assertFalse(any((what in w for w in where)))  # line 126


# More helpers
    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None):  # line 130
        if prefix and not os.path.exists(prefix):  # line 131
            os.makedirs(prefix)  # line 131
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 132
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 132
        sync()  # line 133

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 135
        sync()  # line 136
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 137
            return False  # line 137
        if expectedContents is None:  # line 138
            return True  # line 138
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 139
            return fd.read() == expectedContents  # line 139

    def remoteIsSame(_):  # line 141
        sync()  # line 142
        for dirpath, dirnames, filenames in os.walk(os.path.join(testFolder, sos.metaFolder)):  # line 143
            rmtePath = os.path.normpath(os.path.join(rmteFolder, sos.metaFolder, os.path.relpath(dirpath, os.path.join(testFolder, sos.metaFolder))))  # type: str  # line 144
            others = os.listdir(rmtePath)  # type: List[str]  # line 145
            try:  # line 146
                _.assertAllIn(dirnames, others)  # line 146
                _.assertAllIn(others, dirnames + filenames)  # line 146
            except AssertionError as E:  # line 147
                raise AssertionError("Mismatch vs. remote: %r\n%r in %s" % (dirnames, others, dirpath)) from None  # line 147
            try:  # line 148
                _.assertAllIn(filenames, others)  # line 148
                _.assertAllIn(others, dirnames + filenames)  # line 148
            except AssertionError as E:  # line 149
                raise AssertionError("Mismatch vs. remote: %r\n% in %sr" % (filenames, others, dirpath)) from None  # line 149


# Unit tests
    def testAccessor(_):  # line 153
        a = sos.Accessor({"a": 1})  # type: Accessor  # line 154
        _.assertEqual((1, 1), (a["a"], a.a))  # line 155

    def testCharDet(_):  # line 157
        _.assertEqual("ascii", sos.detectEncoding(b"abc"))  # line 158
        _.assertEqual("UTF-8-SIG", sos.detectEncoding("abc".encode("utf-8-sig")))  # with BOM  # line 159
        _.assertEqual(sos.UTF8, sos.detectEncoding("abcüöä".encode("utf-8")))  # without BOM  # line 160

    def testTimeString(_):  # line 162
        _.assertEqual('1500 ms', sos.pure.timeString(1500))  # line 163
        _.assertEqual('1.5 seconds', sos.pure.timeString(1501))  # line 164
        _.assertEqual('23.0 hours', sos.pure.timeString(1000 * 60 * 60 * 23))  # line 165
        _.assertEqual('8.0 days', sos.pure.timeString(1000 * 60 * 60 * 24 * 8))  # line 166
        _.assertEqual('1.3 weeks', sos.pure.timeString(1000 * 60 * 60 * 24 * 9))  # line 167

    def testUnzip(_):  # line 169
        a = zip([1, 2, 3], ["a", "b", "c"])  # type: _coconut.typing.Sequence[Tuple[int, str]]  # line 170
        i = None  # type: Tuple[int]  # line 171
        c = None  # type: Tuple[str]  # line 171
        i, c = sos.unzip(a)  # line 172
        _.assertEqual((1, 2, 3), i)  # line 173
        _.assertEqual(("a", "b", "c"), c)  # line 174

    def testUsage(_):  # line 176
        out = wrapChannels(lambda _=None: sos.usage.usage("commit"))  # line 177
        _.assertAllIn(["commit [<message>]  Create a new revision", "Arguments:", "Options:"], out)  # line 178

    def testIndexing(_):  # line 180
        m = sos.Metadata()  # line 181
        m.commits = {}  # line 182
        _.assertEqual(1, m.correctNegativeIndexing(1))  # line 183
        _.assertEqual(9999999999999999, m.correctNegativeIndexing(9999999999999999))  # line 184
        _.assertEqual(0, m.correctNegativeIndexing(0))  # zero always returns zero, even no commits present  # line 185
        try:  # line 186
            m.correctNegativeIndexing(-1)  # line 186
            _.fail()  # line 186
        except SystemExit as E:  # line 187
            _.assertEqual(1, E.code)  # line 187
        m.commits = {0: sos.CommitInfo(0, 0), 1: sos.CommitInfo(1, 0)}  # line 188
        _.assertEqual(1, m.correctNegativeIndexing(-1))  # zero always returns zero, even no commits present  # line 189
        _.assertEqual(0, m.correctNegativeIndexing(-2))  # zero always returns zero, even no commits present  # line 190
        try:  # line 191
            m.correctNegativeIndexing(-3)  # line 191
            _.fail()  # line 191
        except SystemExit as E:  # line 192
            _.assertEqual(1, E.code)  # line 192

    def testRestoreFile(_):  # line 194
        m = sos.Metadata()  # line 195
        os.makedirs(sos.revisionFolder(0, 0))  # line 196
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 197
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 198
        _.assertTrue(_.existsFile("restored", b""))  # line 199

    def testGetAnyOfmap(_):  # line 201
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 202
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 203

    def testAjoin(_):  # line 205
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 206
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 207

    def testFindChanges(_):  # line 209
        m = sos.Metadata(os.getcwd())  # line 210
        try:  # line 211
            sos.config(["set", "texttype", "*"])  # line 211
        except SystemExit as E:  # line 212
            _.assertEqual(0, E.code)  # line 212
        try:  # will be stripped from leading paths anyway  # line 213
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 213
        except SystemExit as E:  # line 214
            _.assertEqual(0, E.code)  # line 214
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 215
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 216
            os.unlink(file)  # remove configuration file  # line 216
        _.createFile(9, b"")  # line 217
        _.createFile(1, "1")  # line 218
        m.createBranch(0)  # line 219
        _.assertEqual(2, len(m.paths))  # line 220
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 221
        _.createFile(1, "2")  # modify existing file  # line 222
        _.createFile(2, "2")  # add another file  # line 223
        m.loadCommit(0, 0)  # line 224
        changes, msg = m.findChanges()  # detect time skew  # line 225
        _.assertEqual(1, len(changes.additions))  # line 226
        _.assertEqual(0, len(changes.deletions))  # line 227
        _.assertEqual(1, len(changes.modifications))  # line 228
        _.assertEqual(0, len(changes.moves))  # line 229
        m.paths.update(changes.additions)  # line 230
        m.paths.update(changes.modifications)  # line 231
        _.createFile(2, "12")  # modify file again  # line 232
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 233
        _.assertEqual(0, len(changes.additions))  # line 234
        _.assertEqual(0, len(changes.deletions))  # line 235
        _.assertEqual(1, len(changes.modifications))  # line 236
        _.assertEqual(0, len(changes.moves))  # line 237
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 238
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 239
# TODO test moves

    def testDumpSorting(_):  # line 242
        m = sos.Metadata()  # type: Metadata  # line 243
        _.createFile(1)  # line 244
        sos.offline()  # line 245
        _.createFile(2)  # line 246
        _.createFile(3)  # line 247
        sos.commit()  # line 248
        _.createFile(4)  # line 249
        _.createFile(5)  # line 250
        sos.commit()  # line 251
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # type: List[str]  # line 252
        _.assertTrue(out.index("b0%sr2" % os.sep) > out.index("b0%sr1" % os.sep))  # line 253
        _.assertTrue(out.index("b0%sr1" % os.sep) > out.index("b0%sr0" % os.sep))  # line 254

    def testFitStrings(_):  # line 256
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 257
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 258
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 259
    def testMoves(_):  # line 260
        _.createFile(1, "1")  # line 261
        _.createFile(2, "2", "sub")  # line 262
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 263
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 264
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 265
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 266
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 267
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 268
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # line 269
        _.assertIn("MOV ..%sfile2  <-  file2" % os.sep, out)  # no ./ for relative OS-specific paths  # line 270
        _.assertIn("MOV file1  <-  ..%sfile1" % os.sep, out)  # line 271
        out = wrapChannels(lambda _=None: sos.commit())  # line 272
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 273
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 274
        _.assertAllIn(["Created new revision r01", "summing 628 bytes in 2 files (88.22% SOS overhead)"], out)  # TODO why is this not captured?  # line 275

    def testPatternPaths(_):  # line 277
        sos.offline(options=["--track"])  # line 278
        os.mkdir("sub")  # line 279
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 280
        out = wrapChannels(lambda _=None: sos.add(["sub"], ["sub/file?"]))  # type: str  # line 281
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", os.path.abspath("sub")], out)  # line 282
        sos.commit("test")  # should pick up sub/file1 pattern  # line 283
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 284
        _.createFile(1)  # line 285
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 286
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 286
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 286
        except:  # line 287
            pass  # line 287

    def testNoArgs(_):  # line 289
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 290

    def testAutoMetadataUpgrade(_):  # line 292
        sos.offline()  # line 293
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 294
            repo, branches, config = json.load(fd)  # line 294
        repo["version"] = None  # lower than any pip version  # line 295
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 296
        del repo["format"]  # simulate pre-1.3.5  # line 297
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 298
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 298
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # type: str  # line 299
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 300

    def testFastBranching(_):  # line 302
        _.createFile(1)  # line 303
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict", "--verbose"]))  # type: str  # b0/r0 = ./file1  # line 304
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 305
        _.createFile(2)  # line 306
        os.unlink("file1")  # line 307
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 308
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 309
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 310
        _.createFile(3)  # line 311
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 312
        _.assertAllIn([sos.metaFile, sos.metaBack, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 313
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 314
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 315
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 316
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 317
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 318
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 321
        now = time.time()  # type: float  # line 322
        _.createFile(1)  # line 323
        sync()  # line 324
        sos.offline(options=["--strict"])  # line 325
        _.createFile(1, "abc")  # modify contents  # line 326
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 327
        sync()  # line 328
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 329
        _.assertIn("<older than previously committed>", out)  # line 330
        out = wrapChannels(lambda _=None: sos.commit())  # line 331
        _.assertIn("<older than previously committed>", out)  # line 332

    def testGetParentBranch(_):  # line 334
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 335
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 336
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 337
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 338
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 339

    def testTokenizeGlobPattern(_):  # line 341
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 342
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 343
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 344
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 345
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 346
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 347

    def testTokenizeGlobPatterns(_):  # line 349
        try:  # because number of literal strings differs  # line 350
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 350
            _.fail()  # because number of literal strings differs  # line 350
        except:  # line 351
            pass  # line 351
        try:  # because glob patterns differ  # line 352
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 352
            _.fail()  # because glob patterns differ  # line 352
        except:  # line 353
            pass  # line 353
        try:  # glob patterns differ, regardless of position  # line 354
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 354
            _.fail()  # glob patterns differ, regardless of position  # line 354
        except:  # line 355
            pass  # line 355
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 356
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 357
        try:  # succeeds, because glob patterns match (differ only in position)  # line 358
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 358
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 358
        except:  # line 359
            pass  # line 359

    def testConvertGlobFiles(_):  # line 361
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 362
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 363

    def testFolderRemove(_):  # line 365
        m = sos.Metadata(os.getcwd())  # line 366
        _.createFile(1)  # line 367
        _.createFile("a", prefix="sub")  # line 368
        sos.offline()  # line 369
        _.createFile(2)  # line 370
        os.unlink("sub" + os.sep + "a")  # line 371
        os.rmdir("sub")  # line 372
        changes = sos.changes()  # TODO #254 replace by output check  # line 373
        _.assertEqual(1, len(changes.additions))  # line 374
        _.assertEqual(0, len(changes.modifications))  # line 375
        _.assertEqual(1, len(changes.deletions))  # line 376
        _.createFile("a", prefix="sub")  # line 377
        changes = sos.changes()  # line 378
        _.assertEqual(0, len(changes.deletions))  # line 379

    def testSwitchConflict(_):  # line 381
        sos.offline(options=["--strict"])  # (r0)  # line 382
        _.createFile(1)  # line 383
        sos.commit()  # add file (r1)  # line 384
        os.unlink("file1")  # line 385
        sos.commit()  # remove (r2)  # line 386
        _.createFile(1, "something else")  # line 387
        sos.commit()  # (r3)  # line 388
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 389
        _.existsFile(1, "x" * 10)  # line 390
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 391
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 392
        sos.switch("/1")  # add file1 back  # line 393
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 394
        _.existsFile(1, "something else")  # line 395

    def testComputeSequentialPathSet(_):  # line 397
        os.makedirs(sos.revisionFolder(0, 0))  # line 398
        os.makedirs(sos.revisionFolder(0, 1))  # line 399
        os.makedirs(sos.revisionFolder(0, 2))  # line 400
        os.makedirs(sos.revisionFolder(0, 3))  # line 401
        os.makedirs(sos.revisionFolder(0, 4))  # line 402
        m = sos.Metadata(os.getcwd())  # line 403
        m.branch = 0  # line 404
        m.commit = 2  # line 405
        m.saveBranches()  # line 406
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 407
        m.saveCommit(0, 0)  # initial  # line 408
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 409
        m.saveCommit(0, 1)  # mod  # line 410
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 411
        m.saveCommit(0, 2)  # add  # line 412
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 413
        m.saveCommit(0, 3)  # del  # line 414
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 415
        m.saveCommit(0, 4)  # readd  # line 416
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 417
        m.saveBranch(0)  # line 418
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 419
        m.saveBranches()  # line 420
        m.computeSequentialPathSet(0, 4)  # line 421
        _.assertEqual(2, len(m.paths))  # line 422

    def testParseRevisionString(_):  # line 424
        m = sos.Metadata(os.getcwd())  # line 425
        m.branch = 1  # line 426
        m.commits = {0: 0, 1: 1, 2: 2}  # line 427
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 428
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 429
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 430
        _.assertEqual((None, None), m.parseRevisionString(""))  # line 431
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 432
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 433
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 434

    def testOfflineEmpty(_):  # line 436
        os.mkdir("." + os.sep + sos.metaFolder)  # line 437
        try:  # line 438
            sos.offline("trunk")  # line 438
            _.fail()  # line 438
        except SystemExit as E:  # line 439
            _.assertEqual(1, E.code)  # line 439
        os.rmdir("." + os.sep + sos.metaFolder)  # line 440
        sos.offline("test")  # line 441
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 442
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 443
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 444
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 445
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 446
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 447

    def testOfflineWithFiles(_):  # line 449
        _.createFile(1, "x" * 100)  # line 450
        _.createFile(2)  # line 451
        sos.offline("test")  # line 452
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 453
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 454
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 455
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 456
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 457
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 458
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 459

    def testBranch(_):  # line 461
        _.createFile(1, "x" * 100)  # line 462
        _.createFile(2)  # line 463
        sos.offline("test")  # b0/r0  # line 464
        sos.branch("other")  # b1/r0  # line 465
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 466
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 467
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 469
        _.createFile(1, "z")  # modify file  # line 471
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 472
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 473
        _.createFile(3, "z")  # line 475
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 476
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 477
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 482
        _.createFile(1, "x" * 100)  # line 483
        _.createFile(2)  # line 484
        sos.offline("test")  # line 485
        changes = sos.changes()  # line 486
        _.assertEqual(0, len(changes.additions))  # line 487
        _.assertEqual(0, len(changes.deletions))  # line 488
        _.assertEqual(0, len(changes.modifications))  # line 489
        _.createFile(1, "z")  # size change  # line 490
        changes = sos.changes()  # line 491
        _.assertEqual(0, len(changes.additions))  # line 492
        _.assertEqual(0, len(changes.deletions))  # line 493
        _.assertEqual(1, len(changes.modifications))  # line 494
        sos.commit("message")  # line 495
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 496
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 497
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 498
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 499
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 500
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 501
        os.unlink("file2")  # line 502
        changes = sos.changes()  # line 503
        _.assertEqual(0, len(changes.additions))  # line 504
        _.assertEqual(1, len(changes.deletions))  # line 505
        _.assertEqual(1, len(changes.modifications))  # line 506
        sos.commit("modified")  # line 507
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 508
        try:  # expecting Exit due to no changes  # line 509
            sos.commit("nothing")  # expecting Exit due to no changes  # line 509
            _.fail()  # expecting Exit due to no changes  # line 509
        except:  # line 510
            pass  # line 510

    def testGetBranch(_):  # line 512
        m = sos.Metadata(os.getcwd())  # line 513
        m.branch = 1  # current branch  # line 514
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 515
        _.assertEqual(27, m.getBranchByName(27))  # line 516
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 517
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 518
        _.assertIsNone(m.getBranchByName("unknown"))  # line 519
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 520
        _.assertEqual(13, m.getRevisionByName("13"))  # line 521
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 522
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 523

    def testTagging(_):  # line 525
        m = sos.Metadata(os.getcwd())  # line 526
        sos.offline()  # line 527
        _.createFile(111)  # line 528
        sos.commit("tag", ["--tag"])  # line 529
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # type: str  # line 530
        _.assertTrue(any(("|tag" in line and line.endswith("|%sTAG%s" % (sos.Fore.MAGENTA, sos.Fore.RESET)) for line in out)))  # line 531
        _.createFile(2)  # line 532
        try:  # line 533
            sos.commit("tag")  # line 533
            _.fail()  # line 533
        except:  # line 534
            pass  # line 534
        sos.commit("tag-2", ["--tag"])  # line 535
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 536
        _.assertIn("TAG tag", out)  # line 537

    def testSwitch(_):  # line 539
        try:  # line 540
            shutil.rmtree(os.path.join(rmteFolder, sos.metaFolder))  # line 540
        except:  # line 541
            pass  # line 541
        _.createFile(1, "x" * 100)  # line 542
        _.createFile(2, "y")  # line 543
        sos.offline("test", remotes=[rmteFolder])  # file1-2  in initial branch commit  # line 544
        sos.branch("second")  # file1-2  switch, having same files  # line 545
        sos.switch("0")  # no change, switch back, no problem  # line 546
        sos.switch("second")  # no change  # switch back, no problem  # line 547
        _.createFile(3, "y")  # generate a file  # line 548
        try:  # uncommited changes detected  # line 549
            sos.switch("test")  # uncommited changes detected  # line 549
            _.fail()  # uncommited changes detected  # line 549
        except SystemExit as E:  # line 550
            _.assertEqual(1, E.code)  # line 550
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 551
        sos.changes()  # line 552
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 553
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 554
        _.createFile("XXX")  # line 555
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 556
        _.assertIn("File tree has changes", out)  # line 557
        _.assertNotIn("File tree is unchanged", out)  # line 558
        _.assertIn("  * b0   'test'", out)  # line 559
        _.assertIn("    b1 'second'", out)  # line 560
        _.assertIn("modified", out)  # one branch has commits  # line 561
        _.assertIn("in sync", out)  # the other doesn't  # line 562
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 563
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 564
        _.assertAllIn(["Metadata format", "Content checking:    %ssize & timestamp" % sos.Fore.BLUE, "Data compression:    %sdeactivated" % sos.Fore.BLUE, "Repository mode:     %ssimple" % sos.Fore.GREEN, "Number of branches:  2"], out)  # line 565
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 566
        _.createFile(4, "xy")  # generate a file  # line 567
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 568
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 569
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 570
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 571
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 572
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 573
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 574
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 575
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 576
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 577
        _.assertNotIn("Creating backup", out)  # line 578
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 579
        _.assertIn("Dumping revisions", out)  # line 580
        _.assertNotIn("Creating backup", out)  # line 581
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 582
        _.assertAllIn(["Creating backup"], out)  # line 583
        _.assertIn("Dumping revisions", out)  # line 584
        sos.verbose.pop()  # line 585
        _.remoteIsSame()  # line 586
        os.chdir(rmteFolder)  # line 587
        try:  # line 588
            sos.status()  # line 588
        except SystemExit as E:  # line 589
            _.assertEqual(1, E.code)  # line 589

    def testAutoDetectVCS(_):  # line 591
        os.mkdir(".git")  # line 592
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 593
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 594
            meta = fd.read()  # line 594
        _.assertTrue("\"master\"" in meta)  # line 595
        os.rmdir(".git")  # line 596

    def testNoRemotes(_):  # line 598
        sos.offline(remotes=[rmteFolder])  # line 599
        _.createFile(1)  # line 600
        sos.commit(options=["--no-remotes"])  # line 601
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")))  # line 602
        _.assertFalse(_.existsFile(os.path.join(sos.branchFolder(0, rmteFolder), "r%d" % 1, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")))  # line 603

    def testUpdate(_):  # line 605
        sos.offline("trunk")  # create initial branch b0/r0  # line 606
        _.createFile(1, "x" * 100)  # line 607
        sos.commit("second")  # create b0/r1  # line 608

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 610
        _.assertFalse(_.existsFile(1))  # line 611

        sos.update("/1")  # recreate file1  # line 613
        _.assertTrue(_.existsFile(1))  # line 614

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 616
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 617
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 618
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 619

        sos.update("/1")  # do nothing, as nothing has changed  # line 621
        _.assertTrue(_.existsFile(1))  # line 622

        _.createFile(2, "y" * 100)  # line 624
#    out:str = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 627
        _.assertTrue(_.existsFile(2))  # line 628
        sos.update("trunk", ["--add"])  # only add stuff  # line 629
        _.assertTrue(_.existsFile(2))  # line 630
        sos.update("trunk")  # nothing to do  # line 631
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 632

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 634
        _.createFile(10, theirs)  # line 635
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 636
        _.createFile(11, mine)  # line 637
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 638
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 639

    def testUpdate2(_):  # line 641
        _.createFile("test.txt", "x" * 10)  # line 642
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 643
        sync()  # line 644
        sos.branch("mod")  # line 645
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 646
        sos.commit("mod")  # create b0/r1  # line 647
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 648
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 649
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 650
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 651
        _.createFile("test.txt", "x" * 10)  # line 652
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 653
        sync()  # line 654
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 655
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 656
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 657
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 658
        sync()  # line 659
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 660
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 661

    def testIsTextType(_):  # line 663
        m = sos.Metadata(".")  # line 664
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 665
        m.c.bintype = ["*.md.confluence"]  # line 666
        _.assertTrue(m.isTextType("ab.txt"))  # line 667
        _.assertTrue(m.isTextType("./ab.txt"))  # line 668
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 669
        _.assertFalse(m.isTextType("bc/ab."))  # line 670
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 671
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 672
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 673
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 674

    def testEolDet(_):  # line 676
        ''' Check correct end-of-line detection. '''  # line 677
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 678
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 679
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 680
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 681
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 682
        _.assertIsNone(sos.eoldet(b""))  # line 683
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 684

    def testMergeClassic(_):  # line 686
        _.createFile(1, contents=b"abcdefg")  # line 687
        b = b"iabcxeg"  # type: bytes  # line 688
        _.assertEqual.__self__.maxDiff = None  # to get a full diff  # line 689
        out = wrapChannels(lambda _=None: sos.mergeClassic(b, "file1", "from", "to", 24523234, 1))  # type: str  # line 690
        try:  # line 691
            _.assertAllIn(["*** from\tThu Jan  1 07:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # line 691
        except:  # differing local time on CI system TODO make this better  # line 692
            _.assertAllIn(["*** from\tThu Jan  1 06:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # differing local time on CI system TODO make this better  # line 692

    def testMerge(_):  # line 694
        ''' Check merge results depending on user options. '''  # line 695
        a = b"a\nb\ncc\nd"  # type: bytes  # line 696
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 697
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 698
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 699
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 700
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 701
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 702
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 703
        a = b"a\nb\ncc\nd"  # line 704
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 705
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 706
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 707
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 708
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 710
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 711
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 713
        b = b"a\nc\ne"  # line 714
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 715
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 716
        a = b"a\nb\ne"  # intra-line merge  # line 717
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 718
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 719
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 720
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 721
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 722
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 723

    def testMergeEol(_):  # line 725
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 726
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 727
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 728
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 729
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 730

    def testPickyMode(_):  # line 732
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 733
        sos.offline("trunk", None, ["--picky"])  # line 734
        changes = sos.changes()  # line 735
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 736
        out = wrapChannels(lambda _=None: sos.add(["."], ["./file?"], options=["--force", "--relative"]))  # type: str  # line 737
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", "'.'"], out)  # line 738
        _.createFile(1, "aa")  # line 739
        sos.commit("First")  # add one file  # line 740
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 741
        _.createFile(2, "b")  # line 742
        try:  # add nothing, because picky  # line 743
            sos.commit("Second")  # add nothing, because picky  # line 743
        except:  # line 744
            pass  # line 744
        sos.add(["."], ["./file?"])  # line 745
        sos.commit("Third")  # line 746
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 747
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 748
        _.assertIn("    r0", out)  # line 749
        sys.argv.extend(["-n", "2"])  # We cannot use the opions array for named argument options  # line 750
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 751
        sys.argv.pop()  # line 752
        sys.argv.pop()  # line 752
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 753
        _.assertIn("    r1", out)  # line 754
        _.assertIn("  * r2", out)  # line 755
        try:  # line 756
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 756
        except SystemExit as E:  # line 757
            _.assertEqual(0, E.code)  # line 757
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 758
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 759
        _.assertNotIn("    r1", out)  # line 760
        _.assertIn("  * r2", out)  # line 761
        _.createFile(3, prefix="sub")  # line 762
        sos.add(["sub"], ["sub/file?"])  # line 763
        changes = sos.changes()  # line 764
        _.assertEqual(1, len(changes.additions))  # line 765
        _.assertTrue("sub/file3" in changes.additions)  # line 766

    def testTrackedSubfolder(_):  # line 768
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 769
        os.mkdir("." + os.sep + "sub")  # line 770
        sos.offline("trunk", None, ["--track"])  # line 771
        _.createFile(1, "x")  # line 772
        _.createFile(1, "x", prefix="sub")  # line 773
        sos.add(["."], ["./file?"])  # add glob pattern to track  # line 774
        sos.commit("First")  # line 775
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 776
        sos.add(["."], ["sub/file?"])  # add glob pattern to track  # line 777
        sos.commit("Second")  # one new file + meta  # line 778
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 779
        os.unlink("file1")  # remove from basefolder  # line 780
        _.createFile(2, "y")  # line 781
        sos.remove(["."], ["sub/file?"])  # line 782
        try:  # TODO check more textual details here  # line 783
            sos.remove(["."], ["sub/bla"])  # TODO check more textual details here  # line 783
            _.fail("Expected exit")  # TODO check more textual details here  # line 783
        except SystemExit as E:  # line 784
            _.assertEqual(1, E.code)  # line 784
        sos.commit("Third")  # line 785
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 786
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 789
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 794
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 795
        _.createFile(1)  # line 796
        _.createFile("a123a")  # untracked file "a123a"  # line 797
        sos.add(["."], ["./file?"])  # add glob tracking pattern  # line 798
        sos.commit("second")  # versions "file1"  # line 799
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 800
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 801
        _.assertTrue(any(("|" in o and "./file?" in o for o in out.split("\n"))))  # line 802

        _.createFile(2)  # untracked file "file2"  # line 804
        sos.commit("third")  # versions "file2"  # line 805
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 806

        os.mkdir("." + os.sep + "sub")  # line 808
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 809
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 810
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 811

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 813
        sos.remove(["."], ["./file?"])  # remove tracking pattern, but don't touch previously created and versioned files  # line 814
        sos.add([".", "."], ["./a*a", "./a*?"])  # add tracking pattern  # line 815
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 816
        _.assertEqual(0, len(changes.modifications))  # line 817
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 818
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 819

        sos.commit("Second_2")  # line 821
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 822
        _.existsFile(1, b"x" * 10)  # line 823
        _.existsFile(2, b"x" * 10)  # line 824

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 826
        _.existsFile(1, b"x" * 10)  # line 827
        _.existsFile("a123a", b"x" * 10)  # line 828

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 830
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 831
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 832

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 834
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 835
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 836
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 837
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 838
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 839
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 840
# TODO test switch --meta

    def testLsTracked(_):  # line 843
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 844
        _.createFile(1)  # line 845
        _.createFile("foo")  # line 846
        sos.add(["."], ["./file*"])  # capture one file  # line 847
        sos.ls()  # line 848
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # type: str  # line 849
        _.assertInAny("TRK file1  (file*)", out)  # line 850
        _.assertNotInAny("... file1  (file*)", out)  # line 851
        _.assertInAny("    foo", out)  # line 852
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 853
        _.assertInAny("TRK file*", out)  # line 854
        _.createFile("a", prefix="sub")  # line 855
        sos.add(["sub"], ["sub/a"])  # line 856
        sos.ls("sub")  # line 857
        _.assertInAny("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 858

    def testLineMerge(_):  # line 860
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # integrate all of other into -> mine  # line 861
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 862
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # keep old and insert new  # line 863
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # remove old and no change of new  # line 864

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 866
        _.createFile(1)  # line 867
        sos.offline("master", options=["--force"])  # line 868
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # type: str  # line 869
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 870
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 871
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 872
        _.createFile(2)  # line 873
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 874
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 875
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 876
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 877

    def testLocalConfig(_):  # line 879
        sos.offline("bla", options=[])  # line 880
        try:  # line 881
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 881
        except SystemExit as E:  # line 882
            _.assertEqual(0, E.code)  # line 882
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 883

    def testConfigVariations(_):  # line 885
        def makeRepo():  # line 886
            try:  # line 887
                os.unlink("file1")  # line 887
            except:  # line 888
                pass  # line 888
            sos.offline("master", options=["--force"])  # line 889
            _.createFile(1)  # line 890
            sos.commit("Added file1")  # line 891
        try:  # line 892
            sos.config(["set", "strict", "on"])  # line 892
        except SystemExit as E:  # line 893
            _.assertEqual(0, E.code)  # line 893
        makeRepo()  # line 894
        _.assertTrue(checkRepoFlag("strict", True))  # line 895
        try:  # line 896
            sos.config(["set", "strict", "off"])  # line 896
        except SystemExit as E:  # line 897
            _.assertEqual(0, E.code)  # line 897
        makeRepo()  # line 898
        _.assertTrue(checkRepoFlag("strict", False))  # line 899
        try:  # line 900
            sos.config(["set", "strict", "yes"])  # line 900
        except SystemExit as E:  # line 901
            _.assertEqual(0, E.code)  # line 901
        makeRepo()  # line 902
        _.assertTrue(checkRepoFlag("strict", True))  # line 903
        try:  # line 904
            sos.config(["set", "strict", "no"])  # line 904
        except SystemExit as E:  # line 905
            _.assertEqual(0, E.code)  # line 905
        makeRepo()  # line 906
        _.assertTrue(checkRepoFlag("strict", False))  # line 907
        try:  # line 908
            sos.config(["set", "strict", "1"])  # line 908
        except SystemExit as E:  # line 909
            _.assertEqual(0, E.code)  # line 909
        makeRepo()  # line 910
        _.assertTrue(checkRepoFlag("strict", True))  # line 911
        try:  # line 912
            sos.config(["set", "strict", "0"])  # line 912
        except SystemExit as E:  # line 913
            _.assertEqual(0, E.code)  # line 913
        makeRepo()  # line 914
        _.assertTrue(checkRepoFlag("strict", False))  # line 915
        try:  # line 916
            sos.config(["set", "strict", "true"])  # line 916
        except SystemExit as E:  # line 917
            _.assertEqual(0, E.code)  # line 917
        makeRepo()  # line 918
        _.assertTrue(checkRepoFlag("strict", True))  # line 919
        try:  # line 920
            sos.config(["set", "strict", "false"])  # line 920
        except SystemExit as E:  # line 921
            _.assertEqual(0, E.code)  # line 921
        makeRepo()  # line 922
        _.assertTrue(checkRepoFlag("strict", False))  # line 923
        try:  # line 924
            sos.config(["set", "strict", "enable"])  # line 924
        except SystemExit as E:  # line 925
            _.assertEqual(0, E.code)  # line 925
        makeRepo()  # line 926
        _.assertTrue(checkRepoFlag("strict", True))  # line 927
        try:  # line 928
            sos.config(["set", "strict", "disable"])  # line 928
        except SystemExit as E:  # line 929
            _.assertEqual(0, E.code)  # line 929
        makeRepo()  # line 930
        _.assertTrue(checkRepoFlag("strict", False))  # line 931
        try:  # line 932
            sos.config(["set", "strict", "enabled"])  # line 932
        except SystemExit as E:  # line 933
            _.assertEqual(0, E.code)  # line 933
        makeRepo()  # line 934
        _.assertTrue(checkRepoFlag("strict", True))  # line 935
        try:  # line 936
            sos.config(["set", "strict", "disabled"])  # line 936
        except SystemExit as E:  # line 937
            _.assertEqual(0, E.code)  # line 937
        makeRepo()  # line 938
        _.assertTrue(checkRepoFlag("strict", False))  # line 939
        try:  # line 940
            sos.config(["set", "strict", "nope"])  # line 940
            _.fail()  # line 940
        except SystemExit as E:  # line 941
            _.assertEqual(1, E.code)  # line 941

    def testLsSimple(_):  # line 943
        _.createFile(1)  # line 944
        _.createFile("foo")  # line 945
        _.createFile("ign1")  # line 946
        _.createFile("ign2")  # line 947
        _.createFile("bar", prefix="sub")  # line 948
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 949
        try:  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 950
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 950
        except SystemExit as E:  # line 951
            _.assertEqual(0, E.code)  # line 951
        try:  # additional ignore pattern  # line 952
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 952
        except SystemExit as E:  # line 953
            _.assertEqual(0, E.code)  # line 953
        try:  # define a list of ignore patterns  # line 954
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 954
        except SystemExit as E:  # line 955
            _.assertEqual(0, E.code)  # line 955
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # type: str  # line 956
        _.assertAllIn(["             ignores", "[global]", "['ign1', 'ign2']"], out)  # line 957
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 958
        _.assertAllIn(["             ignores", "[global]", "['ign1', 'ign2']"], out)  # line 959
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 960
        _.assertInAny('    file1', out)  # line 961
        _.assertInAny('    ign1', out)  # line 962
        _.assertInAny('    ign2', out)  # line 963
        _.assertNotIn('DIR sub', out)  # line 964
        _.assertNotIn('    bar', out)  # line 965
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 966
        _.assertIn('DIR sub', out)  # line 967
        _.assertIn('    bar', out)  # line 968
        try:  # line 969
            sos.config(["rm", "foo", "bar"])  # line 969
            _.fail()  # line 969
        except SystemExit as E:  # line 970
            _.assertEqual(1, E.code)  # line 970
        try:  # line 971
            sos.config(["rm", "ignores", "foo"])  # line 971
            _.fail()  # line 971
        except SystemExit as E:  # line 972
            _.assertEqual(1, E.code)  # line 972
        try:  # line 973
            sos.config(["rm", "ignores", "ign1"])  # line 973
        except SystemExit as E:  # line 974
            _.assertEqual(0, E.code)  # line 974
        try:  # remove ignore pattern  # line 975
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 975
        except SystemExit as E:  # line 976
            _.assertEqual(0, E.code)  # line 976
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 977
        _.assertInAny('    ign1', out)  # line 978
        _.assertInAny('IGN ign2', out)  # line 979
        _.assertNotInAny('    ign2', out)  # line 980

    def testWhitelist(_):  # line 982
# TODO test same for simple mode
        _.createFile(1)  # line 984
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 985
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 986
        sos.add(["."], ["./file*"])  # add tracking pattern for "file1"  # line 987
        sos.commit(options=["--force"])  # attempt to commit the file  # line 988
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 989
        try:  # Exit because dirty  # line 990
            sos.online()  # Exit because dirty  # line 990
            _.fail()  # Exit because dirty  # line 990
        except:  # exception expected  # line 991
            pass  # exception expected  # line 991
        _.createFile("x2")  # add another change  # line 992
        sos.add(["."], ["./x?"])  # add tracking pattern for "file1"  # line 993
        try:  # force beyond dirty flag check  # line 994
            sos.online(["--force"])  # force beyond dirty flag check  # line 994
            _.fail()  # force beyond dirty flag check  # line 994
        except:  # line 995
            pass  # line 995
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 996
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 997

        _.createFile(1)  # line 999
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 1000
        sos.offline("xx", None, ["--track"])  # line 1001
        sos.add(["."], ["./file*"])  # line 1002
        sos.commit()  # should NOT ask for force here  # line 1003
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 1004

    def testRemove(_):  # line 1006
        _.createFile(1, "x" * 100)  # line 1007
        sos.offline("trunk")  # line 1008
        try:  # line 1009
            sos.destroy("trunk")  # line 1009
            _fail()  # line 1009
        except:  # line 1010
            pass  # line 1010
        _.createFile(2, "y" * 10)  # line 1011
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 1012
        sos.destroy("trunk")  # line 1013
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 1014
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 1015
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 1016
        sos.branch("next")  # line 1017
        _.createFile(3, "y" * 10)  # make a change  # line 1018
        sos.destroy("added", "--force")  # should succeed  # line 1019

    def testFastBranchingOnEmptyHistory(_):  # line 1021
        ''' Test fast branching without revisions and with them. '''  # line 1022
        sos.offline(options=["--strict", "--compress"])  # b0  # line 1023
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 1024
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 1025
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 1026
        sos.destroy("2")  # line 1027
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 1028
        _.assertIn("b0 'trunk' @", out)  # line 1029
        _.assertIn("b1         @", out)  # line 1030
        _.assertIn("b3         @", out)  # line 1031
        _.assertNotIn("b2         @", out)  # line 1032
        sos.branch("", "")  # non-fast branching of b4  # line 1033
        _.createFile(1)  # line 1034
        _.createFile(2)  # line 1035
        sos.commit("")  # line 1036
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 1037
        sos.destroy("4")  # line 1038
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 1039
        _.assertIn("b0 'trunk' @", out)  # line 1040
        _.assertIn("b1         @", out)  # line 1041
        _.assertIn("b3         @", out)  # line 1042
        _.assertIn("b5         @", out)  # line 1043
        _.assertNotIn("b2         @", out)  # line 1044
        _.assertNotIn("b4         @", out)  # line 1045
# TODO add more files and branch again

    def testUsage(_):  # line 1048
        try:  # TODO expect sys.exit(0)  # line 1049
            sos.usage()  # TODO expect sys.exit(0)  # line 1049
            _.fail()  # TODO expect sys.exit(0)  # line 1049
        except:  # line 1050
            pass  # line 1050
        try:  # TODO expect sys.exit(0)  # line 1051
            sos.usage("help")  # TODO expect sys.exit(0)  # line 1051
            _.fail()  # TODO expect sys.exit(0)  # line 1051
        except:  # line 1052
            pass  # line 1052
        try:  # TODO expect sys.exit(0)  # line 1053
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 1053
            _.fail()  # TODO expect sys.exit(0)  # line 1053
        except:  # line 1054
            pass  # line 1054
        try:  # line 1055
            sos.usage(version=True)  # line 1055
            _.fail()  # line 1055
        except:  # line 1056
            pass  # line 1056
        try:  # line 1057
            sos.usage(version=True)  # line 1057
            _.fail()  # line 1057
        except:  # line 1058
            pass  # line 1058

    def testOnlyExcept(_):  # line 1060
        ''' Test blacklist glob rules. '''  # line 1061
        sos.offline(options=["--track"])  # line 1062
        _.createFile("a.1")  # line 1063
        _.createFile("a.2")  # line 1064
        _.createFile("b.1")  # line 1065
        _.createFile("b.2")  # line 1066
        sos.add(["."], ["./a.?"])  # line 1067
        sos.add(["."], ["./?.1"], negative=True)  # line 1068
        out = wrapChannels(lambda _=None: sos.commit())  # type: str  # line 1069
        _.assertIn("ADD ./a.2", out)  # line 1070
        _.assertNotIn("ADD ./a.1", out)  # line 1071
        _.assertNotIn("ADD ./b.1", out)  # line 1072
        _.assertNotIn("ADD ./b.2", out)  # line 1073

    def testOnly(_):  # line 1075
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",)), ["bla"], ["blo"]), tuple([r if i < 2 else [os.path.basename(x) for x in r] for i, r in enumerate(sos.parseArgumentOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--remote", "bla", "--exclude-remote", "blo", "--only"]))]))  # line 1076
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1077
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1078
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1079
        sos.offline(options=["--track", "--strict"])  # line 1080
        _.createFile(1)  # line 1081
        _.createFile(2)  # line 1082
        sos.add(["."], ["./file1"])  # line 1083
        sos.add(["."], ["./file2"])  # line 1084
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1085
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1086
        sos.commit()  # adds also file2  # line 1087
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1088
        _.createFile(1, "cc")  # modify both files  # line 1089
        _.createFile(2, "dd")  # line 1090
        try:  # line 1091
            sos.config(["set", "texttype", "file2"])  # line 1091
        except SystemExit as E:  # line 1092
            _.assertEqual(0, E.code)  # line 1092
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1093
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1094
        _.assertTrue("./file2" in changes.modifications)  # line 1095
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # line 1096
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1097
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1098
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # line 1099

    def testEmptyFiles(_):  # line 1101
        sos.offline()  # line 1102
        _.createFile(1, "")  # empty file  # line 1103
        sos.commit()  # line 1104
        changes = sos.changes()  # line 1105
        _.assertEqual(0, len(changes.additions) + len(changes.modifications) + len(changes.deletions))  # line 1106

        setRepoFlag("strict", True)  # line 1108
        changes = sos.changes()  # line 1109
        _.assertEqual(1, len(changes.modifications))  # because hash was set to None in simple mode  # line 1110
        sos.commit()  # commit now with hash computation  # line 1111
        setRepoFlag("strict", False)  # line 1112

        time.sleep(FS_PRECISION)  # line 1114
        _.createFile(1, "")  # touch file  # line 1115
        changes = sos.changes()  # line 1116
        _.assertEqual(1, len(changes.modifications))  # since modified timestamp  # line 1117

    def testDiff(_):  # line 1119
        try:  # manually mark this file as "textual"  # line 1120
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1120
        except SystemExit as E:  # line 1121
            _.assertEqual(0, E.code)  # line 1121
        sos.offline(options=["--strict"])  # line 1122
        _.createFile(1)  # line 1123
        _.createFile(2)  # line 1124
        sos.commit()  # line 1125
        _.createFile(1, "sdfsdgfsdf")  # line 1126
        _.createFile(2, "12343")  # line 1127
        sos.commit()  # line 1128
        _.createFile(1, "foobar")  # line 1129
        _.createFile(3)  # line 1130
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # type: str  # compare with r1 (second counting from last which is r2)  # line 1131
        _.assertIn("ADD ./file3", out)  # line 1132
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "old 0 |xxxxxxxxxx|", "now 0 |foobar|"], out)  # line 1133
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1134

    def testReorderRenameActions(_):  # line 1136
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1137
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1138
        try:  # line 1139
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1139
            _.fail()  # line 1139
        except:  # line 1140
            pass  # line 1140

    def testPublish(_):  # line 1142
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1143

    def testColorFlag(_):  # line 1145
        sos.offline()  # line 1146
        _.createFile(1)  # line 1147
#    setRepoFlag("useColorOutput", False, toConfig = True)
#    sos.Metadata.singleton = None  # for new slurp of configuration
        sos.enableColor(False, force=True)  # line 1150
        sos.verbose[:] = [None]  # set "true"  # line 1151
        out = wrapChannels(lambda _=None: sos.changes()).replace("\r\n", "\n").split("\n")  # type: List[str]  # line 1152
        _.assertTrue(any((line.startswith(sos.usage.MARKER_TEXT + "Changes of file tree") for line in out)))  # line 1153
#    setRepoFlag("useColorOutput", True,  toConfig = True)
#    sos.Metadata.singleton = None
        sos.enableColor(True, force=True)  # line 1156
        out = wrapChannels(lambda _=None: sos.changes()).replace("\r\n", "\n").split("\n")  # line 1157
        _.assertTrue(any((line.startswith((sos.usage.MARKER_TEXT if sys.platform == "win32" else sos.MARKER_COLOR) + "Changes of file tree") for line in out)))  # because it may start with a color code  # line 1158
        sos.verbose.pop()  # line 1159

    def testMove(_):  # line 1161
        ''' Move primarily modifies tracking patterns and moves files around accordingly. '''  # line 1162
        sos.offline(options=["--strict", "--track"])  # line 1163
        _.createFile(1)  # line 1164
        sos.add(["."], ["./file?"])  # line 1165
# assert error when source folder is missing
        out = wrapChannels(lambda _=None: sos.move("sub", "sub/file?", ".", "./?file"))  # type: str  # line 1167
        _.assertIn("Source folder doesn't exist", out)  # line 1168
        _.assertIn("EXIT CODE 1", out)  # line 1169
# if target folder missing: create it and move matching files into it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1171
        _.assertTrue(os.path.exists("sub"))  # line 1172
        _.assertTrue(os.path.exists("sub/file1"))  # line 1173
        _.assertFalse(os.path.exists("file1"))  # line 1174
# test move back to previous location, plus rename the file
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1176
        _.assertTrue(os.path.exists("1file"))  # line 1177
        _.assertFalse(os.path.exists("sub/file1"))  # line 1178
# assert error when nothing matches source pattern
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*"))  # line 1180
        _.assertIn("No files match the specified file pattern", out)  # line 1181
        _.assertIn("EXIT CODE", out)  # line 1182
        sos.add(["."], ["./*"])  # add catch-all tracking pattern to root folder  # line 1183
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*", options=["--force"]))  # line 1184
        _.assertIn("  './*' matches 3 files", out)  # line 1185
        _.assertIn("EXIT CODE", out)  # line 1186
# test rename no conflict
        _.createFile(1)  # line 1188
        _.createFile(2)  # line 1189
        _.createFile(3)  # line 1190
        sos.add(["."], ["./file*"])  # line 1191
        sos.remove(["."], ["./*"])  # line 1192
        try:  # define an ignore pattern  # line 1193
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1193
        except SystemExit as E:  # line 1194
            _.assertEqual(0, E.code)  # line 1194
        try:  # line 1195
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1195
        except SystemExit as E:  # line 1196
            _.assertEqual(0, E.code)  # line 1196
        sos.move(".", "./file*", ".", "./fi*le")  # should only move not ignored files files  # line 1197
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1198
        _.assertTrue(all((not os.path.exists("file%d" % i) for i in range(1, 4))))  # line 1199
        _.assertFalse(os.path.exists("fi4le"))  # line 1200
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1202
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(["."], ["./?file"])  # untrack pattern, which was renamed before  # line 1206
        sos.add(["."], ["./?a?b"], ["--force"])  # line 1207
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1208
        _.createFile("1a2b")  # should not be tracked  # line 1209
        _.createFile("a1b2")  # should be tracked  # line 1210
        sos.commit()  # line 1211
        _.assertEqual(5, len(os.listdir(sos.revisionFolder(0, 1))))  # meta, a1b2, fi[1-3]le  # line 1212
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1213
        _.createFile("1a1b1")  # line 1214
        _.createFile("1a1b2")  # line 1215
        sos.add(["."], ["./?a?b*"])  # line 1216
# test target pattern exists
        out = wrapChannels(lambda _=None: sos.move(".", "./?a?b*", ".", "./z?z?"))  # line 1218
        _.assertIn("not unique", out)  # line 1219
# TODO only rename if actually any files are versioned? or simply what is currently alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1223
        _.createFile(1)  # line 1224
        _.createFile(3)  # line 1225
        _.createFile(5)  # line 1226
        sos.offline()  # branch 0: only file1  # line 1227
        sos.branch()  # line 1228
        os.unlink("file1")  # line 1229
        os.unlink("file3")  # line 1230
        os.unlink("file5")  # line 1231
        _.createFile(2)  # line 1232
        _.createFile(4)  # line 1233
        _.createFile(6)  # line 1234
        sos.commit()  # branch 1: only file2  # line 1235
        sos.switch("0/")  # line 1236
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1237
        _.assertFalse(_.existsFile(1))  # line 1238
        _.assertFalse(_.existsFile(3))  # line 1239
        _.assertFalse(_.existsFile(5))  # line 1240
        _.assertTrue(_.existsFile(2))  # line 1241
        _.assertTrue(_.existsFile(4))  # line 1242
        _.assertTrue(_.existsFile(6))  # line 1243

    def testMoveDetection(_):  # line 1245
        _.createFile(1, "bla")  # line 1246
        sos.offline()  # line 1247
        os.mkdir("sub1")  # line 1248
        os.mkdir("sub2")  # line 1249
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1250
        shutil.move("file1", "sub2")  # line 1251
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 1252
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1253
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1254
        sos.commit("Moved the file")  # line 1255
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1259

    def testHashCollision(_):  # line 1261
        old = sos.Metadata.findChanges  # line 1262
        @_coconut_tco  # line 1263
        def patched(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False, remotes: 'List[str]'=[]) -> 'Tuple[sos.ChangeSet, _coconut.typing.Optional[str]]':  # line 1263
            import collections  # used only in this method  # line 1264
            write = branch is not None and revision is not None  # line 1265
            if write:  # line 1266
                try:  # line 1267
                    os.makedirs(sos.encode(sos.revisionFolder(branch, revision, base=_.root)))  # line 1267
                except FileExistsError:  # HINT "try" only necessary for hash collision *test code* (!)  # line 1268
                    pass  # HINT "try" only necessary for hash collision *test code* (!)  # line 1268
            return _coconut_tail_call(old, _, branch, revision, checkContent, inverse, considerOnly, dontConsider, progress)  # line 1269
        sos.Metadata.findChanges = patched  # monkey-patch  # line 1270
        sos.offline()  # line 1271
        _.createFile(1)  # line 1272
        os.mkdir(sos.revisionFolder(0, 1))  # line 1273
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # hashed file name for not-yet-committed file1  # line 1274
        _.createFile(1)  # line 1275
        try:  # line 1276
            sos.commit()  # line 1276
            _.fail("Expected system exit due to hash collision detection")  # line 1276
        except SystemExit as E:  # HINT exit is implemented in utility.hashFile  # line 1277
            _.assertEqual(1, E.code)  # HINT exit is implemented in utility.hashFile  # line 1277
        sos.Metadata.findChanges = old  # revert monkey patch  # line 1278

    def testFindBase(_):  # line 1280
        old = os.getcwd()  # line 1281
        try:  # line 1282
            os.mkdir("." + os.sep + ".git")  # line 1283
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1284
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1285
            os.chdir("a" + os.sep + "b")  # line 1286
            s, vcs, cmd = sos.findSosVcsBase()  # line 1287
            _.assertIsNotNone(s)  # line 1288
            _.assertIsNotNone(vcs)  # line 1289
            _.assertEqual("git", cmd)  # line 1290
        finally:  # line 1291
            os.chdir(old)  # line 1291

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise

def load_tests(loader, tests, ignore):  # line 1301
    ''' Python unittest by-convention test definition. '''  # line 1302
    tests.addTests(doctest.DocTestSuite("sos.pure", optionflags=doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.NORMALIZE_WHITESPACE))  # line 1303
    tests.addTests(doctest.DocTestSuite("sos.utility", optionflags=doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.NORMALIZE_WHITESPACE))  # line 1304
    return tests  # line 1305


if __name__ == '__main__':  # line 1308
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1309
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1310
