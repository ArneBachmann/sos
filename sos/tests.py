#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x6bab4b1b

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
        for entry in os.listdir(testFolder):  # cannot reliably remove testFolder on Windows when using TortoiseSVN as VCS  # line 109
            resource = os.path.join(testFolder, entry)  # type: str  # line 110
            shutil.rmtree(sos.encode(resource)) if os.path.isdir(sos.encode(resource)) else os.unlink(sos.encode(resource))  # line 111
        os.chdir(testFolder)  # line 112

# Assertion helpers
    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]', only: 'bool'=False):  # line 115
        for w in what:  # line 116
            _.assertIn(w, where)  # line 116
        if only:  # line 117
            _.assertEqual(len(what), len(where))  # line 117

    def assertAllNotIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]'):  # line 119
        for w in what:  # line 120
            _.assertNotIn(w, where)  # line 120

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 122
        for w in where:  # line 123
            _.assertIn(what, w)  # line 123

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 125
        _.assertTrue(any((what in w for w in where)))  # line 125

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 127
        _.assertFalse(any((what in w for w in where)))  # line 127


# More helpers
    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None):  # line 131
        if prefix and not os.path.exists(prefix):  # line 132
            os.makedirs(prefix)  # line 132
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 133
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 133
        sync()  # line 134

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 136
        sync()  # line 137
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 138
            return False  # line 138
        if expectedContents is None:  # line 139
            return True  # line 139
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 140
            return fd.read() == expectedContents  # line 140

    def remoteIsSame(_):  # line 142
        sync()  # line 143
        for dirpath, dirnames, filenames in os.walk(os.path.join(testFolder, sos.metaFolder)):  # line 144
            rmtePath = os.path.normpath(os.path.join(rmteFolder, sos.metaFolder, os.path.relpath(dirpath, os.path.join(testFolder, sos.metaFolder))))  # type: str  # line 145
            others = os.listdir(rmtePath)  # type: List[str]  # line 146
            try:  # line 147
                _.assertAllIn(dirnames, others)  # line 147
                _.assertAllIn(others, dirnames + filenames)  # line 147
            except AssertionError as E:  # line 148
                raise AssertionError("Mismatch vs. remote: %r\n%r in %s" % (dirnames, others, dirpath)) from None  # line 148
            try:  # line 149
                _.assertAllIn(filenames, others)  # line 149
                _.assertAllIn(others, dirnames + filenames)  # line 149
            except AssertionError as E:  # line 150
                raise AssertionError("Mismatch vs. remote: %r\n% in %sr" % (filenames, others, dirpath)) from None  # line 150


