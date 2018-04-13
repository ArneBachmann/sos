#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xf0c25d66

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
        from typing import *  # line 9
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
        sos.__dict__["verbose"] = True  # required when executing tests manually  # line 102
        sos.Metadata.singleton = None  # line 103
        for entry in os.listdir(testFolder):  # cannot remove testFolder on Windows when using TortoiseSVN as VCS  # line 104
            resource = os.path.join(testFolder, entry)  # line 105
            shutil.rmtree(sos.encode(resource)) if os.path.isdir(sos.encode(resource)) else os.unlink(sos.encode(resource))  # line 106
        os.chdir(testFolder)  # line 107


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
        out = wrapChannels(lambda _=None: sos.commit())  # line 227
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 228
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 229
        _.assertIn("Created new revision r01 (+00/-00/~00/#02)", out)  # TODO why is this not captured?  # line 230

    def testPatternPaths(_):  # line 232
        sos.offline(options=["--track"])  # line 233
        os.mkdir("sub")  # line 234
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 235
        sos.add("sub", "sub/file?")  # line 236
        sos.commit("test")  # should pick up sub/file1 pattern  # line 237
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 238
        _.createFile(1)  # line 239
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 240
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 240
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 240
        except:  # line 241
            pass  # line 241

    def testNoArgs(_):  # line 243
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 244

    def testAutoMetadataUpgrade(_):  # line 246
        sos.offline()  # line 247
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 248
            repo, branches, config = json.load(fd)  # line 248
        repo["version"] = None  # lower than any pip version  # line 249
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 250
        del repo["format"]  # simulate pre-1.3.5  # line 251
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 252
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 252
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # line 253
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 254

    def testFastBranching(_):  # line 256
        _.createFile(1)  # line 257
        sos.offline(options=["--strict"])  # b0/r0 = ./file1  # line 258
        _.createFile(2)  # line 259
        os.unlink("file1")  # line 260
        sos.commit()  # b0/r1 = ./file2  # line 261
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify once --fast becomes the new normal  # line 262
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 263
        _.createFile(3)  # line 264
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 265
        _.assertAllIn([sos.metaFile, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 266
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 267
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 268
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 269
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # revisions were copied to branch 1  # line 270
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # revisions were copied to branch 1  # line 271
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 274
        now = time.time()  # type: float  # line 275
        _.createFile(1)  # line 276
        sync()  # line 277
        sos.offline(options=["--strict"])  # line 278
        _.createFile(1, "abc")  # modify contents  # line 279
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 280
        sync()  # line 281
        out = wrapChannels(lambda _=None: sos.changes())  # line 282
        _.assertAllIn(["<older than last revision>", "<older than previously committed>"], out)  # line 283
        out = wrapChannels(lambda _=None: sos.commit())  # line 284
        _.assertAllIn(["<older than last revision>", "<older than previously committed>"], out)  # line 285

    def testGetParentBranch(_):  # line 287
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}})  # line 288
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 289
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 290
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 291
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 292

    def testTokenizeGlobPattern(_):  # line 294
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 295
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 296
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 297
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 298
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 299
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 300

    def testTokenizeGlobPatterns(_):  # line 302
        try:  # because number of literal strings differs  # line 303
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 303
            _.fail()  # because number of literal strings differs  # line 303
        except:  # line 304
            pass  # line 304
        try:  # because glob patterns differ  # line 305
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 305
            _.fail()  # because glob patterns differ  # line 305
        except:  # line 306
            pass  # line 306
        try:  # glob patterns differ, regardless of position  # line 307
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 307
            _.fail()  # glob patterns differ, regardless of position  # line 307
        except:  # line 308
            pass  # line 308
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 309
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 310
        try:  # succeeds, because glob patterns match (differ only in position)  # line 311
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 311
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 311
        except:  # line 312
            pass  # line 312

    def testConvertGlobFiles(_):  # line 314
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 315
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 316

    def testFolderRemove(_):  # line 318
        m = sos.Metadata(os.getcwd())  # line 319
        _.createFile(1)  # line 320
        _.createFile("a", prefix="sub")  # line 321
        sos.offline()  # line 322
        _.createFile(2)  # line 323
        os.unlink("sub" + os.sep + "a")  # line 324
        os.rmdir("sub")  # line 325
        changes = sos.changes()  # TODO replace by output check  # line 326
        _.assertEqual(1, len(changes.additions))  # line 327
        _.assertEqual(0, len(changes.modifications))  # line 328
        _.assertEqual(1, len(changes.deletions))  # line 329
        _.createFile("a", prefix="sub")  # line 330
        changes = sos.changes()  # line 331
        _.assertEqual(0, len(changes.deletions))  # line 332

    def testSwitchConflict(_):  # line 334
        sos.offline(options=["--strict"])  # (r0)  # line 335
        _.createFile(1)  # line 336
        sos.commit()  # add file (r1)  # line 337
        os.unlink("file1")  # line 338
        sos.commit()  # remove (r2)  # line 339
        _.createFile(1, "something else")  # line 340
        sos.commit()  # (r3)  # line 341
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 342
        _.existsFile(1, "x" * 10)  # line 343
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 344
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 345
        sos.switch("/1")  # add file1 back  # line 346
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 347
        _.existsFile(1, "something else")  # line 348

    def testComputeSequentialPathSet(_):  # line 350
        os.makedirs(sos.revisionFolder(0, 0))  # line 351
        os.makedirs(sos.revisionFolder(0, 1))  # line 352
        os.makedirs(sos.revisionFolder(0, 2))  # line 353
        os.makedirs(sos.revisionFolder(0, 3))  # line 354
        os.makedirs(sos.revisionFolder(0, 4))  # line 355
        m = sos.Metadata(os.getcwd())  # line 356
        m.branch = 0  # line 357
        m.commit = 2  # line 358
        m.saveBranches()  # line 359
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 360
        m.saveCommit(0, 0)  # initial  # line 361
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 362
        m.saveCommit(0, 1)  # mod  # line 363
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 364
        m.saveCommit(0, 2)  # add  # line 365
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 366
        m.saveCommit(0, 3)  # del  # line 367
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 368
        m.saveCommit(0, 4)  # readd  # line 369
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 370
        m.saveBranch(0)  # line 371
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 372
        m.saveBranches()  # line 373
        m.computeSequentialPathSet(0, 4)  # line 374
        _.assertEqual(2, len(m.paths))  # line 375

    def testParseRevisionString(_):  # line 377
        m = sos.Metadata(os.getcwd())  # line 378
        m.branch = 1  # line 379
        m.commits = {0: 0, 1: 1, 2: 2}  # line 380
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 381
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 382
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 383
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 384
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 385
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 386
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 387

    def testOfflineEmpty(_):  # line 389
        os.mkdir("." + os.sep + sos.metaFolder)  # line 390
        try:  # line 391
            sos.offline("trunk")  # line 391
            _.fail()  # line 391
        except SystemExit as E:  # line 392
            _.assertEqual(1, E.code)  # line 392
        os.rmdir("." + os.sep + sos.metaFolder)  # line 393
        sos.offline("test")  # line 394
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 395
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 396
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 397
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 398
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 399
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 400

    def testOfflineWithFiles(_):  # line 402
        _.createFile(1, "x" * 100)  # line 403
        _.createFile(2)  # line 404
        sos.offline("test")  # line 405
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 406
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 407
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 408
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 409
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 410
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 411
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 412

    def testBranch(_):  # line 414
        _.createFile(1, "x" * 100)  # line 415
        _.createFile(2)  # line 416
        sos.offline("test")  # b0/r0  # line 417
        sos.branch("other")  # b1/r0  # line 418
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 419
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 420
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 422
        _.createFile(1, "z")  # modify file  # line 424
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 425
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 426
        _.createFile(3, "z")  # line 428
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 429
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 430
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 435
        _.createFile(1, "x" * 100)  # line 436
        _.createFile(2)  # line 437
        sos.offline("test")  # line 438
        changes = sos.changes()  # line 439
        _.assertEqual(0, len(changes.additions))  # line 440
        _.assertEqual(0, len(changes.deletions))  # line 441
        _.assertEqual(0, len(changes.modifications))  # line 442
        _.createFile(1, "z")  # size change  # line 443
        changes = sos.changes()  # line 444
        _.assertEqual(0, len(changes.additions))  # line 445
        _.assertEqual(0, len(changes.deletions))  # line 446
        _.assertEqual(1, len(changes.modifications))  # line 447
        sos.commit("message")  # line 448
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 449
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 450
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 451
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 452
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 453
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 454
        os.unlink("file2")  # line 455
        changes = sos.changes()  # line 456
        _.assertEqual(0, len(changes.additions))  # line 457
        _.assertEqual(1, len(changes.deletions))  # line 458
        _.assertEqual(1, len(changes.modifications))  # line 459
        sos.commit("modified")  # line 460
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 461
        try:  # expecting Exit due to no changes  # line 462
            sos.commit("nothing")  # expecting Exit due to no changes  # line 462
            _.fail()  # expecting Exit due to no changes  # line 462
        except:  # line 463
            pass  # line 463

    def testGetBranch(_):  # line 465
        m = sos.Metadata(os.getcwd())  # line 466
        m.branch = 1  # current branch  # line 467
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 468
        _.assertEqual(27, m.getBranchByName(27))  # line 469
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 470
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 471
        _.assertIsNone(m.getBranchByName("unknown"))  # line 472
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 473
        _.assertEqual(13, m.getRevisionByName("13"))  # line 474
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 475
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 476

    def testTagging(_):  # line 478
        m = sos.Metadata(os.getcwd())  # line 479
        sos.offline()  # line 480
        _.createFile(111)  # line 481
        sos.commit("tag", ["--tag"])  # line 482
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # line 483
        _.assertTrue(any(("|tag" in line and line.endswith("|TAG") for line in out)))  # line 484
        _.createFile(2)  # line 485
        try:  # line 486
            sos.commit("tag")  # line 486
            _.fail()  # line 486
        except:  # line 487
            pass  # line 487
        sos.commit("tag-2", ["--tag"])  # line 488
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 489
        _.assertIn("TAG tag", out)  # line 490

    def testSwitch(_):  # line 492
        _.createFile(1, "x" * 100)  # line 493
        _.createFile(2, "y")  # line 494
        sos.offline("test")  # file1-2  in initial branch commit  # line 495
        sos.branch("second")  # file1-2  switch, having same files  # line 496
        sos.switch("0")  # no change  switch back, no problem  # line 497
        sos.switch("second")  # no change  # switch back, no problem  # line 498
        _.createFile(3, "y")  # generate a file  # line 499
        try:  # uncommited changes detected  # line 500
            sos.switch("test")  # uncommited changes detected  # line 500
            _.fail()  # uncommited changes detected  # line 500
        except SystemExit as E:  # line 501
            _.assertEqual(1, E.code)  # line 501
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 502
        sos.changes()  # line 503
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 504
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 505
        _.createFile("XXX")  # line 506
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 507
        _.assertIn("File tree has changes", out)  # line 508
        _.assertNotIn("File tree is unchanged", out)  # line 509
        _.assertIn("  * b00   'test'", out)  # line 510
        _.assertIn("    b01 'second'", out)  # line 511
        _.assertIn("(modified)", out)  # one branch has commits  # line 512
        _.assertIn("(in sync)", out)  # the other doesn't  # line 513
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 514
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 515
        _.assertAllIn(["Metadata format", "Content checking:    deactivated", "Data compression:    deactivated", "Repository mode:     simple", "Number of branches:  2"], out)  # line 516
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 517
        _.createFile(4, "xy")  # generate a file  # line 518
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 519
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 520
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 521
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 522
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 523
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 524
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 525
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 526
        _.assertAllIn(["Dumping revisions"], out)  # line 527
        _.assertNotIn("Creating backup", out)  # line 528
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 529
        _.assertIn("Dumping revisions", out)  # line 530
        _.assertNotIn("Creating backup", out)  # line 531
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 532
        _.assertAllIn(["Creating backup"], out)  # line 533
        _.assertIn("Dumping revisions", out)  # line 534

    def testAutoDetectVCS(_):  # line 536
        os.mkdir(".git")  # line 537
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 538
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 539
            meta = fd.read()  # line 539
        _.assertTrue("\"master\"" in meta)  # line 540
        os.rmdir(".git")  # line 541

    def testUpdate(_):  # line 543
        sos.offline("trunk")  # create initial branch b0/r0  # line 544
        _.createFile(1, "x" * 100)  # line 545
        sos.commit("second")  # create b0/r1  # line 546

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 548
        _.assertFalse(_.existsFile(1))  # line 549

        sos.update("/1")  # recreate file1  # line 551
        _.assertTrue(_.existsFile(1))  # line 552

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 554
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 555
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 556
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 557

        sos.update("/1")  # do nothing, as nothing has changed  # line 559
        _.assertTrue(_.existsFile(1))  # line 560

        _.createFile(2, "y" * 100)  # line 562
