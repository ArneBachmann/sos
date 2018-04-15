#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1cecf7d5

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
import codecs  # only essential modules  # line 5
import fnmatch  # only essential modules  # line 5
import json  # only essential modules  # line 5
import logging  # only essential modules  # line 5
import mimetypes  # only essential modules  # line 5
import os  # only essential modules  # line 5
sys = _coconut_sys  # only essential modules  # line 5
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # TODO this looks just wrong, but is currently required (check again, why)  # line 6
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

# Dependencies
import configr  # line 21


# Lazy imports for quicker initialization
shutil = None  # type: Any  # line 25
class shutil:  # line 26
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


# Main data class
class Metadata:  # line 46
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 50

    singleton = None  # type: _coconut.typing.Optional[configr.Configr]  # line 52

    def __init__(_, path: '_coconut.typing.Optional[str]'=None, offline: 'bool'=False) -> 'None':  # line 54
        ''' Create empty container object for various repository operations, and import configuration. '''  # line 55
        _.root = (os.getcwd() if path is None else path)  # type: str  # line 56
        _.tags = []  # type: List[str]  # list of known (unique) tags  # line 57
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 58
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 59
        _.repoConf = {}  # type: Dict[str, Any]  # line 60
        _.track = None  # type: bool  # line 61
        _.picky = None  # type: bool  # line 61
        _.strict = None  # type: bool  # line 61
        _.compress = None  # type: bool  # line 61
        _.version = None  # type: _coconut.typing.Optional[str]  # line 61
        _.format = None  # type: _coconut.typing.Optional[int]  # line 61
        _.loadBranches(offline=offline)  # loads above values from repository, or uses application defaults  # line 62

        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 64
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 65
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 66

        if Metadata.singleton is None:  # load configuration only once per runtime  # line 68
            Metadata.singleton = configr.Configr(data=_.repoConf, defaults=loadConfig())  # load global configuration with defaults behind the local configuration  # line 69
        _.c = Metadata.singleton  # type: configr.Configr  # line 70

    def isTextType(_, filename: 'str') -> 'bool':  # line 72
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 72

    def correctNegativeIndexing(_, revision: 'int') -> 'int':  # line 74
        ''' As the na_e says, this deter_ines the correct positive revision nu_ber for negative indexing (-1 being last, -2 being second last). '''  # line 75
        revision = revision if revision >= 0 else (max(_.commits) if _.commits else (lambda _coconut_none_coalesce_item: -1 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.getHighestRevision(_.branch))) + 1 + revision  # negative indexing  # line 76
        if revision < 0 or (_.commits and revision > max(_.commits)):  # line 77
            Exit("Unknown revision r%02d" % revision)  # line 77
        return revision  # line 78

    def listChanges(_, changed: 'ChangeSet', commitTime: '_coconut.typing.Optional[float]'=None):  # line 80
        ''' List changes. If commitTime (in ms) is defined, also check timestamps of modified files for plausibility (if mtime older than last commit, note so). '''  # line 81
        moves = dict(changed.moves.values())  # type: Dict[str, PathInfo]  # of origin-pathinfo  # line 82
        realadditions = {k: v for k, v in changed.additions.items() if k not in changed.moves}  # type: Dict[str, PathInfo]  # line 83
        realdeletions = {k: v for k, v in changed.deletions.items() if k not in moves}  # type: Dict[str, PathInfo]  # line 84
        if len(changed.moves) > 0:  # line 85
            printo(ajoin("MOV ", ["%s  <-  %s" % (path, dpath) for path, (dpath, dinfo) in sorted(changed.moves.items())], "\n"))  # line 85
        if len(realadditions) > 0:  # line 86
            printo(ajoin("ADD ", sorted(realadditions.keys()), "\n"))  # line 86
        if len(realdeletions) > 0:  # line 87
            printo(ajoin("DEL ", sorted(realdeletions.keys()), "\n"))  # line 87
        if len(changed.modifications) > 0:  # line 88
            printo(ajoin("MOD ", [m if commitTime is None else (m + (" <older than previously committed>" if pi.mtime < _.paths[m].mtime else "") + (" <older than last revision>" if pi.mtime < commitTime else "")) for (m, pi) in sorted(changed.modifications.items())], "\n"))  # line 88

    def loadBranches(_, offline: 'bool'=False):  # line 90
        ''' Load list of branches and current branch info from metadata file. offline = offline command avoids message. '''  # line 91
        try:  # fails if not yet created (on initial branch/commit)  # line 92
            branches = None  # type: List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)  # line 93
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 94
                repo, branches, config = json.load(fd)  # line 95
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 96
            _.branch = repo["branch"]  # current branch integer  # line 97
            _.track, _.picky, _.strict, _.compress, _.version, _.format = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format"]]  # line 98
            upgraded = []  # type: List[str]  # line 99
            if _.version is None:  # line 100
                _.version = "0 - pre-1.2"  # line 101
                upgraded.append("pre-1.2")  # line 102
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 103
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 104
                upgraded.append("2018.1210.3028")  # line 105
            if _.format is None:  # must be before 1.3.5+  # line 106
                _.format = METADATA_FORMAT  # marker for first metadata file format  # line 107
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 108
                upgraded.append("1.3.5")  # line 109
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 110
            _.repoConf = config  # line 111
            if upgraded:  # line 112
                for upgrade in upgraded:  # line 113
                    warn("!!! Upgraded repository metadata to match SOS version %r" % upgrade)  # line 113
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 114
                _.saveBranches()  # line 115
        except Exception as E:  # if not found, create metadata folder with default values  # line 116
            _.branches = {}  # line 117
            _.track, _.picky, _.strict, _.compress, _.version, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, METADATA_FORMAT]  # line 118
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # line 119

    def saveBranches(_, also: 'Dict[str, Any]'={}):  # line 121
        ''' Save list of branches and current branch info to metadata file. '''  # line 122
        tryOrIgnore(lambda: shutil.copy2(encode(os.path.join(_.root, metaFolder, metaFile)), encode(os.path.join(_.root, metaFolder, metaBack))))  # backup  # line 123
        with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 124
            store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT}  # type: Dict[str, Any]  # line 125
            store.update(also)  # allows overriding certain values at certain points in time  # line 129
            json.dump((store, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints, fd knows how to encode them  # line 130

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 132
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 133
        if name == "":  # line 134
            return -1  # line 134
        try:  # attempt to parse integer string  # line 135
            return int(name)  # attempt to parse integer string  # line 135
        except ValueError:  # line 136
            pass  # line 136
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 137
        return found[0] if found else None  # line 138

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 140
        ''' Convenience accessor for named branches. '''  # line 141
        if name == "":  # current  # line 142
            return _.branch  # current  # line 142
        try:  # attempt to parse integer string  # line 143
            return int(name)  # attempt to parse integer string  # line 143
        except ValueError:  # line 144
            pass  # line 144
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 145
        return found[0] if found else None  # line 146

    def loadBranch(_, branch: 'int'):  # line 148
        ''' Load all commit information from a branch meta data file. '''  # line 149
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 150
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 151
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 152
        _.branch = branch  # line 153

    def saveBranch(_, branch: 'int'):  # line 155
        ''' Save all commits to a branch meta data file. '''  # line 156
        tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile)), encode(branchFolder(branch, metaBack))))  # backup  # line 157
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "w", encoding=UTF8) as fd:  # line 158
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 159

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 161
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 169
        if verbose:  # line 170
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 170
        now = int(time.time() * 1000)  # type: int  # line 171
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 172
        revision = max(_.commits)  # type: int  # line 173
        _.commits.clear()  # line 174
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 175
        os.makedirs(encode(revisionFolder(branch, 0, base=_.root) if full else branchFolder(branch, base=_.root)))  # line 180
        if full:  # not fast branching via reference - copy all current files to new branch  # line 181
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 182
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 183
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 183
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit TODO also contain message from latest revision of originating branch  # line 184
            _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 185
        _.saveBranch(branch)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 186
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 187

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 189
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 195
        now = int(time.time() * 1000)  # type: int  # line 196
        simpleMode = not (_.track or _.picky)  # line 197
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 198
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 199
        if verbose:  # line 200
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 200
        _.paths = {}  # type: Dict[str, PathInfo]  # line 201
        if simpleMode:  # branches from file system state  # line 202
            changed, msg = _.findChanges(branch, 0, progress=simpleMode)  # creates revision folder and versioned files  # line 203
            _.listChanges(changed)  # line 204
            if msg:  # display compression factor and time taken  # line 205
                printo(msg)  # display compression factor and time taken  # line 205
            _.paths.update(changed.additions.items())  # line 206
        else:  # tracking or picky mode: branch from latest revision  # line 207
            os.makedirs(encode(revisionFolder(branch, 0, base=_.root)))  # line 208
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 209
                _.loadBranch(_.branch)  # line 210
                revision = max(_.commits)  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 211
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 212
                for path, pinfo in _.paths.items():  # line 213
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 214
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 215
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 216
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 217
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 218

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 220
        ''' Entirely remove a branch and all its revisions from the file system. '''  # line 221
        binfo = None  # type: BranchInfo  # line 222
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and _.getParentBranch(binfo.number, 0) == branch]  # type: List[Tuple[int, int]]  # get transitively depending branches  # line 223
        if deps:  # need to copy all parent revisions to dependet branches first  # line 224
            minrev = min([e[1] for e in deps])  # type: int  # minimum revision ever branched from parent (ignoring transitive branching!)  # line 225
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 226
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed in all depending branches  # line 227
                for dep, _rev in deps:  # line 228
                    if rev <= _rev:  # line 228
                        printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 229
                        shutil.copytree(encode(revisionFolder(branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # folder would not exist yet  # line 230
            for dep, _rev in deps:  # copy remaining revisions per branch  # line 231
                for rev in range(minrev + 1, _rev + 1):  # line 232
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 233
                    shutil.copytree(encode(revisionFolder(_.getParentBranch(dep, rev), rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 234
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # remove reference information  # line 235
        printo(pure.ljust() + "\r")  # line 236
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 237
        try:  # line 238
            os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX))  # line 238
        except:  # line 239
            Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?")  # line 239
        binfo = _.branches[branch]  # keep reference for caller  # line 240
        del _.branches[branch]  # line 241
        _.branch = max(_.branches)  # switch to another valid branch  # line 242
        _.saveBranches()  # line 243
        _.commits.clear()  # line 244
        return binfo  # line 245

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 247
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 248
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 249
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 250
            _.paths = json.load(fd)  # line 250
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 251
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 252

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 254
        ''' Save all file information to a commit meta data file. '''  # line 255
        target = revisionFolder(branch, revision, base=_.root)  # type: str  # line 256
        tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 257
        tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 258
        with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 259
            json.dump(_.paths, fd, ensure_ascii=False)  # line 259

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 261
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 270
        import collections  # used only in this method  # line 271
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
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 347
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
        other = branch  # type: _coconut.typing.Optional[int]  # line 404
        while other is not None:  # line 405
            m.loadBranch(other)  # line 406
            if m.commits:  # line 407
                return _coconut_tail_call(max, m.commits)  # line 407
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 408
        return None  # line 409

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 411
        ''' Copy versioned file to other branch/revision. '''  # line 412
        target = revisionFolder(toBranch, toRevision, base=_.root, file=pinfo.nameHash)  # type: str  # line 413
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 414
        shutil.copy2(encode(source), encode(target))  # line 415

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 417
        ''' Return file contents, or copy contents into file path provided. '''  # line 418
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 419
        try:  # line 420
            with openIt(source, "r", _.compress) as fd:  # line 420
                if toFile is None:  # read bytes into memory and return  # line 421
                    return fd.read()  # read bytes into memory and return  # line 421
                with open(encode(toFile), "wb") as to:  # line 422
                    while True:  # line 423
                        buffer = fd.read(bufSize)  # line 424
                        to.write(buffer)  # line 425
                        if len(buffer) < bufSize:  # line 426
                            break  # line 426
                    return None  # line 427
        except Exception as E:  # line 428
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 428

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 430
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 431
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 432
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 432
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 433
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 434
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 435
        if pinfo.size == 0:  # line 436
            with open(encode(target), "wb"):  # line 437
                pass  # line 437
            try:  # update access/modification timestamps on file system  # line 438
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 438
            except Exception as E:  # line 439
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 439
            return None  # line 440
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 441
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 443
            while True:  # line 444
                buffer = fd.read(bufSize)  # line 445
                to.write(buffer)  # line 446
                if len(buffer) < bufSize:  # line 447
                    break  # line 447
        try:  # update access/modification timestamps on file system  # line 448
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 448
        except Exception as E:  # line 449
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 449
        return None  # line 450


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 454
    ''' Initial command to start working offline. '''  # line 455
    if os.path.exists(encode(metaFolder)):  # line 456
        if '--force' not in options:  # line 457
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 457
        try:  # line 458
            for entry in os.listdir(metaFolder):  # line 459
                resource = metaFolder + os.sep + entry  # line 460
                if os.path.isdir(resource):  # line 461
                    shutil.rmtree(encode(resource))  # line 461
                else:  # line 462
                    os.unlink(encode(resource))  # line 462
        except:  # line 463
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 463
    m = Metadata(offline=True)  # type: Metadata  # line 464
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 465
        m.compress = True  # plain file copies instead of compressed ones  # line 465
    if '--picky' in options or m.c.picky:  # Git-like  # line 466
        m.picky = True  # Git-like  # line 466
    elif '--track' in options or m.c.track:  # Svn-like  # line 467
        m.track = True  # Svn-like  # line 467
    if '--strict' in options or m.c.strict:  # always hash contents  # line 468
        m.strict = True  # always hash contents  # line 468
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 469
    if title:  # line 470
        printo(title)  # line 470
    if verbose:  # line 471
        info(usage.MARKER + "Going offline...")  # line 471
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 472
    m.branch = 0  # line 473
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 474
    info(usage.MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 475

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 477
    ''' Finish working offline. '''  # line 478
    if verbose:  # line 479
        info(usage.MARKER + "Going back online...")  # line 479
    force = '--force' in options  # type: bool  # line 480
    m = Metadata()  # type: Metadata  # line 481
    strict = '--strict' in options or m.strict  # type: bool  # line 482
    m.loadBranches()  # line 483
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 484
        Exit("There are still unsynchronized (modified) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 484
    m.loadBranch(m.branch)  # line 485
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 486
    if options.count("--force") < 2:  # line 487
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 488
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 489
        if modified(changed):  # line 490
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 494
    try:  # line 495
        shutil.rmtree(encode(metaFolder))  # line 495
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 495
    except Exception as E:  # line 496
        Exit("Error removing offline repository: %r" % E)  # line 496
    info(usage.MARKER + "Offline repository removed, you're back online")  # line 497

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 499
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not necessary, as either branching from last  revision anyway, or branching file tree anyway.
  '''  # line 502
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 503
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 504
    fast = '--fast' in options  # type: bool  # branch by referencing TODO move to default and use --full instead for old behavior  # line 505
    m = Metadata()  # type: Metadata  # line 506
    m.loadBranch(m.branch)  # line 507
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 508
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 509
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 509
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 510
    if verbose:  # line 511
        info(usage.MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 511
    if last:  # branch from last revision  # line 512
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 512
    else:  # branch from current file tree state  # line 513
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 513
    if not stay:  # line 514
        m.branch = branch  # line 514
    m.saveBranches()  # TODO or indent again?  # line 515
    info(usage.MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 516

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 518
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 519
    m = Metadata()  # type: Metadata  # line 520
    branch = None  # type: _coconut.typing.Optional[int]  # line 520
    revision = None  # type: _coconut.typing.Optional[int]  # line 520
    strict = '--strict' in options or m.strict  # type: bool  # line 521
    branch, revision = m.parseRevisionString(argument)  # line 522
    if branch not in m.branches:  # line 523
        Exit("Unknown branch")  # line 523
    m.loadBranch(branch)  # knows commits  # line 524
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 525
    if verbose:  # line 526
        info(usage.MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 526
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 527
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 528
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time())  # line 533
    return changed  # returning for unit tests only TODO remove?  # line 534

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False):  # TODO introduce option to diff against committed revision  # line 536
    ''' The diff display code. '''  # line 537
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 538
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 539
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 540
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 541
        content = b""  # type: _coconut.typing.Optional[bytes]  # line 542
        if pinfo.size != 0:  # versioned file  # line 543
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 543
            assert content is not None  # versioned file  # line 543
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current file  # line 544
        blocks = None  # type: List[MergeBlock]  # line 545
        nl = None  # type: bytes  # line 545
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 546
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 547
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 548
        for block in blocks:  # line 549
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 552
                for no, line in enumerate(block.lines):  # line 553
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 553
            elif block.tipe == MergeBlockType.REMOVE:  # line 554
                for no, line in enumerate(block.lines):  # line 555
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 555
            elif block.tipe == MergeBlockType.REPLACE:  # line 556
                for no, line in enumerate(block.replaces.lines):  # line 557
                    printo(wrap("- | %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)))  # line 557
                for no, line in enumerate(block.lines):  # line 558
                    printo(wrap("+ | %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 558
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 561
                printo()  # line 561

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 563
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 564
    m = Metadata()  # type: Metadata  # line 565
    branch = None  # type: _coconut.typing.Optional[int]  # line 565
    revision = None  # type: _coconut.typing.Optional[int]  # line 565
    strict = '--strict' in options or m.strict  # type: bool  # line 566
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 567
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 568
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 569
    if branch not in m.branches:  # line 570
        Exit("Unknown branch")  # line 570
    m.loadBranch(branch)  # knows commits  # line 571
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 572
    if verbose:  # line 573
        info(usage.MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 573
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 574
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 575
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap)  # line 580

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 582
    ''' Create new revision from file tree changes vs. last commit. '''  # line 583
    m = Metadata()  # type: Metadata  # line 584
    if argument is not None and argument in m.tags:  # line 585
        Exit("Illegal commit message. It was already used as a tag name")  # line 585
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 586
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 588
        Exit("No file patterns staged for commit in picky mode")  # line 588
    if verbose:  # line 589
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 589
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 590
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed))  # line 591
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 592
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 593
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 594
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 595
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 596
    m.saveBranch(m.branch)  # line 597
    m.loadBranches()  # TODO is it necessary to load again?  # line 598
    if m.picky:  # remove tracked patterns  # line 599
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 599
    else:  # track or simple mode: set branch modified  # line 600
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 600
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 601
        m.tags.append(argument)  # memorize unique tag  # line 601
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 601
    m.saveBranches()  # line 602
    printo(usage.MARKER + "Created new revision r%02d%s (+%02d/-%02d/%s%02d/%s%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changed.additions) - len(changed.moves), len(changed.deletions) - len(changed.moves), PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", len(changed.modifications), MOVE_SYMBOL if m.c.useUnicodeFont else "#", len(changed.moves)))  # line 603

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 605
    ''' Show branches and current repository state. '''  # line 606
    m = Metadata()  # type: Metadata  # line 607
    if not (m.c.useChangesCommand or '--repo' in options):  # line 608
        changes(argument, options, onlys, excps)  # line 608
        return  # line 608
    current = m.branch  # type: int  # line 609
    strict = '--strict' in options or m.strict  # type: bool  # line 610
    info(usage.MARKER + "Offline repository status")  # line 611
    info("Repository root:     %s" % os.getcwd())  # line 612
    info("Underlying VCS root: %s" % vcs)  # line 613
    info("Underlying VCS type: %s" % cmd)  # line 614
    info("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # line 615
    info("Current SOS version: %s" % version.__version__)  # line 616
    info("At creation version: %s" % m.version)  # line 617
    info("Metadata format:     %s" % m.format)  # line 618
    info("Content checking:    %sactivated" % ("" if m.strict else "de"))  # line 619
    info("Data compression:    %sactivated" % ("" if m.compress else "de"))  # line 620
    info("Repository mode:     %s" % ("track" if m.track else ("picky" if m.picky else "simple")))  # line 621
    info("Number of branches:  %d" % len(m.branches))  # line 622
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 623
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 624
    m.loadBranch(current)  # line 625
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 626
    m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision  # line 508  # line 627
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 628
    printo("%s File tree %s" % ((CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged"))  # TODO use other marks if no unicode console detected TODO bad choice of symbols for changed vs. unchanged  # line 633
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 634
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 635
        payload = 0  # type: int  # count used storage per branch  # line 636
        overhead = 0  # type: int  # count used storage per branch  # line 636
        original = 0  # type: int  # count used storage per branch  # line 636
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 637
            for f in fs:  # TODO count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 638
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 639
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 639
                else:  # line 640
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 640
        pl_amount = float(payload) / MEBI  # type: float  # line 641
        oh_amount = float(overhead) / MEBI  # type: float  # line 641
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 643
        for commit_ in range(max(m.commits) if m.commits else 0):  # line 644
            m.loadCommit(m.branch, commit_)  # line 645
            for pinfo in m.paths.values():  # line 646
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 646
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 647
        printo("  %s b%d%s @%s (%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % ("'%s'" % branch.name)) if branch.name else "", strftime(branch.ctime), "in sync" if branch.inSync else "modified", len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 648
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 649
        info("\nTracked file patterns:")  # TODO print matching untracking patterns side-by-side  # line 650
        printo(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 651
        info("\nUntracked file patterns:")  # line 652
        printo(ajoin("  | ", m.branches[m.branch].untracked, "\n"))  # line 653

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 655
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 662
    assert not (check and commit)  # line 663
    m = Metadata()  # type: Metadata  # line 664
    force = '--force' in options  # type: bool  # line 665
    strict = '--strict' in options or m.strict  # type: bool  # line 666
    if argument is not None:  # line 667
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 668
        if branch is None:  # line 669
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 669
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 670
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 671

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 674
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 675
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 676
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 677
    if check and modified(changed) and not force:  # line 682
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 683
        Exit("File tree contains changes. Use --force to proceed")  # line 684
    elif commit:  # line 685
        if not modified(changed) and not force:  # line 686
            Exit("Nothing to commit")  # line 686
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 687
        if msg:  # line 688
            printo(msg)  # line 688

    if argument is not None:  # branch/revision specified  # line 690
        m.loadBranch(branch)  # knows commits of target branch  # line 691
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 692
        revision = m.correctNegativeIndexing(revision)  # line 693
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 694
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 695

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 697
    ''' Continue work on another branch, replacing file tree changes. '''  # line 698
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 699
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 700

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 703
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 704
    else:  # full file switch  # line 705
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 706
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 707

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 714
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 715
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 716
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 717
                rms.append(a)  # line 717
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 718
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 718
        if modified(changed) and not force:  # line 719
            m.listChanges(changed)  # line 719
            Exit("File tree contains changes. Use --force to proceed")  # line 719
        if verbose:  # line 720
            info(usage.MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 720
        if not modified(todos):  # line 721
            info("No changes to current file tree")  # line 722
        else:  # integration required  # line 723
            for path, pinfo in todos.deletions.items():  # line 724
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 725
                printo("ADD " + path)  # line 726
            for path, pinfo in todos.additions.items():  # line 727
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 728
                printo("DEL " + path)  # line 729
            for path, pinfo in todos.modifications.items():  # line 730
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 731
                printo("MOD " + path)  # line 732
    m.branch = branch  # line 733
    m.saveBranches()  # store switched path info  # line 734
    info(usage.MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 735

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 737
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 741
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 742
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 743
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 744
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 745
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 746
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 747
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 748
    if verbose:  # line 749
        info(usage.MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 749

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 752
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 753
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 754
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 755
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 760
        if trackingUnion != trackingPatterns:  # nothing added  # line 761
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 762
        else:  # line 763
            info("Nothing to update")  # but write back updated branch info below  # line 764
    else:  # integration required  # line 765
        add_all = None  # type: _coconut.typing.Optional[str]  # line 766
        del_all = None  # type: _coconut.typing.Optional[str]  # line 766
        selection = None  # type: str  # line 766
        if changed.deletions.items():  # line 767
            printo("Additions:")  # line 767
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 768
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 769
            if add_all is None and mrg == MergeOperation.ASK:  # line 770
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 771
                if selection in "ao":  # line 772
                    add_all = "y" if selection == "a" else "n"  # line 772
                    selection = add_all  # line 772
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 773
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 773
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path)  # TODO document (A) as "selected not to add by user choice"  # line 774
        if changed.additions.items():  # line 775
            printo("Deletions:")  # line 775
        for path, pinfo in changed.additions.items():  # line 776
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 777
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 777
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 778
            if del_all is None and mrg == MergeOperation.ASK:  # line 779
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 780
                if selection in "ao":  # line 781
                    del_all = "y" if selection == "a" else "n"  # line 781
                    selection = del_all  # line 781
            if "y" in (del_all, selection):  # line 782
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 782
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path)  # not contained in other branch, but maybe kept  # line 783
        if changed.modifications.items():  # line 784
            printo("Modifications:")  # line 784
        for path, pinfo in changed.modifications.items():  # line 785
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 786
            binary = not m.isTextType(path)  # type: bool  # line 787
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 788
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 789
                printo(("MOD " if not binary else "BIN ") + path)  # TODO print mtime, size differences?  # line 790
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 791
            if op == "t":  # line 792
                printo("THR " + path)  # blockwise copy of contents  # line 793
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 793
            elif op == "m":  # line 794
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 795
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 795
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 796
                if current == file and verbose:  # line 797
                    info("No difference to versioned file")  # line 797
                elif file is not None:  # if None, error message was already logged  # line 798
                    merged = None  # type: bytes  # line 799
                    nl = None  # type: bytes  # line 799
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 800
                    if merged != current:  # line 801
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 802
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 802
                    elif verbose:  # TODO but update timestamp?  # line 803
                        info("No change")  # TODO but update timestamp?  # line 803
            else:  # mine or wrong input  # line 804
                printo("MNE " + path)  # nothing to do! same as skip  # line 805
    info(usage.MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 806
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 807
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 808
    m.saveBranches()  # line 809

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 811
    ''' Remove a branch entirely. '''  # line 812
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 813
    if len(m.branches) == 1:  # line 814
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 814
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 815
    if branch is None or branch not in m.branches:  # line 816
        Exit("Cannot delete unknown branch %r" % branch)  # line 816
    if verbose:  # line 817
        info(usage.MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 817
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 818
    info(usage.MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 819

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 821
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 822
    force = '--force' in options  # type: bool  # line 823
    m = Metadata()  # type: Metadata  # line 824
    if not (m.track or m.picky):  # line 825
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 825
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 826
    if pattern in patterns:  # line 827
        Exit("Pattern '%s' already tracked" % pattern)  # line 827
    if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 828
        Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 828
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 829
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 830
    patterns.append(pattern)  # line 831
    m.saveBranches()  # line 832
    info(usage.MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 833

def remove(relPath: 'str', pattern: 'str', negative: 'bool'=False):  # line 835
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 836
    m = Metadata()  # type: Metadata  # line 837
    if not (m.track or m.picky):  # line 838
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 838
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 839
    if pattern not in patterns:  # line 840
        suggestion = _coconut.set()  # type: Set[str]  # line 841
        for pat in patterns:  # line 842
            if fnmatch.fnmatch(pattern, pat):  # line 842
                suggestion.add(pat)  # line 842
        if suggestion:  # TODO use same wording as in move  # line 843
            printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 843
        Exit("Tracked pattern '%s' not found" % pattern)  # line 844
    patterns.remove(pattern)  # line 845
    m.saveBranches()  # line 846
    info(usage.MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 847

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 849
    ''' List specified directory, augmenting with repository metadata. '''  # line 850
    m = Metadata()  # type: Metadata  # line 851
    folder = (os.getcwd() if folder is None else folder)  # line 852
    if '--all' in options:  # always start at SOS repo root with --all  # line 853
        folder = m.root  # always start at SOS repo root with --all  # line 853
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 854
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 855
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # line 856
    if verbose:  # line 857
        info(usage.MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 857
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 858
    if relPath.startswith(os.pardir):  # line 859
        Exit("Cannot list contents of folder outside offline repository")  # line 859
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 860
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 861
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 862
        if len(m.tags) > 0:  # line 863
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 863
        return  # line 864
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 865
        if not recursive:  # avoid recursion  # line 866
            dirnames.clear()  # avoid recursion  # line 866
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 867
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 868

        folder = decode(dirpath)  # line 870
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 871
        if patterns:  # line 872
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 873
            if out:  # line 874
                printo("DIR %s\n" % relPath + out)  # line 874
            continue  # with next folder  # line 875
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 876
        if len(files) > 0:  # line 877
            printo("DIR %s" % relPath)  # line 877
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 878
            ignore = None  # type: _coconut.typing.Optional[str]  # line 879
            for ig in m.c.ignores:  # remember first match  # line 880
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 880
                    ignore = ig  # remember first match  # line 880
                    break  # remember first match  # line 880
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 881
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 881
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 881
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 881
                        break  # found a white list entry for ignored file, undo ignoring it  # line 881
            matches = []  # type: List[str]  # line 882
            if not ignore:  # line 883
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 884
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 885
                        matches.append(os.path.basename(pattern))  # line 885
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 886
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 887

def log(options: '_coconut.typing.Sequence[str]'=[]):  # line 889
    ''' List previous commits on current branch. '''  # line 890
    changes_ = "--changes" in options  # type: bool  # line 891
    diff_ = "--diff" in options  # type: bool  # line 892
    number_ = tryOrDefault(lambda _=None: int(sys.argv[sys.argv.index("-n") + 1]), None)  # type: _coconut.typing.Optional[int]  # line 893
    m = Metadata()  # type: Metadata  # line 894
    m.loadBranch(m.branch)  # knows commit history  # line 895
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 896
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 897
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 898
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 899
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 900
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 901
    commit = None  # type: CommitInfo  # line 902
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 903
    for no in range(maxi + 1):  # line 904
        if no in m.commits:  # line 905
            commit = m.commits[no]  # line 905
        else:  # line 906
            if n.branch != n.getParentBranch(m.branch, no):  # line 907
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 907
            commit = n.commits[no]  # line 908
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 909
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 910
        if "--all" in options or no >= max(0, maxi + 1 - ((lambda _coconut_none_coalesce_item: m.c.logLines if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(number_))):  # line 911
            _add = news - olds  # type: FrozenSet[str]  # line 912
            _del = olds - news  # type: FrozenSet[str]  # line 913
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 915
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds})  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 917
            printo("  %s r%s @%s (+%02d/-%02d/%s%02d/T%02d) |%s|%s" % ("*" if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(_add), len(_del), PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", len(_mod), _txt, ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)), "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else ""))  # line 918
            if changes_:  # TODO moves detection?  # line 919
                (m.listChanges)(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}))  # TODO moves detection?  # line 919
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 920
                pass  #  _diff(m, changes)  # needs from revision diff  # line 920
        olds = news  # replaces olds for next revision compare  # line 921
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 922

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 924
    ''' Exported entire repository as archive for easy transfer. '''  # line 925
    if verbose:  # line 926
        info(usage.MARKER + "Dumping repository to archive...")  # line 926
    m = Metadata()  # type: Metadata  # to load the configuration  # line 927
    progress = '--progress' in options  # type: bool  # line 928
    delta = '--full' not in options  # type: bool  # line 929
    skipBackup = '--skip-backup' in options  # type: bool  # line 930
    import functools  # line 931
    import locale  # line 931
    import warnings  # line 931
    import zipfile  # line 931
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 932
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 932
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 932
    except:  # line 933
        compression = zipfile.ZIP_STORED  # line 933

    if argument is None:  # line 935
        Exit("Argument missing (target filename)")  # line 935
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 936
    entries = []  # type: List[str]  # line 937
    if os.path.exists(encode(argument)) and not skipBackup:  # line 938
        try:  # line 939
            if verbose:  # line 940
                info("Creating backup...")  # line 940
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 941
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 942
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 942
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 942
        except Exception as E:  # line 943
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 943
    if verbose:  # line 944
        info("Dumping revisions...")  # line 944
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 945
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 945
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 946
        _zip.debug = 0  # suppress debugging output  # line 947
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 948
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 949
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 950
        totalsize = 0  # type: int  # line 951
        start_time = time.time()  # type: float  # line 952
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 953
            dirpath = decode(dirpath)  # line 954
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 955
                continue  # don't backup backups  # line 955
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 956
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 957
            filenames[:] = sorted([decode(f) for f in filenames])  # line 958
            for filename in filenames:  # line 959
                abspath = os.path.join(dirpath, filename)  # type: str  # line 960
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 961
                totalsize += os.stat(encode(abspath)).st_size  # line 962
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 963
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 964
                    continue  # don't backup backups  # line 964
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 965
                    if show:  # line 966
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 966
                    _zip.write(abspath, relpath)  # write entry into archive  # line 967
        if delta:  # line 968
            _zip.comment = (encode(UTF8))(("Delta dump from %r" % strftime()))  # line 968
    info("\r" + pure.ljust(usage.MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 969

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 971
    ''' Write changes made to the branch into one commit of the underlying VCS. TODO add option to non-permanently add files for VCSs that track by default. '''  # line 972
    m = Metadata()  # line 973
    if not (m.track or m.picky):  # TODO add manual file picking mode (add by extension, recursive, ... see issue for that)  # line 974
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode (add by extension, recursive, ... see issue for that)  # line 974
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 975
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 976
    if maxi is None:  # line 977
        Exit("No revision to publish on current (or any parent-) branch")  # line 977
    m.computeSequentialPathSet(branch, maxi)  # load all commits up to specified revision  # line 978
# TODO only add changed files!
    import subprocess  # only required in this section  # line 980
# TODO stash/rollback when Git? or implement global mechanism?
# TODO discuss only commit changes from r1.. forward, or everything in repo
    for path, pinfo in m.paths.items():  # line 983
        command = fitStrings(m.paths, prefix="%s add" % cmd)  # type: str  # line 984
#    returncode:int = subprocess.Popen(command, shell = False).wait()
        returncode = 0  # type: int  # line 986
        printo(command, shell=False)  # line 986
        if returncode != 0:  # TODO use VCS name, not command  # line 987
            Exit("Error adding files from SOS revision to underlying VCS. Leaving in inconsistent %s state" % cmd)  # TODO use VCS name, not command  # line 987
    tracked = None  # type: bool  # line 988
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 988
    tracked, commitArgs = vcsCommits[cmd]  # line 988
#returncode = subprocess.Popen('%s commit -m "%s" %s' % (cmd, message ?? "Committed from SOS branch/revision %s/r%02d on %s" % (strftime(now)).replace("\"", "\\\""), _.branches[branch].name ?? ("b%d" % _.branch), revision, commitArgs ?? "")).wait()  # TODO quote-escaping on Windows
    printo('%s commit -m "%s" %s' % (cmd, ("Committed from SOS branch/revision %s/r%02d on %s" % (strftime(now)).replace("\"", "\\\"") if message is None else message), (lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[branch].name), revision, ("" if commitArgs is None else commitArgs)))  # TODO quote-escaping on Windows  # line 990
    if returncode != 0:  # line 991
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 991
    if tracked:  # line 992
        printo("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 992

def config(arguments: 'List[str]', options: 'List[str]'=[]):  # line 994
    command = None  # type: str  # line 995
    key = None  # type: str  # line 995
    value = None  # type: str  # line 995
    v = None  # type: str  # line 995
    command, key, value = (arguments + [None] * 2)[:3]  # line 996
    if command is None:  # line 997
        usage.usage("help", verbose=True)  # line 997
    if command not in ["set", "unset", "show", "list", "add", "rm"]:  # line 998
        Exit("Unknown config command")  # line 998
    local = "--local" in options  # type: bool  # line 999
    m = Metadata()  # type: Metadata  # loads layered configuration as well. TODO warning if repo not exists  # line 1000
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1001
    if command == "set":  # line 1002
        if None in (key, value):  # line 1003
            Exit("Key or value not specified")  # line 1003
        if key not in (([] if local else CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1004
            Exit("Unsupported key for %s configuration %r" % ("local " if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1004
        if key in CONFIGURABLE_FLAGS and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1005
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1005
        c[key] = value.lower() in TRUTH_VALUES if key in CONFIGURABLE_FLAGS else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1006
    elif command == "unset":  # line 1007
        if key is None:  # line 1008
            Exit("No key specified")  # line 1008
        if key not in c.keys():  # HINT: Works on local configurations when used with --local  # line 1009
            Exit("Unknown key")  # HINT: Works on local configurations when used with --local  # line 1009
        del c[key]  # line 1010
    elif command == "add":  # line 1011
        if None in (key, value):  # line 1012
            Exit("Key or value not specified")  # line 1012
        if key not in CONFIGURABLE_LISTS:  # line 1013
            Exit("Unsupported key %r" % key)  # line 1013
        if key not in c.keys():  # prepare empty list, or copy from global, add new value below  # line 1014
            c[key] = [_ for _ in c.__defaults[key]] if local else []  # prepare empty list, or copy from global, add new value below  # line 1014
        elif value in c[key]:  # line 1015
            Exit("Value already contained, nothing to do")  # line 1015
        if ";" in value:  # line 1016
            c[key].append(removePath(key, value))  # line 1016
        else:  # line 1017
            c[key].extend([removePath(key, v) for v in value.split(";")])  # line 1017
    elif command == "rm":  # line 1018
        if None in (key, value):  # line 1019
            Exit("Key or value not specified")  # line 1019
        if key not in c.keys():  # line 1020
            Exit("Unknown key %r" % key)  # line 1020
        if value not in c[key]:  # line 1021
            Exit("Unknown value %r" % value)  # line 1021
        c[key].remove(value)  # line 1022
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1023
            del c[key]  # remove local entry, to fallback to global  # line 1023
    else:  # Show or list  # line 1024
        if key == "ints":  # list valid configuration items  # line 1025
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1025
        elif key == "flags":  # line 1026
            printo(", ".join(CONFIGURABLE_FLAGS))  # line 1026
        elif key == "lists":  # line 1027
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1027
        elif key == "texts":  # line 1028
            printo(", ".join([_ for _ in defaults.keys() if _ not in (CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS)]))  # line 1028
        else:  # line 1029
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1030
            c = m.c  # always use full configuration chain  # line 1031
            try:  # attempt single key  # line 1032
                assert key is not None  # force exception  # line 1033
                c[key]  # force exception  # line 1033
                l = key in c.keys()  # type: bool  # line 1034
                g = key in c.__defaults.keys()  # type: bool  # line 1034
                printo("%s %s %r" % (key.rjust(20), out[3] if not (l or g) else (out[1] if l else out[2]), c[key]))  # line 1035
            except:  # normal value listing  # line 1036
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # line 1037
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1038
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1039
                for k, vt in sorted(vals.items()):  # line 1040
                    printo("%s %s %s" % (k.rjust(20), out[vt[1]], vt[0]))  # line 1040
                if len(c.keys()) == 0:  # line 1041
                    info("No local configuration stored")  # line 1041
                if len(c.__defaults.keys()) == 0:  # line 1042
                    info("No global configuration stored")  # line 1042
        return  # in case of list, no need to store anything  # line 1043
    if local:  # saves changes of repoConfig  # line 1044
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1044
        m.saveBranches()  # saves changes of repoConfig  # line 1044
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1044
    else:  # global config  # line 1045
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1046
        if f is None:  # line 1047
            error("Error saving user configuration: %r" % h)  # line 1047
        else:  # line 1048
            Exit("OK", code=0)  # line 1048

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1050
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1053
    if verbose:  # line 1054
        info(usage.MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1054
    force = '--force' in options  # type: bool  # line 1055
    soft = '--soft' in options  # type: bool  # line 1056
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1057
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1057
    m = Metadata()  # type: Metadata  # line 1058
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1059
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1060
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1061
    if not matching and not force:  # line 1062
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1062
    if not (m.track or m.picky):  # line 1063
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 1063
    if pattern not in patterns:  # list potential alternatives and exit  # line 1064
        for tracked in (t for t in patterns if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 1065
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1066
            if alternative:  # line 1067
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 1067
        if not (force or soft):  # line 1068
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 1068
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1069
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1070
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1071
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 1075
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1076
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1076
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1077
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1078
    if len({st[1] for st in matches}) != len(matches):  # line 1079
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1079
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1080
    if os.path.exists(encode(newRelPath)):  # line 1081
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1082
        if exists and not (force or soft):  # line 1083
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1083
    else:  # line 1084
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1084
    if not soft:  # perform actual renaming  # line 1085
        for (source, target) in matches:  # line 1086
            try:  # line 1087
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1087
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1088
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1088
    patterns[patterns.index(pattern)] = newPattern  # line 1089
    m.saveBranches()  # line 1090

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1092
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1093
    debug("Parsing command-line arguments...")  # line 1094
    root = os.getcwd()  # line 1095
    try:  # line 1096
        onlys, excps = parseOnlyOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1097
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1098
        arguments = [c.strip() for c in sys.argv[2:] if not (c.startswith("-") and (len(c) == 2 or c[1] == "-"))]  # type: List[_coconut.typing.Optional[str]]  # line 1099
        options = [c.strip() for c in sys.argv[2:] if c.startswith("-") and (len(c) == 2 or c[1] == "-")]  # options with arguments have to be parsed from sys.argv  # line 1100
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1101
        if command[:1] in "amr":  # line 1102
            relPath, pattern = relativize(root, os.path.join(cwd, arguments[0] if arguments else "."))  # line 1102
        if command[:1] == "m":  # line 1103
            if len(arguments) < 2:  # line 1104
                Exit("Need a second file pattern argument as target for move command")  # line 1104
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1105
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1106
        if command[:1] == "a":  # addnot  # line 1107
            add(relPath, pattern, options, negative="n" in command)  # addnot  # line 1107
        elif command[:1] == "b":  # line 1108
            branch(arguments[0], arguments[1], options)  # line 1108
        elif command[:3] == "com":  # line 1109
            commit(arguments[0], options, onlys, excps)  # line 1109
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1110
            changes(arguments[0], options, onlys, excps)  # "changes" (legacy)  # line 1110
        elif command[:2] == "ci":  # line 1111
            commit(arguments[0], options, onlys, excps)  # line 1111
        elif command[:3] == 'con':  # line 1112
            config(arguments, options)  # line 1112
        elif command[:2] == "de":  # line 1113
            destroy(arguments[0], options)  # line 1113
        elif command[:2] == "di":  # line 1114
            diff(arguments[0], options, onlys, excps)  # line 1114
        elif command[:2] == "du":  # line 1115
            dump(arguments[0], options)  # line 1115
        elif command[:1] == "h":  # line 1116
            usage.usage(arguments[0], verbose=verbose)  # line 1116
        elif command[:2] == "lo":  # line 1117
            log(options)  # line 1117
        elif command[:2] == "li":  # line 1118
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1118
        elif command[:2] == "ls":  # line 1119
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1119
        elif command[:1] == "m":  # mvnot  # line 1120
            move(relPath, pattern, newRelPath, newPattern, options, negative="n" in command)  # mvnot  # line 1120
        elif command[:2] == "of":  # line 1121
            offline(arguments[0], arguments[1], options)  # line 1121
        elif command[:2] == "on":  # line 1122
            online(options)  # line 1122
        elif command[:1] == "p":  # line 1123
            publish(arguments[0], cmd, options, onlys, excps)  # line 1123
        elif command[:1] == "r":  # rmnot  # line 1124
            remove(relPath, pattern, negative="n" in command)  # rmnot  # line 1124
        elif command[:2] == "st":  # line 1125
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1125
        elif command[:2] == "sw":  # line 1126
            switch(arguments[0], options, onlys, excps)  # line 1126
        elif command[:1] == "u":  # line 1127
            update(arguments[0], options, onlys, excps)  # line 1127
        elif command[:1] == "v":  # line 1128
            usage.usage(arguments[0], version=True)  # line 1128
        else:  # line 1129
            Exit("Unknown command '%s'" % command)  # line 1129
        Exit(code=0)  # regular exit  # line 1130
    except (Exception, RuntimeError) as E:  # line 1131
        exception(E)  # line 1132
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing")  # line 1133

def main():  # line 1135
    global debug, info, warn, error  # to modify logger  # line 1136
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1137
    _log = Logger(logging.getLogger(__name__))  # line 1138
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1138
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1139
        sys.argv.remove(option)  # clean up program arguments  # line 1139
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1140
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1140
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1141
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1142
    debug("Found root folders for SOS | VCS:  %s | %s" % (("-" if root is None else root), ("-" if vcs is None else vcs)))  # line 1143
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1144
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1145
    if force_sos or root is not None or (("" if command is None else command))[:2] == "of" or (("" if command is None else command))[:1] in "hv":  # in offline mode or just going offline TODO what about git config?  # line 1146
        cwd = os.getcwd()  # line 1147
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1148
        parse(vcs, cwd, cmd)  # line 1149
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1150
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1151
        import subprocess  # only required in this section  # line 1152
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1153
        inp = ""  # type: str  # line 1154
        while True:  # line 1155
            so, se = process.communicate(input=inp)  # line 1156
            if process.returncode is not None:  # line 1157
                break  # line 1157
            inp = sys.stdin.read()  # line 1158
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1159
            if root is None:  # line 1160
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1160
            m = Metadata(root)  # type: Metadata  # line 1161
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1162
            m.saveBranches()  # line 1163
    else:  # line 1164
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1164


# Main part
force_sos = '--sos' in sys.argv  # type: bool  # line 1168
force_vcs = '--vcs' in sys.argv  # type: bool  # line 1169
verbose = '--verbose' in sys.argv or '-v' in sys.argv  # type: bool  # imported from utility, and only modified here  # line 1170
debug_ = os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv  # type: bool  # line 1171
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1172
_log = Logger(logging.getLogger(__name__))  # line 1173
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1173
if __name__ == '__main__':  # line 1174
    main()  # line 1174
