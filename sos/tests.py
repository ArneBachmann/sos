#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x92e94c18

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
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 261
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 262
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 263
        _.createFile(3)  # line 264
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 265
        _.assertAllIn([sos.metaFile, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 266
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 267
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 268
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 269
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 270
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 271
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
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 288
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
        _.assertIn("  * b0   'test'", out)  # line 510
        _.assertIn("    b1 'second'", out)  # line 511
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
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 526
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 527
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 528
        _.assertNotIn("Creating backup", out)  # line 529
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 530
        _.assertIn("Dumping revisions", out)  # line 531
        _.assertNotIn("Creating backup", out)  # line 532
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 533
        _.assertAllIn(["Creating backup"], out)  # line 534
        _.assertIn("Dumping revisions", out)  # line 535
        sos.verbose.pop()  # line 536

    def testAutoDetectVCS(_):  # line 538
        os.mkdir(".git")  # line 539
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 540
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 541
            meta = fd.read()  # line 541
        _.assertTrue("\"master\"" in meta)  # line 542
        os.rmdir(".git")  # line 543

    def testUpdate(_):  # line 545
        sos.offline("trunk")  # create initial branch b0/r0  # line 546
        _.createFile(1, "x" * 100)  # line 547
        sos.commit("second")  # create b0/r1  # line 548

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 550
        _.assertFalse(_.existsFile(1))  # line 551

        sos.update("/1")  # recreate file1  # line 553
        _.assertTrue(_.existsFile(1))  # line 554

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 556
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 557
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 558
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 559

        sos.update("/1")  # do nothing, as nothing has changed  # line 561
        _.assertTrue(_.existsFile(1))  # line 562

        _.createFile(2, "y" * 100)  # line 564
#    out = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 567
        _.assertTrue(_.existsFile(2))  # line 568
        sos.update("trunk", ["--add"])  # only add stuff  # line 569
        _.assertTrue(_.existsFile(2))  # line 570
        sos.update("trunk")  # nothing to do  # line 571
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 572

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 574
        _.createFile(10, theirs)  # line 575
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 576
        _.createFile(11, mine)  # line 577
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 578
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 579

    def testUpdate2(_):  # line 581
        _.createFile("test.txt", "x" * 10)  # line 582
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 583
        sync()  # line 584
        sos.branch("mod")  # line 585
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 586
        sos.commit("mod")  # create b0/r1  # line 587
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 588
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 589
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 590
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 591
        _.createFile("test.txt", "x" * 10)  # line 592
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 593
        sync()  # line 594
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 595
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 596
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 597
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 598
        sync()  # line 599
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 600
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 601

    def testIsTextType(_):  # line 603
        m = sos.Metadata(".")  # line 604
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 605
        m.c.bintype = ["*.md.confluence"]  # line 606
        _.assertTrue(m.isTextType("ab.txt"))  # line 607
        _.assertTrue(m.isTextType("./ab.txt"))  # line 608
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 609
        _.assertFalse(m.isTextType("bc/ab."))  # line 610
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 611
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 612
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 613
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 614

    def testEolDet(_):  # line 616
        ''' Check correct end-of-line detection. '''  # line 617
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 618
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 619
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 620
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 621
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 622
        _.assertIsNone(sos.eoldet(b""))  # line 623
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 624

    def testMerge(_):  # line 626
        ''' Check merge results depending on user options. '''  # line 627
        a = b"a\nb\ncc\nd"  # type: bytes  # line 628
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 629
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 630
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 631
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 632
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 633
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 634
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 635
        a = b"a\nb\ncc\nd"  # line 636
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 637
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 638
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 639
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 640
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 642
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 643
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 645
        b = b"a\nc\ne"  # line 646
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 647
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 648
        a = b"a\nb\ne"  # intra-line merge  # line 649
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 650
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 651
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 652
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 653
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 654
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 655

    def testMergeEol(_):  # line 657
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 658
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 659
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 660
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 661
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 662

    def testPickyMode(_):  # line 664
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 665
        sos.offline("trunk", None, ["--picky"])  # line 666
        changes = sos.changes()  # line 667
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 668
        sos.add(".", "./file?", ["--force"])  # line 669
        _.createFile(1, "aa")  # line 670
        sos.commit("First")  # add one file  # line 671
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 672
        _.createFile(2, "b")  # line 673
        try:  # add nothing, because picky  # line 674
            sos.commit("Second")  # add nothing, because picky  # line 674
        except:  # line 675
            pass  # line 675
        sos.add(".", "./file?")  # line 676
        sos.commit("Third")  # line 677
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 678
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 679
        _.assertIn("    r0", out)  # line 680
        sys.argv.extend(["-n", "2"])  # line 681
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 682
        sys.argv.pop()  # line 683
        sys.argv.pop()  # line 683
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 684
        _.assertIn("    r1", out)  # line 685
        _.assertIn("  * r2", out)  # line 686
        try:  # line 687
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 687
        except SystemExit as E:  # line 688
            _.assertEqual(0, E.code)  # line 688
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 689
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 690
        _.assertNotIn("    r1", out)  # line 691
        _.assertIn("  * r2", out)  # line 692
        _.createFile(3, prefix="sub")  # line 693
        sos.add("sub", "sub/file?")  # line 694
        changes = sos.changes()  # line 695
        _.assertEqual(1, len(changes.additions))  # line 696
        _.assertTrue("sub/file3" in changes.additions)  # line 697

    def testTrackedSubfolder(_):  # line 699
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 700
        os.mkdir("." + os.sep + "sub")  # line 701
        sos.offline("trunk", None, ["--track"])  # line 702
        _.createFile(1, "x")  # line 703
        _.createFile(1, "x", prefix="sub")  # line 704
        sos.add(".", "./file?")  # add glob pattern to track  # line 705
        sos.commit("First")  # line 706
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 707
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 708
        sos.commit("Second")  # one new file + meta  # line 709
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 710
        os.unlink("file1")  # remove from basefolder  # line 711
        _.createFile(2, "y")  # line 712
        sos.remove(".", "sub/file?")  # line 713
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 714
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 714
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 714
        except:  # line 715
            pass  # line 715
        sos.commit("Third")  # line 716
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 717
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 720
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 725
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 726
        _.createFile(1)  # line 727
        _.createFile("a123a")  # untracked file "a123a"  # line 728
        sos.add(".", "./file?")  # add glob tracking pattern  # line 729
        sos.commit("second")  # versions "file1"  # line 730
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 731
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 732
        _.assertIn("  | ./file?", out)  # line 733

        _.createFile(2)  # untracked file "file2"  # line 735
        sos.commit("third")  # versions "file2"  # line 736
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 737

        os.mkdir("." + os.sep + "sub")  # line 739
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 740
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 741
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 742

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 744
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 745
        sos.add(".", "./a*a")  # add tracking pattern  # line 746
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 747
        _.assertEqual(0, len(changes.modifications))  # line 748
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 749
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 750

        sos.commit("Second_2")  # line 752
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 753
        _.existsFile(1, b"x" * 10)  # line 754
        _.existsFile(2, b"x" * 10)  # line 755

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 757
        _.existsFile(1, b"x" * 10)  # line 758
        _.existsFile("a123a", b"x" * 10)  # line 759

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 761
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 762
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 763

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 765
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 766
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 767
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 768
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 769
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 770
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 771
# TODO test switch --meta

    def testLsTracked(_):  # line 774
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 775
        _.createFile(1)  # line 776
        _.createFile("foo")  # line 777
        sos.add(".", "./file*")  # capture one file  # line 778
        sos.ls()  # line 779
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 780
        _.assertInAny("TRK file1  (file*)", out)  # line 781
        _.assertNotInAny("... file1  (file*)", out)  # line 782
        _.assertInAny("    foo", out)  # line 783
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 784
        _.assertInAny("TRK file*", out)  # line 785
        _.createFile("a", prefix="sub")  # line 786
        sos.add("sub", "sub/a")  # line 787
        sos.ls("sub")  # line 788
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 789

    def testLineMerge(_):  # line 791
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 792
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 793
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 794
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 795

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 797
        _.createFile(1)  # line 798
        sos.offline("master", options=["--force"])  # line 799
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # line 800
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 801
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 802
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 803
        _.createFile(2)  # line 804
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 805
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 806
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 807
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 808

    def testLocalConfig(_):  # line 810
        sos.offline("bla", options=[])  # line 811
        try:  # line 812
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 812
        except SystemExit as E:  # line 813
            _.assertEqual(0, E.code)  # line 813
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 814

    def testConfigVariations(_):  # line 816
        def makeRepo():  # line 817
            try:  # line 818
                os.unlink("file1")  # line 818
            except:  # line 819
                pass  # line 819
            sos.offline("master", options=["--force"])  # line 820
            _.createFile(1)  # line 821
            sos.commit("Added file1")  # line 822
        try:  # line 823
            sos.config(["set", "strict", "on"])  # line 823
        except SystemExit as E:  # line 824
            _.assertEqual(0, E.code)  # line 824
        makeRepo()  # line 825
        _.assertTrue(checkRepoFlag("strict", True))  # line 826
        try:  # line 827
            sos.config(["set", "strict", "off"])  # line 827
        except SystemExit as E:  # line 828
            _.assertEqual(0, E.code)  # line 828
        makeRepo()  # line 829
        _.assertTrue(checkRepoFlag("strict", False))  # line 830
        try:  # line 831
            sos.config(["set", "strict", "yes"])  # line 831
        except SystemExit as E:  # line 832
            _.assertEqual(0, E.code)  # line 832
        makeRepo()  # line 833
        _.assertTrue(checkRepoFlag("strict", True))  # line 834
        try:  # line 835
            sos.config(["set", "strict", "no"])  # line 835
        except SystemExit as E:  # line 836
            _.assertEqual(0, E.code)  # line 836
        makeRepo()  # line 837
        _.assertTrue(checkRepoFlag("strict", False))  # line 838
        try:  # line 839
            sos.config(["set", "strict", "1"])  # line 839
        except SystemExit as E:  # line 840
            _.assertEqual(0, E.code)  # line 840
        makeRepo()  # line 841
        _.assertTrue(checkRepoFlag("strict", True))  # line 842
        try:  # line 843
            sos.config(["set", "strict", "0"])  # line 843
        except SystemExit as E:  # line 844
            _.assertEqual(0, E.code)  # line 844
        makeRepo()  # line 845
        _.assertTrue(checkRepoFlag("strict", False))  # line 846
        try:  # line 847
            sos.config(["set", "strict", "true"])  # line 847
        except SystemExit as E:  # line 848
            _.assertEqual(0, E.code)  # line 848
        makeRepo()  # line 849
        _.assertTrue(checkRepoFlag("strict", True))  # line 850
        try:  # line 851
            sos.config(["set", "strict", "false"])  # line 851
        except SystemExit as E:  # line 852
            _.assertEqual(0, E.code)  # line 852
        makeRepo()  # line 853
        _.assertTrue(checkRepoFlag("strict", False))  # line 854
        try:  # line 855
            sos.config(["set", "strict", "enable"])  # line 855
        except SystemExit as E:  # line 856
            _.assertEqual(0, E.code)  # line 856
        makeRepo()  # line 857
        _.assertTrue(checkRepoFlag("strict", True))  # line 858
        try:  # line 859
            sos.config(["set", "strict", "disable"])  # line 859
        except SystemExit as E:  # line 860
            _.assertEqual(0, E.code)  # line 860
        makeRepo()  # line 861
        _.assertTrue(checkRepoFlag("strict", False))  # line 862
        try:  # line 863
            sos.config(["set", "strict", "enabled"])  # line 863
        except SystemExit as E:  # line 864
            _.assertEqual(0, E.code)  # line 864
        makeRepo()  # line 865
        _.assertTrue(checkRepoFlag("strict", True))  # line 866
        try:  # line 867
            sos.config(["set", "strict", "disabled"])  # line 867
        except SystemExit as E:  # line 868
            _.assertEqual(0, E.code)  # line 868
        makeRepo()  # line 869
        _.assertTrue(checkRepoFlag("strict", False))  # line 870
        try:  # line 871
            sos.config(["set", "strict", "nope"])  # line 871
            _.fail()  # line 871
        except SystemExit as E:  # line 872
            _.assertEqual(1, E.code)  # line 872

    def testLsSimple(_):  # line 874
        _.createFile(1)  # line 875
        _.createFile("foo")  # line 876
        _.createFile("ign1")  # line 877
        _.createFile("ign2")  # line 878
        _.createFile("bar", prefix="sub")  # line 879
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 880
        try:  # define an ignore pattern  # line 881
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern  # line 881
        except SystemExit as E:  # line 882
            _.assertEqual(0, E.code)  # line 882
        try:  # additional ignore pattern  # line 883
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 883
        except SystemExit as E:  # line 884
            _.assertEqual(0, E.code)  # line 884
        try:  # define a list of ignore patterns  # line 885
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 885
        except SystemExit as E:  # line 886
            _.assertEqual(0, E.code)  # line 886
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # line 887
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 888
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 889
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 890
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 891
        _.assertInAny('    file1', out)  # line 892
        _.assertInAny('    ign1', out)  # line 893
        _.assertInAny('    ign2', out)  # line 894
        _.assertNotIn('DIR sub', out)  # line 895
        _.assertNotIn('    bar', out)  # line 896
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 897
        _.assertIn('DIR sub', out)  # line 898
        _.assertIn('    bar', out)  # line 899
        try:  # line 900
            sos.config(["rm", "foo", "bar"])  # line 900
            _.fail()  # line 900
        except SystemExit as E:  # line 901
            _.assertEqual(1, E.code)  # line 901
        try:  # line 902
            sos.config(["rm", "ignores", "foo"])  # line 902
            _.fail()  # line 902
        except SystemExit as E:  # line 903
            _.assertEqual(1, E.code)  # line 903
        try:  # line 904
            sos.config(["rm", "ignores", "ign1"])  # line 904
        except SystemExit as E:  # line 905
            _.assertEqual(0, E.code)  # line 905
        try:  # remove ignore pattern  # line 906
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 906
        except SystemExit as E:  # line 907
            _.assertEqual(0, E.code)  # line 907
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 908
        _.assertInAny('    ign1', out)  # line 909
        _.assertInAny('IGN ign2', out)  # line 910
        _.assertNotInAny('    ign2', out)  # line 911

    def testWhitelist(_):  # line 913
# TODO test same for simple mode
        _.createFile(1)  # line 915
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 916
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 917
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 918
        sos.commit(options=["--force"])  # attempt to commit the file  # line 919
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 920
        try:  # Exit because dirty  # line 921
            sos.online()  # Exit because dirty  # line 921
            _.fail()  # Exit because dirty  # line 921
        except:  # exception expected  # line 922
            pass  # exception expected  # line 922
        _.createFile("x2")  # add another change  # line 923
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 924
        try:  # force beyond dirty flag check  # line 925
            sos.online(["--force"])  # force beyond dirty flag check  # line 925
            _.fail()  # force beyond dirty flag check  # line 925
        except:  # line 926
            pass  # line 926
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 927
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 928

        _.createFile(1)  # line 930
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 931
        sos.offline("xx", None, ["--track"])  # line 932
        sos.add(".", "./file*")  # line 933
        sos.commit()  # should NOT ask for force here  # line 934
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 935

    def testRemove(_):  # line 937
        _.createFile(1, "x" * 100)  # line 938
        sos.offline("trunk")  # line 939
        try:  # line 940
            sos.destroy("trunk")  # line 940
            _fail()  # line 940
        except:  # line 941
            pass  # line 941
        _.createFile(2, "y" * 10)  # line 942
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 943
        sos.destroy("trunk")  # line 944
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 945
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 946
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 947
        sos.branch("next")  # line 948
        _.createFile(3, "y" * 10)  # make a change  # line 949
        sos.destroy("added", "--force")  # should succeed  # line 950

    def testFastBranchingOnEmptyHistory(_):  # line 952
        ''' Test fast branching without revisions and with them. '''  # line 953
        sos.offline(options=["--strict", "--compress"])  # b0  # line 954
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 955
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 956
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 957
        sos.destroy("2")  # line 958
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 959
        _.assertIn("b0 'trunk' @", out)  # line 960
        _.assertIn("b1         @", out)  # line 961
        _.assertIn("b3         @", out)  # line 962
        _.assertNotIn("b2         @", out)  # line 963
        sos.branch("", "")  # non-fast branching of b4  # line 964
        _.createFile(1)  # line 965
        _.createFile(2)  # line 966
        sos.commit("")  # line 967
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 968
        sos.destroy("4")  # line 969
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 970
        _.assertIn("b0 'trunk' @", out)  # line 971
        _.assertIn("b1         @", out)  # line 972
        _.assertIn("b3         @", out)  # line 973
        _.assertIn("b5         @", out)  # line 974
        _.assertNotIn("b2         @", out)  # line 975
        _.assertNotIn("b4         @", out)  # line 976
# TODO add more files and branch again

    def testUsage(_):  # line 979
        try:  # TODO expect sys.exit(0)  # line 980
            sos.usage()  # TODO expect sys.exit(0)  # line 980
            _.fail()  # TODO expect sys.exit(0)  # line 980
        except:  # line 981
            pass  # line 981
        try:  # TODO expect sys.exit(0)  # line 982
            sos.usage("help")  # TODO expect sys.exit(0)  # line 982
            _.fail()  # TODO expect sys.exit(0)  # line 982
        except:  # line 983
            pass  # line 983
        try:  # TODO expect sys.exit(0)  # line 984
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 984
            _.fail()  # TODO expect sys.exit(0)  # line 984
        except:  # line 985
            pass  # line 985
        try:  # line 986
            sos.usage(version=True)  # line 986
            _.fail()  # line 986
        except:  # line 987
            pass  # line 987
        try:  # line 988
            sos.usage(version=True)  # line 988
            _.fail()  # line 988
        except:  # line 989
            pass  # line 989

    def testOnlyExcept(_):  # line 991
        ''' Test blacklist glob rules. '''  # line 992
        sos.offline(options=["--track"])  # line 993
        _.createFile("a.1")  # line 994
        _.createFile("a.2")  # line 995
        _.createFile("b.1")  # line 996
        _.createFile("b.2")  # line 997
        sos.add(".", "./a.?")  # line 998
        sos.add(".", "./?.1", negative=True)  # line 999
        out = wrapChannels(lambda _=None: sos.commit())  # line 1000
        _.assertIn("ADD ./a.2", out)  # line 1001
        _.assertNotIn("ADD ./a.1", out)  # line 1002
        _.assertNotIn("ADD ./b.1", out)  # line 1003
        _.assertNotIn("ADD ./b.2", out)  # line 1004

    def testOnly(_):  # line 1006
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 1007
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1008
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1009
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1010
        sos.offline(options=["--track", "--strict"])  # line 1011
        _.createFile(1)  # line 1012
        _.createFile(2)  # line 1013
        sos.add(".", "./file1")  # line 1014
        sos.add(".", "./file2")  # line 1015
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1016
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1017
        sos.commit()  # adds also file2  # line 1018
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1019
        _.createFile(1, "cc")  # modify both files  # line 1020
        _.createFile(2, "dd")  # line 1021
        try:  # line 1022
            sos.config(["set", "texttype", "file2"])  # line 1022
        except SystemExit as E:  # line 1023
            _.assertEqual(0, E.code)  # line 1023
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1024
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1025
        _.assertTrue("./file2" in changes.modifications)  # line 1026
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 1027
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1028
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1029
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff(excps=_coconut.frozenset(("./file2",)))))  # line 1030

    def testDiff(_):  # line 1032
        try:  # manually mark this file as "textual"  # line 1033
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1033
        except SystemExit as E:  # line 1034
            _.assertEqual(0, E.code)  # line 1034
        sos.offline(options=["--strict"])  # line 1035
        _.createFile(1)  # line 1036
        _.createFile(2)  # line 1037
        sos.commit()  # line 1038
        _.createFile(1, "sdfsdgfsdf")  # line 1039
        _.createFile(2, "12343")  # line 1040
        sos.commit()  # line 1041
        _.createFile(1, "foobar")  # line 1042
        _.createFile(3)  # line 1043
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # compare with r1 (second counting from last which is r2)  # line 1044
        _.assertIn("ADD ./file3", out)  # line 1045
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "-~- 0 |xxxxxxxxxx|", "+~+ 0 |foobar|"], out)  # line 1046
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1047

    def testReorderRenameActions(_):  # line 1049
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1050
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1051
        try:  # line 1052
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1052
            _.fail()  # line 1052
        except:  # line 1053
            pass  # line 1053

    def testPublish(_):  # line 1055
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1056

    def testMove(_):  # line 1058
        sos.offline(options=["--strict", "--track"])  # line 1059
        _.createFile(1)  # line 1060
        sos.add(".", "./file?")  # line 1061
