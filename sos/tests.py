#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x7b257ad8

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
sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 24
sos.defaults["useUnicodeFont"] = False  # because sos.main() is never called  # line 25


def determineFilesystemTimeResolution() -> 'float':  # line 28
    name = str(uuid.uuid4())  # type: str  # line 29
    with open(name, "w") as fd:  # create temporary file  # line 30
        fd.write("x")  # create temporary file  # line 30
    mt = os.stat(sos.encode(name)).st_mtime  # type: float  # get current timestamp  # line 31
    while os.stat(sos.encode(name)).st_mtime == mt:  # wait until timestamp modified  # line 32
        time.sleep(0.05)  # to avoid 0.00s bugs (came up some time for unknown reasons)  # line 33
        with open(name, "w") as fd:  # line 34
            fd.write("x")  # line 34
    mt, start, _count = os.stat(sos.encode(name)).st_mtime, time.time(), 0  # line 35
    while os.stat(sos.encode(name)).st_mtime == mt:  # now cound and measure time until modified again  # line 36
        time.sleep(0.05)  # line 37
        _count += 1  # line 38
        with open(name, "w") as fd:  # line 39
            fd.write("x")  # line 39
    os.unlink(name)  # line 40
    fsprecision = round(time.time() - start, 2)  # type: float  # line 41
    print("File system timestamp precision is %s%.2fs; wrote to the file %d times during that time" % ("probably even higher than " if fsprecision == 0.05 else "", fsprecision, _count))  # line 42
    return fsprecision  # line 43


FS_PRECISION = determineFilesystemTimeResolution() * 1.55  # line 46

def sync():  # line 48
    try:  # only Linux  if sys.version_info[:2] >= (3, 3):  # line 49
        os.sync()  # only Linux  if sys.version_info[:2] >= (3, 3):  # line 49
    except:  # Windows testing on AppVeyor  # line 50
        time.sleep(FS_PRECISION)  # Windows testing on AppVeyor  # line 50


@_coconut_tco  # line 53
def debugTestRunner(post_mortem=None):  # line 53
    ''' Unittest runner doing post mortem debugging on failing tests. '''  # line 54
    import pdb  # line 55
    if post_mortem is None:  # line 56
        post_mortem = pdb.post_mortem  # line 56
    class DebugTestResult(unittest.TextTestResult):  # line 57
        def addError(_, test, err):  # called before tearDown()  # line 58
            traceback.print_exception(*err)  # line 59
            post_mortem(err[2])  # line 60
            super(DebugTestResult, _).addError(test, err)  # line 61
        def addFailure(_, test, err):  # line 62
            traceback.print_exception(*err)  # line 63
            post_mortem(err[2])  # line 64
            super(DebugTestResult, _).addFailure(test, err)  # line 65
    return _coconut_tail_call(unittest.TextTestRunner, resultclass=DebugTestResult)  # line 66

@_coconut_tco  # line 68
def wrapChannels(func: '_coconut.typing.Callable[..., Any]') -> 'str':  # line 68
    ''' Wrap function call to capture and return strings emitted on stdout and stderr. '''  # line 69
    oldv, oldso, oldse = sys.argv, sys.stdout, sys.stderr  # line 70
    buf = TextIOWrapper(BufferedRandom(BytesIO(b"")), encoding=sos.UTF8)  # line 71
    handler = logging.StreamHandler(buf)  # TODO doesn't seem to be captured  # line 72
    sys.stdout = sys.stderr = buf  # line 73
    logging.getLogger().addHandler(handler)  # line 74
    try:  # capture output into buf  # line 75
        func()  # capture output into buf  # line 75
    except Exception as E:  # line 76
        buf.write(str(E) + "\n")  # line 76
        traceback.print_exc(file=buf)  # line 76
    except SystemExit as F:  # line 77
        buf.write("EXIT CODE %s" % F.code + "\n")  # line 77
        traceback.print_exc(file=buf)  # line 77
    logging.getLogger().removeHandler(handler)  # line 78
    sys.argv, sys.stdout, sys.stderr = oldv, oldso, oldse  # TODO when run using pythonw.exe and/or no console, these could be None  # line 79
    buf.seek(0)  # line 80
    return _coconut_tail_call(buf.read)  # line 81

def mockInput(datas: '_coconut.typing.Sequence[str]', func: '_coconut.typing.Callable[..., Any]') -> 'Any':  # line 83
    try:  # via python sos/tests.py  # line 84
        with mock.patch("sos._utility.input", side_effect=datas):  # line 85
            return func()  # line 85
    except:  # via setup.py  # line 86
        with mock.patch("sos.utility.input", side_effect=datas):  # line 87
            return func()  # line 87

def setRepoFlag(name: 'str', value: 'Any'):  # line 89
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 90
        flags, branches, config = json.loads(fd.read())  # line 90
    flags[name] = value  # line 91
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 92
        fd.write(json.dumps((flags, branches, config)))  # line 92

def checkRepoFlag(name: 'str', flag: '_coconut.typing.Optional[bool]'=None, value: '_coconut.typing.Optional[Any]'=None) -> 'bool':  # line 94
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 95
        flags, branches, config = json.loads(fd.read())  # line 95
    return (name in flags and flags[name] == flag) if flag is not None else (name in config and config[name] == value)  # line 96


class Tests(unittest.TestCase):  # line 99
    ''' Entire test suite. '''  # line 100

    def setUp(_):  # line 102
        sos.Metadata.singleton = None  # line 103
        for entry in os.listdir(testFolder):  # cannot reliably remove testFolder on Windows when using TortoiseSVN as VCS  # line 104
            resource = os.path.join(testFolder, entry)  # type: str  # line 105
            shutil.rmtree(sos.encode(resource)) if os.path.isdir(sos.encode(resource)) else os.unlink(sos.encode(resource))  # line 106
        os.chdir(testFolder)  # line 107

# Assertion helpers
    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]', only: 'bool'=False):  # line 110
        for w in what:  # line 111
            _.assertIn(w, where)  # line 111
        if only:  # line 112
            _.assertEqual(len(what), len(where))  # line 112

    def assertAllNotIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]'):  # line 114
        for w in what:  # line 115
            _.assertNotIn(w, where)  # line 115

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 117
        for w in where:  # line 118
            _.assertIn(what, w)  # line 118

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 120
        _.assertTrue(any((what in w for w in where)))  # line 120

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 122
        _.assertFalse(any((what in w for w in where)))  # line 122