#    out = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 565
        _.assertTrue(_.existsFile(2))  # line 566
        sos.update("trunk", ["--add"])  # only add stuff  # line 567
        _.assertTrue(_.existsFile(2))  # line 568
        sos.update("trunk")  # nothing to do  # line 569
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 570

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 572
        _.createFile(10, theirs)  # line 573
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 574
        _.createFile(11, mine)  # line 575
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 576
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 577

    def testUpdate2(_):  # line 579
        _.createFile("test.txt", "x" * 10)  # line 580
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 581
        sync()  # line 582
        sos.branch("mod")  # line 583
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 584
        sos.commit("mod")  # create b0/r1  # line 585
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 586
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 587
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 588
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 589
        _.createFile("test.txt", "x" * 10)  # line 590
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 591
        sync()  # line 592
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 593
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 594
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 595
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 596
        sync()  # line 597
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 598
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 599

    def testIsTextType(_):  # line 601
        m = sos.Metadata(".")  # line 602
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 603
        m.c.bintype = ["*.md.confluence"]  # line 604
        _.assertTrue(m.isTextType("ab.txt"))  # line 605
        _.assertTrue(m.isTextType("./ab.txt"))  # line 606
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 607
        _.assertFalse(m.isTextType("bc/ab."))  # line 608
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 609
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 610
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 611
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 612

    def testEolDet(_):  # line 614
        ''' Check correct end-of-line detection. '''  # line 615
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 616
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 617
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 618
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 619
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 620
        _.assertIsNone(sos.eoldet(b""))  # line 621
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 622

    def testMerge(_):  # line 624
        ''' Check merge results depending on user options. '''  # line 625
        a = b"a\nb\ncc\nd"  # type: bytes  # line 626
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 627
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 628
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 629
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 630
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 631
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 632
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 633
        a = b"a\nb\ncc\nd"  # line 634
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 635
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 636
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 637
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 638
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 640
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 641
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 643
        b = b"a\nc\ne"  # line 644
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 645
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 646
        a = b"a\nb\ne"  # intra-line merge  # line 647
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 648
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 649

    def testMergeEol(_):  # line 651
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 652
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 653
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 654
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 655
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 656

    def testPickyMode(_):  # line 658
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 659
        sos.offline("trunk", None, ["--picky"])  # line 660
        changes = sos.changes()  # line 661
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 662
        sos.add(".", "./file?", ["--force"])  # line 663
        _.createFile(1, "aa")  # line 664
        sos.commit("First")  # add one file  # line 665
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 666
        _.createFile(2, "b")  # line 667
        try:  # add nothing, because picky  # line 668
            sos.commit("Second")  # add nothing, because picky  # line 668
        except:  # line 669
            pass  # line 669
        sos.add(".", "./file?")  # line 670
        sos.commit("Third")  # line 671
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 672
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 673
        _.assertIn("    r0", out)  # line 674
        sys.argv.extend(["-n", "2"])  # line 675
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 676
        sys.argv.pop()  # line 677
        sys.argv.pop()  # line 677
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 678
        _.assertIn("    r1", out)  # line 679
        _.assertIn("  * r2", out)  # line 680
        try:  # line 681
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 681
        except SystemExit as E:  # line 682
            _.assertEqual(0, E.code)  # line 682
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 683
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 684
        _.assertNotIn("    r1", out)  # line 685
        _.assertIn("  * r2", out)  # line 686
        _.createFile(3, prefix="sub")  # line 687
        sos.add("sub", "sub/file?")  # line 688
        changes = sos.changes()  # line 689
        _.assertEqual(1, len(changes.additions))  # line 690
        _.assertTrue("sub/file3" in changes.additions)  # line 691

    def testTrackedSubfolder(_):  # line 693
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 694
        os.mkdir("." + os.sep + "sub")  # line 695
        sos.offline("trunk", None, ["--track"])  # line 696
        _.createFile(1, "x")  # line 697
        _.createFile(1, "x", prefix="sub")  # line 698
        sos.add(".", "./file?")  # add glob pattern to track  # line 699
        sos.commit("First")  # line 700
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 701
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 702
        sos.commit("Second")  # one new file + meta  # line 703
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 704
        os.unlink("file1")  # remove from basefolder  # line 705
        _.createFile(2, "y")  # line 706
        sos.remove(".", "sub/file?")  # line 707
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 708
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 708
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 708
        except:  # line 709
            pass  # line 709
        sos.commit("Third")  # line 710
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 711
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 714
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 719
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 720
        _.createFile(1)  # line 721
        _.createFile("a123a")  # untracked file "a123a"  # line 722
        sos.add(".", "./file?")  # add glob tracking pattern  # line 723
        sos.commit("second")  # versions "file1"  # line 724
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 725
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 726
        _.assertIn("  | ./file?", out)  # line 727

        _.createFile(2)  # untracked file "file2"  # line 729
        sos.commit("third")  # versions "file2"  # line 730
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 731

        os.mkdir("." + os.sep + "sub")  # line 733
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 734
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 735
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 736

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 738
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 739
        sos.add(".", "./a*a")  # add tracking pattern  # line 740
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 741
        _.assertEqual(0, len(changes.modifications))  # line 742
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 743
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 744

        sos.commit("Second_2")  # line 746
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 747
        _.existsFile(1, b"x" * 10)  # line 748
        _.existsFile(2, b"x" * 10)  # line 749

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 751
        _.existsFile(1, b"x" * 10)  # line 752
        _.existsFile("a123a", b"x" * 10)  # line 753

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 755
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 756
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 757

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 759
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 760
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 761
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 762
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 763
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 764
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 765
# TODO test switch --meta

    def testLsTracked(_):  # line 768
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 769
        _.createFile(1)  # line 770
        _.createFile("foo")  # line 771
        sos.add(".", "./file*")  # capture one file  # line 772
        sos.ls()  # line 773
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 774
        _.assertInAny("TRK file1  (file*)", out)  # line 775
        _.assertNotInAny("... file1  (file*)", out)  # line 776
        _.assertInAny("    foo", out)  # line 777
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 778
        _.assertInAny("TRK file*", out)  # line 779
        _.createFile("a", prefix="sub")  # line 780
        sos.add("sub", "sub/a")  # line 781
        sos.ls("sub")  # line 782
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 783

    def testLineMerge(_):  # line 785
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 786
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 787
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 788
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 789

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 791
        _.createFile(1)  # line 792
        sos.offline("master", options=["--force"])  # line 793
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # line 794
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 795
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 796
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 797
        _.createFile(2)  # line 798
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 799
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 800
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 801
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 802

    def testLocalConfig(_):  # line 804
        sos.offline("bla", options=[])  # line 805
        try:  # line 806
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 806
        except SystemExit as E:  # line 807
            _.assertEqual(0, E.code)  # line 807
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 808

    def testConfigVariations(_):  # line 810
        def makeRepo():  # line 811
            try:  # line 812
                os.unlink("file1")  # line 812
            except:  # line 813
                pass  # line 813
            sos.offline("master", options=["--force"])  # line 814
            _.createFile(1)  # line 815
            sos.commit("Added file1")  # line 816
        try:  # line 817
            sos.config(["set", "strict", "on"])  # line 817
        except SystemExit as E:  # line 818
            _.assertEqual(0, E.code)  # line 818
        makeRepo()  # line 819
        _.assertTrue(checkRepoFlag("strict", True))  # line 820
        try:  # line 821
            sos.config(["set", "strict", "off"])  # line 821
        except SystemExit as E:  # line 822
            _.assertEqual(0, E.code)  # line 822
        makeRepo()  # line 823
        _.assertTrue(checkRepoFlag("strict", False))  # line 824
        try:  # line 825
            sos.config(["set", "strict", "yes"])  # line 825
        except SystemExit as E:  # line 826
            _.assertEqual(0, E.code)  # line 826
        makeRepo()  # line 827
        _.assertTrue(checkRepoFlag("strict", True))  # line 828
        try:  # line 829
            sos.config(["set", "strict", "no"])  # line 829
        except SystemExit as E:  # line 830
            _.assertEqual(0, E.code)  # line 830
        makeRepo()  # line 831
        _.assertTrue(checkRepoFlag("strict", False))  # line 832
        try:  # line 833
            sos.config(["set", "strict", "1"])  # line 833
        except SystemExit as E:  # line 834
            _.assertEqual(0, E.code)  # line 834
        makeRepo()  # line 835
        _.assertTrue(checkRepoFlag("strict", True))  # line 836
        try:  # line 837
            sos.config(["set", "strict", "0"])  # line 837
        except SystemExit as E:  # line 838
            _.assertEqual(0, E.code)  # line 838
        makeRepo()  # line 839
        _.assertTrue(checkRepoFlag("strict", False))  # line 840
        try:  # line 841
            sos.config(["set", "strict", "true"])  # line 841
        except SystemExit as E:  # line 842
            _.assertEqual(0, E.code)  # line 842
        makeRepo()  # line 843
        _.assertTrue(checkRepoFlag("strict", True))  # line 844
        try:  # line 845
            sos.config(["set", "strict", "false"])  # line 845
        except SystemExit as E:  # line 846
            _.assertEqual(0, E.code)  # line 846
        makeRepo()  # line 847
        _.assertTrue(checkRepoFlag("strict", False))  # line 848
        try:  # line 849
            sos.config(["set", "strict", "enable"])  # line 849
        except SystemExit as E:  # line 850
            _.assertEqual(0, E.code)  # line 850
        makeRepo()  # line 851
        _.assertTrue(checkRepoFlag("strict", True))  # line 852
        try:  # line 853
            sos.config(["set", "strict", "disable"])  # line 853
        except SystemExit as E:  # line 854
            _.assertEqual(0, E.code)  # line 854
        makeRepo()  # line 855
        _.assertTrue(checkRepoFlag("strict", False))  # line 856
        try:  # line 857
            sos.config(["set", "strict", "enabled"])  # line 857
        except SystemExit as E:  # line 858
            _.assertEqual(0, E.code)  # line 858
        makeRepo()  # line 859
        _.assertTrue(checkRepoFlag("strict", True))  # line 860
        try:  # line 861
            sos.config(["set", "strict", "disabled"])  # line 861
        except SystemExit as E:  # line 862
            _.assertEqual(0, E.code)  # line 862
        makeRepo()  # line 863
        _.assertTrue(checkRepoFlag("strict", False))  # line 864
        try:  # line 865
            sos.config(["set", "strict", "nope"])  # line 865
            _.fail()  # line 865
        except SystemExit as E:  # line 866
            _.assertEqual(1, E.code)  # line 866

    def testLsSimple(_):  # line 868
        _.createFile(1)  # line 869
        _.createFile("foo")  # line 870
        _.createFile("ign1")  # line 871
        _.createFile("ign2")  # line 872
        _.createFile("bar", prefix="sub")  # line 873
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 874
        try:  # define an ignore pattern  # line 875
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern  # line 875
        except SystemExit as E:  # line 876
            _.assertEqual(0, E.code)  # line 876
        try:  # additional ignore pattern  # line 877
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 877
        except SystemExit as E:  # line 878
            _.assertEqual(0, E.code)  # line 878
        try:  # define a list of ignore patterns  # line 879
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 879
        except SystemExit as E:  # line 880
            _.assertEqual(0, E.code)  # line 880
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # line 881
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 882
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 883
        _.assertInAny('    file1', out)  # line 884
        _.assertInAny('    ign1', out)  # line 885
        _.assertInAny('    ign2', out)  # line 886
        _.assertNotIn('DIR sub', out)  # line 887
        _.assertNotIn('    bar', out)  # line 888
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 889
        _.assertIn('DIR sub', out)  # line 890
        _.assertIn('    bar', out)  # line 891
        try:  # line 892
            sos.config(["rm", "foo", "bar"])  # line 892
            _.fail()  # line 892
        except SystemExit as E:  # line 893
            _.assertEqual(1, E.code)  # line 893
        try:  # line 894
            sos.config(["rm", "ignores", "foo"])  # line 894
            _.fail()  # line 894
        except SystemExit as E:  # line 895
            _.assertEqual(1, E.code)  # line 895
        try:  # line 896
            sos.config(["rm", "ignores", "ign1"])  # line 896
        except SystemExit as E:  # line 897
            _.assertEqual(0, E.code)  # line 897
        try:  # remove ignore pattern  # line 898
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 898
        except SystemExit as E:  # line 899
            _.assertEqual(0, E.code)  # line 899
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 900
        _.assertInAny('    ign1', out)  # line 901
        _.assertInAny('IGN ign2', out)  # line 902
        _.assertNotInAny('    ign2', out)  # line 903

    def testWhitelist(_):  # line 905
