#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xbf038a14

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
        a = sos.Accessor({"a": 1})  # line 155
        _.assertEqual((1, 1), (a["a"], a.a))  # line 156

    def testUnzip(_):  # line 158
        a = zip([1, 2, 3], ["a", "b", "c"])  # type: _coconut.typing.Sequence[Tuple[int, str]]  # line 159
        i = None  # type: Tuple[int]  # line 160
        c = None  # type: Tuple[str]  # line 160
        i, c = sos.unzip(a)  # line 161
        _.assertEqual((1, 2, 3), i)  # line 162
        _.assertEqual(("a", "b", "c"), c)  # line 163

    def testIndexing(_):  # line 165
        m = sos.Metadata()  # line 166
        m.commits = {}  # line 167
        _.assertEqual(1, m.correctNegativeIndexing(1))  # line 168
        _.assertEqual(9999999999999999, m.correctNegativeIndexing(9999999999999999))  # line 169
        _.assertEqual(0, m.correctNegativeIndexing(0))  # zero always returns zero, even no commits present  # line 170
        try:  # line 171
            m.correctNegativeIndexing(-1)  # line 171
            _.fail()  # line 171
        except SystemExit as E:  # line 172
            _.assertEqual(1, E.code)  # line 172
        m.commits = {0: sos.CommitInfo(0, 0), 1: sos.CommitInfo(1, 0)}  # line 173
        _.assertEqual(1, m.correctNegativeIndexing(-1))  # zero always returns zero, even no commits present  # line 174
        _.assertEqual(0, m.correctNegativeIndexing(-2))  # zero always returns zero, even no commits present  # line 175
        try:  # line 176
            m.correctNegativeIndexing(-3)  # line 176
            _.fail()  # line 176
        except SystemExit as E:  # line 177
            _.assertEqual(1, E.code)  # line 177

    def testRestoreFile(_):  # line 179
        m = sos.Metadata()  # line 180
        os.makedirs(sos.revisionFolder(0, 0))  # line 181
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 182
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 183
        _.assertTrue(_.existsFile("restored", b""))  # line 184

    def testGetAnyOfmap(_):  # line 186
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 187
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 188

    def testAjoin(_):  # line 190
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 191
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 192

    def testFindChanges(_):  # line 194
        m = sos.Metadata(os.getcwd())  # line 195
        try:  # line 196
            sos.config(["set", "texttype", "*"])  # line 196
        except SystemExit as E:  # line 197
            _.assertEqual(0, E.code)  # line 197
        try:  # will be stripped from leading paths anyway  # line 198
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 198
        except SystemExit as E:  # line 199
            _.assertEqual(0, E.code)  # line 199
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 200
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 201
            os.unlink(file)  # remove configuration file  # line 201
        _.createFile(9, b"")  # line 202
        _.createFile(1, "1")  # line 203
        m.createBranch(0)  # line 204
        _.assertEqual(2, len(m.paths))  # line 205
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 206
        _.createFile(1, "2")  # modify existing file  # line 207
        _.createFile(2, "2")  # add another file  # line 208
        m.loadCommit(0, 0)  # line 209
        changes, msg = m.findChanges()  # detect time skew  # line 210
        _.assertEqual(1, len(changes.additions))  # line 211
        _.assertEqual(0, len(changes.deletions))  # line 212
        _.assertEqual(1, len(changes.modifications))  # line 213
        _.assertEqual(0, len(changes.moves))  # line 214
        m.paths.update(changes.additions)  # line 215
        m.paths.update(changes.modifications)  # line 216
        _.createFile(2, "12")  # modify file again  # line 217
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 218
        _.assertEqual(0, len(changes.additions))  # line 219
        _.assertEqual(0, len(changes.deletions))  # line 220
        _.assertEqual(1, len(changes.modifications))  # line 221
        _.assertEqual(0, len(changes.moves))  # line 222
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 223
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 224
# TODO test moves

    def testDumpSorting(_):  # line 227
        m = sos.Metadata()  # type: Metadata  # line 228
        _.createFile(1)  # line 229
        sos.offline()  # line 230
        _.createFile(2)  # line 231
        _.createFile(3)  # line 232
        sos.commit()  # line 233
        _.createFile(4)  # line 234
        _.createFile(5)  # line 235
        sos.commit()  # line 236
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # type: List[str]  # line 237
        _.assertTrue(out.index("b0%sr2" % os.sep) > out.index("b0%sr1" % os.sep))  # line 238
        _.assertTrue(out.index("b0%sr1" % os.sep) > out.index("b0%sr0" % os.sep))  # line 239

    def testFitStrings(_):  # line 241
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 242
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 243
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 244
    def testMoves(_):  # line 245
        _.createFile(1, "1")  # line 246
        _.createFile(2, "2", "sub")  # line 247
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 248
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 249
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 250
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 251
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 252
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 253
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # line 254
        _.assertIn("MOV ..%sfile2  <-  file2" % os.sep, out)  # no ./ for relative OS-specific paths  # line 255
        _.assertIn("MOV file1  <-  ..%sfile1" % os.sep, out)  # line 256
        out = wrapChannels(lambda _=None: sos.commit())  # line 257
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 258
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 259
        _.assertAllIn(["Created new revision r01", "summing 628 bytes in 2 files (88.22% SOS overhead)"], out)  # TODO why is this not captured?  # line 260

    def testPatternPaths(_):  # line 262
        sos.offline(options=["--track"])  # line 263
        os.mkdir("sub")  # line 264
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 265
        out = wrapChannels(lambda _=None: sos.add(["sub"], ["sub/file?"]))  # type: str  # line 266
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", os.path.abspath("sub")], out)  # line 267
        sos.commit("test")  # should pick up sub/file1 pattern  # line 268
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 269
        _.createFile(1)  # line 270
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 271
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 271
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 271
        except:  # line 272
            pass  # line 272

    def testNoArgs(_):  # line 274
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 275

    def testAutoMetadataUpgrade(_):  # line 277
        sos.offline()  # line 278
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 279
            repo, branches, config = json.load(fd)  # line 279
        repo["version"] = None  # lower than any pip version  # line 280
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 281
        del repo["format"]  # simulate pre-1.3.5  # line 282
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 283
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 283
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # type: str  # line 284
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 285

    def testFastBranching(_):  # line 287
        _.createFile(1)  # line 288
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict", "--verbose"]))  # type: str  # b0/r0 = ./file1  # line 289
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 290
        _.createFile(2)  # line 291
        os.unlink("file1")  # line 292
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 293
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 294
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 295
        _.createFile(3)  # line 296
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 297
        _.assertAllIn([sos.metaFile, sos.metaBack, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 298
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 299
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 300
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 301
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 302
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 303
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 306
        now = time.time()  # type: float  # line 307
        _.createFile(1)  # line 308
        sync()  # line 309
        sos.offline(options=["--strict"])  # line 310
        _.createFile(1, "abc")  # modify contents  # line 311
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 312
        sync()  # line 313
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 314
        _.assertIn("<older than previously committed>", out)  # line 315
        out = wrapChannels(lambda _=None: sos.commit())  # line 316
        _.assertIn("<older than previously committed>", out)  # line 317

    def testGetParentBranch(_):  # line 319
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 320
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 321
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 322
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 323
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 324

    def testTokenizeGlobPattern(_):  # line 326
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 327
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 328
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 329
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 330
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 331
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 332

    def testTokenizeGlobPatterns(_):  # line 334
        try:  # because number of literal strings differs  # line 335
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 335
            _.fail()  # because number of literal strings differs  # line 335
        except:  # line 336
            pass  # line 336
        try:  # because glob patterns differ  # line 337
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 337
            _.fail()  # because glob patterns differ  # line 337
        except:  # line 338
            pass  # line 338
        try:  # glob patterns differ, regardless of position  # line 339
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 339
            _.fail()  # glob patterns differ, regardless of position  # line 339
        except:  # line 340
            pass  # line 340
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 341
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 342
        try:  # succeeds, because glob patterns match (differ only in position)  # line 343
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 343
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 343
        except:  # line 344
            pass  # line 344

    def testConvertGlobFiles(_):  # line 346
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 347
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 348

    def testFolderRemove(_):  # line 350
        m = sos.Metadata(os.getcwd())  # line 351
        _.createFile(1)  # line 352
        _.createFile("a", prefix="sub")  # line 353
        sos.offline()  # line 354
        _.createFile(2)  # line 355
        os.unlink("sub" + os.sep + "a")  # line 356
        os.rmdir("sub")  # line 357
        changes = sos.changes()  # TODO #254 replace by output check  # line 358
        _.assertEqual(1, len(changes.additions))  # line 359
        _.assertEqual(0, len(changes.modifications))  # line 360
        _.assertEqual(1, len(changes.deletions))  # line 361
        _.createFile("a", prefix="sub")  # line 362
        changes = sos.changes()  # line 363
        _.assertEqual(0, len(changes.deletions))  # line 364

    def testSwitchConflict(_):  # line 366
        sos.offline(options=["--strict"])  # (r0)  # line 367
        _.createFile(1)  # line 368
        sos.commit()  # add file (r1)  # line 369
        os.unlink("file1")  # line 370
        sos.commit()  # remove (r2)  # line 371
        _.createFile(1, "something else")  # line 372
        sos.commit()  # (r3)  # line 373
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 374
        _.existsFile(1, "x" * 10)  # line 375
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 376
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 377
        sos.switch("/1")  # add file1 back  # line 378
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 379
        _.existsFile(1, "something else")  # line 380

    def testComputeSequentialPathSet(_):  # line 382
        os.makedirs(sos.revisionFolder(0, 0))  # line 383
        os.makedirs(sos.revisionFolder(0, 1))  # line 384
        os.makedirs(sos.revisionFolder(0, 2))  # line 385
        os.makedirs(sos.revisionFolder(0, 3))  # line 386
        os.makedirs(sos.revisionFolder(0, 4))  # line 387
        m = sos.Metadata(os.getcwd())  # line 388
        m.branch = 0  # line 389
        m.commit = 2  # line 390
        m.saveBranches()  # line 391
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 392
        m.saveCommit(0, 0)  # initial  # line 393
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 394
        m.saveCommit(0, 1)  # mod  # line 395
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 396
        m.saveCommit(0, 2)  # add  # line 397
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 398
        m.saveCommit(0, 3)  # del  # line 399
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 400
        m.saveCommit(0, 4)  # readd  # line 401
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 402
        m.saveBranch(0)  # line 403
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 404
        m.saveBranches()  # line 405
        m.computeSequentialPathSet(0, 4)  # line 406
        _.assertEqual(2, len(m.paths))  # line 407

    def testParseRevisionString(_):  # line 409
        m = sos.Metadata(os.getcwd())  # line 410
        m.branch = 1  # line 411
        m.commits = {0: 0, 1: 1, 2: 2}  # line 412
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 413
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 414
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 415
        _.assertEqual((None, None), m.parseRevisionString(""))  # line 416
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 417
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 418
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 419

    def testOfflineEmpty(_):  # line 421
        os.mkdir("." + os.sep + sos.metaFolder)  # line 422
        try:  # line 423
            sos.offline("trunk")  # line 423
            _.fail()  # line 423
        except SystemExit as E:  # line 424
            _.assertEqual(1, E.code)  # line 424
        os.rmdir("." + os.sep + sos.metaFolder)  # line 425
        sos.offline("test")  # line 426
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 427
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 428
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 429
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 430
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 431
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 432

    def testOfflineWithFiles(_):  # line 434
        _.createFile(1, "x" * 100)  # line 435
        _.createFile(2)  # line 436
        sos.offline("test")  # line 437
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 438
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 439
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 440
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 441
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 442
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 443
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 444

    def testBranch(_):  # line 446
        _.createFile(1, "x" * 100)  # line 447
        _.createFile(2)  # line 448
        sos.offline("test")  # b0/r0  # line 449
        sos.branch("other")  # b1/r0  # line 450
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 451
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 452
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 454
        _.createFile(1, "z")  # modify file  # line 456
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 457
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 458
        _.createFile(3, "z")  # line 460
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 461
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 462
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 467
        _.createFile(1, "x" * 100)  # line 468
        _.createFile(2)  # line 469
        sos.offline("test")  # line 470
        changes = sos.changes()  # line 471
        _.assertEqual(0, len(changes.additions))  # line 472
        _.assertEqual(0, len(changes.deletions))  # line 473
        _.assertEqual(0, len(changes.modifications))  # line 474
        _.createFile(1, "z")  # size change  # line 475
        changes = sos.changes()  # line 476
        _.assertEqual(0, len(changes.additions))  # line 477
        _.assertEqual(0, len(changes.deletions))  # line 478
        _.assertEqual(1, len(changes.modifications))  # line 479
        sos.commit("message")  # line 480
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 481
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 482
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 483
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 484
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 485
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 486
        os.unlink("file2")  # line 487
        changes = sos.changes()  # line 488
        _.assertEqual(0, len(changes.additions))  # line 489
        _.assertEqual(1, len(changes.deletions))  # line 490
        _.assertEqual(1, len(changes.modifications))  # line 491
        sos.commit("modified")  # line 492
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 493
        try:  # expecting Exit due to no changes  # line 494
            sos.commit("nothing")  # expecting Exit due to no changes  # line 494
            _.fail()  # expecting Exit due to no changes  # line 494
        except:  # line 495
            pass  # line 495

    def testGetBranch(_):  # line 497
        m = sos.Metadata(os.getcwd())  # line 498
        m.branch = 1  # current branch  # line 499
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 500
        _.assertEqual(27, m.getBranchByName(27))  # line 501
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 502
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 503
        _.assertIsNone(m.getBranchByName("unknown"))  # line 504
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 505
        _.assertEqual(13, m.getRevisionByName("13"))  # line 506
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 507
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 508

    def testTagging(_):  # line 510
        m = sos.Metadata(os.getcwd())  # line 511
        sos.offline()  # line 512
        _.createFile(111)  # line 513
        sos.commit("tag", ["--tag"])  # line 514
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # type: str  # line 515
        _.assertTrue(any(("|tag" in line and line.endswith("|%sTAG%s" % (sos.Fore.MAGENTA, sos.Fore.RESET)) for line in out)))  # line 516
        _.createFile(2)  # line 517
        try:  # line 518
            sos.commit("tag")  # line 518
            _.fail()  # line 518
        except:  # line 519
            pass  # line 519
        sos.commit("tag-2", ["--tag"])  # line 520
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 521
        _.assertIn("TAG tag", out)  # line 522

    def testSwitch(_):  # line 524
        try:  # line 525
            shutil.rmtree(os.path.join(rmteFolder, sos.metaFolder))  # line 525
        except:  # line 526
            pass  # line 526
        _.createFile(1, "x" * 100)  # line 527
        _.createFile(2, "y")  # line 528
        sos.offline("test", remotes=[rmteFolder])  # file1-2  in initial branch commit  # line 529
        sos.branch("second")  # file1-2  switch, having same files  # line 530
        sos.switch("0")  # no change, switch back, no problem  # line 531
        sos.switch("second")  # no change  # switch back, no problem  # line 532
        _.createFile(3, "y")  # generate a file  # line 533
        try:  # uncommited changes detected  # line 534
            sos.switch("test")  # uncommited changes detected  # line 534
            _.fail()  # uncommited changes detected  # line 534
        except SystemExit as E:  # line 535
            _.assertEqual(1, E.code)  # line 535
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 536
        sos.changes()  # line 537
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 538
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 539
        _.createFile("XXX")  # line 540
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 541
        _.assertIn("File tree has changes", out)  # line 542
        _.assertNotIn("File tree is unchanged", out)  # line 543
        _.assertIn("  * b0   'test'", out)  # line 544
        _.assertIn("    b1 'second'", out)  # line 545
        _.assertIn("modified", out)  # one branch has commits  # line 546
        _.assertIn("in sync", out)  # the other doesn't  # line 547
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 548
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 549
        _.assertAllIn(["Metadata format", "Content checking:    %ssize & timestamp" % sos.Fore.BLUE, "Data compression:    %sdeactivated" % sos.Fore.BLUE, "Repository mode:     %ssimple" % sos.Fore.GREEN, "Number of branches:  2"], out)  # line 550
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 551
        _.createFile(4, "xy")  # generate a file  # line 552
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 553
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 554
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 555
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 556
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 557
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 558
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 559
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 560
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 561
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 562
        _.assertNotIn("Creating backup", out)  # line 563
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 564
        _.assertIn("Dumping revisions", out)  # line 565
        _.assertNotIn("Creating backup", out)  # line 566
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 567
        _.assertAllIn(["Creating backup"], out)  # line 568
        _.assertIn("Dumping revisions", out)  # line 569
        sos.verbose.pop()  # line 570
        _.remoteIsSame()  # line 571
        os.chdir(rmteFolder)  # line 572
        try:  # line 573
            sos.status()  # line 573
        except SystemExit as E:  # line 574
            _.assertEqual(1, E.code)  # line 574

    def testAutoDetectVCS(_):  # line 576
        os.mkdir(".git")  # line 577
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 578
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 579
            meta = fd.read()  # line 579
        _.assertTrue("\"master\"" in meta)  # line 580
        os.rmdir(".git")  # line 581

    def testUpdate(_):  # line 583
        sos.offline("trunk")  # create initial branch b0/r0  # line 584
        _.createFile(1, "x" * 100)  # line 585
        sos.commit("second")  # create b0/r1  # line 586

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 588
        _.assertFalse(_.existsFile(1))  # line 589

        sos.update("/1")  # recreate file1  # line 591
        _.assertTrue(_.existsFile(1))  # line 592

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 594
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 595
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 596
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 597

        sos.update("/1")  # do nothing, as nothing has changed  # line 599
        _.assertTrue(_.existsFile(1))  # line 600

        _.createFile(2, "y" * 100)  # line 602
#    out:str = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 605
        _.assertTrue(_.existsFile(2))  # line 606
        sos.update("trunk", ["--add"])  # only add stuff  # line 607
        _.assertTrue(_.existsFile(2))  # line 608
        sos.update("trunk")  # nothing to do  # line 609
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 610

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 612
        _.createFile(10, theirs)  # line 613
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 614
        _.createFile(11, mine)  # line 615
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 616
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 617

    def testUpdate2(_):  # line 619
        _.createFile("test.txt", "x" * 10)  # line 620
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 621
        sync()  # line 622
        sos.branch("mod")  # line 623
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 624
        sos.commit("mod")  # create b0/r1  # line 625
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 626
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 627
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 628
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 629
        _.createFile("test.txt", "x" * 10)  # line 630
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 631
        sync()  # line 632
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 633
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 634
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 635
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 636
        sync()  # line 637
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 638
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 639

    def testIsTextType(_):  # line 641
        m = sos.Metadata(".")  # line 642
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 643
        m.c.bintype = ["*.md.confluence"]  # line 644
        _.assertTrue(m.isTextType("ab.txt"))  # line 645
        _.assertTrue(m.isTextType("./ab.txt"))  # line 646
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 647
        _.assertFalse(m.isTextType("bc/ab."))  # line 648
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 649
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 650
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 651
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 652

    def testEolDet(_):  # line 654
        ''' Check correct end-of-line detection. '''  # line 655
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 656
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 657
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 658
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 659
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 660
        _.assertIsNone(sos.eoldet(b""))  # line 661
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 662

    def testMergeClassic(_):  # line 664
        _.createFile(1, contents=b"abcdefg")  # line 665
        b = b"iabcxeg"  # type: bytes  # line 666
        _.assertEqual.__self__.maxDiff = None  # to get a full diff  # line 667
        out = wrapChannels(lambda _=None: sos.mergeClassic(b, "file1", "from", "to", 24523234, 1))  # type: str  # line 668
        try:  # line 669
            _.assertAllIn(["*** from\tThu Jan  1 07:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # line 669
        except:  # differing local time on CI system TODO make this better  # line 670
            _.assertAllIn(["*** from\tThu Jan  1 06:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # differing local time on CI system TODO make this better  # line 670

    def testMerge(_):  # line 672
        ''' Check merge results depending on user options. '''  # line 673
        a = b"a\nb\ncc\nd"  # type: bytes  # line 674
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 675
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 676
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 677
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 678
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 679
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 680
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 681
        a = b"a\nb\ncc\nd"  # line 682
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 683
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 684
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 685
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 686
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 688
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 689
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 691
        b = b"a\nc\ne"  # line 692
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 693
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 694
        a = b"a\nb\ne"  # intra-line merge  # line 695
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 696
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 697
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 698
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 699
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 700
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 701

    def testMergeEol(_):  # line 703
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 704
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 705
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 706
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 707
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 708

    def testPickyMode(_):  # line 710
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 711
        sos.offline("trunk", None, ["--picky"])  # line 712
        changes = sos.changes()  # line 713
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 714
        out = wrapChannels(lambda _=None: sos.add(["."], ["./file?"], options=["--force", "--relative"]))  # type: str  # line 715
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", "'.'"], out)  # line 716
        _.createFile(1, "aa")  # line 717
        sos.commit("First")  # add one file  # line 718
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 719
        _.createFile(2, "b")  # line 720
        try:  # add nothing, because picky  # line 721
            sos.commit("Second")  # add nothing, because picky  # line 721
        except:  # line 722
            pass  # line 722
        sos.add(["."], ["./file?"])  # line 723
        sos.commit("Third")  # line 724
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 725
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 726
        _.assertIn("    r0", out)  # line 727
        sys.argv.extend(["-n", "2"])  # We cannot use the opions array for named argument options  # line 728
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 729
        sys.argv.pop()  # line 730
        sys.argv.pop()  # line 730
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 731
        _.assertIn("    r1", out)  # line 732
        _.assertIn("  * r2", out)  # line 733
        try:  # line 734
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 734
        except SystemExit as E:  # line 735
            _.assertEqual(0, E.code)  # line 735
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 736
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 737
        _.assertNotIn("    r1", out)  # line 738
        _.assertIn("  * r2", out)  # line 739
        _.createFile(3, prefix="sub")  # line 740
        sos.add(["sub"], ["sub/file?"])  # line 741
        changes = sos.changes()  # line 742
        _.assertEqual(1, len(changes.additions))  # line 743
        _.assertTrue("sub/file3" in changes.additions)  # line 744

    def testTrackedSubfolder(_):  # line 746
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 747
        os.mkdir("." + os.sep + "sub")  # line 748
        sos.offline("trunk", None, ["--track"])  # line 749
        _.createFile(1, "x")  # line 750
        _.createFile(1, "x", prefix="sub")  # line 751
        sos.add(["."], ["./file?"])  # add glob pattern to track  # line 752
        sos.commit("First")  # line 753
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 754
        sos.add(["."], ["sub/file?"])  # add glob pattern to track  # line 755
        sos.commit("Second")  # one new file + meta  # line 756
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 757
        os.unlink("file1")  # remove from basefolder  # line 758
        _.createFile(2, "y")  # line 759
        sos.remove(["."], ["sub/file?"])  # line 760
        try:  # TODO check more textual details here  # line 761
            sos.remove(["."], ["sub/bla"])  # TODO check more textual details here  # line 761
            _.fail("Expected exit")  # TODO check more textual details here  # line 761
        except SystemExit as E:  # line 762
            _.assertEqual(1, E.code)  # line 762
        sos.commit("Third")  # line 763
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 764
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 767
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 772
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 773
        _.createFile(1)  # line 774
        _.createFile("a123a")  # untracked file "a123a"  # line 775
        sos.add(["."], ["./file?"])  # add glob tracking pattern  # line 776
        sos.commit("second")  # versions "file1"  # line 777
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 778
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 779
        _.assertTrue(any(("|" in o and "./file?" in o for o in out.split("\n"))))  # line 780

        _.createFile(2)  # untracked file "file2"  # line 782
        sos.commit("third")  # versions "file2"  # line 783
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 784

        os.mkdir("." + os.sep + "sub")  # line 786
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 787
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 788
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 789

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 791
        sos.remove(["."], ["./file?"])  # remove tracking pattern, but don't touch previously created and versioned files  # line 792
        sos.add([".", "."], ["./a*a", "./a*?"])  # add tracking pattern  # line 793
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 794
        _.assertEqual(0, len(changes.modifications))  # line 795
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 796
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 797

        sos.commit("Second_2")  # line 799
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 800
        _.existsFile(1, b"x" * 10)  # line 801
        _.existsFile(2, b"x" * 10)  # line 802

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 804
        _.existsFile(1, b"x" * 10)  # line 805
        _.existsFile("a123a", b"x" * 10)  # line 806

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 808
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 809
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 810

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 812
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 813
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 814
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 815
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 816
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 817
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 818
# TODO test switch --meta

    def testLsTracked(_):  # line 821
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 822
        _.createFile(1)  # line 823
        _.createFile("foo")  # line 824
        sos.add(["."], ["./file*"])  # capture one file  # line 825
        sos.ls()  # line 826
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # type: str  # line 827
        _.assertInAny("TRK file1  (file*)", out)  # line 828
        _.assertNotInAny("... file1  (file*)", out)  # line 829
        _.assertInAny("    foo", out)  # line 830
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 831
        _.assertInAny("TRK file*", out)  # line 832
        _.createFile("a", prefix="sub")  # line 833
        sos.add(["sub"], ["sub/a"])  # line 834
        sos.ls("sub")  # line 835
        _.assertInAny("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 836

    def testLineMerge(_):  # line 838
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 839
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 840
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 841
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 842

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 844
        _.createFile(1)  # line 845
        sos.offline("master", options=["--force"])  # line 846
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # type: str  # line 847
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 848
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 849
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 850
        _.createFile(2)  # line 851
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 852
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 853
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 854
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 855

    def testLocalConfig(_):  # line 857
        sos.offline("bla", options=[])  # line 858
        try:  # line 859
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 859
        except SystemExit as E:  # line 860
            _.assertEqual(0, E.code)  # line 860
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 861

    def testConfigVariations(_):  # line 863
        def makeRepo():  # line 864
            try:  # line 865
                os.unlink("file1")  # line 865
            except:  # line 866
                pass  # line 866
            sos.offline("master", options=["--force"])  # line 867
            _.createFile(1)  # line 868
            sos.commit("Added file1")  # line 869
        try:  # line 870
            sos.config(["set", "strict", "on"])  # line 870
        except SystemExit as E:  # line 871
            _.assertEqual(0, E.code)  # line 871
        makeRepo()  # line 872
        _.assertTrue(checkRepoFlag("strict", True))  # line 873
        try:  # line 874
            sos.config(["set", "strict", "off"])  # line 874
        except SystemExit as E:  # line 875
            _.assertEqual(0, E.code)  # line 875
        makeRepo()  # line 876
        _.assertTrue(checkRepoFlag("strict", False))  # line 877
        try:  # line 878
            sos.config(["set", "strict", "yes"])  # line 878
        except SystemExit as E:  # line 879
            _.assertEqual(0, E.code)  # line 879
        makeRepo()  # line 880
        _.assertTrue(checkRepoFlag("strict", True))  # line 881
        try:  # line 882
            sos.config(["set", "strict", "no"])  # line 882
        except SystemExit as E:  # line 883
            _.assertEqual(0, E.code)  # line 883
        makeRepo()  # line 884
        _.assertTrue(checkRepoFlag("strict", False))  # line 885
        try:  # line 886
            sos.config(["set", "strict", "1"])  # line 886
        except SystemExit as E:  # line 887
            _.assertEqual(0, E.code)  # line 887
        makeRepo()  # line 888
        _.assertTrue(checkRepoFlag("strict", True))  # line 889
        try:  # line 890
            sos.config(["set", "strict", "0"])  # line 890
        except SystemExit as E:  # line 891
            _.assertEqual(0, E.code)  # line 891
        makeRepo()  # line 892
        _.assertTrue(checkRepoFlag("strict", False))  # line 893
        try:  # line 894
            sos.config(["set", "strict", "true"])  # line 894
        except SystemExit as E:  # line 895
            _.assertEqual(0, E.code)  # line 895
        makeRepo()  # line 896
        _.assertTrue(checkRepoFlag("strict", True))  # line 897
        try:  # line 898
            sos.config(["set", "strict", "false"])  # line 898
        except SystemExit as E:  # line 899
            _.assertEqual(0, E.code)  # line 899
        makeRepo()  # line 900
        _.assertTrue(checkRepoFlag("strict", False))  # line 901
        try:  # line 902
            sos.config(["set", "strict", "enable"])  # line 902
        except SystemExit as E:  # line 903
            _.assertEqual(0, E.code)  # line 903
        makeRepo()  # line 904
        _.assertTrue(checkRepoFlag("strict", True))  # line 905
        try:  # line 906
            sos.config(["set", "strict", "disable"])  # line 906
        except SystemExit as E:  # line 907
            _.assertEqual(0, E.code)  # line 907
        makeRepo()  # line 908
        _.assertTrue(checkRepoFlag("strict", False))  # line 909
        try:  # line 910
            sos.config(["set", "strict", "enabled"])  # line 910
        except SystemExit as E:  # line 911
            _.assertEqual(0, E.code)  # line 911
        makeRepo()  # line 912
        _.assertTrue(checkRepoFlag("strict", True))  # line 913
        try:  # line 914
            sos.config(["set", "strict", "disabled"])  # line 914
        except SystemExit as E:  # line 915
            _.assertEqual(0, E.code)  # line 915
        makeRepo()  # line 916
        _.assertTrue(checkRepoFlag("strict", False))  # line 917
        try:  # line 918
            sos.config(["set", "strict", "nope"])  # line 918
            _.fail()  # line 918
        except SystemExit as E:  # line 919
            _.assertEqual(1, E.code)  # line 919

    def testLsSimple(_):  # line 921
        _.createFile(1)  # line 922
        _.createFile("foo")  # line 923
        _.createFile("ign1")  # line 924
        _.createFile("ign2")  # line 925
        _.createFile("bar", prefix="sub")  # line 926
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 927
        try:  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 928
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 928
        except SystemExit as E:  # line 929
            _.assertEqual(0, E.code)  # line 929
        try:  # additional ignore pattern  # line 930
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 930
        except SystemExit as E:  # line 931
            _.assertEqual(0, E.code)  # line 931
        try:  # define a list of ignore patterns  # line 932
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 932
        except SystemExit as E:  # line 933
            _.assertEqual(0, E.code)  # line 933
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # type: str  # line 934
        _.assertAllIn(["             ignores", "[global]", "['ign1', 'ign2']"], out)  # line 935
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 936
        _.assertAllIn(["             ignores", "[global]", "['ign1', 'ign2']"], out)  # line 937
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 938
        _.assertInAny('    file1', out)  # line 939
        _.assertInAny('    ign1', out)  # line 940
        _.assertInAny('    ign2', out)  # line 941
        _.assertNotIn('DIR sub', out)  # line 942
        _.assertNotIn('    bar', out)  # line 943
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 944
        _.assertIn('DIR sub', out)  # line 945
        _.assertIn('    bar', out)  # line 946
        try:  # line 947
            sos.config(["rm", "foo", "bar"])  # line 947
            _.fail()  # line 947
        except SystemExit as E:  # line 948
            _.assertEqual(1, E.code)  # line 948
        try:  # line 949
            sos.config(["rm", "ignores", "foo"])  # line 949
            _.fail()  # line 949
        except SystemExit as E:  # line 950
            _.assertEqual(1, E.code)  # line 950
        try:  # line 951
            sos.config(["rm", "ignores", "ign1"])  # line 951
        except SystemExit as E:  # line 952
            _.assertEqual(0, E.code)  # line 952
        try:  # remove ignore pattern  # line 953
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 953
        except SystemExit as E:  # line 954
            _.assertEqual(0, E.code)  # line 954
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 955
        _.assertInAny('    ign1', out)  # line 956
        _.assertInAny('IGN ign2', out)  # line 957
        _.assertNotInAny('    ign2', out)  # line 958

    def testWhitelist(_):  # line 960
# TODO test same for simple mode
        _.createFile(1)  # line 962
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 963
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 964
        sos.add(["."], ["./file*"])  # add tracking pattern for "file1"  # line 965
        sos.commit(options=["--force"])  # attempt to commit the file  # line 966
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 967
        try:  # Exit because dirty  # line 968
            sos.online()  # Exit because dirty  # line 968
            _.fail()  # Exit because dirty  # line 968
        except:  # exception expected  # line 969
            pass  # exception expected  # line 969
        _.createFile("x2")  # add another change  # line 970
        sos.add(["."], ["./x?"])  # add tracking pattern for "file1"  # line 971
        try:  # force beyond dirty flag check  # line 972
            sos.online(["--force"])  # force beyond dirty flag check  # line 972
            _.fail()  # force beyond dirty flag check  # line 972
        except:  # line 973
            pass  # line 973
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 974
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 975

        _.createFile(1)  # line 977
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 978
        sos.offline("xx", None, ["--track"])  # line 979
        sos.add(["."], ["./file*"])  # line 980
        sos.commit()  # should NOT ask for force here  # line 981
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 982

    def testRemove(_):  # line 984
        _.createFile(1, "x" * 100)  # line 985
        sos.offline("trunk")  # line 986
        try:  # line 987
            sos.destroy("trunk")  # line 987
            _fail()  # line 987
        except:  # line 988
            pass  # line 988
        _.createFile(2, "y" * 10)  # line 989
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 990
        sos.destroy("trunk")  # line 991
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 992
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 993
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 994
        sos.branch("next")  # line 995
        _.createFile(3, "y" * 10)  # make a change  # line 996
        sos.destroy("added", "--force")  # should succeed  # line 997

    def testFastBranchingOnEmptyHistory(_):  # line 999
        ''' Test fast branching without revisions and with them. '''  # line 1000
        sos.offline(options=["--strict", "--compress"])  # b0  # line 1001
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 1002
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 1003
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 1004
        sos.destroy("2")  # line 1005
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 1006
        _.assertIn("b0 'trunk' @", out)  # line 1007
        _.assertIn("b1         @", out)  # line 1008
        _.assertIn("b3         @", out)  # line 1009
        _.assertNotIn("b2         @", out)  # line 1010
        sos.branch("", "")  # non-fast branching of b4  # line 1011
        _.createFile(1)  # line 1012
        _.createFile(2)  # line 1013
        sos.commit("")  # line 1014
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 1015
        sos.destroy("4")  # line 1016
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 1017
        _.assertIn("b0 'trunk' @", out)  # line 1018
        _.assertIn("b1         @", out)  # line 1019
        _.assertIn("b3         @", out)  # line 1020
        _.assertIn("b5         @", out)  # line 1021
        _.assertNotIn("b2         @", out)  # line 1022
        _.assertNotIn("b4         @", out)  # line 1023
# TODO add more files and branch again

    def testUsage(_):  # line 1026
        try:  # TODO expect sys.exit(0)  # line 1027
            sos.usage()  # TODO expect sys.exit(0)  # line 1027
            _.fail()  # TODO expect sys.exit(0)  # line 1027
        except:  # line 1028
            pass  # line 1028
        try:  # TODO expect sys.exit(0)  # line 1029
            sos.usage("help")  # TODO expect sys.exit(0)  # line 1029
            _.fail()  # TODO expect sys.exit(0)  # line 1029
        except:  # line 1030
            pass  # line 1030
        try:  # TODO expect sys.exit(0)  # line 1031
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 1031
            _.fail()  # TODO expect sys.exit(0)  # line 1031
        except:  # line 1032
            pass  # line 1032
        try:  # line 1033
            sos.usage(version=True)  # line 1033
            _.fail()  # line 1033
        except:  # line 1034
            pass  # line 1034
        try:  # line 1035
            sos.usage(version=True)  # line 1035
            _.fail()  # line 1035
        except:  # line 1036
            pass  # line 1036

    def testOnlyExcept(_):  # line 1038
        ''' Test blacklist glob rules. '''  # line 1039
        sos.offline(options=["--track"])  # line 1040
        _.createFile("a.1")  # line 1041
        _.createFile("a.2")  # line 1042
        _.createFile("b.1")  # line 1043
        _.createFile("b.2")  # line 1044
        sos.add(["."], ["./a.?"])  # line 1045
        sos.add(["."], ["./?.1"], negative=True)  # line 1046
        out = wrapChannels(lambda _=None: sos.commit())  # type: str  # line 1047
        _.assertIn("ADD ./a.2", out)  # line 1048
        _.assertNotIn("ADD ./a.1", out)  # line 1049
        _.assertNotIn("ADD ./b.1", out)  # line 1050
        _.assertNotIn("ADD ./b.2", out)  # line 1051

    def testOnly(_):  # line 1053
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",)), ["bla"]), sos.parseArgumentOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--remote", "bla", "--only"]))  # line 1054
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1055
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1056
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1057
        sos.offline(options=["--track", "--strict"])  # line 1058
        _.createFile(1)  # line 1059
        _.createFile(2)  # line 1060
        sos.add(["."], ["./file1"])  # line 1061
        sos.add(["."], ["./file2"])  # line 1062
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1063
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1064
        sos.commit()  # adds also file2  # line 1065
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1066
        _.createFile(1, "cc")  # modify both files  # line 1067
        _.createFile(2, "dd")  # line 1068
        try:  # line 1069
            sos.config(["set", "texttype", "file2"])  # line 1069
        except SystemExit as E:  # line 1070
            _.assertEqual(0, E.code)  # line 1070
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1071
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1072
        _.assertTrue("./file2" in changes.modifications)  # line 1073
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # line 1074
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1075
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1076
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # line 1077

    def testEmptyFiles(_):  # line 1079
        sos.offline()  # line 1080
        _.createFile(1, "")  # empty file  # line 1081
        sos.commit()  # line 1082
        changes = sos.changes()  # line 1083
        _.assertEqual(0, len(changes.additions) + len(changes.modifications) + len(changes.deletions))  # line 1084

        setRepoFlag("strict", True)  # line 1086
        changes = sos.changes()  # line 1087
        _.assertEqual(1, len(changes.modifications))  # because hash was set to None in simple mode  # line 1088
        sos.commit()  # commit now with hash computation  # line 1089
        setRepoFlag("strict", False)  # line 1090

        time.sleep(FS_PRECISION)  # line 1092
        _.createFile(1, "")  # touch file  # line 1093
        changes = sos.changes()  # line 1094
        _.assertEqual(1, len(changes.modifications))  # since modified timestamp  # line 1095

    def testDiff(_):  # line 1097
        try:  # manually mark this file as "textual"  # line 1098
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1098
        except SystemExit as E:  # line 1099
            _.assertEqual(0, E.code)  # line 1099
        sos.offline(options=["--strict"])  # line 1100
        _.createFile(1)  # line 1101
        _.createFile(2)  # line 1102
        sos.commit()  # line 1103
        _.createFile(1, "sdfsdgfsdf")  # line 1104
        _.createFile(2, "12343")  # line 1105
        sos.commit()  # line 1106
        _.createFile(1, "foobar")  # line 1107
        _.createFile(3)  # line 1108
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # type: str  # compare with r1 (second counting from last which is r2)  # line 1109
        _.assertIn("ADD ./file3", out)  # line 1110
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "old 0 |xxxxxxxxxx|", "now 0 |foobar|"], out)  # line 1111
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1112

    def testReorderRenameActions(_):  # line 1114
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1115
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1116
        try:  # line 1117
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1117
            _.fail()  # line 1117
        except:  # line 1118
            pass  # line 1118

    def testPublish(_):  # line 1120
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1121

    def testColorFlag(_):  # line 1123
        sos.offline()  # line 1124
        _.createFile(1)  # line 1125
#    setRepoFlag("useColorOutput", False, toConfig = True)
#    sos.Metadata.singleton = None  # for new slurp of configuration
        sos.enableColor(False, force=True)  # line 1128
        sos.verbose[:] = [None]  # set "true"  # line 1129
        out = wrapChannels(lambda _=None: sos.changes()).replace("\r\n", "\n").split("\n")  # type: List[str]  # line 1130
        _.assertTrue(any((line.startswith(sos.usage.MARKER_TEXT + "Changes of file tree") for line in out)))  # line 1131
#    setRepoFlag("useColorOutput", True,  toConfig = True)
#    sos.Metadata.singleton = None
        sos.enableColor(True, force=True)  # line 1134
        out = wrapChannels(lambda _=None: sos.changes()).replace("\r\n", "\n").split("\n")  # line 1135
        _.assertTrue(any((line.startswith((sos.usage.MARKER_TEXT if sys.platform == "win32" else sos.MARKER_COLOR) + "Changes of file tree") for line in out)))  # because it may start with a color code  # line 1136
        sos.verbose.pop()  # line 1137

    def testMove(_):  # line 1139
        ''' Move primarily modifies tracking patterns and moves files around accordingly. '''  # line 1140
        sos.offline(options=["--strict", "--track"])  # line 1141
        _.createFile(1)  # line 1142
        sos.add(["."], ["./file?"])  # line 1143
# assert error when source folder is missing
        out = wrapChannels(lambda _=None: sos.move("sub", "sub/file?", ".", "./?file"))  # type: str  # line 1145
        _.assertIn("Source folder doesn't exist", out)  # line 1146
        _.assertIn("EXIT CODE 1", out)  # line 1147
# if target folder missing: create it and move matching files into it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1149
        _.assertTrue(os.path.exists("sub"))  # line 1150
        _.assertTrue(os.path.exists("sub/file1"))  # line 1151
        _.assertFalse(os.path.exists("file1"))  # line 1152
# test move back to previous location, plus rename the file
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1154
        _.assertTrue(os.path.exists("1file"))  # line 1155
        _.assertFalse(os.path.exists("sub/file1"))  # line 1156
# assert error when nothing matches source pattern
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*"))  # line 1158
        _.assertIn("No files match the specified file pattern", out)  # line 1159
        _.assertIn("EXIT CODE", out)  # line 1160
        sos.add(["."], ["./*"])  # add catch-all tracking pattern to root folder  # line 1161
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*", options=["--force"]))  # line 1162
        _.assertIn("  './*' matches 3 files", out)  # line 1163
        _.assertIn("EXIT CODE", out)  # line 1164
# test rename no conflict
        _.createFile(1)  # line 1166
        _.createFile(2)  # line 1167
        _.createFile(3)  # line 1168
        sos.add(["."], ["./file*"])  # line 1169
        sos.remove(["."], ["./*"])  # line 1170
        try:  # define an ignore pattern  # line 1171
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1171
        except SystemExit as E:  # line 1172
            _.assertEqual(0, E.code)  # line 1172
        try:  # line 1173
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1173
        except SystemExit as E:  # line 1174
            _.assertEqual(0, E.code)  # line 1174
        sos.move(".", "./file*", ".", "./fi*le")  # should only move not ignored files files  # line 1175
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1176
        _.assertTrue(all((not os.path.exists("file%d" % i) for i in range(1, 4))))  # line 1177
        _.assertFalse(os.path.exists("fi4le"))  # line 1178
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1180
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(["."], ["./?file"])  # untrack pattern, which was renamed before  # line 1184
        sos.add(["."], ["./?a?b"], ["--force"])  # line 1185
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1186
        _.createFile("1a2b")  # should not be tracked  # line 1187
        _.createFile("a1b2")  # should be tracked  # line 1188
        sos.commit()  # line 1189
        _.assertEqual(5, len(os.listdir(sos.revisionFolder(0, 1))))  # meta, a1b2, fi[1-3]le  # line 1190
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1191
        _.createFile("1a1b1")  # line 1192
        _.createFile("1a1b2")  # line 1193
        sos.add(["."], ["./?a?b*"])  # line 1194
# test target pattern exists
        out = wrapChannels(lambda _=None: sos.move(".", "./?a?b*", ".", "./z?z?"))  # line 1196
        _.assertIn("not unique", out)  # line 1197
# TODO only rename if actually any files are versioned? or simply what is currently alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1201
        _.createFile(1)  # line 1202
        _.createFile(3)  # line 1203
        _.createFile(5)  # line 1204
        sos.offline()  # branch 0: only file1  # line 1205
        sos.branch()  # line 1206
        os.unlink("file1")  # line 1207
        os.unlink("file3")  # line 1208
        os.unlink("file5")  # line 1209
        _.createFile(2)  # line 1210
        _.createFile(4)  # line 1211
        _.createFile(6)  # line 1212
        sos.commit()  # branch 1: only file2  # line 1213
        sos.switch("0/")  # line 1214
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1215
        _.assertFalse(_.existsFile(1))  # line 1216
        _.assertFalse(_.existsFile(3))  # line 1217
        _.assertFalse(_.existsFile(5))  # line 1218
        _.assertTrue(_.existsFile(2))  # line 1219
        _.assertTrue(_.existsFile(4))  # line 1220
        _.assertTrue(_.existsFile(6))  # line 1221

    def testMoveDetection(_):  # line 1223
        _.createFile(1, "bla")  # line 1224
        sos.offline()  # line 1225
        os.mkdir("sub1")  # line 1226
        os.mkdir("sub2")  # line 1227
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1228
        shutil.move("file1", "sub2")  # line 1229
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 1230
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1231
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1232
        sos.commit("Moved the file")  # line 1233
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1237

    def testHashCollision(_):  # line 1239
        old = sos.Metadata.findChanges  # line 1240
        @_coconut_tco  # line 1241
        def patched(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[sos.ChangeSet, _coconut.typing.Optional[str]]':  # line 1241
            import collections  # used only in this method  # line 1242
            write = branch is not None and revision is not None  # line 1243
            if write:  # line 1244
                try:  # line 1245
                    os.makedirs(sos.encode(sos.revisionFolder(branch, revision, base=_.root)))  # line 1245
                except FileExistsError:  # HINT "try" only necessary for hash collision *test code* (!)  # line 1246
                    pass  # HINT "try" only necessary for hash collision *test code* (!)  # line 1246
            return _coconut_tail_call(old, _, branch, revision, checkContent, inverse, considerOnly, dontConsider, progress)  # line 1247
        sos.Metadata.findChanges = patched  # monkey-patch  # line 1248
        sos.offline()  # line 1249
        _.createFile(1)  # line 1250
        os.mkdir(sos.revisionFolder(0, 1))  # line 1251
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # hashed file name for not-yet-committed file1  # line 1252
        _.createFile(1)  # line 1253
        try:  # line 1254
            sos.commit()  # line 1254
            _.fail("Expected system exit due to hash collision detection")  # line 1254
        except SystemExit as E:  # HINT exit is implemented in utility.hashFile  # line 1255
            _.assertEqual(1, E.code)  # HINT exit is implemented in utility.hashFile  # line 1255
        sos.Metadata.findChanges = old  # revert monkey patch  # line 1256

    def testFindBase(_):  # line 1258
        old = os.getcwd()  # line 1259
        try:  # line 1260
            os.mkdir("." + os.sep + ".git")  # line 1261
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1262
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1263
            os.chdir("a" + os.sep + "b")  # line 1264
            s, vcs, cmd = sos.findSosVcsBase()  # line 1265
            _.assertIsNotNone(s)  # line 1266
            _.assertIsNotNone(vcs)  # line 1267
            _.assertEqual("git", cmd)  # line 1268
        finally:  # line 1269
            os.chdir(old)  # line 1269

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1280
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1281
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1282
