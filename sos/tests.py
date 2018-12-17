#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x6ee11e54

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

import codecs  # line 4
import collections  # line 4
import enum  # line 4
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

try:  # line 7
    if TYPE_CHECKING:  # true only during compilation/mypy run  # line 8
        from typing import Any  # line 9
        from typing import Dict  # line 9
        from typing import FrozenSet  # line 9
        from typing import List  # line 9
        from typing import Set  # line 9
        from typing import Tuple  # line 9
        from typing import Union  # line 9
        mock = None  # type: Any  # to avoid mypy complaint  # line 10
except:  # line 11
    pass  # line 11

try:  # Python 3  # line 13
    from unittest import mock  # Python 3  # line 13
except:  # installed via pip  # line 14
    import mock  # installed via pip  # line 14

testFolder = os.path.abspath(os.path.join(os.getcwd(), "test", "repo"))  # this needs to be set before the configr and sos imports TODO explain why  # line 16
rmteFolder = os.path.abspath(os.path.join(os.getcwd(), "test", "remote"))  # line 17
os.environ["TEST"] = testFolder  # needed to mock configr library calls in sos  # line 18

import configr  # line 20
import sos  # import of package, not file  # line 21

sos.defaults["defaultbranch"] = "trunk"  # because sos.main() is never called  # line 23
sos.defaults["useChangesCommand"] = True  # line 24
sos.defaults["useUnicodeFont"] = False  # line 25
sos.defaults["useColorOutput"] = True  # line 26


def determineFilesystemTimeResolution() -> 'float':  # line 29
    name = str(uuid.uuid4())  # type: str  # line 30
    with open(name, "w") as fd:  # create temporary file  # line 31
        fd.write("x")  # create temporary file  # line 31
    mt = os.stat(sos.encode(name)).st_mtime  # type: float  # get current timestamp  # line 32
    while os.stat(sos.encode(name)).st_mtime == mt:  # wait until timestamp modified  # line 33
        time.sleep(0.05)  # to avoid 0.00s bugs (came up some time for unknown reasons)  # line 34
        with open(name, "w") as fd:  # line 35
            fd.write("x")  # line 35
    mt, start, _count = os.stat(sos.encode(name)).st_mtime, time.time(), 0  # line 36
    while os.stat(sos.encode(name)).st_mtime == mt:  # now cound and measure time until modified again  # line 37
        time.sleep(0.05)  # line 38
        _count += 1  # line 39
        with open(name, "w") as fd:  # line 40
            fd.write("x")  # line 40
    os.unlink(name)  # line 41
    fsprecision = round(time.time() - start, 2)  # type: float  # line 42
    print("File system timestamp precision is %s%.2fs; wrote to the file %d times during that time" % ("probably even higher than " if fsprecision == 0.05 else "", fsprecision, _count))  # line 43
    return fsprecision  # line 44


FS_PRECISION = determineFilesystemTimeResolution() * 1.55  # line 47

def sync():  # line 49
    try:  # only Linux  if sys.version_info[:2] >= (3, 3):  # line 50
        os.sync()  # only Linux  if sys.version_info[:2] >= (3, 3):  # line 50
    except:  # Windows testing on AppVeyor  # line 51
        time.sleep(FS_PRECISION)  # Windows testing on AppVeyor  # line 51


@_coconut_tco  # line 54
def debugTestRunner(post_mortem=None):  # line 54
    ''' Unittest runner doing post mortem debugging on failing tests. '''  # line 55
    import pdb  # line 56
    if post_mortem is None:  # line 57
        post_mortem = pdb.post_mortem  # line 57
    class DebugTestResult(unittest.TextTestResult):  # line 58
        def addError(_, test, err):  # called before tearDown()  # line 59
            traceback.print_exception(*err)  # line 60
            post_mortem(err[2])  # line 61
            super(DebugTestResult, _).addError(test, err)  # line 62
        def addFailure(_, test, err):  # line 63
            traceback.print_exception(*err)  # line 64
            post_mortem(err[2])  # line 65
            super(DebugTestResult, _).addFailure(test, err)  # line 66
    return _coconut_tail_call(unittest.TextTestRunner, resultclass=DebugTestResult)  # line 67

@_coconut_tco  # line 69
def wrapChannels(func: '_coconut.typing.Callable[..., Any]') -> 'str':  # line 69
    ''' Wrap function call to capture and return strings emitted on stdout and stderr. '''  # line 70
    oldv, oldso, oldse = sys.argv, sys.stdout, sys.stderr  # line 71
    class StreamCopyWrapper(TextIOWrapper):  # line 72
        def __init__(_):  # line 73
            TextIOWrapper.__init__(_, BufferedRandom(BytesIO(b"")), encoding=sos.UTF8)  # line 73
        def write(_, bla):  # line 74
            oldso.write(bla)  # line 74
            TextIOWrapper.write(_, bla)  # line 74
    buf = StreamCopyWrapper()  # line 75
    handler = logging.StreamHandler(buf)  # TODO doesn't seem to be captured  # line 76
    sys.stdout = sys.stderr = buf  # assignment goes right to left  # line 77
    logging.getLogger().addHandler(handler)  # line 78
    try:  # capture output into buf  # line 79
        func()  # capture output into buf  # line 79
    except Exception as E:  # line 80
        buf.write(str(E) + "\n")  # line 80
        traceback.print_exc(file=buf)  # line 80
    except SystemExit as F:  # line 81
        buf.write("EXIT CODE %s" % F.code + "\n")  # line 81
        traceback.print_exc(file=buf)  # line 81
    logging.getLogger().removeHandler(handler)  # line 82
    sys.argv, sys.stdout, sys.stderr = oldv, oldso, oldse  # TODO when run using pythonw.exe and/or no console, these could be None  # line 83
    buf.seek(0)  # line 84
    return _coconut_tail_call(buf.read)  # line 85

def mockInput(datas: '_coconut.typing.Sequence[str]', func: '_coconut.typing.Callable[[], Any]') -> 'Any':  # line 87
    try:  # via python sos/tests.py  # line 88
        with mock.patch("sos._utility.input", side_effect=datas):  # line 89
            return func()  # line 89
    except:  # via setup.py  # line 90
        with mock.patch("sos.utility.input", side_effect=datas):  # line 91
            return func()  # line 91

def setRepoFlag(name: 'str', value: 'Any', toConfig: 'bool'=False):  # line 93
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 94
        flags, branches, config = json.loads(fd.read())  # line 94
    if not toConfig:  # line 95
        flags[name] = value  # line 95
    else:  # line 96
        config[name] = value  # line 96
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 97
        fd.write(json.dumps((flags, branches, config)))  # line 97

def checkRepoFlag(name: 'str', flag: '_coconut.typing.Optional[bool]'=None, value: '_coconut.typing.Optional[Any]'=None) -> 'bool':  # line 99
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 100
        flags, branches, config = json.loads(fd.read())  # line 100
    return (name in flags and flags[name] == flag) if flag is not None else (name in config and config[name] == value)  # line 101


class Tests(unittest.TestCase):  # line 104
    ''' Entire test suite. '''  # line 105

    def setUp(_):  # line 107
        sos.Metadata.singleton = None  # line 108
        for folder in (testFolder, rmteFolder):  # line 109
            for entry in os.listdir(folder):  # cannot reliably remove testFolder on Windows when using TortoiseSVN as VCS  # line 110
                resource = os.path.join(folder, entry)  # type: str  # line 111
                shutil.rmtree(sos.encode(resource)) if os.path.isdir(sos.encode(resource)) else os.unlink(sos.encode(resource))  # line 112
        os.chdir(testFolder)  # line 113

