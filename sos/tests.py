#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xfd742924

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

    def testRestoreFile(_):  # line 139
        m = sos.Metadata()  # line 140
        os.makedirs(sos.revisionFolder(0, 0))  # line 141
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 142
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 143
        _.assertTrue(_.existsFile("restored", b""))  # line 144

    def testGetAnyOfmap(_):  # line 146
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 147
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 148

    def testAjoin(_):  # line 150
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 151
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 152

    def testFindChanges(_):  # line 154
        m = sos.Metadata(os.getcwd())  # line 155
        try:  # line 156
            sos.config(["set", "texttype", "*"])  # line 156
        except SystemExit as E:  # line 157
            _.assertEqual(0, E.code)  # line 157
        try:  # will be stripped from leading paths anyway  # line 158
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 158
        except SystemExit as E:  # line 159
            _.assertEqual(0, E.code)  # line 159
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 160
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 161
            os.unlink(file)  # remove configuration file  # line 161
        _.createFile(1, "1")  # line 162
        m.createBranch(0)  # line 163
        _.assertEqual(1, len(m.paths))  # line 164
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 165
        _.createFile(1, "2")  # modify existing file  # line 166
        _.createFile(2, "2")  # add another file  # line 167
        m.loadCommit(0, 0)  # line 168
        changes, msg = m.findChanges()  # detect time skew  # line 169
        _.assertEqual(1, len(changes.additions))  # line 170
        _.assertEqual(0, len(changes.deletions))  # line 171
        _.assertEqual(1, len(changes.modifications))  # line 172
        _.assertEqual(0, len(changes.moves))  # line 173
        m.paths.update(changes.additions)  # line 174
        m.paths.update(changes.modifications)  # line 175
        _.createFile(2, "12")  # modify file again  # line 176
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 177
        _.assertEqual(0, len(changes.additions))  # line 178
        _.assertEqual(0, len(changes.deletions))  # line 179
        _.assertEqual(1, len(changes.modifications))  # line 180
        _.assertEqual(0, len(changes.moves))  # line 181
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 182
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 183
# TODO test moves

    def testFitStrings(_):  # line 186
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 187
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 188
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 189
    def testMoves(_):  # line 190
        _.createFile(1, "1")  # line 191
        _.createFile(2, "2", "sub")  # line 192
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 193
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 194
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 195
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 196
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 197
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 198
        out = wrapChannels(lambda _=None: sos.commit())  # line 199
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 200
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 201
        _.assertIn("Created new revision r01 (+00/-00/~00/#02)", out)  # TODO why is this not captured?  # line 202

    def testPatternPaths(_):  # line 204
        sos.offline(options=["--track"])  # line 205
        os.mkdir("sub")  # line 206
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 207
        sos.add("sub", "sub/file?")  # line 208
        sos.commit("test")  # should pick up sub/file1 pattern  # line 209
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 210
        _.createFile(1)  # line 211
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 212
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 212
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 212
        except:  # line 213
            pass  # line 213

    def testNoArgs(_):  # line 215
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 216

    def testAutoMetadataUpgrade(_):  # line 218
        sos.offline()  # line 219
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 220
            repo, branches, config = json.load(fd)  # line 220
        repo["version"] = None  # lower than any pip version  # line 221
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 222
        del repo["format"]  # simulate pre-1.3.5  # line 223
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 224
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 224
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # line 225
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 226

    def testFastBranching(_):  # line 228
        _.createFile(1)  # line 229
        sos.offline(options=["--strict"])  # b0/r0 = ./file1  # line 230
        _.createFile(2)  # line 231
        os.unlink("file1")  # line 232
        sos.commit()  # b0/r1 = ./file2  # line 233
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify once --fast becomes the new normal  # line 234
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 235
        _.createFile(3)  # line 236
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 237
        _.assertAllIn([sos.metaFile, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 238
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 239
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 240
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 241
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # revisions were copied to branch 1  # line 242
        _.assertAllIn([sos.metaFile, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # revisions were copied to branch 1  # line 243
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 246
        now = time.time()  # type: float  # line 247
        _.createFile(1)  # line 248
        sync()  # line 249
        sos.offline(options=["--strict"])  # line 250
        _.createFile(1, "abc")  # modify contents  # line 251
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 252
        sync()  # line 253
        out = wrapChannels(lambda _=None: sos.changes())  # line 254
        _.assertAllIn(["<older than last revision>", "<older than previously committed>"], out)  # line 255
        out = wrapChannels(lambda _=None: sos.commit())  # line 256
        _.assertAllIn(["<older than last revision>", "<older than previously committed>"], out)  # line 257

    def testGetParentBranch(_):  # line 259
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}})  # line 260
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 261
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 262
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 263
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 264

    def testTokenizeGlobPattern(_):  # line 266
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 267
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 268
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 269
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 270
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 271
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 272

    def testTokenizeGlobPatterns(_):  # line 274
        try:  # because number of literal strings differs  # line 275
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 275
            _.fail()  # because number of literal strings differs  # line 275
        except:  # line 276
            pass  # line 276
        try:  # because glob patterns differ  # line 277
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 277
            _.fail()  # because glob patterns differ  # line 277
        except:  # line 278
            pass  # line 278
        try:  # glob patterns differ, regardless of position  # line 279
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 279
            _.fail()  # glob patterns differ, regardless of position  # line 279
        except:  # line 280
            pass  # line 280
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 281
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 282
        try:  # succeeds, because glob patterns match (differ only in position)  # line 283
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 283
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 283
        except:  # line 284
            pass  # line 284

    def testConvertGlobFiles(_):  # line 286
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 287
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 288

    def testFolderRemove(_):  # line 290
        m = sos.Metadata(os.getcwd())  # line 291
        _.createFile(1)  # line 292
        _.createFile("a", prefix="sub")  # line 293
        sos.offline()  # line 294
        _.createFile(2)  # line 295
        os.unlink("sub" + os.sep + "a")  # line 296
        os.rmdir("sub")  # line 297
        changes = sos.changes()  # TODO replace by output check  # line 298
        _.assertEqual(1, len(changes.additions))  # line 299
        _.assertEqual(0, len(changes.modifications))  # line 300
        _.assertEqual(1, len(changes.deletions))  # line 301
        _.createFile("a", prefix="sub")  # line 302
        changes = sos.changes()  # line 303
        _.assertEqual(0, len(changes.deletions))  # line 304

    def testSwitchConflict(_):  # line 306
        sos.offline(options=["--strict"])  # (r0)  # line 307
        _.createFile(1)  # line 308
        sos.commit()  # add file (r1)  # line 309
        os.unlink("file1")  # line 310
        sos.commit()  # remove (r2)  # line 311
        _.createFile(1, "something else")  # line 312
        sos.commit()  # (r3)  # line 313
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 314
        _.existsFile(1, "x" * 10)  # line 315
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 316
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 317
        sos.switch("/1")  # add file1 back  # line 318
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 319
        _.existsFile(1, "something else")  # line 320

    def testComputeSequentialPathSet(_):  # line 322
        os.makedirs(sos.revisionFolder(0, 0))  # line 323
        os.makedirs(sos.revisionFolder(0, 1))  # line 324
        os.makedirs(sos.revisionFolder(0, 2))  # line 325
        os.makedirs(sos.revisionFolder(0, 3))  # line 326
        os.makedirs(sos.revisionFolder(0, 4))  # line 327
        m = sos.Metadata(os.getcwd())  # line 328
        m.branch = 0  # line 329
        m.commit = 2  # line 330
        m.saveBranches()  # line 331
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 332
        m.saveCommit(0, 0)  # initial  # line 333
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 334
        m.saveCommit(0, 1)  # mod  # line 335
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 336
        m.saveCommit(0, 2)  # add  # line 337
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 338
        m.saveCommit(0, 3)  # del  # line 339
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 340
        m.saveCommit(0, 4)  # readd  # line 341
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 342
        m.saveBranch(0)  # line 343
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 344
        m.saveBranches()  # line 345
        m.computeSequentialPathSet(0, 4)  # line 346
        _.assertEqual(2, len(m.paths))  # line 347

    def testParseRevisionString(_):  # line 349
        m = sos.Metadata(os.getcwd())  # line 350
        m.branch = 1  # line 351
        m.commits = {0: 0, 1: 1, 2: 2}  # line 352
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 353
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 354
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 355
        _.assertEqual((1, -1), m.parseRevisionString(""))  # line 356
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 357
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 358
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 359

    def testOfflineEmpty(_):  # line 361
        os.mkdir("." + os.sep + sos.metaFolder)  # line 362
        try:  # line 363
            sos.offline("trunk")  # line 363
            _.fail()  # line 363
        except SystemExit as E:  # line 364
            _.assertEqual(1, E.code)  # line 364
        os.rmdir("." + os.sep + sos.metaFolder)  # line 365
        sos.offline("test")  # line 366
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 367
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 368
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 369
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 370
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 371
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 372

    def testOfflineWithFiles(_):  # line 374
        _.createFile(1, "x" * 100)  # line 375
        _.createFile(2)  # line 376
        sos.offline("test")  # line 377
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 378
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 379
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 380
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 381
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 382
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 383
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 384

    def testBranch(_):  # line 386
        _.createFile(1, "x" * 100)  # line 387
        _.createFile(2)  # line 388
        sos.offline("test")  # b0/r0  # line 389
        sos.branch("other")  # b1/r0  # line 390
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 391
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 392
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 394
        _.createFile(1, "z")  # modify file  # line 396
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 397
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 398
        _.createFile(3, "z")  # line 400
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 401
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 402
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 407
        _.createFile(1, "x" * 100)  # line 408
        _.createFile(2)  # line 409
        sos.offline("test")  # line 410
        changes = sos.changes()  # line 411
        _.assertEqual(0, len(changes.additions))  # line 412
        _.assertEqual(0, len(changes.deletions))  # line 413
        _.assertEqual(0, len(changes.modifications))  # line 414
        _.createFile(1, "z")  # size change  # line 415
        changes = sos.changes()  # line 416
        _.assertEqual(0, len(changes.additions))  # line 417
        _.assertEqual(0, len(changes.deletions))  # line 418
        _.assertEqual(1, len(changes.modifications))  # line 419
        sos.commit("message")  # line 420
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 421
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 422
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 423
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 424
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 425
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 426
        os.unlink("file2")  # line 427
        changes = sos.changes()  # line 428
        _.assertEqual(0, len(changes.additions))  # line 429
        _.assertEqual(1, len(changes.deletions))  # line 430
        _.assertEqual(1, len(changes.modifications))  # line 431
        sos.commit("modified")  # line 432
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 433
        try:  # expecting Exit due to no changes  # line 434
            sos.commit("nothing")  # expecting Exit due to no changes  # line 434
            _.fail()  # expecting Exit due to no changes  # line 434
        except:  # line 435
            pass  # line 435

    def testGetBranch(_):  # line 437
        m = sos.Metadata(os.getcwd())  # line 438
        m.branch = 1  # current branch  # line 439
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 440
        _.assertEqual(27, m.getBranchByName(27))  # line 441
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 442
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 443
        _.assertIsNone(m.getBranchByName("unknown"))  # line 444
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 445
        _.assertEqual(13, m.getRevisionByName("13"))  # line 446
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 447
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 448

    def testTagging(_):  # line 450
        m = sos.Metadata(os.getcwd())  # line 451
        sos.offline()  # line 452
        _.createFile(111)  # line 453
        sos.commit("tag", ["--tag"])  # line 454
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # line 455
        _.assertTrue(any(("|tag" in line and line.endswith("|TAG") for line in out)))  # line 456
        _.createFile(2)  # line 457
        try:  # line 458
            sos.commit("tag")  # line 458
            _.fail()  # line 458
        except:  # line 459
            pass  # line 459
        sos.commit("tag-2", ["--tag"])  # line 460
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 461
        _.assertIn("TAG tag", out)  # line 462

    def testSwitch(_):  # line 464
        _.createFile(1, "x" * 100)  # line 465
        _.createFile(2, "y")  # line 466
        sos.offline("test")  # file1-2  in initial branch commit  # line 467
        sos.branch("second")  # file1-2  switch, having same files  # line 468
        sos.switch("0")  # no change  switch back, no problem  # line 469
        sos.switch("second")  # no change  # switch back, no problem  # line 470
        _.createFile(3, "y")  # generate a file  # line 471
        try:  # uncommited changes detected  # line 472
            sos.switch("test")  # uncommited changes detected  # line 472
            _.fail()  # uncommited changes detected  # line 472
        except SystemExit as E:  # line 473
            _.assertEqual(1, E.code)  # line 473
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 474
        sos.changes()  # line 475
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 476
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 477
        _.createFile("XXX")  # line 478
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 479
        _.assertIn("File tree has changes", out)  # line 480
        _.assertNotIn("File tree is unchanged", out)  # line 481
        _.assertIn("  * b00   'test'", out)  # line 482
        _.assertIn("    b01 'second'", out)  # line 483
        _.assertIn("(dirty)", out)  # one branch has commits  # line 484
        _.assertIn("(in sync)", out)  # the other doesn't  # line 485
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 486
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 487
        _.assertAllIn(["Metadata format", "Content checking:    deactivated", "Data compression:    deactivated", "Repository mode:     simple", "Number of branches:  2"], out)  # line 488
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 489
        _.createFile(4, "xy")  # generate a file  # line 490
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 491
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 492
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 493
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 494
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 495
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 496
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 497
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 498
        _.assertAllIn(["Dumping revisions"], out)  # line 499
        _.assertNotIn("Creating backup", out)  # line 500
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 501
        _.assertIn("Dumping revisions", out)  # line 502
        _.assertNotIn("Creating backup", out)  # line 503
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 504
        _.assertAllIn(["Creating backup"], out)  # line 505
        _.assertIn("Dumping revisions", out)  # line 506

    def testAutoDetectVCS(_):  # line 508
        os.mkdir(".git")  # line 509
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 510
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 511
            meta = fd.read()  # line 511
        _.assertTrue("\"master\"" in meta)  # line 512
        os.rmdir(".git")  # line 513

    def testUpdate(_):  # line 515
        sos.offline("trunk")  # create initial branch b0/r0  # line 516
        _.createFile(1, "x" * 100)  # line 517
        sos.commit("second")  # create b0/r1  # line 518

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 520
        _.assertFalse(_.existsFile(1))  # line 521

        sos.update("/1")  # recreate file1  # line 523
        _.assertTrue(_.existsFile(1))  # line 524

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 526
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 527
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 528
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 529

        sos.update("/1")  # do nothing, as nothing has changed  # line 531
        _.assertTrue(_.existsFile(1))  # line 532

        _.createFile(2, "y" * 100)  # line 534
#    out = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 537
        _.assertTrue(_.existsFile(2))  # line 538
        sos.update("trunk", ["--add"])  # only add stuff  # line 539
        _.assertTrue(_.existsFile(2))  # line 540
        sos.update("trunk")  # nothing to do  # line 541
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 542

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 544
        _.createFile(10, theirs)  # line 545
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 546
        _.createFile(11, mine)  # line 547
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 548
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 549

    def testUpdate2(_):  # line 551
        _.createFile("test.txt", "x" * 10)  # line 552
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 553
        sync()  # line 554
        sos.branch("mod")  # line 555
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 556
        sos.commit("mod")  # create b0/r1  # line 557
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 558
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 559
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 560
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 561
        _.createFile("test.txt", "x" * 10)  # line 562
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 563
        sync()  # line 564
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 565
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 566
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 567
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 568
        sync()  # line 569
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 570
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 571

    def testIsTextType(_):  # line 573
        m = sos.Metadata(".")  # line 574
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 575
        m.c.bintype = ["*.md.confluence"]  # line 576
        _.assertTrue(m.isTextType("ab.txt"))  # line 577
        _.assertTrue(m.isTextType("./ab.txt"))  # line 578
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 579
        _.assertFalse(m.isTextType("bc/ab."))  # line 580
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 581
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 582
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 583
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 584

    def testEolDet(_):  # line 586
        ''' Check correct end-of-line detection. '''  # line 587
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 588
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 589
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 590
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 591
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 592
        _.assertIsNone(sos.eoldet(b""))  # line 593
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 594

    def testMerge(_):  # line 596
        ''' Check merge results depending on user options. '''  # line 597
        a = b"a\nb\ncc\nd"  # type: bytes  # line 598
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 599
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 600
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 601
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 602
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 603
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 604
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 605
        a = b"a\nb\ncc\nd"  # line 606
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 607
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 608
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 609
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 610
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 612
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 613
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 615
        b = b"a\nc\ne"  # line 616
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 617
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 618
        a = b"a\nb\ne"  # intra-line merge  # line 619
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 620
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 621

    def testMergeEol(_):  # line 623
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 624
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 625
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 626
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 627
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 628

    def testPickyMode(_):  # line 630
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 631
        sos.offline("trunk", None, ["--picky"])  # line 632
        changes = sos.changes()  # line 633
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 634
        sos.add(".", "./file?", ["--force"])  # line 635
        _.createFile(1, "aa")  # line 636
        sos.commit("First")  # add one file  # line 637
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 638
        _.createFile(2, "b")  # line 639
        try:  # add nothing, because picky  # line 640
            sos.commit("Second")  # add nothing, because picky  # line 640
        except:  # line 641
            pass  # line 641
        sos.add(".", "./file?")  # line 642
        sos.commit("Third")  # line 643
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 644
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 645
        _.assertIn("    r0", out)  # because number of log lines was limited  # line 646
        _.assertIn("    r1", out)  # line 647
        _.assertIn("  * r2", out)  # line 648
        try:  # line 649
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 649
        except SystemExit as E:  # line 650
            _.assertEqual(0, E.code)  # line 650
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 651
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 652
        _.assertNotIn("    r1", out)  # line 653
        _.assertIn("  * r2", out)  # line 654
        _.createFile(3, prefix="sub")  # line 655
        sos.add("sub", "sub/file?")  # line 656
        changes = sos.changes()  # line 657
        _.assertEqual(1, len(changes.additions))  # line 658
        _.assertTrue("sub/file3" in changes.additions)  # line 659

    def testTrackedSubfolder(_):  # line 661
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 662
        os.mkdir("." + os.sep + "sub")  # line 663
        sos.offline("trunk", None, ["--track"])  # line 664
        _.createFile(1, "x")  # line 665
        _.createFile(1, "x", prefix="sub")  # line 666
        sos.add(".", "./file?")  # add glob pattern to track  # line 667
        sos.commit("First")  # line 668
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 669
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 670
        sos.commit("Second")  # one new file + meta  # line 671
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 672
        os.unlink("file1")  # remove from basefolder  # line 673
        _.createFile(2, "y")  # line 674
        sos.remove(".", "sub/file?")  # line 675
        try:  # raises Exit. TODO test the "suggest a pattern" case  # line 676
            sos.remove(".", "sub/bla")  # raises Exit. TODO test the "suggest a pattern" case  # line 676
            _.fail()  # raises Exit. TODO test the "suggest a pattern" case  # line 676
        except:  # line 677
            pass  # line 677
        sos.commit("Third")  # line 678
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 679
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 682
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 687
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 688
        _.createFile(1)  # line 689
        _.createFile("a123a")  # untracked file "a123a"  # line 690
        sos.add(".", "./file?")  # add glob tracking pattern  # line 691
        sos.commit("second")  # versions "file1"  # line 692
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 693
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 694
        _.assertIn("  | ./file?", out)  # line 695

        _.createFile(2)  # untracked file "file2"  # line 697
        sos.commit("third")  # versions "file2"  # line 698
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 699

        os.mkdir("." + os.sep + "sub")  # line 701
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 702
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 703
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 704

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 706
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 707
        sos.add(".", "./a*a")  # add tracking pattern  # line 708
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 709
        _.assertEqual(0, len(changes.modifications))  # line 710
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 711
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 712

        sos.commit("Second_2")  # line 714
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 715
        _.existsFile(1, b"x" * 10)  # line 716
        _.existsFile(2, b"x" * 10)  # line 717

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 719
        _.existsFile(1, b"x" * 10)  # line 720
        _.existsFile("a123a", b"x" * 10)  # line 721

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 723
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 724
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 725

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 727
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 728
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 729
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 730
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 731
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 732
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 733
# TODO test switch --meta

    def testLsTracked(_):  # line 736
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 737
        _.createFile(1)  # line 738
        _.createFile("foo")  # line 739
        sos.add(".", "./file*")  # capture one file  # line 740
        sos.ls()  # line 741
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 742
        _.assertInAny("TRK file1  (file*)", out)  # line 743
        _.assertNotInAny("... file1  (file*)", out)  # line 744
        _.assertInAny("    foo", out)  # line 745
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 746
        _.assertInAny("TRK file*", out)  # line 747
        _.createFile("a", prefix="sub")  # line 748
        sos.add("sub", "sub/a")  # line 749
        sos.ls("sub")  # line 750
        _.assertIn("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 751

    def testLineMerge(_):  # line 753
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 754
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 755
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 756
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 757

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 759
        _.createFile(1)  # line 760
        sos.offline("master", options=["--force"])  # line 761
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # line 762
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 763
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 764
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 765
        _.createFile(2)  # line 766
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 767
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 768
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 769
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 770

    def testLocalConfig(_):  # line 772
        sos.offline("bla", options=[])  # line 773
        try:  # line 774
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 774
        except SystemExit as E:  # line 775
            _.assertEqual(0, E.code)  # line 775
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 776

    def testConfigVariations(_):  # line 778
        def makeRepo():  # line 779
            try:  # line 780
                os.unlink("file1")  # line 780
            except:  # line 781
                pass  # line 781
            sos.offline("master", options=["--force"])  # line 782
            _.createFile(1)  # line 783
            sos.commit("Added file1")  # line 784
        try:  # line 785
            sos.config(["set", "strict", "on"])  # line 785
        except SystemExit as E:  # line 786
            _.assertEqual(0, E.code)  # line 786
        makeRepo()  # line 787
        _.assertTrue(checkRepoFlag("strict", True))  # line 788
        try:  # line 789
            sos.config(["set", "strict", "off"])  # line 789
        except SystemExit as E:  # line 790
            _.assertEqual(0, E.code)  # line 790
        makeRepo()  # line 791
        _.assertTrue(checkRepoFlag("strict", False))  # line 792
        try:  # line 793
            sos.config(["set", "strict", "yes"])  # line 793
        except SystemExit as E:  # line 794
            _.assertEqual(0, E.code)  # line 794
        makeRepo()  # line 795
        _.assertTrue(checkRepoFlag("strict", True))  # line 796
        try:  # line 797
            sos.config(["set", "strict", "no"])  # line 797
        except SystemExit as E:  # line 798
            _.assertEqual(0, E.code)  # line 798
        makeRepo()  # line 799
        _.assertTrue(checkRepoFlag("strict", False))  # line 800
        try:  # line 801
            sos.config(["set", "strict", "1"])  # line 801
        except SystemExit as E:  # line 802
            _.assertEqual(0, E.code)  # line 802
        makeRepo()  # line 803
        _.assertTrue(checkRepoFlag("strict", True))  # line 804
        try:  # line 805
            sos.config(["set", "strict", "0"])  # line 805
        except SystemExit as E:  # line 806
            _.assertEqual(0, E.code)  # line 806
        makeRepo()  # line 807
        _.assertTrue(checkRepoFlag("strict", False))  # line 808
        try:  # line 809
            sos.config(["set", "strict", "true"])  # line 809
        except SystemExit as E:  # line 810
            _.assertEqual(0, E.code)  # line 810
        makeRepo()  # line 811
        _.assertTrue(checkRepoFlag("strict", True))  # line 812
        try:  # line 813
            sos.config(["set", "strict", "false"])  # line 813
        except SystemExit as E:  # line 814
            _.assertEqual(0, E.code)  # line 814
        makeRepo()  # line 815
        _.assertTrue(checkRepoFlag("strict", False))  # line 816
        try:  # line 817
            sos.config(["set", "strict", "enable"])  # line 817
        except SystemExit as E:  # line 818
            _.assertEqual(0, E.code)  # line 818
        makeRepo()  # line 819
        _.assertTrue(checkRepoFlag("strict", True))  # line 820
        try:  # line 821
            sos.config(["set", "strict", "disable"])  # line 821
        except SystemExit as E:  # line 822
            _.assertEqual(0, E.code)  # line 822
        makeRepo()  # line 823
        _.assertTrue(checkRepoFlag("strict", False))  # line 824
        try:  # line 825
            sos.config(["set", "strict", "enabled"])  # line 825
        except SystemExit as E:  # line 826
            _.assertEqual(0, E.code)  # line 826
        makeRepo()  # line 827
        _.assertTrue(checkRepoFlag("strict", True))  # line 828
        try:  # line 829
            sos.config(["set", "strict", "disabled"])  # line 829
        except SystemExit as E:  # line 830
            _.assertEqual(0, E.code)  # line 830
        makeRepo()  # line 831
        _.assertTrue(checkRepoFlag("strict", False))  # line 832
        try:  # line 833
            sos.config(["set", "strict", "nope"])  # line 833
            _.fail()  # line 833
        except SystemExit as E:  # line 834
            _.assertEqual(1, E.code)  # line 834

    def testLsSimple(_):  # line 836
        _.createFile(1)  # line 837
        _.createFile("foo")  # line 838
        _.createFile("ign1")  # line 839
        _.createFile("ign2")  # line 840
        _.createFile("bar", prefix="sub")  # line 841
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 842
        try:  # define an ignore pattern  # line 843
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern  # line 843
        except SystemExit as E:  # line 844
            _.assertEqual(0, E.code)  # line 844
        try:  # additional ignore pattern  # line 845
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 845
        except SystemExit as E:  # line 846
            _.assertEqual(0, E.code)  # line 846
        try:  # define a list of ignore patterns  # line 847
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 847
        except SystemExit as E:  # line 848
            _.assertEqual(0, E.code)  # line 848
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # line 849
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 850
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 851
        _.assertInAny('    file1', out)  # line 852
        _.assertInAny('    ign1', out)  # line 853
        _.assertInAny('    ign2', out)  # line 854
        _.assertNotIn('DIR sub', out)  # line 855
        _.assertNotIn('    bar', out)  # line 856
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 857
        _.assertIn('DIR sub', out)  # line 858
        _.assertIn('    bar', out)  # line 859
        try:  # line 860
            sos.config(["rm", "foo", "bar"])  # line 860
            _.fail()  # line 860
        except SystemExit as E:  # line 861
            _.assertEqual(1, E.code)  # line 861
        try:  # line 862
            sos.config(["rm", "ignores", "foo"])  # line 862
            _.fail()  # line 862
        except SystemExit as E:  # line 863
            _.assertEqual(1, E.code)  # line 863
        try:  # line 864
            sos.config(["rm", "ignores", "ign1"])  # line 864
        except SystemExit as E:  # line 865
            _.assertEqual(0, E.code)  # line 865
        try:  # remove ignore pattern  # line 866
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 866
        except SystemExit as E:  # line 867
            _.assertEqual(0, E.code)  # line 867
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 868
        _.assertInAny('    ign1', out)  # line 869
        _.assertInAny('IGN ign2', out)  # line 870
        _.assertNotInAny('    ign2', out)  # line 871

    def testWhitelist(_):  # line 873
# TODO test same for simple mode
        _.createFile(1)  # line 875
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 876
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 877
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 878
        sos.commit(options=["--force"])  # attempt to commit the file  # line 879
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 880
        try:  # Exit because dirty  # line 881
            sos.online()  # Exit because dirty  # line 881
            _.fail()  # Exit because dirty  # line 881
        except:  # exception expected  # line 882
            pass  # exception expected  # line 882
        _.createFile("x2")  # add another change  # line 883
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 884
        try:  # force beyond dirty flag check  # line 885
            sos.online(["--force"])  # force beyond dirty flag check  # line 885
            _.fail()  # force beyond dirty flag check  # line 885
        except:  # line 886
            pass  # line 886
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 887
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 888

        _.createFile(1)  # line 890
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 891
        sos.offline("xx", None, ["--track"])  # line 892
        sos.add(".", "./file*")  # line 893
        sos.commit()  # should NOT ask for force here  # line 894
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 895

    def testRemove(_):  # line 897
        _.createFile(1, "x" * 100)  # line 898
        sos.offline("trunk")  # line 899
        try:  # line 900
            sos.destroy("trunk")  # line 900
            _fail()  # line 900
        except:  # line 901
            pass  # line 901
        _.createFile(2, "y" * 10)  # line 902
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 903
        sos.destroy("trunk")  # line 904
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 905
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 906
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 907
        sos.branch("next")  # line 908
        _.createFile(3, "y" * 10)  # make a change  # line 909
        sos.destroy("added", "--force")  # should succeed  # line 910

    def testUsage(_):  # line 912
        try:  # TODO expect sys.exit(0)  # line 913
            sos.usage()  # TODO expect sys.exit(0)  # line 913
            _.fail()  # TODO expect sys.exit(0)  # line 913
        except:  # line 914
            pass  # line 914
        try:  # line 915
            sos.usage(short=True)  # line 915
            _.fail()  # line 915
        except:  # line 916
            pass  # line 916

    def testOnlyExcept(_):  # line 918
        ''' Test blacklist glob rules. '''  # line 919
        sos.offline(options=["--track"])  # line 920
        _.createFile("a.1")  # line 921
        _.createFile("a.2")  # line 922
        _.createFile("b.1")  # line 923
        _.createFile("b.2")  # line 924
        sos.add(".", "./a.?")  # line 925
        sos.add(".", "./?.1", negative=True)  # line 926
        out = wrapChannels(lambda _=None: sos.commit())  # line 927
        _.assertIn("ADD ./a.2", out)  # line 928
        _.assertNotIn("ADD ./a.1", out)  # line 929
        _.assertNotIn("ADD ./b.1", out)  # line 930
        _.assertNotIn("ADD ./b.2", out)  # line 931

    def testOnly(_):  # line 933
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",))), sos.parseOnlyOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--only"]))  # line 934
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 935
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 936
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 937
        sos.offline(options=["--track", "--strict"])  # line 938
        _.createFile(1)  # line 939
        _.createFile(2)  # line 940
        sos.add(".", "./file1")  # line 941
        sos.add(".", "./file2")  # line 942
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 943
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 944
        sos.commit()  # adds also file2  # line 945
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 946
        _.createFile(1, "cc")  # modify both files  # line 947
        _.createFile(2, "dd")  # line 948
        try:  # line 949
            sos.config(["set", "texttype", "file2"])  # line 949
        except SystemExit as E:  # line 950
            _.assertEqual(0, E.code)  # line 950
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 951
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 952
        _.assertTrue("./file2" in changes.modifications)  # line 953
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 954
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff(onlys=_coconut.frozenset(("./file2",)))))  # line 955

    def testDiff(_):  # line 957
        try:  # manually mark this file as "textual"  # line 958
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 958
        except SystemExit as E:  # line 959
            _.assertEqual(0, E.code)  # line 959
        sos.offline(options=["--strict"])  # line 960
        _.createFile(1)  # line 961
        _.createFile(2)  # line 962
        sos.commit()  # line 963
        _.createFile(1, "sdfsdgfsdf")  # line 964
        _.createFile(2, "12343")  # line 965
        sos.commit()  # line 966
        _.createFile(1, "foobar")  # line 967
        _.createFile(3)  # line 968
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # compare with r1 (second counting from last which is r2)  # line 969
        _.assertIn("ADD ./file3", out)  # line 970
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "- | 0 |xxxxxxxxxx|", "+ | 0 |foobar|"], out)  # line 971
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 972

    def testReorderRenameActions(_):  # line 974
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 975
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 976
        try:  # line 977
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 977
            _.fail()  # line 977
        except:  # line 978
            pass  # line 978

    def testMove(_):  # line 980
        sos.offline(options=["--strict", "--track"])  # line 981
        _.createFile(1)  # line 982
        sos.add(".", "./file?")  # line 983