# More helpers
    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None):  # line 126
        if prefix and not os.path.exists(prefix):  # line 127
            os.makedirs(prefix)  # line 127
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 128
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 128
        sync()  # line 129

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 131
        sync()  # line 132
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 133
            return False  # line 133
        if expectedContents is None:  # line 134
            return True  # line 134
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 135
            return fd.read() == expectedContents  # line 135

    def remoteIsSame(_):  # line 137
        sync()  # line 138
        for dirpath, dirnames, filenames in os.walk(os.path.join(testFolder, sos.metaFolder)):  # line 139
            rmtePath = os.path.normpath(os.path.join(rmteFolder, sos.metaFolder, os.path.relpath(dirpath, os.path.join(testFolder, sos.metaFolder))))  # type: str  # line 140
            others = os.listdir(rmtePath)  # type: List[str]  # line 141
            try:  # line 142
                _.assertAllIn(dirnames, others)  # line 142
                _.assertAllIn(others, dirnames + filenames)  # line 142
            except AssertionError as E:  # line 143
                raise AssertionError("Mismatch vs. remote: %r\n%r in %s" % (dirnames, others, dirpath)) from None  # line 143
            try:  # line 144
                _.assertAllIn(filenames, others)  # line 144
                _.assertAllIn(others, dirnames + filenames)  # line 144
            except AssertionError as E:  # line 145
                raise AssertionError("Mismatch vs. remote: %r\n% in %sr" % (filenames, others, dirpath)) from None  # line 145


