#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xb3a447ad

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

# Standard modules
import codecs  # line 5
import fnmatch  # line 5
import json  # line 5
import logging  # line 5
import mimetypes  # line 5
import os  # line 5
sys = _coconut_sys  # line 5
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # TODO this looks just wrong, but is currently required  # line 6
try:  # try needed as paths differ when installed via pip TODO investigate further  # line 7
    from sos import usage  # line 8
    from sos import version  # line 9
    from sos.utility import *  # line 10
    from sos.pure import *  # line 11
    import sos.utility as _utility  # WARN necessary because "tests" can only mock "sos.utility.input", because "sos" does "import *"" from "utility" and "sos.input" cannot be mocked for some reason  # line 12
except:  # line 13
    import usage  # line 14
    import version  # line 15
    from utility import *  # line 16
    from pure import *  # line 17
    import utility as _utility  # line 18

# External dependencies
import configr  # line 21


# Lazy imports for quicker initialization
class shutil:  # line 25
    @_coconut_tco  # line 26
    def __getattribute__(_, key):  # line 26
        global shutil  # line 27
        import shutil  # overrides global reference  # line 28
        return _coconut_tail_call(shutil.__getattribute__, key)  # line 29
shutil = shutil()  # line 30


# Functions
def loadConfig() -> 'configr.Configr':  # Accessor when using defaults only  # line 34
    ''' Simplifies loading user-global config from file system or returning application defaults. '''  # line 35
    config = configr.Configr(usage.COMMAND, defaults=defaults)  # type: configr.Configr  # defaults are used if key is not configured, but won't be saved  # line 36
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # latter for testing only  # line 37
    if f is None:  # line 38
        debug("Encountered a problem while loading the user configuration: %r" % g)  # line 38
    return config  # line 39