# Assertion helpers
    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]', only: 'bool'=False):  # line 116
        for w in what:  # line 117
            _.assertIn(w, where)  # line 117
        if only:  # line 118
            _.assertEqual(len(what), len(where))  # line 118

    def assertAllNotIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]'):  # line 120
        for w in what:  # line 121
            _.assertNotIn(w, where)  # line 121

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 123
        for w in where:  # line 124
            _.assertIn(what, w)  # line 124

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 126
        _.assertTrue(any((what in w for w in where)))  # line 126

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 128
        _.assertFalse(any((what in w for w in where)))  # line 128


# More helpers
    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None):  # line 132
        if prefix and not os.path.exists(prefix):  # line 133
            os.makedirs(prefix)  # line 133
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 134
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 134
        sync()  # line 135

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 137
        sync()  # line 138
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 139
            return False  # line 139
        if expectedContents is None:  # line 140
            return True  # line 140
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 141
            return fd.read() == expectedContents  # line 141

    def remoteIsSame(_):  # line 143
        sync()  # line 144
        for dirpath, dirnames, filenames in os.walk(os.path.join(testFolder, sos.metaFolder)):  # line 145
            rmtePath = os.path.normpath(os.path.join(rmteFolder, sos.metaFolder, os.path.relpath(dirpath, os.path.join(testFolder, sos.metaFolder))))  # type: str  # line 146
            others = os.listdir(rmtePath)  # type: List[str]  # line 147
            try:  # line 148
                _.assertAllIn(dirnames, others)  # line 148
                _.assertAllIn(others, dirnames + filenames)  # line 148
            except AssertionError as E:  # line 149
                raise AssertionError("Mismatch vs. remote: %r\n%r in %s" % (dirnames, others, dirpath)) from None  # line 149
            try:  # line 150
                _.assertAllIn(filenames, others)  # line 150
                _.assertAllIn(others, dirnames + filenames)  # line 150
            except AssertionError as E:  # line 151
                raise AssertionError("Mismatch vs. remote: %r\n% in %sr" % (filenames, others, dirpath)) from None  # line 151