# Uni tests
    def testAccessor(_):  # line 149
        a = sos.Accessor({"a": 1})  # line 150
        _.assertEqual((1, 1), (a["a"], a.a))  # line 151

    def testIndexing(_):  # line 153
        m = sos.Metadata()  # line 154
        m.commits = {}  # line 155
        _.assertEqual(1, m.correctNegativeIndexing(1))  # line 156
        _.assertEqual(9999999999999999, m.correctNegativeIndexing(9999999999999999))  # line 157
        _.assertEqual(0, m.correctNegativeIndexing(0))  # zero always returns zero, even no commits present  # line 158
        try:  # line 159
            m.correctNegativeIndexing(-1)  # line 159
            _.fail()  # line 159
        except SystemExit as E:  # line 160
            _.assertEqual(1, E.code)  # line 160
        m.commits = {0: sos.CommitInfo(0, 0), 1: sos.CommitInfo(1, 0)}  # line 161
        _.assertEqual(1, m.correctNegativeIndexing(-1))  # zero always returns zero, even no commits present  # line 162
        _.assertEqual(0, m.correctNegativeIndexing(-2))  # zero always returns zero, even no commits present  # line 163
        try:  # line 164
            m.correctNegativeIndexing(-3)  # line 164
            _.fail()  # line 164
        except SystemExit as E:  # line 165
            _.assertEqual(1, E.code)  # line 165

    def testRestoreFile(_):  # line 167
        m = sos.Metadata()  # line 168
        os.makedirs(sos.revisionFolder(0, 0))  # line 169
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 170
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 171
        _.assertTrue(_.existsFile("restored", b""))  # line 172

    def testGetAnyOfmap(_):  # line 174
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 175
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 176

    def testAjoin(_):  # line 178
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 179
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 180

    def testFindChanges(_):  # line 182
        m = sos.Metadata(os.getcwd())  # line 183
        try:  # line 184
            sos.config(["set", "texttype", "*"])  # line 184
        except SystemExit as E:  # line 185
            _.assertEqual(0, E.code)  # line 185
        try:  # will be stripped from leading paths anyway  # line 186
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 186
        except SystemExit as E:  # line 187
            _.assertEqual(0, E.code)  # line 187
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 188
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 189
            os.unlink(file)  # remove configuration file  # line 189
        _.createFile(1, "1")  # line 190
        m.createBranch(0)  # line 191
        _.assertEqual(1, len(m.paths))  # line 192
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 193
        _.createFile(1, "2")  # modify existing file  # line 194
        _.createFile(2, "2")  # add another file  # line 195
        m.loadCommit(0, 0)  # line 196
        changes, msg = m.findChanges()  # detect time skew  # line 197
        _.assertEqual(1, len(changes.additions))  # line 198
        _.assertEqual(0, len(changes.deletions))  # line 199
        _.assertEqual(1, len(changes.modifications))  # line 200
        _.assertEqual(0, len(changes.moves))  # line 201
        m.paths.update(changes.additions)  # line 202
        m.paths.update(changes.modifications)  # line 203
        _.createFile(2, "12")  # modify file again  # line 204
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 205
        _.assertEqual(0, len(changes.additions))  # line 206
        _.assertEqual(0, len(changes.deletions))  # line 207
        _.assertEqual(1, len(changes.modifications))  # line 208
        _.assertEqual(0, len(changes.moves))  # line 209
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 210
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 211
# TODO test moves

    def testDumpSorting(_):  # line 214
        m = sos.Metadata()  # type: Metadata  # line 215
        _.createFile(1)  # line 216
        sos.offline()  # line 217
        _.createFile(2)  # line 218
        _.createFile(3)  # line 219
        sos.commit()  # line 220
        _.createFile(4)  # line 221
        _.createFile(5)  # line 222
        sos.commit()  # line 223
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # type: List[str]  # line 224
        _.assertTrue(out.index("b0%sr2" % os.sep) > out.index("b0%sr1" % os.sep))  # line 225
        _.assertTrue(out.index("b0%sr1" % os.sep) > out.index("b0%sr0" % os.sep))  # line 226

    def testFitStrings(_):  # line 228
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 229
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 230
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 231
    def testMoves(_):  # line 232
        _.createFile(1, "1")  # line 233
        _.createFile(2, "2", "sub")  # line 234
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 235
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 236
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 237
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 238
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 239
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 240
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # line 241
        _.assertIn("MOV ..%sfile2  <-  file2" % os.sep, out)  # no ./ for relative OS-specific paths  # line 242
        _.assertIn("MOV file1  <-  ..%sfile1" % os.sep, out)  # line 243
        out = wrapChannels(lambda _=None: sos.commit())  # line 244
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 245
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 246
        _.assertAllIn(["Created new revision r01", "summing 628 bytes in 2 files (88.22% SOS overhead)"], out)  # TODO why is this not captured?  # line 247

    def testPatternPaths(_):  # line 249
        sos.offline(options=["--track"])  # line 250
        os.mkdir("sub")  # line 251
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 252
        out = wrapChannels(lambda _=None: sos.add("sub", "sub/file?"))  # type: str  # line 253
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", os.path.abspath("sub")], out)  # line 254
        sos.commit("test")  # should pick up sub/file1 pattern  # line 255
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 256
        _.createFile(1)  # line 257
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 258
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 258
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 258
        except:  # line 259
            pass  # line 259

    def testNoArgs(_):  # line 261
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 262

    def testAutoMetadataUpgrade(_):  # line 264
        sos.offline()  # line 265
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 266
            repo, branches, config = json.load(fd)  # line 266
        repo["version"] = None  # lower than any pip version  # line 267
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 268
        del repo["format"]  # simulate pre-1.3.5  # line 269
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 270
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 270
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # type: str  # line 271
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 272

    def testFastBranching(_):  # line 274
        _.createFile(1)  # line 275
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict", "--verbose"]))  # type: str  # b0/r0 = ./file1  # line 276
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 277
        _.createFile(2)  # line 278
        os.unlink("file1")  # line 279
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 280
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 281
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 282
        _.createFile(3)  # line 283
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 284
        _.assertAllIn([sos.metaFile, sos.metaBack, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 285
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 286
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 287
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 288
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 289
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 290
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 293
        now = time.time()  # type: float  # line 294
        _.createFile(1)  # line 295
        sync()  # line 296
        sos.offline(options=["--strict"])  # line 297
        _.createFile(1, "abc")  # modify contents  # line 298
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 299
        sync()  # line 300
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 301
        _.assertIn("<older than previously committed>", out)  # line 302
        out = wrapChannels(lambda _=None: sos.commit())  # line 303
        _.assertIn("<older than previously committed>", out)  # line 304

    def testGetParentBranch(_):  # line 306
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 307
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 308
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 309
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 310
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 311

    def testTokenizeGlobPattern(_):  # line 313
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 314
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 315
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 316
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 317
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 318
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 319

    def testTokenizeGlobPatterns(_):  # line 321
        try:  # because number of literal strings differs  # line 322
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 322
            _.fail()  # because number of literal strings differs  # line 322
        except:  # line 323
            pass  # line 323
        try:  # because glob patterns differ  # line 324
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 324
            _.fail()  # because glob patterns differ  # line 324
        except:  # line 325
            pass  # line 325
        try:  # glob patterns differ, regardless of position  # line 326
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 326
            _.fail()  # glob patterns differ, regardless of position  # line 326
        except:  # line 327
            pass  # line 327
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 328
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 329
        try:  # succeeds, because glob patterns match (differ only in position)  # line 330
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 330
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 330
        except:  # line 331
            pass  # line 331

    def testConvertGlobFiles(_):  # line 333
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 334
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 335

    def testFolderRemove(_):  # line 337
        m = sos.Metadata(os.getcwd())  # line 338
        _.createFile(1)  # line 339
        _.createFile("a", prefix="sub")  # line 340
        sos.offline()  # line 341
        _.createFile(2)  # line 342
        os.unlink("sub" + os.sep + "a")  # line 343
        os.rmdir("sub")  # line 344
        changes = sos.changes()  # TODO replace by output check  # line 345
        _.assertEqual(1, len(changes.additions))  # line 346
        _.assertEqual(0, len(changes.modifications))  # line 347
        _.assertEqual(1, len(changes.deletions))  # line 348
        _.createFile("a", prefix="sub")  # line 349
        changes = sos.changes()  # line 350
        _.assertEqual(0, len(changes.deletions))  # line 351

    def testSwitchConflict(_):  # line 353
        sos.offline(options=["--strict"])  # (r0)  # line 354
        _.createFile(1)  # line 355
        sos.commit()  # add file (r1)  # line 356
        os.unlink("file1")  # line 357
        sos.commit()  # remove (r2)  # line 358
        _.createFile(1, "something else")  # line 359
        sos.commit()  # (r3)  # line 360
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 361
        _.existsFile(1, "x" * 10)  # line 362
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 363
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 364
        sos.switch("/1")  # add file1 back  # line 365
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 366
        _.existsFile(1, "something else")  # line 367

    def testComputeSequentialPathSet(_):  # line 369
        os.makedirs(sos.revisionFolder(0, 0))  # line 370
        os.makedirs(sos.revisionFolder(0, 1))  # line 371
        os.makedirs(sos.revisionFolder(0, 2))  # line 372
        os.makedirs(sos.revisionFolder(0, 3))  # line 373
        os.makedirs(sos.revisionFolder(0, 4))  # line 374
        m = sos.Metadata(os.getcwd())  # line 375
        m.branch = 0  # line 376
        m.commit = 2  # line 377
        m.saveBranches()  # line 378
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 379
        m.saveCommit(0, 0)  # initial  # line 380
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 381
        m.saveCommit(0, 1)  # mod  # line 382
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 383
        m.saveCommit(0, 2)  # add  # line 384
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 385
        m.saveCommit(0, 3)  # del  # line 386
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 387
        m.saveCommit(0, 4)  # readd  # line 388
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 389
        m.saveBranch(0)  # line 390
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 391
        m.saveBranches()  # line 392
        m.computeSequentialPathSet(0, 4)  # line 393
        _.assertEqual(2, len(m.paths))  # line 394

    def testParseRevisionString(_):  # line 396
        m = sos.Metadata(os.getcwd())  # line 397
        m.branch = 1  # line 398
        m.commits = {0: 0, 1: 1, 2: 2}  # line 399
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 400
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 401
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 402
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 403
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 404
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 405
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 406

    def testOfflineEmpty(_):  # line 408
        os.mkdir("." + os.sep + sos.metaFolder)  # line 409
        try:  # line 410
            sos.offline("trunk")  # line 410
            _.fail()  # line 410
        except SystemExit as E:  # line 411
            _.assertEqual(1, E.code)  # line 411
        os.rmdir("." + os.sep + sos.metaFolder)  # line 412
        sos.offline("test")  # line 413
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 414
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 415
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 416
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 417
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 418
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 419

    def testOfflineWithFiles(_):  # line 421
        _.createFile(1, "x" * 100)  # line 422
        _.createFile(2)  # line 423
        sos.offline("test")  # line 424
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 425
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 426
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 427
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 428
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 429
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 430
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 431

    def testBranch(_):  # line 433
        _.createFile(1, "x" * 100)  # line 434
        _.createFile(2)  # line 435
        sos.offline("test")  # b0/r0  # line 436
        sos.branch("other")  # b1/r0  # line 437
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 438
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 439
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 441
        _.createFile(1, "z")  # modify file  # line 443
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 444
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 445
        _.createFile(3, "z")  # line 447
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 448
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 449
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 454
        _.createFile(1, "x" * 100)  # line 455
        _.createFile(2)  # line 456
        sos.offline("test")  # line 457
        changes = sos.changes()  # line 458
        _.assertEqual(0, len(changes.additions))  # line 459
        _.assertEqual(0, len(changes.deletions))  # line 460
        _.assertEqual(0, len(changes.modifications))  # line 461
        _.createFile(1, "z")  # size change  # line 462
        changes = sos.changes()  # line 463
        _.assertEqual(0, len(changes.additions))  # line 464
        _.assertEqual(0, len(changes.deletions))  # line 465
        _.assertEqual(1, len(changes.modifications))  # line 466
        sos.commit("message")  # line 467
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 468
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 469
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 470
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 471
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 472
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 473
        os.unlink("file2")  # line 474
        changes = sos.changes()  # line 475
        _.assertEqual(0, len(changes.additions))  # line 476
        _.assertEqual(1, len(changes.deletions))  # line 477
        _.assertEqual(1, len(changes.modifications))  # line 478
        sos.commit("modified")  # line 479
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 480
        try:  # expecting Exit due to no changes  # line 481
            sos.commit("nothing")  # expecting Exit due to no changes  # line 481
            _.fail()  # expecting Exit due to no changes  # line 481
        except:  # line 482
            pass  # line 482

    def testGetBranch(_):  # line 484
        m = sos.Metadata(os.getcwd())  # line 485
        m.branch = 1  # current branch  # line 486
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 487
        _.assertEqual(27, m.getBranchByName(27))  # line 488
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 489
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 490
        _.assertIsNone(m.getBranchByName("unknown"))  # line 491
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 492
        _.assertEqual(13, m.getRevisionByName("13"))  # line 493
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 494
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 495

    def testTagging(_):  # line 497
        m = sos.Metadata(os.getcwd())  # line 498
        sos.offline()  # line 499
        _.createFile(111)  # line 500
        sos.commit("tag", ["--tag"])  # line 501
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # type: str  # line 502
        _.assertTrue(any(("|tag" in line and line.endswith("|%sTAG%s" % (sos.Fore.MAGENTA, sos.Fore.RESET)) for line in out)))  # line 503
        _.createFile(2)  # line 504
        try:  # line 505
            sos.commit("tag")  # line 505
            _.fail()  # line 505
        except:  # line 506
            pass  # line 506
        sos.commit("tag-2", ["--tag"])  # line 507
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 508
        _.assertIn("TAG tag", out)  # line 509

    def testSwitch(_):  # line 511
        try: shutil.rmtree(os.path.join(rmteFolder, sos.metaFolder))  # line 512
        except: pass
        _.createFile(1, "x" * 100)  # line 513
        _.createFile(2, "y")  # line 514
        import pdb; pdb.set_trace()
        sos.offline("test", remotes=[rmteFolder])  # file1-2  in initial branch commit  # line 515
        sos.branch("second")  # file1-2  switch, having same files  # line 516
        sos.switch("0")  # no change, switch back, no problem  # line 517
        sos.switch("second")  # no change  # switch back, no problem  # line 518
        _.createFile(3, "y")  # generate a file  # line 519
        try:  # uncommited changes detected  # line 520
            sos.switch("test")  # uncommited changes detected  # line 520
            _.fail()  # uncommited changes detected  # line 520
        except SystemExit as E:  # line 521
            _.assertEqual(1, E.code)  # line 521
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 522
        sos.changes()  # line 523
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 524
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 525
        _.createFile("XXX")  # line 526
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 527
        _.assertIn("File tree has changes", out)  # line 528
        _.assertNotIn("File tree is unchanged", out)  # line 529
        _.assertIn("  * b0   'test'", out)  # line 530
        _.assertIn("    b1 'second'", out)  # line 531
        _.assertIn("modified", out)  # one branch has commits  # line 532
        _.assertIn("in sync", out)  # the other doesn't  # line 533
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 534
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 535
        _.assertAllIn(["Metadata format", "Content checking:    %sdeactivated" % sos.Fore.BLUE, "Data compression:    %sdeactivated" % sos.Fore.BLUE, "Repository mode:     %ssimple" % sos.Fore.GREEN, "Number of branches:  2"], out)  # line 536
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 537
        _.createFile(4, "xy")  # generate a file  # line 538
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 539
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 540
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 541
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 542
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 543
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 544
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 545
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 546
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 547
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 548
        _.assertNotIn("Creating backup", out)  # line 549
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 550
        _.assertIn("Dumping revisions", out)  # line 551
        _.assertNotIn("Creating backup", out)  # line 552
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 553
        _.assertAllIn(["Creating backup"], out)  # line 554
        _.assertIn("Dumping revisions", out)  # line 555
        sos.verbose.pop()  # line 556
        _.remoteIsSame()  # line 557

    def testAutoDetectVCS(_):  # line 559
        os.mkdir(".git")  # line 560
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 561
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 562
            meta = fd.read()  # line 562
        _.assertTrue("\"master\"" in meta)  # line 563
        os.rmdir(".git")  # line 564

    def testUpdate(_):  # line 566
        sos.offline("trunk")  # create initial branch b0/r0  # line 567
        _.createFile(1, "x" * 100)  # line 568
        sos.commit("second")  # create b0/r1  # line 569

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 571
        _.assertFalse(_.existsFile(1))  # line 572

        sos.update("/1")  # recreate file1  # line 574
        _.assertTrue(_.existsFile(1))  # line 575

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 577
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 578
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 579
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 580

        sos.update("/1")  # do nothing, as nothing has changed  # line 582
        _.assertTrue(_.existsFile(1))  # line 583

        _.createFile(2, "y" * 100)  # line 585
#    out:str = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 588
        _.assertTrue(_.existsFile(2))  # line 589
        sos.update("trunk", ["--add"])  # only add stuff  # line 590
        _.assertTrue(_.existsFile(2))  # line 591
        sos.update("trunk")  # nothing to do  # line 592
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 593

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 595
        _.createFile(10, theirs)  # line 596
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 597
        _.createFile(11, mine)  # line 598
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 599
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 600

    def testUpdate2(_):  # line 602
        _.createFile("test.txt", "x" * 10)  # line 603
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 604
        sync()  # line 605
        sos.branch("mod")  # line 606
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 607
        sos.commit("mod")  # create b0/r1  # line 608
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 609
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 610
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 611
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 612
        _.createFile("test.txt", "x" * 10)  # line 613
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 614
        sync()  # line 615
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 616
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 617
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 618
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 619
        sync()  # line 620
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 621
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 622

    def testIsTextType(_):  # line 624
        m = sos.Metadata(".")  # line 625
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 626
        m.c.bintype = ["*.md.confluence"]  # line 627
        _.assertTrue(m.isTextType("ab.txt"))  # line 628
        _.assertTrue(m.isTextType("./ab.txt"))  # line 629
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 630
        _.assertFalse(m.isTextType("bc/ab."))  # line 631
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 632
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 633
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 634
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 635

    def testEolDet(_):  # line 637
        ''' Check correct end-of-line detection. '''  # line 638
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 639
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 640
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 641
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 642
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 643
        _.assertIsNone(sos.eoldet(b""))  # line 644
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 645

    def testMerge(_):  # line 647
        ''' Check merge results depending on user options. '''  # line 648
        a = b"a\nb\ncc\nd"  # type: bytes  # line 649
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 650
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 651
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 652
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 653
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 654
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 655
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 656
        a = b"a\nb\ncc\nd"  # line 657
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 658
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 659
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 660
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 661
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 663
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 664
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 666
        b = b"a\nc\ne"  # line 667
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 668
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 669
        a = b"a\nb\ne"  # intra-line merge  # line 670
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 671
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 672
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 673
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 674
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 675
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 676

    def testMergeEol(_):  # line 678
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 679
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 680
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 681
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 682
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 683

    def testPickyMode(_):  # line 685
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 686
        sos.offline("trunk", None, ["--picky"])  # line 687
        changes = sos.changes()  # line 688
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 689
        out = wrapChannels(lambda _=None: sos.add(".", "./file?", options=["--force", "--relative"]))  # type: str  # line 690
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", "'.'"], out)  # line 691
        _.createFile(1, "aa")  # line 692
        sos.commit("First")  # add one file  # line 693
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 694
        _.createFile(2, "b")  # line 695
        try:  # add nothing, because picky  # line 696
            sos.commit("Second")  # add nothing, because picky  # line 696
        except:  # line 697
            pass  # line 697
        sos.add(".", "./file?")  # line 698
        sos.commit("Third")  # line 699
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 700
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 701
        _.assertIn("    r0", out)  # line 702
        sys.argv.extend(["-n", "2"])  # We cannot use the opions array for named argument options  # line 703
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 704
        sys.argv.pop()  # line 705
        sys.argv.pop()  # line 705
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 706
        _.assertIn("    r1", out)  # line 707
        _.assertIn("  * r2", out)  # line 708
        try:  # line 709
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 709
        except SystemExit as E:  # line 710
            _.assertEqual(0, E.code)  # line 710
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 711
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 712
        _.assertNotIn("    r1", out)  # line 713
        _.assertIn("  * r2", out)  # line 714
        _.createFile(3, prefix="sub")  # line 715
        sos.add("sub", "sub/file?")  # line 716
        changes = sos.changes()  # line 717
        _.assertEqual(1, len(changes.additions))  # line 718
        _.assertTrue("sub/file3" in changes.additions)  # line 719

    def testTrackedSubfolder(_):  # line 721
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 722
        os.mkdir("." + os.sep + "sub")  # line 723
        sos.offline("trunk", None, ["--track"])  # line 724
        _.createFile(1, "x")  # line 725
        _.createFile(1, "x", prefix="sub")  # line 726
        sos.add(".", "./file?")  # add glob pattern to track  # line 727
        sos.commit("First")  # line 728
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 729
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 730
        sos.commit("Second")  # one new file + meta  # line 731
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 732
        os.unlink("file1")  # remove from basefolder  # line 733
        _.createFile(2, "y")  # line 734
        sos.remove(".", "sub/file?")  # line 735
        try:  # TODO check more textual details here  # line 736
            sos.remove(".", "sub/bla")  # TODO check more textual details here  # line 736
            _.fail("Expected exit")  # TODO check more textual details here  # line 736
        except SystemExit as E:  # line 737
            _.assertEqual(1, E.code)  # line 737
        sos.commit("Third")  # line 738
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 739
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 742
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 747
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 748
        _.createFile(1)  # line 749
        _.createFile("a123a")  # untracked file "a123a"  # line 750
        sos.add(".", "./file?")  # add glob tracking pattern  # line 751
        sos.commit("second")  # versions "file1"  # line 752
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 753
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 754
        _.assertIn("  | ./file?", out)  # line 755

        _.createFile(2)  # untracked file "file2"  # line 757
        sos.commit("third")  # versions "file2"  # line 758
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 759

        os.mkdir("." + os.sep + "sub")  # line 761
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 762
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 763
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 764

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 766
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 767
        sos.add(".", "./a*a")  # add tracking pattern  # line 768
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 769
        _.assertEqual(0, len(changes.modifications))  # line 770
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 771
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 772

        sos.commit("Second_2")  # line 774
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 775
        _.existsFile(1, b"x" * 10)  # line 776
        _.existsFile(2, b"x" * 10)  # line 777

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 779
        _.existsFile(1, b"x" * 10)  # line 780
        _.existsFile("a123a", b"x" * 10)  # line 781

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 783
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 784
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 785

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 787
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 788
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 789
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 790
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 791
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 792
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 793
# TODO test switch --meta

    def testLsTracked(_):  # line 796
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 797
        _.createFile(1)  # line 798
        _.createFile("foo")  # line 799
        sos.add(".", "./file*")  # capture one file  # line 800
        sos.ls()  # line 801
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # type: str  # line 802
        _.assertInAny("TRK file1  (file*)", out)  # line 803
        _.assertNotInAny("... file1  (file*)", out)  # line 804
        _.assertInAny("    foo", out)  # line 805
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 806
        _.assertInAny("TRK file*", out)  # line 807
        _.createFile("a", prefix="sub")  # line 808
        sos.add("sub", "sub/a")  # line 809
        sos.ls("sub")  # line 810
        _.assertInAny("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 811

    def testLineMerge(_):  # line 813
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 814
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 815
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 816
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 817

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 819
        _.createFile(1)  # line 820
        sos.offline("master", options=["--force"])  # line 821
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # type: str  # line 822
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 823
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 824
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 825
        _.createFile(2)  # line 826
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 827
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 828
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 829
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 830

    def testLocalConfig(_):  # line 832
        sos.offline("bla", options=[])  # line 833
        try:  # line 834
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 834
        except SystemExit as E:  # line 835
            _.assertEqual(0, E.code)  # line 835
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 836

    def testConfigVariations(_):  # line 838
        def makeRepo():  # line 839
            try:  # line 840
                os.unlink("file1")  # line 840
            except:  # line 841
                pass  # line 841
            sos.offline("master", options=["--force"])  # line 842
            _.createFile(1)  # line 843
            sos.commit("Added file1")  # line 844
        try:  # line 845
            sos.config(["set", "strict", "on"])  # line 845
        except SystemExit as E:  # line 846
            _.assertEqual(0, E.code)  # line 846
        makeRepo()  # line 847
        _.assertTrue(checkRepoFlag("strict", True))  # line 848
        try:  # line 849
            sos.config(["set", "strict", "off"])  # line 849
        except SystemExit as E:  # line 850
            _.assertEqual(0, E.code)  # line 850
        makeRepo()  # line 851
        _.assertTrue(checkRepoFlag("strict", False))  # line 852
        try:  # line 853
            sos.config(["set", "strict", "yes"])  # line 853
        except SystemExit as E:  # line 854
            _.assertEqual(0, E.code)  # line 854
        makeRepo()  # line 855
        _.assertTrue(checkRepoFlag("strict", True))  # line 856
        try:  # line 857
            sos.config(["set", "strict", "no"])  # line 857
        except SystemExit as E:  # line 858
            _.assertEqual(0, E.code)  # line 858
        makeRepo()  # line 859
        _.assertTrue(checkRepoFlag("strict", False))  # line 860
        try:  # line 861
            sos.config(["set", "strict", "1"])  # line 861
        except SystemExit as E:  # line 862
            _.assertEqual(0, E.code)  # line 862
        makeRepo()  # line 863
        _.assertTrue(checkRepoFlag("strict", True))  # line 864
        try:  # line 865
            sos.config(["set", "strict", "0"])  # line 865
        except SystemExit as E:  # line 866
            _.assertEqual(0, E.code)  # line 866
        makeRepo()  # line 867
        _.assertTrue(checkRepoFlag("strict", False))  # line 868
        try:  # line 869
            sos.config(["set", "strict", "true"])  # line 869
        except SystemExit as E:  # line 870
            _.assertEqual(0, E.code)  # line 870
        makeRepo()  # line 871
        _.assertTrue(checkRepoFlag("strict", True))  # line 872
        try:  # line 873
            sos.config(["set", "strict", "false"])  # line 873
        except SystemExit as E:  # line 874
            _.assertEqual(0, E.code)  # line 874
        makeRepo()  # line 875
        _.assertTrue(checkRepoFlag("strict", False))  # line 876
        try:  # line 877
            sos.config(["set", "strict", "enable"])  # line 877
        except SystemExit as E:  # line 878
            _.assertEqual(0, E.code)  # line 878
        makeRepo()  # line 879
        _.assertTrue(checkRepoFlag("strict", True))  # line 880
        try:  # line 881
            sos.config(["set", "strict", "disable"])  # line 881
        except SystemExit as E:  # line 882
            _.assertEqual(0, E.code)  # line 882
        makeRepo()  # line 883
        _.assertTrue(checkRepoFlag("strict", False))  # line 884
        try:  # line 885
            sos.config(["set", "strict", "enabled"])  # line 885
        except SystemExit as E:  # line 886
            _.assertEqual(0, E.code)  # line 886
        makeRepo()  # line 887
        _.assertTrue(checkRepoFlag("strict", True))  # line 888
        try:  # line 889
            sos.config(["set", "strict", "disabled"])  # line 889
        except SystemExit as E:  # line 890
            _.assertEqual(0, E.code)  # line 890
        makeRepo()  # line 891
        _.assertTrue(checkRepoFlag("strict", False))  # line 892
        try:  # line 893
            sos.config(["set", "strict", "nope"])  # line 893
            _.fail()  # line 893
        except SystemExit as E:  # line 894
            _.assertEqual(1, E.code)  # line 894

    def testLsSimple(_):  # line 896
        _.createFile(1)  # line 897
        _.createFile("foo")  # line 898
        _.createFile("ign1")  # line 899
        _.createFile("ign2")  # line 900
        _.createFile("bar", prefix="sub")  # line 901
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 902
        try:  # define an ignore pattern  # line 903
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern  # line 903
        except SystemExit as E:  # line 904
            _.assertEqual(0, E.code)  # line 904
        try:  # additional ignore pattern  # line 905
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 905
        except SystemExit as E:  # line 906
            _.assertEqual(0, E.code)  # line 906
        try:  # define a list of ignore patterns  # line 907
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 907
        except SystemExit as E:  # line 908
            _.assertEqual(0, E.code)  # line 908
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # type: str  # line 909
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 910
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 911
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 912
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 913
        _.assertInAny('    file1', out)  # line 914
        _.assertInAny('    ign1', out)  # line 915
        _.assertInAny('    ign2', out)  # line 916
        _.assertNotIn('DIR sub', out)  # line 917
        _.assertNotIn('    bar', out)  # line 918
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 919
        _.assertIn('DIR sub', out)  # line 920
        _.assertIn('    bar', out)  # line 921
        try:  # line 922
            sos.config(["rm", "foo", "bar"])  # line 922
            _.fail()  # line 922
        except SystemExit as E:  # line 923
            _.assertEqual(1, E.code)  # line 923
        try:  # line 924
            sos.config(["rm", "ignores", "foo"])  # line 924
            _.fail()  # line 924
        except SystemExit as E:  # line 925
            _.assertEqual(1, E.code)  # line 925
        try:  # line 926
            sos.config(["rm", "ignores", "ign1"])  # line 926
        except SystemExit as E:  # line 927
            _.assertEqual(0, E.code)  # line 927
        try:  # remove ignore pattern  # line 928
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 928
        except SystemExit as E:  # line 929
            _.assertEqual(0, E.code)  # line 929
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 930
        _.assertInAny('    ign1', out)  # line 931
        _.assertInAny('IGN ign2', out)  # line 932
        _.assertNotInAny('    ign2', out)  # line 933

    def testWhitelist(_):  # line 935
# TODO test same for simple mode
        _.createFile(1)  # line 937
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 938
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 939
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 940
        sos.commit(options=["--force"])  # attempt to commit the file  # line 941
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 942
        try:  # Exit because dirty  # line 943
            sos.online()  # Exit because dirty  # line 943
            _.fail()  # Exit because dirty  # line 943
        except:  # exception expected  # line 944
            pass  # exception expected  # line 944
        _.createFile("x2")  # add another change  # line 945
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 946
        try:  # force beyond dirty flag check  # line 947
            sos.online(["--force"])  # force beyond dirty flag check  # line 947
            _.fail()  # force beyond dirty flag check  # line 947
        except:  # line 948
            pass  # line 948
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 949
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 950

        _.createFile(1)  # line 952
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 953
        sos.offline("xx", None, ["--track"])  # line 954
        sos.add(".", "./file*")  # line 955
        sos.commit()  # should NOT ask for force here  # line 956
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 957

    def testRemove(_):  # line 959
        _.createFile(1, "x" * 100)  # line 960
        sos.offline("trunk")  # line 961
        try:  # line 962
            sos.destroy("trunk")  # line 962
            _fail()  # line 962
        except:  # line 963
            pass  # line 963
        _.createFile(2, "y" * 10)  # line 964
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 965
        sos.destroy("trunk")  # line 966
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 967
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 968
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 969
        sos.branch("next")  # line 970
        _.createFile(3, "y" * 10)  # make a change  # line 971
        sos.destroy("added", "--force")  # should succeed  # line 972

    def testFastBranchingOnEmptyHistory(_):  # line 974
        ''' Test fast branching without revisions and with them. '''  # line 975
        sos.offline(options=["--strict", "--compress"])  # b0  # line 976
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 977
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 978
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 979
        sos.destroy("2")  # line 980
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 981
        _.assertIn("b0 'trunk' @", out)  # line 982
        _.assertIn("b1         @", out)  # line 983
        _.assertIn("b3         @", out)  # line 984
        _.assertNotIn("b2         @", out)  # line 985
        sos.branch("", "")  # non-fast branching of b4  # line 986
        _.createFile(1)  # line 987
        _.createFile(2)  # line 988
        sos.commit("")  # line 989
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 990
        sos.destroy("4")  # line 991
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 992
        _.assertIn("b0 'trunk' @", out)  # line 993
        _.assertIn("b1         @", out)  # line 994
        _.assertIn("b3         @", out)  # line 995
        _.assertIn("b5         @", out)  # line 996
        _.assertNotIn("b2         @", out)  # line 997
        _.assertNotIn("b4         @", out)  # line 998
# TODO add more files and branch again

    def testUsage(_):  # line 1001
        try:  # TODO expect sys.exit(0)  # line 1002
            sos.usage()  # TODO expect sys.exit(0)  # line 1002
            _.fail()  # TODO expect sys.exit(0)  # line 1002
        except:  # line 1003
            pass  # line 1003
        try:  # TODO expect sys.exit(0)  # line 1004
            sos.usage("help")  # TODO expect sys.exit(0)  # line 1004
            _.fail()  # TODO expect sys.exit(0)  # line 1004
        except:  # line 1005
            pass  # line 1005
        try:  # TODO expect sys.exit(0)  # line 1006
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 1006
            _.fail()  # TODO expect sys.exit(0)  # line 1006
        except:  # line 1007
            pass  # line 1007
        try:  # line 1008
            sos.usage(version=True)  # line 1008
            _.fail()  # line 1008
        except:  # line 1009
            pass  # line 1009
        try:  # line 1010
            sos.usage(version=True)  # line 1010
            _.fail()  # line 1010
        except:  # line 1011
            pass  # line 1011

    def testOnlyExcept(_):  # line 1013
        ''' Test blacklist glob rules. '''  # line 1014
        sos.offline(options=["--track"])  # line 1015
        _.createFile("a.1")  # line 1016
        _.createFile("a.2")  # line 1017
        _.createFile("b.1")  # line 1018
        _.createFile("b.2")  # line 1019
        sos.add(".", "./a.?")  # line 1020
        sos.add(".", "./?.1", negative=True)  # line 1021
        out = wrapChannels(lambda _=None: sos.commit())  # type: str  # line 1022
        _.assertIn("ADD ./a.2", out)  # line 1023
        _.assertNotIn("ADD ./a.1", out)  # line 1024
        _.assertNotIn("ADD ./b.1", out)  # line 1025
        _.assertNotIn("ADD ./b.2", out)  # line 1026

    def testOnly(_):  # line 1028
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",)), ["bla"]), sos.parseArgumentOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--remote", "bla", "--only"]))  # line 1029
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1030
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1031
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1032
        sos.offline(options=["--track", "--strict"])  # line 1033
        _.createFile(1)  # line 1034
        _.createFile(2)  # line 1035
        sos.add(".", "./file1")  # line 1036
        sos.add(".", "./file2")  # line 1037
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1038
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1039
        sos.commit()  # adds also file2  # line 1040
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1041
        _.createFile(1, "cc")  # modify both files  # line 1042
        _.createFile(2, "dd")  # line 1043
        try:  # line 1044
            sos.config(["set", "texttype", "file2"])  # line 1044
        except SystemExit as E:  # line 1045
            _.assertEqual(0, E.code)  # line 1045
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1046
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1047
        _.assertTrue("./file2" in changes.modifications)  # line 1048
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 1049
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1050
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1051
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # line 1052

    def testDiff(_):  # line 1054
        try:  # manually mark this file as "textual"  # line 1055
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1055
        except SystemExit as E:  # line 1056
            _.assertEqual(0, E.code)  # line 1056
        sos.offline(options=["--strict"])  # line 1057
        _.createFile(1)  # line 1058
        _.createFile(2)  # line 1059
        sos.commit()  # line 1060
        _.createFile(1, "sdfsdgfsdf")  # line 1061
        _.createFile(2, "12343")  # line 1062
        sos.commit()  # line 1063
        _.createFile(1, "foobar")  # line 1064
        _.createFile(3)  # line 1065
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # type: str  # compare with r1 (second counting from last which is r2)  # line 1066
        _.assertIn("ADD ./file3", out)  # line 1067
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "-~- 0 |xxxxxxxxxx|", "+~+ 0 |foobar|"], out)  # line 1068
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1069

    def testReorderRenameActions(_):  # line 1071
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1072
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1073
        try:  # line 1074
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1074
            _.fail()  # line 1074
        except:  # line 1075
            pass  # line 1075

    def testPublish(_):  # line 1077
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1078

    def testMove(_):  # line 1080
        ''' Move primarily modifies tracking patterns and moves files around accordingly. '''  # line 1081
        sos.offline(options=["--strict", "--track"])  # line 1082
        _.createFile(1)  # line 1083
        sos.add(".", "./file?")  # line 1084