@_coconut_tco  # line 41
def saveConfig(config: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 41
    return _coconut_tail_call(config.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # saves global config, not local one  # line 42

def correctNegativeIndexing(m, revision: 'int') -> 'int':  # line 44
    revision = revision if revision >= 0 else (max(m.commits) if m.commits else m.getHighestRevision(m.branch)) + 1 + revision  # negative indexing TODO evaluates to 0 for -1 on empty branch which won't be recognized as error  # line 45
    if revision < 0 or (m.commits and revision > max(m.commits)):  # line 46
        Exit("Unknown revision r%02d" % revision)  # line 46
    return revision  # line 47


# Main data class
class Metadata:  # line 51
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 55

    singleton = None  # type: _coconut.typing.Optional[configr.Configr]  # line 57

    def __init__(_, path: '_coconut.typing.Optional[str]'=None, offline: 'bool'=False) -> 'None':  # line 59
        ''' Create empty container object for various repository operations, and import configuration. '''  # line 60
        _.root = (os.getcwd() if path is None else path)  # type: str  # line 61
        _.tags = []  # type: List[str]  # list of known (unique) tags  # line 62
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 63
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 64
        _.repoConf = {}  # type: Dict[str, Any]  # line 65
        _.track = None  # type: bool  # line 66
        _.picky = None  # type: bool  # line 66
        _.strict = None  # type: bool  # line 66
        _.compress = None  # type: bool  # line 66
        _.version = None  # type: _coconut.typing.Optional[str]  # line 66
        _.format = None  # type: _coconut.typing.Optional[int]  # line 66
        _.loadBranches(offline=offline)  # loads above values from repository, or uses application defaults  # line 67

        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 69
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 70
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 71

        if Metadata.singleton is None:  # only load once  # line 73
            Metadata.singleton = configr.Configr(data=_.repoConf, defaults=loadConfig())  # load global configuration with defaults behind the local configuration  # line 74
        _.c = Metadata.singleton  # type: configr.Configr  # line 75

    def isTextType(_, filename: 'str') -> 'bool':  # line 77
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 77

    def listChanges(_, changed: 'ChangeSet', commitTime: '_coconut.typing.Optional[float]'=None):  # line 79
        ''' List changes. If commitTime (in ms) is defined, also check timestamps of modified files for plausibility (if mtime older than last commit, note so). '''  # line 80
        moves = dict(changed.moves.values())  # type: Dict[str, PathInfo]  # of origin-pathinfo  # line 81
        realadditions = {k: v for k, v in changed.additions.items() if k not in changed.moves}  # type: Dict[str, PathInfo]  # line 82
        realdeletions = {k: v for k, v in changed.deletions.items() if k not in moves}  # type: Dict[str, PathInfo]  # line 83
        if len(changed.moves) > 0:  # line 84
            printo(ajoin("MOV ", ["%s  <-  %s" % (path, dpath) for path, (dpath, dinfo) in sorted(changed.moves.items())], "\n"))  # line 84
        if len(realadditions) > 0:  # line 85
            printo(ajoin("ADD ", sorted(realadditions.keys()), "\n"))  # line 85
        if len(realdeletions) > 0:  # line 86
            printo(ajoin("DEL ", sorted(realdeletions.keys()), "\n"))  # line 86
        if len(changed.modifications) > 0:  # line 87
            printo(ajoin("MOD ", [m if commitTime is None else (m + (" <older than previously committed>" if pi.mtime < _.paths[m].mtime else "") + (" <older than last revision>" if pi.mtime < commitTime else "")) for (m, pi) in sorted(changed.modifications.items())], "\n"))  # line 87

    def loadBranches(_, offline: 'bool'=False):  # line 89
        ''' Load list of branches and current branch info from metadata file. offline = offline command avoids message. '''  # line 90
        try:  # fails if not yet created (on initial branch/commit)  # line 91
            branches = None  # type: List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)  # line 92
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 93
                repo, branches, config = json.load(fd)  # line 94
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 95
            _.branch = repo["branch"]  # current branch integer  # line 96
            _.track, _.picky, _.strict, _.compress, _.version, _.format = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format"]]  # line 97
            upgraded = []  # type: List[str]  # line 98
            if _.version is None:  # line 99
                _.version = "0 - pre-1.2"  # line 100
                upgraded.append("pre-1.2")  # line 101
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 102
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 103
                upgraded.append("2018.1210.3028")  # line 104
            if _.format is None:  # must be before 1.3.5+  # line 105
                _.format = METADATA_FORMAT  # marker for first metadata file format  # line 106
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 107
                upgraded.append("1.3.5")  # line 108
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 109
            _.repoConf = config  # line 110
            if upgraded:  # line 111
                for upgrade in upgraded:  # line 112
                    warn("!!! Upgraded repository metadata to match SOS version %r" % upgrade)  # line 112
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 113
                _.saveBranches()  # line 114
        except Exception as E:  # if not found, create metadata folder with default values  # line 115
            _.branches = {}  # line 116
            _.track, _.picky, _.strict, _.compress, _.version, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, METADATA_FORMAT]  # line 117
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # line 118

    def saveBranches(_, also: 'Dict[str, Any]'={}):  # line 120
        ''' Save list of branches and current branch info to metadata file. '''  # line 121
        tryOrIgnore(lambda: shutil.copy2(encode(os.path.join(_.root, metaFolder, metaFile)), encode(os.path.join(_.root, metaFolder, metaBack))))  # backup  # line 122
        with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 123
            store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT}  # type: Dict[str, Any]  # line 124
            store.update(also)  # allows overriding certain values at certain points in time  # line 128
            json.dump((store, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints, fd knows how to encode them  # line 129

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 131
        ''' Convenience accessor for named revisions (using commit message as name as a convention). '''  # line 132
        if name == "":  # line 133
            return -1  # line 133
        try:  # attempt to parse integer string  # line 134
            return int(name)  # attempt to parse integer string  # line 134
        except ValueError:  # line 135
            pass  # line 135
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 136
        return found[0] if found else None  # line 137

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 139
        ''' Convenience accessor for named branches. '''  # line 140
        if name == "":  # current  # line 141
            return _.branch  # current  # line 141
        try:  # attempt to parse integer string  # line 142
            return int(name)  # attempt to parse integer string  # line 142
        except ValueError:  # line 143
            pass  # line 143
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 144
        return found[0] if found else None  # line 145

    def loadBranch(_, branch: 'int'):  # line 147
        ''' Load all commit information from a branch meta data file. '''  # line 148
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 149
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 150
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 151
        _.branch = branch  # line 152

    def saveBranch(_, branch: 'int'):  # line 154
        ''' Save all commits to a branch meta data file. '''  # line 155
        tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile)), encode(branchFolder(branch, metaBack))))  # backup  # line 156
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "w", encoding=UTF8) as fd:  # line 157
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 158

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 160
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 168
        if verbose:  # line 169
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 169
        now = int(time.time() * 1000)  # type: int  # line 170
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 171
        revision = max(_.commits)  # type: int  # line 172
        _.commits.clear()  # line 173
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 174
        os.makedirs(encode(revisionFolder(branch, 0, base=_.root) if full else branchFolder(branch, base=_.root)))  # line 179
        if full:  # not fast branching via reference - copy all current files to new branch  # line 180
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 181
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 182
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 182
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit TODO also contain message from latest revision of originating branch  # line 183
            _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 184
        _.saveBranch(branch)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 185
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 186

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 188
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 194
        now = int(time.time() * 1000)  # type: int  # line 195
        simpleMode = not (_.track or _.picky)  # line 196
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 197
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 198
        if verbose:  # line 199
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 199
        _.paths = {}  # type: Dict[str, PathInfo]  # line 200
        if simpleMode:  # branches from file system state  # line 201
            changed, msg = _.findChanges(branch, 0, progress=simpleMode)  # creates revision folder and versioned files  # line 202
            _.listChanges(changed)  # line 203
            if msg:  # display compression factor and time taken  # line 204
                printo(msg)  # display compression factor and time taken  # line 204
            _.paths.update(changed.additions.items())  # line 205
        else:  # tracking or picky mode: branch from latest revision  # line 206
            os.makedirs(encode(revisionFolder(branch, 0, base=_.root)))  # line 207
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 208
                _.loadBranch(_.branch)  # line 209
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 210
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 211
                for path, pinfo in _.paths.items():  # line 212
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 213
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 214
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 215
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 216
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 217

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 219
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 220
        binfo = None  # type: BranchInfo  # line 221
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and _.getParentBranch(binfo.number, 0) == branch]  # type: List[Tuple[int, int]]  # get transitively depending branches  # line 222
        if deps:  # need to copy all parent revisions to dependet branches first  # line 223
            minrev = min([e[1] for e in deps])  # type: int  # minimum revision ever branched from parent (ignoring transitive branching!)  # line 224
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 225
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed in all depending branches  # line 226
                for dep, _rev in deps:  # line 227
                    if rev <= _rev:  # line 227
                        printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 228
                        shutil.copytree(encode(revisionFolder(branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # folder would not exist yet  # line 229
            for dep, _rev in deps:  # copy remaining revisions per branch  # line 230
                for rev in range(minrev + 1, _rev + 1):  # line 231
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 232
                    shutil.copytree(encode(revisionFolder(_.getParentBranch(dep, rev), rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 233
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # remove reference information  # line 234
        printo(pure.ljust() + "\r")  # line 235
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 236
        try:  # line 237
            os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX))  # line 237
        except:  # line 238
            Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?")  # line 238
        binfo = _.branches[branch]  # keep reference for caller  # line 239
        del _.branches[branch]  # line 240
        _.branch = max(_.branches)  # switch to another valid branch  # line 241
        _.saveBranches()  # line 242
        _.commits.clear()  # line 243
        return binfo  # line 244

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 246
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 247
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 248
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 249
            _.paths = json.load(fd)  # line 249
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 250
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 251

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 253
        ''' Save all file information to a commit meta data file. '''  # line 254
        target = revisionFolder(branch, revision, base=_.root)  # type: str  # line 255
        try:  # line 256
            os.makedirs(encode(target))  # line 256
        except:  # line 257
            pass  # line 257
        tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 258
        with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 259
            json.dump(_.paths, fd, ensure_ascii=False)  # line 259

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 261
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for simple mode. For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 270
        import collections  # line 271
        write = branch is not None and revision is not None  # line 272
        if write:  # line 273
            try:  # line 274
                os.makedirs(encode(revisionFolder(branch, revision, base=_.root)))  # line 274
            except FileExistsError:  # HINT "try" only necessary for *testing* hash collision code (!) TODO probably raise exception otherwise in any case?  # line 275
                pass  # HINT "try" only necessary for *testing* hash collision code (!) TODO probably raise exception otherwise in any case?  # line 275
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # TODO Needs explicity initialization due to mypy problems with default arguments :-(  # line 276
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 277
        hashed = None  # type: _coconut.typing.Optional[str]  # line 278
        written = None  # type: int  # line 278
        compressed = 0  # type: int  # line 278
        original = 0  # type: int  # line 278
        start_time = time.time()  # type: float  # line 278
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 279
        for path, pinfo in _.paths.items():  # line 280
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 281
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter and set operations for all files per path for speed  # line 284
        for path, dirnames, filenames in os.walk(_.root):  # line 285
            path = decode(path)  # line 286
            dirnames[:] = [decode(d) for d in dirnames]  # line 287
            filenames[:] = [decode(f) for f in filenames]  # line 288
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 289
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 290
            dirnames.sort()  # line 291
            filenames.sort()  # line 291
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 292
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 293
            if dontConsider:  # line 294
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 295
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 296
                filename = relPath + SLASH + file  # line 297
                filepath = os.path.join(path, file)  # line 298
                try:  # line 299
                    stat = os.stat(encode(filepath))  # line 299
                except Exception as E:  # line 300
                    exception(E)  # line 300
                    continue  # line 300
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 301
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 302
                if show:  # indication character returned  # line 303
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 304
                    printo(pure.ljust(outstring), nl="")  # line 305
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 306
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 307
                    nameHash = hashStr(filename)  # line 308
                    try:  # line 309
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=nameHash) if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 310
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 311
                        compressed += written  # line 312
                        original += size  # line 312
                    except Exception as E:  # line 313
                        exception(E)  # line 313
                    continue  # with next file  # line 314
                last = _.paths[filename]  # filename is known - check for modifications  # line 315
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 316
                    try:  # line 317
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=last.nameHash) if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 318
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 319
                        continue  # line 319
                    except Exception as E:  # line 320
                        exception(E)  # line 320
                elif size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False)):  # detected a modification TODO wrap hashFile exception  # line 321
                    try:  # line 322
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=last.nameHash) if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 323
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 324
                    except Exception as E:  # line 325
                        exception(E)  # line 325
                else:  # with next file  # line 326
                    continue  # with next file  # line 326
                compressed += written  # line 327
                original += last.size if inverse else size  # line 327
            if relPath in knownPaths:  # at least one file is tracked TODO may leave empty lists in dict  # line 328
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked TODO may leave empty lists in dict  # line 328
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 329
            for file in names:  # line 330
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 331
                    continue  # don't mark ignored files as deleted  # line 331
                pth = path + SLASH + file  # type: str  # line 332
                changed.deletions[pth] = _.paths[pth]  # line 333
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed))  # line 334
        if progress:  # forces clean line of progress output  # line 335
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 335
        elif verbose:  # line 336
            info("Finished detecting changes")  # line 336
        tt = time.time() - start_time  # type: float  # line 337
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # line 337
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 338
        msg = (msg + " | " if msg else "") + ("Transfer speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 339
        return (changed, msg if msg else None)  # line 340

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 342
        ''' Returns nothing, just updates _.paths in place. '''  # line 343
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 344

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 346
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and until specified revision (inclusively) by traversing revision on the file system. '''  # line 347
        _.loadCommit(branch, 0)  # load initial paths  # line 348
        if incrementally:  # line 349
            yield _.paths  # line 349
        m = Metadata(_.root)  # type: Metadata  # next changes TODO avoid loading all metadata and config  # line 350
        rev = None  # type: int  # next changes TODO avoid loading all metadata and config  # line 350
        for rev in range(1, revision + 1):  # line 351
            m.loadCommit(_.getParentBranch(branch, rev), rev)  # line 352
            for p, info in m.paths.items():  # line 353
                if info.size == None:  # line 354
                    del _.paths[p]  # line 354
                else:  # line 355
                    _.paths[p] = info  # line 355
            if incrementally:  # line 356
                yield _.paths  # line 356
        yield None  # for the default case - not incrementally  # line 357

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 359
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 360
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 361

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 363
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 366
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 367
            return (_.branch, -1)  # no branch/revision specified  # line 367
        argument = argument.strip()  # line 368
        if argument.startswith(SLASH):  # current branch  # line 369
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 369
        if argument.endswith(SLASH):  # line 370
            try:  # line 371
                return (_.getBranchByName(argument[:-1]), -1)  # line 371
            except ValueError:  # line 372
                Exit("Unknown branch label '%s'" % argument)  # line 372
        if SLASH in argument:  # line 373
            b, r = argument.split(SLASH)[:2]  # line 374
            try:  # line 375
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 375
            except ValueError:  # line 376
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 376
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 377
        if branch not in _.branches:  # line 378
            branch = None  # line 378
        try:  # either branch name/number or reverse/absolute revision number  # line 379
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 379
        except:  # line 380
            Exit("Unknown branch label or wrong number format")  # line 380
        Exit("This should never happen. Please create a issue report")  # line 381
        return (None, None)  # line 381

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 383
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 385
        while True:  # line 386
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 387
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 388
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 389
                break  # line 389
            revision -= 1  # line 390
            if revision < 0:  # line 391
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 391
        return revision, source  # line 392

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 394
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 395
        other = _.branches[branch].parent  # type: _coconut.typing.Optional[int]  # reference to originating parent branch, or None  # line 396
        if other is None or revision > _.branches[branch].revision:  # need to load commit from other branch instead  # line 397
            return branch  # need to load commit from other branch instead  # line 397
        while _.branches[other].parent is not None and revision <= _.branches[other].revision:  # line 398
            other = _.branches[other].parent  # line 398
        return other  # line 399

    @_coconut_tco  # line 401
    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 401
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 402
        m = Metadata()  # type: Metadata  # line 403
#    while branch is not None:
#      m.loadBranch(other)
#      if not _.commits:
#        if _.branches[branch].parent is None: return None
#        return _.branches[branch].revision  # branch point revision must be correct
#      return max(_.commits)
        other = branch  # type: _coconut.typing.Optional[int]  # line 410
        while other is not None:  # line 411
            m.loadBranch(other)  # line 412
            if m.commits:  # line 413
                return _coconut_tail_call(max, m.commits)  # line 413
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 414
        return None  # line 415

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 417
        ''' Copy versioned file to other branch/revision. '''  # line 418
        target = revisionFolder(toBranch, toRevision, base=_.root, file=pinfo.nameHash)  # type: str  # line 419
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 420
        shutil.copy2(encode(source), encode(target))  # line 421

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 423
        ''' Return file contents, or copy contents into file path provided. '''  # line 424
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 425
        try:  # line 426
            with openIt(source, "r", _.compress) as fd:  # line 427
                if toFile is None:  # read bytes into memory and return  # line 428
                    return fd.read()  # read bytes into memory and return  # line 428
                with open(encode(toFile), "wb") as to:  # line 429
                    while True:  # line 430
                        buffer = fd.read(bufSize)  # line 431
                        to.write(buffer)  # line 432
                        if len(buffer) < bufSize:  # line 433
                            break  # line 433
                    return None  # line 434
        except Exception as E:  # line 435
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 435
        return None  # line 436

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 438
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 439
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 440
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 440
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 441
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 442
            try:  # line 443
                os.makedirs(encode(os.path.dirname(target)))  # line 443
            except:  # line 444
                pass  # line 444
        if pinfo.size == 0:  # line 445
            with open(encode(target), "wb"):  # line 446
                pass  # line 446
            try:  # update access/modification timestamps on file system  # line 447
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 447
            except Exception as E:  # line 448
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 448
            return None  # line 449
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 450
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 452
            while True:  # line 453
                buffer = fd.read(bufSize)  # line 454
                to.write(buffer)  # line 455
                if len(buffer) < bufSize:  # line 456
                    break  # line 456
        try:  # update access/modification timestamps on file system  # line 457
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 457
        except Exception as E:  # line 458
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 458
        return None  # line 459


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 463
    ''' Initial command to start working offline. '''  # line 464
    if os.path.exists(encode(metaFolder)):  # line 465
        if '--force' not in options:  # line 466
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for dirty branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 466
        try:  # line 467
            for entry in os.listdir(metaFolder):  # line 468
                resource = metaFolder + os.sep + entry  # line 469
                if os.path.isdir(resource):  # line 470
                    shutil.rmtree(encode(resource))  # line 470
                else:  # line 471
                    os.unlink(encode(resource))  # line 471
        except:  # line 472
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 472
    m = Metadata(offline=True)  # type: Metadata  # line 473
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 474
        m.compress = True  # plain file copies instead of compressed ones  # line 474
    if '--picky' in options or m.c.picky:  # Git-like  # line 475
        m.picky = True  # Git-like  # line 475
    elif '--track' in options or m.c.track:  # Svn-like  # line 476
        m.track = True  # Svn-like  # line 476
    if '--strict' in options or m.c.strict:  # always hash contents  # line 477
        m.strict = True  # always hash contents  # line 477
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 478
    if title:  # line 479
        printo(title)  # line 479
    if verbose:  # line 480
        info(usage.MARKER + "Going offline...")  # line 480
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 481
    m.branch = 0  # line 482
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 483
    info(usage.MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 484

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 486
    ''' Finish working offline. '''  # line 487
    if verbose:  # line 488
        info(usage.MARKER + "Going back online...")  # line 488
    force = '--force' in options  # type: bool  # line 489
    m = Metadata()  # type: Metadata  # line 490
    strict = '--strict' in options or m.strict  # type: bool  # line 491
    m.loadBranches()  # line 492
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 493
        Exit("There are still unsynchronized (dirty) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit dirty branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 493
    m.loadBranch(m.branch)  # line 494
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 495
    if options.count("--force") < 2:  # line 496
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 497
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 498
        if modified(changed):  # line 499
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 503
    try:  # line 504
        shutil.rmtree(encode(metaFolder))  # line 504
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 504
    except Exception as E:  # line 505
        Exit("Error removing offline repository: %r" % E)  # line 505
    info(usage.MARKER + "Offline repository removed, you're back online")  # line 506

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 508
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not necessary, as either branching from last  revision anyway, or branching file tree anyway.
  '''  # line 511
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 512
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 513
    fast = '--fast' in options  # type: bool  # branch by referencing TODO move to default and use --full instead for old behavior  # line 514
    m = Metadata()  # type: Metadata  # line 515
    m.loadBranch(m.branch)  # line 516
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 517
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 518
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 518
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 519
    if verbose:  # line 520
        info(usage.MARKER + "Branching to %sbranch b%02d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 520
    if last:  # branch from last revision  # line 521
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from r%02d/b%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 521
    else:  # branch from current file tree state  # line 522
        m.createBranch(branch, name, ("Branched from file tree after r%02d/b%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 522
    if not stay:  # line 523
        m.branch = branch  # line 523
    m.saveBranches()  # TODO or indent again?  # line 524
    info(usage.MARKER + "%s new %sbranch b%02d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 525

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 527
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 528
    m = Metadata()  # type: Metadata  # line 529
    branch = None  # type: _coconut.typing.Optional[int]  # line 529
    revision = None  # type: _coconut.typing.Optional[int]  # line 529
    strict = '--strict' in options or m.strict  # type: bool  # line 530
    branch, revision = m.parseRevisionString(argument)  # line 531
    if branch not in m.branches:  # line 532
        Exit("Unknown branch")  # line 532
    m.loadBranch(branch)  # knows commits  # line 533
    revision = correctNegativeIndexing(m, revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 534
    if verbose:  # line 535
        info(usage.MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 535
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 536
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 537
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time())  # line 542
    return changed  # returning for unit tests only TODO remove?  # line 543

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False):  # TODO introduce option to diff against committed revision  # line 545
    ''' The diff display code. '''  # line 546
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 547
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 548
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 549
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 550
        content = b""  # type: _coconut.typing.Optional[bytes]  # line 551
        if pinfo.size != 0:  # versioned file  # line 552
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 552
            assert content is not None  # versioned file  # line 552
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current file  # line 553
        blocks = None  # type: List[MergeBlock]  # line 554
        nl = None  # type: bytes  # line 554
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 555
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 556
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 557
        for block in blocks:  # line 558
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 561
                for no, line in enumerate(block.lines):  # line 562
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 562
            elif block.tipe == MergeBlockType.REMOVE:  # line 563
                for no, line in enumerate(block.lines):  # line 564
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 564
            elif block.tipe == MergeBlockType.REPLACE:  # line 565
                for no, line in enumerate(block.replaces.lines):  # line 566
                    printo(wrap("- | %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)))  # line 566
                for no, line in enumerate(block.lines):  # line 567
                    printo(wrap("+ | %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 567
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 570
                printo()  # line 570

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 572
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 573
    m = Metadata()  # type: Metadata  # line 574
    branch = None  # type: _coconut.typing.Optional[int]  # line 574
    revision = None  # type: _coconut.typing.Optional[int]  # line 574
    strict = '--strict' in options or m.strict  # type: bool  # line 575
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 576
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 577
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 578
    if branch not in m.branches:  # line 579
        Exit("Unknown branch")  # line 579
    m.loadBranch(branch)  # knows commits  # line 580
    revision = correctNegativeIndexing(m, revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 581
    if verbose:  # line 582
        info(usage.MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 582
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 583
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 584
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap)  # line 589

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 591
    ''' Create new revision from file tree changes vs. last commit. '''  # line 592
    m = Metadata()  # type: Metadata  # line 593
    if argument is not None and argument in m.tags:  # line 594
        Exit("Illegal commit message. It was already used as a tag name")  # line 594
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 595
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 597
        Exit("No file patterns staged for commit in picky mode")  # line 597
    if verbose:  # line 598
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 598
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 599
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed))  # line 600
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 601
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 602
    m.paths.update({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 603
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 604
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 605
    m.saveBranch(m.branch)  # line 606
    m.loadBranches()  # TODO is it necessary to load again?  # line 607
    if m.picky:  # remove tracked patterns  # line 608
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 608
    else:  # track or simple mode: set branch dirty  # line 609
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch dirty  # line 609
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 610
        m.tags.append(argument)  # memorize unique tag  # line 610
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 610
    m.saveBranches()  # line 611
    printo(usage.MARKER + "Created new revision r%02d%s (+%02d/-%02d/%s%02d/%s%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changed.additions) - len(changed.moves), len(changed.deletions) - len(changed.moves), PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", len(changed.modifications), MOVE_SYMBOL if m.c.useUnicodeFont else "#", len(changed.moves)))  # line 612

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 614
    ''' Show branches and current repository state. '''  # line 615
    m = Metadata()  # type: Metadata  # line 616
    if not (m.c.useChangesCommand or '--repo' in options):  # line 617
        changes(argument, options, onlys, excps)  # line 617
        return  # line 617
    current = m.branch  # type: int  # line 618
    strict = '--strict' in options or m.strict  # type: bool  # line 619
    info(usage.MARKER + "Offline repository status")  # line 620
    info("Repository root:     %s" % os.getcwd())  # line 621
    info("Underlying VCS root: %s" % vcs)  # line 622
    info("Underlying VCS type: %s" % cmd)  # line 623
    info("Installation path:   %s" % os.path.abspath(os.path.dirname(__file__)))  # line 624
    info("Current SOS version: %s" % version.__version__)  # line 625
    info("At creation version: %s" % m.version)  # line 626
    info("Metadata format:     %s" % m.format)  # line 627
    info("Content checking:    %sactivated" % ("" if m.strict else "de"))  # line 628
    info("Data compression:    %sactivated" % ("" if m.compress else "de"))  # line 629
    info("Repository mode:     %s" % ("track" if m.track else ("picky" if m.picky else "simple")))  # line 630
    info("Number of branches:  %d" % len(m.branches))  # line 631
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 632
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 633
    m.loadBranch(current)  # line 634
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 635
    m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision  # line 508  # line 636
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 637
    printo("%s File tree %s" % ((CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged"))  # TODO use other marks if no unicode console detected TODO bad choice of symbols for changed vs. unchanged  # line 642
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 643
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 644
        payload = 0  # type: int  # count used storage per branch  # line 645
        overhead = 0  # type: int  # count used storage per branch  # line 645
        original = 0  # type: int  # count used storage per branch  # line 645
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 646
            for f in fs:  # TODO count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 647
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 648
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 648
                else:  # line 649
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 649
        pl_amount = float(payload) / MEBI  # type: float  # line 650
        oh_amount = float(overhead) / MEBI  # type: float  # line 650
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 652
        for commit_ in range(max(m.commits) if m.commits else 0):  # line 653
            m.loadCommit(m.branch, commit_)  # line 654
            for pinfo in m.paths.values():  # line 655
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 655
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 656
        printo("  %s b%02d%s @%s (%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "dirty", len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 657
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 658
        info("\nTracked file patterns:")  # TODO print matching untracking patterns side-by-side  # line 659
        printo(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 660
        info("\nUntracked file patterns:")  # line 661
        printo(ajoin("  | ", m.branches[m.branch].untracked, "\n"))  # line 662

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 664
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 671
    assert not (check and commit)  # line 672
    m = Metadata()  # type: Metadata  # line 673
    force = '--force' in options  # type: bool  # line 674
    strict = '--strict' in options or m.strict  # type: bool  # line 675
    if argument is not None:  # line 676
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 677
        if branch is None:  # line 678
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 678
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 679
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 680

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 683
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 684
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 685
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 686
    if check and modified(changed) and not force:  # line 691
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 692
        Exit("File tree contains changes. Use --force to proceed")  # line 693
    elif commit:  # line 694
        if not modified(changed) and not force:  # line 695
            Exit("Nothing to commit")  # line 695
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 696
        if msg:  # line 697
            printo(msg)  # line 697

    if argument is not None:  # branch/revision specified  # line 699
        m.loadBranch(branch)  # knows commits of target branch  # line 700
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 701
        revision = correctNegativeIndexing(m, revision)  # line 702
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 703
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 704

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 706
    ''' Continue work on another branch, replacing file tree changes. '''  # line 707
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 708
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 709

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 712
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 713
    else:  # full file switch  # line 714
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 715
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 716

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 723
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 724
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 725
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 726
                rms.append(a)  # line 726
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 727
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 727
        if modified(changed) and not force:  # line 728
            m.listChanges(changed)  # line 728
            Exit("File tree contains changes. Use --force to proceed")  # line 728
        if verbose:  # line 729
            info(usage.MARKER + "Switching to branch %sb%02d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 729
        if not modified(todos):  # line 730
            info("No changes to current file tree")  # line 731
        else:  # integration required  # line 732
            for path, pinfo in todos.deletions.items():  # line 733
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target  # line 734
                printo("ADD " + path)  # line 735
            for path, pinfo in todos.additions.items():  # line 736
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target  # line 737
                printo("DEL " + path)  # line 738
            for path, pinfo in todos.modifications.items():  # line 739
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 740
                printo("MOD " + path)  # line 741
    m.branch = branch  # line 742
    m.saveBranches()  # store switched path info  # line 743
    info(usage.MARKER + "Switched to branch %sb%02d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 744

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 746
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 750
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 751
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 752
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 753
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 754
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 755
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 756
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 757
    if verbose:  # line 758
        info(usage.MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 758

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 761
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 762
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 763
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 764
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 769
        if trackingUnion != trackingPatterns:  # nothing added  # line 770
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 771
        else:  # line 772
            info("Nothing to update")  # but write back updated branch info below  # line 773
    else:  # integration required  # line 774
        add_all = None  # type: _coconut.typing.Optional[str]  # line 775
        del_all = None  # type: _coconut.typing.Optional[str]  # line 775
        selection = None  # type: str  # line 775
        if changed.deletions.items():  # line 776
            printo("Additions:")  # line 776
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 777
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 778
            if add_all is None and mrg == MergeOperation.ASK:  # line 779
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 780
                if selection in "ao":  # line 781
                    add_all = "y" if selection == "a" else "n"  # line 781
                    selection = add_all  # line 781
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 782
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 782
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path)  # TODO document (A) as "selected not to add by user choice"  # line 783
        if changed.additions.items():  # line 784
            printo("Deletions:")  # line 784
        for path, pinfo in changed.additions.items():  # line 785
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 786
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 786
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 787
            if del_all is None and mrg == MergeOperation.ASK:  # line 788
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 789
                if selection in "ao":  # line 790
                    del_all = "y" if selection == "a" else "n"  # line 790
                    selection = del_all  # line 790
            if "y" in (del_all, selection):  # line 791
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 791
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path)  # not contained in other branch, but maybe kept  # line 792
        if changed.modifications.items():  # line 793
            printo("Modifications:")  # line 793
        for path, pinfo in changed.modifications.items():  # line 794
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 795
            binary = not m.isTextType(path)  # type: bool  # line 796
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 797
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 798
                printo(("MOD " if not binary else "BIN ") + path)  # TODO print mtime, size differences?  # line 799
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 800
            if op == "t":  # line 801
                printo("THR " + path)  # blockwise copy of contents  # line 802
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 802
            elif op == "m":  # line 803
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 804
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 804
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 805
                if current == file and verbose:  # line 806
                    info("No difference to versioned file")  # line 806
                elif file is not None:  # if None, error message was already logged  # line 807
                    merged = None  # type: bytes  # line 808
                    nl = None  # type: bytes  # line 808
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 809
                    if merged != current:  # line 810
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 811
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 811
                    elif verbose:  # TODO but update timestamp?  # line 812
                        info("No change")  # TODO but update timestamp?  # line 812
            else:  # mine or wrong input  # line 813
                printo("MNE " + path)  # nothing to do! same as skip  # line 814
    info(usage.MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%02d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 815
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 816
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 817
    m.saveBranches()  # line 818

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 820
    ''' Remove a branch entirely. '''  # line 821
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 822
    if len(m.branches) == 1:  # line 823
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 823
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 824
    if branch is None or branch not in m.branches:  # line 825
        Exit("Cannot delete unknown branch %r" % branch)  # line 825
    if verbose:  # line 826
        info(usage.MARKER + "Removing branch b%02d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 826
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 827
    info(usage.MARKER + "Branch b%02d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 828

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 830
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 831
    force = '--force' in options  # type: bool  # line 832
    m = Metadata()  # type: Metadata  # line 833
    if not (m.track or m.picky):  # line 834
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 834
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 835
    if pattern in patterns:  # line 836
        Exit("Pattern '%s' already tracked" % pattern)  # line 836
    if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 837
        Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 837
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 838
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 839
    patterns.append(pattern)  # line 840
    m.saveBranches()  # line 841
    info(usage.MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 842

def remove(relPath: 'str', pattern: 'str', negative: 'bool'=False):  # line 844
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 845
    m = Metadata()  # type: Metadata  # line 846
    if not (m.track or m.picky):  # line 847
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 847
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 848
    if pattern not in patterns:  # line 849
        suggestion = _coconut.set()  # type: Set[str]  # line 850
        for pat in patterns:  # line 851
            if fnmatch.fnmatch(pattern, pat):  # line 851
                suggestion.add(pat)  # line 851
        if suggestion:  # TODO use same wording as in move  # line 852
            printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 852
        Exit("Tracked pattern '%s' not found" % pattern)  # line 853
    patterns.remove(pattern)  # line 854
    m.saveBranches()  # line 855
    info(usage.MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 856

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 858
    ''' List specified directory, augmenting with repository metadata. '''  # line 859
    m = Metadata()  # type: Metadata  # line 860
    folder = (os.getcwd() if folder is None else folder)  # line 861
    if '--all' in options:  # always start at SOS repo root with --all  # line 862
        folder = m.root  # always start at SOS repo root with --all  # line 862
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 863
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 864
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # line 865
    if verbose:  # line 866
        info(usage.MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 866
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 867
    if relPath.startswith(os.pardir):  # line 868
        Exit("Cannot list contents of folder outside offline repository")  # line 868
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 869
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 870
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 871
        if len(m.tags) > 0:  # line 872
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 872
        return  # line 873
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 874
        if not recursive:  # avoid recursion  # line 875
            dirnames.clear()  # avoid recursion  # line 875
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 876
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 877

        folder = decode(dirpath)  # line 879
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 880
        if patterns:  # line 881
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 882
            if out:  # line 883
                printo("DIR %s\n" % relPath + out)  # line 883
            continue  # with next folder  # line 884
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 885
        if len(files) > 0:  # line 886
            printo("DIR %s" % relPath)  # line 886
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 887
            ignore = None  # type: _coconut.typing.Optional[str]  # line 888
            for ig in m.c.ignores:  # remember first match  # line 889
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 889
                    ignore = ig  # remember first match  # line 889
                    break  # remember first match  # line 889
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 890
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 890
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 890
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 890
                        break  # found a white list entry for ignored file, undo ignoring it  # line 890
            matches = []  # type: List[str]  # line 891
            if not ignore:  # line 892
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 893
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 894
                        matches.append(os.path.basename(pattern))  # line 894
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 895
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 896

def log(options: '_coconut.typing.Sequence[str]'=[]):  # line 898
    ''' List previous commits on current branch. '''  # line 899
    changes_ = "--changes" in options  # type: bool  # line 900
    diff_ = "--diff" in options  # type: bool  # line 901
    number_ = tryOrDefault(lambda _=None: options[options.index("-n") + 1], None)  # type: _coconut.typing.Optional[int]  # line 902
    m = Metadata()  # type: Metadata  # line 903
    m.loadBranch(m.branch)  # knows commit history  # line 904
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 905
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 906
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 907
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 908
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 909
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 910
    commit = None  # type: CommitInfo  # line 911
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 912
    for no in range(maxi + 1):  # line 913
        if no in m.commits:  # line 914
            commit = m.commits[no]  # line 914
        else:  # line 915
            if n.branch != n.getParentBranch(m.branch, no):  # line 916
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 916
            commit = n.commits[no]  # line 917
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 918
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 919
        if "--all" in options or no >= max(0, maxi + 1 - ((lambda _coconut_none_coalesce_item: m.c.logLines if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(number_))):  # line 920
            _add = news - olds  # type: FrozenSet[str]  # line 921
            _del = olds - news  # type: FrozenSet[str]  # line 922
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 924
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds})  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 926
            printo("  %s r%s @%s (+%02d/-%02d/%s%02d/T%02d) |%s|%s" % ("*" if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(_add), len(_del), PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", len(_mod), _txt, ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)), "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else ""))  # line 927
            if changes_:  # TODO moves detection?  # line 928
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}))  # TODO moves detection?  # line 928
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 929
                pass  #  _diff(m, changes)  # needs from revision diff  # line 929
        olds = news  # replaces olds for next revision compare  # line 930
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 931

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 933
    ''' Exported entire repository as archive for easy transfer. '''  # line 934
    if verbose:  # line 935
        info(usage.MARKER + "Dumping repository to archive...")  # line 935
    m = Metadata()  # type: Metadata  # to load the configuration  # line 936
    progress = '--progress' in options  # type: bool  # line 937
    delta = '--full' not in options  # type: bool  # line 938
    skipBackup = '--skip-backup' in options  # type: bool  # line 939
    import functools  # line 940
    import locale  # line 940
    import warnings  # line 940
    import zipfile  # line 940
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 941
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 941
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 941
    except:  # line 942
        compression = zipfile.ZIP_STORED  # line 942

    if argument is None:  # line 944
        Exit("Argument missing (target filename)")  # line 944
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 945
    entries = []  # type: List[str]  # line 946
    if os.path.exists(encode(argument)) and not skipBackup:  # line 947
        try:  # line 948
            if verbose:  # line 949
                info("Creating backup...")  # line 949
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 950
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 951
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 951
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 951
        except Exception as E:  # line 952
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 952
    if verbose:  # line 953
        info("Dumping revisions...")  # line 953
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 954
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 954
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 955
        _zip.debug = 0  # suppress debugging output  # line 956
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 957
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 958
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 959
        totalsize = 0  # type: int  # line 960
        start_time = time.time()  # type: float  # line 961
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 962
            dirpath = decode(dirpath)  # line 963
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 964
                continue  # don't backup backups  # line 964
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 965
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 966
            filenames[:] = sorted([decode(f) for f in filenames])  # line 967
            for filename in filenames:  # line 968
                abspath = os.path.join(dirpath, filename)  # type: str  # line 969
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 970
                totalsize += os.stat(encode(abspath)).st_size  # line 971
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 972
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 973
                    continue  # don't backup backups  # line 973
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 974
                    if show:  # line 975
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 975
                    _zip.write(abspath, relpath)  # write entry into archive  # line 976
        if delta:  # line 977
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 977
    info("\r" + pure.ljust(usage.MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 978

def publish(options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 980
    ''' Write changes made to the branch into one commit of the underlying VCS. TODO add option to non-permanently add files for VCSs that track by default. '''  # line 981
    m = None  # type: Metadata  # = Metadata()  # line 982
    if not (m.track or m.picky):  # TODO manual file picking mode  # line 983
        Exit("Not implemented for simple repository mode yet")  # TODO manual file picking mode  # line 983
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 984
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # get highest commit number  # line 985
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 986
# TODO only add changed files!
# fitStrings(m.paths, prefix = "%s add")

def config(arguments: 'List[str]', options: 'List[str]'=[]):  # line 990
    command, key, value = (arguments + [None] * 2)[:3]  # line 991
    if command is None:  # line 992
        usage.usage("help", verbose=True)  # line 992
    if command not in ["set", "unset", "show", "list", "add", "rm"]:  # line 993
        Exit("Unknown config command")  # line 993
    local = "--local" in options  # type: bool  # line 994
    m = Metadata()  # type: Metadata  # loads layered configuration as well. TODO warning if repo not exists  # line 995
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 996
    if command == "set":  # line 997
        if None in (key, value):  # line 998
            Exit("Key or value not specified")  # line 998
        if key not in (([] if local else CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 999
            Exit("Unsupported key for %s configuration %r" % ("local " if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 999
        if key in CONFIGURABLE_FLAGS and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1000
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1000
        c[key] = value.lower() in TRUTH_VALUES if key in CONFIGURABLE_FLAGS else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1001
    elif command == "unset":  # line 1002
        if key is None:  # line 1003
            Exit("No key specified")  # line 1003
        if key not in c.keys():  # HINT: Works on local configurations when used with --local  # line 1004
            Exit("Unknown key")  # HINT: Works on local configurations when used with --local  # line 1004
        del c[key]  # line 1005
    elif command == "add":  # line 1006
        if None in (key, value):  # line 1007
            Exit("Key or value not specified")  # line 1007
        if key not in CONFIGURABLE_LISTS:  # line 1008
            Exit("Unsupported key %r" % key)  # line 1008
        if key not in c.keys():  # prepare empty list, or copy from global, add new value below  # line 1009
            c[key] = [_ for _ in c.__defaults[key]] if local else []  # prepare empty list, or copy from global, add new value below  # line 1009
        elif value in c[key]:  # line 1010
            Exit("Value already contained, nothing to do")  # line 1010
        if ";" in value:  # line 1011
            c[key].append(removePath(key, value))  # line 1011
        else:  # line 1012
            c[key].extend([removePath(key, v) for v in value.split(";")])  # line 1012
    elif command == "rm":  # line 1013
        if None in (key, value):  # line 1014
            Exit("Key or value not specified")  # line 1014
        if key not in c.keys():  # line 1015
            Exit("Unknown key %r" % key)  # line 1015
        if value not in c[key]:  # line 1016
            Exit("Unknown value %r" % value)  # line 1016
        c[key].remove(value)  # line 1017
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1018
            del c[key]  # remove local entry, to fallback to global  # line 1018
    else:  # Show or list  # line 1019
        if key == "ints":  # list valid configuration items  # line 1020
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1020
        elif key == "flags":  # line 1021
            printo(", ".join(CONFIGURABLE_FLAGS))  # line 1021
        elif key == "lists":  # line 1022
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1022
        elif key == "texts":  # line 1023
            printo(", ".join([_ for _ in defaults.keys() if _ not in (CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS)]))  # line 1023
        else:  # line 1024
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # line 1025
            c = m.c  # always use full configuration chain  # line 1026
            try:  # attempt single key  # line 1027
                assert key is not None  # line 1028
                c[key]  # line 1028
                l = key in c.keys()  # type: bool  # line 1029
                g = key in c.__defaults.keys()  # type: bool  # line 1029
                printo("%s %s %r" % (key.rjust(20), out[3] if not (l or g) else (out[1] if l else out[2]), c[key]))  # line 1030
            except:  # normal value listing  # line 1031
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # line 1032
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1033
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1034
                for k, vt in sorted(vals.items()):  # line 1035
                    printo("%s %s %s" % (k.rjust(20), out[vt[1]], vt[0]))  # line 1035
                if len(c.keys()) == 0:  # line 1036
                    info("No local configuration stored")  # line 1036
                if len(c.__defaults.keys()) == 0:  # line 1037
                    info("No global configuration stored")  # line 1037
        return  # in case of list, no need to store anything  # line 1038
    if local:  # saves changes of repoConfig  # line 1039
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1039
        m.saveBranches()  # saves changes of repoConfig  # line 1039
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1039
    else:  # global config  # line 1040
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1041
        if f is None:  # line 1042
            error("Error saving user configuration: %r" % h)  # line 1042
        else:  # line 1043
            Exit("OK", code=0)  # line 1043

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1045
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1048
    if verbose:  # line 1049
        info(usage.MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1049
    force = '--force' in options  # type: bool  # line 1050
    soft = '--soft' in options  # type: bool  # line 1051
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1052
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1052
    m = Metadata()  # type: Metadata  # line 1053
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1054
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1055
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1056
    if not matching and not force:  # line 1057
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1057
    if not (m.track or m.picky):  # line 1058
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 1058
    if pattern not in patterns:  # list potential alternatives and exit  # line 1059
        for tracked in (t for t in patterns if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 1060
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1061
            if alternative:  # line 1062
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 1062
        if not (force or soft):  # line 1063
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 1063
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1064
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1065
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1066
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 1070
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1071
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1071
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1072
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1073
    if len({st[1] for st in matches}) != len(matches):  # line 1074
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1074
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1075
    if os.path.exists(encode(newRelPath)):  # line 1076
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1077
        if exists and not (force or soft):  # line 1078
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1078
    else:  # line 1079
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1079
    if not soft:  # perform actual renaming  # line 1080
        for (source, target) in matches:  # line 1081
            try:  # line 1082
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1082
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1083
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1083
    patterns[patterns.index(pattern)] = newPattern  # line 1084
    m.saveBranches()  # line 1085

def parse(root: 'str', cwd: 'str', cmd: 'str'):  # line 1087
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1088
    debug("Parsing command-line arguments...")  # line 1089
    try:  # line 1090
        onlys, excps = parseOnlyOptions(cwd, sys.argv)  # extracts folder-relative information for changes, commit, diff, switch, update  # line 1091
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1092
        arguments = [c.strip() for c in sys.argv[2:] if not c.startswith("--")]  # type: List[_coconut.typing.Optional[str]]  # line 1093
        options = [c.strip() for c in sys.argv[2:] if c.startswith("--")]  # line 1094
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1095
        if command[:1] in "amr":  # line 1096
            relPath, pattern = relativize(root, os.path.join(cwd, arguments[0] if arguments else "."))  # line 1096
        if command[:1] == "m":  # line 1097
            if len(arguments) < 2:  # line 1098
                Exit("Need a second file pattern argument as target for move command")  # line 1098
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1099
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1100
        if command[:1] == "a":  # addnot  # line 1101
            add(relPath, pattern, options, negative="n" in command)  # addnot  # line 1101
        elif command[:1] == "b":  # line 1102
            branch(arguments[0], arguments[1], options)  # line 1102
        elif command[:3] == "com":  # line 1103
            commit(arguments[0], options, onlys, excps)  # line 1103
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1104
            changes(arguments[0], options, onlys, excps)  # "changes" (legacy)  # line 1104
        elif command[:2] == "ci":  # line 1105
            commit(arguments[0], options, onlys, excps)  # line 1105
        elif command[:3] == 'con':  # line 1106
            config(arguments, options)  # line 1106
        elif command[:2] == "de":  # line 1107
            destroy(arguments[0], options)  # line 1107
        elif command[:2] == "di":  # line 1108
            diff(arguments[0], options, onlys, excps)  # line 1108
        elif command[:2] == "du":  # line 1109
            dump(arguments[0], options)  # line 1109
        elif command[:1] == "h":  # line 1110
            usage.usage(arguments[0], verbose=verbose)  # line 1110
        elif command[:2] == "lo":  # line 1111
            log(options)  # line 1111
        elif command[:2] == "li":  # line 1112
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1112
        elif command[:2] == "ls":  # line 1113
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1113
        elif command[:1] == "m":  # mvnot  # line 1114
            move(relPath, pattern, newRelPath, newPattern, options, negative="n" in command)  # mvnot  # line 1114
        elif command[:2] == "of":  # line 1115
            offline(arguments[0], arguments[1], options)  # line 1115
        elif command[:2] == "on":  # line 1116
            online(options)  # line 1116
        elif command[:1] == "p":  # line 1117
            publish()  # line 1117
        elif command[:1] == "r":  # rmnot  # line 1118
            remove(relPath, pattern, negative="n" in command)  # rmnot  # line 1118
        elif command[:2] == "st":  # line 1119
            status(arguments[0], cwd, cmd, options, onlys, excps)  # line 1119
        elif command[:2] == "sw":  # line 1120
            switch(arguments[0], options, onlys, excps)  # line 1120
        elif command[:1] == "u":  # line 1121
            update(arguments[0], options, onlys, excps)  # line 1121
        elif command[:1] == "v":  # line 1122
            usage.usage(arguments[0], version=True)  # line 1122
        else:  # line 1123
            Exit("Unknown command '%s'" % command)  # line 1123
        Exit(code=0)  # regular exit  # line 1124
    except (Exception, RuntimeError) as E:  # line 1125
        exception(E)  # line 1126
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing")  # line 1127

def main():  # line 1129
    global debug, info, warn, error  # to modify logger  # line 1130
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1131
    _log = Logger(logging.getLogger(__name__))  # line 1132
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1132
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1133
        sys.argv.remove(option)  # clean up program arguments  # line 1133
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1134
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1134
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1135
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1136
    debug("Found root folders for SOS | VCS:  %s | %s" % (("-" if root is None else root), ("-" if vcs is None else vcs)))  # line 1137
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1138
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1139
    if force_sos or root is not None or (("" if command is None else command))[:2] == "of" or (("" if command is None else command))[:1] in "hv":  # in offline mode or just going offline TODO what about git config?  # line 1140
        cwd = os.getcwd()  # line 1141
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1142
        parse(vcs, cwd, cmd)  # line 1143
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1144
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1145
        import subprocess  # only required in this section  # line 1146
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1147
        inp = ""  # type: str  # line 1148
        while True:  # line 1149
            so, se = process.communicate(input=inp)  # line 1150
            if process.returncode is not None:  # line 1151
                break  # line 1151
            inp = sys.stdin.read()  # line 1152
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1153
            if root is None:  # line 1154
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1154
            m = Metadata(root)  # type: Metadata  # line 1155
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1156
            m.saveBranches()  # line 1157
    else:  # line 1158
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1158


# Main part
force_sos = '--sos' in sys.argv  # type: bool  # line 1162
force_vcs = '--vcs' in sys.argv  # type: bool  # line 1163
verbose = '--verbose' in sys.argv or '-v' in sys.argv  # type: bool  # imported from utility, and only modified here  # line 1164
debug_ = os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv  # type: bool  # line 1165
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1166
_log = Logger(logging.getLogger(__name__))  # line 1167
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1167
if __name__ == '__main__':  # line 1168
    main()  # line 1168
