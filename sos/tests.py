#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x775de0f4

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


# Uni tests
    def testAccessor(_):  # line 154
        a = sos.Accessor({"a": 1})  # line 155
        _.assertEqual((1, 1), (a["a"], a.a))  # line 156

    def testIndexing(_):  # line 158
        m = sos.Metadata()  # line 159
        m.commits = {}  # line 160
        _.assertEqual(1, m.correctNegativeIndexing(1))  # line 161
        _.assertEqual(9999999999999999, m.correctNegativeIndexing(9999999999999999))  # line 162
        _.assertEqual(0, m.correctNegativeIndexing(0))  # zero always returns zero, even no commits present  # line 163
        try:  # line 164
            m.correctNegativeIndexing(-1)  # line 164
            _.fail()  # line 164
        except SystemExit as E:  # line 165
            _.assertEqual(1, E.code)  # line 165
        m.commits = {0: sos.CommitInfo(0, 0), 1: sos.CommitInfo(1, 0)}  # line 166
        _.assertEqual(1, m.correctNegativeIndexing(-1))  # zero always returns zero, even no commits present  # line 167
        _.assertEqual(0, m.correctNegativeIndexing(-2))  # zero always returns zero, even no commits present  # line 168
        try:  # line 169
            m.correctNegativeIndexing(-3)  # line 169
            _.fail()  # line 169
        except SystemExit as E:  # line 170
            _.assertEqual(1, E.code)  # line 170

    def testRestoreFile(_):  # line 172
        m = sos.Metadata()  # line 173
        os.makedirs(sos.revisionFolder(0, 0))  # line 174
        _.createFile("hashed_file", "content", sos.revisionFolder(0, 0))  # line 175
        m.restoreFile(relPath="restored", branch=0, revision=0, pinfo=sos.PathInfo("hashed_file", 0, (time.time() - 2000) * 1000, "content hash"))  # line 176
        _.assertTrue(_.existsFile("restored", b""))  # line 177

    def testGetAnyOfmap(_):  # line 179
        _.assertEqual(2, sos.getAnyOfMap({"a": 1, "b": 2}, ["x", "b"]))  # line 180
        _.assertIsNone(sos.getAnyOfMap({"a": 1, "b": 2}, []))  # line 181

    def testAjoin(_):  # line 183
        _.assertEqual("a1a2", sos.ajoin("a", ["1", "2"]))  # line 184
        _.assertEqual("* a\n* b", sos.ajoin("* ", ["a", "b"], "\n"))  # line 185

    def testFindChanges(_):  # line 187
        m = sos.Metadata(os.getcwd())  # line 188
        try:  # line 189
            sos.config(["set", "texttype", "*"])  # line 189
        except SystemExit as E:  # line 190
            _.assertEqual(0, E.code)  # line 190
        try:  # will be stripped from leading paths anyway  # line 191
            sos.config(["set", "ignores", "test/*.cfg;D:\\apps\\*.cfg.bak"])  # will be stripped from leading paths anyway  # line 191
        except SystemExit as E:  # line 192
            _.assertEqual(0, E.code)  # line 192
        m = sos.Metadata(os.getcwd())  # reload from file system  # line 193
        for file in [f for f in os.listdir() if f.endswith(".bak")]:  # remove configuration file  # line 194
            os.unlink(file)  # remove configuration file  # line 194
        _.createFile(9, b"")  # line 195
        _.createFile(1, "1")  # line 196
        m.createBranch(0)  # line 197
        _.assertEqual(2, len(m.paths))  # line 198
        time.sleep(FS_PRECISION)  # time required by filesystem time resolution issues  # line 199
        _.createFile(1, "2")  # modify existing file  # line 200
        _.createFile(2, "2")  # add another file  # line 201
        m.loadCommit(0, 0)  # line 202
        changes, msg = m.findChanges()  # detect time skew  # line 203
        _.assertEqual(1, len(changes.additions))  # line 204
        _.assertEqual(0, len(changes.deletions))  # line 205
        _.assertEqual(1, len(changes.modifications))  # line 206
        _.assertEqual(0, len(changes.moves))  # line 207
        m.paths.update(changes.additions)  # line 208
        m.paths.update(changes.modifications)  # line 209
        _.createFile(2, "12")  # modify file again  # line 210
        changes, msg = m.findChanges(0, 1)  # by size, creating new commit  # line 211
        _.assertEqual(0, len(changes.additions))  # line 212
        _.assertEqual(0, len(changes.deletions))  # line 213
        _.assertEqual(1, len(changes.modifications))  # line 214
        _.assertEqual(0, len(changes.moves))  # line 215
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1)))  # line 216
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # line 217
# TODO test moves

    def testDumpSorting(_):  # line 220
        m = sos.Metadata()  # type: Metadata  # line 221
        _.createFile(1)  # line 222
        sos.offline()  # line 223
        _.createFile(2)  # line 224
        _.createFile(3)  # line 225
        sos.commit()  # line 226
        _.createFile(4)  # line 227
        _.createFile(5)  # line 228
        sos.commit()  # line 229
        out = [__.replace(os.getcwd() + os.sep + sos.metaFolder + os.sep, "").strip() for __ in wrapChannels(lambda _=None: sos.dump("x." + sos.DUMP_FILE)).replace("\r", "").split("\n")]  # type: List[str]  # line 230
        _.assertTrue(out.index("b0%sr2" % os.sep) > out.index("b0%sr1" % os.sep))  # line 231
        _.assertTrue(out.index("b0%sr1" % os.sep) > out.index("b0%sr0" % os.sep))  # line 232

    def testFitStrings(_):  # line 234
        a = ["a", "a" * 6, "a" * 15]  # type: List[str]  # line 235
        _.assertEqual('pre "a" "aaaaaa"', sos.fitStrings(a, "pre", length=20))  # line 236
        _.assertEqual('pre "aaaaaaaaaaaaaaa"', sos.fitStrings(a, "pre", length=25))  # line 237
    def testMoves(_):  # line 238
        _.createFile(1, "1")  # line 239
        _.createFile(2, "2", "sub")  # line 240
        sos.offline(options=["--strict", "--compress"])  # TODO move compress flag to own test function and check if it actually works  # line 241
        os.renames(sos.encode("." + os.sep + "file1"), sos.encode("sub" + os.sep + "file1"))  # line 242
        os.renames(sos.encode("sub" + os.sep + "file2"), sos.encode("." + os.sep + "file2"))  # line 243
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 244
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 245
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 246
        out = wrapChannels(lambda _=None: sos.changes(options=["--relative"], cwd="sub"))  # line 247
        _.assertIn("MOV ..%sfile2  <-  file2" % os.sep, out)  # no ./ for relative OS-specific paths  # line 248
        _.assertIn("MOV file1  <-  ..%sfile1" % os.sep, out)  # line 249
        out = wrapChannels(lambda _=None: sos.commit())  # line 250
        _.assertIn("MOV ./file2  <-  sub/file2", out)  # line 251
        _.assertIn("MOV sub/file1  <-  ./file1", out)  # line 252
        _.assertAllIn(["Created new revision r01", "summing 628 bytes in 2 files (88.22% SOS overhead)"], out)  # TODO why is this not captured?  # line 253

    def testPatternPaths(_):  # line 255
        sos.offline(options=["--track"])  # line 256
        os.mkdir("sub")  # line 257
        _.createFile("sub" + os.sep + "file1", "sdfsdf")  # line 258
        out = wrapChannels(lambda _=None: sos.add("sub", "sub/file?"))  # type: str  # line 259
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", os.path.abspath("sub")], out)  # line 260
        sos.commit("test")  # should pick up sub/file1 pattern  # line 261
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # sub/file1 was added  # line 262
        _.createFile(1)  # line 263
        try:  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 264
            sos.commit("nothing")  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 264
            _.fail()  # should not commit anything, as the file in base folder doesn't match the tracked pattern  # line 264
        except:  # line 265
            pass  # line 265

    def testNoArgs(_):  # line 267
        pass  # call "sos" without arguments should simply show help or info about missing arguments  # line 268

    def testAutoMetadataUpgrade(_):  # line 270
        sos.offline()  # line 271
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "r", encoding=sos.UTF8) as fd:  # line 272
            repo, branches, config = json.load(fd)  # line 272
        repo["version"] = None  # lower than any pip version  # line 273
        branches[:] = [branch[:5] for branch in branches]  # simulate some older state  # line 274
        del repo["format"]  # simulate pre-1.3.5  # line 275
        with codecs.open(sos.encode(os.path.join(sos.metaFolder, sos.metaFile)), "w", encoding=sos.UTF8) as fd:  # line 276
            json.dump((repo, branches, config), fd, ensure_ascii=False)  # line 276
        out = wrapChannels(lambda _=None: sos.status(options=["--repo"]))  # type: str  # line 277
        _.assertAllIn(["pre-1.2", "Upgraded repository metadata to match SOS version '2018.1210.3028'", "Upgraded repository metadata to match SOS version '1.3.5'"], out)  # line 278

    def testFastBranching(_):  # line 280
        _.createFile(1)  # line 281
        out = wrapChannels(lambda _=None: sos.offline(options=["--strict", "--verbose"]))  # type: str  # b0/r0 = ./file1  # line 282
        _.assertIn("1 file added to initial branch 'trunk'", out)  # line 283
        _.createFile(2)  # line 284
        os.unlink("file1")  # line 285
        sos.commit()  # b0/r1 = +./file2  -./file1  # line 286
        sos.branch(options=["--fast", "--last"])  # branch b1 from b0/1 TODO modify option switch once --fast becomes the new normal  # line 287
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0", "b1"], os.listdir(sos.metaFolder), only=True)  # line 288
        _.createFile(3)  # line 289
        sos.commit()  # b1/r2 = ./file2, ./file3  # line 290
        _.assertAllIn([sos.metaFile, sos.metaBack, "r2"], os.listdir(sos.branchFolder(1)), only=True)  # line 291
        sos.branch(options=["--fast", "--last"])  # branch b2 from b1/2  # line 292
        sos.destroy("0")  # remove parent of b1 and transitive parent of b2  # line 293
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1", "b2"], os.listdir(sos.metaFolder), only=True)  # branch 0 was removed  # line 294
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(1)), only=True)  # all revisions before branch point were copied to branch 1  # line 295
        _.assertAllIn([sos.metaFile, sos.metaBack, "r0", "r1", "r2"], os.listdir(sos.branchFolder(2)), only=True)  # line 296