# test source folder missing
        try:  # line 1063
            sos.move("sub", "sub/file?", ".", "?file")  # line 1063
            _.fail()  # line 1063
        except:  # line 1064
            pass  # line 1064
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1066
        _.assertTrue(os.path.exists("sub"))  # line 1067
        _.assertTrue(os.path.exists("sub/file1"))  # line 1068
        _.assertFalse(os.path.exists("file1"))  # line 1069
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1071
        _.assertTrue(os.path.exists("1file"))  # line 1072
        _.assertFalse(os.path.exists("sub/file1"))  # line 1073
# test nothing matches source pattern
        try:  # line 1075
            sos.move(".", "a*", ".", "b*")  # line 1075
            _.fail()  # line 1075
        except:  # line 1076
            pass  # line 1076
        sos.add(".", "*")  # anything pattern  # line 1077
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1078
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1078
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1078
        except:  # line 1079
            pass  # line 1079
# test rename no conflict
        _.createFile(1)  # line 1081
        _.createFile(2)  # line 1082
        _.createFile(3)  # line 1083
        sos.add(".", "./file*")  # line 1084
        try:  # define an ignore pattern  # line 1085
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1085
        except SystemExit as E:  # line 1086
            _.assertEqual(0, E.code)  # line 1086
        try:  # line 1087
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1087
        except SystemExit as E:  # line 1088
            _.assertEqual(0, E.code)  # line 1088
        sos.move(".", "./file*", ".", "fi*le")  # line 1089
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1090
        _.assertFalse(os.path.exists("fi4le"))  # line 1091
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1093
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 1097
        sos.add(".", "./?a?b", ["--force"])  # line 1098
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1099
        _.createFile("1a2b")  # should not be tracked  # line 1100
        _.createFile("a1b2")  # should be tracked  # line 1101
        sos.commit()  # line 1102
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 1103
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1104
        _.createFile("1a1b1")  # line 1105
        _.createFile("1a1b2")  # line 1106
        sos.add(".", "?a?b*")  # line 1107
        _.assertIn("not unique", wrapChannels(lambda _=None: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 1108
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1112
        _.createFile(1)  # line 1113
        _.createFile(3)  # line 1114
        _.createFile(5)  # line 1115
        sos.offline()  # branch 0: only file1  # line 1116
        sos.branch()  # line 1117
        os.unlink("file1")  # line 1118
        os.unlink("file3")  # line 1119
        os.unlink("file5")  # line 1120
        _.createFile(2)  # line 1121
        _.createFile(4)  # line 1122
        _.createFile(6)  # line 1123
        sos.commit()  # branch 1: only file2  # line 1124
        sos.switch("0/")  # line 1125
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1126
        _.assertFalse(_.existsFile(1))  # line 1127
        _.assertFalse(_.existsFile(3))  # line 1128
        _.assertFalse(_.existsFile(5))  # line 1129
        _.assertTrue(_.existsFile(2))  # line 1130
        _.assertTrue(_.existsFile(4))  # line 1131
        _.assertTrue(_.existsFile(6))  # line 1132

    def testHashCollision(_):  # line 1134
        sos.offline()  # line 1135
        _.createFile(1)  # line 1136
        os.mkdir(sos.revisionFolder(0, 1))  # line 1137
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # line 1138
        _.createFile(1)  # line 1139
        try:  # should exit with error due to collision detection  # line 1140
            sos.commit()  # should exit with error due to collision detection  # line 1140
            _.fail()  # should exit with error due to collision detection  # line 1140
        except SystemExit as E:  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1141
            _.assertEqual(1, E.code)  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1141

    def testFindBase(_):  # line 1143
        old = os.getcwd()  # line 1144
        try:  # line 1145
            os.mkdir("." + os.sep + ".git")  # line 1146
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1147
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1148
            os.chdir("a" + os.sep + "b")  # line 1149
            s, vcs, cmd = sos.findSosVcsBase()  # line 1150
            _.assertIsNotNone(s)  # line 1151
            _.assertIsNotNone(vcs)  # line 1152
            _.assertEqual("git", cmd)  # line 1153
        finally:  # line 1154
            os.chdir(old)  # line 1154

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1165
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1166
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1167