# Unit tests
    def testAccessor(_):  # line 155
        a = sos.Accessor({"a": 1})  # type: Accessor  # line 156
        _.assertEqual((1, 1), (a["a"], a.a))  # line 157

    def testCharDet(_):  # line 159
        _.assertEqual("ascii", sos.detectEncoding(b"abc"))  # line 160
        _.assertEqual("UTF-8-SIG", sos.detectEncoding("abc".encode("utf-8-sig")))  # with BOM  # line 161
        _.assertEqual(sos.UTF8, sos.detectEncoding("abcüöä".encode("utf-8")))  # without BOM  # line 162

    def testTimeString(_):  # line 164
        _.assertEqual('1500 ms', sos.pure.timeString(1500))  # line 165
        _.assertEqual('1.5 seconds', sos.pure.timeString(1501))  # line 166
        _.assertEqual('23.0 hours', sos.pure.timeString(1000 * 60 * 60 * 23))  # line 167
        _.assertEqual('8.0 days', sos.pure.timeString(1000 * 60 * 60 * 24 * 8))  # line 168
        _.assertEqual('1.3 weeks', sos.pure.timeString(1000 * 60 * 60 * 24 * 9))  # line 169

    def testUnzip(_):  # line 171
        a = zip([1, 2, 3], ["a", "b", "c"])  # type: _coconut.typing.Sequence[Tuple[int, str]]  # line 172
        i = None  # type: Tuple[int]  # line 173
        c = None  # type: Tuple[str]  # line 173
        i, c = sos.unzip(a)  # line 174
        _.assertEqual((1, 2, 3), i)  # line 175
        _.assertEqual(("a", "b", "c"), c)  # line 176

    def testUsage(_):  # line 178
        out = wrapChannels(lambda _=None: sos.usage.usage("commit"))  # line 179
        _.assertAllIn(["commit [<message>]  Create a new revision", "Arguments:", "Options:"], out)  # line 180

    def testIndexing(_):  # line 182
        m = sos.Metadata()  # line 183
        m.commits = {}  # line 184
        _.assertEqual(1, m.correctNegativeIndexing(1))  # line 185
        _.assertEqual(9999999999999999, m.correctNegativeIndexing(9999999999999999))  # line 186
        _.assertEqual(0, m.correctNegativeIndexing(0))  # zero always returns zero, even no commits present  # line 187
        try:  # line 188
            m.correctNegativeIndexing(-1)  # line 188
            _.fail()  # line 188
        except SystemExit as E:  # line 189
            _.assertEqual(1, E.code)  # line 189
        m.commits = {0: sos.CommitInfo(0, 0), 1: sos.CommitInfo(1, 0)}  # line 190
        _.assertEqual(1, m.correctNegativeIndexing(-1))  # zero always returns zero, even no commits present  # line 191
        _.assertEqual(0, m.correctNegativeIndexing(-2))  # zero always returns zero, even no commits present  # line 192
        try:  # line 193
            m.correctNegativeIndexing(-3)  # line 193
            _.fail()  # line 193
        except SystemExit as E:  # line 194
            _.assertEqual(1, E.code)  # line 194

    def testRestoreFile(_):  # line 196
        m = sos.Metadata()  # line 197
        os.makedirs(sos.revisionFolder(0, 0))  # line 198
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 199
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 200
        _.assertTrue(_.existsFile("restored", b""))  # line 201

    def testGetAnyOfmap(_):  # line 203
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 204
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 205

    def testAjoin(_):  # line 207
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 208
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 209

    def testFindChanges(_):  # line 211
        m = sos.Metadata(os.getcwd())  # line 212
        try:  # line 213
            sos.config(["set", "texttype", "*"])  # line 213
        except SystemExit as E:  # line 214
            _.assertEqual(0, E.code)  # line 214
        try:  # will be stripped from leading paths anyway  # line 215
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 215
        except SystemExit as E:  # line 216
            _.assertEqual(0, E.code)  # line 216
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 217
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 218
            os.unlink(file)  # remove configuration file  # line 218
        _.createFile(9, b"")  # line 219
        _.createFile(1, "1")  # line 220
        m.createBranch(0)  # line 221
        _.assertEqual(2, len(m.paths))  # line 222
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 223
        _.createFile(1, "2")  # modify existing file  # line 224
        _.createFile(2, "2")  # add another file  # line 225
        m.loadCommit(0, 0)  # line 226
        changes, msg = m.findChanges()  # detect time skew  # line 227
        _.assertEqual(1, len(changes.additions))  # line 228
        _.assertEqual(0, len(changes.deletions))  # line 229
        _.assertEqual(1, len(changes.modifications))  # line 230
        _.assertEqual(0, len(changes.moves))  # line 231
        m.paths.update(changes.additions)  # line 232
        m.paths.update(changes.modifications)  # line 233
        _.createFile(2, "12")  # modify file again  # line 234
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 235
        _.assertEqual(0, len(changes.additions))  # line 236
        _.assertEqual(0, len(changes.deletions))  # line 237
        _.assertEqual(1, len(changes.modifications))  # line 238
        _.assertEqual(0, len(changes.moves))  # line 239
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 240
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 241
# TODO test moves

    def testDumpSorting(_):  # line 244
        m = sos.Metadata()  # type: Metadata  # line 245
        _.createFile(1)  # line 246
        sos.offline()  # line 247
        _.createFile(2)  # line 248
        _.createFile(3)  # line 249
        sos.commit()  # line 250
        _.createFile(4)  # line 251
        _.createFile(5)  # line 252
        sos.commit()  # line 253
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # type: List[str]  # line 254
        _.assertTrue(out.index("b0%sr2" % os.sep) > out.index("b0%sr1" % os.sep))  # line 255
        _.assertTrue(out.index("b0%sr1" % os.sep) > out.index("b0%sr0" % os.sep))  # line 256

    def testFitStrings(_):  # line 258
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 259
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 260
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 261
    def testMoves(_):  # line 262
        _.createFile(1, "1")  # line 263
        _.createFile(2, "2", "sub")  # line 264
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 265
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 266
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 267
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 268
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 269
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 270
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # line 271
        _.assertIn("MOV ..%sfile2  <-  file2" % os.sep, out)  # no ./ for relative OS-specific paths  # line 272
        _.assertIn("MOV file1  <-  ..%sfile1" % os.sep, out)  # line 273
        out = wrapChannels(lambda _=None: sos.commit())  # line 274
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 275
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 276
        _.assertAllIn(["Created new revision r01", "summing 628 bytes in 2 files (88.22% SOS overhead)"], out)  # TODO why is this not captured?  # line 277

    def testPatternPaths(_):  # line 279
        sos.offline(options=["--track"])  # line 280
        os.mkdir("sub")  # line 281
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 282
        out = wrapChannels(lambda _=None: sos.add(["sub"], ["sub/file?"]))  # type: str  # line 283
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", os.path.abspath("sub")], out)  # line 284
        sos.commit("test")  # should pick up sub/file1 pattern  # line 285
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 286
        _.createFile(1)  # line 287
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 288
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 288
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 288
        except:  # line 289
            pass  # line 289

    def testNoArgs(_):  # line 291
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 292

    def testAutoMetadataUpgrade(_):  # line 294
        sos.offline()  # line 295
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 296
            repo, branches, config = json.load(fd)  # line 296
        repo["version"] = None  # lower than any pip version  # line 297
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 298
        del repo["format"]  # simulate pre-1.3.5  # line 299
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 300
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 300
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # type: str  # line 301
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 302

    def testFastBranching(_):  # line 304
        _.createFile(1)  # line 305
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict", "--verbose"]))  # type: str  # b0/r0 = ./file1  # line 306
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 307
        _.createFile(2)  # line 308
        os.unlink("file1")  # line 309
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 310
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 311
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 312
        _.createFile(3)  # line 313
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 314
        _.assertAllIn([sos.metaFile, sos.metaBack, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 315
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 316
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 317
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 318
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 319
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 320
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 323
        now = time.time()  # type: float  # line 324
        _.createFile(1)  # line 325
        sync()  # line 326
        sos.offline(options=["--strict"])  # line 327
        _.createFile(1, "abc")  # modify contents  # line 328
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 329
        sync()  # line 330
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 331
        _.assertIn("<older than previously committed>", out)  # line 332
        out = wrapChannels(lambda _=None: sos.commit())  # line 333
        _.assertIn("<older than previously committed>", out)  # line 334

    def testGetParentBranch(_):  # line 336
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 337
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 338
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 339
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 340
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 341

    def testTokenizeGlobPattern(_):  # line 343
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 344
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 345
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 346
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 347
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 348
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 349

    def testTokenizeGlobPatterns(_):  # line 351
        try:  # because number of literal strings differs  # line 352
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 352
            _.fail()  # because number of literal strings differs  # line 352
        except:  # line 353
            pass  # line 353
        try:  # because glob patterns differ  # line 354
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 354
            _.fail()  # because glob patterns differ  # line 354
        except:  # line 355
            pass  # line 355
        try:  # glob patterns differ, regardless of position  # line 356
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 356
            _.fail()  # glob patterns differ, regardless of position  # line 356
        except:  # line 357
            pass  # line 357
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 358
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 359
        try:  # succeeds, because glob patterns match (differ only in position)  # line 360
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 360
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 360
        except:  # line 361
            pass  # line 361

    def testConvertGlobFiles(_):  # line 363
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 364
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 365

    def testFolderRemove(_):  # line 367
        m = sos.Metadata(os.getcwd())  # line 368
        _.createFile(1)  # line 369
        _.createFile("a", prefix="sub")  # line 370
        sos.offline()  # line 371
        _.createFile(2)  # line 372
        os.unlink("sub" + os.sep + "a")  # line 373
        os.rmdir("sub")  # line 374
        changes = sos.changes()  # TODO #254 replace by output check  # line 375
        _.assertEqual(1, len(changes.additions))  # line 376
        _.assertEqual(0, len(changes.modifications))  # line 377
        _.assertEqual(1, len(changes.deletions))  # line 378
        _.createFile("a", prefix="sub")  # line 379
        changes = sos.changes()  # line 380
        _.assertEqual(0, len(changes.deletions))  # line 381

    def testSwitchConflict(_):  # line 383
        sos.offline(options=["--strict"])  # (r0)  # line 384
        _.createFile(1)  # line 385
        sos.commit()  # add file (r1)  # line 386
        os.unlink("file1")  # line 387
        sos.commit()  # remove (r2)  # line 388
        _.createFile(1, "something else")  # line 389
        sos.commit()  # (r3)  # line 390
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 391
        _.existsFile(1, "x" * 10)  # line 392
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 393
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 394
        sos.switch("/1")  # add file1 back  # line 395
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 396
        _.existsFile(1, "something else")  # line 397

    def testComputeSequentialPathSet(_):  # line 399
        os.makedirs(sos.revisionFolder(0, 0))  # line 400
        os.makedirs(sos.revisionFolder(0, 1))  # line 401
        os.makedirs(sos.revisionFolder(0, 2))  # line 402
        os.makedirs(sos.revisionFolder(0, 3))  # line 403
        os.makedirs(sos.revisionFolder(0, 4))  # line 404
        m = sos.Metadata(os.getcwd())  # line 405
        m.branch = 0  # line 406
        m.commit = 2  # line 407
        m.saveBranches()  # line 408
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 409
        m.saveCommit(0, 0)  # initial  # line 410
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 411
        m.saveCommit(0, 1)  # mod  # line 412
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 413
        m.saveCommit(0, 2)  # add  # line 414
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 415
        m.saveCommit(0, 3)  # del  # line 416
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 417
        m.saveCommit(0, 4)  # readd  # line 418
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 419
        m.saveBranch(0)  # line 420
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 421
        m.saveBranches()  # line 422
        m.computeSequentialPathSet(0, 4)  # line 423
        _.assertEqual(2, len(m.paths))  # line 424

    def testParseRevisionString(_):  # line 426
        m = sos.Metadata(os.getcwd())  # line 427
        m.branch = 1  # line 428
        m.commits = {0: 0, 1: 1, 2: 2}  # line 429
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 430
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 431
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 432
        _.assertEqual((None, None), m.parseRevisionString(""))  # line 433
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 434
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 435
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 436

    def testOfflineEmpty(_):  # line 438
        os.mkdir("." + os.sep + sos.metaFolder)  # line 439
        try:  # line 440
            sos.offline("trunk")  # line 440
            _.fail()  # line 440
        except SystemExit as E:  # line 441
            _.assertEqual(1, E.code)  # line 441
        os.rmdir("." + os.sep + sos.metaFolder)  # line 442
        sos.offline("test")  # line 443
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 444
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 445
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 446
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 447
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 448
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 449

    def testOfflineWithFiles(_):  # line 451
        _.createFile(1, "x" * 100)  # line 452
        _.createFile(2)  # line 453
        sos.offline("test")  # line 454
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 455
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 456
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 457
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 458
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 459
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 460
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 461

    def testBranch(_):  # line 463
        _.createFile(1, "x" * 100)  # line 464
        _.createFile(2)  # line 465
        sos.offline("test")  # b0/r0  # line 466
        sos.branch("other")  # b1/r0  # line 467
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 468
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 469
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 471
        _.createFile(1, "z")  # modify file  # line 473
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 474
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 475
        _.createFile(3, "z")  # line 477
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 478
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 479
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 484
        _.createFile(1, "x" * 100)  # line 485
        _.createFile(2)  # line 486
        sos.offline("test")  # line 487
        changes = sos.changes()  # line 488
        _.assertEqual(0, len(changes.additions))  # line 489
        _.assertEqual(0, len(changes.deletions))  # line 490
        _.assertEqual(0, len(changes.modifications))  # line 491
        _.createFile(1, "z")  # size change  # line 492
        changes = sos.changes()  # line 493
        _.assertEqual(0, len(changes.additions))  # line 494
        _.assertEqual(0, len(changes.deletions))  # line 495
        _.assertEqual(1, len(changes.modifications))  # line 496
        sos.commit("message")  # line 497
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 498
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 499
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 500
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 501
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 502
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 503
        os.unlink("file2")  # line 504
        changes = sos.changes()  # line 505
        _.assertEqual(0, len(changes.additions))  # line 506
        _.assertEqual(1, len(changes.deletions))  # line 507
        _.assertEqual(1, len(changes.modifications))  # line 508
        sos.commit("modified")  # line 509
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 510
        try:  # expecting Exit due to no changes  # line 511
            sos.commit("nothing")  # expecting Exit due to no changes  # line 511
            _.fail()  # expecting Exit due to no changes  # line 511
        except:  # line 512
            pass  # line 512

    def testGetBranch(_):  # line 514
        m = sos.Metadata(os.getcwd())  # line 515
        m.branch = 1  # current branch  # line 516
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 517
        _.assertEqual(27, m.getBranchByName(27))  # line 518
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 519
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 520
        _.assertIsNone(m.getBranchByName("unknown"))  # line 521
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 522
        _.assertEqual(13, m.getRevisionByName("13"))  # line 523
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 524
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 525

    def testTagging(_):  # line 527
        m = sos.Metadata(os.getcwd())  # line 528
        sos.offline()  # line 529
        _.createFile(111)  # line 530
        sos.commit("tag", ["--tag"])  # line 531
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # type: str  # line 532
        _.assertTrue(any(("|tag" in line and line.endswith("|%sTAG%s" % (sos.Fore.MAGENTA, sos.Fore.RESET)) for line in out)))  # line 533
        _.createFile(2)  # line 534
        try:  # line 535
            sos.commit("tag")  # line 535
            _.fail()  # line 535
        except:  # line 536
            pass  # line 536
        sos.commit("tag-2", ["--tag"])  # line 537
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 538
        _.assertIn("TAG tag", out)  # line 539

    def testSwitch(_):  # line 541
        try:  # line 542
            shutil.rmtree(os.path.join(rmteFolder, sos.metaFolder))  # line 542
        except:  # line 543
            pass  # line 543
        _.createFile(1, "x" * 100)  # line 544
        _.createFile(2, "y")  # line 545
        sos.offline("test", remotes=[rmteFolder])  # file1-2  in initial branch commit  # line 546
        sos.branch("second")  # file1-2  switch, having same files  # line 547
        sos.switch("0")  # no change, switch back, no problem  # line 548
        sos.switch("second")  # no change  # switch back, no problem  # line 549
        _.createFile(3, "y")  # generate a file  # line 550
        try:  # uncommited changes detected  # line 551
            sos.switch("test")  # uncommited changes detected  # line 551
            _.fail()  # uncommited changes detected  # line 551
        except SystemExit as E:  # line 552
            _.assertEqual(1, E.code)  # line 552
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 553
        sos.changes()  # line 554
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 555
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 556
        _.createFile("XXX")  # line 557
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 558
        _.assertIn("File tree has changes", out)  # line 559
        _.assertNotIn("File tree is unchanged", out)  # line 560
        _.assertIn("  * b0   'test'", out)  # line 561
        _.assertIn("    b1 'second'", out)  # line 562
        _.assertIn("modified", out)  # one branch has commits  # line 563
        _.assertIn("in sync", out)  # the other doesn't  # line 564
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 565
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 566
        _.assertAllIn(["Metadata format", "Content checking:    %ssize & timestamp" % sos.Fore.BLUE, "Data compression:    %sdeactivated" % sos.Fore.BLUE, "Repository mode:     %ssimple" % sos.Fore.GREEN, "Number of branches:  2"], out)  # line 567
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 568
        _.createFile(4, "xy")  # generate a file  # line 569
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 570
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 571
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 572
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 573
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 574
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 575
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 576
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 577
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 578
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 579
        _.assertNotIn("Creating backup", out)  # line 580
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 581
        _.assertIn("Dumping revisions", out)  # line 582
        _.assertNotIn("Creating backup", out)  # line 583
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 584
        _.assertAllIn(["Creating backup"], out)  # line 585
        _.assertIn("Dumping revisions", out)  # line 586
        sos.verbose.pop()  # line 587
        _.remoteIsSame()  # line 588
        os.chdir(rmteFolder)  # line 589
        try:  # line 590
            sos.status()  # line 590
        except SystemExit as E:  # line 591
            _.assertEqual(1, E.code)  # line 591

    def testAutoDetectVCS(_):  # line 593
        os.mkdir(".git")  # line 594
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 595
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 596
            meta = fd.read()  # line 596
        _.assertTrue("\"master\"" in meta)  # line 597
        os.rmdir(".git")  # line 598

    def testNoRemotes(_):  # line 600
        sos.offline(remotes=[rmteFolder])  # line 601
        _.createFile(1)  # line 602
        sos.commit(options=["--no-remotes"])  # line 603
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")))  # line 604
        _.assertFalse(_.existsFile(os.path.join(sos.branchFolder(0, rmteFolder), "r%d" % 1, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")))  # line 605

    def testUpdate(_):  # line 607
        sos.offline("trunk")  # create initial branch b0/r0  # line 608
        _.createFile(1, "x" * 100)  # line 609
        sos.commit("second")  # create b0/r1  # line 610

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 612
        _.assertFalse(_.existsFile(1))  # line 613

        sos.update("/1")  # recreate file1  # line 615
        _.assertTrue(_.existsFile(1))  # line 616

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 618
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 619
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 620
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 621

        sos.update("/1")  # do nothing, as nothing has changed  # line 623
        _.assertTrue(_.existsFile(1))  # line 624

        _.createFile(2, "y" * 100)  # line 626
#    out:str = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 629
        _.assertTrue(_.existsFile(2))  # line 630
        sos.update("trunk", ["--add"])  # only add stuff  # line 631
        _.assertTrue(_.existsFile(2))  # line 632
        sos.update("trunk")  # nothing to do  # line 633
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 634

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 636
        _.createFile(10, theirs)  # line 637
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 638
        _.createFile(11, mine)  # line 639
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 640
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 641

    def testUpdate2(_):  # line 643
        _.createFile("test.txt", "x" * 10)  # line 644
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 645
        sync()  # line 646
        sos.branch("mod")  # line 647
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 648
        sos.commit("mod")  # create b0/r1  # line 649
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 650
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 651
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 652
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 653
        _.createFile("test.txt", "x" * 10)  # line 654
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 655
        sync()  # line 656
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 657
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 658
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 659
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 660
        sync()  # line 661
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 662
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 663

    def testIsTextType(_):  # line 665
        m = sos.Metadata(".")  # line 666
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 667
        m.c.bintype = ["*.md.confluence"]  # line 668
        _.assertTrue(m.isTextType("ab.txt"))  # line 669
        _.assertTrue(m.isTextType("./ab.txt"))  # line 670
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 671
        _.assertFalse(m.isTextType("bc/ab."))  # line 672
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 673
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 674
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 675
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 676

    def testEolDet(_):  # line 678
        ''' Check correct end-of-line detection. '''  # line 679
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 680
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 681
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 682
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 683
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 684
        _.assertIsNone(sos.eoldet(b""))  # line 685
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 686

    def testMergeClassic(_):  # line 688
        _.createFile(1, contents=b"abcdefg")  # line 689
        b = b"iabcxeg"  # type: bytes  # line 690
        _.assertEqual.__self__.maxDiff = None  # to get a full diff  # line 691
        out = wrapChannels(lambda _=None: sos.mergeClassic(b, "file1", "from", "to", 24523234, 1))  # type: str  # line 692
        try:  # line 693
            _.assertAllIn(["*** from\tThu Jan  1 07:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # line 693
        except:  # differing local time on CI system TODO make this better  # line 694
            _.assertAllIn(["*** from\tThu Jan  1 06:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # differing local time on CI system TODO make this better  # line 694

    def testMerge(_):  # line 696
        ''' Check merge results depending on user options. '''  # line 697
        a = b"a\nb\ncc\nd"  # type: bytes  # line 698
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 699
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 700
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 701
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 702
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 703
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 704
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 705
        a = b"a\nb\ncc\nd"  # line 706
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 707
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 708
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 709
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 710
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 712
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 713
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 715
        b = b"a\nc\ne"  # line 716
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 717
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 718
        a = b"a\nb\ne"  # intra-line merge  # line 719
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 720
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 721
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 722
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 723
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 724
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 725

    def testMergeEol(_):  # line 727
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 728
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 729
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 730
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 731
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 732

    def testPickyMode(_):  # line 734
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 735
        sos.offline("trunk", None, ["--picky"])  # line 736
        changes = sos.changes()  # line 737
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 738
        out = wrapChannels(lambda _=None: sos.add(["."], ["./file?"], options=["--force", "--relative"]))  # type: str  # line 739
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", "'.'"], out)  # line 740
        _.createFile(1, "aa")  # line 741
        sos.commit("First")  # add one file  # line 742
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 743
        _.createFile(2, "b")  # line 744
        try:  # add nothing, because picky  # line 745
            sos.commit("Second")  # add nothing, because picky  # line 745
        except:  # line 746
            pass  # line 746
        sos.add(["."], ["./file?"])  # line 747
        sos.commit("Third")  # line 748
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 749
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 750
        _.assertIn("    r0", out)  # line 751
        sys.argv.extend(["-n", "2"])  # We cannot use the opions array for named argument options  # line 752
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 753
        sys.argv.pop()  # line 754
        sys.argv.pop()  # line 754
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 755
        _.assertIn("    r1", out)  # line 756
        _.assertIn("  * r2", out)  # line 757
        try:  # line 758
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 758
        except SystemExit as E:  # line 759
            _.assertEqual(0, E.code)  # line 759
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 760
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 761
        _.assertNotIn("    r1", out)  # line 762
        _.assertIn("  * r2", out)  # line 763
        _.createFile(3, prefix="sub")  # line 764
        sos.add(["sub"], ["sub/file?"])  # line 765
        changes = sos.changes()  # line 766
        _.assertEqual(1, len(changes.additions))  # line 767
        _.assertTrue("sub/file3" in changes.additions)  # line 768

    def testTrackedSubfolder(_):  # line 770
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 771
        os.mkdir("." + os.sep + "sub")  # line 772
        sos.offline("trunk", None, ["--track"])  # line 773
        _.createFile(1, "x")  # line 774
        _.createFile(1, "x", prefix="sub")  # line 775
        sos.add(["."], ["./file?"])  # add glob pattern to track  # line 776
        sos.commit("First")  # line 777
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 778
        sos.add(["."], ["sub/file?"])  # add glob pattern to track  # line 779
        sos.commit("Second")  # one new file + meta  # line 780
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 781
        os.unlink("file1")  # remove from basefolder  # line 782
        _.createFile(2, "y")  # line 783
        sos.remove(["."], ["sub/file?"])  # line 784
        try:  # TODO check more textual details here  # line 785
            sos.remove(["."], ["sub/bla"])  # TODO check more textual details here  # line 785
            _.fail("Expected exit")  # TODO check more textual details here  # line 785
        except SystemExit as E:  # line 786
            _.assertEqual(1, E.code)  # line 786
        sos.commit("Third")  # line 787
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 788
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 791
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 796
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 797
        _.createFile(1)  # line 798
        _.createFile("a123a")  # untracked file "a123a"  # line 799
        sos.add(["."], ["./file?"])  # add glob tracking pattern  # line 800
        sos.commit("second")  # versions "file1"  # line 801
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 802
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 803
        _.assertTrue(any(("|" in o and "./file?" in o for o in out.split("\n"))))  # line 804

        _.createFile(2)  # untracked file "file2"  # line 806
        sos.commit("third")  # versions "file2"  # line 807
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 808

        os.mkdir("." + os.sep + "sub")  # line 810
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 811
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 812
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 813

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 815
        sos.remove(["."], ["./file?"])  # remove tracking pattern, but don't touch previously created and versioned files  # line 816
        sos.add([".", "."], ["./a*a", "./a*?"])  # add tracking pattern  # line 817
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 818
        _.assertEqual(0, len(changes.modifications))  # line 819
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 820
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 821

        sos.commit("Second_2")  # line 823
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 824
        _.existsFile(1, b"x" * 10)  # line 825
        _.existsFile(2, b"x" * 10)  # line 826

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 828
        _.existsFile(1, b"x" * 10)  # line 829
        _.existsFile("a123a", b"x" * 10)  # line 830

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 832
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 833
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 834

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 836
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 837
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 838
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 839
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 840
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 841
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 842
# TODO test switch --meta

    def testLsTracked(_):  # line 845
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 846
        _.createFile(1)  # line 847
        _.createFile("foo")  # line 848
        sos.add(["."], ["./file*"])  # capture one file  # line 849
        sos.ls()  # line 850
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # type: str  # line 851
        _.assertInAny("TRK file1  (file*)", out)  # line 852
        _.assertNotInAny("... file1  (file*)", out)  # line 853
        _.assertInAny("    foo", out)  # line 854
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 855
        _.assertInAny("TRK file*", out)  # line 856
        _.createFile("a", prefix="sub")  # line 857
        sos.add(["sub"], ["sub/a"])  # line 858
        sos.ls("sub")  # line 859
        _.assertInAny("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 860

    def testLineMerge(_):  # line 862
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 863
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 864
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 865
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 866

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 868
        _.createFile(1)  # line 869
        sos.offline("master", options=["--force"])  # line 870
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # type: str  # line 871
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 872
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 873
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 874
        _.createFile(2)  # line 875
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 876
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 877
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 878
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 879

    def testLocalConfig(_):  # line 881
        sos.offline("bla", options=[])  # line 882
        try:  # line 883
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 883
        except SystemExit as E:  # line 884
            _.assertEqual(0, E.code)  # line 884
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 885

    def testConfigVariations(_):  # line 887
        def makeRepo():  # line 888
            try:  # line 889
                os.unlink("file1")  # line 889
            except:  # line 890
                pass  # line 890
            sos.offline("master", options=["--force"])  # line 891
            _.createFile(1)  # line 892
            sos.commit("Added file1")  # line 893
        try:  # line 894
            sos.config(["set", "strict", "on"])  # line 894
        except SystemExit as E:  # line 895
            _.assertEqual(0, E.code)  # line 895
        makeRepo()  # line 896
        _.assertTrue(checkRepoFlag("strict", True))  # line 897
        try:  # line 898
            sos.config(["set", "strict", "off"])  # line 898
        except SystemExit as E:  # line 899
            _.assertEqual(0, E.code)  # line 899
        makeRepo()  # line 900
        _.assertTrue(checkRepoFlag("strict", False))  # line 901
        try:  # line 902
            sos.config(["set", "strict", "yes"])  # line 902
        except SystemExit as E:  # line 903
            _.assertEqual(0, E.code)  # line 903
        makeRepo()  # line 904
        _.assertTrue(checkRepoFlag("strict", True))  # line 905
        try:  # line 906
            sos.config(["set", "strict", "no"])  # line 906
        except SystemExit as E:  # line 907
            _.assertEqual(0, E.code)  # line 907
        makeRepo()  # line 908
        _.assertTrue(checkRepoFlag("strict", False))  # line 909
        try:  # line 910
            sos.config(["set", "strict", "1"])  # line 910
        except SystemExit as E:  # line 911
            _.assertEqual(0, E.code)  # line 911
        makeRepo()  # line 912
        _.assertTrue(checkRepoFlag("strict", True))  # line 913
        try:  # line 914
            sos.config(["set", "strict", "0"])  # line 914
        except SystemExit as E:  # line 915
            _.assertEqual(0, E.code)  # line 915
        makeRepo()  # line 916
        _.assertTrue(checkRepoFlag("strict", False))  # line 917
        try:  # line 918
            sos.config(["set", "strict", "true"])  # line 918
        except SystemExit as E:  # line 919
            _.assertEqual(0, E.code)  # line 919
        makeRepo()  # line 920
        _.assertTrue(checkRepoFlag("strict", True))  # line 921
        try:  # line 922
            sos.config(["set", "strict", "false"])  # line 922
        except SystemExit as E:  # line 923
            _.assertEqual(0, E.code)  # line 923
        makeRepo()  # line 924
        _.assertTrue(checkRepoFlag("strict", False))  # line 925
        try:  # line 926
            sos.config(["set", "strict", "enable"])  # line 926
        except SystemExit as E:  # line 927
            _.assertEqual(0, E.code)  # line 927
        makeRepo()  # line 928
        _.assertTrue(checkRepoFlag("strict", True))  # line 929
        try:  # line 930
            sos.config(["set", "strict", "disable"])  # line 930
        except SystemExit as E:  # line 931
            _.assertEqual(0, E.code)  # line 931
        makeRepo()  # line 932
        _.assertTrue(checkRepoFlag("strict", False))  # line 933
        try:  # line 934
            sos.config(["set", "strict", "enabled"])  # line 934
        except SystemExit as E:  # line 935
            _.assertEqual(0, E.code)  # line 935
        makeRepo()  # line 936
        _.assertTrue(checkRepoFlag("strict", True))  # line 937
        try:  # line 938
            sos.config(["set", "strict", "disabled"])  # line 938
        except SystemExit as E:  # line 939
            _.assertEqual(0, E.code)  # line 939
        makeRepo()  # line 940
        _.assertTrue(checkRepoFlag("strict", False))  # line 941
        try:  # line 942
            sos.config(["set", "strict", "nope"])  # line 942
            _.fail()  # line 942
        except SystemExit as E:  # line 943
            _.assertEqual(1, E.code)  # line 943

    def testLsSimple(_):  # line 945
        _.createFile(1)  # line 946
        _.createFile("foo")  # line 947
        _.createFile("ign1")  # line 948
        _.createFile("ign2")  # line 949
        _.createFile("bar", prefix="sub")  # line 950
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 951
        try:  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 952
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 952
        except SystemExit as E:  # line 953
            _.assertEqual(0, E.code)  # line 953
        try:  # additional ignore pattern  # line 954
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 954
        except SystemExit as E:  # line 955
            _.assertEqual(0, E.code)  # line 955
        try:  # define a list of ignore patterns  # line 956
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 956
        except SystemExit as E:  # line 957
            _.assertEqual(0, E.code)  # line 957
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # type: str  # line 958
        _.assertAllIn(["             ignores", "[global]", "['ign1', 'ign2']"], out)  # line 959
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 960
        _.assertAllIn(["             ignores", "[global]", "['ign1', 'ign2']"], out)  # line 961
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 962
        _.assertInAny('    file1', out)  # line 963
        _.assertInAny('    ign1', out)  # line 964
        _.assertInAny('    ign2', out)  # line 965
        _.assertNotIn('DIR sub', out)  # line 966
        _.assertNotIn('    bar', out)  # line 967
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 968
        _.assertIn('DIR sub', out)  # line 969
        _.assertIn('    bar', out)  # line 970
        try:  # line 971
            sos.config(["rm", "foo", "bar"])  # line 971
            _.fail()  # line 971
        except SystemExit as E:  # line 972
            _.assertEqual(1, E.code)  # line 972
        try:  # line 973
            sos.config(["rm", "ignores", "foo"])  # line 973
            _.fail()  # line 973
        except SystemExit as E:  # line 974
            _.assertEqual(1, E.code)  # line 974
        try:  # line 975
            sos.config(["rm", "ignores", "ign1"])  # line 975
        except SystemExit as E:  # line 976
            _.assertEqual(0, E.code)  # line 976
        try:  # remove ignore pattern  # line 977
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 977
        except SystemExit as E:  # line 978
            _.assertEqual(0, E.code)  # line 978
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 979
        _.assertInAny('    ign1', out)  # line 980
        _.assertInAny('IGN ign2', out)  # line 981
        _.assertNotInAny('    ign2', out)  # line 982

    def testWhitelist(_):  # line 984
# TODO test same for simple mode
        _.createFile(1)  # line 986
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 987
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 988
        sos.add(["."], ["./file*"])  # add tracking pattern for "file1"  # line 989
        sos.commit(options=["--force"])  # attempt to commit the file  # line 990
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 991
        try:  # Exit because dirty  # line 992
            sos.online()  # Exit because dirty  # line 992
            _.fail()  # Exit because dirty  # line 992
        except:  # exception expected  # line 993
            pass  # exception expected  # line 993
        _.createFile("x2")  # add another change  # line 994
        sos.add(["."], ["./x?"])  # add tracking pattern for "file1"  # line 995
        try:  # force beyond dirty flag check  # line 996
            sos.online(["--force"])  # force beyond dirty flag check  # line 996
            _.fail()  # force beyond dirty flag check  # line 996
        except:  # line 997
            pass  # line 997
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 998
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 999

        _.createFile(1)  # line 1001
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 1002
        sos.offline("xx", None, ["--track"])  # line 1003
        sos.add(["."], ["./file*"])  # line 1004
        sos.commit()  # should NOT ask for force here  # line 1005
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 1006

    def testRemove(_):  # line 1008
        _.createFile(1, "x" * 100)  # line 1009
        sos.offline("trunk")  # line 1010
        try:  # line 1011
            sos.destroy("trunk")  # line 1011
            _fail()  # line 1011
        except:  # line 1012
            pass  # line 1012
        _.createFile(2, "y" * 10)  # line 1013
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 1014
        sos.destroy("trunk")  # line 1015
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 1016
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 1017
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 1018
        sos.branch("next")  # line 1019
        _.createFile(3, "y" * 10)  # make a change  # line 1020
        sos.destroy("added", "--force")  # should succeed  # line 1021

    def testFastBranchingOnEmptyHistory(_):  # line 1023
        ''' Test fast branching without revisions and with them. '''  # line 1024
        sos.offline(options=["--strict", "--compress"])  # b0  # line 1025
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 1026
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 1027
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 1028
        sos.destroy("2")  # line 1029
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 1030
        _.assertIn("b0 'trunk' @", out)  # line 1031
        _.assertIn("b1         @", out)  # line 1032
        _.assertIn("b3         @", out)  # line 1033
        _.assertNotIn("b2         @", out)  # line 1034
        sos.branch("", "")  # non-fast branching of b4  # line 1035
        _.createFile(1)  # line 1036
        _.createFile(2)  # line 1037
        sos.commit("")  # line 1038
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 1039
        sos.destroy("4")  # line 1040
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 1041
        _.assertIn("b0 'trunk' @", out)  # line 1042
        _.assertIn("b1         @", out)  # line 1043
        _.assertIn("b3         @", out)  # line 1044
        _.assertIn("b5         @", out)  # line 1045
        _.assertNotIn("b2         @", out)  # line 1046
        _.assertNotIn("b4         @", out)  # line 1047
# TODO add more files and branch again

    def testUsage(_):  # line 1050
        try:  # TODO expect sys.exit(0)  # line 1051
            sos.usage()  # TODO expect sys.exit(0)  # line 1051
            _.fail()  # TODO expect sys.exit(0)  # line 1051
        except:  # line 1052
            pass  # line 1052
        try:  # TODO expect sys.exit(0)  # line 1053
            sos.usage("help")  # TODO expect sys.exit(0)  # line 1053
            _.fail()  # TODO expect sys.exit(0)  # line 1053
        except:  # line 1054
            pass  # line 1054
        try:  # TODO expect sys.exit(0)  # line 1055
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 1055
            _.fail()  # TODO expect sys.exit(0)  # line 1055
        except:  # line 1056
            pass  # line 1056
        try:  # line 1057
            sos.usage(version=True)  # line 1057
            _.fail()  # line 1057
        except:  # line 1058
            pass  # line 1058
        try:  # line 1059
            sos.usage(version=True)  # line 1059
            _.fail()  # line 1059
        except:  # line 1060
            pass  # line 1060

    def testOnlyExcept(_):  # line 1062
        ''' Test blacklist glob rules. '''  # line 1063
        sos.offline(options=["--track"])  # line 1064
        _.createFile("a.1")  # line 1065
        _.createFile("a.2")  # line 1066
        _.createFile("b.1")  # line 1067
        _.createFile("b.2")  # line 1068
        sos.add(["."], ["./a.?"])  # line 1069
        sos.add(["."], ["./?.1"], negative=True)  # line 1070
        out = wrapChannels(lambda _=None: sos.commit())  # type: str  # line 1071
        _.assertIn("ADD ./a.2", out)  # line 1072
        _.assertNotIn("ADD ./a.1", out)  # line 1073
        _.assertNotIn("ADD ./b.1", out)  # line 1074
        _.assertNotIn("ADD ./b.2", out)  # line 1075

    def testOnly(_):  # line 1077
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",)), ["bla"], ["blo"]), sos.parseArgumentOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--remote", "bla", "--exclude-remote", "blo", "--only"]))  # line 1078
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1079
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1080
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1081
        sos.offline(options=["--track", "--strict"])  # line 1082
        _.createFile(1)  # line 1083
        _.createFile(2)  # line 1084
        sos.add(["."], ["./file1"])  # line 1085
        sos.add(["."], ["./file2"])  # line 1086
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1087
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1088
        sos.commit()  # adds also file2  # line 1089
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1090
        _.createFile(1, "cc")  # modify both files  # line 1091
        _.createFile(2, "dd")  # line 1092
        try:  # line 1093
            sos.config(["set", "texttype", "file2"])  # line 1093
        except SystemExit as E:  # line 1094
            _.assertEqual(0, E.code)  # line 1094
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1095
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1096
        _.assertTrue("./file2" in changes.modifications)  # line 1097
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # line 1098
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1099
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1100
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # line 1101

    def testEmptyFiles(_):  # line 1103
        sos.offline()  # line 1104
        _.createFile(1, "")  # empty file  # line 1105
        sos.commit()  # line 1106
        changes = sos.changes()  # line 1107
        _.assertEqual(0, len(changes.additions) + len(changes.modifications) + len(changes.deletions))  # line 1108

        setRepoFlag("strict", True)  # line 1110
        changes = sos.changes()  # line 1111
        _.assertEqual(1, len(changes.modifications))  # because hash was set to None in simple mode  # line 1112
        sos.commit()  # commit now with hash computation  # line 1113
        setRepoFlag("strict", False)  # line 1114

        time.sleep(FS_PRECISION)  # line 1116
        _.createFile(1, "")  # touch file  # line 1117
        changes = sos.changes()  # line 1118
        _.assertEqual(1, len(changes.modifications))  # since modified timestamp  # line 1119

    def testDiff(_):  # line 1121
        try:  # manually mark this file as "textual"  # line 1122
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1122
        except SystemExit as E:  # line 1123
            _.assertEqual(0, E.code)  # line 1123
        sos.offline(options=["--strict"])  # line 1124
        _.createFile(1)  # line 1125
        _.createFile(2)  # line 1126
        sos.commit()  # line 1127
        _.createFile(1, "sdfsdgfsdf")  # line 1128
        _.createFile(2, "12343")  # line 1129
        sos.commit()  # line 1130
        _.createFile(1, "foobar")  # line 1131
        _.createFile(3)  # line 1132
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # type: str  # compare with r1 (second counting from last which is r2)  # line 1133
        _.assertIn("ADD ./file3", out)  # line 1134
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "old 0 |xxxxxxxxxx|", "now 0 |foobar|"], out)  # line 1135
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1136

    def testReorderRenameActions(_):  # line 1138
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1139
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1140
        try:  # line 1141
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1141
            _.fail()  # line 1141
        except:  # line 1142
            pass  # line 1142

    def testPublish(_):  # line 1144
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1145

    def testColorFlag(_):  # line 1147
        sos.offline()  # line 1148
        _.createFile(1)  # line 1149
#    setRepoFlag("useColorOutput", False, toConfig = True)
#    sos.Metadata.singleton = None  # for new slurp of configuration
        sos.enableColor(False, force=True)  # line 1152
        sos.verbose[:] = [None]  # set "true"  # line 1153
        out = wrapChannels(lambda _=None: sos.changes()).replace("\r\n", "\n").split("\n")  # type: List[str]  # line 1154
        _.assertTrue(any((line.startswith(sos.usage.MARKER_TEXT + "Changes of file tree") for line in out)))  # line 1155
#    setRepoFlag("useColorOutput", True,  toConfig = True)
#    sos.Metadata.singleton = None
        sos.enableColor(True, force=True)  # line 1158
        out = wrapChannels(lambda _=None: sos.changes()).replace("\r\n", "\n").split("\n")  # line 1159
        _.assertTrue(any((line.startswith((sos.usage.MARKER_TEXT if sys.platform == "win32" else sos.MARKER_COLOR) + "Changes of file tree") for line in out)))  # because it may start with a color code  # line 1160
        sos.verbose.pop()  # line 1161

    def testMove(_):  # line 1163
        ''' Move primarily modifies tracking patterns and moves files around accordingly. '''  # line 1164
        sos.offline(options=["--strict", "--track"])  # line 1165
        _.createFile(1)  # line 1166
        sos.add(["."], ["./file?"])  # line 1167
# assert error when source folder is missing
        out = wrapChannels(lambda _=None: sos.move("sub", "sub/file?", ".", "./?file"))  # type: str  # line 1169
        _.assertIn("Source folder doesn't exist", out)  # line 1170
        _.assertIn("EXIT CODE 1", out)  # line 1171
# if target folder missing: create it and move matching files into it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1173
        _.assertTrue(os.path.exists("sub"))  # line 1174
        _.assertTrue(os.path.exists("sub/file1"))  # line 1175
        _.assertFalse(os.path.exists("file1"))  # line 1176
# test move back to previous location, plus rename the file
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1178
        _.assertTrue(os.path.exists("1file"))  # line 1179
        _.assertFalse(os.path.exists("sub/file1"))  # line 1180
# assert error when nothing matches source pattern
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*"))  # line 1182
        _.assertIn("No files match the specified file pattern", out)  # line 1183
        _.assertIn("EXIT CODE", out)  # line 1184
        sos.add(["."], ["./*"])  # add catch-all tracking pattern to root folder  # line 1185
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*", options=["--force"]))  # line 1186
        _.assertIn("  './*' matches 3 files", out)  # line 1187
        _.assertIn("EXIT CODE", out)  # line 1188
# test rename no conflict
        _.createFile(1)  # line 1190
        _.createFile(2)  # line 1191
        _.createFile(3)  # line 1192
        sos.add(["."], ["./file*"])  # line 1193
        sos.remove(["."], ["./*"])  # line 1194
        try:  # define an ignore pattern  # line 1195
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1195
        except SystemExit as E:  # line 1196
            _.assertEqual(0, E.code)  # line 1196
        try:  # line 1197
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1197
        except SystemExit as E:  # line 1198
            _.assertEqual(0, E.code)  # line 1198
        sos.move(".", "./file*", ".", "./fi*le")  # should only move not ignored files files  # line 1199
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1200
        _.assertTrue(all((not os.path.exists("file%d" % i) for i in range(1, 4))))  # line 1201
        _.assertFalse(os.path.exists("fi4le"))  # line 1202
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1204
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(["."], ["./?file"])  # untrack pattern, which was renamed before  # line 1208
        sos.add(["."], ["./?a?b"], ["--force"])  # line 1209
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1210
        _.createFile("1a2b")  # should not be tracked  # line 1211
        _.createFile("a1b2")  # should be tracked  # line 1212
        sos.commit()  # line 1213
        _.assertEqual(5, len(os.listdir(sos.revisionFolder(0, 1))))  # meta, a1b2, fi[1-3]le  # line 1214
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1215
        _.createFile("1a1b1")  # line 1216
        _.createFile("1a1b2")  # line 1217
        sos.add(["."], ["./?a?b*"])  # line 1218
# test target pattern exists
        out = wrapChannels(lambda _=None: sos.move(".", "./?a?b*", ".", "./z?z?"))  # line 1220
        _.assertIn("not unique", out)  # line 1221
# TODO only rename if actually any files are versioned? or simply what is currently alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1225
        _.createFile(1)  # line 1226
        _.createFile(3)  # line 1227
        _.createFile(5)  # line 1228
        sos.offline()  # branch 0: only file1  # line 1229
        sos.branch()  # line 1230
        os.unlink("file1")  # line 1231
        os.unlink("file3")  # line 1232
        os.unlink("file5")  # line 1233
        _.createFile(2)  # line 1234
        _.createFile(4)  # line 1235
        _.createFile(6)  # line 1236
        sos.commit()  # branch 1: only file2  # line 1237
        sos.switch("0/")  # line 1238
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1239
        _.assertFalse(_.existsFile(1))  # line 1240
        _.assertFalse(_.existsFile(3))  # line 1241
        _.assertFalse(_.existsFile(5))  # line 1242
        _.assertTrue(_.existsFile(2))  # line 1243
        _.assertTrue(_.existsFile(4))  # line 1244
        _.assertTrue(_.existsFile(6))  # line 1245

    def testMoveDetection(_):  # line 1247
        _.createFile(1, "bla")  # line 1248
        sos.offline()  # line 1249
        os.mkdir("sub1")  # line 1250
        os.mkdir("sub2")  # line 1251
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1252
        shutil.move("file1", "sub2")  # line 1253
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 1254
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1255
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1256
        sos.commit("Moved the file")  # line 1257
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1261

    def testHashCollision(_):  # line 1263
        old = sos.Metadata.findChanges  # line 1264
        @_coconut_tco  # line 1265
        def patched(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False, remotes: 'List[str]'=[]) -> 'Tuple[sos.ChangeSet, _coconut.typing.Optional[str]]':  # line 1265
            import collections  # used only in this method  # line 1266
            write = branch is not None and revision is not None  # line 1267
            if write:  # line 1268
                try:  # line 1269
                    os.makedirs(sos.encode(sos.revisionFolder(branch, revision, base=_.root)))  # line 1269
                except FileExistsError:  # HINT "try" only necessary for hash collision *test code* (!)  # line 1270
                    pass  # HINT "try" only necessary for hash collision *test code* (!)  # line 1270
            return _coconut_tail_call(old, _, branch, revision, checkContent, inverse, considerOnly, dontConsider, progress)  # line 1271
        sos.Metadata.findChanges = patched  # monkey-patch  # line 1272
        sos.offline()  # line 1273
        _.createFile(1)  # line 1274
        os.mkdir(sos.revisionFolder(0, 1))  # line 1275
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # hashed file name for not-yet-committed file1  # line 1276
        _.createFile(1)  # line 1277
        try:  # line 1278
            sos.commit()  # line 1278
            _.fail("Expected system exit due to hash collision detection")  # line 1278
        except SystemExit as E:  # HINT exit is implemented in utility.hashFile  # line 1279
            _.assertEqual(1, E.code)  # HINT exit is implemented in utility.hashFile  # line 1279
        sos.Metadata.findChanges = old  # revert monkey patch  # line 1280

    def testFindBase(_):  # line 1282
        old = os.getcwd()  # line 1283
        try:  # line 1284
            os.mkdir("." + os.sep + ".git")  # line 1285
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1286
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1287
            os.chdir("a" + os.sep + "b")  # line 1288
            s, vcs, cmd = sos.findSosVcsBase()  # line 1289
            _.assertIsNotNone(s)  # line 1290
            _.assertIsNotNone(vcs)  # line 1291
            _.assertEqual("git", cmd)  # line 1292
        finally:  # line 1293
            os.chdir(old)  # line 1293

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1304
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1305
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1306
