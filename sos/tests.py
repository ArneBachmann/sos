#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xdf2c2fd9

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
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # line 210
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
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # type: str  # line 227
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
        sos.add("sub", "sub/file?")  # line 239
        sos.commit("test")  # should pick up sub/file1 pattern  # line 240
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 241
        _.createFile(1)  # line 242
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 243
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 243
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 243
        except:  # line 244
            pass  # line 244

    def testNoArgs(_):  # line 246
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 247

    def testAutoMetadataUpgrade(_):  # line 249
        sos.offline()  # line 250
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 251
            repo, branches, config = json.load(fd)  # line 251
        repo["version"] = None  # lower than any pip version  # line 252
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 253
        del repo["format"]  # simulate pre-1.3.5  # line 254
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 255
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 255
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # line 256
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 257

    def testFastBranching(_):  # line 259
        _.createFile(1)  # line 260
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict"]))  # b0/r0 = ./file1  # line 261
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 262
        _.createFile(2)  # line 263
        os.unlink("file1")  # line 264
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 265
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 266
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 267
        _.createFile(3)  # line 268
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 269
        _.assertAllIn([sos.metaFile, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 270
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 271
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 272
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 273
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 274
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 275
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 278
        now = time.time()  # type: float  # line 279
        _.createFile(1)  # line 280
        sync()  # line 281
        sos.offline(options=["--strict"])  # line 282
        _.createFile(1, "abc")  # modify contents  # line 283
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 284
        sync()  # line 285
        out = wrapChannels(lambda _=None: sos.changes())  # line 286
        _.assertIn("<older than previously committed>", out)  # line 287
        out = wrapChannels(lambda _=None: sos.commit())  # line 288
        _.assertIn("<older than previously committed>", out)  # line 289

    def testGetParentBranch(_):  # line 291
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 292
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 293
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 294
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 295
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 296

    def testTokenizeGlobPattern(_):  # line 298
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 299
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 300
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 301
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 302
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 303
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 304

    def testTokenizeGlobPatterns(_):  # line 306
        try:  # because number of literal strings differs  # line 307
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 307
            _.fail()  # because number of literal strings differs  # line 307
        except:  # line 308
            pass  # line 308
        try:  # because glob patterns differ  # line 309
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 309
            _.fail()  # because glob patterns differ  # line 309
        except:  # line 310
            pass  # line 310
        try:  # glob patterns differ, regardless of position  # line 311
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 311
            _.fail()  # glob patterns differ, regardless of position  # line 311
        except:  # line 312
            pass  # line 312
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 313
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 314
        try:  # succeeds, because glob patterns match (differ only in position)  # line 315
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 315
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 315
        except:  # line 316
            pass  # line 316

    def testConvertGlobFiles(_):  # line 318
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 319
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 320

    def testFolderRemove(_):  # line 322
        m = sos.Metadata(os.getcwd())  # line 323
        _.createFile(1)  # line 324
        _.createFile("a", prefix="sub")  # line 325
        sos.offline()  # line 326
        _.createFile(2)  # line 327
        os.unlink("sub" + os.sep + "a")  # line 328
        os.rmdir("sub")  # line 329
        changes = sos.changes()  # TODO replace by output check  # line 330
        _.assertEqual(1, len(changes.additions))  # line 331
        _.assertEqual(0, len(changes.modifications))  # line 332
        _.assertEqual(1, len(changes.deletions))  # line 333
        _.createFile("a", prefix="sub")  # line 334
        changes = sos.changes()  # line 335
        _.assertEqual(0, len(changes.deletions))  # line 336

    def testSwitchConflict(_):  # line 338
        sos.offline(options=["--strict"])  # (r0)  # line 339
        _.createFile(1)  # line 340
        sos.commit()  # add file (r1)  # line 341
        os.unlink("file1")  # line 342
        sos.commit()  # remove (r2)  # line 343
        _.createFile(1, "something else")  # line 344
        sos.commit()  # (r3)  # line 345
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 346
        _.existsFile(1, "x" * 10)  # line 347
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 348
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 349
        sos.switch("/1")  # add file1 back  # line 350
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 351
        _.existsFile(1, "something else")  # line 352

    def testComputeSequentialPathSet(_):  # line 354
        os.makedirs(sos.revisionFolder(0, 0))  # line 355
        os.makedirs(sos.revisionFolder(0, 1))  # line 356
        os.makedirs(sos.revisionFolder(0, 2))  # line 357
        os.makedirs(sos.revisionFolder(0, 3))  # line 358
        os.makedirs(sos.revisionFolder(0, 4))  # line 359
        m = sos.Metadata(os.getcwd())  # line 360
        m.branch = 0  # line 361
        m.commit = 2  # line 362
        m.saveBranches()  # line 363
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 364
        m.saveCommit(0, 0)  # initial  # line 365
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 366
        m.saveCommit(0, 1)  # mod  # line 367
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 368
        m.saveCommit(0, 2)  # add  # line 369
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 370
        m.saveCommit(0, 3)  # del  # line 371
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 372
        m.saveCommit(0, 4)  # readd  # line 373
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 374
        m.saveBranch(0)  # line 375
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 376
        m.saveBranches()  # line 377
        m.computeSequentialPathSet(0, 4)  # line 378
        _.assertEqual(2, len(m.paths))  # line 379

    def testParseRevisionString(_):  # line 381
        m = sos.Metadata(os.getcwd())  # line 382
        m.branch = 1  # line 383
        m.commits = {0: 0, 1: 1, 2: 2}  # line 384
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 385
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 386
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 387
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 388
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 389
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 390
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 391

    def testOfflineEmpty(_):  # line 393
        os.mkdir("." + os.sep + sos.metaFolder)  # line 394
        try:  # line 395
            sos.offline("trunk")  # line 395
            _.fail()  # line 395
        except SystemExit as E:  # line 396
            _.assertEqual(1, E.code)  # line 396
        os.rmdir("." + os.sep + sos.metaFolder)  # line 397
        sos.offline("test")  # line 398
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 399
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 400
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 401
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 402
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 403
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 404

    def testOfflineWithFiles(_):  # line 406
        _.createFile(1, "x" * 100)  # line 407
        _.createFile(2)  # line 408
        sos.offline("test")  # line 409
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 410
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 411
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 412
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 413
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 414
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 415
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 416

    def testBranch(_):  # line 418
        _.createFile(1, "x" * 100)  # line 419
        _.createFile(2)  # line 420
        sos.offline("test")  # b0/r0  # line 421
        sos.branch("other")  # b1/r0  # line 422
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 423
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 424
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 426
        _.createFile(1, "z")  # modify file  # line 428
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 429
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 430
        _.createFile(3, "z")  # line 432
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 433
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 434
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 439
        _.createFile(1, "x" * 100)  # line 440
        _.createFile(2)  # line 441
        sos.offline("test")  # line 442
        changes = sos.changes()  # line 443
        _.assertEqual(0, len(changes.additions))  # line 444
        _.assertEqual(0, len(changes.deletions))  # line 445
        _.assertEqual(0, len(changes.modifications))  # line 446
        _.createFile(1, "z")  # size change  # line 447
        changes = sos.changes()  # line 448
        _.assertEqual(0, len(changes.additions))  # line 449
        _.assertEqual(0, len(changes.deletions))  # line 450
        _.assertEqual(1, len(changes.modifications))  # line 451
        sos.commit("message")  # line 452
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 453
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 454
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 455
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 456
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 457
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 458
        os.unlink("file2")  # line 459
        changes = sos.changes()  # line 460
        _.assertEqual(0, len(changes.additions))  # line 461
        _.assertEqual(1, len(changes.deletions))  # line 462
        _.assertEqual(1, len(changes.modifications))  # line 463
        sos.commit("modified")  # line 464
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 465
        try:  # expecting Exit due to no changes  # line 466
            sos.commit("nothing")  # expecting Exit due to no changes  # line 466
            _.fail()  # expecting Exit due to no changes  # line 466
        except:  # line 467
            pass  # line 467

    def testGetBranch(_):  # line 469
        m = sos.Metadata(os.getcwd())  # line 470
        m.branch = 1  # current branch  # line 471
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 472
        _.assertEqual(27, m.getBranchByName(27))  # line 473
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 474
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 475
        _.assertIsNone(m.getBranchByName("unknown"))  # line 476
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 477
        _.assertEqual(13, m.getRevisionByName("13"))  # line 478
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 479
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 480

    def testTagging(_):  # line 482
        m = sos.Metadata(os.getcwd())  # line 483
        sos.offline()  # line 484
        _.createFile(111)  # line 485
        sos.commit("tag", ["--tag"])  # line 486
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # line 487
        _.assertTrue(any(("|tag" in line and line.endswith("|TAG") for line in out)))  # line 488
        _.createFile(2)  # line 489
        try:  # line 490
            sos.commit("tag")  # line 490
            _.fail()  # line 490
        except:  # line 491
            pass  # line 491
        sos.commit("tag-2", ["--tag"])  # line 492
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 493
        _.assertIn("TAG tag", out)  # line 494

    def testSwitch(_):  # line 496
        _.createFile(1, "x" * 100)  # line 497
        _.createFile(2, "y")  # line 498
        sos.offline("test")  # file1-2  in initial branch commit  # line 499
        sos.branch("second")  # file1-2  switch, having same files  # line 500
        sos.switch("0")  # no change  switch back, no problem  # line 501
        sos.switch("second")  # no change  # switch back, no problem  # line 502
        _.createFile(3, "y")  # generate a file  # line 503
        try:  # uncommited changes detected  # line 504
            sos.switch("test")  # uncommited changes detected  # line 504
            _.fail()  # uncommited changes detected  # line 504
        except SystemExit as E:  # line 505
            _.assertEqual(1, E.code)  # line 505
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 506
        sos.changes()  # line 507
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 508
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 509
        _.createFile("XXX")  # line 510
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 511
        _.assertIn("File tree has changes", out)  # line 512
        _.assertNotIn("File tree is unchanged", out)  # line 513
        _.assertIn("  * b0   'test'", out)  # line 514
        _.assertIn("    b1 'second'", out)  # line 515
        _.assertIn("(modified)", out)  # one branch has commits  # line 516
        _.assertIn("(in sync)", out)  # the other doesn't  # line 517
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 518
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 519
        _.assertAllIn(["Metadata format", "Content checking:    deactivated", "Data compression:    deactivated", "Repository mode:     simple", "Number of branches:  2"], out)  # line 520
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 521
        _.createFile(4, "xy")  # generate a file  # line 522
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 523
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 524
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 525
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 526
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 527
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 528
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 529
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 530
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 531
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 532
        _.assertNotIn("Creating backup", out)  # line 533
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 534
        _.assertIn("Dumping revisions", out)  # line 535
        _.assertNotIn("Creating backup", out)  # line 536
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 537
        _.assertAllIn(["Creating backup"], out)  # line 538
        _.assertIn("Dumping revisions", out)  # line 539
        sos.verbose.pop()  # line 540

    def testAutoDetectVCS(_):  # line 542
        os.mkdir(".git")  # line 543
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 544
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 545
            meta = fd.read()  # line 545
        _.assertTrue("\"master\"" in meta)  # line 546
        os.rmdir(".git")  # line 547

    def testUpdate(_):  # line 549
        sos.offline("trunk")  # create initial branch b0/r0  # line 550
        _.createFile(1, "x" * 100)  # line 551
        sos.commit("second")  # create b0/r1  # line 552

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 554
        _.assertFalse(_.existsFile(1))  # line 555

        sos.update("/1")  # recreate file1  # line 557
        _.assertTrue(_.existsFile(1))  # line 558

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 560
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 561
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 562
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 563

        sos.update("/1")  # do nothing, as nothing has changed  # line 565
        _.assertTrue(_.existsFile(1))  # line 566

        _.createFile(2, "y" * 100)  # line 568
#    out = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 571
        _.assertTrue(_.existsFile(2))  # line 572
        sos.update("trunk", ["--add"])  # only add stuff  # line 573
        _.assertTrue(_.existsFile(2))  # line 574
        sos.update("trunk")  # nothing to do  # line 575
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 576

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 578
        _.createFile(10, theirs)  # line 579
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 580
        _.createFile(11, mine)  # line 581
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 582
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 583

    def testUpdate2(_):  # line 585
        _.createFile("test.txt", "x" * 10)  # line 586
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 587
        sync()  # line 588
        sos.branch("mod")  # line 589
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 590
        sos.commit("mod")  # create b0/r1  # line 591
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 592
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 593
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 594
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 595
        _.createFile("test.txt", "x" * 10)  # line 596
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 597
        sync()  # line 598
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 599
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 600
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 601
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 602
        sync()  # line 603
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 604
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 605

    def testIsTextType(_):  # line 607
        m = sos.Metadata(".")  # line 608
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 609
        m.c.bintype = ["*.md.confluence"]  # line 610
        _.assertTrue(m.isTextType("ab.txt"))  # line 611
        _.assertTrue(m.isTextType("./ab.txt"))  # line 612
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 613
        _.assertFalse(m.isTextType("bc/ab."))  # line 614
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 615
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 616
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 617
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 618

    def testEolDet(_):  # line 620
        ''' Check correct end-of-line detection. '''  # line 621
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 622
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 623
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 624
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 625
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 626
        _.assertIsNone(sos.eoldet(b""))  # line 627
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 628

    def testMerge(_):  # line 630
        ''' Check merge results depending on user options. '''  # line 631
        a = b"a\nb\ncc\nd"  # type: bytes  # line 632
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 633
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 634
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 635
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 636
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 637
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 638
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 639
        a = b"a\nb\ncc\nd"  # line 640
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 641
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 642
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 643
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 644
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 646
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 647
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 649
        b = b"a\nc\ne"  # line 650
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 651
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 652
        a = b"a\nb\ne"  # intra-line merge  # line 653
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 654
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 655
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 656
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 657
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 658
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 659

    def testMergeEol(_):  # line 661
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 662
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 663
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 664
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 665
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 666

    def testPickyMode(_):  # line 668
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 669
        sos.offline("trunk", None, ["--picky"])  # line 670
        changes = sos.changes()  # line 671
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 672
        sos.add(".", "./file?", ["--force"])  # line 673
        _.createFile(1, "aa")  # line 674
        sos.commit("First")  # add one file  # line 675
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 676
        _.createFile(2, "b")  # line 677
        try:  # add nothing, because picky  # line 678
            sos.commit("Second")  # add nothing, because picky  # line 678
        except:  # line 679
            pass  # line 679
        sos.add(".", "./file?")  # line 680
        sos.commit("Third")  # line 681
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 682
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 683
        _.assertIn("    r0", out)  # line 684
        sys.argv.extend(["-n", "2"])  # line 685
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 686
        sys.argv.pop()  # line 687
        sys.argv.pop()  # line 687
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 688
        _.assertIn("    r1", out)  # line 689
        _.assertIn("  * r2", out)  # line 690
        try:  # line 691
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 691
        except SystemExit as E:  # line 692
            _.assertEqual(0, E.code)  # line 692
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 693
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 694
        _.assertNotIn("    r1", out)  # line 695
        _.assertIn("  * r2", out)  # line 696
        _.createFile(3, prefix="sub")  # line 697
        sos.add("sub", "sub/file?")  # line 698
        changes = sos.changes()  # line 699
        _.assertEqual(1, len(changes.additions))  # line 700
        _.assertTrue("sub/file3" in changes.additions)  # line 701

    def testTrackedSubfolder(_):  # line 703
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 704
        os.mkdir("." + os.sep + "sub")  # line 705
        sos.offline("trunk", None, ["--track"])  # line 706
        _.createFile(1, "x")  # line 707
        _.createFile(1, "x", prefix="sub")  # line 708
        sos.add(".", "./file?")  # add glob pattern to track  # line 709
        sos.commit("First")  # line 710
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 711
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 712
        sos.commit("Second")  # one new file + meta  # line 713
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 714
        os.unlink("file1")  # remove from basefolder  # line 715
        _.createFile(2, "y")  # line 716
        sos.remove(".", "sub/file?")  # line 717
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 718
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 718
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 718
        except:  # line 719
            pass  # line 719
        sos.commit("Third")  # line 720
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 721
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 724
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 729
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 730
        _.createFile(1)  # line 731
        _.createFile("a123a")  # untracked file "a123a"  # line 732
        sos.add(".", "./file?")  # add glob tracking pattern  # line 733
        sos.commit("second")  # versions "file1"  # line 734
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 735
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 736
        _.assertIn("  | ./file?", out)  # line 737

        _.createFile(2)  # untracked file "file2"  # line 739
        sos.commit("third")  # versions "file2"  # line 740
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 741

        os.mkdir("." + os.sep + "sub")  # line 743
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 744
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 745
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 746

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 748
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 749
        sos.add(".", "./a*a")  # add tracking pattern  # line 750
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 751
        _.assertEqual(0, len(changes.modifications))  # line 752
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 753
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 754

        sos.commit("Second_2")  # line 756
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 757
        _.existsFile(1, b"x" * 10)  # line 758
        _.existsFile(2, b"x" * 10)  # line 759

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 761
        _.existsFile(1, b"x" * 10)  # line 762
        _.existsFile("a123a", b"x" * 10)  # line 763

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 765
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 766
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 767

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 769
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 770
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 771
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 772
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 773
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 774
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 775
# TODO test switch --meta

    def testLsTracked(_):  # line 778
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 779
        _.createFile(1)  # line 780
        _.createFile("foo")  # line 781
        sos.add(".", "./file*")  # capture one file  # line 782
        sos.ls()  # line 783
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 784
        _.assertInAny("TRK file1  (file*)", out)  # line 785
        _.assertNotInAny("... file1  (file*)", out)  # line 786
        _.assertInAny("    foo", out)  # line 787
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 788
        _.assertInAny("TRK file*", out)  # line 789
        _.createFile("a", prefix="sub")  # line 790
        sos.add("sub", "sub/a")  # line 791
        sos.ls("sub")  # line 792
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 793

    def testLineMerge(_):  # line 795
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 796
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 797
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 798
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 799

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 801
        _.createFile(1)  # line 802
        sos.offline("master", options=["--force"])  # line 803
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # line 804
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 805
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 806
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 807
        _.createFile(2)  # line 808
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 809
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 810
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 811
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 812

    def testLocalConfig(_):  # line 814
        sos.offline("bla", options=[])  # line 815
        try:  # line 816
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 816
        except SystemExit as E:  # line 817
            _.assertEqual(0, E.code)  # line 817
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 818

    def testConfigVariations(_):  # line 820
        def makeRepo():  # line 821
            try:  # line 822
                os.unlink("file1")  # line 822
            except:  # line 823
                pass  # line 823
            sos.offline("master", options=["--force"])  # line 824
            _.createFile(1)  # line 825
            sos.commit("Added file1")  # line 826
        try:  # line 827
            sos.config(["set", "strict", "on"])  # line 827
        except SystemExit as E:  # line 828
            _.assertEqual(0, E.code)  # line 828
        makeRepo()  # line 829
        _.assertTrue(checkRepoFlag("strict", True))  # line 830
        try:  # line 831
            sos.config(["set", "strict", "off"])  # line 831
        except SystemExit as E:  # line 832
            _.assertEqual(0, E.code)  # line 832
        makeRepo()  # line 833
        _.assertTrue(checkRepoFlag("strict", False))  # line 834
        try:  # line 835
            sos.config(["set", "strict", "yes"])  # line 835
        except SystemExit as E:  # line 836
            _.assertEqual(0, E.code)  # line 836
        makeRepo()  # line 837
        _.assertTrue(checkRepoFlag("strict", True))  # line 838
        try:  # line 839
            sos.config(["set", "strict", "no"])  # line 839
        except SystemExit as E:  # line 840
            _.assertEqual(0, E.code)  # line 840
        makeRepo()  # line 841
        _.assertTrue(checkRepoFlag("strict", False))  # line 842
        try:  # line 843
            sos.config(["set", "strict", "1"])  # line 843
        except SystemExit as E:  # line 844
            _.assertEqual(0, E.code)  # line 844
        makeRepo()  # line 845
        _.assertTrue(checkRepoFlag("strict", True))  # line 846
        try:  # line 847
            sos.config(["set", "strict", "0"])  # line 847
        except SystemExit as E:  # line 848
            _.assertEqual(0, E.code)  # line 848
        makeRepo()  # line 849
        _.assertTrue(checkRepoFlag("strict", False))  # line 850
        try:  # line 851
            sos.config(["set", "strict", "true"])  # line 851
        except SystemExit as E:  # line 852
            _.assertEqual(0, E.code)  # line 852
        makeRepo()  # line 853
        _.assertTrue(checkRepoFlag("strict", True))  # line 854
        try:  # line 855
            sos.config(["set", "strict", "false"])  # line 855
        except SystemExit as E:  # line 856
            _.assertEqual(0, E.code)  # line 856
        makeRepo()  # line 857
        _.assertTrue(checkRepoFlag("strict", False))  # line 858
        try:  # line 859
            sos.config(["set", "strict", "enable"])  # line 859
        except SystemExit as E:  # line 860
            _.assertEqual(0, E.code)  # line 860
        makeRepo()  # line 861
        _.assertTrue(checkRepoFlag("strict", True))  # line 862
        try:  # line 863
            sos.config(["set", "strict", "disable"])  # line 863
        except SystemExit as E:  # line 864
            _.assertEqual(0, E.code)  # line 864
        makeRepo()  # line 865
        _.assertTrue(checkRepoFlag("strict", False))  # line 866
        try:  # line 867
            sos.config(["set", "strict", "enabled"])  # line 867
        except SystemExit as E:  # line 868
            _.assertEqual(0, E.code)  # line 868
        makeRepo()  # line 869
        _.assertTrue(checkRepoFlag("strict", True))  # line 870
        try:  # line 871
            sos.config(["set", "strict", "disabled"])  # line 871
        except SystemExit as E:  # line 872
            _.assertEqual(0, E.code)  # line 872
        makeRepo()  # line 873
        _.assertTrue(checkRepoFlag("strict", False))  # line 874
        try:  # line 875
            sos.config(["set", "strict", "nope"])  # line 875
            _.fail()  # line 875
        except SystemExit as E:  # line 876
            _.assertEqual(1, E.code)  # line 876

    def testLsSimple(_):  # line 878
        _.createFile(1)  # line 879
        _.createFile("foo")  # line 880
        _.createFile("ign1")  # line 881
        _.createFile("ign2")  # line 882
        _.createFile("bar", prefix="sub")  # line 883
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 884
        try:  # define an ignore pattern  # line 885
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern  # line 885
        except SystemExit as E:  # line 886
            _.assertEqual(0, E.code)  # line 886
        try:  # additional ignore pattern  # line 887
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 887
        except SystemExit as E:  # line 888
            _.assertEqual(0, E.code)  # line 888
        try:  # define a list of ignore patterns  # line 889
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 889
        except SystemExit as E:  # line 890
            _.assertEqual(0, E.code)  # line 890
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # line 891
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 892
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 893
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 894
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 895
        _.assertInAny('    file1', out)  # line 896
        _.assertInAny('    ign1', out)  # line 897
        _.assertInAny('    ign2', out)  # line 898
        _.assertNotIn('DIR sub', out)  # line 899
        _.assertNotIn('    bar', out)  # line 900
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 901
        _.assertIn('DIR sub', out)  # line 902
        _.assertIn('    bar', out)  # line 903
        try:  # line 904
            sos.config(["rm", "foo", "bar"])  # line 904
            _.fail()  # line 904
        except SystemExit as E:  # line 905
            _.assertEqual(1, E.code)  # line 905
        try:  # line 906
            sos.config(["rm", "ignores", "foo"])  # line 906
            _.fail()  # line 906
        except SystemExit as E:  # line 907
            _.assertEqual(1, E.code)  # line 907
        try:  # line 908
            sos.config(["rm", "ignores", "ign1"])  # line 908
        except SystemExit as E:  # line 909
            _.assertEqual(0, E.code)  # line 909
        try:  # remove ignore pattern  # line 910
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 910
        except SystemExit as E:  # line 911
            _.assertEqual(0, E.code)  # line 911
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 912
        _.assertInAny('    ign1', out)  # line 913
        _.assertInAny('IGN ign2', out)  # line 914
        _.assertNotInAny('    ign2', out)  # line 915

    def testWhitelist(_):  # line 917
# TODO test same for simple mode
        _.createFile(1)  # line 919
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 920
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 921
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 922
        sos.commit(options=["--force"])  # attempt to commit the file  # line 923
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 924
        try:  # Exit because dirty  # line 925
            sos.online()  # Exit because dirty  # line 925
            _.fail()  # Exit because dirty  # line 925
        except:  # exception expected  # line 926
            pass  # exception expected  # line 926
        _.createFile("x2")  # add another change  # line 927
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 928
        try:  # force beyond dirty flag check  # line 929
            sos.online(["--force"])  # force beyond dirty flag check  # line 929
            _.fail()  # force beyond dirty flag check  # line 929
        except:  # line 930
            pass  # line 930
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 931
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 932

        _.createFile(1)  # line 934
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 935
        sos.offline("xx", None, ["--track"])  # line 936
        sos.add(".", "./file*")  # line 937
        sos.commit()  # should NOT ask for force here  # line 938
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 939

    def testRemove(_):  # line 941
        _.createFile(1, "x" * 100)  # line 942
        sos.offline("trunk")  # line 943
        try:  # line 944
            sos.destroy("trunk")  # line 944
            _fail()  # line 944
        except:  # line 945
            pass  # line 945
        _.createFile(2, "y" * 10)  # line 946
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 947
        sos.destroy("trunk")  # line 948
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 949
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 950
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 951
        sos.branch("next")  # line 952
        _.createFile(3, "y" * 10)  # make a change  # line 953
        sos.destroy("added", "--force")  # should succeed  # line 954

    def testFastBranchingOnEmptyHistory(_):  # line 956
        ''' Test fast branching without revisions and with them. '''  # line 957
        sos.offline(options=["--strict", "--compress"])  # b0  # line 958
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 959
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 960
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 961
        sos.destroy("2")  # line 962
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 963
        _.assertIn("b0 'trunk' @", out)  # line 964
        _.assertIn("b1         @", out)  # line 965
        _.assertIn("b3         @", out)  # line 966
        _.assertNotIn("b2         @", out)  # line 967
        sos.branch("", "")  # non-fast branching of b4  # line 968
        _.createFile(1)  # line 969
        _.createFile(2)  # line 970
        sos.commit("")  # line 971
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 972
        sos.destroy("4")  # line 973
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 974
        _.assertIn("b0 'trunk' @", out)  # line 975
        _.assertIn("b1         @", out)  # line 976
        _.assertIn("b3         @", out)  # line 977
        _.assertIn("b5         @", out)  # line 978
        _.assertNotIn("b2         @", out)  # line 979
        _.assertNotIn("b4         @", out)  # line 980
# TODO add more files and branch again

    def testUsage(_):  # line 983
        try:  # TODO expect sys.exit(0)  # line 984
            sos.usage()  # TODO expect sys.exit(0)  # line 984
            _.fail()  # TODO expect sys.exit(0)  # line 984
        except:  # line 985
            pass  # line 985
        try:  # TODO expect sys.exit(0)  # line 986
            sos.usage("help")  # TODO expect sys.exit(0)  # line 986
            _.fail()  # TODO expect sys.exit(0)  # line 986
        except:  # line 987
            pass  # line 987
        try:  # TODO expect sys.exit(0)  # line 988
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 988
            _.fail()  # TODO expect sys.exit(0)  # line 988
        except:  # line 989
            pass  # line 989
        try:  # line 990
            sos.usage(version=True)  # line 990
            _.fail()  # line 990
        except:  # line 991
            pass  # line 991
        try:  # line 992
            sos.usage(version=True)  # line 992
            _.fail()  # line 992
        except:  # line 993
            pass  # line 993

    def testOnlyExcept(_):  # line 995
        ''' Test blacklist glob rules. '''  # line 996
        sos.offline(options=["--track"])  # line 997
        _.createFile("a.1")  # line 998
        _.createFile("a.2")  # line 999
        _.createFile("b.1")  # line 1000
        _.createFile("b.2")  # line 1001
        sos.add(".", "./a.?")  # line 1002
        sos.add(".", "./?.1", negative=True)  # line 1003
        out = wrapChannels(lambda _=None: sos.commit())  # line 1004
        _.assertIn("ADD ./a.2", out)  # line 1005
        _.assertNotIn("ADD ./a.1", out)  # line 1006
        _.assertNotIn("ADD ./b.1", out)  # line 1007
        _.assertNotIn("ADD ./b.2", out)  # line 1008

    def testOnly(_):  # line 1010
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 1011
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1012
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1013
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1014
        sos.offline(options=["--track", "--strict"])  # line 1015
        _.createFile(1)  # line 1016
        _.createFile(2)  # line 1017
        sos.add(".", "./file1")  # line 1018
        sos.add(".", "./file2")  # line 1019
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1020
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1021
        sos.commit()  # adds also file2  # line 1022
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1023
        _.createFile(1, "cc")  # modify both files  # line 1024
        _.createFile(2, "dd")  # line 1025
        try:  # line 1026
            sos.config(["set", "texttype", "file2"])  # line 1026
        except SystemExit as E:  # line 1027
            _.assertEqual(0, E.code)  # line 1027
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1028
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1029
        _.assertTrue("./file2" in changes.modifications)  # line 1030
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 1031
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1032
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1033
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # line 1034

    def testDiff(_):  # line 1036
        try:  # manually mark this file as "textual"  # line 1037
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1037
        except SystemExit as E:  # line 1038
            _.assertEqual(0, E.code)  # line 1038
        sos.offline(options=["--strict"])  # line 1039
        _.createFile(1)  # line 1040
        _.createFile(2)  # line 1041
        sos.commit()  # line 1042
        _.createFile(1, "sdfsdgfsdf")  # line 1043
        _.createFile(2, "12343")  # line 1044
        sos.commit()  # line 1045
        _.createFile(1, "foobar")  # line 1046
        _.createFile(3)  # line 1047
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # compare with r1 (second counting from last which is r2)  # line 1048
        _.assertIn("ADD ./file3", out)  # line 1049
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "-~- 0 |xxxxxxxxxx|", "+~+ 0 |foobar|"], out)  # line 1050
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1051

    def testReorderRenameActions(_):  # line 1053
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1054
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1055
        try:  # line 1056
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1056
            _.fail()  # line 1056
        except:  # line 1057
            pass  # line 1057

    def testPublish(_):  # line 1059
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1060

    def testMove(_):  # line 1062
        sos.offline(options=["--strict", "--track"])  # line 1063
        _.createFile(1)  # line 1064
        sos.add(".", "./file?")  # line 1065