# assert error when source folder is missing
        out = wrapChannels(lambda _=None: sos.move("sub", "sub/file?", ".", "./?file"))  # type: str  # line 1086
        _.assertIn("Source folder doesn't exist", out)  # line 1087
        _.assertIn("EXIT CODE 1", out)  # line 1088
# if target folder missing: create it and move matching files into it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1090
        _.assertTrue(os.path.exists("sub"))  # line 1091
        _.assertTrue(os.path.exists("sub/file1"))  # line 1092
        _.assertFalse(os.path.exists("file1"))  # line 1093
# test move back to previous location, plus rename the file
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1095
        _.assertTrue(os.path.exists("1file"))  # line 1096
        _.assertFalse(os.path.exists("sub/file1"))  # line 1097
# assert error when nothing matches source pattern
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*"))  # line 1099
        _.assertIn("No files match the specified file pattern", out)  # line 1100
        _.assertIn("EXIT CODE", out)  # line 1101
        sos.add(".", "./*")  # add catch-all tracking pattern to root folder  # line 1102
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*", options=["--force"]))  # line 1103
        _.assertIn("  './*' matches 3 files", out)  # line 1104
        _.assertIn("EXIT CODE", out)  # line 1105
# test rename no conflict
        _.createFile(1)  # line 1107
        _.createFile(2)  # line 1108
        _.createFile(3)  # line 1109
        sos.add(".", "./file*")  # line 1110
        sos.remove(".", "./*")  # line 1111
        try:  # define an ignore pattern  # line 1112
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1112
        except SystemExit as E:  # line 1113
            _.assertEqual(0, E.code)  # line 1113
        try:  # line 1114
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1114
        except SystemExit as E:  # line 1115
            _.assertEqual(0, E.code)  # line 1115
        sos.move(".", "./file*", ".", "./fi*le")  # should only move not ignored files files  # line 1116
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1117
        _.assertTrue(all((not os.path.exists("file%d" % i) for i in range(1, 4))))  # line 1118
        _.assertFalse(os.path.exists("fi4le"))  # line 1119
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1121
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # untrack pattern, which was renamed before  # line 1125
        sos.add(".", "./?a?b", ["--force"])  # line 1126
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1127
        _.createFile("1a2b")  # should not be tracked  # line 1128
        _.createFile("a1b2")  # should be tracked  # line 1129
        sos.commit()  # line 1130
        _.assertEqual(5, len(os.listdir(sos.revisionFolder(0, 1))))  # meta, a1b2, fi[1-3]le  # line 1131
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1132
        _.createFile("1a1b1")  # line 1133
        _.createFile("1a1b2")  # line 1134
        sos.add(".", "./?a?b*")  # line 1135
