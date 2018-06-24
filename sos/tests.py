#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x28de1fb3

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

testFolder = os.path.abspath(os.path.join(os.getcwd(), "test"))  # this needs to be set before the configr and sos imports  # line 16
os.environ["TEST"] = testFolder  # needed to mock configr library calls in sos  # line 17

import configr  # line 19
import sos  # import of package, not file  # line 20

sos.defaults["defaultbranch"] = "trunk"  # because sos.main() is never called  # line 22
sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 23
sos.defaults["useUnicodeFont"] = False  # because sos.main() is never called  # line 24


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
    oldv = sys.argv  # line 69
    buf = TextIOWrapper(BufferedRandom(BytesIO(b"")), encoding=sos.UTF8)  # line 70
    handler = logging.StreamHandler(buf)  # TODO doesn't seem to be captured  # line 71
    sys.stdout = sys.stderr = buf  # line 72
    logging.getLogger().addHandler(handler)  # line 73
    try:  # capture output into buf  # line 74
        func()  # capture output into buf  # line 74
    except Exception as E:  # line 75
        buf.write(str(E) + "\n")  # line 75
        traceback.print_exc(file=buf)  # line 75
    except SystemExit as F:  # line 76
        buf.write("EXIT CODE %s" % F.code + "\n")  # line 76
        traceback.print_exc(file=buf)  # line 76
    logging.getLogger().removeHandler(handler)  # line 77
    sys.argv, sys.stdout, sys.stderr = oldv, sys.__stdout__, sys.__stderr__  # TODO when run using pythonw.exe and/or no console, these could be None  # line 78
    buf.seek(0)  # line 79
    return _coconut_tail_call(buf.read)  # line 80

def mockInput(datas: '_coconut.typing.Sequence[str]', func: '_coconut.typing.Callable[..., Any]') -> 'Any':  # line 82
    try:  # via python sos/tests.py  # line 83
        with mock.patch("sos._utility.input", side_effect=datas):  # line 84
            return func()  # line 84
    except:  # via setup.py  # line 85
        with mock.patch("sos.utility.input", side_effect=datas):  # line 86
            return func()  # line 86

def setRepoFlag(name: 'str', value: 'bool'):  # line 88
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 89
        flags, branches, config = json.loads(fd.read())  # line 89
    flags[name] = value  # line 90
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 91
        fd.write(json.dumps((flags, branches, config)))  # line 91

def checkRepoFlag(name: 'str', flag: '_coconut.typing.Optional[bool]'=None, value: '_coconut.typing.Optional[Any]'=None) -> 'bool':  # line 93
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 94
        flags, branches, config = json.loads(fd.read())  # line 94
    return (name in flags and flags[name] == flag) if flag is not None else (name in config and config[name] == value)  # line 95


