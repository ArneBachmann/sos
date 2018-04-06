#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xea071639

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

    def testFitStrings(_):  # line 200
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 201
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 202
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 203
    def testMoves(_):  # line 204
        _.createFile(1, "1")  # line 205
        _.createFile(2, "2", "sub")  # line 206
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 207
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 208
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 209
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 210
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 211
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 212
        out = wrapChannels(lambda _=None: sos.commit())  # line 213
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 214
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 215
        _.assertIn("Created new revision r01 (+00/-00/~00/#02)", out)  # TODO why is this not captured?  # line 216

    def testPatternPaths(_):  # line 218
        sos.offline(options=["--track"])  # line 219
        os.mkdir("sub")  # line 220
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 221
        sos.add("sub", "sub/file?")  # line 222
        sos.commit("test")  # should pick up sub/file1 pattern  # line 223
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 224
        _.createFile(1)  # line 225
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 226
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 226
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 226
        except:  # line 227
            pass  # line 227

    def testNoArgs(_):  # line 229
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 230

    def testAutoMetadataUpgrade(_):  # line 232
        sos.offline()  # line 233
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 234
            repo, branches, config = json.load(fd)  # line 234
        repo["version"] = None  # lower than any pip version  # line 235
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 236
        del repo["format"]  # simulate pre-1.3.5  # line 237
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 238
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 238
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # line 239
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 240

    def testFastBranching(_):  # line 242
        _.createFile(1)  # line 243
        sos.offline(options=["--strict"])  # b0/r0 = ./file1  # line 244
        _.createFile(2)  # line 245
        os.unlink("file1")  # line 246
        sos.commit()  # b0/r1 = ./file2  # line 247
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify once --fast becomes the new normal  # line 248
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 249
        _.createFile(3)  # line 250
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 251
        _.assertAllIn([sos.metaFile, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 252
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 253
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 254
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 255
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # revisions were copied to branch 1  # line 256
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # revisions were copied to branch 1  # line 257
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 260
        now = time.time()  # type: float  # line 261
        _.createFile(1)  # line 262
        sync()  # line 263
        sos.offline(options=["--strict"])  # line 264
        _.createFile(1, "abc")  # modify contents  # line 265
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 266
        sync()  # line 267
        out = wrapChannels(lambda _=None: sos.changes())  # line 268
        _.assertAllIn(["<older than last revision>", "<older than previously committed>"], out)  # line 269
        out = wrapChannels(lambda _=None: sos.commit())  # line 270
        _.assertAllIn(["<older than last revision>", "<older than previously committed>"], out)  # line 271

    def testGetParentBranch(_):  # line 273
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}})  # line 274
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 275
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 276
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 277
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 278

    def testTokenizeGlobPattern(_):  # line 280
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 281
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 282
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 283
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 284
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 285
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 286

    def testTokenizeGlobPatterns(_):  # line 288
        try:  # because number of literal strings differs  # line 289
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 289
            _.fail()  # because number of literal strings differs  # line 289
        except:  # line 290
            pass  # line 290
        try:  # because glob patterns differ  # line 291
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 291
            _.fail()  # because glob patterns differ  # line 291
        except:  # line 292
            pass  # line 292
        try:  # glob patterns differ, regardless of position  # line 293
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 293
            _.fail()  # glob patterns differ, regardless of position  # line 293
        except:  # line 294
            pass  # line 294
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 295
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 296
        try:  # succeeds, because glob patterns match (differ only in position)  # line 297
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 297
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 297
        except:  # line 298
            pass  # line 298

    def testConvertGlobFiles(_):  # line 300
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 301
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 302

    def testFolderRemove(_):  # line 304
        m = sos.Metadata(os.getcwd())  # line 305
        _.createFile(1)  # line 306
        _.createFile("a", prefix="sub")  # line 307
        sos.offline()  # line 308
        _.createFile(2)  # line 309
        os.unlink("sub" + os.sep + "a")  # line 310
        os.rmdir("sub")  # line 311
        changes = sos.changes()  # TODO replace by output check  # line 312
        _.assertEqual(1, len(changes.additions))  # line 313
        _.assertEqual(0, len(changes.modifications))  # line 314
        _.assertEqual(1, len(changes.deletions))  # line 315
        _.createFile("a", prefix="sub")  # line 316
        changes = sos.changes()  # line 317
        _.assertEqual(0, len(changes.deletions))  # line 318

    def testSwitchConflict(_):  # line 320
        sos.offline(options=["--strict"])  # (r0)  # line 321
        _.createFile(1)  # line 322
        sos.commit()  # add file (r1)  # line 323
        os.unlink("file1")  # line 324
        sos.commit()  # remove (r2)  # line 325
        _.createFile(1, "something else")  # line 326
        sos.commit()  # (r3)  # line 327
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 328
        _.existsFile(1, "x" * 10)  # line 329
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 330
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 331
        sos.switch("/1")  # add file1 back  # line 332
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 333
        _.existsFile(1, "something else")  # line 334

    def testComputeSequentialPathSet(_):  # line 336
        os.makedirs(sos.revisionFolder(0, 0))  # line 337
        os.makedirs(sos.revisionFolder(0, 1))  # line 338
        os.makedirs(sos.revisionFolder(0, 2))  # line 339
        os.makedirs(sos.revisionFolder(0, 3))  # line 340
        os.makedirs(sos.revisionFolder(0, 4))  # line 341
        m = sos.Metadata(os.getcwd())  # line 342
        m.branch = 0  # line 343
        m.commit = 2  # line 344
        m.saveBranches()  # line 345
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 346
        m.saveCommit(0, 0)  # initial  # line 347
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 348
        m.saveCommit(0, 1)  # mod  # line 349
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 350
        m.saveCommit(0, 2)  # add  # line 351
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 352
        m.saveCommit(0, 3)  # del  # line 353
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 354
        m.saveCommit(0, 4)  # readd  # line 355
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 356
        m.saveBranch(0)  # line 357
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 358
        m.saveBranches()  # line 359
        m.computeSequentialPathSet(0, 4)  # line 360
        _.assertEqual(2, len(m.paths))  # line 361

    def testParseRevisionString(_):  # line 363
        m = sos.Metadata(os.getcwd())  # line 364
        m.branch = 1  # line 365
        m.commits = {0: 0, 1: 1, 2: 2}  # line 366
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 367
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 368
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 369
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 370
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 371
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 372
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 373

    def testOfflineEmpty(_):  # line 375
        os.mkdir("." + os.sep + sos.metaFolder)  # line 376
        try:  # line 377
            sos.offline("trunk")  # line 377
            _.fail()  # line 377
        except SystemExit as E:  # line 378
            _.assertEqual(1, E.code)  # line 378
        os.rmdir("." + os.sep + sos.metaFolder)  # line 379
        sos.offline("test")  # line 380
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 381
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 382
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 383
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 384
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 385
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 386

    def testOfflineWithFiles(_):  # line 388
        _.createFile(1, "x" * 100)  # line 389
        _.createFile(2)  # line 390
        sos.offline("test")  # line 391
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 392
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 393
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 394
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 395
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 396
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 397
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 398

    def testBranch(_):  # line 400
        _.createFile(1, "x" * 100)  # line 401
        _.createFile(2)  # line 402
        sos.offline("test")  # b0/r0  # line 403
        sos.branch("other")  # b1/r0  # line 404
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 405
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 406
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 408
        _.createFile(1, "z")  # modify file  # line 410
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 411
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 412
        _.createFile(3, "z")  # line 414
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 415
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 416
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 421
        _.createFile(1, "x" * 100)  # line 422
        _.createFile(2)  # line 423
        sos.offline("test")  # line 424
        changes = sos.changes()  # line 425
        _.assertEqual(0, len(changes.additions))  # line 426
        _.assertEqual(0, len(changes.deletions))  # line 427
        _.assertEqual(0, len(changes.modifications))  # line 428
        _.createFile(1, "z")  # size change  # line 429
        changes = sos.changes()  # line 430
        _.assertEqual(0, len(changes.additions))  # line 431
        _.assertEqual(0, len(changes.deletions))  # line 432
        _.assertEqual(1, len(changes.modifications))  # line 433
        sos.commit("message")  # line 434
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 435
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 436
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 437
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 438
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 439
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 440
        os.unlink("file2")  # line 441
        changes = sos.changes()  # line 442
        _.assertEqual(0, len(changes.additions))  # line 443
        _.assertEqual(1, len(changes.deletions))  # line 444
        _.assertEqual(1, len(changes.modifications))  # line 445
        sos.commit("modified")  # line 446
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 447
        try:  # expecting Exit due to no changes  # line 448
            sos.commit("nothing")  # expecting Exit due to no changes  # line 448
            _.fail()  # expecting Exit due to no changes  # line 448
        except:  # line 449
            pass  # line 449

    def testGetBranch(_):  # line 451
        m = sos.Metadata(os.getcwd())  # line 452
        m.branch = 1  # current branch  # line 453
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 454
        _.assertEqual(27, m.getBranchByName(27))  # line 455
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 456
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 457
        _.assertIsNone(m.getBranchByName("unknown"))  # line 458
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 459
        _.assertEqual(13, m.getRevisionByName("13"))  # line 460
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 461
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 462

    def testTagging(_):  # line 464
        m = sos.Metadata(os.getcwd())  # line 465
        sos.offline()  # line 466
        _.createFile(111)  # line 467
        sos.commit("tag", ["--tag"])  # line 468
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # line 469
        _.assertTrue(any(("|tag" in line and line.endswith("|TAG") for line in out)))  # line 470
        _.createFile(2)  # line 471
        try:  # line 472
            sos.commit("tag")  # line 472
            _.fail()  # line 472
        except:  # line 473
            pass  # line 473
        sos.commit("tag-2", ["--tag"])  # line 474
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 475
        _.assertIn("TAG tag", out)  # line 476

    def testSwitch(_):  # line 478
        _.createFile(1, "x" * 100)  # line 479
        _.createFile(2, "y")  # line 480
        sos.offline("test")  # file1-2  in initial branch commit  # line 481
        sos.branch("second")  # file1-2  switch, having same files  # line 482
        sos.switch("0")  # no change  switch back, no problem  # line 483
        sos.switch("second")  # no change  # switch back, no problem  # line 484
        _.createFile(3, "y")  # generate a file  # line 485
        try:  # uncommited changes detected  # line 486
            sos.switch("test")  # uncommited changes detected  # line 486
            _.fail()  # uncommited changes detected  # line 486
        except SystemExit as E:  # line 487
            _.assertEqual(1, E.code)  # line 487
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 488
        sos.changes()  # line 489
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 490
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 491
        _.createFile("XXX")  # line 492
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 493
        _.assertIn("File tree has changes", out)  # line 494
        _.assertNotIn("File tree is unchanged", out)  # line 495
        _.assertIn("  * b00   'test'", out)  # line 496
        _.assertIn("    b01 'second'", out)  # line 497
        _.assertIn("(dirty)", out)  # one branch has commits  # line 498
        _.assertIn("(in sync)", out)  # the other doesn't  # line 499
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 500
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 501
        _.assertAllIn(["Metadata format", "Content checking:    deactivated", "Data compression:    deactivated", "Repository mode:     simple", "Number of branches:  2"], out)  # line 502
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 503
        _.createFile(4, "xy")  # generate a file  # line 504
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 505
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 506
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 507
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 508
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 509
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 510
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 511
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 512
        _.assertAllIn(["Dumping revisions"], out)  # line 513
        _.assertNotIn("Creating backup", out)  # line 514
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 515
        _.assertIn("Dumping revisions", out)  # line 516
        _.assertNotIn("Creating backup", out)  # line 517
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 518
        _.assertAllIn(["Creating backup"], out)  # line 519
        _.assertIn("Dumping revisions", out)  # line 520

    def testAutoDetectVCS(_):  # line 522
        os.mkdir(".git")  # line 523
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 524
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 525
            meta = fd.read()  # line 525
        _.assertTrue("\"master\"" in meta)  # line 526
        os.rmdir(".git")  # line 527

    def testUpdate(_):  # line 529
        sos.offline("trunk")  # create initial branch b0/r0  # line 530
        _.createFile(1, "x" * 100)  # line 531
        sos.commit("second")  # create b0/r1  # line 532

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 534
        _.assertFalse(_.existsFile(1))  # line 535

        sos.update("/1")  # recreate file1  # line 537
        _.assertTrue(_.existsFile(1))  # line 538

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 540
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 541
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 542
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 543

        sos.update("/1")  # do nothing, as nothing has changed  # line 545
        _.assertTrue(_.existsFile(1))  # line 546

        _.createFile(2, "y" * 100)  # line 548
