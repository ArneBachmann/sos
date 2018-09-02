#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xc970a226

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
    class StreamCopyWrapper(TextIOWrapper):  # line 71
        def __init__(_):  # line 72
            TextIOWrapper.__init__(_, BufferedRandom(BytesIO(b"")), encoding=sos.UTF8)  # line 72
        def write(_, bla):  # line 73
            oldso.write(bla)  # line 73
            TextIOWrapper.write(_, bla)  # line 73
    buf = StreamCopyWrapper()  # line 74
    handler = logging.StreamHandler(buf)  # TODO doesn't seem to be captured  # line 75
    sys.stdout = sys.stderr = buf  # assignment goes right to left  # line 76
    logging.getLogger().addHandler(handler)  # line 77
    try:  # capture output into buf  # line 78
        func()  # capture output into buf  # line 78
    except Exception as E:  # line 79
        buf.write(str(E) + "\n")  # line 79
        traceback.print_exc(file=buf)  # line 79
    except SystemExit as F:  # line 80
        buf.write("EXIT CODE %s" % F.code + "\n")  # line 80
        traceback.print_exc(file=buf)  # line 80
    logging.getLogger().removeHandler(handler)  # line 81
    sys.argv, sys.stdout, sys.stderr = oldv, oldso, oldse  # TODO when run using pythonw.exe and/or no console, these could be None  # line 82
    buf.seek(0)  # line 83
    return _coconut_tail_call(buf.read)  # line 84

def mockInput(datas: '_coconut.typing.Sequence[str]', func: '_coconut.typing.Callable[[], Any]') -> 'Any':  # line 86
    try:  # via python sos/tests.py  # line 87
        with mock.patch("sos._utility.input", side_effect=datas):  # line 88
            return func()  # line 88
    except:  # via setup.py  # line 89
        with mock.patch("sos.utility.input", side_effect=datas):  # line 90
            return func()  # line 90

def setRepoFlag(name: 'str', value: 'Any', toConfig: 'bool'=False):  # line 92
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 93
        flags, branches, config = json.loads(fd.read())  # line 93
    if not toConfig:  # line 94
        flags[name] = value  # line 94
    else:  # line 95
        config[name] = value  # line 95
    with open(sos.metaFolder + os.sep + sos.metaFile, "w") as fd:  # line 96
        fd.write(json.dumps((flags, branches, config)))  # line 96

def checkRepoFlag(name: 'str', flag: '_coconut.typing.Optional[bool]'=None, value: '_coconut.typing.Optional[Any]'=None) -> 'bool':  # line 98
    with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 99
        flags, branches, config = json.loads(fd.read())  # line 99
    return (name in flags and flags[name] == flag) if flag is not None else (name in config and config[name] == value)  # line 100


class Tests(unittest.TestCase):  # line 103
    ''' Entire test suite. '''  # line 104

    def setUp(_):  # line 106
        sos.Metadata.singleton = None  # line 107
        for entry in os.listdir(testFolder):  # cannot reliably remove testFolder on Windows when using TortoiseSVN as VCS  # line 108
            resource = os.path.join(testFolder, entry)  # type: str  # line 109
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