# TODO test same for simple mode
        _.createFile(1)  # line 907
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 908
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 909
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 910
        sos.commit(options=["--force"])  # attempt to commit the file  # line 911
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 912
        try:  # Exit because dirty  # line 913
            sos.online()  # Exit because dirty  # line 913
            _.fail()  # Exit because dirty  # line 913
        except:  # exception expected  # line 914
            pass  # exception expected  # line 914
        _.createFile("x2")  # add another change  # line 915
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 916
        try:  # force beyond dirty flag check  # line 917
            sos.online(["--force"])  # force beyond dirty flag check  # line 917
            _.fail()  # force beyond dirty flag check  # line 917
        except:  # line 918
            pass  # line 918
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 919
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 920

        _.createFile(1)  # line 922
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 923
        sos.offline("xx", None, ["--track"])  # line 924
        sos.add(".", "./file*")  # line 925
        sos.commit()  # should NOT ask for force here  # line 926
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 927

    def testRemove(_):  # line 929
        _.createFile(1, "x" * 100)  # line 930
        sos.offline("trunk")  # line 931
        try:  # line 932
            sos.destroy("trunk")  # line 932
            _fail()  # line 932
        except:  # line 933
            pass  # line 933
        _.createFile(2, "y" * 10)  # line 934
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 935
        sos.destroy("trunk")  # line 936
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 937
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 938
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 939
        sos.branch("next")  # line 940
        _.createFile(3, "y" * 10)  # make a change  # line 941
        sos.destroy("added", "--force")  # should succeed  # line 942

    def testUsage(_):  # line 944
        try:  # TODO expect sys.exit(0)  # line 945
            sos.usage()  # TODO expect sys.exit(0)  # line 945
            _.fail()  # TODO expect sys.exit(0)  # line 945
        except:  # line 946
            pass  # line 946
        try:  # TODO expect sys.exit(0)  # line 947
            sos.usage("help")  # TODO expect sys.exit(0)  # line 947
            _.fail()  # TODO expect sys.exit(0)  # line 947
        except:  # line 948
            pass  # line 948
        try:  # TODO expect sys.exit(0)  # line 949
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 949
            _.fail()  # TODO expect sys.exit(0)  # line 949
        except:  # line 950
            pass  # line 950
        try:  # line 951
            sos.usage(version=True)  # line 951
            _.fail()  # line 951
        except:  # line 952
            pass  # line 952
        try:  # line 953
            sos.usage(version=True)  # line 953
            _.fail()  # line 953
        except:  # line 954
            pass  # line 954

    def testOnlyExcept(_):  # line 956
        ''' Test blacklist glob rules. '''  # line 957
        sos.offline(options=["--track"])  # line 958
        _.createFile("a.1")  # line 959
        _.createFile("a.2")  # line 960
        _.createFile("b.1")  # line 961
        _.createFile("b.2")  # line 962
        sos.add(".", "./a.?")  # line 963
        sos.add(".", "./?.1", negative=True)  # line 964
        out = wrapChannels(lambda _=None: sos.commit())  # line 965
        _.assertIn("ADD ./a.2", out)  # line 966
        _.assertNotIn("ADD ./a.1", out)  # line 967
        _.assertNotIn("ADD ./b.1", out)  # line 968
        _.assertNotIn("ADD ./b.2", out)  # line 969

    def testOnly(_):  # line 971
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 972
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 973
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 974
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 975
        sos.offline(options=["--track", "--strict"])  # line 976
        _.createFile(1)  # line 977
        _.createFile(2)  # line 978
        sos.add(".", "./file1")  # line 979
        sos.add(".", "./file2")  # line 980
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 981
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 982
        sos.commit()  # adds also file2  # line 983
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 984
        _.createFile(1, "cc")  # modify both files  # line 985
        _.createFile(2, "dd")  # line 986
        try:  # line 987
            sos.config(["set", "texttype", "file2"])  # line 987
        except SystemExit as E:  # line 988
            _.assertEqual(0, E.code)  # line 988
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 989
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 990
        _.assertTrue("./file2" in changes.modifications)  # line 991
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 992
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 993
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 994
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # line 995

    def testDiff(_):  # line 997
        try:  # manually mark this file as "textual"  # line 998
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 998
        except SystemExit as E:  # line 999
            _.assertEqual(0, E.code)  # line 999
        sos.offline(options=["--strict"])  # line 1000
        _.createFile(1)  # line 1001
        _.createFile(2)  # line 1002
        sos.commit()  # line 1003
        _.createFile(1, "sdfsdgfsdf")  # line 1004
        _.createFile(2, "12343")  # line 1005
        sos.commit()  # line 1006
        _.createFile(1, "foobar")  # line 1007
        _.createFile(3)  # line 1008
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # compare with r1 (second counting from last which is r2)  # line 1009
        _.assertIn("ADD ./file3", out)  # line 1010
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "- | 0 |xxxxxxxxxx|", "+ | 0 |foobar|"], out)  # line 1011
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1012

    def testReorderRenameActions(_):  # line 1014
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1015
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1016
        try:  # line 1017
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1017
            _.fail()  # line 1017
        except:  # line 1018
            pass  # line 1018

    def testMove(_):  # line 1020
        sos.offline(options=["--strict", "--track"])  # line 1021
        _.createFile(1)  # line 1022
        sos.add(".", "./file?")  # line 1023