#    out = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 551
        _.assertTrue(_.existsFile(2))  # line 552
        sos.update("trunk", ["--add"])  # only add stuff  # line 553
        _.assertTrue(_.existsFile(2))  # line 554
        sos.update("trunk")  # nothing to do  # line 555
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 556

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 558
        _.createFile(10, theirs)  # line 559
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 560
        _.createFile(11, mine)  # line 561
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 562
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 563

    def testUpdate2(_):  # line 565
        _.createFile("test.txt", "x" * 10)  # line 566
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 567
        sync()  # line 568
        sos.branch("mod")  # line 569
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 570
        sos.commit("mod")  # create b0/r1  # line 571
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 572
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 573
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 574
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 575
        _.createFile("test.txt", "x" * 10)  # line 576
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 577
        sync()  # line 578
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 579
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 580
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 581
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 582
        sync()  # line 583
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 584
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 585

    def testIsTextType(_):  # line 587
        m = sos.Metadata(".")  # line 588
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 589
        m.c.bintype = ["*.md.confluence"]  # line 590
        _.assertTrue(m.isTextType("ab.txt"))  # line 591
        _.assertTrue(m.isTextType("./ab.txt"))  # line 592
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 593
        _.assertFalse(m.isTextType("bc/ab."))  # line 594
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 595
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 596
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 597
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 598

    def testEolDet(_):  # line 600
        ''' Check correct end-of-line detection. '''  # line 601
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 602
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 603
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 604
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 605
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 606
        _.assertIsNone(sos.eoldet(b""))  # line 607
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 608

    def testMerge(_):  # line 610
        ''' Check merge results depending on user options. '''  # line 611
        a = b"a\nb\ncc\nd"  # type: bytes  # line 612
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 613
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 614
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 615
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 616
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 617
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 618
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 619
        a = b"a\nb\ncc\nd"  # line 620
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 621
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 622
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 623
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 624
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 626
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 627
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 629
        b = b"a\nc\ne"  # line 630
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 631
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 632
        a = b"a\nb\ne"  # intra-line merge  # line 633
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 634
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 635

    def testMergeEol(_):  # line 637
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 638
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 639
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 640
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 641
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 642

    def testPickyMode(_):  # line 644
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 645
        sos.offline("trunk", None, ["--picky"])  # line 646
        changes = sos.changes()  # line 647
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 648
        sos.add(".", "./file?", ["--force"])  # line 649
        _.createFile(1, "aa")  # line 650
        sos.commit("First")  # add one file  # line 651
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 652
        _.createFile(2, "b")  # line 653
        try:  # add nothing, because picky  # line 654
            sos.commit("Second")  # add nothing, because picky  # line 654
        except:  # line 655
            pass  # line 655
        sos.add(".", "./file?")  # line 656
        sos.commit("Third")  # line 657
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 658
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 659
        _.assertIn("    r0", out)  # because number of log lines was limited  # line 660
        _.assertIn("    r1", out)  # line 661
        _.assertIn("  * r2", out)  # line 662
        try:  # line 663
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 663
        except SystemExit as E:  # line 664
            _.assertEqual(0, E.code)  # line 664
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 665
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 666
        _.assertNotIn("    r1", out)  # line 667
        _.assertIn("  * r2", out)  # line 668
        _.createFile(3, prefix="sub")  # line 669
        sos.add("sub", "sub/file?")  # line 670
        changes = sos.changes()  # line 671
        _.assertEqual(1, len(changes.additions))  # line 672
        _.assertTrue("sub/file3" in changes.additions)  # line 673

    def testTrackedSubfolder(_):  # line 675
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 676
        os.mkdir("." + os.sep + "sub")  # line 677
        sos.offline("trunk", None, ["--track"])  # line 678
        _.createFile(1, "x")  # line 679
        _.createFile(1, "x", prefix="sub")  # line 680
        sos.add(".", "./file?")  # add glob pattern to track  # line 681
        sos.commit("First")  # line 682
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 683
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 684
        sos.commit("Second")  # one new file + meta  # line 685
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 686
        os.unlink("file1")  # remove from basefolder  # line 687
        _.createFile(2, "y")  # line 688
        sos.remove(".", "sub/file?")  # line 689
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 690
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 690
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 690
        except:  # line 691
            pass  # line 691
        sos.commit("Third")  # line 692
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 693
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 696
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 701
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 702
        _.createFile(1)  # line 703
        _.createFile("a123a")  # untracked file "a123a"  # line 704
        sos.add(".", "./file?")  # add glob tracking pattern  # line 705
        sos.commit("second")  # versions "file1"  # line 706
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 707
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 708
        _.assertIn("  | ./file?", out)  # line 709

        _.createFile(2)  # untracked file "file2"  # line 711
        sos.commit("third")  # versions "file2"  # line 712
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 713

        os.mkdir("." + os.sep + "sub")  # line 715
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 716
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 717
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 718

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 720
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 721
        sos.add(".", "./a*a")  # add tracking pattern  # line 722
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 723
        _.assertEqual(0, len(changes.modifications))  # line 724
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 725
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 726

        sos.commit("Second_2")  # line 728
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 729
        _.existsFile(1, b"x" * 10)  # line 730
        _.existsFile(2, b"x" * 10)  # line 731

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 733
        _.existsFile(1, b"x" * 10)  # line 734
        _.existsFile("a123a", b"x" * 10)  # line 735

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 737
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 738
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 739

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 741
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 742
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 743
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 744
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 745
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 746
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 747
# TODO test switch --meta

    def testLsTracked(_):  # line 750
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 751
        _.createFile(1)  # line 752
        _.createFile("foo")  # line 753
        sos.add(".", "./file*")  # capture one file  # line 754
        sos.ls()  # line 755
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 756
        _.assertInAny("TRK file1  (file*)", out)  # line 757
        _.assertNotInAny("... file1  (file*)", out)  # line 758
        _.assertInAny("    foo", out)  # line 759
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 760
        _.assertInAny("TRK file*", out)  # line 761
        _.createFile("a", prefix="sub")  # line 762
        sos.add("sub", "sub/a")  # line 763
        sos.ls("sub")  # line 764
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 765

    def testLineMerge(_):  # line 767
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 768
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 769
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 770
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 771

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 773
        _.createFile(1)  # line 774
        sos.offline("master", options=["--force"])  # line 775
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # line 776
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 777
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 778
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 779
        _.createFile(2)  # line 780
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 781
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 782
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 783
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 784

    def testLocalConfig(_):  # line 786
        sos.offline("bla", options=[])  # line 787
        try:  # line 788
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 788
        except SystemExit as E:  # line 789
            _.assertEqual(0, E.code)  # line 789
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 790

    def testConfigVariations(_):  # line 792
        def makeRepo():  # line 793
            try:  # line 794
                os.unlink("file1")  # line 794
            except:  # line 795
                pass  # line 795
            sos.offline("master", options=["--force"])  # line 796
            _.createFile(1)  # line 797
            sos.commit("Added file1")  # line 798
        try:  # line 799
            sos.config(["set", "strict", "on"])  # line 799
        except SystemExit as E:  # line 800
            _.assertEqual(0, E.code)  # line 800
        makeRepo()  # line 801
        _.assertTrue(checkRepoFlag("strict", True))  # line 802
        try:  # line 803
            sos.config(["set", "strict", "off"])  # line 803
        except SystemExit as E:  # line 804
            _.assertEqual(0, E.code)  # line 804
        makeRepo()  # line 805
        _.assertTrue(checkRepoFlag("strict", False))  # line 806
        try:  # line 807
            sos.config(["set", "strict", "yes"])  # line 807
        except SystemExit as E:  # line 808
            _.assertEqual(0, E.code)  # line 808
        makeRepo()  # line 809
        _.assertTrue(checkRepoFlag("strict", True))  # line 810
        try:  # line 811
            sos.config(["set", "strict", "no"])  # line 811
        except SystemExit as E:  # line 812
            _.assertEqual(0, E.code)  # line 812
        makeRepo()  # line 813
        _.assertTrue(checkRepoFlag("strict", False))  # line 814
        try:  # line 815
            sos.config(["set", "strict", "1"])  # line 815
        except SystemExit as E:  # line 816
            _.assertEqual(0, E.code)  # line 816
        makeRepo()  # line 817
        _.assertTrue(checkRepoFlag("strict", True))  # line 818
        try:  # line 819
            sos.config(["set", "strict", "0"])  # line 819
        except SystemExit as E:  # line 820
            _.assertEqual(0, E.code)  # line 820
        makeRepo()  # line 821
        _.assertTrue(checkRepoFlag("strict", False))  # line 822
        try:  # line 823
            sos.config(["set", "strict", "true"])  # line 823
        except SystemExit as E:  # line 824
            _.assertEqual(0, E.code)  # line 824
        makeRepo()  # line 825
        _.assertTrue(checkRepoFlag("strict", True))  # line 826
        try:  # line 827
            sos.config(["set", "strict", "false"])  # line 827
        except SystemExit as E:  # line 828
            _.assertEqual(0, E.code)  # line 828
        makeRepo()  # line 829
        _.assertTrue(checkRepoFlag("strict", False))  # line 830
        try:  # line 831
            sos.config(["set", "strict", "enable"])  # line 831
        except SystemExit as E:  # line 832
            _.assertEqual(0, E.code)  # line 832
        makeRepo()  # line 833
        _.assertTrue(checkRepoFlag("strict", True))  # line 834
        try:  # line 835
            sos.config(["set", "strict", "disable"])  # line 835
        except SystemExit as E:  # line 836
            _.assertEqual(0, E.code)  # line 836
        makeRepo()  # line 837
        _.assertTrue(checkRepoFlag("strict", False))  # line 838
        try:  # line 839
            sos.config(["set", "strict", "enabled"])  # line 839
        except SystemExit as E:  # line 840
            _.assertEqual(0, E.code)  # line 840
        makeRepo()  # line 841
        _.assertTrue(checkRepoFlag("strict", True))  # line 842
        try:  # line 843
            sos.config(["set", "strict", "disabled"])  # line 843
        except SystemExit as E:  # line 844
            _.assertEqual(0, E.code)  # line 844
        makeRepo()  # line 845
        _.assertTrue(checkRepoFlag("strict", False))  # line 846
        try:  # line 847
            sos.config(["set", "strict", "nope"])  # line 847
            _.fail()  # line 847
        except SystemExit as E:  # line 848
            _.assertEqual(1, E.code)  # line 848

    def testLsSimple(_):  # line 850
        _.createFile(1)  # line 851
        _.createFile("foo")  # line 852
        _.createFile("ign1")  # line 853
        _.createFile("ign2")  # line 854
        _.createFile("bar", prefix="sub")  # line 855
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 856
        try:  # define an ignore pattern  # line 857
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern  # line 857
        except SystemExit as E:  # line 858
            _.assertEqual(0, E.code)  # line 858
        try:  # additional ignore pattern  # line 859
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 859
        except SystemExit as E:  # line 860
            _.assertEqual(0, E.code)  # line 860
        try:  # define a list of ignore patterns  # line 861
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 861
        except SystemExit as E:  # line 862
            _.assertEqual(0, E.code)  # line 862
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # line 863
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 864
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 865
        _.assertInAny('    file1', out)  # line 866
        _.assertInAny('    ign1', out)  # line 867
        _.assertInAny('    ign2', out)  # line 868
        _.assertNotIn('DIR sub', out)  # line 869
        _.assertNotIn('    bar', out)  # line 870
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 871
        _.assertIn('DIR sub', out)  # line 872
        _.assertIn('    bar', out)  # line 873
        try:  # line 874
            sos.config(["rm", "foo", "bar"])  # line 874
            _.fail()  # line 874
        except SystemExit as E:  # line 875
            _.assertEqual(1, E.code)  # line 875
        try:  # line 876
            sos.config(["rm", "ignores", "foo"])  # line 876
            _.fail()  # line 876
        except SystemExit as E:  # line 877
            _.assertEqual(1, E.code)  # line 877
        try:  # line 878
            sos.config(["rm", "ignores", "ign1"])  # line 878
        except SystemExit as E:  # line 879
            _.assertEqual(0, E.code)  # line 879
        try:  # remove ignore pattern  # line 880
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 880
        except SystemExit as E:  # line 881
            _.assertEqual(0, E.code)  # line 881
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 882
        _.assertInAny('    ign1', out)  # line 883
        _.assertInAny('IGN ign2', out)  # line 884
        _.assertNotInAny('    ign2', out)  # line 885

    def testWhitelist(_):  # line 887