# Uni tests
    def testAccessor(_):  # line 153
        a = sos.Accessor({"a": 1})  # line 154
        _.assertEqual((1, 1), (a["a"], a.a))  # line 155

    def testIndexing(_):  # line 157
        m = sos.Metadata()  # line 158
        m.commits = {}  # line 159
        _.assertEqual(1, m.correctNegativeIndexing(1))  # line 160
        _.assertEqual(9999999999999999, m.correctNegativeIndexing(9999999999999999))  # line 161
        _.assertEqual(0, m.correctNegativeIndexing(0))  # zero always returns zero, even no commits present  # line 162
        try:  # line 163
            m.correctNegativeIndexing(-1)  # line 163
            _.fail()  # line 163
        except SystemExit as E:  # line 164
            _.assertEqual(1, E.code)  # line 164
        m.commits = {0: sos.CommitInfo(0, 0), 1: sos.CommitInfo(1, 0)}  # line 165
        _.assertEqual(1, m.correctNegativeIndexing(-1))  # zero always returns zero, even no commits present  # line 166
        _.assertEqual(0, m.correctNegativeIndexing(-2))  # zero always returns zero, even no commits present  # line 167
        try:  # line 168
            m.correctNegativeIndexing(-3)  # line 168
            _.fail()  # line 168
        except SystemExit as E:  # line 169
            _.assertEqual(1, E.code)  # line 169

    def testRestoreFile(_):  # line 171
        m = sos.Metadata()  # line 172
        os.makedirs(sos.revisionFolder(0, 0))  # line 173
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 174
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 175
        _.assertTrue(_.existsFile("restored", b""))  # line 176

    def testGetAnyOfmap(_):  # line 178
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 179
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 180

    def testAjoin(_):  # line 182
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 183
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 184

    def testFindChanges(_):  # line 186
        m = sos.Metadata(os.getcwd())  # line 187
        try:  # line 188
            sos.config(["set", "texttype", "*"])  # line 188
        except SystemExit as E:  # line 189
            _.assertEqual(0, E.code)  # line 189
        try:  # will be stripped from leading paths anyway  # line 190
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 190
        except SystemExit as E:  # line 191
            _.assertEqual(0, E.code)  # line 191
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 192
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 193
            os.unlink(file)  # remove configuration file  # line 193
        _.createFile(9, b"")  # line 194
        _.createFile(1, "1")  # line 195
        m.createBranch(0)  # line 196
        _.assertEqual(2, len(m.paths))  # line 197
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 198
        _.createFile(1, "2")  # modify existing file  # line 199
        _.createFile(2, "2")  # add another file  # line 200
        m.loadCommit(0, 0)  # line 201
        changes, msg = m.findChanges()  # detect time skew  # line 202
        _.assertEqual(1, len(changes.additions))  # line 203
        _.assertEqual(0, len(changes.deletions))  # line 204
        _.assertEqual(1, len(changes.modifications))  # line 205
        _.assertEqual(0, len(changes.moves))  # line 206
        m.paths.update(changes.additions)  # line 207
        m.paths.update(changes.modifications)  # line 208
        _.createFile(2, "12")  # modify file again  # line 209
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 210
        _.assertEqual(0, len(changes.additions))  # line 211
        _.assertEqual(0, len(changes.deletions))  # line 212
        _.assertEqual(1, len(changes.modifications))  # line 213
        _.assertEqual(0, len(changes.moves))  # line 214
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 215
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 216
# TODO test moves

    def testDumpSorting(_):  # line 219
        m = sos.Metadata()  # type: Metadata  # line 220
        _.createFile(1)  # line 221
        sos.offline()  # line 222
        _.createFile(2)  # line 223
        _.createFile(3)  # line 224
        sos.commit()  # line 225
        _.createFile(4)  # line 226
        _.createFile(5)  # line 227
        sos.commit()  # line 228
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # type: List[str]  # line 229
        _.assertTrue(out.index("b0%sr2" % os.sep) > out.index("b0%sr1" % os.sep))  # line 230
        _.assertTrue(out.index("b0%sr1" % os.sep) > out.index("b0%sr0" % os.sep))  # line 231

    def testFitStrings(_):  # line 233
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 234
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 235
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 236
    def testMoves(_):  # line 237
        _.createFile(1, "1")  # line 238
        _.createFile(2, "2", "sub")  # line 239
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 240
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 241
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 242
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 243
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 244
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 245
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # line 246
        _.assertIn("MOV ..%sfile2  <-  file2" % os.sep, out)  # no ./ for relative OS-specific paths  # line 247
        _.assertIn("MOV file1  <-  ..%sfile1" % os.sep, out)  # line 248
        out = wrapChannels(lambda _=None: sos.commit())  # line 249
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 250
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 251
        _.assertAllIn(["Created new revision r01", "summing 628 bytes in 2 files (88.22% SOS overhead)"], out)  # TODO why is this not captured?  # line 252

    def testPatternPaths(_):  # line 254
        sos.offline(options=["--track"])  # line 255
        os.mkdir("sub")  # line 256
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 257
        out = wrapChannels(lambda _=None: sos.add("sub", "sub/file?"))  # type: str  # line 258
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", os.path.abspath("sub")], out)  # line 259
        sos.commit("test")  # should pick up sub/file1 pattern  # line 260
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 261
        _.createFile(1)  # line 262
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 263
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 263
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 263
        except:  # line 264
            pass  # line 264

    def testNoArgs(_):  # line 266
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 267

    def testAutoMetadataUpgrade(_):  # line 269
        sos.offline()  # line 270
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 271
            repo, branches, config = json.load(fd)  # line 271
        repo["version"] = None  # lower than any pip version  # line 272
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 273
        del repo["format"]  # simulate pre-1.3.5  # line 274
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 275
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 275
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # type: str  # line 276
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 277

    def testFastBranching(_):  # line 279
        _.createFile(1)  # line 280
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict", "--verbose"]))  # type: str  # b0/r0 = ./file1  # line 281
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 282
        _.createFile(2)  # line 283
        os.unlink("file1")  # line 284
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 285
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 286
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 287
        _.createFile(3)  # line 288
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 289
        _.assertAllIn([sos.metaFile, sos.metaBack, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 290
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 291
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 292
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 293
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 294
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 295
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 298
        now = time.time()  # type: float  # line 299
        _.createFile(1)  # line 300
        sync()  # line 301
        sos.offline(options=["--strict"])  # line 302
        _.createFile(1, "abc")  # modify contents  # line 303
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 304
        sync()  # line 305
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 306
        _.assertIn("<older than previously committed>", out)  # line 307
        out = wrapChannels(lambda _=None: sos.commit())  # line 308
        _.assertIn("<older than previously committed>", out)  # line 309

    def testGetParentBranch(_):  # line 311
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 312
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 313
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 314
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 315
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 316

    def testTokenizeGlobPattern(_):  # line 318
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 319
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 320
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 321
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 322
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 323
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 324

    def testTokenizeGlobPatterns(_):  # line 326
        try:  # because number of literal strings differs  # line 327
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 327
            _.fail()  # because number of literal strings differs  # line 327
        except:  # line 328
            pass  # line 328
        try:  # because glob patterns differ  # line 329
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 329
            _.fail()  # because glob patterns differ  # line 329
        except:  # line 330
            pass  # line 330
        try:  # glob patterns differ, regardless of position  # line 331
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 331
            _.fail()  # glob patterns differ, regardless of position  # line 331
        except:  # line 332
            pass  # line 332
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 333
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 334
        try:  # succeeds, because glob patterns match (differ only in position)  # line 335
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 335
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 335
        except:  # line 336
            pass  # line 336

    def testConvertGlobFiles(_):  # line 338
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 339
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 340

    def testFolderRemove(_):  # line 342
        m = sos.Metadata(os.getcwd())  # line 343
        _.createFile(1)  # line 344
        _.createFile("a", prefix="sub")  # line 345
        sos.offline()  # line 346
        _.createFile(2)  # line 347
        os.unlink("sub" + os.sep + "a")  # line 348
        os.rmdir("sub")  # line 349
        changes = sos.changes()  # TODO #254 replace by output check  # line 350
        _.assertEqual(1, len(changes.additions))  # line 351
        _.assertEqual(0, len(changes.modifications))  # line 352
        _.assertEqual(1, len(changes.deletions))  # line 353
        _.createFile("a", prefix="sub")  # line 354
        changes = sos.changes()  # line 355
        _.assertEqual(0, len(changes.deletions))  # line 356

    def testSwitchConflict(_):  # line 358
        sos.offline(options=["--strict"])  # (r0)  # line 359
        _.createFile(1)  # line 360
        sos.commit()  # add file (r1)  # line 361
        os.unlink("file1")  # line 362
        sos.commit()  # remove (r2)  # line 363
        _.createFile(1, "something else")  # line 364
        sos.commit()  # (r3)  # line 365
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 366
        _.existsFile(1, "x" * 10)  # line 367
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 368
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 369
        sos.switch("/1")  # add file1 back  # line 370
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 371
        _.existsFile(1, "something else")  # line 372

    def testComputeSequentialPathSet(_):  # line 374
        os.makedirs(sos.revisionFolder(0, 0))  # line 375
        os.makedirs(sos.revisionFolder(0, 1))  # line 376
        os.makedirs(sos.revisionFolder(0, 2))  # line 377
        os.makedirs(sos.revisionFolder(0, 3))  # line 378
        os.makedirs(sos.revisionFolder(0, 4))  # line 379
        m = sos.Metadata(os.getcwd())  # line 380
        m.branch = 0  # line 381
        m.commit = 2  # line 382
        m.saveBranches()  # line 383
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 384
        m.saveCommit(0, 0)  # initial  # line 385
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 386
        m.saveCommit(0, 1)  # mod  # line 387
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 388
        m.saveCommit(0, 2)  # add  # line 389
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 390
        m.saveCommit(0, 3)  # del  # line 391
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 392
        m.saveCommit(0, 4)  # readd  # line 393
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 394
        m.saveBranch(0)  # line 395
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 396
        m.saveBranches()  # line 397
        m.computeSequentialPathSet(0, 4)  # line 398
        _.assertEqual(2, len(m.paths))  # line 399

    def testParseRevisionString(_):  # line 401
        m = sos.Metadata(os.getcwd())  # line 402
        m.branch = 1  # line 403
        m.commits = {0: 0, 1: 1, 2: 2}  # line 404
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 405
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 406
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 407
        _.assertEqual((None, None), m.parseRevisionString(""))  # line 408
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 409
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 410
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 411

    def testOfflineEmpty(_):  # line 413
        os.mkdir("." + os.sep + sos.metaFolder)  # line 414
        try:  # line 415
            sos.offline("trunk")  # line 415
            _.fail()  # line 415
        except SystemExit as E:  # line 416
            _.assertEqual(1, E.code)  # line 416
        os.rmdir("." + os.sep + sos.metaFolder)  # line 417
        sos.offline("test")  # line 418
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 419
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 420
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 421
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 422
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 423
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 424

    def testOfflineWithFiles(_):  # line 426
        _.createFile(1, "x" * 100)  # line 427
        _.createFile(2)  # line 428
        sos.offline("test")  # line 429
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 430
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 431
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 432
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 433
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 434
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 435
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 436

    def testBranch(_):  # line 438
        _.createFile(1, "x" * 100)  # line 439
        _.createFile(2)  # line 440
        sos.offline("test")  # b0/r0  # line 441
        sos.branch("other")  # b1/r0  # line 442
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 443
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 444
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 446
        _.createFile(1, "z")  # modify file  # line 448
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 449
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 450
        _.createFile(3, "z")  # line 452
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 453
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 454
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 459
        _.createFile(1, "x" * 100)  # line 460
        _.createFile(2)  # line 461
        sos.offline("test")  # line 462
        changes = sos.changes()  # line 463
        _.assertEqual(0, len(changes.additions))  # line 464
        _.assertEqual(0, len(changes.deletions))  # line 465
        _.assertEqual(0, len(changes.modifications))  # line 466
        _.createFile(1, "z")  # size change  # line 467
        changes = sos.changes()  # line 468
        _.assertEqual(0, len(changes.additions))  # line 469
        _.assertEqual(0, len(changes.deletions))  # line 470
        _.assertEqual(1, len(changes.modifications))  # line 471
        sos.commit("message")  # line 472
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 473
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 474
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 475
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 476
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 477
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 478
        os.unlink("file2")  # line 479
        changes = sos.changes()  # line 480
        _.assertEqual(0, len(changes.additions))  # line 481
        _.assertEqual(1, len(changes.deletions))  # line 482
        _.assertEqual(1, len(changes.modifications))  # line 483
        sos.commit("modified")  # line 484
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 485
        try:  # expecting Exit due to no changes  # line 486
            sos.commit("nothing")  # expecting Exit due to no changes  # line 486
            _.fail()  # expecting Exit due to no changes  # line 486
        except:  # line 487
            pass  # line 487

    def testGetBranch(_):  # line 489
        m = sos.Metadata(os.getcwd())  # line 490
        m.branch = 1  # current branch  # line 491
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 492
        _.assertEqual(27, m.getBranchByName(27))  # line 493
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 494
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 495
        _.assertIsNone(m.getBranchByName("unknown"))  # line 496
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 497
        _.assertEqual(13, m.getRevisionByName("13"))  # line 498
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 499
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 500

    def testTagging(_):  # line 502
        m = sos.Metadata(os.getcwd())  # line 503
        sos.offline()  # line 504
        _.createFile(111)  # line 505
        sos.commit("tag", ["--tag"])  # line 506
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # type: str  # line 507
        _.assertTrue(any(("|tag" in line and line.endswith("|%sTAG%s" % (sos.Fore.MAGENTA, sos.Fore.RESET)) for line in out)))  # line 508
        _.createFile(2)  # line 509
        try:  # line 510
            sos.commit("tag")  # line 510
            _.fail()  # line 510
        except:  # line 511
            pass  # line 511
        sos.commit("tag-2", ["--tag"])  # line 512
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 513
        _.assertIn("TAG tag", out)  # line 514

    def testSwitch(_):  # line 516
        try:  # line 517
            shutil.rmtree(os.path.join(rmteFolder, sos.metaFolder))  # line 517
        except:  # line 518
            pass  # line 518
        _.createFile(1, "x" * 100)  # line 519
        _.createFile(2, "y")  # line 520
        sos.offline("test", remotes=[rmteFolder])  # file1-2  in initial branch commit  # line 521
        sos.branch("second")  # file1-2  switch, having same files  # line 522
        sos.switch("0")  # no change, switch back, no problem  # line 523
        sos.switch("second")  # no change  # switch back, no problem  # line 524
        _.createFile(3, "y")  # generate a file  # line 525
        try:  # uncommited changes detected  # line 526
            sos.switch("test")  # uncommited changes detected  # line 526
            _.fail()  # uncommited changes detected  # line 526
        except SystemExit as E:  # line 527
            _.assertEqual(1, E.code)  # line 527
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 528
        sos.changes()  # line 529
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 530
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 531
        _.createFile("XXX")  # line 532
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 533
        _.assertIn("File tree has changes", out)  # line 534
        _.assertNotIn("File tree is unchanged", out)  # line 535
        _.assertIn("  * b0   'test'", out)  # line 536
        _.assertIn("    b1 'second'", out)  # line 537
        _.assertIn("modified", out)  # one branch has commits  # line 538
        _.assertIn("in sync", out)  # the other doesn't  # line 539
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 540
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 541
        _.assertAllIn(["Metadata format", "Content checking:    %sSize & timestamp" % sos.Fore.BLUE, "Data compression:    %sdeactivated" % sos.Fore.BLUE, "Repository mode:     %ssimple" % sos.Fore.GREEN, "Number of branches:  2"], out)  # line 542
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 543
        _.createFile(4, "xy")  # generate a file  # line 544
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 545
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 546
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 547
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 548
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 549
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 550
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 551
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 552
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 553
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 554
        _.assertNotIn("Creating backup", out)  # line 555
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 556
        _.assertIn("Dumping revisions", out)  # line 557
        _.assertNotIn("Creating backup", out)  # line 558
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 559
        _.assertAllIn(["Creating backup"], out)  # line 560
        _.assertIn("Dumping revisions", out)  # line 561
        sos.verbose.pop()  # line 562
        _.remoteIsSame()  # line 563
        os.chdir(rmteFolder)  # line 564
        try:  # line 565
            sos.status()  # line 565
        except SystemExit as E:  # line 566
            _.assertEqual(1, E.code)  # line 566

    def testAutoDetectVCS(_):  # line 568
        os.mkdir(".git")  # line 569
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 570
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 571
            meta = fd.read()  # line 571
        _.assertTrue("\"master\"" in meta)  # line 572
        os.rmdir(".git")  # line 573

    def testUpdate(_):  # line 575
        sos.offline("trunk")  # create initial branch b0/r0  # line 576
        _.createFile(1, "x" * 100)  # line 577
        sos.commit("second")  # create b0/r1  # line 578

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 580
        _.assertFalse(_.existsFile(1))  # line 581

        sos.update("/1")  # recreate file1  # line 583
        _.assertTrue(_.existsFile(1))  # line 584

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 586
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 587
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 588
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 589

        sos.update("/1")  # do nothing, as nothing has changed  # line 591
        _.assertTrue(_.existsFile(1))  # line 592

        _.createFile(2, "y" * 100)  # line 594
#    out:str = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 597
        _.assertTrue(_.existsFile(2))  # line 598
        sos.update("trunk", ["--add"])  # only add stuff  # line 599
        _.assertTrue(_.existsFile(2))  # line 600
        sos.update("trunk")  # nothing to do  # line 601
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 602

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 604
        _.createFile(10, theirs)  # line 605
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 606
        _.createFile(11, mine)  # line 607
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 608
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 609

    def testUpdate2(_):  # line 611
        _.createFile("test.txt", "x" * 10)  # line 612
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 613
        sync()  # line 614
        sos.branch("mod")  # line 615
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 616
        sos.commit("mod")  # create b0/r1  # line 617
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 618
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 619
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 620
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 621
        _.createFile("test.txt", "x" * 10)  # line 622
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 623
        sync()  # line 624
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 625
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 626
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 627
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 628
        sync()  # line 629
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 630
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 631

    def testIsTextType(_):  # line 633
        m = sos.Metadata(".")  # line 634
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 635
        m.c.bintype = ["*.md.confluence"]  # line 636
        _.assertTrue(m.isTextType("ab.txt"))  # line 637
        _.assertTrue(m.isTextType("./ab.txt"))  # line 638
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 639
        _.assertFalse(m.isTextType("bc/ab."))  # line 640
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 641
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 642
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 643
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 644

    def testEolDet(_):  # line 646
        ''' Check correct end-of-line detection. '''  # line 647
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 648
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 649
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 650
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 651
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 652
        _.assertIsNone(sos.eoldet(b""))  # line 653
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 654

    def testMergeClassic(_):  # line 656
        _.createFile(1, contents=b"abcdefg")  # line 657
        b = b"iabcxeg"  # type: bytes  # line 658
        _.assertEqual.__self__.maxDiff = None  # to get a full diff  # line 659
        out = wrapChannels(lambda _=None: sos.mergeClassic(b, "file1", "from", "to", 24523234, 1))  # type: str  # line 660
        _.assertAllIn(["*** from\tThu Jan  1 07:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # line 661

    def testMerge(_):  # line 663
        ''' Check merge results depending on user options. '''  # line 664
        a = b"a\nb\ncc\nd"  # type: bytes  # line 665
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 666
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 667
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 668
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 669
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 670
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 671
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 672
        a = b"a\nb\ncc\nd"  # line 673
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 674
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 675
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 676
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 677
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 679
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 680
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 682
        b = b"a\nc\ne"  # line 683
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 684
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 685
        a = b"a\nb\ne"  # intra-line merge  # line 686
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 687
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 688
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 689
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 690
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 691
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 692

    def testMergeEol(_):  # line 694
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 695
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 696
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 697
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 698
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 699

    def testPickyMode(_):  # line 701
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 702
        sos.offline("trunk", None, ["--picky"])  # line 703
        changes = sos.changes()  # line 704
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 705
        out = wrapChannels(lambda _=None: sos.add(".", "./file?", options=["--force", "--relative"]))  # type: str  # line 706
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", "'.'"], out)  # line 707
        _.createFile(1, "aa")  # line 708
        sos.commit("First")  # add one file  # line 709
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 710
        _.createFile(2, "b")  # line 711
        try:  # add nothing, because picky  # line 712
            sos.commit("Second")  # add nothing, because picky  # line 712
        except:  # line 713
            pass  # line 713
        sos.add(".", "./file?")  # line 714
        sos.commit("Third")  # line 715
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 716
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 717
        _.assertIn("    r0", out)  # line 718
        sys.argv.extend(["-n", "2"])  # We cannot use the opions array for named argument options  # line 719
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 720
        sys.argv.pop()  # line 721
        sys.argv.pop()  # line 721
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 722
        _.assertIn("    r1", out)  # line 723
        _.assertIn("  * r2", out)  # line 724
        try:  # line 725
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 725
        except SystemExit as E:  # line 726
            _.assertEqual(0, E.code)  # line 726
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 727
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 728
        _.assertNotIn("    r1", out)  # line 729
        _.assertIn("  * r2", out)  # line 730
        _.createFile(3, prefix="sub")  # line 731
        sos.add("sub", "sub/file?")  # line 732
        changes = sos.changes()  # line 733
        _.assertEqual(1, len(changes.additions))  # line 734
        _.assertTrue("sub/file3" in changes.additions)  # line 735

    def testTrackedSubfolder(_):  # line 737
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 738
        os.mkdir("." + os.sep + "sub")  # line 739
        sos.offline("trunk", None, ["--track"])  # line 740
        _.createFile(1, "x")  # line 741
        _.createFile(1, "x", prefix="sub")  # line 742
        sos.add(".", "./file?")  # add glob pattern to track  # line 743
        sos.commit("First")  # line 744
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 745
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 746
        sos.commit("Second")  # one new file + meta  # line 747
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 748
        os.unlink("file1")  # remove from basefolder  # line 749
        _.createFile(2, "y")  # line 750
        sos.remove(".", "sub/file?")  # line 751
        try:  # TODO check more textual details here  # line 752
            sos.remove(".", "sub/bla")  # TODO check more textual details here  # line 752
            _.fail("Expected exit")  # TODO check more textual details here  # line 752
        except SystemExit as E:  # line 753
            _.assertEqual(1, E.code)  # line 753
        sos.commit("Third")  # line 754
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 755
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 758
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 763
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 764
        _.createFile(1)  # line 765
        _.createFile("a123a")  # untracked file "a123a"  # line 766
        sos.add(".", "./file?")  # add glob tracking pattern  # line 767
        sos.commit("second")  # versions "file1"  # line 768
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 769
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 770
        _.assertTrue(any(("|" in o and "./file?" in o for o in out.split("\n"))))  # line 771

        _.createFile(2)  # untracked file "file2"  # line 773
        sos.commit("third")  # versions "file2"  # line 774
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 775

        os.mkdir("." + os.sep + "sub")  # line 777
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 778
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 779
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 780

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 782
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 783
        sos.add(".", "./a*a")  # add tracking pattern  # line 784
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 785
        _.assertEqual(0, len(changes.modifications))  # line 786
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 787
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 788

        sos.commit("Second_2")  # line 790
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 791
        _.existsFile(1, b"x" * 10)  # line 792
        _.existsFile(2, b"x" * 10)  # line 793

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 795
        _.existsFile(1, b"x" * 10)  # line 796
        _.existsFile("a123a", b"x" * 10)  # line 797

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 799
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 800
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 801

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 803
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 804
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 805
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 806
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 807
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 808
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 809
# TODO test switch --meta

    def testLsTracked(_):  # line 812
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 813
        _.createFile(1)  # line 814
        _.createFile("foo")  # line 815
        sos.add(".", "./file*")  # capture one file  # line 816
        sos.ls()  # line 817
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # type: str  # line 818
        _.assertInAny("TRK file1  (file*)", out)  # line 819
        _.assertNotInAny("... file1  (file*)", out)  # line 820
        _.assertInAny("    foo", out)  # line 821
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 822
        _.assertInAny("TRK file*", out)  # line 823
        _.createFile("a", prefix="sub")  # line 824
        sos.add("sub", "sub/a")  # line 825
        sos.ls("sub")  # line 826
        _.assertInAny("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 827

    def testLineMerge(_):  # line 829
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 830
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 831
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 832
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 833

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 835
        _.createFile(1)  # line 836
        sos.offline("master", options=["--force"])  # line 837
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # type: str  # line 838
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 839
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 840
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 841
        _.createFile(2)  # line 842
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 843
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 844
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 845
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 846

    def testLocalConfig(_):  # line 848
        sos.offline("bla", options=[])  # line 849
        try:  # line 850
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 850
        except SystemExit as E:  # line 851
            _.assertEqual(0, E.code)  # line 851
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 852

    def testConfigVariations(_):  # line 854
        def makeRepo():  # line 855
            try:  # line 856
                os.unlink("file1")  # line 856
            except:  # line 857
                pass  # line 857
            sos.offline("master", options=["--force"])  # line 858
            _.createFile(1)  # line 859
            sos.commit("Added file1")  # line 860
        try:  # line 861
            sos.config(["set", "strict", "on"])  # line 861
        except SystemExit as E:  # line 862
            _.assertEqual(0, E.code)  # line 862
        makeRepo()  # line 863
        _.assertTrue(checkRepoFlag("strict", True))  # line 864
        try:  # line 865
            sos.config(["set", "strict", "off"])  # line 865
        except SystemExit as E:  # line 866
            _.assertEqual(0, E.code)  # line 866
        makeRepo()  # line 867
        _.assertTrue(checkRepoFlag("strict", False))  # line 868
        try:  # line 869
            sos.config(["set", "strict", "yes"])  # line 869
        except SystemExit as E:  # line 870
            _.assertEqual(0, E.code)  # line 870
        makeRepo()  # line 871
        _.assertTrue(checkRepoFlag("strict", True))  # line 872
        try:  # line 873
            sos.config(["set", "strict", "no"])  # line 873
        except SystemExit as E:  # line 874
            _.assertEqual(0, E.code)  # line 874
        makeRepo()  # line 875
        _.assertTrue(checkRepoFlag("strict", False))  # line 876
        try:  # line 877
            sos.config(["set", "strict", "1"])  # line 877
        except SystemExit as E:  # line 878
            _.assertEqual(0, E.code)  # line 878
        makeRepo()  # line 879
        _.assertTrue(checkRepoFlag("strict", True))  # line 880
        try:  # line 881
            sos.config(["set", "strict", "0"])  # line 881
        except SystemExit as E:  # line 882
            _.assertEqual(0, E.code)  # line 882
        makeRepo()  # line 883
        _.assertTrue(checkRepoFlag("strict", False))  # line 884
        try:  # line 885
            sos.config(["set", "strict", "true"])  # line 885
        except SystemExit as E:  # line 886
            _.assertEqual(0, E.code)  # line 886
        makeRepo()  # line 887
        _.assertTrue(checkRepoFlag("strict", True))  # line 888
        try:  # line 889
            sos.config(["set", "strict", "false"])  # line 889
        except SystemExit as E:  # line 890
            _.assertEqual(0, E.code)  # line 890
        makeRepo()  # line 891
        _.assertTrue(checkRepoFlag("strict", False))  # line 892
        try:  # line 893
            sos.config(["set", "strict", "enable"])  # line 893
        except SystemExit as E:  # line 894
            _.assertEqual(0, E.code)  # line 894
        makeRepo()  # line 895
        _.assertTrue(checkRepoFlag("strict", True))  # line 896
        try:  # line 897
            sos.config(["set", "strict", "disable"])  # line 897
        except SystemExit as E:  # line 898
            _.assertEqual(0, E.code)  # line 898
        makeRepo()  # line 899
        _.assertTrue(checkRepoFlag("strict", False))  # line 900
        try:  # line 901
            sos.config(["set", "strict", "enabled"])  # line 901
        except SystemExit as E:  # line 902
            _.assertEqual(0, E.code)  # line 902
        makeRepo()  # line 903
        _.assertTrue(checkRepoFlag("strict", True))  # line 904
        try:  # line 905
            sos.config(["set", "strict", "disabled"])  # line 905
        except SystemExit as E:  # line 906
            _.assertEqual(0, E.code)  # line 906
        makeRepo()  # line 907
        _.assertTrue(checkRepoFlag("strict", False))  # line 908
        try:  # line 909
            sos.config(["set", "strict", "nope"])  # line 909
            _.fail()  # line 909
        except SystemExit as E:  # line 910
            _.assertEqual(1, E.code)  # line 910

    def testLsSimple(_):  # line 912
        _.createFile(1)  # line 913
        _.createFile("foo")  # line 914
        _.createFile("ign1")  # line 915
        _.createFile("ign2")  # line 916
        _.createFile("bar", prefix="sub")  # line 917
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 918
        try:  # define an ignore pattern  # line 919
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern  # line 919
        except SystemExit as E:  # line 920
            _.assertEqual(0, E.code)  # line 920
        try:  # additional ignore pattern  # line 921
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 921
        except SystemExit as E:  # line 922
            _.assertEqual(0, E.code)  # line 922
        try:  # define a list of ignore patterns  # line 923
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 923
        except SystemExit as E:  # line 924
            _.assertEqual(0, E.code)  # line 924
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # type: str  # line 925
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 926
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 927
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 928
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 929
        _.assertInAny('    file1', out)  # line 930
        _.assertInAny('    ign1', out)  # line 931
        _.assertInAny('    ign2', out)  # line 932
        _.assertNotIn('DIR sub', out)  # line 933
        _.assertNotIn('    bar', out)  # line 934
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 935
        _.assertIn('DIR sub', out)  # line 936
        _.assertIn('    bar', out)  # line 937
        try:  # line 938
            sos.config(["rm", "foo", "bar"])  # line 938
            _.fail()  # line 938
        except SystemExit as E:  # line 939
            _.assertEqual(1, E.code)  # line 939
        try:  # line 940
            sos.config(["rm", "ignores", "foo"])  # line 940
            _.fail()  # line 940
        except SystemExit as E:  # line 941
            _.assertEqual(1, E.code)  # line 941
        try:  # line 942
            sos.config(["rm", "ignores", "ign1"])  # line 942
        except SystemExit as E:  # line 943
            _.assertEqual(0, E.code)  # line 943
        try:  # remove ignore pattern  # line 944
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 944
        except SystemExit as E:  # line 945
            _.assertEqual(0, E.code)  # line 945
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 946
        _.assertInAny('    ign1', out)  # line 947
        _.assertInAny('IGN ign2', out)  # line 948
        _.assertNotInAny('    ign2', out)  # line 949

    def testWhitelist(_):  # line 951
# TODO test same for simple mode
        _.createFile(1)  # line 953
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 954
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 955
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 956
        sos.commit(options=["--force"])  # attempt to commit the file  # line 957
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 958
        try:  # Exit because dirty  # line 959
            sos.online()  # Exit because dirty  # line 959
            _.fail()  # Exit because dirty  # line 959
        except:  # exception expected  # line 960
            pass  # exception expected  # line 960
        _.createFile("x2")  # add another change  # line 961
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 962
        try:  # force beyond dirty flag check  # line 963
            sos.online(["--force"])  # force beyond dirty flag check  # line 963
            _.fail()  # force beyond dirty flag check  # line 963
        except:  # line 964
            pass  # line 964
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 965
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 966

        _.createFile(1)  # line 968
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 969
        sos.offline("xx", None, ["--track"])  # line 970
        sos.add(".", "./file*")  # line 971
        sos.commit()  # should NOT ask for force here  # line 972
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 973

    def testRemove(_):  # line 975
        _.createFile(1, "x" * 100)  # line 976
        sos.offline("trunk")  # line 977
        try:  # line 978
            sos.destroy("trunk")  # line 978
            _fail()  # line 978
        except:  # line 979
            pass  # line 979
        _.createFile(2, "y" * 10)  # line 980
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 981
        sos.destroy("trunk")  # line 982
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 983
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 984
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 985
        sos.branch("next")  # line 986
        _.createFile(3, "y" * 10)  # make a change  # line 987
        sos.destroy("added", "--force")  # should succeed  # line 988

    def testFastBranchingOnEmptyHistory(_):  # line 990
        ''' Test fast branching without revisions and with them. '''  # line 991
        sos.offline(options=["--strict", "--compress"])  # b0  # line 992
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 993
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 994
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 995
        sos.destroy("2")  # line 996
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 997
        _.assertIn("b0 'trunk' @", out)  # line 998
        _.assertIn("b1         @", out)  # line 999
        _.assertIn("b3         @", out)  # line 1000
        _.assertNotIn("b2         @", out)  # line 1001
        sos.branch("", "")  # non-fast branching of b4  # line 1002
        _.createFile(1)  # line 1003
        _.createFile(2)  # line 1004
        sos.commit("")  # line 1005
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 1006
        sos.destroy("4")  # line 1007
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 1008
        _.assertIn("b0 'trunk' @", out)  # line 1009
        _.assertIn("b1         @", out)  # line 1010
        _.assertIn("b3         @", out)  # line 1011
        _.assertIn("b5         @", out)  # line 1012
        _.assertNotIn("b2         @", out)  # line 1013
        _.assertNotIn("b4         @", out)  # line 1014
# TODO add more files and branch again

    def testUsage(_):  # line 1017
        try:  # TODO expect sys.exit(0)  # line 1018
            sos.usage()  # TODO expect sys.exit(0)  # line 1018
            _.fail()  # TODO expect sys.exit(0)  # line 1018
        except:  # line 1019
            pass  # line 1019
        try:  # TODO expect sys.exit(0)  # line 1020
            sos.usage("help")  # TODO expect sys.exit(0)  # line 1020
            _.fail()  # TODO expect sys.exit(0)  # line 1020
        except:  # line 1021
            pass  # line 1021
        try:  # TODO expect sys.exit(0)  # line 1022
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 1022
            _.fail()  # TODO expect sys.exit(0)  # line 1022
        except:  # line 1023
            pass  # line 1023
        try:  # line 1024
            sos.usage(version=True)  # line 1024
            _.fail()  # line 1024
        except:  # line 1025
            pass  # line 1025
        try:  # line 1026
            sos.usage(version=True)  # line 1026
            _.fail()  # line 1026
        except:  # line 1027
            pass  # line 1027

    def testOnlyExcept(_):  # line 1029
        ''' Test blacklist glob rules. '''  # line 1030
        sos.offline(options=["--track"])  # line 1031
        _.createFile("a.1")  # line 1032
        _.createFile("a.2")  # line 1033
        _.createFile("b.1")  # line 1034
        _.createFile("b.2")  # line 1035
        sos.add(".", "./a.?")  # line 1036
        sos.add(".", "./?.1", negative=True)  # line 1037
        out = wrapChannels(lambda _=None: sos.commit())  # type: str  # line 1038
        _.assertIn("ADD ./a.2", out)  # line 1039
        _.assertNotIn("ADD ./a.1", out)  # line 1040
        _.assertNotIn("ADD ./b.1", out)  # line 1041
        _.assertNotIn("ADD ./b.2", out)  # line 1042

    def testOnly(_):  # line 1044
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",)), ["bla"]), sos.parseArgumentOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--remote", "bla", "--only"]))  # line 1045
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1046
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1047
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1048
        sos.offline(options=["--track", "--strict"])  # line 1049
        _.createFile(1)  # line 1050
        _.createFile(2)  # line 1051
        sos.add(".", "./file1")  # line 1052
        sos.add(".", "./file2")  # line 1053
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1054
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1055
        sos.commit()  # adds also file2  # line 1056
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1057
        _.createFile(1, "cc")  # modify both files  # line 1058
        _.createFile(2, "dd")  # line 1059
        try:  # line 1060
            sos.config(["set", "texttype", "file2"])  # line 1060
        except SystemExit as E:  # line 1061
            _.assertEqual(0, E.code)  # line 1061
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1062
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1063
        _.assertTrue("./file2" in changes.modifications)  # line 1064
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # line 1065
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1066
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1067
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # line 1068

    def testDiff(_):  # line 1070
        try:  # manually mark this file as "textual"  # line 1071
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1071
        except SystemExit as E:  # line 1072
            _.assertEqual(0, E.code)  # line 1072
        sos.offline(options=["--strict"])  # line 1073
        _.createFile(1)  # line 1074
        _.createFile(2)  # line 1075
        sos.commit()  # line 1076
        _.createFile(1, "sdfsdgfsdf")  # line 1077
        _.createFile(2, "12343")  # line 1078
        sos.commit()  # line 1079
        _.createFile(1, "foobar")  # line 1080
        _.createFile(3)  # line 1081
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # type: str  # compare with r1 (second counting from last which is r2)  # line 1082
        _.assertIn("ADD ./file3", out)  # line 1083
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "-~- 0 |xxxxxxxxxx|", "+~+ 0 |foobar|"], out)  # line 1084
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1085

    def testReorderRenameActions(_):  # line 1087
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1088
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1089
        try:  # line 1090
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1090
            _.fail()  # line 1090
        except:  # line 1091
            pass  # line 1091

    def testPublish(_):  # line 1093
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1094

    def testColorFlag(_):  # line 1096
        sos.offline()  # line 1097
        _.createFile(1)  # line 1098