# TODO test also other functions like status --repo, log

    def testModificationWithOldRevisionRecognition(_):  # line 299
        now = time.time()  # type: float  # line 300
        _.createFile(1)  # line 301
        sync()  # line 302
        sos.offline(options=["--strict"])  # line 303
        _.createFile(1, "abc")  # modify contents  # line 304
        os.utime(sos.encode("file1"), (now - 2000, now - 2000))  # make it look like an older version  # line 305
        sync()  # line 306
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 307
        _.assertIn("<older than previously committed>", out)  # line 308
        out = wrapChannels(lambda _=None: sos.commit())  # line 309
        _.assertIn("<older than previously committed>", out)  # line 310

    def testGetParentBranch(_):  # line 312
        m = sos.Accessor({"branches": {0: sos.Accessor({"parent": None, "revision": None}), 1: sos.Accessor({"parent": 0, "revision": 1})}, "getParentBranches": lambda b, r: sos.Metadata.getParentBranches(m, b, r)})  # stupid workaround for the self-reference in the implementation  # line 313
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 0))  # line 314
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 1, 1))  # line 315
        _.assertEqual(1, sos.Metadata.getParentBranch(m, 1, 2))  # line 316
        _.assertEqual(0, sos.Metadata.getParentBranch(m, 0, 10))  # line 317

    def testTokenizeGlobPattern(_):  # line 319
        _.assertEqual([], sos.tokenizeGlobPattern(""))  # line 320
        _.assertEqual([sos.GlobBlock(False, "*", 0)], sos.tokenizeGlobPattern("*"))  # line 321
        _.assertEqual([sos.GlobBlock(False, "*", 0), sos.GlobBlock(False, "???", 1)], sos.tokenizeGlobPattern("*???"))  # line 322
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(True, "x", 2)], sos.tokenizeGlobPattern("x*x"))  # line 323
        _.assertEqual([sos.GlobBlock(True, "x", 0), sos.GlobBlock(False, "*", 1), sos.GlobBlock(False, "??", 2), sos.GlobBlock(False, "*", 4), sos.GlobBlock(True, "x", 5)], sos.tokenizeGlobPattern("x*??*x"))  # line 324
        _.assertEqual([sos.GlobBlock(False, "?", 0), sos.GlobBlock(True, "abc", 1), sos.GlobBlock(False, "*", 4)], sos.tokenizeGlobPattern("?abc*"))  # line 325

    def testTokenizeGlobPatterns(_):  # line 327
        try:  # because number of literal strings differs  # line 328
            sos.tokenizeGlobPatterns("x*x", "x*")  # because number of literal strings differs  # line 328
            _.fail()  # because number of literal strings differs  # line 328
        except:  # line 329
            pass  # line 329
        try:  # because glob patterns differ  # line 330
            sos.tokenizeGlobPatterns("x*", "x?")  # because glob patterns differ  # line 330
            _.fail()  # because glob patterns differ  # line 330
        except:  # line 331
            pass  # line 331
        try:  # glob patterns differ, regardless of position  # line 332
            sos.tokenizeGlobPatterns("x*", "?x")  # glob patterns differ, regardless of position  # line 332
            _.fail()  # glob patterns differ, regardless of position  # line 332
        except:  # line 333
            pass  # line 333
        sos.tokenizeGlobPatterns("x*", "*x")  # succeeds, because glob patterns match (differ only in position)  # line 334
        sos.tokenizeGlobPatterns("*xb?c", "*x?bc")  # succeeds, because glob patterns match (differ only in position)  # line 335
        try:  # succeeds, because glob patterns match (differ only in position)  # line 336
            sos.tokenizeGlobPatterns("a???b*", "ab???*")  # succeeds, because glob patterns match (differ only in position)  # line 336
            _.fail()  # succeeds, because glob patterns match (differ only in position)  # line 336
        except:  # line 337
            pass  # line 337

    def testConvertGlobFiles(_):  # line 339
        _.assertEqual(["xxayb", "aacb"], [r[1] for r in sos.convertGlobFiles(["axxby", "aabc"], *sos.tokenizeGlobPatterns("a*b?", "*a?b"))])  # line 340
        _.assertEqual(["1qq2ww3", "1abcbx2xbabc3"], [r[1] for r in sos.convertGlobFiles(["qqxbww", "abcbxxbxbabc"], *sos.tokenizeGlobPatterns("*xb*", "1*2*3"))])  # line 341

    def testFolderRemove(_):  # line 343
        m = sos.Metadata(os.getcwd())  # line 344
        _.createFile(1)  # line 345
        _.createFile("a", prefix="sub")  # line 346
        sos.offline()  # line 347
        _.createFile(2)  # line 348
        os.unlink("sub" + os.sep + "a")  # line 349
        os.rmdir("sub")  # line 350
        changes = sos.changes()  # TODO #254 replace by output check  # line 351
        _.assertEqual(1, len(changes.additions))  # line 352
        _.assertEqual(0, len(changes.modifications))  # line 353
        _.assertEqual(1, len(changes.deletions))  # line 354
        _.createFile("a", prefix="sub")  # line 355
        changes = sos.changes()  # line 356
        _.assertEqual(0, len(changes.deletions))  # line 357

    def testSwitchConflict(_):  # line 359
        sos.offline(options=["--strict"])  # (r0)  # line 360
        _.createFile(1)  # line 361
        sos.commit()  # add file (r1)  # line 362
        os.unlink("file1")  # line 363
        sos.commit()  # remove (r2)  # line 364
        _.createFile(1, "something else")  # line 365
        sos.commit()  # (r3)  # line 366
        sos.switch("/1")  # updates file1 - marked as MOD, because mtime was changed  # line 367
        _.existsFile(1, "x" * 10)  # line 368
        sos.switch("/2", ["--force"])  # remove file1 requires --force, because size/content (or mtime in non-strict mode) is different to head of branch  # line 369
        sos.switch("/0")  # do nothing, as file1 is already removed  # line 370
        sos.switch("/1")  # add file1 back  # line 371
        sos.switch("/", ["--force"])  # requires force because changed vs. head of branch  # line 372
        _.existsFile(1, "something else")  # line 373

    def testComputeSequentialPathSet(_):  # line 375
        os.makedirs(sos.revisionFolder(0, 0))  # line 376
        os.makedirs(sos.revisionFolder(0, 1))  # line 377
        os.makedirs(sos.revisionFolder(0, 2))  # line 378
        os.makedirs(sos.revisionFolder(0, 3))  # line 379
        os.makedirs(sos.revisionFolder(0, 4))  # line 380
        m = sos.Metadata(os.getcwd())  # line 381
        m.branch = 0  # line 382
        m.commit = 2  # line 383
        m.saveBranches()  # line 384
        m.paths = {"./a": sos.PathInfo("", 0, 0, "")}  # line 385
        m.saveCommit(0, 0)  # initial  # line 386
        m.paths["./a"] = sos.PathInfo("", 1, 0, "")  # line 387
        m.saveCommit(0, 1)  # mod  # line 388
        m.paths["./b"] = sos.PathInfo("", 0, 0, "")  # line 389
        m.saveCommit(0, 2)  # add  # line 390
        m.paths["./a"] = sos.PathInfo("", None, 0, "")  # line 391
        m.saveCommit(0, 3)  # del  # line 392
        m.paths["./a"] = sos.PathInfo("", 2, 0, "")  # line 393
        m.saveCommit(0, 4)  # readd  # line 394
        m.commits = {i: sos.CommitInfo(i, 0, None) for i in range(5)}  # line 395
        m.saveBranch(0)  # line 396
        m.branches = {0: sos.BranchInfo(0, 0), 1: sos.BranchInfo(1, 0)}  # line 397
        m.saveBranches()  # line 398
        m.computeSequentialPathSet(0, 4)  # line 399
        _.assertEqual(2, len(m.paths))  # line 400

    def testParseRevisionString(_):  # line 402
        m = sos.Metadata(os.getcwd())  # line 403
        m.branch = 1  # line 404
        m.commits = {0: 0, 1: 1, 2: 2}  # line 405
        _.assertEqual((1, 3), m.parseRevisionString("3"))  # line 406
        _.assertEqual((2, 3), m.parseRevisionString("2/3"))  # line 407
        _.assertEqual((1, -1), m.parseRevisionString(None))  # line 408
        _.assertEqual((None, None), m.parseRevisionString(""))  # line 409
        _.assertEqual((2, -1), m.parseRevisionString("2/"))  # line 410
        _.assertEqual((1, -2), m.parseRevisionString("/-2"))  # line 411
        _.assertEqual((1, -1), m.parseRevisionString("/"))  # line 412

    def testOfflineEmpty(_):  # line 414
        os.mkdir("." + os.sep + sos.metaFolder)  # line 415
        try:  # line 416
            sos.offline("trunk")  # line 416
            _.fail()  # line 416
        except SystemExit as E:  # line 417
            _.assertEqual(1, E.code)  # line 417
        os.rmdir("." + os.sep + sos.metaFolder)  # line 418
        sos.offline("test")  # line 419
        _.assertIn(sos.metaFolder, os.listdir("."))  # line 420
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 421
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 422
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 423
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 424
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file  # line 425

    def testOfflineWithFiles(_):  # line 427
        _.createFile(1, "x" * 100)  # line 428
        _.createFile(2)  # line 429
        sos.offline("test")  # line 430
        _.assertAllIn(["file1", "file2", sos.metaFolder], os.listdir("."))  # line 431
        _.assertAllIn(["b0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 432
        _.assertAllIn(["r0", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 433
        _.assertAllIn([sos.metaFile, "03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2", "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0" + os.sep + "r0"))  # line 434
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder)))  # only branch folder and meta data file  # line 435
        _.assertEqual(2, len(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0")))  # only commit folder and meta data file  # line 436
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 0))))  # only meta data file plus branch base file copies  # line 437

    def testBranch(_):  # line 439
        _.createFile(1, "x" * 100)  # line 440
        _.createFile(2)  # line 441
        sos.offline("test")  # b0/r0  # line 442
        sos.branch("other")  # b1/r0  # line 443
        _.assertAllIn(["b0", "b1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder))  # line 444
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b1"))))  # line 445
        _.assertEqual(list(sorted(os.listdir(sos.revisionFolder(0, 0)))), list(sorted(os.listdir(sos.revisionFolder(1, 0)))))  # line 447
        _.createFile(1, "z")  # modify file  # line 449
        sos.branch()  # b2/r0  branch to unnamed branch with modified file tree contents  # line 450
        _.assertNotEqual(os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b1" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size, os.stat(sos.encode("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0" + os.sep + "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa")).st_size)  # line 451
        _.createFile(3, "z")  # line 453
        sos.branch("from_last_revision", options=["--last", "--stay"])  # b3/r0 create copy of other file1,file2 and don't switch  # line 454
        _.assertEqual(list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b3" + os.sep + "r0"))), list(sorted(os.listdir("." + os.sep + sos.metaFolder + os.sep + "b2" + os.sep + "r0"))))  # line 455
# Check sos.status output which branch is marked


    def testComittingAndChanges(_):  # line 460
        _.createFile(1, "x" * 100)  # line 461
        _.createFile(2)  # line 462
        sos.offline("test")  # line 463
        changes = sos.changes()  # line 464
        _.assertEqual(0, len(changes.additions))  # line 465
        _.assertEqual(0, len(changes.deletions))  # line 466
        _.assertEqual(0, len(changes.modifications))  # line 467
        _.createFile(1, "z")  # size change  # line 468
        changes = sos.changes()  # line 469
        _.assertEqual(0, len(changes.additions))  # line 470
        _.assertEqual(0, len(changes.deletions))  # line 471
        _.assertEqual(1, len(changes.modifications))  # line 472
        sos.commit("message")  # line 473
        _.assertAllIn(["r0", "r1", sos.metaFile], os.listdir("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 474
        _.assertAllIn([sos.metaFile, "b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"], os.listdir(sos.revisionFolder(0, 1)))  # line 475
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # no further files, only the modified one  # line 476
        _.assertEqual(1, len(sos.changes("/0").modifications))  # vs. explicit revision on current branch  # line 477
        _.assertEqual(1, len(sos.changes("0/0").modifications))  # vs. explicit branch/revision  # line 478
        _.createFile(1, "")  # modify to empty file, mentioned in meta data, but not stored as own file  # line 479
        os.unlink("file2")  # line 480
        changes = sos.changes()  # line 481
        _.assertEqual(0, len(changes.additions))  # line 482
        _.assertEqual(1, len(changes.deletions))  # line 483
        _.assertEqual(1, len(changes.modifications))  # line 484
        sos.commit("modified")  # line 485
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # no additional files, only mentions in metadata  # line 486
        try:  # expecting Exit due to no changes  # line 487
            sos.commit("nothing")  # expecting Exit due to no changes  # line 487
            _.fail()  # expecting Exit due to no changes  # line 487
        except:  # line 488
            pass  # line 488

    def testGetBranch(_):  # line 490
        m = sos.Metadata(os.getcwd())  # line 491
        m.branch = 1  # current branch  # line 492
        m.branches = {0: sos.BranchInfo(0, 0, "trunk")}  # line 493
        _.assertEqual(27, m.getBranchByName(27))  # line 494
        _.assertEqual(0, m.getBranchByName("trunk"))  # line 495
        _.assertEqual(1, m.getBranchByName(""))  # split from "/"  # line 496
        _.assertIsNone(m.getBranchByName("unknown"))  # line 497
        m.commits = {0: sos.CommitInfo(0, 0, "bla")}  # line 498
        _.assertEqual(13, m.getRevisionByName("13"))  # line 499
        _.assertEqual(0, m.getRevisionByName("bla"))  # line 500
        _.assertEqual(-1, m.getRevisionByName(""))  # split from "/"  # line 501

    def testTagging(_):  # line 503
        m = sos.Metadata(os.getcwd())  # line 504
        sos.offline()  # line 505
        _.createFile(111)  # line 506
        sos.commit("tag", ["--tag"])  # line 507
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "").split("\n")  # type: str  # line 508
        _.assertTrue(any(("|tag" in line and line.endswith("|%sTAG%s" % (sos.Fore.MAGENTA, sos.Fore.RESET)) for line in out)))  # line 509
        _.createFile(2)  # line 510
        try:  # line 511
            sos.commit("tag")  # line 511
            _.fail()  # line 511
        except:  # line 512
            pass  # line 512
        sos.commit("tag-2", ["--tag"])  # line 513
        out = wrapChannels(lambda _=None: sos.ls(options=["--tags"])).replace("\r", "")  # line 514
        _.assertIn("TAG tag", out)  # line 515

    def testSwitch(_):  # line 517
        try:  # line 518
            shutil.rmtree(os.path.join(rmteFolder, sos.metaFolder))  # line 518
        except:  # line 519
            pass  # line 519
        _.createFile(1, "x" * 100)  # line 520
        _.createFile(2, "y")  # line 521
        sos.offline("test", remotes=[rmteFolder])  # file1-2  in initial branch commit  # line 522
        sos.branch("second")  # file1-2  switch, having same files  # line 523
        sos.switch("0")  # no change, switch back, no problem  # line 524
        sos.switch("second")  # no change  # switch back, no problem  # line 525
        _.createFile(3, "y")  # generate a file  # line 526
        try:  # uncommited changes detected  # line 527
            sos.switch("test")  # uncommited changes detected  # line 527
            _.fail()  # uncommited changes detected  # line 527
        except SystemExit as E:  # line 528
            _.assertEqual(1, E.code)  # line 528
        sos.commit("Finish")  # file1-3  commit third file into branch second  # line 529
        sos.changes()  # line 530
        sos.switch("test")  # file1-2, remove file3 from file tree  # line 531
        _.assertFalse(_.existsFile(3))  # removed when switching back to test  # line 532
        _.createFile("XXX")  # line 533
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 534
        _.assertIn("File tree has changes", out)  # line 535
        _.assertNotIn("File tree is unchanged", out)  # line 536
        _.assertIn("  * b0   'test'", out)  # line 537
        _.assertIn("    b1 'second'", out)  # line 538
        _.assertIn("modified", out)  # one branch has commits  # line 539
        _.assertIn("in sync", out)  # the other doesn't  # line 540
        sos.defaults["useChangesCommand"] = False  # because sos.main() is never called  # line 541
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # trigger repo info  # line 542
        _.assertAllIn(["Metadata format", "Content checking:    %ssize & timestamp" % sos.Fore.BLUE, "Data compression:    %sdeactivated" % sos.Fore.BLUE, "Repository mode:     %ssimple" % sos.Fore.GREEN, "Number of branches:  2"], out)  # line 543
        sos.defaults["useChangesCommand"] = True  # because sos.main() is never called  # line 544
        _.createFile(4, "xy")  # generate a file  # line 545
        sos.switch("second", ["--force"])  # avoids warning on uncommited changes, but keeps file4  # line 546
        _.assertFalse(_.existsFile(4))  # removed when forcedly switching back to test  # line 547
        _.assertTrue(_.existsFile(3))  # was restored from branch's revision r1  # line 548
        os.unlink("." + os.sep + "file1")  # remove old file1  # line 549
        sos.switch("test", ["--force"])  # should restore file1 and remove file3  # line 550
        _.assertTrue(_.existsFile(1))  # was restored from branch's revision r1  # line 551
        _.assertFalse(_.existsFile(3))  # was restored from branch's revision r1  # line 552
        sos.verbose.append(None)  # dict access necessary, as references on module-top-level are frozen  # line 553
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup", "--full"])).replace("\r", "")  # line 554
        _.assertAllIn(["Dumping revisions"], out)  # TODO cannot set verbose flag afer module loading. Use transparent wrapper instead  # line 555
        _.assertNotIn("Creating backup", out)  # line 556
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--skip-backup"])).replace("\r", "")  # line 557
        _.assertIn("Dumping revisions", out)  # line 558
        _.assertNotIn("Creating backup", out)  # line 559
        out = wrapChannels(lambda _=None: sos.dump("dumped.sos.zip", options=["--full"])).replace("\r", "")  # line 560
        _.assertAllIn(["Creating backup"], out)  # line 561
        _.assertIn("Dumping revisions", out)  # line 562
        sos.verbose.pop()  # line 563
        _.remoteIsSame()  # line 564
        os.chdir(rmteFolder)  # line 565
        try:  # line 566
            sos.status()  # line 566
        except SystemExit as E:  # line 567
            _.assertEqual(1, E.code)  # line 567

    def testAutoDetectVCS(_):  # line 569
        os.mkdir(".git")  # line 570
        sos.offline(sos.vcsBranches[sos.findSosVcsBase()[2]])  # create initial branch  # line 571
        with open(sos.metaFolder + os.sep + sos.metaFile, "r") as fd:  # line 572
            meta = fd.read()  # line 572
        _.assertTrue("\"master\"" in meta)  # line 573
        os.rmdir(".git")  # line 574

    def testUpdate(_):  # line 576
        sos.offline("trunk")  # create initial branch b0/r0  # line 577
        _.createFile(1, "x" * 100)  # line 578
        sos.commit("second")  # create b0/r1  # line 579

        sos.switch("/0")  # go back to b0/r0 - deletes file1  # line 581
        _.assertFalse(_.existsFile(1))  # line 582

        sos.update("/1")  # recreate file1  # line 584
        _.assertTrue(_.existsFile(1))  # line 585

        sos.commit("third", ["--force"])  # force because nothing to commit. should create r2 with same contents as r1, but as differential from r1, not from r0 (= no changes in meta folder)  # line 587
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2)))  # line 588
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 2, file=sos.metaFile)))  # line 589
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta data file, no differential files  # line 590

        sos.update("/1")  # do nothing, as nothing has changed  # line 592
        _.assertTrue(_.existsFile(1))  # line 593

        _.createFile(2, "y" * 100)  # line 595