# TODO test same for simple mode
        _.createFile(1)  # line 889
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 890
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 891
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 892
        sos.commit(options=["--force"])  # attempt to commit the file  # line 893
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 894
        try:  # Exit because dirty  # line 895
            sos.online()  # Exit because dirty  # line 895
            _.fail()  # Exit because dirty  # line 895
        except:  # exception expected  # line 896
            pass  # exception expected  # line 896
        _.createFile("x2")  # add another change  # line 897
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 898
        try:  # force beyond dirty flag check  # line 899
            sos.online(["--force"])  # force beyond dirty flag check  # line 899
            _.fail()  # force beyond dirty flag check  # line 899
        except:  # line 900
            pass  # line 900
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 901
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 902

        _.createFile(1)  # line 904
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 905
        sos.offline("xx", None, ["--track"])  # line 906
        sos.add(".", "./file*")  # line 907
        sos.commit()  # should NOT ask for force here  # line 908
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 909

    def testRemove(_):  # line 911
        _.createFile(1, "x" * 100)  # line 912
        sos.offline("trunk")  # line 913
        try:  # line 914
            sos.destroy("trunk")  # line 914
            _fail()  # line 914
        except:  # line 915
            pass  # line 915
        _.createFile(2, "y" * 10)  # line 916
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 917
        sos.destroy("trunk")  # line 918
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 919
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 920
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 921
        sos.branch("next")  # line 922
        _.createFile(3, "y" * 10)  # make a change  # line 923
        sos.destroy("added", "--force")  # should succeed  # line 924

    def testUsage(_):  # line 926
        try:  # TODO expect sys.exit(0)  # line 927
            sos.usage()  # TODO expect sys.exit(0)  # line 927
            _.fail()  # TODO expect sys.exit(0)  # line 927
        except:  # line 928
            pass  # line 928
        try:  # TODO expect sys.exit(0)  # line 929
            sos.usage("help")  # TODO expect sys.exit(0)  # line 929
            _.fail()  # TODO expect sys.exit(0)  # line 929
        except:  # line 930
            pass  # line 930
        try:  # TODO expect sys.exit(0)  # line 931
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 931
            _.fail()  # TODO expect sys.exit(0)  # line 931
        except:  # line 932
            pass  # line 932
        try:  # line 933
            sos.usage(version=True)  # line 933
            _.fail()  # line 933
        except:  # line 934
            pass  # line 934
        try:  # line 935
            sos.usage(version=True)  # line 935
            _.fail()  # line 935
        except:  # line 936
            pass  # line 936

    def testOnlyExcept(_):  # line 938
        ''' Test blacklist glob rules. '''  # line 939
        sos.offline(options=["--track"])  # line 940
        _.createFile("a.1")  # line 941
        _.createFile("a.2")  # line 942
        _.createFile("b.1")  # line 943
        _.createFile("b.2")  # line 944
        sos.add(".", "./a.?")  # line 945
        sos.add(".", "./?.1", negative=True)  # line 946
        out = wrapChannels(lambda _=None: sos.commit())  # line 947
        _.assertIn("ADD ./a.2", out)  # line 948
        _.assertNotIn("ADD ./a.1", out)  # line 949
        _.assertNotIn("ADD ./b.1", out)  # line 950
        _.assertNotIn("ADD ./b.2", out)  # line 951

    def testOnly(_):  # line 953
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 954
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 955
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 956
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 957
        sos.offline(options=["--track", "--strict"])  # line 958
        _.createFile(1)  # line 959
        _.createFile(2)  # line 960
        sos.add(".", "./file1")  # line 961
        sos.add(".", "./file2")  # line 962
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 963
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 964
        sos.commit()  # adds also file2  # line 965
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 966
        _.createFile(1, "cc")  # modify both files  # line 967
        _.createFile(2, "dd")  # line 968
        try:  # line 969
            sos.config(["set", "texttype", "file2"])  # line 969
        except SystemExit as E:  # line 970
            _.assertEqual(0, E.code)  # line 970
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 971
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 972
        _.assertTrue("./file2" in changes.modifications)  # line 973
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 974
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 975

    def testDiff(_):  # line 977
        try:  # manually mark this file as "textual"  # line 978
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 978
        except SystemExit as E:  # line 979
            _.assertEqual(0, E.code)  # line 979
        sos.offline(options=["--strict"])  # line 980
        _.createFile(1)  # line 981
        _.createFile(2)  # line 982
        sos.commit()  # line 983
        _.createFile(1, "sdfsdgfsdf")  # line 984
        _.createFile(2, "12343")  # line 985
        sos.commit()  # line 986
        _.createFile(1, "foobar")  # line 987
        _.createFile(3)  # line 988
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # compare with r1 (second counting from last which is r2)  # line 989
        _.assertIn("ADD ./file3", out)  # line 990
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "- | 0 |xxxxxxxxxx|", "+ | 0 |foobar|"], out)  # line 991
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 992

    def testReorderRenameActions(_):  # line 994
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 995
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 996
        try:  # line 997
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 997
            _.fail()  # line 997
        except:  # line 998
            pass  # line 998

    def testMove(_):  # line 1000
        sos.offline(options=["--strict", "--track"])  # line 1001
        _.createFile(1)  # line 1002
        sos.add(".", "./file?")  # line 1003