# test source folder missing
        try:  # line 985
            sos.move("sub", "sub/file?", ".", "?file")  # line 985
            _.fail()  # line 985
        except:  # line 986
            pass  # line 986
# test target folder missing: create it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 988
        _.assertTrue(os.path.exists("sub"))  # line 989
        _.assertTrue(os.path.exists("sub/file1"))  # line 990
        _.assertFalse(os.path.exists("file1"))  # line 991
# test move
        sos.move("sub", "sub/file?", ".", "./?file")  # line 993
        _.assertTrue(os.path.exists("1file"))  # line 994
        _.assertFalse(os.path.exists("sub/file1"))  # line 995
# test nothing matches source pattern
        try:  # line 997
            sos.move(".", "a*", ".", "b*")  # line 997
            _.fail()  # line 997
        except:  # line 998
            pass  # line 998
        sos.add(".", "*")  # anything pattern  # line 999
        try:  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1000
            sos.move(".", "a*", ".", "b*")  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1000
            _.fail()  # TODO check that alternative pattern "*" was suggested (1 hit)  # line 1000
        except:  # line 1001
            pass  # line 1001
# test rename no conflict
        _.createFile(1)  # line 1003
        _.createFile(2)  # line 1004
        _.createFile(3)  # line 1005
        sos.add(".", "./file*")  # line 1006
        try:  # define an ignore pattern  # line 1007
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1007
        except SystemExit as E:  # line 1008
            _.assertEqual(0, E.code)  # line 1008
        try:  # line 1009
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1009
        except SystemExit as E:  # line 1010
            _.assertEqual(0, E.code)  # line 1010
        sos.move(".", "./file*", ".", "fi*le")  # line 1011
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1012
        _.assertFalse(os.path.exists("fi4le"))  # line 1013
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1015
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # was renamed before  # line 1019
        sos.add(".", "./?a?b", ["--force"])  # line 1020
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1021
        _.createFile("1a2b")  # should not be tracked  # line 1022
        _.createFile("a1b2")  # should be tracked  # line 1023
        sos.commit()  # line 1024
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 1025
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1026
        _.createFile("1a1b1")  # line 1027
        _.createFile("1a1b2")  # line 1028
        sos.add(".", "?a?b*")  # line 1029
        _.assertIn("not unique", wrapChannels(lambda _=None: sos.move(".", "?a?b*", ".", "z?z?")))  # should raise error due to same target name  # line 1030