class Tests(unittest.TestCase):  # line 98
    ''' Entire test suite. '''  # line 99

    def setUp(_):  # line 101
        sos.Metadata.singleton = None  # line 102
        for entry in os.listdir(testFolder):  # cannot remove testFolder on Windows when using TortoiseSVN as VCS  # line 103
            resource = os.path.join(testFolder, entry)  # line 104
            shutil.rmtree(sos.encode(resource)) if os.path.isdir(sos.encode(resource)) else os.unlink(sos.encode(resource))  # line 105
        os.chdir(testFolder)  # line 106


    def assertAllIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]', only: 'bool'=False):  # line 109
        for w in what:  # line 110
            _.assertIn(w, where)  # line 110
        if only:  # line 111
            _.assertEqual(len(what), len(where))  # line 111

    def assertAllNotIn(_, what: '_coconut.typing.Sequence[str]', where: 'Union[str, List[str]]'):  # line 113
        for w in what:  # line 114
            _.assertNotIn(w, where)  # line 114

    def assertInAll(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 116
        for w in where:  # line 117
            _.assertIn(what, w)  # line 117

    def assertInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 119
        _.assertTrue(any((what in w for w in where)))  # line 119

    def assertNotInAny(_, what: 'str', where: '_coconut.typing.Sequence[str]'):  # line 121
        _.assertFalse(any((what in w for w in where)))  # line 121


    def createFile(_, number: 'Union[int, str]', contents: 'str'="x" * 10, prefix: '_coconut.typing.Optional[str]'=None):  # line 124
        if prefix and not os.path.exists(prefix):  # line 125
            os.makedirs(prefix)  # line 125
        with open(("." if prefix is None else prefix) + os.sep + (("file%d" % number) if isinstance(number, int) else number), "wb") as fd:  # line 126
            fd.write(contents if isinstance(contents, bytes) else contents.encode("cp1252"))  # line 126
        sync()  # line 127

    def existsFile(_, number: 'Union[int, str]', expectedContents: 'bytes'=None) -> 'bool':  # line 129
        sync()  # line 130
        if not os.path.exists(("." + os.sep + "file%d" % number) if isinstance(number, int) else number):  # line 131
            return False  # line 131
        if expectedContents is None:  # line 132
            return True  # line 132
        with open(("." + os.sep + "file%d" % number) if isinstance(number, int) else number, "rb") as fd:  # line 133
            return fd.read() == expectedContents  # line 133

    def testAccessor(_):  # line 135
        a = sos.Accessor({"a": 1})  # line 136
        _.assertEqual((1, 1), (a["a"], a.a))  # line 137

    def testIndexing(_):  # line 139
        m = sos.Metadata()  # line 140
        m.commits = {}  # line 141
        _.assertEqual(1, m.correctNegativeIndexing(1))  # line 142
        _.assertEqual(9999999999999999, m.correctNegativeIndexing(9999999999999999))  # line 143
        _.assertEqual(0, m.correctNegativeIndexing(0))  # zero always returns zero, even no commits present  # line 144
        try:  # line 145
            m.correctNegativeIndexing(-1)  # line 145
            _.fail()  # line 145
        except SystemExit as E:  # line 146
            _.assertEqual(1, E.code)  # line 146
        m.commits = {0: sos.CommitInfo(0, 0), 1: sos.CommitInfo(1, 0)}  # line 147
        _.assertEqual(1, m.correctNegativeIndexing(-1))  # zero always returns zero, even no commits present  # line 148
        _.assertEqual(0, m.correctNegativeIndexing(-2))  # zero always returns zero, even no commits present  # line 149
        try:  # line 150
            m.correctNegativeIndexing(-3)  # line 150
            _.fail()  # line 150
        except SystemExit as E:  # line 151
            _.assertEqual(1, E.code)  # line 151

    def testRestoreFile(_):  # line 153
        m = sos.Metadata()  # line 154
        os.makedirs(sos.revisionFolder(0, 0))  # line 155
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 156
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 157
        _.assertTrue(_.existsFile("restored", b""))  # line 158

    def testGetAnyOfmap(_):  # line 160
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 161
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 162

    def testAjoin(_):  # line 164
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 165
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 166

    def testFindChanges(_):  # line 168
        m = sos.Metadata(os.getcwd())  # line 169
        try:  # line 170
            sos.config(["set", "texttype", "*"])  # line 170
        except SystemExit as E:  # line 171
            _.assertEqual(0, E.code)  # line 171
        try:  # will be stripped from leading paths anyway  # line 172
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 172
        except SystemExit as E:  # line 173
            _.assertEqual(0, E.code)  # line 173
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 174
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 175
            os.unlink(file)  # remove configuration file  # line 175
        _.createFile(1, "1")  # line 176
        m.createBranch(0)  # line 177
        _.assertEqual(1, len(m.paths))  # line 178
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 179
        _.createFile(1, "2")  # modify existing file  # line 180
        _.createFile(2, "2")  # add another file  # line 181
        m.loadCommit(0, 0)  # line 182
        changes, msg = m.findChanges()  # detect time skew  # line 183
        _.assertEqual(1, len(changes.additions))  # line 184
        _.assertEqual(0, len(changes.deletions))  # line 185
        _.assertEqual(1, len(changes.modifications))  # line 186
        _.assertEqual(0, len(changes.moves))  # line 187
        m.paths.update(changes.additions)  # line 188
        m.paths.update(changes.modifications)  # line 189
        _.createFile(2, "12")  # modify file again  # line 190
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 191
        _.assertEqual(0, len(changes.additions))  # line 192
        _.assertEqual(0, len(changes.deletions))  # line 193
        _.assertEqual(1, len(changes.modifications))  # line 194
        _.assertEqual(0, len(changes.moves))  # line 195
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 196
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 197
# TODO test moves

    def testDumpSorting(_):  # line 200
        m = sos.Metadata()  # type: Metadata  # line 201
        _.createFile(1)  # line 202
        sos.offline()  # line 203
        _.createFile(2)  # line 204
        _.createFile(3)  # line 205
        sos.commit()  # line 206
        _.createFile(4)  # line 207
        _.createFile(5)  # line 208
        sos.commit()  # line 209
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # type: List[str]  # line 210
        _.assertTrue(out.index("b0%sr2" % os.sep) > out.index("b0%sr1" % os.sep))  # line 211
        _.assertTrue(out.index("b0%sr1" % os.sep) > out.index("b0%sr0" % os.sep))  # line 212

    def testFitStrings(_):  # line 214
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 215
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 216
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 217
    def testMoves(_):  # line 218
        _.createFile(1, "1")  # line 219
        _.createFile(2, "2", "sub")  # line 220
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 221
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 222
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 223
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 224
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 225
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 226
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # line 227
        _.assertIn("MOV ../file2  <-  ./file2", out)  # line 228
        _.assertIn("MOV ./file1  <-  ../file1", out)  # line 229
        out = wrapChannels(lambda _=None: sos.commit())  # line 230
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 231
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 232
        _.assertIn("Created new revision r01 (+00/-00/~00/#02) summing 628 bytes in 2 files (88.22% SOS overhead)", out)  # TODO why is this not captured?  # line 233

    def testPatternPaths(_):  # line 235
        sos.offline(options=["--track"])  # line 236
        os.mkdir("sub")  # line 237
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 238
        out = wrapChannels(lambda _=None: sos.add("sub", "sub/file?"))  # type: str  # line 239
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", os.path.abspath("sub")], out)  # line 240
        sos.commit("test")  # should pick up sub/file1 pattern  # line 241
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 242
        _.createFile(1)  # line 243
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 244
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 244
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 244
        except:  # line 245
            pass  # line 245

    def testNoArgs(_):  # line 247
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 248

    def testAutoMetadataUpgrade(_):  # line 250
        sos.offline()  # line 251
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 252
            repo, branches, config = json.load(fd)  # line 252
        repo["version"] = None  # lower than any pip version  # line 253
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 254
        del repo["format"]  # simulate pre-1.3.5  # line 255
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 256
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 256
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # type: str  # line 257
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 258

    def testFastBranching(_):  # line 260
        _.createFile(1)  # line 261
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict", "--verbose"]))  # type: str  # b0/r0 = ./file1  # line 262
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 263
        _.createFile(2)  # line 264
        os.unlink("file1")  # line 265
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 266
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 267
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 268
        _.createFile(3)  # line 269
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 270
        _.assertAllIn([sos.metaFile, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 271
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 272
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 273
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 274
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 275
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 276
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 279
        now = time.time()  # type: float  # line 280
        _.createFile(1)  # line 281
        sync()  # line 282
        sos.offline(options=["--strict"])  # line 283
        _.createFile(1, "abc")  # modify contents  # line 284
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 285
        sync()  # line 286
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 287
        _.assertIn("<older than previously committed>", out)  # line 288
        out = wrapChannels(lambda _=None: sos.commit())  # line 289
        _.assertIn("<older than previously committed>", out)  # line 290

    def testGetParentBranch(_):  # line 292
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 293
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 294
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 295
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 296
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 297

    def testTokenizeGlobPattern(_):  # line 299
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 300
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 301
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 302
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 303
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 304
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 305

    def testTokenizeGlobPatterns(_):  # line 307
        try:  # because number of literal strings differs  # line 308
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 308
            _.fail()  # because number of literal strings differs  # line 308
        except:  # line 309
            pass  # line 309
        try:  # because glob patterns differ  # line 310
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 310
            _.fail()  # because glob patterns differ  # line 310
        except:  # line 311
            pass  # line 311
        try:  # glob patterns differ, regardless of position  # line 312
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 312
            _.fail()  # glob patterns differ, regardless of position  # line 312
        except:  # line 313
            pass  # line 313
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 314
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 315
        try:  # succeeds, because glob patterns match (differ only in position)  # line 316
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 316
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 316
        except:  # line 317
            pass  # line 317

    def testConvertGlobFiles(_):  # line 319
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 320
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 321

    def testFolderRemove(_):  # line 323
        m = sos.Metadata(os.getcwd())  # line 324
        _.createFile(1)  # line 325
        _.createFile("a", prefix="sub")  # line 326
        sos.offline()  # line 327
        _.createFile(2)  # line 328
        os.unlink("sub" + os.sep + "a")  # line 329
        os.rmdir("sub")  # line 330
        changes = sos.changes()  # TODO replace by output check  # line 331
        _.assertEqual(1, len(changes.additions))  # line 332
        _.assertEqual(0, len(changes.modifications))  # line 333
        _.assertEqual(1, len(changes.deletions))  # line 334
        _.createFile("a", prefix="sub")  # line 335
        changes = sos.changes()  # line 336
        _.assertEqual(0, len(changes.deletions))  # line 337

    def testSwitchConflict(_):  # line 339
        sos.offline(options=["--strict"])  # (r0)  # line 340
        _.createFile(1)  # line 341
        sos.commit()  # add file (r1)  # line 342
        os.unlink("file1")  # line 343
        sos.commit()  # remove (r2)  # line 344
        _.createFile(1, "something else")  # line 345
        sos.commit()  # (r3)  # line 346
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 347
        _.existsFile(1, "x" * 10)  # line 348
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 349
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 350
        sos.switch("/1")  # add file1 back  # line 351
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 352
        _.existsFile(1, "something else")  # line 353

    def testComputeSequentialPathSet(_):  # line 355
        os.makedirs(sos.revisionFolder(0, 0))  # line 356
        os.makedirs(sos.revisionFolder(0, 1))  # line 357
        os.makedirs(sos.revisionFolder(0, 2))  # line 358
        os.makedirs(sos.revisionFolder(0, 3))  # line 359
        os.makedirs(sos.revisionFolder(0, 4))  # line 360
        m = sos.Metadata(os.getcwd())  # line 361
        m.branch = 0  # line 362
        m.commit = 2  # line 363
        m.saveBranches()  # line 364
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 365
        m.saveCommit(0, 0)  # initial  # line 366
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 367
        m.saveCommit(0, 1)  # mod  # line 368
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 369
        m.saveCommit(0, 2)  # add  # line 370
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 371
        m.saveCommit(0, 3)  # del  # line 372
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 373
        m.saveCommit(0, 4)  # readd  # line 374
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 375
        m.saveBranch(0)  # line 376
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 377
        m.saveBranches()  # line 378
        m.computeSequentialPathSet(0, 4)  # line 379
        _.assertEqual(2, len(m.paths))  # line 380

    def testParseRevisionString(_):  # line 382
        m = sos.Metadata(os.getcwd())  # line 383
        m.branch = 1  # line 384
        m.commits = {0: 0, 1: 1, 2: 2}  # line 385
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 386
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 387
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 388
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 389
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 390
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 391
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 392

    def testOfflineEmpty(_):  # line 394
        os.mkdir("." + os.sep + sos.metaFolder)  # line 395
        try:  # line 396
            sos.offline("trunk")  # line 396
            _.fail()  # line 396
        except SystemExit as E:  # line 397
            _.assertEqual(1, E.code)  # line 397
        os.rmdir("." + os.sep + sos.metaFolder)  # line 398
        sos.offline("test")  # line 399
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 400
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 401
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 402
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 403
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 404
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 405

    def testOfflineWithFiles(_):  # line 407
        _.createFile(1, "x" * 100)  # line 408
        _.createFile(2)  # line 409
        sos.offline("test")  # line 410
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 411
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 412
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 413
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 414
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 415
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 416
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 417

    def testBranch(_):  # line 419
        _.createFile(1, "x" * 100)  # line 420
        _.createFile(2)  # line 421
        sos.offline("test")  # b0/r0  # line 422
        sos.branch("other")  # b1/r0  # line 423
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 424
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 425
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 427
        _.createFile(1, "z")  # modify file  # line 429
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 430
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 431
        _.createFile(3, "z")  # line 433
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 434
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 435
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 440
        _.createFile(1, "x" * 100)  # line 441
        _.createFile(2)  # line 442
        sos.offline("test")  # line 443
        changes = sos.changes()  # line 444
        _.assertEqual(0, len(changes.additions))  # line 445
        _.assertEqual(0, len(changes.deletions))  # line 446
        _.assertEqual(0, len(changes.modifications))  # line 447
        _.createFile(1, "z")  # size change  # line 448
        changes = sos.changes()  # line 449
        _.assertEqual(0, len(changes.additions))  # line 450
        _.assertEqual(0, len(changes.deletions))  # line 451
        _.assertEqual(1, len(changes.modifications))  # line 452
        sos.commit("message")  # line 453
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 454
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 455
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 456
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 457
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 458
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 459
        os.unlink("file2")  # line 460
        changes = sos.changes()  # line 461
        _.assertEqual(0, len(changes.additions))  # line 462
        _.assertEqual(1, len(changes.deletions))  # line 463
        _.assertEqual(1, len(changes.modifications))  # line 464
        sos.commit("modified")  # line 465
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 466
        try:  # expecting Exit due to no changes  # line 467
            sos.commit("nothing")  # expecting Exit due to no changes  # line 467
            _.fail()  # expecting Exit due to no changes  # line 467
        except:  # line 468
            pass  # line 468

    def testGetBranch(_):  # line 470
        m = sos.Metadata(os.getcwd())  # line 471
        m.branch = 1  # current branch  # line 472
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 473
        _.assertEqual(27, m.getBranchByName(27))  # line 474
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 475
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 476
        _.assertIsNone(m.getBranchByName("unknown"))  # line 477
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 478
        _.assertEqual(13, m.getRevisionByName("13"))  # line 479
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 480
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 481

    def testTagging(_):  # line 483
        m = sos.Metadata(os.getcwd())  # line 484
        sos.offline()  # line 485
        _.createFile(111)  # line 486
        sos.commit("tag", ["--tag"])  # line 487
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # type: str  # line 488
        _.assertTrue(any(("|tag" in line and line.endswith("|TAG") for line in out)))  # line 489
        _.createFile(2)  # line 490
        try:  # line 491
            sos.commit("tag")  # line 491
            _.fail()  # line 491
        except:  # line 492
            pass  # line 492
        sos.commit("tag-2", ["--tag"])  # line 493
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 494
        _.assertIn("TAG tag", out)  # line 495

    def testSwitch(_):  # line 497
        _.createFile(1, "x" * 100)  # line 498
        _.createFile(2, "y")  # line 499
        sos.offline("test")  # file1-2  in initial branch commit  # line 500
        sos.branch("second")  # file1-2  switch, having same files  # line 501
        sos.switch("0")  # no change  switch back, no problem  # line 502
        sos.switch("second")  # no change  # switch back, no problem  # line 503
        _.createFile(3, "y")  # generate a file  # line 504
        try:  # uncommited changes detected  # line 505
            sos.switch("test")  # uncommited changes detected  # line 505
            _.fail()  # uncommited changes detected  # line 505
        except SystemExit as E:  # line 506
            _.assertEqual(1, E.code)  # line 506
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 507
        sos.changes()  # line 508
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 509
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 510
        _.createFile("XXX")  # line 511
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 512
        _.assertIn("File tree has changes", out)  # line 513
        _.assertNotIn("File tree is unchanged", out)  # line 514
        _.assertIn("  * b0   'test'", out)  # line 515
        _.assertIn("    b1 'second'", out)  # line 516
        _.assertIn("(modified)", out)  # one branch has commits  # line 517
        _.assertIn("(in sync)", out)  # the other doesn't  # line 518
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 519
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 520
        _.assertAllIn(["Metadata format", "Content checking:    deactivated", "Data compression:    deactivated", "Repository mode:     simple", "Number of branches:  2"], out)  # line 521
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 522
        _.createFile(4, "xy")  # generate a file  # line 523
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 524
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 525
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 526
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 527
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 528
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 529
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 530
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 531
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 532
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 533
        _.assertNotIn("Creating backup", out)  # line 534
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 535
        _.assertIn("Dumping revisions", out)  # line 536
        _.assertNotIn("Creating backup", out)  # line 537
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 538
        _.assertAllIn(["Creating backup"], out)  # line 539
        _.assertIn("Dumping revisions", out)  # line 540
        sos.verbose.pop()  # line 541

    def testAutoDetectVCS(_):  # line 543
        os.mkdir(".git")  # line 544
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 545
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 546
            meta = fd.read()  # line 546
        _.assertTrue("\"master\"" in meta)  # line 547
        os.rmdir(".git")  # line 548

    def testUpdate(_):  # line 550
        sos.offline("trunk")  # create initial branch b0/r0  # line 551
        _.createFile(1, "x" * 100)  # line 552
        sos.commit("second")  # create b0/r1  # line 553

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 555
        _.assertFalse(_.existsFile(1))  # line 556

        sos.update("/1")  # recreate file1  # line 558
        _.assertTrue(_.existsFile(1))  # line 559

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 561
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 562
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 563
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 564

        sos.update("/1")  # do nothing, as nothing has changed  # line 566
        _.assertTrue(_.existsFile(1))  # line 567

        _.createFile(2, "y" * 100)  # line 569
#    out:str = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 572
        _.assertTrue(_.existsFile(2))  # line 573
        sos.update("trunk", ["--add"])  # only add stuff  # line 574
        _.assertTrue(_.existsFile(2))  # line 575
        sos.update("trunk")  # nothing to do  # line 576
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 577

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 579
        _.createFile(10, theirs)  # line 580
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 581
        _.createFile(11, mine)  # line 582
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 583
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 584

    def testUpdate2(_):  # line 586
        _.createFile("test.txt", "x" * 10)  # line 587
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 588
        sync()  # line 589
        sos.branch("mod")  # line 590
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 591
        sos.commit("mod")  # create b0/r1  # line 592
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 593
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 594
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 595
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 596
        _.createFile("test.txt", "x" * 10)  # line 597
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 598
        sync()  # line 599
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 600
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 601
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 602
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 603
        sync()  # line 604
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 605
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 606

    def testIsTextType(_):  # line 608
        m = sos.Metadata(".")  # line 609
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 610
        m.c.bintype = ["*.md.confluence"]  # line 611
        _.assertTrue(m.isTextType("ab.txt"))  # line 612
        _.assertTrue(m.isTextType("./ab.txt"))  # line 613
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 614
        _.assertFalse(m.isTextType("bc/ab."))  # line 615
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 616
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 617
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 618
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 619

    def testEolDet(_):  # line 621
        ''' Check correct end-of-line detection. '''  # line 622
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 623
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 624
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 625
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 626
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 627
        _.assertIsNone(sos.eoldet(b""))  # line 628
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 629

    def testMerge(_):  # line 631
        ''' Check merge results depending on user options. '''  # line 632
        a = b"a\nb\ncc\nd"  # type: bytes  # line 633
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 634
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 635
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 636
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 637
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 638
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 639
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 640
        a = b"a\nb\ncc\nd"  # line 641
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 642
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 643
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 644
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 645
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 647
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 648
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 650
        b = b"a\nc\ne"  # line 651
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 652
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 653
        a = b"a\nb\ne"  # intra-line merge  # line 654
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 655
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 656
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 657
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 658
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 659
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 660

    def testMergeEol(_):  # line 662
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 663
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 664
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 665
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 666
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 667

    def testPickyMode(_):  # line 669
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 670
        sos.offline("trunk", None, ["--picky"])  # line 671
        changes = sos.changes()  # line 672
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 673
        out = wrapChannels(lambda _=None: sos.add(".", "./file?", options=["--force", "--relative"]))  # type: str  # line 674
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", "'.'"], out)  # line 675
        _.createFile(1, "aa")  # line 676
        sos.commit("First")  # add one file  # line 677
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 678
        _.createFile(2, "b")  # line 679
        try:  # add nothing, because picky  # line 680
            sos.commit("Second")  # add nothing, because picky  # line 680
        except:  # line 681
            pass  # line 681
        sos.add(".", "./file?")  # line 682
        sos.commit("Third")  # line 683
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 684
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 685
        _.assertIn("    r0", out)  # line 686
        sys.argv.extend(["-n", "2"])  # We cannot use the opions array for named argument options  # line 687
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 688
        sys.argv.pop()  # line 689
        sys.argv.pop()  # line 689
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 690
        _.assertIn("    r1", out)  # line 691
        _.assertIn("  * r2", out)  # line 692
        try:  # line 693
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 693
        except SystemExit as E:  # line 694
            _.assertEqual(0, E.code)  # line 694
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 695
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 696
        _.assertNotIn("    r1", out)  # line 697
        _.assertIn("  * r2", out)  # line 698
        _.createFile(3, prefix="sub")  # line 699
        sos.add("sub", "sub/file?")  # line 700
        changes = sos.changes()  # line 701
        _.assertEqual(1, len(changes.additions))  # line 702
        _.assertTrue("sub/file3" in changes.additions)  # line 703

    def testTrackedSubfolder(_):  # line 705
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 706
        os.mkdir("." + os.sep + "sub")  # line 707
        sos.offline("trunk", None, ["--track"])  # line 708
        _.createFile(1, "x")  # line 709
        _.createFile(1, "x", prefix="sub")  # line 710
        sos.add(".", "./file?")  # add glob pattern to track  # line 711
        sos.commit("First")  # line 712
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 713
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 714
        sos.commit("Second")  # one new file + meta  # line 715
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 716
        os.unlink("file1")  # remove from basefolder  # line 717
        _.createFile(2, "y")  # line 718
        sos.remove(".", "sub/file?")  # line 719
        try:  # TODO check more textual details here  # line 720
            sos.remove(".", "sub/bla")  # TODO check more textual details here  # line 720
            _.fail("Expected exit")  # TODO check more textual details here  # line 720
        except SystemExit as E:  # line 721
            _.assertEqual(1, E.code)  # line 721
        sos.commit("Third")  # line 722
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 723
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 726
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 731
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 732
        _.createFile(1)  # line 733
        _.createFile("a123a")  # untracked file "a123a"  # line 734
        sos.add(".", "./file?")  # add glob tracking pattern  # line 735
        sos.commit("second")  # versions "file1"  # line 736
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 737
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 738
        _.assertIn("  | ./file?", out)  # line 739

        _.createFile(2)  # untracked file "file2"  # line 741
        sos.commit("third")  # versions "file2"  # line 742
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 743

        os.mkdir("." + os.sep + "sub")  # line 745
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 746
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 747
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 748

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 750
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 751
        sos.add(".", "./a*a")  # add tracking pattern  # line 752
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 753
        _.assertEqual(0, len(changes.modifications))  # line 754
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 755
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 756

        sos.commit("Second_2")  # line 758
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 759
        _.existsFile(1, b"x" * 10)  # line 760
        _.existsFile(2, b"x" * 10)  # line 761

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 763
        _.existsFile(1, b"x" * 10)  # line 764
        _.existsFile("a123a", b"x" * 10)  # line 765

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 767
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 768
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 769

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 771
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 772
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 773
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 774
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 775
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 776
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 777
# TODO test switch --meta

    def testLsTracked(_):  # line 780
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 781
        _.createFile(1)  # line 782
        _.createFile("foo")  # line 783
        sos.add(".", "./file*")  # capture one file  # line 784
        sos.ls()  # line 785
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # type: str  # line 786
        _.assertInAny("TRK file1  (file*)", out)  # line 787
        _.assertNotInAny("... file1  (file*)", out)  # line 788
        _.assertInAny("    foo", out)  # line 789
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 790
        _.assertInAny("TRK file*", out)  # line 791
        _.createFile("a", prefix="sub")  # line 792
        sos.add("sub", "sub/a")  # line 793
        sos.ls("sub")  # line 794
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 795

    def testLineMerge(_):  # line 797
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 798
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 799
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 800
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 801

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 803
        _.createFile(1)  # line 804
        sos.offline("master", options=["--force"])  # line 805
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # type: str  # line 806
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 807
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 808
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 809
        _.createFile(2)  # line 810
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 811
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 812
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 813
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 814

    def testLocalConfig(_):  # line 816
        sos.offline("bla", options=[])  # line 817
        try:  # line 818
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 818
        except SystemExit as E:  # line 819
            _.assertEqual(0, E.code)  # line 819
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 820

    def testConfigVariations(_):  # line 822
        def makeRepo():  # line 823
            try:  # line 824
                os.unlink("file1")  # line 824
            except:  # line 825
                pass  # line 825
            sos.offline("master", options=["--force"])  # line 826
            _.createFile(1)  # line 827
            sos.commit("Added file1")  # line 828
        try:  # line 829
            sos.config(["set", "strict", "on"])  # line 829
        except SystemExit as E:  # line 830
            _.assertEqual(0, E.code)  # line 830
        makeRepo()  # line 831
        _.assertTrue(checkRepoFlag("strict", True))  # line 832
        try:  # line 833
            sos.config(["set", "strict", "off"])  # line 833
        except SystemExit as E:  # line 834
            _.assertEqual(0, E.code)  # line 834
        makeRepo()  # line 835
        _.assertTrue(checkRepoFlag("strict", False))  # line 836
        try:  # line 837
            sos.config(["set", "strict", "yes"])  # line 837
        except SystemExit as E:  # line 838
            _.assertEqual(0, E.code)  # line 838
        makeRepo()  # line 839
        _.assertTrue(checkRepoFlag("strict", True))  # line 840
        try:  # line 841
            sos.config(["set", "strict", "no"])  # line 841
        except SystemExit as E:  # line 842
            _.assertEqual(0, E.code)  # line 842
        makeRepo()  # line 843
        _.assertTrue(checkRepoFlag("strict", False))  # line 844
        try:  # line 845
            sos.config(["set", "strict", "1"])  # line 845
        except SystemExit as E:  # line 846
            _.assertEqual(0, E.code)  # line 846
        makeRepo()  # line 847
        _.assertTrue(checkRepoFlag("strict", True))  # line 848
        try:  # line 849
            sos.config(["set", "strict", "0"])  # line 849
        except SystemExit as E:  # line 850
            _.assertEqual(0, E.code)  # line 850
        makeRepo()  # line 851
        _.assertTrue(checkRepoFlag("strict", False))  # line 852
        try:  # line 853
            sos.config(["set", "strict", "true"])  # line 853
        except SystemExit as E:  # line 854
            _.assertEqual(0, E.code)  # line 854
        makeRepo()  # line 855
        _.assertTrue(checkRepoFlag("strict", True))  # line 856
        try:  # line 857
            sos.config(["set", "strict", "false"])  # line 857
        except SystemExit as E:  # line 858
            _.assertEqual(0, E.code)  # line 858
        makeRepo()  # line 859
        _.assertTrue(checkRepoFlag("strict", False))  # line 860
        try:  # line 861
            sos.config(["set", "strict", "enable"])  # line 861
        except SystemExit as E:  # line 862
            _.assertEqual(0, E.code)  # line 862
        makeRepo()  # line 863
        _.assertTrue(checkRepoFlag("strict", True))  # line 864
        try:  # line 865
            sos.config(["set", "strict", "disable"])  # line 865
        except SystemExit as E:  # line 866
            _.assertEqual(0, E.code)  # line 866
        makeRepo()  # line 867
        _.assertTrue(checkRepoFlag("strict", False))  # line 868
        try:  # line 869
            sos.config(["set", "strict", "enabled"])  # line 869
        except SystemExit as E:  # line 870
            _.assertEqual(0, E.code)  # line 870
        makeRepo()  # line 871
        _.assertTrue(checkRepoFlag("strict", True))  # line 872
        try:  # line 873
            sos.config(["set", "strict", "disabled"])  # line 873
        except SystemExit as E:  # line 874
            _.assertEqual(0, E.code)  # line 874
        makeRepo()  # line 875
        _.assertTrue(checkRepoFlag("strict", False))  # line 876
        try:  # line 877
            sos.config(["set", "strict", "nope"])  # line 877
            _.fail()  # line 877
        except SystemExit as E:  # line 878
            _.assertEqual(1, E.code)  # line 878

    def testLsSimple(_):  # line 880
        _.createFile(1)  # line 881
        _.createFile("foo")  # line 882
        _.createFile("ign1")  # line 883
        _.createFile("ign2")  # line 884
        _.createFile("bar", prefix="sub")  # line 885
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 886
        try:  # define an ignore pattern  # line 887
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern  # line 887
        except SystemExit as E:  # line 888
            _.assertEqual(0, E.code)  # line 888
        try:  # additional ignore pattern  # line 889
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 889
        except SystemExit as E:  # line 890
            _.assertEqual(0, E.code)  # line 890
        try:  # define a list of ignore patterns  # line 891
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 891
        except SystemExit as E:  # line 892
            _.assertEqual(0, E.code)  # line 892
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # type: str  # line 893
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 894
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 895
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 896
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 897
        _.assertInAny('    file1', out)  # line 898
        _.assertInAny('    ign1', out)  # line 899
        _.assertInAny('    ign2', out)  # line 900
        _.assertNotIn('DIR sub', out)  # line 901
        _.assertNotIn('    bar', out)  # line 902
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 903
        _.assertIn('DIR sub', out)  # line 904
        _.assertIn('    bar', out)  # line 905
        try:  # line 906
            sos.config(["rm", "foo", "bar"])  # line 906
            _.fail()  # line 906
        except SystemExit as E:  # line 907
            _.assertEqual(1, E.code)  # line 907
        try:  # line 908
            sos.config(["rm", "ignores", "foo"])  # line 908
            _.fail()  # line 908
        except SystemExit as E:  # line 909
            _.assertEqual(1, E.code)  # line 909
        try:  # line 910
            sos.config(["rm", "ignores", "ign1"])  # line 910
        except SystemExit as E:  # line 911
            _.assertEqual(0, E.code)  # line 911
        try:  # remove ignore pattern  # line 912
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 912
        except SystemExit as E:  # line 913
            _.assertEqual(0, E.code)  # line 913
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 914
        _.assertInAny('    ign1', out)  # line 915
        _.assertInAny('IGN ign2', out)  # line 916
        _.assertNotInAny('    ign2', out)  # line 917

    def testWhitelist(_):  # line 919
# TODO test same for simple mode
        _.createFile(1)  # line 921
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 922
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 923
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 924
        sos.commit(options=["--force"])  # attempt to commit the file  # line 925
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 926
        try:  # Exit because dirty  # line 927
            sos.online()  # Exit because dirty  # line 927
            _.fail()  # Exit because dirty  # line 927
        except:  # exception expected  # line 928
            pass  # exception expected  # line 928
        _.createFile("x2")  # add another change  # line 929
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 930
        try:  # force beyond dirty flag check  # line 931
            sos.online(["--force"])  # force beyond dirty flag check  # line 931
            _.fail()  # force beyond dirty flag check  # line 931
        except:  # line 932
            pass  # line 932
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 933
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 934

        _.createFile(1)  # line 936
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 937
        sos.offline("xx", None, ["--track"])  # line 938
        sos.add(".", "./file*")  # line 939
        sos.commit()  # should NOT ask for force here  # line 940
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 941

    def testRemove(_):  # line 943
        _.createFile(1, "x" * 100)  # line 944
        sos.offline("trunk")  # line 945
        try:  # line 946
            sos.destroy("trunk")  # line 946
            _fail()  # line 946
        except:  # line 947
            pass  # line 947
        _.createFile(2, "y" * 10)  # line 948
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 949
        sos.destroy("trunk")  # line 950
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 951
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 952
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 953
        sos.branch("next")  # line 954
        _.createFile(3, "y" * 10)  # make a change  # line 955
        sos.destroy("added", "--force")  # should succeed  # line 956

    def testFastBranchingOnEmptyHistory(_):  # line 958
        ''' Test fast branching without revisions and with them. '''  # line 959
        sos.offline(options=["--strict", "--compress"])  # b0  # line 960
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 961
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 962
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 963
        sos.destroy("2")  # line 964
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 965
        _.assertIn("b0 'trunk' @", out)  # line 966
        _.assertIn("b1         @", out)  # line 967
        _.assertIn("b3         @", out)  # line 968
        _.assertNotIn("b2         @", out)  # line 969
        sos.branch("", "")  # non-fast branching of b4  # line 970
        _.createFile(1)  # line 971
        _.createFile(2)  # line 972
        sos.commit("")  # line 973
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 974
        sos.destroy("4")  # line 975
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 976
        _.assertIn("b0 'trunk' @", out)  # line 977
        _.assertIn("b1         @", out)  # line 978
        _.assertIn("b3         @", out)  # line 979
        _.assertIn("b5         @", out)  # line 980
        _.assertNotIn("b2         @", out)  # line 981
        _.assertNotIn("b4         @", out)  # line 982
# TODO add more files and branch again

    def testUsage(_):  # line 985
        try:  # TODO expect sys.exit(0)  # line 986
            sos.usage()  # TODO expect sys.exit(0)  # line 986
            _.fail()  # TODO expect sys.exit(0)  # line 986
        except:  # line 987
            pass  # line 987
        try:  # TODO expect sys.exit(0)  # line 988
            sos.usage("help")  # TODO expect sys.exit(0)  # line 988
            _.fail()  # TODO expect sys.exit(0)  # line 988
        except:  # line 989
            pass  # line 989
        try:  # TODO expect sys.exit(0)  # line 990
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 990
            _.fail()  # TODO expect sys.exit(0)  # line 990
        except:  # line 991
            pass  # line 991
        try:  # line 992
            sos.usage(version=True)  # line 992
            _.fail()  # line 992
        except:  # line 993
            pass  # line 993
        try:  # line 994
            sos.usage(version=True)  # line 994
            _.fail()  # line 994
        except:  # line 995
            pass  # line 995

    def testOnlyExcept(_):  # line 997
        ''' Test blacklist glob rules. '''  # line 998
        sos.offline(options=["--track"])  # line 999
        _.createFile("a.1")  # line 1000
        _.createFile("a.2")  # line 1001
        _.createFile("b.1")  # line 1002
        _.createFile("b.2")  # line 1003
        sos.add(".", "./a.?")  # line 1004
        sos.add(".", "./?.1", negative=True)  # line 1005
        out = wrapChannels(lambda _=None: sos.commit())  # type: str  # line 1006
        _.assertIn("ADD ./a.2", out)  # line 1007
        _.assertNotIn("ADD ./a.1", out)  # line 1008
        _.assertNotIn("ADD ./b.1", out)  # line 1009
        _.assertNotIn("ADD ./b.2", out)  # line 1010

    def testOnly(_):  # line 1012
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 1013
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1014
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1015
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1016
        sos.offline(options=["--track", "--strict"])  # line 1017
        _.createFile(1)  # line 1018
        _.createFile(2)  # line 1019
        sos.add(".", "./file1")  # line 1020
        sos.add(".", "./file2")  # line 1021
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1022
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1023
        sos.commit()  # adds also file2  # line 1024
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1025
        _.createFile(1, "cc")  # modify both files  # line 1026
        _.createFile(2, "dd")  # line 1027
        try:  # line 1028
            sos.config(["set", "texttype", "file2"])  # line 1028
        except SystemExit as E:  # line 1029
            _.assertEqual(0, E.code)  # line 1029
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1030
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1031
        _.assertTrue("./file2" in changes.modifications)  # line 1032
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 1033
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1034
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1035
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # line 1036

    def testDiff(_):  # line 1038
        try:  # manually mark this file as "textual"  # line 1039
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1039
        except SystemExit as E:  # line 1040
            _.assertEqual(0, E.code)  # line 1040
        sos.offline(options=["--strict"])  # line 1041
        _.createFile(1)  # line 1042
        _.createFile(2)  # line 1043
        sos.commit()  # line 1044
        _.createFile(1, "sdfsdgfsdf")  # line 1045
        _.createFile(2, "12343")  # line 1046
        sos.commit()  # line 1047
        _.createFile(1, "foobar")  # line 1048
        _.createFile(3)  # line 1049
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # type: str  # compare with r1 (second counting from last which is r2)  # line 1050
        _.assertIn("ADD ./file3", out)  # line 1051
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "-~- 0 |xxxxxxxxxx|", "+~+ 0 |foobar|"], out)  # line 1052
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1053

    def testReorderRenameActions(_):  # line 1055
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1056
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1057
        try:  # line 1058
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1058
            _.fail()  # line 1058
        except:  # line 1059
            pass  # line 1059

    def testPublish(_):  # line 1061
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1062

    def testMove(_):  # line 1064
        ''' Move primarily modifies tracking patterns and moves files around accordingly. '''  # line 1065
        sos.offline(options=["--strict", "--track"])  # line 1066
        _.createFile(1)  # line 1067
        sos.add(".", "./file?")  # line 1068
# assert error when source folder is missing
        out = wrapChannels(lambda _=None: sos.move("sub", "sub/file?", ".", "./?file"))  # type: str  # line 1070
        _.assertIn("Source folder doesn't exist", out)  # line 1071
        _.assertIn("EXIT CODE 1", out)  # line 1072
# if target folder missing: create it and move matching files into it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1074
        _.assertTrue(os.path.exists("sub"))  # line 1075
        _.assertTrue(os.path.exists("sub/file1"))  # line 1076
        _.assertFalse(os.path.exists("file1"))  # line 1077
# test move back to previous location, plus rename the file
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1079
        _.assertTrue(os.path.exists("1file"))  # line 1080
        _.assertFalse(os.path.exists("sub/file1"))  # line 1081
# assert error when nothing matches source pattern
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*"))  # line 1083
        _.assertIn("No files match the specified file pattern", out)  # line 1084
        _.assertIn("EXIT CODE", out)  # line 1085
        sos.add(".", "./*")  # add catch-all tracking pattern to root folder  # line 1086
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*", options=["--force"]))  # line 1087
        _.assertIn("  './*' matches 3 files", out)  # line 1088
        _.assertIn("EXIT CODE", out)  # line 1089
# test rename no conflict
        _.createFile(1)  # line 1091
        _.createFile(2)  # line 1092
        _.createFile(3)  # line 1093
        sos.add(".", "./file*")  # line 1094
        sos.remove(".", "./*")  # line 1095
        try:  # define an ignore pattern  # line 1096
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1096
        except SystemExit as E:  # line 1097
            _.assertEqual(0, E.code)  # line 1097
        try:  # line 1098
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1098
        except SystemExit as E:  # line 1099
            _.assertEqual(0, E.code)  # line 1099
        sos.move(".", "./file*", ".", "./fi*le")  # should only move not ignored files files  # line 1100
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1101
        _.assertTrue(all((not os.path.exists("file%d" % i) for i in range(1, 4))))  # line 1102
        _.assertFalse(os.path.exists("fi4le"))  # line 1103
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1105
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # untrack pattern, which was renamed before  # line 1109
        sos.add(".", "./?a?b", ["--force"])  # line 1110
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1111
        _.createFile("1a2b")  # should not be tracked  # line 1112
        _.createFile("a1b2")  # should be tracked  # line 1113
        sos.commit()  # line 1114
        _.assertEqual(5, len(os.listdir(sos.revisionFolder(0, 1))))  # meta, a1b2, fi[1-3]le  # line 1115
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1116
        _.createFile("1a1b1")  # line 1117
        _.createFile("1a1b2")  # line 1118
        sos.add(".", "./?a?b*")  # line 1119
# test target pattern exists
        out = wrapChannels(lambda _=None: sos.move(".", "./?a?b*", ".", "./z?z?"))  # line 1121
        _.assertIn("not unique", out)  # line 1122
# TODO only rename if actually any files are versioned? or simply what is currently alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1126
        _.createFile(1)  # line 1127
        _.createFile(3)  # line 1128
        _.createFile(5)  # line 1129
        sos.offline()  # branch 0: only file1  # line 1130
        sos.branch()  # line 1131
        os.unlink("file1")  # line 1132
        os.unlink("file3")  # line 1133
        os.unlink("file5")  # line 1134
        _.createFile(2)  # line 1135
        _.createFile(4)  # line 1136
        _.createFile(6)  # line 1137
        sos.commit()  # branch 1: only file2  # line 1138
        sos.switch("0/")  # line 1139
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1140
        _.assertFalse(_.existsFile(1))  # line 1141
        _.assertFalse(_.existsFile(3))  # line 1142
        _.assertFalse(_.existsFile(5))  # line 1143
        _.assertTrue(_.existsFile(2))  # line 1144
        _.assertTrue(_.existsFile(4))  # line 1145
        _.assertTrue(_.existsFile(6))  # line 1146

    def testMoveDetection(_):  # line 1148
        _.createFile(1, "bla")  # line 1149
        sos.offline()  # line 1150
        os.mkdir("sub1")  # line 1151
        os.mkdir("sub2")  # line 1152
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1153
        shutil.move("file1", "sub2")  # line 1154
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 1155
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1156
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1157
        sos.commit("Moved the file")  # line 1158
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1162

    def testHashCollision(_):  # line 1164
        old = sos.Metadata.findChanges  # line 1165
        @_coconut_tco  # line 1166
        def patched(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 1166
            import collections  # used only in this method  # line 1167
            write = branch is not None and revision is not None  # line 1168
            if write:  # line 1169
                try:  # line 1170
                    os.makedirs(sos.encode(sos.revisionFolder(branch, revision, base=_.root)))  # line 1170
                except FileExistsError:  # HINT "try" only necessary for hash collision *test code* (!)  # line 1171
                    pass  # HINT "try" only necessary for hash collision *test code* (!)  # line 1171
            return _coconut_tail_call(old, _, branch, revision, checkContent, inverse, considerOnly, dontConsider, progress)  # line 1172
        sos.Metadata.findChanges = patched  # monkey-patch  # line 1173
        sos.offline()  # line 1174
        _.createFile(1)  # line 1175
        os.mkdir(sos.revisionFolder(0, 1))  # line 1176
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # hashed file name for not-yet-committed file1  # line 1177
        _.createFile(1)  # line 1178
        try:  # line 1179
            sos.commit()  # line 1179
            _.fail("Expected system exit due to hash collision detection")  # line 1179
        except SystemExit as E:  # HINT exit is implemented in utility.hashFile  # line 1180
            _.assertEqual(1, E.code)  # HINT exit is implemented in utility.hashFile  # line 1180
        sos.Metadata.findChanges = old  # revert monkey patch  # line 1181

    def testFindBase(_):  # line 1183
        old = os.getcwd()  # line 1184
        try:  # line 1185
            os.mkdir("." + os.sep + ".git")  # line 1186
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1187
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1188
            os.chdir("a" + os.sep + "b")  # line 1189
            s, vcs, cmd = sos.findSosVcsBase()  # line 1190
            _.assertIsNotNone(s)  # line 1191
            _.assertIsNotNone(vcs)  # line 1192
            _.assertEqual("git", cmd)  # line 1193
        finally:  # line 1194
            os.chdir(old)  # line 1194

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1205
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1206
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1207