# test target pattern exists
        out = wrapChannels(lambda _=None: sos.move(".", "./?a?b*", ".", "./z?z?"))  # line 1137
        _.assertIn("not unique", out)  # line 1138
# TODO only rename if actually any files are versioned? or simply what is currently alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1142
        _.createFile(1)  # line 1143
        _.createFile(3)  # line 1144
        _.createFile(5)  # line 1145
        sos.offline()  # branch 0: only file1  # line 1146
        sos.branch()  # line 1147
        os.unlink("file1")  # line 1148
        os.unlink("file3")  # line 1149
        os.unlink("file5")  # line 1150
        _.createFile(2)  # line 1151
        _.createFile(4)  # line 1152
        _.createFile(6)  # line 1153
        sos.commit()  # branch 1: only file2  # line 1154
        sos.switch("0/")  # line 1155
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1156
        _.assertFalse(_.existsFile(1))  # line 1157
        _.assertFalse(_.existsFile(3))  # line 1158
        _.assertFalse(_.existsFile(5))  # line 1159
        _.assertTrue(_.existsFile(2))  # line 1160
        _.assertTrue(_.existsFile(4))  # line 1161
        _.assertTrue(_.existsFile(6))  # line 1162

    def testMoveDetection(_):  # line 1164
        _.createFile(1, "bla")  # line 1165
        sos.offline()  # line 1166
        os.mkdir("sub1")  # line 1167
        os.mkdir("sub2")  # line 1168
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1169
        shutil.move("file1", "sub2")  # line 1170
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 1171
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1172
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1173
        sos.commit("Moved the file")  # line 1174
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1178

    def testHashCollision(_):  # line 1180
        old = sos.Metadata.findChanges  # line 1181
        @_coconut_tco  # line 1182
        def patched(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 1182
            import collections  # used only in this method  # line 1183
            write = branch is not None and revision is not None  # line 1184
            if write:  # line 1185
                try:  # line 1186
                    os.makedirs(sos.encode(sos.revisionFolder(branch, revision, base=_.root)))  # line 1186
                except FileExistsError:  # HINT "try" only necessary for hash collision *test code* (!)  # line 1187
                    pass  # HINT "try" only necessary for hash collision *test code* (!)  # line 1187
            return _coconut_tail_call(old, _, branch, revision, checkContent, inverse, considerOnly, dontConsider, progress)  # line 1188
        sos.Metadata.findChanges = patched  # monkey-patch  # line 1189
        sos.offline()  # line 1190
        _.createFile(1)  # line 1191
        os.mkdir(sos.revisionFolder(0, 1))  # line 1192
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # hashed file name for not-yet-committed file1  # line 1193
        _.createFile(1)  # line 1194
        try:  # line 1195
            sos.commit()  # line 1195
            _.fail("Expected system exit due to hash collision detection")  # line 1195
        except SystemExit as E:  # HINT exit is implemented in utility.hashFile  # line 1196
            _.assertEqual(1, E.code)  # HINT exit is implemented in utility.hashFile  # line 1196
        sos.Metadata.findChanges = old  # revert monkey patch  # line 1197

    def testFindBase(_):  # line 1199
        old = os.getcwd()  # line 1200
        try:  # line 1201
            os.mkdir("." + os.sep + ".git")  # line 1202
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1203
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1204
            os.chdir("a" + os.sep + "b")  # line 1205
            s, vcs, cmd = sos.findSosVcsBase()  # line 1206
            _.assertIsNotNone(s)  # line 1207
            _.assertIsNotNone(vcs)  # line 1208
            _.assertEqual("git", cmd)  # line 1209
        finally:  # line 1210
            os.chdir(old)  # line 1210

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1221
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1222
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1223