#    setRepoFlag("useColorOutput", False, toConfig = True)
#    sos.Metadata.singleton = None  # for new read of configuration
        sos.enableColor(False)  # line 1101
        out = wrapChannels(lambda _=None: sos.changes(options="--verbose")).replace("\r\n", "\n").split("\n")  # type: List[str]  # line 1102
        _.assertTrue(any((line.startswith(sos.usage.MARKER_TEXT + "Changes of file tree") for line in out)))  # line 1103
#    setRepoFlag("useColorOutput", True,  toConfig = True)
#    sos.Metadata.singleton = None
        sos.enableColor(True)  # line 1106
        out = wrapChannels(lambda _=None: sos.changes(options="--verbose")).replace("\r\n", "\n").split("\n")  # line 1107
        _.assertTrue(any((line.startswith(sos.utility.MARKER_COLOR + "Changes of file tree") for line in out)))  # because it may start with a color code  # line 1108

    def testMove(_):  # line 1110
        ''' Move primarily modifies tracking patterns and moves files around accordingly. '''  # line 1111
        sos.offline(options=["--strict", "--track"])  # line 1112
        _.createFile(1)  # line 1113
        sos.add(".", "./file?")  # line 1114
# assert error when source folder is missing
        out = wrapChannels(lambda _=None: sos.move("sub", "sub/file?", ".", "./?file"))  # type: str  # line 1116
        _.assertIn("Source folder doesn't exist", out)  # line 1117
        _.assertIn("EXIT CODE 1", out)  # line 1118