#    out:str = wrapChannels(-> sos.branch("other"))  # won't comply as there are changes
#    _.assertIn("--force", out)
        sos.branch("other", options=["--force"])  # automatically including file 2 (as we are in simple mode)  # line 598
        _.assertTrue(_.existsFile(2))  # line 599
        sos.update("trunk", ["--add"])  # only add stuff  # line 600
        _.assertTrue(_.existsFile(2))  # line 601
        sos.update("trunk")  # nothing to do  # line 602
        _.assertFalse(_.existsFile(2))  # removes file not present in original branch  # line 603

        theirs = b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk"  # line 605
        _.createFile(10, theirs)  # line 606
        mine = b"a\nc\nd\ne\ng\nf\nx\nh\ny\ny\nj"  # missing "b", inserted g, modified g->x, replace x/x -> y/y, removed k  # line 607
        _.createFile(11, mine)  # line 608
        _.assertEqual((b"a\nb\nc\nd\ne\nf\ng\nh\nx\nx\nj\nk", b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.BOTH))  # completely recreated other file  # line 609
        _.assertEqual((b'a\nb\nc\nd\ne\ng\nf\ng\nh\ny\ny\nx\nx\nj\nk', b"\n"), sos.merge(filename="." + os.sep + "file10", intoname="." + os.sep + "file11", mergeOperation=sos.MergeOperation.INSERT))  # line 610

    def testUpdate2(_):  # line 612
        _.createFile("test.txt", "x" * 10)  # line 613
        sos.offline("trunk", ["--strict"])  # use strict mode, as timestamp differences are too small for testing  # line 614
        sync()  # line 615
        sos.branch("mod")  # line 616
        _.createFile("test.txt", "x" * 5 + "y" * 5)  # line 617
        sos.commit("mod")  # create b0/r1  # line 618
        sos.switch("trunk", ["--force"])  # should replace contents, force in case some other files were modified (e.g. during working on the code) TODO investigate more  # line 619
        _.assertTrue(_.existsFile("test.txt", b"x" * 10))  # line 620
        sos.update("mod")  # integrate changes TODO same with ask -> theirs  # line 621
        _.existsFile("test.txt", b"x" * 5 + b"y" * 5)  # line 622
        _.createFile("test.txt", "x" * 10)  # line 623
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask-lines"]))  # line 624
        sync()  # line 625
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 626
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 627
        sos.update("mod")  # auto-insert/removes (no intra-line conflict)  # line 628
        _.createFile("test.txt", "x" * 5 + "z" + "y" * 4)  # line 629
        sync()  # line 630
        mockInput(["t"], lambda _=None: sos.update("mod", ["--ask"]))  # same as above with interaction -> use theirs (overwrite current file state)  # line 631
        _.assertTrue(_.existsFile("test.txt", b"x" * 5 + b"y" * 5))  # line 632

    def testIsTextType(_):  # line 634
        m = sos.Metadata(".")  # line 635
        m.c.texttype = ["*.x", "*.md", "*.md.*"]  # line 636
        m.c.bintype = ["*.md.confluence"]  # line 637
        _.assertTrue(m.isTextType("ab.txt"))  # line 638
        _.assertTrue(m.isTextType("./ab.txt"))  # line 639
        _.assertTrue(m.isTextType("bc/ab.txt"))  # line 640
        _.assertFalse(m.isTextType("bc/ab."))  # line 641
        _.assertTrue(m.isTextType("23_3.x.x"))  # line 642
        _.assertTrue(m.isTextType("dfg/dfglkjdf7/test.md"))  # line 643
        _.assertTrue(m.isTextType("./test.md.pdf"))  # line 644
        _.assertFalse(m.isTextType("./test_a.md.confluence"))  # line 645

    def testEolDet(_):  # line 647
        ''' Check correct end-of-line detection. '''  # line 648
        _.assertEqual(b"\n", sos.eoldet(b"a\nb"))  # line 649
        _.assertEqual(b"\r\n", sos.eoldet(b"a\r\nb\r\n"))  # line 650
        _.assertEqual(b"\r", sos.eoldet(b"\ra\rb"))  # line 651
        _.assertAllIn(["Inconsistent", "with "], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\r\na\r\nb\n"))))  # line 652
        _.assertAllIn(["Inconsistent", "without"], wrapChannels(lambda: _.assertEqual(b"\n", sos.eoldet(b"\ra\nnb\n"))))  # line 653
        _.assertIsNone(sos.eoldet(b""))  # line 654
        _.assertIsNone(sos.eoldet(b"sdf"))  # line 655

    def testMergeClassic(_):  # line 657
        _.createFile(1, contents=b"abcdefg")  # line 658
        b = b"iabcxeg"  # type: bytes  # line 659
        _.assertEqual.__self__.maxDiff = None  # to get a full diff  # line 660
        out = wrapChannels(lambda _=None: sos.mergeClassic(b, "file1", "from", "to", 24523234, 1))  # type: str  # line 661
        _.assertAllIn(["*** from\tThu Jan  1 07:48:43 1970", "! iabcxeg", "! abcdefg"], out)  # line 662

    def testMerge(_):  # line 664
        ''' Check merge results depending on user options. '''  # line 665
        a = b"a\nb\ncc\nd"  # type: bytes  # line 666
        b = b"a\nb\nee\nd"  # type: bytes  # replaces cc by ee  # line 667
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # one-line block replacement using lineMerge  # line 668
        _.assertEqual(b"a\nb\neecc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.INSERT)[0])  # means insert changes from a into b, but don't replace  # line 669
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # means insert changes from a into b, but don't replace  # line 670
        _.assertEqual(b"a\nb\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # one-line block replacement using lineMerge  # line 671
        _.assertEqual(b"a\nb\n\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE, charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 672
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 673
        a = b"a\nb\ncc\nd"  # line 674
        b = b"a\nb\nee\nf\nd"  # replaces cc by block of two lines ee, f  # line 675
        _.assertEqual(b"a\nb\nee\nf\ncc\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.INSERT)[0])  # multi-line block replacement  # line 676
        _.assertEqual(b"a\nb\nd", sos.merge(a, b, mergeOperation=sos.MergeOperation.REMOVE)[0])  # line 677
        _.assertEqual(a, sos.merge(a, b, mergeOperation=sos.MergeOperation.BOTH)[0])  # keeps any changes in b  # line 678
# Test with change + insert
        _.assertEqual(b"a\nb fdcd d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.INSERT)[0])  # line 680
        _.assertEqual(b"a\nb d d\ne", sos.merge(b"a\nb cd d\ne", b"a\nb fdd d\ne", charMergeOperation=sos.MergeOperation.REMOVE)[0])  # line 681
# Test interactive merge
        a = b"a\nb\nb\ne"  # block-wise replacement  # line 683
        b = b"a\nc\ne"  # line 684
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 685
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, mergeOperation=sos.MergeOperation.ASK)[0]))  # line 686
        a = b"a\nb\ne"  # intra-line merge  # line 687
        _.assertEqual(b, mockInput(["i"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 688
        _.assertEqual(a, mockInput(["t"], lambda _=None: sos.merge(a, b, charMergeOperation=sos.MergeOperation.ASK)[0]))  # line 689
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaacaaa")[0])  # line 690
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aaaaaaa")[0])  # line 691
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"aabaacaaaa")[0])  # line 692
        _.assertEqual(b"aabaacaaa", sos.merge(b"aabaacaaa", b"xaaaadaaac")[0])  # line 693

    def testMergeEol(_):  # line 695
        _.assertEqual(b"\r\n", sos.merge(b"a\nb", b"a\r\nb")[1])  # line 696
        _.assertIn("Differing EOL-styles", wrapChannels(lambda _=None: sos.merge(b"a\nb", b"a\r\nb")))  # expects a warning  # line 697
        _.assertIn(b"a\r\nb", sos.merge(b"a\nb", b"a\r\nb")[0])  # when in doubt, use "mine" CR-LF  # line 698
        _.assertIn(b"a\nb", sos.merge(b"a\nb", b"a\r\nb", eol=True)[0])  # line 699
        _.assertEqual(b"\n", sos.merge(b"a\nb", b"a\r\nb", eol=True)[1])  # line 700

    def testPickyMode(_):  # line 702
        ''' Confirm that picky mode reset tracked patterns after commits. '''  # line 703
        sos.offline("trunk", None, ["--picky"])  # line 704
        changes = sos.changes()  # line 705
        _.assertEqual(0, len(changes.additions))  # do not list any existing file as an addition  # line 706
        out = wrapChannels(lambda _=None: sos.add(".", "./file?", options=["--force", "--relative"]))  # type: str  # line 707
        _.assertAllIn(["Added tracking pattern", "'%s'" % "file?", "'.'"], out)  # line 708
        _.createFile(1, "aa")  # line 709
        sos.commit("First")  # add one file  # line 710
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # line 711
        _.createFile(2, "b")  # line 712
        try:  # add nothing, because picky  # line 713
            sos.commit("Second")  # add nothing, because picky  # line 713
        except:  # line 714
            pass  # line 714
        sos.add(".", "./file?")  # line 715
        sos.commit("Third")  # line 716
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # line 717
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 718
        _.assertIn("    r0", out)  # line 719
        sys.argv.extend(["-n", "2"])  # We cannot use the opions array for named argument options  # line 720
        out = wrapChannels(lambda _=None: sos.log()).replace("\r", "")  # line 721
        sys.argv.pop()  # line 722
        sys.argv.pop()  # line 722
        _.assertNotIn("    r0", out)  # because number of log lines was limited by argument  # line 723
        _.assertIn("    r1", out)  # line 724
        _.assertIn("  * r2", out)  # line 725
        try:  # line 726
            sos.config(["set", "logLines", "1"], options=["--local"])  # line 726
        except SystemExit as E:  # line 727
            _.assertEqual(0, E.code)  # line 727
        out = wrapChannels(lambda _=None: sos.log([])).replace("\r", "")  # line 728
        _.assertNotIn("    r0", out)  # because number of log lines was limited  # line 729
        _.assertNotIn("    r1", out)  # line 730
        _.assertIn("  * r2", out)  # line 731
        _.createFile(3, prefix="sub")  # line 732
        sos.add("sub", "sub/file?")  # line 733
        changes = sos.changes()  # line 734
        _.assertEqual(1, len(changes.additions))  # line 735
        _.assertTrue("sub/file3" in changes.additions)  # line 736

    def testTrackedSubfolder(_):  # line 738
        ''' See if patterns for files in sub folders are picked up correctly. '''  # line 739
        os.mkdir("." + os.sep + "sub")  # line 740
        sos.offline("trunk", None, ["--track"])  # line 741
        _.createFile(1, "x")  # line 742
        _.createFile(1, "x", prefix="sub")  # line 743
        sos.add(".", "./file?")  # add glob pattern to track  # line 744
        sos.commit("First")  # line 745
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 746
        sos.add(".", "sub/file?")  # add glob pattern to track  # line 747
        sos.commit("Second")  # one new file + meta  # line 748
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 749
        os.unlink("file1")  # remove from basefolder  # line 750
        _.createFile(2, "y")  # line 751
        sos.remove(".", "sub/file?")  # line 752
        try:  # TODO check more textual details here  # line 753
            sos.remove(".", "sub/bla")  # TODO check more textual details here  # line 753
            _.fail("Expected exit")  # TODO check more textual details here  # line 753
        except SystemExit as E:  # line 754
            _.assertEqual(1, E.code)  # line 754
        sos.commit("Third")  # line 755
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta  # line 756
# TODO also check if /file1 and sub/file1 were removed from index

    def testTrackedMode(_):  # line 759
        ''' Difference in semantics vs simple mode:
          - For remote/other branch we can only know and consider tracked files, thus ignoring all complexity stemming from handling addition of untracked files.
          - For current branch, we can take into account tracked and untracked ones, in theory, but it doesn't make sense.
        In conclusion, using the union of tracking patterns from both sides to find affected files makes sense, but disallow deleting files not present in remote branch.
    '''  # line 764
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 765
        _.createFile(1)  # line 766
        _.createFile("a123a")  # untracked file "a123a"  # line 767
        sos.add(".", "./file?")  # add glob tracking pattern  # line 768
        sos.commit("second")  # versions "file1"  # line 769
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # one new file + meta file  # line 770
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 771
        _.assertTrue(any(("|" in o and "./file?" in o for o in out.split("\n"))))  # line 772

        _.createFile(2)  # untracked file "file2"  # line 774
        sos.commit("third")  # versions "file2"  # line 775
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # one new file + meta file  # line 776

        os.mkdir("." + os.sep + "sub")  # line 778
        _.createFile(3, prefix="sub")  # untracked file "sub/file3"  # line 779
        sos.commit("fourth", ["--force"])  # no tracking pattern matches the subfolder  # line 780
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 3))))  # meta file only, no other tracked path/file  # line 781

        sos.branch("Other")  # second branch containing file1 and file2 tracked by "./file?"  # line 783
        sos.remove(".", "./file?")  # remove tracking pattern, but don't touch previously created and versioned files  # line 784
        sos.add(".", "./a*a")  # add tracking pattern  # line 785
        changes = sos.changes()  # should pick up addition only, because tracked, but not the deletion, as not tracked anymore  # line 786
        _.assertEqual(0, len(changes.modifications))  # line 787
        _.assertEqual(0, len(changes.deletions))  # not tracked anymore, but contained in version history and not removed  # line 788
        _.assertEqual(1, len(changes.additions))  # detected one addition "a123a", but won't recognize untracking files as deletion  # line 789

        sos.commit("Second_2")  # line 791
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(1, 1))))  # "a123a" + meta file  # line 792
        _.existsFile(1, b"x" * 10)  # line 793
        _.existsFile(2, b"x" * 10)  # line 794

        sos.switch("test")  # go back to first branch - tracks only "file?", but not "a*a"  # line 796
        _.existsFile(1, b"x" * 10)  # line 797
        _.existsFile("a123a", b"x" * 10)  # line 798

        sos.update("Other")  # integrate tracked files and tracking pattern from second branch into working state of master branch  # line 800
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 801
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 802

        _.createFile("axxxa")  # new file that should be tracked on "test" now that we integrated "Other"  # line 804
        sos.commit("fifth")  # create new revision after integrating updates from second branch  # line 805
        _.assertEqual(3, len(os.listdir(sos.revisionFolder(0, 4))))  # one new file from other branch + one new in current folder + meta file  # line 806
        sos.switch("Other")  # switch back to just integrated branch that tracks only "a*a" - shouldn't do anything  # line 807
        _.assertTrue(os.path.exists("." + os.sep + "file1"))  # line 808
        _.assertTrue(os.path.exists("." + os.sep + "a123a"))  # line 809
        _.assertFalse(os.path.exists("." + os.sep + "axxxa"))  # because tracked in both branches, but not present in other -> delete in file tree  # line 810