# test source folder missing
        try:  # line 1025
            sos.move("sub", "sub/file?", ".", "?file")  # line 1025
            _.fail()  # line 1025
        except:  # line 1026
            pass  # line 1026
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1028
        _.assertTrue(os.path.exists("sub"))  # line 1029
        _.assertTrue(os.path.exists("sub/file1"))  # line 1030
        _.assertFalse(os.path.exists("file1"))  # line 1031
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1033
        _.assertTrue(os.path.exists("1file"))  # line 1034
        _.assertFalse(os.path.exists("sub/file1"))  # line 1035
# test nothing matches source pattern
        try:  # line 1037
            sos.move(".", "a*", ".", "b*")  # line 1037
            _.fail()  # line 1037
        except:  # line 1038
            pass  # line 1038
        sos.add(".", "*")  # anything pattern  # line 1039
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1040
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1040
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1040
        except:  # line 1041
            pass  # line 1041
# test rename no conflict
        _.createFile(1)  # line 1043
        _.createFile(2)  # line 1044
        _.createFile(3)  # line 1045
        sos.add(".", "./file*")  # line 1046
        try:  # define an ignore pattern  # line 1047
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1047
        except SystemExit as E:  # line 1048
            _.assertEqual(0, E.code)  # line 1048
        try:  # line 1049
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1049
        except SystemExit as E:  # line 1050
            _.assertEqual(0, E.code)  # line 1050
        sos.move(".", "./file*", ".", "fi*le")  # line 1051
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1052
        _.assertFalse(os.path.exists("fi4le"))  # line 1053
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1055
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 1059
        sos.add(".", "./?a?b", ["--force"])  # line 1060
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1061
        _.createFile("1a2b")  # should not be tracked  # line 1062
        _.createFile("a1b2")  # should be tracked  # line 1063
        sos.commit()  # line 1064
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 1065
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1066
        _.createFile("1a1b1")  # line 1067
        _.createFile("1a1b2")  # line 1068
        sos.add(".", "?a?b*")  # line 1069
        _.assertIn("not unique", wrapChannels(lambda _=None: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 1070
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1074
        _.createFile(1)  # line 1075
        _.createFile(3)  # line 1076
        _.createFile(5)  # line 1077
        sos.offline()  # branch 0: only file1  # line 1078
        sos.branch()  # line 1079
        os.unlink("file1")  # line 1080
        os.unlink("file3")  # line 1081
        os.unlink("file5")  # line 1082
        _.createFile(2)  # line 1083
        _.createFile(4)  # line 1084
        _.createFile(6)  # line 1085
        sos.commit()  # branch 1: only file2  # line 1086
        sos.switch("0/")  # line 1087
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1088
        _.assertFalse(_.existsFile(1))  # line 1089
        _.assertFalse(_.existsFile(3))  # line 1090
        _.assertFalse(_.existsFile(5))  # line 1091
        _.assertTrue(_.existsFile(2))  # line 1092
        _.assertTrue(_.existsFile(4))  # line 1093
        _.assertTrue(_.existsFile(6))  # line 1094

    def testHashCollision(_):  # line 1096
        sos.offline()  # line 1097
        _.createFile(1)  # line 1098
        os.mkdir(sos.revisionFolder(0, 1))  # line 1099
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # line 1100
        _.createFile(1)  # line 1101
        try:  # should exit with error due to collision detection  # line 1102
            sos.commit()  # should exit with error due to collision detection  # line 1102
            _.fail()  # should exit with error due to collision detection  # line 1102
        except SystemExit as E:  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1103
            _.assertEqual(1, E.code)  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1103

    def testFindBase(_):  # line 1105
        old = os.getcwd()  # line 1106
        try:  # line 1107
            os.mkdir("." + os.sep + ".git")  # line 1108
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1109
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1110
            os.chdir("a" + os.sep + "b")  # line 1111
            s, vcs, cmd = sos.findSosVcsBase()  # line 1112
            _.assertIsNotNone(s)  # line 1113
            _.assertIsNotNone(vcs)  # line 1114
            _.assertEqual("git", cmd)  # line 1115
        finally:  # line 1116
            os.chdir(old)  # line 1116

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise

if __name__ == '__main__':  # line 1126
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1127
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1128