# if target folder missing: create it and move matching files into it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1120
        _.assertTrue(os.path.exists("sub"))  # line 1121
        _.assertTrue(os.path.exists("sub/file1"))  # line 1122
        _.assertFalse(os.path.exists("file1"))  # line 1123
# test move back to previous location, plus rename the file
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1125
        _.assertTrue(os.path.exists("1file"))  # line 1126
        _.assertFalse(os.path.exists("sub/file1"))  # line 1127
# assert error when nothing matches source pattern
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*"))  # line 1129
        _.assertIn("No files match the specified file pattern", out)  # line 1130
        _.assertIn("EXIT CODE", out)  # line 1131
        sos.add(".", "./*")  # add catch-all tracking pattern to root folder  # line 1132
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*", options=["--force"]))  # line 1133
        _.assertIn("  './*' matches 3 files", out)  # line 1134
        _.assertIn("EXIT CODE", out)  # line 1135
# test rename no conflict
        _.createFile(1)  # line 1137
        _.createFile(2)  # line 1138
        _.createFile(3)  # line 1139
        sos.add(".", "./file*")  # line 1140
        sos.remove(".", "./*")  # line 1141
        try:  # define an ignore pattern  # line 1142
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1142
        except SystemExit as E:  # line 1143
            _.assertEqual(0, E.code)  # line 1143
        try:  # line 1144
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1144
        except SystemExit as E:  # line 1145
            _.assertEqual(0, E.code)  # line 1145
        sos.move(".", "./file*", ".", "./fi*le")  # should only move not ignored files files  # line 1146
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1147
        _.assertTrue(all((not os.path.exists("file%d" % i) for i in range(1, 4))))  # line 1148
        _.assertFalse(os.path.exists("fi4le"))  # line 1149
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1151
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # untrack pattern, which was renamed before  # line 1155
        sos.add(".", "./?a?b", ["--force"])  # line 1156
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1157
        _.createFile("1a2b")  # should not be tracked  # line 1158
        _.createFile("a1b2")  # should be tracked  # line 1159
        sos.commit()  # line 1160
        _.assertEqual(5, len(os.listdir(sos.revisionFolder(0, 1))))  # meta, a1b2, fi[1-3]le  # line 1161
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1162
        _.createFile("1a1b1")  # line 1163
        _.createFile("1a1b2")  # line 1164
        sos.add(".", "./?a?b*")  # line 1165
