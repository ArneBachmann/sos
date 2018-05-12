#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x8a4aeb41

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


# Lazy module auto-import for quick initialization
shutil = None  # type: _coconut.typing.Optional[Any]  # line 25
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
        revision = max(_.commits) if _.commits else 0  # type: int  # line 173
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
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO what if last switch was to an earlier revision? no persisting of last checkout  # line 211
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 212
                for path, pinfo in _.paths.items():  # line 213
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 214
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 215
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 216
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 217
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 218

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 220
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 223
        import collections  # used almost only here  # line 224
        binfo = None  # type: BranchInfo  # typing info  # line 225
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 226
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 227
        if deps:  # need to copy all parent revisions to dependent branches first  # line 228
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 229
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 230
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 231
                for dep, _rev in deps:  # line 232
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO align placement of indicator with other uses of progress  # line 233
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 234
#          if rev in _.commits:  # TODO uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 236
                    shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 237
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 238
                for rev in range(minrev + 1, _rev + 1):  # line 239
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 240
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 241
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 242
                        newcommits[dep][rev] = _.commits[rev]  # line 243
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 244
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 245
        printo(pure.ljust() + "\r")  # clean line output  # line 246
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 247
        tryOrIgnore(lambda: os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?"))  # line 248
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 249
        del _.branches[branch]  # line 250
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 251
        _.saveBranches()  # persist modified branches list  # line 252
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 253
            _.commits = commits  # line 254
            _.saveBranch(branch)  # line 255
        _.commits.clear()  # clean memory  # line 256
        return binfo  # line 257

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 259
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 260
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 261
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 262
            _.paths = json.load(fd)  # line 262
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 263
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 264

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 266
        ''' Save all file information to a commit meta data file. '''  # line 267
        target = revisionFolder(branch, revision, base=_.root)  # type: str  # line 268
        tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 269
        tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 270
        with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 271
            json.dump(_.paths, fd, ensure_ascii=False)  # line 271

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 273
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 282
        import collections  # used only in this method  # line 283
        write = branch is not None and revision is not None  # line 284
        if write:  # line 285
            try:  # line 286
                os.makedirs(encode(revisionFolder(branch, revision, base=_.root)))  # line 286
            except FileExistsError:  # HINT "try" only necessary for *testing* hash collision code (!) TODO probably raise exception otherwise in any case?  # line 287
                pass  # HINT "try" only necessary for *testing* hash collision code (!) TODO probably raise exception otherwise in any case?  # line 287
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # TODO Needs explicity initialization due to mypy problems with default arguments :-(  # line 288
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 289
        hashed = None  # type: _coconut.typing.Optional[str]  # line 290
        written = None  # type: int  # line 290
        compressed = 0  # type: int  # line 290
        original = 0  # type: int  # line 290
        start_time = time.time()  # type: float  # line 290
        knownPaths = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 291
        for path, pinfo in _.paths.items():  # line 292
            if pinfo.size is not None and (considerOnly is None or any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in considerOnly))) and (dontConsider is None or not any((path[:path.rindex(SLASH)] == pattern[:pattern.rindex(SLASH)] and fnmatch.fnmatch(path[path.rindex(SLASH) + 1:], pattern[pattern.rindex(SLASH) + 1:]) for pattern in dontConsider))):  # line 293
                knownPaths[os.path.dirname(path)].append(os.path.basename(path))  # TODO reimplement using fnmatch.filter and set operations for all files per path for speed  # line 296
        for path, dirnames, filenames in os.walk(_.root):  # line 297
            path = decode(path)  # line 298
            dirnames[:] = [decode(d) for d in dirnames]  # line 299
            filenames[:] = [decode(f) for f in filenames]  # line 300
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 301
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 302
            dirnames.sort()  # line 303
            filenames.sort()  # line 303
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 304
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 305
            if dontConsider:  # line 306
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 307
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 308
                filename = relPath + SLASH + file  # line 309
                filepath = os.path.join(path, file)  # line 310
                try:  # line 311
                    stat = os.stat(encode(filepath))  # line 311
                except Exception as E:  # line 312
                    exception(E)  # line 312
                    continue  # line 312
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 313
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 314
                if show:  # indication character returned  # line 315
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 316
                    printo(pure.ljust(outstring), nl="")  # line 317
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 318
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 319
                    nameHash = hashStr(filename)  # line 320
                    try:  # line 321
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=nameHash) if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 322
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 323
                        compressed += written  # line 324
                        original += size  # line 324
                    except Exception as E:  # line 325
                        exception(E)  # line 325
                    continue  # with next file  # line 326
                last = _.paths[filename]  # filename is known - check for modifications  # line 327
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 328
                    try:  # line 329
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=last.nameHash) if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 330
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 331
                        continue  # line 331
                    except Exception as E:  # line 332
                        exception(E)  # line 332
                elif size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False)):  # detected a modification TODO wrap hashFile exception  # line 333
                    try:  # line 334
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=last.nameHash) if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 335
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 336
                    except Exception as E:  # line 337
                        exception(E)  # line 337
                else:  # with next file  # line 338
                    continue  # with next file  # line 338
                compressed += written  # line 339
                original += last.size if inverse else size  # line 339
            if relPath in knownPaths:  # at least one file is tracked TODO may leave empty lists in dict  # line 340
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked TODO may leave empty lists in dict  # line 340
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 341
            for file in names:  # line 342
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 343
                    continue  # don't mark ignored files as deleted  # line 343
                pth = path + SLASH + file  # type: str  # line 344
                changed.deletions[pth] = _.paths[pth]  # line 345
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed))  # line 346
        if progress:  # forces clean line of progress output  # line 347
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 347
        elif verbose:  # line 348
            info("Finished detecting changes")  # line 348
        tt = time.time() - start_time  # type: float  # line 349
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # line 349
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 350
        msg = (msg + " | " if msg else "") + ("Transfer speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 351
        return (changed, msg if msg else None)  # line 352

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 354
        ''' Returns nothing, just updates _.paths in place. '''  # line 355
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 356

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 358
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 359
        try:  # load initial paths  # line 360
            _.loadCommit(branch, startwith)  # load initial paths  # line 360
        except:  # no revisions  # line 361
            yield {}  # no revisions  # line 361
            return None  # no revisions  # line 361
        if incrementally:  # line 362
            yield _.paths  # line 362
        m = Metadata(_.root)  # type: Metadata  # next changes TODO avoid loading all metadata and config  # line 363
        rev = None  # type: int  # next changes TODO avoid loading all metadata and config  # line 363
        for rev in range(startwith + 1, revision + 1):  # line 364
            m.loadCommit(branch, rev)  # line 365
            for p, info in m.paths.items():  # line 366
                if info.size == None:  # line 367
                    del _.paths[p]  # line 367
                else:  # line 368
                    _.paths[p] = info  # line 368
            if incrementally:  # line 369
                yield _.paths  # line 369
        yield None  # for the default case - not incrementally  # line 370

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 372
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 373
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 374

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 376
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 379
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 380
            return (_.branch, -1)  # no branch/revision specified  # line 380
        argument = argument.strip()  # line 381
        if argument.startswith(SLASH):  # current branch  # line 382
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 382
        if argument.endswith(SLASH):  # line 383
            try:  # line 384
                return (_.getBranchByName(argument[:-1]), -1)  # line 384
            except ValueError:  # line 385
                Exit("Unknown branch label '%s'" % argument)  # line 385
        if SLASH in argument:  # line 386
            b, r = argument.split(SLASH)[:2]  # line 387
            try:  # line 388
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 388
            except ValueError:  # line 389
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 389
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 390
        if branch not in _.branches:  # line 391
            branch = None  # line 391
        try:  # either branch name/number or reverse/absolute revision number  # line 392
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 392
        except:  # line 393
            Exit("Unknown branch label or wrong number format")  # line 393
        Exit("This should never happen. Please create a issue report")  # line 394
        return (None, None)  # line 394

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 396
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 398
        while True:  # line 399
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 400
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 401
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 402
                break  # line 402
            revision -= 1  # line 403
            if revision < 0:  # line 404
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 404
        return revision, source  # line 405

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 407
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 408
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 409
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 410
            return [branch]  # found. need to load commit from other branch instead  # line 410
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 411
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 411
        return others  # line 412

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 414
        return _.getParentBranches(branch, revision)[-1]  # line 414

    @_coconut_tco  # line 416
    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 416
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 417
        m = Metadata()  # type: Metadata  # line 418
        other = branch  # type: _coconut.typing.Optional[int]  # line 419
        while other is not None:  # line 420
            m.loadBranch(other)  # line 421
            if m.commits:  # line 422
                return _coconut_tail_call(max, m.commits)  # line 422
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 423
        return None  # line 424

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 426
        ''' Copy versioned file to other branch/revision. '''  # line 427
        target = revisionFolder(toBranch, toRevision, base=_.root, file=pinfo.nameHash)  # type: str  # line 428
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 429
        shutil.copy2(encode(source), encode(target))  # line 430

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 432
        ''' Return file contents, or copy contents into file path provided. '''  # line 433
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 434
        try:  # line 435
            with openIt(source, "r", _.compress) as fd:  # line 435
                if toFile is None:  # read bytes into memory and return  # line 436
                    return fd.read()  # read bytes into memory and return  # line 436
                with open(encode(toFile), "wb") as to:  # line 437
                    while True:  # line 438
                        buffer = fd.read(bufSize)  # line 439
                        to.write(buffer)  # line 440
                        if len(buffer) < bufSize:  # line 441
                            break  # line 441
                    return None  # line 442
        except Exception as E:  # line 443
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 443
        None  # line 444

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 446
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 447
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 448
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 448
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 449
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 450
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 451
        if pinfo.size == 0:  # line 452
            with open(encode(target), "wb"):  # line 453
                pass  # line 453
            try:  # update access/modification timestamps on file system  # line 454
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 454
            except Exception as E:  # line 455
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 455
            return None  # line 456
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 457
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 459
            while True:  # line 460
                buffer = fd.read(bufSize)  # line 461
                to.write(buffer)  # line 462
                if len(buffer) < bufSize:  # line 463
                    break  # line 463
        try:  # update access/modification timestamps on file system  # line 464
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 464
        except Exception as E:  # line 465
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 465
        return None  # line 466


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 470
    ''' Initial command to start working offline. '''  # line 471
    if os.path.exists(encode(metaFolder)):  # line 472
        if '--force' not in options:  # line 473
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 473
        try:  # line 474
            for entry in os.listdir(metaFolder):  # line 475
                resource = metaFolder + os.sep + entry  # line 476
                if os.path.isdir(resource):  # line 477
                    shutil.rmtree(encode(resource))  # line 477
                else:  # line 478
                    os.unlink(encode(resource))  # line 478
        except:  # line 479
            Exit("Cannot reliably remove previous repository contents. Please remove .sos folder manually prior to going offline")  # line 479
    m = Metadata(offline=True)  # type: Metadata  # line 480
    if '--strict' in options or m.c.strict:  # always hash contents  # line 481
        m.strict = True  # always hash contents  # line 481
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 482
        m.compress = True  # plain file copies instead of compressed ones  # line 482
    if '--picky' in options or m.c.picky:  # Git-like  # line 483
        m.picky = True  # Git-like  # line 483
    elif '--track' in options or m.c.track:  # Svn-like  # line 484
        m.track = True  # Svn-like  # line 484
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 485
    if title:  # line 486
        printo(title)  # line 486
    if verbose:  # line 487
        info(usage.MARKER + "Going offline...")  # line 487
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 488
    m.branch = 0  # line 489
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 490
    info(usage.MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 491

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 493
    ''' Finish working offline. '''  # line 494
    if verbose:  # line 495
        info(usage.MARKER + "Going back online...")  # line 495
    force = '--force' in options  # type: bool  # line 496
    m = Metadata()  # type: Metadata  # line 497
    strict = '--strict' in options or m.strict  # type: bool  # line 498
    m.loadBranches()  # line 499
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 500
        Exit("There are still unsynchronized (modified) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 500
    m.loadBranch(m.branch)  # line 501
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 502
    if options.count("--force") < 2:  # line 503
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 504
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 505
        if modified(changed):  # line 506
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 510
    try:  # line 511
        shutil.rmtree(encode(metaFolder))  # line 511
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 511
    except Exception as E:  # line 512
        Exit("Error removing offline repository: %r" % E)  # line 512
    info(usage.MARKER + "Offline repository removed, you're back online")  # line 513

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 515
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not necessary, as either branching from last  revision anyway, or branching file tree anyway.
  '''  # line 518
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 519
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 520
    fast = '--fast' in options  # type: bool  # branch by referencing TODO move to default and use --full instead for old behavior  # line 521
    m = Metadata()  # type: Metadata  # line 522
    m.loadBranch(m.branch)  # line 523
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 524
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 525
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 525
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 526
    if verbose:  # line 527
        info(usage.MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 527
    if last:  # branch from last revision  # line 528
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 528
    else:  # branch from current file tree state  # line 529
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 529
    if not stay:  # line 530
        m.branch = branch  # line 530
    m.saveBranches()  # TODO or indent again?  # line 531
    info(usage.MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 532

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'ChangeSet':  # line 534
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 535
    m = Metadata()  # type: Metadata  # line 536
    branch = None  # type: _coconut.typing.Optional[int]  # line 536
    revision = None  # type: _coconut.typing.Optional[int]  # line 536
    strict = '--strict' in options or m.strict  # type: bool  # line 537
    branch, revision = m.parseRevisionString(argument)  # line 538
    if branch not in m.branches:  # line 539
        Exit("Unknown branch")  # line 539
    m.loadBranch(branch)  # knows commits  # line 540
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 541
    if verbose:  # line 542
        info(usage.MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 542
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 543
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 544
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time())  # line 549
    return changed  # returning for unit tests only TODO remove?  # line 550

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False):  # TODO introduce option to diff against committed revision  # line 552
    ''' The diff display code. '''  # line 553
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 554
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 555
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 556
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 557
        content = b""  # type: _coconut.typing.Optional[bytes]  # line 558
        if pinfo.size != 0:  # versioned file  # line 559
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 559
            assert content is not None  # versioned file  # line 559
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current file  # line 560
        blocks = None  # type: List[MergeBlock]  # line 561
        nl = None  # type: bytes  # line 561
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 562
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 563
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 564
        for block in blocks:  # line 565
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # TODO show color via (n)curses or other library?  # line 568
                for no, line in enumerate(block.lines):  # line 569
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 569
            elif block.tipe == MergeBlockType.REMOVE:  # line 570
                for no, line in enumerate(block.lines):  # line 571
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 571
            elif block.tipe == MergeBlockType.REPLACE:  # line 572
                for no, line in enumerate(block.replaces.lines):  # line 573
                    printo(wrap("-~- %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)))  # line 573
                for no, line in enumerate(block.lines):  # line 574
                    printo(wrap("+~+ %%0%dd |%%s|" % linemax % (no + block.line, line)))  # line 574
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 577
                printo()  # line 577

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 579
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 580
    m = Metadata()  # type: Metadata  # line 581
    branch = None  # type: _coconut.typing.Optional[int]  # line 581
    revision = None  # type: _coconut.typing.Optional[int]  # line 581
    strict = '--strict' in options or m.strict  # type: bool  # line 582
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 583
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 584
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 585
    if branch not in m.branches:  # line 586
        Exit("Unknown branch")  # line 586
    m.loadBranch(branch)  # knows commits  # line 587
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 588
    if verbose:  # line 589
        info(usage.MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 589
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 590
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 591
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap)  # line 596

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 598
    ''' Create new revision from file tree changes vs. last commit. '''  # line 599
    m = Metadata()  # type: Metadata  # line 600
    if argument is not None and argument in m.tags:  # line 601
        Exit("Illegal commit message. It was already used as a tag name")  # line 601
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 602
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 604
        Exit("No file patterns staged for commit in picky mode")  # line 604
    if verbose:  # line 605
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 605
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 606
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed))  # line 607
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 608
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 609
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 610
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 611
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 612
    m.saveBranch(m.branch)  # line 613
    m.loadBranches()  # TODO is it necessary to load again?  # line 614
    if m.picky:  # remove tracked patterns  # line 615
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 615
    else:  # track or simple mode: set branch modified  # line 616
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 616
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 617
        m.tags.append(argument)  # memorize unique tag  # line 617
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 617
    m.saveBranches()  # line 618
    printo(usage.MARKER + "Created new revision r%02d%s (+%02d/-%02d/%s%02d/%s%02d)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changed.additions) - len(changed.moves), len(changed.deletions) - len(changed.moves), PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", len(changed.modifications), MOVE_SYMBOL if m.c.useUnicodeFont else "#", len(changed.moves)))  # line 619

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 621
    ''' Show branches and current repository state. '''  # line 622
    m = Metadata()  # type: Metadata  # line 623
    if not (m.c.useChangesCommand or '--repo' in options):  # line 624
        changes(argument, options, onlys, excps)  # line 624
        return  # line 624
    current = m.branch  # type: int  # line 625
    strict = '--strict' in options or m.strict  # type: bool  # line 626
    info(usage.MARKER + "Offline repository status")  # line 627
    info("Repository root:     %s" % os.getcwd())  # line 628
    info("Underlying VCS root: %s" % vcs)  # line 629
    info("Underlying VCS type: %s" % cmd)  # line 630
    info("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 631
    info("Current SOS version: %s" % version.__version__)  # line 632
    info("At creation version: %s" % m.version)  # line 633
    info("Metadata format:     %s" % m.format)  # line 634
    info("Content checking:    %sactivated" % ("" if m.strict else "de"))  # line 635
    info("Data compression:    %sactivated" % ("" if m.compress else "de"))  # line 636
    info("Repository mode:     %s" % ("track" if m.track else ("picky" if m.picky else "simple")))  # line 637
    info("Number of branches:  %d" % len(m.branches))  # line 638
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 639
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 640
    m.loadBranch(current)  # line 641
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 642
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 643
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 643
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 644
    printo("%s File tree %s" % ((CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged"))  # TODO use other marks if no unicode console detected TODO bad choice of symbols for changed vs. unchanged  # line 649
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 650
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 651
        payload = 0  # type: int  # count used storage per branch  # line 652
        overhead = 0  # type: int  # count used storage per branch  # line 652
        original = 0  # type: int  # count used storage per branch  # line 652
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 653
            for f in fs:  # TODO count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 654
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 655
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 655
                else:  # line 656
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 656
        pl_amount = float(payload) / MEBI  # type: float  # line 657
        oh_amount = float(overhead) / MEBI  # type: float  # line 657
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 659
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 660
            m.loadCommit(m.branch, commit_)  # line 661
            for pinfo in m.paths.values():  # line 662
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 662
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 663
        printo("  %s b%d%s @%s (%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), "in sync" if branch.inSync else "modified", len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 664
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 665
        info("\nTracked file patterns:")  # TODO print matching untracking patterns side-by-side  # line 666
        printo(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 667
        info("\nUntracked file patterns:")  # line 668
        printo(ajoin("  | ", m.branches[m.branch].untracked, "\n"))  # line 669

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 671
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 678
    assert not (check and commit)  # line 679
    m = Metadata()  # type: Metadata  # line 680
    force = '--force' in options  # type: bool  # line 681
    strict = '--strict' in options or m.strict  # type: bool  # line 682
    if argument is not None:  # line 683
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 684
        if branch is None:  # line 685
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 685
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 686
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 687

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 690
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 691
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 692
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 693
    if check and modified(changed) and not force:  # line 698
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 699
        Exit("File tree contains changes. Use --force to proceed")  # line 700
    elif commit:  # line 701
        if not modified(changed) and not force:  # line 702
            Exit("Nothing to commit")  # line 702
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 703
        if msg:  # line 704
            printo(msg)  # line 704

    if argument is not None:  # branch/revision specified  # line 706
        m.loadBranch(branch)  # knows commits of target branch  # line 707
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 708
        revision = m.correctNegativeIndexing(revision)  # line 709
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 710
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 711

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 713
    ''' Continue work on another branch, replacing file tree changes. '''  # line 714
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 715
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 716

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 719
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 720
    else:  # full file switch  # line 721
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 722
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 723

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 730
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 731
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 732
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 733
                rms.append(a)  # line 733
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 734
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 734
        if modified(changed) and not force:  # line 735
            m.listChanges(changed)  # line 735
            Exit("File tree contains changes. Use --force to proceed")  # line 735
        if verbose:  # line 736
            info(usage.MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 736
        if not modified(todos):  # line 737
            info("No changes to current file tree")  # line 738
        else:  # integration required  # line 739
            for path, pinfo in todos.deletions.items():  # line 740
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 741
                printo("ADD " + path)  # line 742
            for path, pinfo in todos.additions.items():  # line 743
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 744
                printo("DEL " + path)  # line 745
            for path, pinfo in todos.modifications.items():  # line 746
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 747
                printo("MOD " + path)  # line 748
    m.branch = branch  # line 749
    m.saveBranches()  # store switched path info  # line 750
    info(usage.MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 751

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 753
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 757
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 758
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 759
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 760
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 761
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 762
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 763
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 764
    if verbose:  # line 765
        info(usage.MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 765

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 768
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 769
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 770
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 771
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 776
        if trackingUnion != trackingPatterns:  # nothing added  # line 777
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 778
        else:  # line 779
            info("Nothing to update")  # but write back updated branch info below  # line 780
    else:  # integration required  # line 781
        add_all = None  # type: _coconut.typing.Optional[str]  # line 782
        del_all = None  # type: _coconut.typing.Optional[str]  # line 782
        selection = None  # type: str  # line 782
        if changed.deletions.items():  # line 783
            printo("Additions:")  # line 783
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 784
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 785
            if add_all is None and mrg == MergeOperation.ASK:  # line 786
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 787
                if selection in "ao":  # line 788
                    add_all = "y" if selection == "a" else "n"  # line 788
                    selection = add_all  # line 788
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 789
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 789
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path)  # TODO document (A) as "selected not to add by user choice"  # line 790
        if changed.additions.items():  # line 791
            printo("Deletions:")  # line 791
        for path, pinfo in changed.additions.items():  # line 792
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 793
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 793
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 794
            if del_all is None and mrg == MergeOperation.ASK:  # line 795
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 796
                if selection in "ao":  # line 797
                    del_all = "y" if selection == "a" else "n"  # line 797
                    selection = del_all  # line 797
            if "y" in (del_all, selection):  # line 798
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 798
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path)  # not contained in other branch, but maybe kept  # line 799
        if changed.modifications.items():  # line 800
            printo("Modifications:")  # line 800
        for path, pinfo in changed.modifications.items():  # line 801
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 802
            binary = not m.isTextType(path)  # type: bool  # line 803
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 804
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 805
                printo(("MOD " if not binary else "BIN ") + path)  # TODO print mtime, size differences?  # line 806
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 807
            if op == "t":  # line 808
                printo("THR " + path)  # blockwise copy of contents  # line 809
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 809
            elif op == "m":  # line 810
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 811
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 811
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 812
                if current == file and verbose:  # line 813
                    info("No difference to versioned file")  # line 813
                elif file is not None:  # if None, error message was already logged  # line 814
                    merged = None  # type: bytes  # line 815
                    nl = None  # type: bytes  # line 815
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 816
                    if merged != current:  # line 817
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 818
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 818
                    elif verbose:  # TODO but update timestamp?  # line 819
                        info("No change")  # TODO but update timestamp?  # line 819
            else:  # mine or wrong input  # line 820
                printo("MNE " + path)  # nothing to do! same as skip  # line 821
    info(usage.MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 822
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 823
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 824
    m.saveBranches()  # line 825

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 827
    ''' Remove a branch entirely. '''  # line 828
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 829
    if len(m.branches) == 1:  # line 830
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 830
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 831
    if branch is None or branch not in m.branches:  # line 832
        Exit("Cannot delete unknown branch %r" % branch)  # line 832
    if verbose:  # line 833
        info(usage.MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 833
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 834
    info(usage.MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 835

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 837
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 838
    force = '--force' in options  # type: bool  # line 839
    m = Metadata()  # type: Metadata  # line 840
    if not (m.track or m.picky):  # line 841
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 841
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 842
    if pattern in patterns:  # line 843
        Exit("Pattern '%s' already tracked" % pattern)  # line 843
    if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 844
        Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 844
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 845
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 846
    patterns.append(pattern)  # line 847
    m.saveBranches()  # line 848
    info(usage.MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), os.path.abspath(relPath)))  # line 849

def remove(relPath: 'str', pattern: 'str', negative: 'bool'=False):  # line 851
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 852
    m = Metadata()  # type: Metadata  # line 853
    if not (m.track or m.picky):  # line 854
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 854
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 855
    if pattern not in patterns:  # line 856
        suggestion = _coconut.set()  # type: Set[str]  # line 857
        for pat in patterns:  # line 858
            if fnmatch.fnmatch(pattern, pat):  # line 858
                suggestion.add(pat)  # line 858
        if suggestion:  # TODO use same wording as in move  # line 859
            printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 859
        Exit("Tracked pattern '%s' not found" % pattern)  # line 860
    patterns.remove(pattern)  # line 861
    m.saveBranches()  # line 862
    info(usage.MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 863

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 865
    ''' List specified directory, augmenting with repository metadata. '''  # line 866
    m = Metadata()  # type: Metadata  # line 867
    folder = (os.getcwd() if folder is None else folder)  # line 868
    if '--all' in options:  # always start at SOS repo root with --all  # line 869
        folder = m.root  # always start at SOS repo root with --all  # line 869
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 870
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 871
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 872
    if verbose:  # line 873
        info(usage.MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 873
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 874
    if relPath.startswith(os.pardir):  # line 875
        Exit("Cannot list contents of folder outside offline repository")  # line 875
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 876
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 877
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 878
        if len(m.tags) > 0:  # line 879
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 879
        return  # line 880
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 881
        if not recursive:  # avoid recursion  # line 882
            dirnames.clear()  # avoid recursion  # line 882
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 883
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 884

        folder = decode(dirpath)  # line 886
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 887
        if patterns:  # line 888
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 889
            if out:  # line 890
                printo("DIR %s\n" % relPath + out)  # line 890
            continue  # with next folder  # line 891
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 892
        if len(files) > 0:  # line 893
            printo("DIR %s" % relPath)  # line 893
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 894
            ignore = None  # type: _coconut.typing.Optional[str]  # line 895
            for ig in m.c.ignores:  # remember first match  # line 896
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 896
                    ignore = ig  # remember first match  # line 896
                    break  # remember first match  # line 896
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 897
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 897
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 897
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 897
                        break  # found a white list entry for ignored file, undo ignoring it  # line 897
            matches = []  # type: List[str]  # line 898
            if not ignore:  # line 899
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 900
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 901
                        matches.append(os.path.basename(pattern))  # line 901
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 902
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 903

def log(options: '_coconut.typing.Sequence[str]'=[]):  # line 905
    ''' List previous commits on current branch. '''  # line 906
    changes_ = "--changes" in options  # type: bool  # line 907
    diff_ = "--diff" in options  # type: bool  # line 908
    number_ = tryOrDefault(lambda _=None: int(sys.argv[sys.argv.index("-n") + 1]), None)  # type: _coconut.typing.Optional[int]  # line 909
    m = Metadata()  # type: Metadata  # line 910
    m.loadBranch(m.branch)  # knows commit history  # line 911
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 912
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 913
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 914
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 915
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 916
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 917
    commit = None  # type: CommitInfo  # line 918
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 919
    for no in range(maxi + 1):  # line 920
        if no in m.commits:  # line 921
            commit = m.commits[no]  # line 921
        else:  # line 922
            if n.branch != n.getParentBranch(m.branch, no):  # line 923
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 923
            commit = n.commits[no]  # line 924
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 925
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 926
        if "--all" in options or no >= max(0, maxi + 1 - ((lambda _coconut_none_coalesce_item: m.c.logLines if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(number_))):  # line 927
            _add = news - olds  # type: FrozenSet[str]  # line 928
            _del = olds - news  # type: FrozenSet[str]  # line 929
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 931
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds})  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 933
            printo("  %s r%s @%s (+%02d/-%02d/%s%02d/T%02d) |%s|%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), len(_add), len(_del), PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", len(_mod), _txt, ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)), "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else ""))  # line 934
            if changes_:  # TODO moves detection?  # line 935
                (m.listChanges)(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}))  # TODO moves detection?  # line 935
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 936
                pass  #  _diff(m, changes)  # needs from revision diff  # line 936
        olds = news  # replaces olds for next revision compare  # line 937
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 938

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 940
    ''' Exported entire repository as archive for easy transfer. '''  # line 941
    if verbose:  # line 942
        info(usage.MARKER + "Dumping repository to archive...")  # line 942
    m = Metadata()  # type: Metadata  # to load the configuration  # line 943
    progress = '--progress' in options  # type: bool  # line 944
    delta = '--full' not in options  # type: bool  # line 945
    skipBackup = '--skip-backup' in options  # type: bool  # line 946
    import functools  # line 947
    import locale  # line 947
    import warnings  # line 947
    import zipfile  # line 947
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 948
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 948
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 948
    except:  # line 949
        compression = zipfile.ZIP_STORED  # line 949

    if argument is None:  # line 951
        Exit("Argument missing (target filename)")  # line 951
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 952
    entries = []  # type: List[str]  # line 953
    if os.path.exists(encode(argument)) and not skipBackup:  # line 954
        try:  # line 955
            if verbose:  # line 956
                info("Creating backup...")  # line 956
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 957
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 958
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 958
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 958
        except Exception as E:  # line 959
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 959
    if verbose:  # line 960
        info("Dumping revisions...")  # line 960
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 961
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 961
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 962
        _zip.debug = 0  # suppress debugging output  # line 963
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 964
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 965
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 966
        totalsize = 0  # type: int  # line 967
        start_time = time.time()  # type: float  # line 968
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 969
            dirpath = decode(dirpath)  # line 970
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 971
                continue  # don't backup backups  # line 971
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 972
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 973
            filenames[:] = sorted([decode(f) for f in filenames])  # line 974
            for filename in filenames:  # line 975
                abspath = os.path.join(dirpath, filename)  # type: str  # line 976
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 977
                totalsize += os.stat(encode(abspath)).st_size  # line 978
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 979
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 980
                    continue  # don't backup backups  # line 980
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 981
                    if show:  # line 982
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 982
                    _zip.write(abspath, relpath)  # write entry into archive  # line 983
        if delta:  # line 984
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 984
    info("\r" + pure.ljust(usage.MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 985

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 987
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 988
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 989
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 990
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 990
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 991
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 992
    if maxi is None:  # line 993
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 993
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 994
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 997
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 999
    while files:  # line 1000
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1001
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1002
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1004
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1004
    tracked = None  # type: bool  # line 1005
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1005
    tracked, commitArgs = vcsCommits[cmd]  # line 1005
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1006
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1008
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1008
    if tracked:  # line 1009
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1009

def config(arguments: 'List[str]', options: 'List[str]'=[]):  # line 1011
    command = None  # type: str  # line 1012
    key = None  # type: str  # line 1012
    value = None  # type: str  # line 1012
    v = None  # type: str  # line 1012
    command, key, value = (arguments + [None] * 2)[:3]  # line 1013
    if command is None:  # line 1014
        usage.usage("help", verbose=True)  # line 1014
    if command not in ["set", "unset", "show", "list", "add", "rm"]:  # line 1015
        Exit("Unknown config command")  # line 1015
    local = "--local" in options  # type: bool  # line 1016
    m = Metadata()  # type: Metadata  # loads layered configuration as well. TODO warning if repo not exists  # line 1017
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1018
    if command == "set":  # line 1019
        if None in (key, value):  # line 1020
            Exit("Key or value not specified")  # line 1020
        if key not in (([] if local else CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1021
            Exit("Unsupported key for %s configuration %r" % ("local " if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1021
        if key in CONFIGURABLE_FLAGS and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1022
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1022
        c[key] = value.lower() in TRUTH_VALUES if key in CONFIGURABLE_FLAGS else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1023
    elif command == "unset":  # line 1024
        if key is None:  # line 1025
            Exit("No key specified")  # line 1025
        if key not in c.keys():  # HINT: Works on local configurations when used with --local  # line 1026
            Exit("Unknown key")  # HINT: Works on local configurations when used with --local  # line 1026
        del c[key]  # line 1027
    elif command == "add":  # line 1028
        if None in (key, value):  # line 1029
            Exit("Key or value not specified")  # line 1029
        if key not in CONFIGURABLE_LISTS:  # line 1030
            Exit("Unsupported key %r" % key)  # line 1030
        if key not in c.keys():  # prepare empty list, or copy from global, add new value below  # line 1031
            c[key] = [_ for _ in c.__defaults[key]] if local else []  # prepare empty list, or copy from global, add new value below  # line 1031
        elif value in c[key]:  # line 1032
            Exit("Value already contained, nothing to do")  # line 1032
        if ";" in value:  # line 1033
            c[key].append(removePath(key, value))  # line 1033
        else:  # line 1034
            c[key].extend([removePath(key, v) for v in value.split(";")])  # line 1034
    elif command == "rm":  # line 1035
        if None in (key, value):  # line 1036
            Exit("Key or value not specified")  # line 1036
        if key not in c.keys():  # line 1037
            Exit("Unknown key %r" % key)  # line 1037
        if value not in c[key]:  # line 1038
            Exit("Unknown value %r" % value)  # line 1038
        c[key].remove(value)  # line 1039
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1040
            del c[key]  # remove local entry, to fallback to global  # line 1040
    else:  # Show or list  # line 1041
        if key == "ints":  # list valid configuration items  # line 1042
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1042
        elif key == "flags":  # line 1043
            printo(", ".join(CONFIGURABLE_FLAGS))  # line 1043
        elif key == "lists":  # line 1044
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1044
        elif key == "texts":  # line 1045
            printo(", ".join([_ for _ in defaults.keys() if _ not in (CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS)]))  # line 1045
        else:  # line 1046
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1047
            c = m.c  # always use full configuration chain  # line 1048
            try:  # attempt single key  # line 1049
                assert key is not None  # force exception  # line 1050
                c[key]  # force exception  # line 1050
                l = key in c.keys()  # type: bool  # line 1051
                g = key in c.__defaults.keys()  # type: bool  # line 1051
                printo("%s %s %r" % (key.rjust(20), out[3] if not (l or g) else (out[1] if l else out[2]), c[key]))  # line 1052
            except:  # normal value listing  # line 1053
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # line 1054
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1055
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1056
                for k, vt in sorted(vals.items()):  # line 1057
                    printo("%s %s %s" % (k.rjust(20), out[vt[1]], vt[0]))  # line 1057
                if len(c.keys()) == 0:  # line 1058
                    info("No local configuration stored")  # line 1058
                if len(c.__defaults.keys()) == 0:  # line 1059
                    info("No global configuration stored")  # line 1059
        return  # in case of list, no need to store anything  # line 1060
    if local:  # saves changes of repoConfig  # line 1061
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1061
        m.saveBranches()  # saves changes of repoConfig  # line 1061
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1061
    else:  # global config  # line 1062
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1063
        if f is None:  # line 1064
            error("Error saving user configuration: %r" % h)  # line 1064
        else:  # line 1065
            Exit("OK", code=0)  # line 1065

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1067
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1070
    if verbose:  # line 1071
        info(usage.MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1071
    force = '--force' in options  # type: bool  # line 1072
    soft = '--soft' in options  # type: bool  # line 1073
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1074
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1074
    m = Metadata()  # type: Metadata  # line 1075
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1076
    matching = fnmatch.filter(os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else [], os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1077
    matching[:] = [f for f in matching if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1078
    if not matching and not force:  # line 1079
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1079
    if not (m.track or m.picky):  # line 1080
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 1080
    if pattern not in patterns:  # list potential alternatives and exit  # line 1081
        for tracked in (t for t in patterns if os.path.dirname(t) == relPath):  # for all patterns of the same source folder  # line 1082
            alternative = fnmatch.filter(matching, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1083
            if alternative:  # line 1084
                info("  '%s' matches %d files" % (tracked, len(alternative)))  # line 1084
        if not (force or soft):  # line 1085
            Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # line 1085
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1086
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1087
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1088
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching files" % (basePattern, newBasePattern))  # line 1092
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1093
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1093
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1094
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1095
    if len({st[1] for st in matches}) != len(matches):  # line 1096
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1096
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1097
    if os.path.exists(encode(newRelPath)):  # line 1098
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1099
        if exists and not (force or soft):  # line 1100
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1100
    else:  # line 1101
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1101
    if not soft:  # perform actual renaming  # line 1102
        for (source, target) in matches:  # line 1103
            try:  # line 1104
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1104
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1105
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1105
    patterns[patterns.index(pattern)] = newPattern  # line 1106
    m.saveBranches()  # line 1107

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1109
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1110
    debug("Parsing command-line arguments...")  # line 1111
    root = os.getcwd()  # line 1112
    try:  # line 1113
        onlys, excps = parseOnlyOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1114
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1115
        arguments = [c.strip() for c in sys.argv[2:] if not (c.startswith("-") and (len(c) == 2 or c[1] == "-"))]  # type: List[_coconut.typing.Optional[str]]  # line 1116
        options = [c.strip() for c in sys.argv[2:] if c.startswith("-") and (len(c) == 2 or c[1] == "-")]  # options with arguments have to be parsed from sys.argv  # line 1117
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1118
        if command[:1] in "amr":  # line 1119
            relPath, pattern = relativize(root, os.path.join(cwd, arguments[0] if arguments else "."))  # line 1119
        if command[:1] == "m":  # line 1120
            if len(arguments) < 2:  # line 1121
                Exit("Need a second file pattern argument as target for move command")  # line 1121
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1122
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1123
        if command[:1] == "a":  # addnot  # line 1124
            add(relPath, pattern, options, negative="n" in command)  # addnot  # line 1124
        elif command[:1] == "b":  # line 1125
            branch(arguments[0], arguments[1], options)  # line 1125
        elif command[:3] == "com":  # line 1126
            commit(arguments[0], options, onlys, excps)  # line 1126
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1127
            changes(arguments[0], options, onlys, excps)  # "changes" (legacy)  # line 1127
        elif command[:2] == "ci":  # line 1128
            commit(arguments[0], options, onlys, excps)  # line 1128
        elif command[:3] == 'con':  # line 1129
            config(arguments, options)  # line 1129
        elif command[:2] == "de":  # line 1130
            destroy(arguments[0], options)  # line 1130
        elif command[:2] == "di":  # line 1131
            diff(arguments[0], options, onlys, excps)  # line 1131
        elif command[:2] == "du":  # line 1132
            dump(arguments[0], options)  # line 1132
        elif command[:1] == "h":  # line 1133
            usage.usage(arguments[0], verbose=verbose)  # line 1133
        elif command[:2] == "lo":  # line 1134
            log(options)  # line 1134
        elif command[:2] == "li":  # line 1135
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1135
        elif command[:2] == "ls":  # line 1136
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1136
        elif command[:1] == "m":  # mvnot  # line 1137
            move(relPath, pattern, newRelPath, newPattern, options, negative="n" in command)  # mvnot  # line 1137
        elif command[:2] == "of":  # line 1138
            offline(arguments[0], arguments[1], options)  # line 1138
        elif command[:2] == "on":  # line 1139
            online(options)  # line 1139
        elif command[:1] == "p":  # line 1140
            publish(arguments[0], cmd, options, onlys, excps)  # line 1140
        elif command[:1] == "r":  # rmnot  # line 1141
            remove(relPath, pattern, negative="n" in command)  # rmnot  # line 1141
        elif command[:2] == "st":  # line 1142
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1142
        elif command[:2] == "sw":  # line 1143
            switch(arguments[0], options, onlys, excps)  # line 1143
        elif command[:1] == "u":  # line 1144
            update(arguments[0], options, onlys, excps)  # line 1144
        elif command[:1] == "v":  # line 1145
            usage.usage(arguments[0], version=True)  # line 1145
        else:  # line 1146
            Exit("Unknown command '%s'" % command)  # line 1146
        Exit(code=0)  # regular exit  # line 1147
    except (Exception, RuntimeError) as E:  # line 1148
        exception(E)  # line 1149
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing")  # line 1150

def main():  # line 1152
    global debug, info, warn, error  # to modify logger  # line 1153
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1154
    _log = Logger(logging.getLogger(__name__))  # line 1155
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1155
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1156
        sys.argv.remove(option)  # clean up program arguments  # line 1156
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1157
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1157
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1158
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1159
    debug("Detected SOS root folder: %s\nDetected VCS root folder: %s" % (("-" if root is None else root), ("-" if vcs is None else vcs)))  # line 1160
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1161
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1162
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv"):  # in offline mode or just going offline TODO what about git config?  # line 1163
        cwd = os.getcwd()  # line 1164
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1165
        parse(vcs, cwd, cmd)  # line 1166
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1167
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1168
        import subprocess  # only required in this section  # line 1169
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1170
        inp = ""  # type: str  # line 1171
        while True:  # line 1172
            so, se = process.communicate(input=inp)  # line 1173
            if process.returncode is not None:  # line 1174
                break  # line 1174
            inp = sys.stdin.read()  # line 1175
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1176
            if root is None:  # line 1177
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1177
            m = Metadata(root)  # type: Metadata  # line 1178
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1179
            m.saveBranches()  # line 1180
    else:  # line 1181
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1181


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: bool  # this is a trick allowing to modify the flags from the test suite  # line 1185
force_vcs = [None] if '--vcs' in sys.argv else []  # type: bool  # line 1186
verbose = [None] if '--verbose' in sys.argv or '-v' in sys.argv else []  # type: bool  # imported from utility, and only modified here  # line 1187
debug_ = [None] if os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv else []  # type: bool  # line 1188
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1189

_log = Logger(logging.getLogger(__name__))  # line 1191
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1191

if __name__ == '__main__':  # line 1193
    main()  # line 1193