# Unit tests
    def testAccessor(_):  # line 154
        a = sos.Accessor({"a": 1})  # type: Accessor  # line 155
        _.assertEqual((1, 1), (a["a"], a.a))  # line 156

    def testCharDet(_):  # line 158
        _.assertEqual("ascii", sos.detectEncoding(b"abc"))  # line 159
        _.assertEqual("UTF-8-SIG", sos.detectEncoding("abc".encode("utf-8-sig")))  # with BOM  # line 160
        _.assertEqual(sos.UTF8, sos.detectEncoding("abcüöä".encode("utf-8")))  # without BOM  # line 161

    def testTimeString(_):  # line 163
        _.assertEqual('1500 ms', sos.pure.timeString(1500))  # line 164
        _.assertEqual('1.5 seconds', sos.pure.timeString(1501))  # line 165
        _.assertEqual('23.0 hours', sos.pure.timeString(1000 * 60 * 60 * 23))  # line 166
        _.assertEqual('8.0 days', sos.pure.timeString(1000 * 60 * 60 * 24 * 8))  # line 167
        _.assertEqual('1.3 weeks', sos.pure.timeString(1000 * 60 * 60 * 24 * 9))  # line 168

    def testUnzip(_):  # line 170
        a = zip([1, 2, 3], ["a", "b", "c"])  # type: _coconut.typing.Sequence[Tuple[int, str]]  # line 171
        i = None  # type: Tuple[int]  # line 172
        c = None  # type: Tuple[str]  # line 172
        i, c = sos.unzip(a)  # line 173
        _.assertEqual((1, 2, 3), i)  # line 174
        _.assertEqual(("a", "b", "c"), c)  # line 175

    def testUsage(_):  # line 177
        out = wrapChannels(lambda _=None: sos.usage.usage("commit"))  # line 178
        _.assertAllIn(["commit [<message>]  Create a new revision", "Arguments:", "Options:"], out)  # line 179

    def testIndexing(_):  # line 181
        m = sos.Metadata()  # line 182
        m.commits = {}  # line 183
        _.assertEqual(1, m.correctNegativeIndexing(1))  # line 184
        _.assertEqual(9999999999999999, m.correctNegativeIndexing(9999999999999999))  # line 185
        _.assertEqual(0, m.correctNegativeIndexing(0))  # zero always returns zero, even no commits present  # line 186
        try:  # line 187
            m.correctNegativeIndexing(-1)  # line 187
            _.fail()  # line 187
        except SystemExit as E:  # line 188
            _.assertEqual(1, E.code)  # line 188
        m.commits = {0: sos.CommitInfo(0, 0), 1: sos.CommitInfo(1, 0)}  # line 189
        _.assertEqual(1, m.correctNegativeIndexing(-1))  # zero always returns zero, even no commits present  # line 190
        _.assertEqual(0, m.correctNegativeIndexing(-2))  # zero always returns zero, even no commits present  # line 191
        try:  # line 192
            m.correctNegativeIndexing(-3)  # line 192
            _.fail()  # line 192
        except SystemExit as E:  # line 193
            _.assertEqual(1, E.code)  # line 193

    def testRestoreFile(_):  # line 195
        m = sos.Metadata()  # line 196
        os.makedirs(sos.revisionFolder(0, 0))  # line 197
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 198
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 199
        _.assertTrue(_.existsFile("restored", b""))  # line 200

    def testGetAnyOfmap(_):  # line 202
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 203
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 204

    def testAjoin(_):  # line 206
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 207
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 208

    def testFindChanges(_):  # line 210
        m = sos.Metadata(os.getcwd())  # line 211
        try:  # line 212
            sos.config(["set", "texttype", "*"])  # line 212
        except SystemExit as E:  # line 213
            _.assertEqual(0, E.code)  # line 213
        try:  # will be stripped from leading paths anyway  # line 214
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 214
        except SystemExit as E:  # line 215
            _.assertEqual(0, E.code)  # line 215
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 216
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 217
            os.unlink(file)  # remove configuration file  # line 217
        _.createFile(9, b"")  # line 218
        _.createFile(1, "1")  # line 219
        m.createBranch(0)  # line 220
        _.assertEqual(2, len(m.paths))  # line 221
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 222
        _.createFile(1, "2")  # modify existing file  # line 223
        _.createFile(2, "2")  # add another file  # line 224
        m.loadCommit(0, 0)  # line 225
        changes, msg = m.findChanges()  # detect time skew  # line 226
        _.assertEqual(1, len(changes.additions))  # line 227
        _.assertEqual(0, len(changes.deletions))  # line 228
        _.assertEqual(1, len(changes.modifications))  # line 229
        _.assertEqual(0, len(changes.moves))  # line 230
        m.paths.update(changes.additions)  # line 231
        m.paths.update(changes.modifications)  # line 232
        _.createFile(2, "12")  # modify file again  # line 233
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 234
        _.assertEqual(0, len(changes.additions))  # line 235
        _.assertEqual(0, len(changes.deletions))  # line 236
        _.assertEqual(1, len(changes.modifications))  # line 237
        _.assertEqual(0, len(changes.moves))  # line 238
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 239
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 240
# TODO test moves

    def testDumpSorting(_):  # line 243
        m = sos.Metadata()  # type: Metadata  # line 244
        _.createFile(1)  # line 245
        sos.offline()  # line 246
        _.createFile(2)  # line 247
        _.createFile(3)  # line 248
        sos.commit()  # line 249
        _.createFile(4)  # line 250
        _.createFile(5)  # line 251
        sos.commit()  # line 252
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # type: List[str]  # line 253
        _.assertTrue(out.index("b0%sr2" % os.sep) > out.index("b0%sr1" % os.sep))  # line 254
        _.assertTrue(out.index("b0%sr1" % os.sep) > out.index("b0%sr0" % os.sep))  # line 255

    def testFitStrings(_):  # line 257
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 258
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 259
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 260
    def testMoves(_):  # line 261
        _.createFile(1, "1")  # line 262
        _.createFile(2, "2", "sub")  # line 263
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 264
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 265
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 266
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 267
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 268
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 269
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # line 270
        _.assertIn("MOV ..%sfile2  <-  file2" % os.sep, out)  # no ./ for relative OS-specific paths  # line 271
        _.assertIn("MOV file1  <-  ..%sfile1" % os.sep, out)  # line 272
        out = wrapChannels(lambda _=None: sos.commit())  # line 273
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 274
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 275
        _.assertAllIn(["Created new revision r01", "summing 628 bytes in 2 files (88.22% SOS overhead)"], out)  # TODO why is this not captured?  # line 276

    def testPatternPaths(_):  # line 278
        sos.offline(options=["--track"])  # line 279
        os.mkdir("sub")  # line 280
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 281
        out = wrapChannels(lambda _=None: sos.add(["sub"], ["sub/file?"]))  # type: str  # line 282
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", os.path.abspath("sub")], out)  # line 283
        sos.commit("test")  # should pick up sub/file1 pattern  # line 284
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 285
        _.createFile(1)  # line 286
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 287
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 287
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 287
        except:  # line 288
            pass  # line 288

    def testNoArgs(_):  # line 290
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 291

    def testAutoMetadataUpgrade(_):  # line 293
        sos.offline()  # line 294
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 295
            repo, branches, config = json.load(fd)  # line 295
        repo["version"] = None  # lower than any pip version  # line 296
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 297
        del repo["format"]  # simulate pre-1.3.5  # line 298
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 299
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 299
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # type: str  # line 300
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 301

    def testFastBranching(_):  # line 303
        _.createFile(1)  # line 304
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict", "--verbose"]))  # type: str  # b0/r0 = ./file1  # line 305
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 306
        _.createFile(2)  # line 307
        os.unlink("file1")  # line 308
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 309
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 310
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 311
        _.createFile(3)  # line 312
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 313
        _.assertAllIn([sos.metaFile, sos.metaBack, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 314
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 315
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 316
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 317
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 318
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 319
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 322
        now = time.time()  # type: float  # line 323
        _.createFile(1)  # line 324
        sync()  # line 325
        sos.offline(options=["--strict"])  # line 326
        _.createFile(1, "abc")  # modify contents  # line 327
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 328
        sync()  # line 329
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 330
        _.assertIn("<older than previously committed>", out)  # line 331
        out = wrapChannels(lambda _=None: sos.commit())  # line 332
        _.assertIn("<older than previously committed>", out)  # line 333

    def testGetParentBranch(_):  # line 335
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 336
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 337
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 338
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 339
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 340

    def testTokenizeGlobPattern(_):  # line 342
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 343
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 344
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 345
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 346
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 347
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 348

    def testTokenizeGlobPatterns(_):  # line 350
        try:  # because number of literal strings differs  # line 351
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 351
            _.fail()  # because number of literal strings differs  # line 351
        except:  # line 352
            pass  # line 352
        try:  # because glob patterns differ  # line 353
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 353
            _.fail()  # because glob patterns differ  # line 353
        except:  # line 354
            pass  # line 354
        try:  # glob patterns differ, regardless of position  # line 355
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 355
            _.fail()  # glob patterns differ, regardless of position  # line 355
        except:  # line 356
            pass  # line 356
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 357
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 358
        try:  # succeeds, because glob patterns match (differ only in position)  # line 359
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 359
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 359
        except:  # line 360
            pass  # line 360

    def testConvertGlobFiles(_):  # line 362
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 363
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 364

    def testFolderRemove(_):  # line 366
        m = sos.Metadata(os.getcwd())  # line 367
        _.createFile(1)  # line 368
        _.createFile("a", prefix="sub")  # line 369
        sos.offline()  # line 370
        _.createFile(2)  # line 371
        os.unlink("sub" + os.sep + "a")  # line 372
        os.rmdir("sub")  # line 373
        changes = sos.changes()  # TODO #254 replace by output check  # line 374
        _.assertEqual(1, len(changes.additions))  # line 375
        _.assertEqual(0, len(changes.modifications))  # line 376
        _.assertEqual(1, len(changes.deletions))  # line 377
        _.createFile("a", prefix="sub")  # line 378
        changes = sos.changes()  # line 379
        _.assertEqual(0, len(changes.deletions))  # line 380

    def testSwitchConflict(_):  # line 382
        sos.offline(options=["--strict"])  # (r0)  # line 383
        _.createFile(1)  # line 384
        sos.commit()  # add file (r1)  # line 385
        os.unlink("file1")  # line 386
        sos.commit()  # remove (r2)  # line 387
        _.createFile(1, "something else")  # line 388
        sos.commit()  # (r3)  # line 389
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 390
        _.existsFile(1, "x" * 10)  # line 391
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 392
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 393
        sos.switch("/1")  # add file1 back  # line 394
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 395
        _.existsFile(1, "something else")  # line 396

    def testComputeSequentialPathSet(_):  # line 398
        os.makedirs(sos.revisionFolder(0, 0))  # line 399
        os.makedirs(sos.revisionFolder(0, 1))  # line 400
        os.makedirs(sos.revisionFolder(0, 2))  # line 401
        os.makedirs(sos.revisionFolder(0, 3))  # line 402
        os.makedirs(sos.revisionFolder(0, 4))  # line 403
        m = sos.Metadata(os.getcwd())  # line 404
        m.branch = 0  # line 405
        m.commit = 2  # line 406
        m.saveBranches()  # line 407
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 408
        m.saveCommit(0, 0)  # initial  # line 409
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 410
        m.saveCommit(0, 1)  # mod  # line 411
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 412
        m.saveCommit(0, 2)  # add  # line 413
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 414
        m.saveCommit(0, 3)  # del  # line 415
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 416
        m.saveCommit(0, 4)  # readd  # line 417
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 418
        m.saveBranch(0)  # line 419
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 420
        m.saveBranches()  # line 421
        m.computeSequentialPathSet(0, 4)  # line 422
        _.assertEqual(2, len(m.paths))  # line 423

    def testParseRevisionString(_):  # line 425
        m = sos.Metadata(os.getcwd())  # line 426
        m.branch = 1  # line 427
        m.commits = {0: 0, 1: 1, 2: 2}  # line 428
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 429
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 430
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 431
        _.assertEqual((None, None), m.parseRevisionString(""))  # line 432
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 433
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 434
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 435

    def testOfflineEmpty(_):  # line 437
        os.mkdir("." + os.sep + sos.metaFolder)  # line 438
        try:  # line 439
            sos.offline("trunk")  # line 439
            _.fail()  # line 439
        except SystemExit as E:  # line 440
            _.assertEqual(1, E.code)  # line 440
        os.rmdir("." + os.sep + sos.metaFolder)  # line 441
        sos.offline("test")  # line 442
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 443
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 444
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 445
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 446
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 447
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 448

    def testOfflineWithFiles(_):  # line 450
        _.createFile(1, "x" * 100)  # line 451
        _.createFile(2)  # line 452
        sos.offline("test")  # line 453
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 454
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 455
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 456
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 457
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 458
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 459
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 460

    def testBranch(_):  # line 462
        _.createFile(1, "x" * 100)  # line 463
        _.createFile(2)  # line 464
        sos.offline("test")  # b0/r0  # line 465
        sos.branch("other")  # b1/r0  # line 466
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 467
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 468
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 470
        _.createFile(1, "z")  # modify file  # line 472
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 473
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 474
        _.createFile(3, "z")  # line 476
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 477
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 478
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 483
        _.createFile(1, "x" * 100)  # line 484
        _.createFile(2)  # line 485
        sos.offline("test")  # line 486
        changes = sos.changes()  # line 487
        _.assertEqual(0, len(changes.additions))  # line 488
        _.assertEqual(0, len(changes.deletions))  # line 489
        _.assertEqual(0, len(changes.modifications))  # line 490
        _.createFile(1, "z")  # size change  # line 491
        changes = sos.changes()  # line 492
        _.assertEqual(0, len(changes.additions))  # line 493
        _.assertEqual(0, len(changes.deletions))  # line 494
        _.assertEqual(1, len(changes.modifications))  # line 495
        sos.commit("message")  # line 496
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 497
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 498
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 499
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 500
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 501
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 502
        os.unlink("file2")  # line 503
        changes = sos.changes()  # line 504
        _.assertEqual(0, len(changes.additions))  # line 505
        _.assertEqual(1, len(changes.deletions))  # line 506
        _.assertEqual(1, len(changes.modifications))  # line 507
        sos.commit("modified")  # line 508
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 509
        try:  # expecting Exit due to no changes  # line 510
            sos.commit("nothing")  # expecting Exit due to no changes  # line 510
            _.fail()  # expecting Exit due to no changes  # line 510
        except:  # line 511
            pass  # line 511

    def testGetBranch(_):  # line 513
        m = sos.Metadata(os.getcwd())  # line 514
        m.branch = 1  # current branch  # line 515
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 516
        _.assertEqual(27, m.getBranchByName(27))  # line 517
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 518
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 519
        _.assertIsNone(m.getBranchByName("unknown"))  # line 520
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 521
        _.assertEqual(13, m.getRevisionByName("13"))  # line 522
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 523
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 524

    def testTagging(_):  # line 526
        m = sos.Metadata(os.getcwd())  # line 527
        sos.offline()  # line 528
        _.createFile(111)  # line 529
        sos.commit("tag", ["--tag"])  # line 530
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # type: str  # line 531
        _.assertTrue(any(("|tag" in line and line.endswith("|%sTAG%s" % (sos.Fore.MAGENTA, sos.Fore.RESET)) for line in out)))  # line 532
        _.createFile(2)  # line 533
        try:  # line 534
            sos.commit("tag")  # line 534
            _.fail()  # line 534
        except:  # line 535
            pass  # line 535
        sos.commit("tag-2", ["--tag"])  # line 536
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 537
        _.assertIn("TAG tag", out)  # line 538

    def testSwitch(_):  # line 540
        try:  # line 541
            shutil.rmtree(os.path.join(rmteFolder, sos.metaFolder))  # line 541
        except:  # line 542
            pass  # line 542
        _.createFile(1, "x" * 100)  # line 543
        _.createFile(2, "y")  # line 544
        sos.offline("test", remotes=[rmteFolder])  # file1-2  in initial branch commit  # line 545
        sos.branch("second")  # file1-2  switch, having same files  # line 546
        sos.switch("0")  # no change, switch back, no problem  # line 547
        sos.switch("second")  # no change  # switch back, no problem  # line 548
        _.createFile(3, "y")  # generate a file  # line 549
        try:  # uncommited changes detected  # line 550
            sos.switch("test")  # uncommited changes detected  # line 550
            _.fail()  # uncommited changes detected  # line 550
        except SystemExit as E:  # line 551
            _.assertEqual(1, E.code)  # line 551
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 552
        sos.changes()  # line 553
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 554
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 555
        _.createFile("XXX")  # line 556
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 557
        _.assertIn("File tree has changes", out)  # line 558
        _.assertNotIn("File tree is unchanged", out)  # line 559
        _.assertIn("  * b0   'test'", out)  # line 560
        _.assertIn("    b1 'second'", out)  # line 561
        _.assertIn("modified", out)  # one branch has commits  # line 562
        _.assertIn("in sync", out)  # the other doesn't  # line 563
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 564
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 565
        _.assertAllIn(["Metadata format", "Content checking:    %ssize & timestamp" % sos.Fore.BLUE, "Data compression:    %sdeactivated" % sos.Fore.BLUE, "Repository mode:     %ssimple" % sos.Fore.GREEN, "Number of branches:  2"], out)  # line 566
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 567
        _.createFile(4, "xy")  # generate a file  # line 568
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 569
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 570
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 571
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 572
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 573
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 574
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 575
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 576
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 577
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 578
        _.assertNotIn("Creating backup", out)  # line 579
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 580
        _.assertIn("Dumping revisions", out)  # line 581
        _.assertNotIn("Creating backup", out)  # line 582
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 583
        _.assertAllIn(["Creating backup"], out)  # line 584
        _.assertIn("Dumping revisions", out)  # line 585
        sos.verbose.pop()  # line 586
        _.remoteIsSame()  # line 587
        os.chdir(rmteFolder)  # line 588
        try:  # line 589
            sos.status()  # line 589
        except SystemExit as E:  # line 590
            _.assertEqual(1, E.code)  # line 590

    def testAutoDetectVCS(_):  # line 592
        os.mkdir(".git")  # line 593
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 594
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 595
            meta = fd.read()  # line 595
        _.assertTrue("\"master\"" in meta)  # line 596
        os.rmdir(".git")  # line 597

    def testUpdate(_):  # line 599
        sos.offline("trunk")  # create initial branch b0/r0  # line 600
        _.createFile(1, "x" * 100)  # line 601
        sos.commit("second")  # create b0/r1  # line 602

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 604
        _.assertFalse(_.existsFile(1))  # line 605

        sos.update("/1")  # recreate file1  # line 607
        _.assertTrue(_.existsFile(1))  # line 608

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 610
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 611
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 612
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 613

        sos.update("/1")  # do nothing, as nothing has changed  # line 615
        _.assertTrue(_.existsFile(1))  # line 616

        _.createFile(2, "y" * 100)  # line 618
#    out:str = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 621
        _.assertTrue(_.existsFile(2))  # line 622
        sos.update("trunk", ["--add"])  # only add stuff  # line 623
        _.assertTrue(_.existsFile(2))  # line 624
        sos.update("trunk")  # nothing to do  # line 625
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 626

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 628
        _.createFile(10, theirs)  # line 629
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 630
        _.createFile(11, mine)  # line 631
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 632
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 633

    def testUpdate2(_):  # line 635
        _.createFile("test.txt", "x" * 10)  # line 636
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 637
        sync()  # line 638
        sos.branch("mod")  # line 639
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 640
        sos.commit("mod")  # create b0/r1  # line 641
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 642
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 643
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 644
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 645
        _.createFile("test.txt", "x" * 10)  # line 646
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 647
        sync()  # line 648
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 649
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 650
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 651
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 652
        sync()  # line 653
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 654
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 655

    def testIsTextType(_):  # line 657
        m = sos.Metadata(".")  # line 658
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 659
        m.c.bintype = ["*.md.confluence"]  # line 660
        _.assertTrue(m.isTextType("ab.txt"))  # line 661
        _.assertTrue(m.isTextType("./ab.txt"))  # line 662
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 663
        _.assertFalse(m.isTextType("bc/ab."))  # line 664
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 665
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 666
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 667
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 668

    def testEolDet(_):  # line 670
        ''' Check correct end-of-line detection. '''  # line 671
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 672
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 673
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 674
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 675
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 676
        _.assertIsNone(sos.eoldet(b""))  # line 677
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 678

    def testMergeClassic(_):  # line 680
        _.createFile(1, contents=b"abcdefg")  # line 681
        b = b"iabcxeg"  # type: bytes  # line 682
        _.assertEqual.__self__.maxDiff = None  # to get a full diff  # line 683
        out = wrapChannels(lambda _=None: sos.mergeClassic(b, "file1", "from", "to", 24523234, 1))  # type: str  # line 684
        try:  # line 685
            _.assertAllIn(["*** from\tThu Jan  1 07:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # line 685
        except:  # differing local time on CI system TODO make this better  # line 686
            _.assertAllIn(["*** from\tThu Jan  1 06:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # differing local time on CI system TODO make this better  # line 686

    def testMerge(_):  # line 688
        ''' Check merge results depending on user options. '''  # line 689
        a = b"a\nb\ncc\nd"  # type: bytes  # line 690
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 691
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 692
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 693
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 694
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 695
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 696
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 697
        a = b"a\nb\ncc\nd"  # line 698
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 699
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 700
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 701
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 702
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 704
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 705
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 707
        b = b"a\nc\ne"  # line 708
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 709
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 710
        a = b"a\nb\ne"  # intra-line merge  # line 711
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 712
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 713
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 714
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 715
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 716
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 717

    def testMergeEol(_):  # line 719
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 720
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 721
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 722
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 723
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 724

    def testPickyMode(_):  # line 726
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 727
        sos.offline("trunk", None, ["--picky"])  # line 728
        changes = sos.changes()  # line 729
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 730
        out = wrapChannels(lambda _=None: sos.add(["."], ["./file?"], options=["--force", "--relative"]))  # type: str  # line 731
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", "'.'"], out)  # line 732
        _.createFile(1, "aa")  # line 733
        sos.commit("First")  # add one file  # line 734
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 735
        _.createFile(2, "b")  # line 736
        try:  # add nothing, because picky  # line 737
            sos.commit("Second")  # add nothing, because picky  # line 737
        except:  # line 738
            pass  # line 738
        sos.add(["."], ["./file?"])  # line 739
        sos.commit("Third")  # line 740
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 741
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 742
        _.assertIn("    r0", out)  # line 743
        sys.argv.extend(["-n", "2"])  # We cannot use the opions array for named argument options  # line 744
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 745
        sys.argv.pop()  # line 746
        sys.argv.pop()  # line 746
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 747
        _.assertIn("    r1", out)  # line 748
        _.assertIn("  * r2", out)  # line 749
        try:  # line 750
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 750
        except SystemExit as E:  # line 751
            _.assertEqual(0, E.code)  # line 751
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 752
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 753
        _.assertNotIn("    r1", out)  # line 754
        _.assertIn("  * r2", out)  # line 755
        _.createFile(3, prefix="sub")  # line 756
        sos.add(["sub"], ["sub/file?"])  # line 757
        changes = sos.changes()  # line 758
        _.assertEqual(1, len(changes.additions))  # line 759
        _.assertTrue("sub/file3" in changes.additions)  # line 760

    def testTrackedSubfolder(_):  # line 762
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 763
        os.mkdir("." + os.sep + "sub")  # line 764
        sos.offline("trunk", None, ["--track"])  # line 765
        _.createFile(1, "x")  # line 766
        _.createFile(1, "x", prefix="sub")  # line 767
        sos.add(["."], ["./file?"])  # add glob pattern to track  # line 768
        sos.commit("First")  # line 769
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 770
        sos.add(["."], ["sub/file?"])  # add glob pattern to track  # line 771
        sos.commit("Second")  # one new file + meta  # line 772
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 773
        os.unlink("file1")  # remove from basefolder  # line 774
        _.createFile(2, "y")  # line 775
        sos.remove(["."], ["sub/file?"])  # line 776
        try:  # TODO check more textual details here  # line 777
            sos.remove(["."], ["sub/bla"])  # TODO check more textual details here  # line 777
            _.fail("Expected exit")  # TODO check more textual details here  # line 777
        except SystemExit as E:  # line 778
            _.assertEqual(1, E.code)  # line 778
        sos.commit("Third")  # line 779
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 780
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 783
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 788
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 789
        _.createFile(1)  # line 790
        _.createFile("a123a")  # untracked file "a123a"  # line 791
        sos.add(["."], ["./file?"])  # add glob tracking pattern  # line 792
        sos.commit("second")  # versions "file1"  # line 793
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 794
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 795
        _.assertTrue(any(("|" in o and "./file?" in o for o in out.split("\n"))))  # line 796

        _.createFile(2)  # untracked file "file2"  # line 798
        sos.commit("third")  # versions "file2"  # line 799
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 800

        os.mkdir("." + os.sep + "sub")  # line 802
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 803
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 804
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 805

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 807
        sos.remove(["."], ["./file?"])  # remove tracking pattern, but don't touch previously created and versioned files  # line 808
        sos.add([".", "."], ["./a*a", "./a*?"])  # add tracking pattern  # line 809
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 810
        _.assertEqual(0, len(changes.modifications))  # line 811
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 812
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 813

        sos.commit("Second_2")  # line 815
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 816
        _.existsFile(1, b"x" * 10)  # line 817
        _.existsFile(2, b"x" * 10)  # line 818

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 820
        _.existsFile(1, b"x" * 10)  # line 821
        _.existsFile("a123a", b"x" * 10)  # line 822

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 824
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 825
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 826

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 828
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 829
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 830
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 831
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 832
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 833
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 834
# TODO test switch --meta

    def testLsTracked(_):  # line 837
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 838
        _.createFile(1)  # line 839
        _.createFile("foo")  # line 840
        sos.add(["."], ["./file*"])  # capture one file  # line 841
        sos.ls()  # line 842
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # type: str  # line 843
        _.assertInAny("TRK file1  (file*)", out)  # line 844
        _.assertNotInAny("... file1  (file*)", out)  # line 845
        _.assertInAny("    foo", out)  # line 846
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 847
        _.assertInAny("TRK file*", out)  # line 848
        _.createFile("a", prefix="sub")  # line 849
        sos.add(["sub"], ["sub/a"])  # line 850
        sos.ls("sub")  # line 851
        _.assertInAny("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 852

    def testLineMerge(_):  # line 854
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 855
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 856
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 857
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 858

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 860
        _.createFile(1)  # line 861
        sos.offline("master", options=["--force"])  # line 862
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # type: str  # line 863
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 864
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 865
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 866
        _.createFile(2)  # line 867
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 868
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 869
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 870
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 871

    def testLocalConfig(_):  # line 873
        sos.offline("bla", options=[])  # line 874
        try:  # line 875
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 875
        except SystemExit as E:  # line 876
            _.assertEqual(0, E.code)  # line 876
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 877

    def testConfigVariations(_):  # line 879
        def makeRepo():  # line 880
            try:  # line 881
                os.unlink("file1")  # line 881
            except:  # line 882
                pass  # line 882
            sos.offline("master", options=["--force"])  # line 883
            _.createFile(1)  # line 884
            sos.commit("Added file1")  # line 885
        try:  # line 886
            sos.config(["set", "strict", "on"])  # line 886
        except SystemExit as E:  # line 887
            _.assertEqual(0, E.code)  # line 887
        makeRepo()  # line 888
        _.assertTrue(checkRepoFlag("strict", True))  # line 889
        try:  # line 890
            sos.config(["set", "strict", "off"])  # line 890
        except SystemExit as E:  # line 891
            _.assertEqual(0, E.code)  # line 891
        makeRepo()  # line 892
        _.assertTrue(checkRepoFlag("strict", False))  # line 893
        try:  # line 894
            sos.config(["set", "strict", "yes"])  # line 894
        except SystemExit as E:  # line 895
            _.assertEqual(0, E.code)  # line 895
        makeRepo()  # line 896
        _.assertTrue(checkRepoFlag("strict", True))  # line 897
        try:  # line 898
            sos.config(["set", "strict", "no"])  # line 898
        except SystemExit as E:  # line 899
            _.assertEqual(0, E.code)  # line 899
        makeRepo()  # line 900
        _.assertTrue(checkRepoFlag("strict", False))  # line 901
        try:  # line 902
            sos.config(["set", "strict", "1"])  # line 902
        except SystemExit as E:  # line 903
            _.assertEqual(0, E.code)  # line 903
        makeRepo()  # line 904
        _.assertTrue(checkRepoFlag("strict", True))  # line 905
        try:  # line 906
            sos.config(["set", "strict", "0"])  # line 906
        except SystemExit as E:  # line 907
            _.assertEqual(0, E.code)  # line 907
        makeRepo()  # line 908
        _.assertTrue(checkRepoFlag("strict", False))  # line 909
        try:  # line 910
            sos.config(["set", "strict", "true"])  # line 910
        except SystemExit as E:  # line 911
            _.assertEqual(0, E.code)  # line 911
        makeRepo()  # line 912
        _.assertTrue(checkRepoFlag("strict", True))  # line 913
        try:  # line 914
            sos.config(["set", "strict", "false"])  # line 914
        except SystemExit as E:  # line 915
            _.assertEqual(0, E.code)  # line 915
        makeRepo()  # line 916
        _.assertTrue(checkRepoFlag("strict", False))  # line 917
        try:  # line 918
            sos.config(["set", "strict", "enable"])  # line 918
        except SystemExit as E:  # line 919
            _.assertEqual(0, E.code)  # line 919
        makeRepo()  # line 920
        _.assertTrue(checkRepoFlag("strict", True))  # line 921
        try:  # line 922
            sos.config(["set", "strict", "disable"])  # line 922
        except SystemExit as E:  # line 923
            _.assertEqual(0, E.code)  # line 923
        makeRepo()  # line 924
        _.assertTrue(checkRepoFlag("strict", False))  # line 925
        try:  # line 926
            sos.config(["set", "strict", "enabled"])  # line 926
        except SystemExit as E:  # line 927
            _.assertEqual(0, E.code)  # line 927
        makeRepo()  # line 928
        _.assertTrue(checkRepoFlag("strict", True))  # line 929
        try:  # line 930
            sos.config(["set", "strict", "disabled"])  # line 930
        except SystemExit as E:  # line 931
            _.assertEqual(0, E.code)  # line 931
        makeRepo()  # line 932
        _.assertTrue(checkRepoFlag("strict", False))  # line 933
        try:  # line 934
            sos.config(["set", "strict", "nope"])  # line 934
            _.fail()  # line 934
        except SystemExit as E:  # line 935
            _.assertEqual(1, E.code)  # line 935

    def testLsSimple(_):  # line 937
        _.createFile(1)  # line 938
        _.createFile("foo")  # line 939
        _.createFile("ign1")  # line 940
        _.createFile("ign2")  # line 941
        _.createFile("bar", prefix="sub")  # line 942
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 943
        try:  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 944
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 944
        except SystemExit as E:  # line 945
            _.assertEqual(0, E.code)  # line 945
        try:  # additional ignore pattern  # line 946
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 946
        except SystemExit as E:  # line 947
            _.assertEqual(0, E.code)  # line 947
        try:  # define a list of ignore patterns  # line 948
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 948
        except SystemExit as E:  # line 949
            _.assertEqual(0, E.code)  # line 949
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # type: str  # line 950
        _.assertAllIn(["             ignores", "[global]", "['ign1', 'ign2']"], out)  # line 951
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 952
        _.assertAllIn(["             ignores", "[global]", "['ign1', 'ign2']"], out)  # line 953
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 954
        _.assertInAny('    file1', out)  # line 955
        _.assertInAny('    ign1', out)  # line 956
        _.assertInAny('    ign2', out)  # line 957
        _.assertNotIn('DIR sub', out)  # line 958
        _.assertNotIn('    bar', out)  # line 959
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 960
        _.assertIn('DIR sub', out)  # line 961
        _.assertIn('    bar', out)  # line 962
        try:  # line 963
            sos.config(["rm", "foo", "bar"])  # line 963
            _.fail()  # line 963
        except SystemExit as E:  # line 964
            _.assertEqual(1, E.code)  # line 964
        try:  # line 965
            sos.config(["rm", "ignores", "foo"])  # line 965
            _.fail()  # line 965
        except SystemExit as E:  # line 966
            _.assertEqual(1, E.code)  # line 966
        try:  # line 967
            sos.config(["rm", "ignores", "ign1"])  # line 967
        except SystemExit as E:  # line 968
            _.assertEqual(0, E.code)  # line 968
        try:  # remove ignore pattern  # line 969
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 969
        except SystemExit as E:  # line 970
            _.assertEqual(0, E.code)  # line 970
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 971
        _.assertInAny('    ign1', out)  # line 972
        _.assertInAny('IGN ign2', out)  # line 973
        _.assertNotInAny('    ign2', out)  # line 974

    def testWhitelist(_):  # line 976
# TODO test same for simple mode
        _.createFile(1)  # line 978
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 979
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 980
        sos.add(["."], ["./file*"])  # add tracking pattern for "file1"  # line 981
        sos.commit(options=["--force"])  # attempt to commit the file  # line 982
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 983
        try:  # Exit because dirty  # line 984
            sos.online()  # Exit because dirty  # line 984
            _.fail()  # Exit because dirty  # line 984
        except:  # exception expected  # line 985
            pass  # exception expected  # line 985
        _.createFile("x2")  # add another change  # line 986
        sos.add(["."], ["./x?"])  # add tracking pattern for "file1"  # line 987
        try:  # force beyond dirty flag check  # line 988
            sos.online(["--force"])  # force beyond dirty flag check  # line 988
            _.fail()  # force beyond dirty flag check  # line 988
        except:  # line 989
            pass  # line 989
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 990
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 991

        _.createFile(1)  # line 993
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 994
        sos.offline("xx", None, ["--track"])  # line 995
        sos.add(["."], ["./file*"])  # line 996
        sos.commit()  # should NOT ask for force here  # line 997
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 998

    def testRemove(_):  # line 1000
        _.createFile(1, "x" * 100)  # line 1001
        sos.offline("trunk")  # line 1002
        try:  # line 1003
            sos.destroy("trunk")  # line 1003
            _fail()  # line 1003
        except:  # line 1004
            pass  # line 1004
        _.createFile(2, "y" * 10)  # line 1005
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 1006
        sos.destroy("trunk")  # line 1007
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 1008
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 1009
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 1010
        sos.branch("next")  # line 1011
        _.createFile(3, "y" * 10)  # make a change  # line 1012
        sos.destroy("added", "--force")  # should succeed  # line 1013

    def testFastBranchingOnEmptyHistory(_):  # line 1015
        ''' Test fast branching without revisions and with them. '''  # line 1016
        sos.offline(options=["--strict", "--compress"])  # b0  # line 1017
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 1018
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 1019
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 1020
        sos.destroy("2")  # line 1021
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 1022
        _.assertIn("b0 'trunk' @", out)  # line 1023
        _.assertIn("b1         @", out)  # line 1024
        _.assertIn("b3         @", out)  # line 1025
        _.assertNotIn("b2         @", out)  # line 1026
        sos.branch("", "")  # non-fast branching of b4  # line 1027
        _.createFile(1)  # line 1028
        _.createFile(2)  # line 1029
        sos.commit("")  # line 1030
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 1031
        sos.destroy("4")  # line 1032
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 1033
        _.assertIn("b0 'trunk' @", out)  # line 1034
        _.assertIn("b1         @", out)  # line 1035
        _.assertIn("b3         @", out)  # line 1036
        _.assertIn("b5         @", out)  # line 1037
        _.assertNotIn("b2         @", out)  # line 1038
        _.assertNotIn("b4         @", out)  # line 1039
# TODO add more files and branch again

    def testUsage(_):  # line 1042
        try:  # TODO expect sys.exit(0)  # line 1043
            sos.usage()  # TODO expect sys.exit(0)  # line 1043
            _.fail()  # TODO expect sys.exit(0)  # line 1043
        except:  # line 1044
            pass  # line 1044
        try:  # TODO expect sys.exit(0)  # line 1045
            sos.usage("help")  # TODO expect sys.exit(0)  # line 1045
            _.fail()  # TODO expect sys.exit(0)  # line 1045
        except:  # line 1046
            pass  # line 1046
        try:  # TODO expect sys.exit(0)  # line 1047
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 1047
            _.fail()  # TODO expect sys.exit(0)  # line 1047
        except:  # line 1048
            pass  # line 1048
        try:  # line 1049
            sos.usage(version=True)  # line 1049
            _.fail()  # line 1049
        except:  # line 1050
            pass  # line 1050
        try:  # line 1051
            sos.usage(version=True)  # line 1051
            _.fail()  # line 1051
        except:  # line 1052
            pass  # line 1052

    def testOnlyExcept(_):  # line 1054
        ''' Test blacklist glob rules. '''  # line 1055
        sos.offline(options=["--track"])  # line 1056
        _.createFile("a.1")  # line 1057
        _.createFile("a.2")  # line 1058
        _.createFile("b.1")  # line 1059
        _.createFile("b.2")  # line 1060
        sos.add(["."], ["./a.?"])  # line 1061
        sos.add(["."], ["./?.1"], negative=True)  # line 1062
        out = wrapChannels(lambda _=None: sos.commit())  # type: str  # line 1063
        _.assertIn("ADD ./a.2", out)  # line 1064
        _.assertNotIn("ADD ./a.1", out)  # line 1065
        _.assertNotIn("ADD ./b.1", out)  # line 1066
        _.assertNotIn("ADD ./b.2", out)  # line 1067

    def testOnly(_):  # line 1069
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",)), ["bla"]), sos.parseArgumentOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--remote", "bla", "--only"]))  # line 1070
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1071
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1072
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1073
        sos.offline(options=["--track", "--strict"])  # line 1074
        _.createFile(1)  # line 1075
        _.createFile(2)  # line 1076
        sos.add(["."], ["./file1"])  # line 1077
        sos.add(["."], ["./file2"])  # line 1078
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1079
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1080
        sos.commit()  # adds also file2  # line 1081
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1082
        _.createFile(1, "cc")  # modify both files  # line 1083
        _.createFile(2, "dd")  # line 1084
        try:  # line 1085
            sos.config(["set", "texttype", "file2"])  # line 1085
        except SystemExit as E:  # line 1086
            _.assertEqual(0, E.code)  # line 1086
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1087
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1088
        _.assertTrue("./file2" in changes.modifications)  # line 1089
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # line 1090
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1091
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1092
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # line 1093

    def testEmptyFiles(_):  # line 1095
        sos.offline()  # line 1096
        _.createFile(1, "")  # empty file  # line 1097
        sos.commit()  # line 1098
        changes = sos.changes()  # line 1099
        _.assertEqual(0, len(changes.additions) + len(changes.modifications) + len(changes.deletions))  # line 1100

        setRepoFlag("strict", True)  # line 1102
        changes = sos.changes()  # line 1103
        _.assertEqual(1, len(changes.modifications))  # because hash was set to None in simple mode  # line 1104
        sos.commit()  # commit now with hash computation  # line 1105
        setRepoFlag("strict", False)  # line 1106

        time.sleep(FS_PRECISION)  # line 1108
        _.createFile(1, "")  # touch file  # line 1109
        changes = sos.changes()  # line 1110
        _.assertEqual(1, len(changes.modifications))  # since modified timestamp  # line 1111

    def testDiff(_):  # line 1113
        try:  # manually mark this file as "textual"  # line 1114
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1114
        except SystemExit as E:  # line 1115
            _.assertEqual(0, E.code)  # line 1115
        sos.offline(options=["--strict"])  # line 1116
        _.createFile(1)  # line 1117
        _.createFile(2)  # line 1118
        sos.commit()  # line 1119
        _.createFile(1, "sdfsdgfsdf")  # line 1120
        _.createFile(2, "12343")  # line 1121
        sos.commit()  # line 1122
        _.createFile(1, "foobar")  # line 1123
        _.createFile(3)  # line 1124
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # type: str  # compare with r1 (second counting from last which is r2)  # line 1125
        _.assertIn("ADD ./file3", out)  # line 1126
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "old 0 |xxxxxxxxxx|", "now 0 |foobar|"], out)  # line 1127
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1128

    def testReorderRenameActions(_):  # line 1130
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1131
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1132
        try:  # line 1133
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1133
            _.fail()  # line 1133
        except:  # line 1134
            pass  # line 1134

    def testPublish(_):  # line 1136
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1137

    def testColorFlag(_):  # line 1139
        sos.offline()  # line 1140
        _.createFile(1)  # line 1141
#    setRepoFlag("useColorOutput", False, toConfig = True)
#    sos.Metadata.singleton = None  # for new slurp of configuration
        sos.enableColor(False, force=True)  # line 1144
        sos.verbose[:] = [None]  # set "true"  # line 1145
        out = wrapChannels(lambda _=None: sos.changes()).replace("\r\n", "\n").split("\n")  # type: List[str]  # line 1146
        _.assertTrue(any((line.startswith(sos.usage.MARKER_TEXT + "Changes of file tree") for line in out)))  # line 1147
#    setRepoFlag("useColorOutput", True,  toConfig = True)
#    sos.Metadata.singleton = None
        sos.enableColor(True, force=True)  # line 1150
        out = wrapChannels(lambda _=None: sos.changes()).replace("\r\n", "\n").split("\n")  # line 1151
        _.assertTrue(any((line.startswith((sos.usage.MARKER_TEXT if sys.platform == "win32" else sos.MARKER_COLOR) + "Changes of file tree") for line in out)))  # because it may start with a color code  # line 1152
        sos.verbose.pop()  # line 1153

    def testMove(_):  # line 1155
        ''' Move primarily modifies tracking patterns and moves files around accordingly. '''  # line 1156
        sos.offline(options=["--strict", "--track"])  # line 1157
        _.createFile(1)  # line 1158
        sos.add(["."], ["./file?"])  # line 1159
# assert error when source folder is missing
        out = wrapChannels(lambda _=None: sos.move("sub", "sub/file?", ".", "./?file"))  # type: str  # line 1161
        _.assertIn("Source folder doesn't exist", out)  # line 1162
        _.assertIn("EXIT CODE 1", out)  # line 1163
# if target folder missing: create it and move matching files into it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1165
        _.assertTrue(os.path.exists("sub"))  # line 1166
        _.assertTrue(os.path.exists("sub/file1"))  # line 1167
        _.assertFalse(os.path.exists("file1"))  # line 1168
# test move back to previous location, plus rename the file
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1170
        _.assertTrue(os.path.exists("1file"))  # line 1171
        _.assertFalse(os.path.exists("sub/file1"))  # line 1172
# assert error when nothing matches source pattern
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*"))  # line 1174
        _.assertIn("No files match the specified file pattern", out)  # line 1175
        _.assertIn("EXIT CODE", out)  # line 1176
        sos.add(["."], ["./*"])  # add catch-all tracking pattern to root folder  # line 1177
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*", options=["--force"]))  # line 1178
        _.assertIn("  './*' matches 3 files", out)  # line 1179
        _.assertIn("EXIT CODE", out)  # line 1180
# test rename no conflict
        _.createFile(1)  # line 1182
        _.createFile(2)  # line 1183
        _.createFile(3)  # line 1184
        sos.add(["."], ["./file*"])  # line 1185
        sos.remove(["."], ["./*"])  # line 1186
        try:  # define an ignore pattern  # line 1187
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1187
        except SystemExit as E:  # line 1188
            _.assertEqual(0, E.code)  # line 1188
        try:  # line 1189
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1189
        except SystemExit as E:  # line 1190
            _.assertEqual(0, E.code)  # line 1190
        sos.move(".", "./file*", ".", "./fi*le")  # should only move not ignored files files  # line 1191
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1192
        _.assertTrue(all((not os.path.exists("file%d" % i) for i in range(1, 4))))  # line 1193
        _.assertFalse(os.path.exists("fi4le"))  # line 1194
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1196
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(["."], ["./?file"])  # untrack pattern, which was renamed before  # line 1200
        sos.add(["."], ["./?a?b"], ["--force"])  # line 1201
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1202
        _.createFile("1a2b")  # should not be tracked  # line 1203
        _.createFile("a1b2")  # should be tracked  # line 1204
        sos.commit()  # line 1205
        _.assertEqual(5, len(os.listdir(sos.revisionFolder(0, 1))))  # meta, a1b2, fi[1-3]le  # line 1206
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1207
        _.createFile("1a1b1")  # line 1208
        _.createFile("1a1b2")  # line 1209
        sos.add(["."], ["./?a?b*"])  # line 1210
# test target pattern exists
        out = wrapChannels(lambda _=None: sos.move(".", "./?a?b*", ".", "./z?z?"))  # line 1212
        _.assertIn("not unique", out)  # line 1213
# TODO only rename if actually any files are versioned? or simply what is currently alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1217
        _.createFile(1)  # line 1218
        _.createFile(3)  # line 1219
        _.createFile(5)  # line 1220
        sos.offline()  # branch 0: only file1  # line 1221
        sos.branch()  # line 1222
        os.unlink("file1")  # line 1223
        os.unlink("file3")  # line 1224
        os.unlink("file5")  # line 1225
        _.createFile(2)  # line 1226
        _.createFile(4)  # line 1227
        _.createFile(6)  # line 1228
        sos.commit()  # branch 1: only file2  # line 1229
        sos.switch("0/")  # line 1230
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1231
        _.assertFalse(_.existsFile(1))  # line 1232
        _.assertFalse(_.existsFile(3))  # line 1233
        _.assertFalse(_.existsFile(5))  # line 1234
        _.assertTrue(_.existsFile(2))  # line 1235
        _.assertTrue(_.existsFile(4))  # line 1236
        _.assertTrue(_.existsFile(6))  # line 1237

    def testMoveDetection(_):  # line 1239
        _.createFile(1, "bla")  # line 1240
        sos.offline()  # line 1241
        os.mkdir("sub1")  # line 1242
        os.mkdir("sub2")  # line 1243
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1244
        shutil.move("file1", "sub2")  # line 1245
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 1246
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1247
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1248
        sos.commit("Moved the file")  # line 1249
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1253

    def testHashCollision(_):  # line 1255
        old = sos.Metadata.findChanges  # line 1256
        @_coconut_tco  # line 1257
        def patched(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[sos.ChangeSet, _coconut.typing.Optional[str]]':  # line 1257
            import collections  # used only in this method  # line 1258
            write = branch is not None and revision is not None  # line 1259
            if write:  # line 1260
                try:  # line 1261
                    os.makedirs(sos.encode(sos.revisionFolder(branch, revision, base=_.root)))  # line 1261
                except FileExistsError:  # HINT "try" only necessary for hash collision *test code* (!)  # line 1262
                    pass  # HINT "try" only necessary for hash collision *test code* (!)  # line 1262
            return _coconut_tail_call(old, _, branch, revision, checkContent, inverse, considerOnly, dontConsider, progress)  # line 1263
        sos.Metadata.findChanges = patched  # monkey-patch  # line 1264
        sos.offline()  # line 1265
        _.createFile(1)  # line 1266
        os.mkdir(sos.revisionFolder(0, 1))  # line 1267
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # hashed file name for not-yet-committed file1  # line 1268
        _.createFile(1)  # line 1269
        try:  # line 1270
            sos.commit()  # line 1270
            _.fail("Expected system exit due to hash collision detection")  # line 1270
        except SystemExit as E:  # HINT exit is implemented in utility.hashFile  # line 1271
            _.assertEqual(1, E.code)  # HINT exit is implemented in utility.hashFile  # line 1271
        sos.Metadata.findChanges = old  # revert monkey patch  # line 1272

    def testFindBase(_):  # line 1274
        old = os.getcwd()  # line 1275
        try:  # line 1276
            os.mkdir("." + os.sep + ".git")  # line 1277
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1278
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1279
            os.chdir("a" + os.sep + "b")  # line 1280
            s, vcs, cmd = sos.findSosVcsBase()  # line 1281
            _.assertIsNotNone(s)  # line 1282
            _.assertIsNotNone(vcs)  # line 1283
            _.assertEqual("git", cmd)  # line 1284
        finally:  # line 1285
            os.chdir(old)  # line 1285

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1296
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1297
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1298