# test target pattern exists
        out = wrapChannels(lambda _=None: sos.move(".", "./?a?b*", ".", "./z?z?"))  # line 1167
        _.assertIn("not unique", out)  # line 1168
# TODO only rename if actually any files are versioned? or simply what is currently alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1172
        _.createFile(1)  # line 1173
        _.createFile(3)  # line 1174
        _.createFile(5)  # line 1175
        sos.offline()  # branch 0: only file1  # line 1176
        sos.branch()  # line 1177
        os.unlink("file1")  # line 1178
        os.unlink("file3")  # line 1179
        os.unlink("file5")  # line 1180
        _.createFile(2)  # line 1181
        _.createFile(4)  # line 1182
        _.createFile(6)  # line 1183
        sos.commit()  # branch 1: only file2  # line 1184
        sos.switch("0/")  # line 1185
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1186
        _.assertFalse(_.existsFile(1))  # line 1187
        _.assertFalse(_.existsFile(3))  # line 1188
        _.assertFalse(_.existsFile(5))  # line 1189
        _.assertTrue(_.existsFile(2))  # line 1190
        _.assertTrue(_.existsFile(4))  # line 1191
        _.assertTrue(_.existsFile(6))  # line 1192

    def testMoveDetection(_):  # line 1194
        _.createFile(1, "bla")  # line 1195
        sos.offline()  # line 1196
        os.mkdir("sub1")  # line 1197
        os.mkdir("sub2")  # line 1198
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1199
        shutil.move("file1", "sub2")  # line 1200
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 1201
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1202
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1203
        sos.commit("Moved the file")  # line 1204
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1208

    def testHashCollision(_):  # line 1210
        old = sos.Metadata.findChanges  # line 1211
        @_coconut_tco  # line 1212
        def patched(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[sos.ChangeSet, _coconut.typing.Optional[str]]':  # line 1212
            import collections  # used only in this method  # line 1213
            write = branch is not None and revision is not None  # line 1214
            if write:  # line 1215
                try:  # line 1216
                    os.makedirs(sos.encode(sos.revisionFolder(branch, revision, base=_.root)))  # line 1216
                except FileExistsError:  # HINT "try" only necessary for hash collision *test code* (!)  # line 1217
                    pass  # HINT "try" only necessary for hash collision *test code* (!)  # line 1217
            return _coconut_tail_call(old, _, branch, revision, checkContent, inverse, considerOnly, dontConsider, progress)  # line 1218
        sos.Metadata.findChanges = patched  # monkey-patch  # line 1219
        sos.offline()  # line 1220
        _.createFile(1)  # line 1221
        os.mkdir(sos.revisionFolder(0, 1))  # line 1222
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # hashed file name for not-yet-committed file1  # line 1223
        _.createFile(1)  # line 1224
        try:  # line 1225
            sos.commit()  # line 1225
            _.fail("Expected system exit due to hash collision detection")  # line 1225
        except SystemExit as E:  # HINT exit is implemented in utility.hashFile  # line 1226
            _.assertEqual(1, E.code)  # HINT exit is implemented in utility.hashFile  # line 1226
        sos.Metadata.findChanges = old  # revert monkey patch  # line 1227

    def testFindBase(_):  # line 1229
        old = os.getcwd()  # line 1230
        try:  # line 1231
            os.mkdir("." + os.sep + ".git")  # line 1232
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1233
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1234
            os.chdir("a" + os.sep + "b")  # line 1235
            s, vcs, cmd = sos.findSosVcsBase()  # line 1236
            _.assertIsNotNone(s)  # line 1237
            _.assertIsNotNone(vcs)  # line 1238
            _.assertEqual("git", cmd)  # line 1239
        finally:  # line 1240
            os.chdir(old)  # line 1240

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1251
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1252
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1253