# TODO test switch --meta

    def testLsTracked(_):  # line 813
        sos.offline("test", options=["--track"])  # set up repo in tracking mode (SVN- or gitless-style)  # line 814
        _.createFile(1)  # line 815
        _.createFile("foo")  # line 816
        sos.add(".", "./file*")  # capture one file  # line 817
        sos.ls()  # line 818
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # type: str  # line 819
        _.assertInAny("TRK file1  (file*)", out)  # line 820
        _.assertNotInAny("... file1  (file*)", out)  # line 821
        _.assertInAny("    foo", out)  # line 822
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls(options=["--patterns"])).replace("\r", ""), "\n")  # line 823
        _.assertInAny("TRK file*", out)  # line 824
        _.createFile("a", prefix="sub")  # line 825
        sos.add("sub", "sub/a")  # line 826
        sos.ls("sub")  # line 827
        _.assertInAny("TRK a  (a)", sos.safeSplit(wrapChannels(lambda _=None: sos.ls("sub")).replace("\r", ""), "\n"))  # line 828

    def testLineMerge(_):  # line 830
        _.assertEqual("xabc", sos.lineMerge("xabc", "a bd"))  # line 831
        _.assertEqual("xabxxc", sos.lineMerge("xabxxc", "a bd"))  # line 832
        _.assertEqual("xa bdc", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.INSERT))  # line 833
        _.assertEqual("ab", sos.lineMerge("xabc", "a bd", mergeOperation=sos.MergeOperation.REMOVE))  # line 834

    def testCompression(_):  # TODO test output ratio/advantage, also depending on compress flag set or not  # line 836
        _.createFile(1)  # line 837
        sos.offline("master", options=["--force"])  # line 838
        out = wrapChannels(lambda _=None: sos.changes(options=['--progress'])).replace("\r", "").split("\n")  # type: str  # line 839
        _.assertFalse(any(("Compression advantage" in line for line in out)))  # simple mode should always print this to stdout  # line 840
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 0, file="b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa"), b"x" * 10))  # line 841
        setRepoFlag("compress", True)  # was plain = uncompressed before  # line 842
        _.createFile(2)  # line 843
        out = wrapChannels(lambda _=None: sos.commit("Added file2", options=['--progress'])).replace("\r", "").split("\n")  # line 844
        _.assertTrue(any(("Compression advantage" in line for line in out)))  # line 845
        _.assertTrue(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2")))  # exists  # line 846
        _.assertFalse(_.existsFile(sos.revisionFolder(0, 1, file="03b69bc801ae11f1ff2a71a50f165996d0ad681b4f822df13329a27e53f0fcd2"), b"x" * 10))  # but is compressed instead  # line 847

    def testLocalConfig(_):  # line 849
        sos.offline("bla", options=[])  # line 850
        try:  # line 851
            sos.config(["set", "ignores", "one;two"], options=["--local"])  # line 851
        except SystemExit as E:  # line 852
            _.assertEqual(0, E.code)  # line 852
        _.assertTrue(checkRepoFlag("ignores", value=["one", "two"]))  # line 853

    def testConfigVariations(_):  # line 855
        def makeRepo():  # line 856
            try:  # line 857
                os.unlink("file1")  # line 857
            except:  # line 858
                pass  # line 858
            sos.offline("master", options=["--force"])  # line 859
            _.createFile(1)  # line 860
            sos.commit("Added file1")  # line 861
        try:  # line 862
            sos.config(["set", "strict", "on"])  # line 862
        except SystemExit as E:  # line 863
            _.assertEqual(0, E.code)  # line 863
        makeRepo()  # line 864
        _.assertTrue(checkRepoFlag("strict", True))  # line 865
        try:  # line 866
            sos.config(["set", "strict", "off"])  # line 866
        except SystemExit as E:  # line 867
            _.assertEqual(0, E.code)  # line 867
        makeRepo()  # line 868
        _.assertTrue(checkRepoFlag("strict", False))  # line 869
        try:  # line 870
            sos.config(["set", "strict", "yes"])  # line 870
        except SystemExit as E:  # line 871
            _.assertEqual(0, E.code)  # line 871
        makeRepo()  # line 872
        _.assertTrue(checkRepoFlag("strict", True))  # line 873
        try:  # line 874
            sos.config(["set", "strict", "no"])  # line 874
        except SystemExit as E:  # line 875
            _.assertEqual(0, E.code)  # line 875
        makeRepo()  # line 876
        _.assertTrue(checkRepoFlag("strict", False))  # line 877
        try:  # line 878
            sos.config(["set", "strict", "1"])  # line 878
        except SystemExit as E:  # line 879
            _.assertEqual(0, E.code)  # line 879
        makeRepo()  # line 880
        _.assertTrue(checkRepoFlag("strict", True))  # line 881
        try:  # line 882
            sos.config(["set", "strict", "0"])  # line 882
        except SystemExit as E:  # line 883
            _.assertEqual(0, E.code)  # line 883
        makeRepo()  # line 884
        _.assertTrue(checkRepoFlag("strict", False))  # line 885
        try:  # line 886
            sos.config(["set", "strict", "true"])  # line 886
        except SystemExit as E:  # line 887
            _.assertEqual(0, E.code)  # line 887
        makeRepo()  # line 888
        _.assertTrue(checkRepoFlag("strict", True))  # line 889
        try:  # line 890
            sos.config(["set", "strict", "false"])  # line 890
        except SystemExit as E:  # line 891
            _.assertEqual(0, E.code)  # line 891
        makeRepo()  # line 892
        _.assertTrue(checkRepoFlag("strict", False))  # line 893
        try:  # line 894
            sos.config(["set", "strict", "enable"])  # line 894
        except SystemExit as E:  # line 895
            _.assertEqual(0, E.code)  # line 895
        makeRepo()  # line 896
        _.assertTrue(checkRepoFlag("strict", True))  # line 897
        try:  # line 898
            sos.config(["set", "strict", "disable"])  # line 898
        except SystemExit as E:  # line 899
            _.assertEqual(0, E.code)  # line 899
        makeRepo()  # line 900
        _.assertTrue(checkRepoFlag("strict", False))  # line 901
        try:  # line 902
            sos.config(["set", "strict", "enabled"])  # line 902
        except SystemExit as E:  # line 903
            _.assertEqual(0, E.code)  # line 903
        makeRepo()  # line 904
        _.assertTrue(checkRepoFlag("strict", True))  # line 905
        try:  # line 906
            sos.config(["set", "strict", "disabled"])  # line 906
        except SystemExit as E:  # line 907
            _.assertEqual(0, E.code)  # line 907
        makeRepo()  # line 908
        _.assertTrue(checkRepoFlag("strict", False))  # line 909
        try:  # line 910
            sos.config(["set", "strict", "nope"])  # line 910
            _.fail()  # line 910
        except SystemExit as E:  # line 911
            _.assertEqual(1, E.code)  # line 911

    def testLsSimple(_):  # line 913
        _.createFile(1)  # line 914
        _.createFile("foo")  # line 915
        _.createFile("ign1")  # line 916
        _.createFile("ign2")  # line 917
        _.createFile("bar", prefix="sub")  # line 918
        sos.offline("test")  # set up repo in tracking mode (SVN- or gitless-style)  # line 919
        try:  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 920
            sos.config(["set", "ignores", "ign1"])  # define an ignore pattern. HINT this is stored in a local test folder, not in the real global configuration!  # line 920
        except SystemExit as E:  # line 921
            _.assertEqual(0, E.code)  # line 921
        try:  # additional ignore pattern  # line 922
            sos.config(["add", "ignores", "ign2"])  # additional ignore pattern  # line 922
        except SystemExit as E:  # line 923
            _.assertEqual(0, E.code)  # line 923
        try:  # define a list of ignore patterns  # line 924
            sos.config(["set", "ignoresWhitelist", "ign1;ign2"])  # define a list of ignore patterns  # line 924
        except SystemExit as E:  # line 925
            _.assertEqual(0, E.code)  # line 925
        out = wrapChannels(lambda _=None: sos.config(["show"])).replace("\r", "")  # type: str  # line 926
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 927
        out = wrapChannels(lambda _=None: sos.config(["show", "ignores"])).replace("\r", "")  # line 928
        _.assertIn("             ignores [global]  ['ign1', 'ign2']", out)  # line 929
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 930
        _.assertInAny('    file1', out)  # line 931
        _.assertInAny('    ign1', out)  # line 932
        _.assertInAny('    ign2', out)  # line 933
        _.assertNotIn('DIR sub', out)  # line 934
        _.assertNotIn('    bar', out)  # line 935
        out = wrapChannels(lambda _=None: sos.ls(options=["--recursive"])).replace("\r", "")  # line 936
        _.assertIn('DIR sub', out)  # line 937
        _.assertIn('    bar', out)  # line 938
        try:  # line 939
            sos.config(["rm", "foo", "bar"])  # line 939
            _.fail()  # line 939
        except SystemExit as E:  # line 940
            _.assertEqual(1, E.code)  # line 940
        try:  # line 941
            sos.config(["rm", "ignores", "foo"])  # line 941
            _.fail()  # line 941
        except SystemExit as E:  # line 942
            _.assertEqual(1, E.code)  # line 942
        try:  # line 943
            sos.config(["rm", "ignores", "ign1"])  # line 943
        except SystemExit as E:  # line 944
            _.assertEqual(0, E.code)  # line 944
        try:  # remove ignore pattern  # line 945
            sos.config(["unset", "ignoresWhitelist"])  # remove ignore pattern  # line 945
        except SystemExit as E:  # line 946
            _.assertEqual(0, E.code)  # line 946
        out = sos.safeSplit(wrapChannels(lambda _=None: sos.ls()).replace("\r", ""), "\n")  # line 947
        _.assertInAny('    ign1', out)  # line 948
        _.assertInAny('IGN ign2', out)  # line 949
        _.assertNotInAny('    ign2', out)  # line 950

    def testWhitelist(_):  # line 952
# TODO test same for simple mode
        _.createFile(1)  # line 954
        sos.defaults.ignores[:] = ["file*"]  # replace in-place  # line 955
        sos.offline("xx", options=["--track", "--strict"])  # because nothing to commit due to ignore pattern  # line 956
        sos.add(".", "./file*")  # add tracking pattern for "file1"  # line 957
        sos.commit(options=["--force"])  # attempt to commit the file  # line 958
        _.assertEqual(1, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta data, file1 was ignored  # line 959
        try:  # Exit because dirty  # line 960
            sos.online()  # Exit because dirty  # line 960
            _.fail()  # Exit because dirty  # line 960
        except:  # exception expected  # line 961
            pass  # exception expected  # line 961
        _.createFile("x2")  # add another change  # line 962
        sos.add(".", "./x?")  # add tracking pattern for "file1"  # line 963
        try:  # force beyond dirty flag check  # line 964
            sos.online(["--force"])  # force beyond dirty flag check  # line 964
            _.fail()  # force beyond dirty flag check  # line 964
        except:  # line 965
            pass  # line 965
        sos.online(["--force", "--force"])  # force beyond file tree modifications check  # line 966
        _.assertFalse(os.path.exists(sos.metaFolder))  # line 967

        _.createFile(1)  # line 969
        sos.defaults.ignoresWhitelist[:] = ["file*"]  # line 970
        sos.offline("xx", None, ["--track"])  # line 971
        sos.add(".", "./file*")  # line 972
        sos.commit()  # should NOT ask for force here  # line 973
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # meta data and "file1", file1 was whitelisted  # line 974

    def testRemove(_):  # line 976
        _.createFile(1, "x" * 100)  # line 977
        sos.offline("trunk")  # line 978
        try:  # line 979
            sos.destroy("trunk")  # line 979
            _fail()  # line 979
        except:  # line 980
            pass  # line 980
        _.createFile(2, "y" * 10)  # line 981
        sos.branch("added")  # creates new branch, writes repo metadata, and therefore creates backup copy  # line 982
        sos.destroy("trunk")  # line 983
        _.assertAllIn([sos.metaFile, sos.metaBack, "b0_last", "b1"], os.listdir("." + os.sep + sos.metaFolder))  # line 984
        _.assertTrue(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b1"))  # line 985
        _.assertFalse(os.path.exists("." + os.sep + sos.metaFolder + os.sep + "b0"))  # line 986
        sos.branch("next")  # line 987
        _.createFile(3, "y" * 10)  # make a change  # line 988
        sos.destroy("added", "--force")  # should succeed  # line 989

    def testFastBranchingOnEmptyHistory(_):  # line 991
        ''' Test fast branching without revisions and with them. '''  # line 992
        sos.offline(options=["--strict", "--compress"])  # b0  # line 993
        sos.branch("", "", options=["--fast", "--last"])  # b1  # line 994
        sos.branch("", "", options=["--fast", "--last"])  # b2  # line 995
        sos.branch("", "", options=["--fast", "--last"])  # b3  # line 996
        sos.destroy("2")  # line 997
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # type: str  # line 998
        _.assertIn("b0 'trunk' @", out)  # line 999
        _.assertIn("b1         @", out)  # line 1000
        _.assertIn("b3         @", out)  # line 1001
        _.assertNotIn("b2         @", out)  # line 1002
        sos.branch("", "")  # non-fast branching of b4  # line 1003
        _.createFile(1)  # line 1004
        _.createFile(2)  # line 1005
        sos.commit("")  # line 1006
        sos.branch("", "", options=["--fast", "--last"])  # b5  # line 1007
        sos.destroy("4")  # line 1008
        out = wrapChannels(lambda _=None: sos.status()).replace("\r", "")  # line 1009
        _.assertIn("b0 'trunk' @", out)  # line 1010
        _.assertIn("b1         @", out)  # line 1011
        _.assertIn("b3         @", out)  # line 1012
        _.assertIn("b5         @", out)  # line 1013
        _.assertNotIn("b2         @", out)  # line 1014
        _.assertNotIn("b4         @", out)  # line 1015
# TODO add more files and branch again

    def testUsage(_):  # line 1018
        try:  # TODO expect sys.exit(0)  # line 1019
            sos.usage()  # TODO expect sys.exit(0)  # line 1019
            _.fail()  # TODO expect sys.exit(0)  # line 1019
        except:  # line 1020
            pass  # line 1020
        try:  # TODO expect sys.exit(0)  # line 1021
            sos.usage("help")  # TODO expect sys.exit(0)  # line 1021
            _.fail()  # TODO expect sys.exit(0)  # line 1021
        except:  # line 1022
            pass  # line 1022
        try:  # TODO expect sys.exit(0)  # line 1023
            sos.usage("help", verbose=True)  # TODO expect sys.exit(0)  # line 1023
            _.fail()  # TODO expect sys.exit(0)  # line 1023
        except:  # line 1024
            pass  # line 1024
        try:  # line 1025
            sos.usage(version=True)  # line 1025
            _.fail()  # line 1025
        except:  # line 1026
            pass  # line 1026
        try:  # line 1027
            sos.usage(version=True)  # line 1027
            _.fail()  # line 1027
        except:  # line 1028
            pass  # line 1028

    def testOnlyExcept(_):  # line 1030
        ''' Test blacklist glob rules. '''  # line 1031
        sos.offline(options=["--track"])  # line 1032
        _.createFile("a.1")  # line 1033
        _.createFile("a.2")  # line 1034
        _.createFile("b.1")  # line 1035
        _.createFile("b.2")  # line 1036
        sos.add(".", "./a.?")  # line 1037
        sos.add(".", "./?.1", negative=True)  # line 1038
        out = wrapChannels(lambda _=None: sos.commit())  # type: str  # line 1039
        _.assertIn("ADD ./a.2", out)  # line 1040
        _.assertNotIn("ADD ./a.1", out)  # line 1041
        _.assertNotIn("ADD ./b.1", out)  # line 1042
        _.assertNotIn("ADD ./b.2", out)  # line 1043

    def testOnly(_):  # line 1045
        _.assertEqual((_coconut.frozenset(("./A", "x/B")), _coconut.frozenset(("./C",)), ["bla"]), sos.parseArgumentOptions(".", ["abc", "def", "--only", "A", "--x", "--only", "x/B", "--except", "C", "--remote", "bla", "--only"]))  # line 1046
        _.assertEqual(_coconut.frozenset(("B",)), sos.conditionalIntersection(_coconut.frozenset(("A", "B", "C")), _coconut.frozenset(("B", "D"))))  # line 1047
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(_coconut.frozenset(), _coconut.frozenset(("B", "D"))))  # line 1048
        _.assertEqual(_coconut.frozenset(("B", "D")), sos.conditionalIntersection(None, _coconut.frozenset(("B", "D"))))  # line 1049
        sos.offline(options=["--track", "--strict"])  # line 1050
        _.createFile(1)  # line 1051
        _.createFile(2)  # line 1052
        sos.add(".", "./file1")  # line 1053
        sos.add(".", "./file2")  # line 1054
        sos.commit(onlys=_coconut.frozenset(("./file1",)))  # line 1055
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 1))))  # only meta and file1  # line 1056
        sos.commit()  # adds also file2  # line 1057
        _.assertEqual(2, len(os.listdir(sos.revisionFolder(0, 2))))  # only meta and file1  # line 1058
        _.createFile(1, "cc")  # modify both files  # line 1059
        _.createFile(2, "dd")  # line 1060
        try:  # line 1061
            sos.config(["set", "texttype", "file2"])  # line 1061
        except SystemExit as E:  # line 1062
            _.assertEqual(0, E.code)  # line 1062
        changes = sos.changes(excps=_coconut.frozenset(("./file1",)))  # line 1063
        _.assertEqual(1, len(changes.modifications))  # only file2  # line 1064
        _.assertTrue("./file2" in changes.modifications)  # line 1065
        _.assertAllIn(["DIF ./file2", "<No newline>"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # line 1066
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1", "MOD ./file2"], wrapChannels(lambda _=None: sos.diff("/", onlys=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1067
        _.assertIn("MOD ./file1", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # MOD vs. DIF  # line 1068
        _.assertNotIn("MOD ./file2", wrapChannels(lambda _=None: sos.diff("/", excps=_coconut.frozenset(("./file2",)))))  # line 1069

    def testEmptyFiles(_):  # line 1071
        sos.offline()  # line 1072
        _.createFile(1, "")  # empty file  # line 1073
        sos.commit()  # line 1074
        changes = sos.changes()  # line 1075
        _.assertEqual(0, len(changes.additions) + len(changes.modifications) + len(changes.deletions))  # line 1076

        setRepoFlag("strict", True)  # line 1078
        changes = sos.changes()  # line 1079
        _.assertEqual(1, len(changes.modifications))  # because hash was set to None in simple mode  # line 1080
        sos.commit()  # commit now with hash computation  # line 1081
        setRepoFlag("strict", False)  # line 1082

        time.sleep(FS_PRECISION)  # line 1084
        _.createFile(1, "")  # touch file  # line 1085
        changes = sos.changes()  # line 1086
        _.assertEqual(1, len(changes.modifications))  # since modified timestamp  # line 1087

    def testDiff(_):  # line 1089
        try:  # manually mark this file as "textual"  # line 1090
            sos.config(["set", "texttype", "file1"])  # manually mark this file as "textual"  # line 1090
        except SystemExit as E:  # line 1091
            _.assertEqual(0, E.code)  # line 1091
        sos.offline(options=["--strict"])  # line 1092
        _.createFile(1)  # line 1093
        _.createFile(2)  # line 1094
        sos.commit()  # line 1095
        _.createFile(1, "sdfsdgfsdf")  # line 1096
        _.createFile(2, "12343")  # line 1097
        sos.commit()  # line 1098
        _.createFile(1, "foobar")  # line 1099
        _.createFile(3)  # line 1100
        out = wrapChannels(lambda _=None: sos.diff("/-2"))  # type: str  # compare with r1 (second counting from last which is r2)  # line 1101
        _.assertIn("ADD ./file3", out)  # line 1102
        _.assertAllIn(["MOD ./file2", "DIF ./file1  <No newline>", "-~- 0 |xxxxxxxxxx|", "+~+ 0 |foobar|"], out)  # line 1103
        _.assertAllNotIn(["MOD ./file1", "DIF ./file1"], wrapChannels(lambda _=None: sos.diff("/-2", onlys=_coconut.frozenset(("./file2",)))))  # line 1104

    def testReorderRenameActions(_):  # line 1106
        result = sos.reorderRenameActions([("123", "312"), ("312", "132"), ("321", "123")], exitOnConflict=False)  # type: Tuple[str, str]  # line 1107
        _.assertEqual([("312", "132"), ("123", "312"), ("321", "123")], result)  # line 1108
        try:  # line 1109
            sos.reorderRenameActions([("123", "312"), ("312", "123")], exitOnConflict=True)  # line 1109
            _.fail()  # line 1109
        except:  # line 1110
            pass  # line 1110

    def testPublish(_):  # line 1112
        pass  # TODO how to test without modifying anything underlying? probably use --test flag or similar?  # line 1113

    def testColorFlag(_):  # line 1115
        sos.offline()  # line 1116
        _.createFile(1)  # line 1117
#    setRepoFlag("useColorOutput", False, toConfig = True)
#    sos.Metadata.singleton = None  # for new read of configuration
        sos.enableColor(False)  # line 1120
        out = wrapChannels(lambda _=None: sos.changes(options="--verbose")).replace("\r\n", "\n").split("\n")  # type: List[str]  # line 1121
        _.assertTrue(any((line.startswith(sos.usage.MARKER_TEXT + "Changes of file tree") for line in out)))  # line 1122
#    setRepoFlag("useColorOutput", True,  toConfig = True)
#    sos.Metadata.singleton = None
        sos.enableColor(True)  # line 1125
        out = wrapChannels(lambda _=None: sos.changes(options="--verbose")).replace("\r\n", "\n").split("\n")  # line 1126
        _.assertTrue(any((line.startswith(sos.utility.MARKER_COLOR + "Changes of file tree") for line in out)))  # because it may start with a color code  # line 1127

    def testMove(_):  # line 1129
        ''' Move primarily modifies tracking patterns and moves files around accordingly. '''  # line 1130
        sos.offline(options=["--strict", "--track"])  # line 1131
        _.createFile(1)  # line 1132
        sos.add(".", "./file?")  # line 1133
# assert error when source folder is missing
        out = wrapChannels(lambda _=None: sos.move("sub", "sub/file?", ".", "./?file"))  # type: str  # line 1135
        _.assertIn("Source folder doesn't exist", out)  # line 1136
        _.assertIn("EXIT CODE 1", out)  # line 1137
# if target folder missing: create it and move matching files into it
        sos.move(".", "./file?", "sub", "sub/file?")  # line 1139
        _.assertTrue(os.path.exists("sub"))  # line 1140
        _.assertTrue(os.path.exists("sub/file1"))  # line 1141
        _.assertFalse(os.path.exists("file1"))  # line 1142
# test move back to previous location, plus rename the file
        sos.move("sub", "sub/file?", ".", "./?file")  # line 1144
        _.assertTrue(os.path.exists("1file"))  # line 1145
        _.assertFalse(os.path.exists("sub/file1"))  # line 1146
# assert error when nothing matches source pattern
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*"))  # line 1148
        _.assertIn("No files match the specified file pattern", out)  # line 1149
        _.assertIn("EXIT CODE", out)  # line 1150
        sos.add(".", "./*")  # add catch-all tracking pattern to root folder  # line 1151
        out = wrapChannels(lambda _=None: sos.move(".", "./a*", ".", "./b*", options=["--force"]))  # line 1152
        _.assertIn("  './*' matches 3 files", out)  # line 1153
        _.assertIn("EXIT CODE", out)  # line 1154
# test rename no conflict
        _.createFile(1)  # line 1156
        _.createFile(2)  # line 1157
        _.createFile(3)  # line 1158
        sos.add(".", "./file*")  # line 1159
        sos.remove(".", "./*")  # line 1160
        try:  # define an ignore pattern  # line 1161
            sos.config(["set", "ignores", "file3;file4"])  # define an ignore pattern  # line 1161
        except SystemExit as E:  # line 1162
            _.assertEqual(0, E.code)  # line 1162
        try:  # line 1163
            sos.config(["set", "ignoresWhitelist", "file3"])  # line 1163
        except SystemExit as E:  # line 1164
            _.assertEqual(0, E.code)  # line 1164
        sos.move(".", "./file*", ".", "./fi*le")  # should only move not ignored files files  # line 1165
        _.assertTrue(all((os.path.exists("fi%dle" % i) for i in range(1, 4))))  # line 1166
        _.assertTrue(all((not os.path.exists("file%d" % i) for i in range(1, 4))))  # line 1167
        _.assertFalse(os.path.exists("fi4le"))  # line 1168
# test rename solvable conflicts
        [_.createFile("%s-%s-%s" % tuple((c for c in n))) for n in ["312", "321", "123", "231"]]  # line 1170
#    sos.move("?-?-?")
# test rename unsolvable conflicts
# test --soft option
        sos.remove(".", "./?file")  # untrack pattern, which was renamed before  # line 1174
        sos.add(".", "./?a?b", ["--force"])  # line 1175
        sos.move(".", "./?a?b", ".", "./a?b?", ["--force", "--soft"])  # line 1176
        _.createFile("1a2b")  # should not be tracked  # line 1177
        _.createFile("a1b2")  # should be tracked  # line 1178
        sos.commit()  # line 1179
        _.assertEqual(5, len(os.listdir(sos.revisionFolder(0, 1))))  # meta, a1b2, fi[1-3]le  # line 1180
        _.assertTrue(os.path.exists(sos.revisionFolder(0, 1, file="93b38f90892eb5c57779ca9c0b6fbdf6774daeee3342f56f3e78eb2fe5336c50")))  # a1b2  # line 1181
        _.createFile("1a1b1")  # line 1182
        _.createFile("1a1b2")  # line 1183
        sos.add(".", "./?a?b*")  # line 1184
# test target pattern exists
        out = wrapChannels(lambda _=None: sos.move(".", "./?a?b*", ".", "./z?z?"))  # line 1186
        _.assertIn("not unique", out)  # line 1187
# TODO only rename if actually any files are versioned? or simply what is currently alife?
# TODO add test if two single question marks will be moved into adjacent characters

    def testAskUpdate(_):  # line 1191
        _.createFile(1)  # line 1192
        _.createFile(3)  # line 1193
        _.createFile(5)  # line 1194
        sos.offline()  # branch 0: only file1  # line 1195
        sos.branch()  # line 1196
        os.unlink("file1")  # line 1197
        os.unlink("file3")  # line 1198
        os.unlink("file5")  # line 1199
        _.createFile(2)  # line 1200
        _.createFile(4)  # line 1201
        _.createFile(6)  # line 1202
        sos.commit()  # branch 1: only file2  # line 1203
        sos.switch("0/")  # line 1204
        mockInput(["y", "a", "y", "a"], lambda _=None: sos.update("1/", ["--ask"]))  # line 1205
        _.assertFalse(_.existsFile(1))  # line 1206
        _.assertFalse(_.existsFile(3))  # line 1207
        _.assertFalse(_.existsFile(5))  # line 1208
        _.assertTrue(_.existsFile(2))  # line 1209
        _.assertTrue(_.existsFile(4))  # line 1210
        _.assertTrue(_.existsFile(6))  # line 1211

    def testMoveDetection(_):  # line 1213
        _.createFile(1, "bla")  # line 1214
        sos.offline()  # line 1215
        os.mkdir("sub1")  # line 1216
        os.mkdir("sub2")  # line 1217
        shutil.copy2("file1", "sub1" + os.sep + "file_I")  # line 1218
        shutil.move("file1", "sub2")  # line 1219
        out = wrapChannels(lambda _=None: sos.changes())  # type: str  # line 1220
        _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,  # line 1221
        _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added  # line 1222
        sos.commit("Moved the file")  # line 1223
#    out = wrapChannels(-> sos.log(["--changes"]))  # TODO moves detection not yet implemented
#    _.assertIn("MOV sub2/file1  <-  ./file1", out)  # ensure that the correctly named while is detected as a move,
#    _.assertIn("ADD sub1/file_I", out)  # while the differently named (same file) is detected as added
        _.createFile(1, "bla", prefix="sub")  # line 1227

    def testHashCollision(_):  # line 1229
        old = sos.Metadata.findChanges  # line 1230
        @_coconut_tco  # line 1231
        def patched(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[sos.ChangeSet, _coconut.typing.Optional[str]]':  # line 1231
            import collections  # used only in this method  # line 1232
            write = branch is not None and revision is not None  # line 1233
            if write:  # line 1234
                try:  # line 1235
                    os.makedirs(sos.encode(sos.revisionFolder(branch, revision, base=_.root)))  # line 1235
                except FileExistsError:  # HINT "try" only necessary for hash collision *test code* (!)  # line 1236
                    pass  # HINT "try" only necessary for hash collision *test code* (!)  # line 1236
            return _coconut_tail_call(old, _, branch, revision, checkContent, inverse, considerOnly, dontConsider, progress)  # line 1237
        sos.Metadata.findChanges = patched  # monkey-patch  # line 1238
        sos.offline()  # line 1239
        _.createFile(1)  # line 1240
        os.mkdir(sos.revisionFolder(0, 1))  # line 1241
        _.createFile("b9ee10a87f612e299a6eb208210bc0898092a64c48091327cc2aaeee9b764ffa", prefix=sos.revisionFolder(0, 1))  # hashed file name for not-yet-committed file1  # line 1242
        _.createFile(1)  # line 1243
        try:  # line 1244
            sos.commit()  # line 1244
            _.fail("Expected system exit due to hash collision detection")  # line 1244
        except SystemExit as E:  # HINT exit is implemented in utility.hashFile  # line 1245
            _.assertEqual(1, E.code)  # HINT exit is implemented in utility.hashFile  # line 1245
        sos.Metadata.findChanges = old  # revert monkey patch  # line 1246

    def testFindBase(_):  # line 1248
        old = os.getcwd()  # line 1249
        try:  # line 1250
            os.mkdir("." + os.sep + ".git")  # line 1251
            os.makedirs("." + os.sep + "a" + os.sep + sos.metaFolder)  # line 1252
            os.makedirs("." + os.sep + "a" + os.sep + "b")  # line 1253
            os.chdir("a" + os.sep + "b")  # line 1254
            s, vcs, cmd = sos.findSosVcsBase()  # line 1255
            _.assertIsNotNone(s)  # line 1256
            _.assertIsNotNone(vcs)  # line 1257
            _.assertEqual("git", cmd)  # line 1258
        finally:  # line 1259
            os.chdir(old)  # line 1259

# TODO test command line operation --sos vs. --vcs
# check exact output instead of only expected exception/fail

# TODO test +++ --- in diff
# TODO test +01/-02/*..
# TODO tests for loadcommit redirection
# TODO test wrong branch/revision after fast branching, would raise exception for -1 otherwise


if __name__ == '__main__':  # line 1270
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")  # line 1271
    unittest.main(testRunner=debugTestRunner() if '-v' in sys.argv and not os.getenv("CI", "false").lower() == "true" else None)  # warnings = "ignore")  # line 1272