# test source folder missing
        try:  # line 1005
            sos.move("sub", "sub/file?", ".", "?file")  # line 1005
            _.fail()  # line 1005
        except:  # line 1006
            pass  # line 1006
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1008
        _.assertTrue(os.path.exists("sub"))  # line 1009
        _.assertTrue(os.path.exists("sub/file1"))  # line 1010
        _.assertFalse(os.path.exists("file1"))  # line 1011
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1013
        _.assertTrue(os.path.exists("1file"))  # line 1014
        _.assertFalse(os.path.exists("sub/file1"))  # line 1015
# test nothing matches source pattern
        try:  # line 1017
            sos.move(".", "a*", ".", "b*")  # line 1017
            _.fail()  # line 1017
        except:  # line 1018
            pass  # line 1018
        sos.add(".", "*")  # anything pattern  # line 1019
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1020
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1020
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1020
        except:  # line 1021
            pass  # line 1021
# test rename no conflict
        _.createFile(1)  # line 1023
        _.createFile(2)  # line 1024
        _.createFile(3)  # line 1025
        sos.add(".", "./file*")  # line 1026
        try:  # define an ignore pattern  # line 1027
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1027
        except SystemExit as E:  # line 1028
            _.assertEqual(0, E.code)  # line 1028
        try:  # line 1029
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1029
        except SystemExit as E:  # line 1030
            _.assertEqual(0, E.code)  # line 1030
        sos.move(".", "./file*", ".", "fi*le")  # line 1031
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1032
        _.assertFalse(os.path.exists("fi4le"))  # line 1033
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1035
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 1039
        sos.add(".", "./?a?b", ["--force"])  # line 1040
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1041
        _.createFile("1a2b")  # should not be tracked  # line 1042
        _.createFile("a1b2")  # should be tracked  # line 1043
        sos.commit()  # line 1044
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 1045
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1046
        _.createFile("1a1b1")  # line 1047
        _.createFile("1a1b2")  # line 1048
        sos.add(".", "?a?b*")  # line 1049
        _.assertIn("not unique", wrapChannels(lambda _=None: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 1050
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1054
        _.createFile(1)  # line 1055
        _.createFile(3)  # line 1056
        _.createFile(5)  # line 1057
        sos.offline()  # branch 0: only file1  # line 1058
        sos.branch()  # line 1059
        os.unlink("file1")  # line 1060
        os.unlink("file3")  # line 1061
        os.unlink("file5")  # line 1062
        _.createFile(2)  # line 1063
        _.createFile(4)  # line 1064
        _.createFile(6)  # line 1065
        sos.commit()  # branch 1: only file2  # line 1066
        sos.switch("0/")  # line 1067
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1068
        _.assertFalse(_.existsFile(1))  # line 1069
        _.assertFalse(_.existsFile(3))  # line 1070
        _.assertFalse(_.existsFile(5))  # line 1071
        _.assertTrue(_.existsFile(2))  # line 1072
        _.assertTrue(_.existsFile(4))  # line 1073
        _.assertTrue(_.existsFile(6))  # line 1074

    def testHashCollision(_):  # line 1076
        sos.offline()  # line 1077
        _.createFile(1)  # line 1078
        os.mkdir(sos.revisionFolder(0, 1))  # line 1079
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # line 1080
        _.createFile(1)  # line 1081
        try:  # should exit with error due to collision detection  # line 1082
            sos.commit()  # should exit with error due to collision detection  # line 1082
            _.fail()  # should exit with error due to collision detection  # line 1082
        except SystemExit as E:  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1083
            _.assertEqual(1, E.code)  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1083

    def testFindBase(_):  # line 1085
        old = os.getcwd()  # line 1086
        try:  # line 1087
            os.mkdir("." + os.sep + ".git")  # line 1088
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1089
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1090
            os.chdir("a" + os.sep + "b")  # line 1091
            s, vcs, cmd = sos.findSosVcsBase()  # line 1092
            _.assertIsNotNone(s)  # line 1093
            _.assertIsNotNone(vcs)  # line 1094
            _.assertEqual("git", cmd)  # line 1095
        finally:  # line 1096
            os.chdir(old)  # line 1096

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise

if __name__ == '__main__':  # line 1106
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1107
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1108