# test source folder missing
        try:  # line 1067
            sos.move("sub", "sub/file?", ".", "?file")  # line 1067
            _.fail()  # line 1067
        except:  # line 1068
            pass  # line 1068
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1070
        _.assertTrue(os.path.exists("sub"))  # line 1071
        _.assertTrue(os.path.exists("sub/file1"))  # line 1072
        _.assertFalse(os.path.exists("file1"))  # line 1073
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1075
        _.assertTrue(os.path.exists("1file"))  # line 1076
        _.assertFalse(os.path.exists("sub/file1"))  # line 1077
# test nothing matches source pattern
        try:  # line 1079
            sos.move(".", "a*", ".", "b*")  # line 1079
            _.fail()  # line 1079
        except:  # line 1080
            pass  # line 1080
        sos.add(".", "*")  # anything pattern  # line 1081
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1082
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1082
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1082
        except:  # line 1083
            pass  # line 1083
# test rename no conflict
        _.createFile(1)  # line 1085
        _.createFile(2)  # line 1086
        _.createFile(3)  # line 1087
        sos.add(".", "./file*")  # line 1088
        try:  # define an ignore pattern  # line 1089
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1089
        except SystemExit as E:  # line 1090
            _.assertEqual(0, E.code)  # line 1090
        try:  # line 1091
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1091
        except SystemExit as E:  # line 1092
            _.assertEqual(0, E.code)  # line 1092
        sos.move(".", "./file*", ".", "fi*le")  # line 1093
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1094
        _.assertFalse(os.path.exists("fi4le"))  # line 1095
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1097
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 1101
        sos.add(".", "./?a?b", ["--force"])  # line 1102
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1103
        _.createFile("1a2b")  # should not be tracked  # line 1104
        _.createFile("a1b2")  # should be tracked  # line 1105
        sos.commit()  # line 1106
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 1107
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1108
        _.createFile("1a1b1")  # line 1109
        _.createFile("1a1b2")  # line 1110
        sos.add(".", "?a?b*")  # line 1111
        _.assertIn("not unique", wrapChannels(lambda _=None: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 1112
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1116
        _.createFile(1)  # line 1117
        _.createFile(3)  # line 1118
        _.createFile(5)  # line 1119
        sos.offline()  # branch 0: only file1  # line 1120
        sos.branch()  # line 1121
        os.unlink("file1")  # line 1122
        os.unlink("file3")  # line 1123
        os.unlink("file5")  # line 1124
        _.createFile(2)  # line 1125
        _.createFile(4)  # line 1126
        _.createFile(6)  # line 1127
        sos.commit()  # branch 1: only file2  # line 1128
        sos.switch("0/")  # line 1129
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1130
        _.assertFalse(_.existsFile(1))  # line 1131
        _.assertFalse(_.existsFile(3))  # line 1132
        _.assertFalse(_.existsFile(5))  # line 1133
        _.assertTrue(_.existsFile(2))  # line 1134
        _.assertTrue(_.existsFile(4))  # line 1135
        _.assertTrue(_.existsFile(6))  # line 1136

    def testMoveDetection(_):  # line 1138
        _.createFile(1, "bla")  # line 1139
        sos.offline()  # line 1140
        os.mkdir("sub1")  # line 1141
        os.mkdir("sub2")  # line 1142
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1143
        shutil.move("file1", "sub2")  # line 1144
        out = wrapChannels(lambda _=None: sos.changes())  # line 1145
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1146
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1147
        sos.commit("Moved the file")  # line 1148
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1152

    def testHashCollision(_):  # line 1154
        sos.offline()  # line 1155
        _.createFile(1)  # line 1156
        os.mkdir(sos.revisionFolder(0, 1))  # line 1157
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # line 1158
        _.createFile(1)  # line 1159
        try:  # should exit with error due to collision detection  # line 1160
            sos.commit()  # should exit with error due to collision detection  # line 1160
            _.fail()  # should exit with error due to collision detection  # line 1160
        except SystemExit as E:  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1161
            _.assertEqual(1, E.code)  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1161

    def testFindBase(_):  # line 1163
        old = os.getcwd()  # line 1164
        try:  # line 1165
            os.mkdir("." + os.sep + ".git")  # line 1166
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1167
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1168
            os.chdir("a" + os.sep + "b")  # line 1169
            s, vcs, cmd = sos.findSosVcsBase()  # line 1170
            _.assertIsNotNone(s)  # line 1171
            _.assertIsNotNone(vcs)  # line 1172
            _.assertEqual("git", cmd)  # line 1173
        finally:  # line 1174
            os.chdir(old)  # line 1174

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1185
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1186
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1187