# TODO only rename if actually any files are versioned? or simply what is alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1034
        _.createFile(1)  # line 1035
        _.createFile(3)  # line 1036
        _.createFile(5)  # line 1037
        sos.offline()  # branch 0: only file1  # line 1038
        sos.branch()  # line 1039
        os.unlink("file1")  # line 1040
        os.unlink("file3")  # line 1041
        os.unlink("file5")  # line 1042
        _.createFile(2)  # line 1043
        _.createFile(4)  # line 1044
        _.createFile(6)  # line 1045
        sos.commit()  # branch 1: only file2  # line 1046
        sos.switch("0/")  # line 1047
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1048
        _.assertFalse(_.existsFile(1))  # line 1049
        _.assertFalse(_.existsFile(3))  # line 1050
        _.assertFalse(_.existsFile(5))  # line 1051
        _.assertTrue(_.existsFile(2))  # line 1052
        _.assertTrue(_.existsFile(4))  # line 1053
        _.assertTrue(_.existsFile(6))  # line 1054

    def testHashCollision(_):  # line 1056
        sos.offline()  # line 1057
        _.createFile(1)  # line 1058
        os.mkdir(sos.revisionFolder(0, 1))  # line 1059
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # line 1060
        _.createFile(1)  # line 1061
        try:  # should exit with error due to collision detection  # line 1062
            sos.commit()  # should exit with error due to collision detection  # line 1062
            _.fail()  # should exit with error due to collision detection  # line 1062
        except SystemExit as E:  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1063
            _.assertEqual(1, E.code)  # TODO will capture exit(0) which is wrong, change to check code in all places  # line 1063

    def testFindBase(_):  # line 1065
        old = os.getcwd()  # line 1066
        try:  # line 1067
            os.mkdir("." + os.sep + ".git")  # line 1068
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1069
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1070
            os.chdir("a" + os.sep + "b")  # line 1071
            s, vcs, cmd = sos.findSosVcsBase()  # line 1072
            _.assertIsNotNone(s)  # line 1073
            _.assertIsNotNone(vcs)  # line 1074
            _.assertEqual("git", cmd)  # line 1075
        finally:  # line 1076
            os.chdir(old)  # line 1076

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise

if __name__ == '__main__':  # line 1086
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1087
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1088
