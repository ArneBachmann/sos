#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x73c10f90

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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # TODO #243 this looks just wrong, but is currently required (check again, why)  # line 6
try:  # try needed as paths differ when installed via pip TODO #243 investigate further  # line 7
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

    def listChanges(_, changed: 'ChangeSet', commitTime: '_coconut.typing.Optional[float]'=None, root: '_coconut.typing.Optional[str]'=None):  # line 80
        ''' List changes. If commitTime (in ms) is defined, also check timestamps of modified files for plausibility (if mtime of new file is <= / older than in last commit, note so).
        commitTimne == None in switch and log
        root: current user's working dir to compute relative paths (cwd is usually repository root), otherwise None (repo-relative)
    '''  # line 84
        relp = lambda path, root: os.path.relpath(path, root).replace(SLASH, os.sep) if root else path  # type: _coconut.typing.Callable[[str, str], str]  # using relative paths if root is not None, otherwise SOS repo normalized paths  # line 85
        moves = dict(changed.moves.values())  # type: Dict[str, PathInfo]  # of origin-pathinfo  # line 86
        realadditions = {k: v for k, v in changed.additions.items() if k not in changed.moves}  # type: Dict[str, PathInfo]  # line 87
        realdeletions = {k: v for k, v in changed.deletions.items() if k not in moves}  # type: Dict[str, PathInfo]  # line 88
        if len(changed.moves) > 0:  # line 89
            printo(ajoin("MOV ", ["%s  <-  %s" % (relp(path, root), relp(dpath, root)) for path, (dpath, dinfo) in sorted(changed.moves.items())], "\n"), color=Fore.BLUE)  # line 89
        if len(realadditions) > 0:  # line 90
            printo(ajoin("ADD ", sorted([relp(p, root) for p in realadditions.keys()]), "\n"), color=Fore.GREEN)  # line 90
        if len(realdeletions) > 0:  # line 91
            printo(ajoin("DEL ", sorted([relp(p, root) for p in realdeletions.keys()]), "\n"), color=Fore.RED)  # line 91
        if len(changed.modifications) > 0:  # line 92
            printo(ajoin("MOD ", [relp(m, root) if commitTime is None else (relp(m, root) + (" <older than previously committed>" if pi.mtime < _.paths[m].mtime else "")) for (m, pi) in sorted(changed.modifications.items())], "\n"), color=Fore.YELLOW)  # line 92

    def loadBranches(_, offline: 'bool'=False):  # line 94
        ''' Load list of branches and current branch info from metadata file. offline = offline command avoids message. '''  # line 95
        try:  # fails if not yet created (on initial branch/commit)  # line 96
            branches = None  # type: List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)  # line 97
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 98
                repo, branches, config = json.load(fd)  # line 99
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 100
            _.branch = repo["branch"]  # current branch integer  # line 101
            _.track, _.picky, _.strict, _.compress, _.version, _.format = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format"]]  # line 102
            upgraded = []  # type: List[str]  # line 103
            if _.version is None:  # line 104
                _.version = "0 - pre-1.2"  # line 105
                upgraded.append("pre-1.2")  # line 106
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 107
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 108
                upgraded.append("2018.1210.3028")  # line 109
            if _.format is None:  # must be before 1.3.5+  # line 110
                _.format = METADATA_FORMAT  # marker for first metadata file format  # line 111
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 112
                upgraded.append("1.3.5")  # line 113
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 114
            _.repoConf = config  # line 115
            if upgraded:  # line 116
                for upgrade in upgraded:  # line 117
                    warn("!!! Upgraded repository metadata to match SOS version %r" % upgrade)  # line 117
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 118
                _.saveBranches()  # line 119
        except Exception as E:  # if not found, create metadata folder with default values  # line 120
            _.branches = {}  # line 121
            _.track, _.picky, _.strict, _.compress, _.version, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, METADATA_FORMAT]  # line 122
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # line 123

    def saveBranches(_, also: 'Dict[str, Any]'={}):  # line 125
        ''' Save list of branches and current branch info to metadata file. '''  # line 126
        tryOrIgnore(lambda: shutil.copy2(encode(os.path.join(_.root, metaFolder, metaFile)), encode(os.path.join(_.root, metaFolder, metaBack))))  # backup  # line 127
        with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 128
            store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT}  # type: Dict[str, Any]  # line 129
            store.update(also)  # allows overriding certain values at certain points in time  # line 133
            json.dump((store, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints, fd knows how to encode them  # line 134

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 136
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 137
        if name == "":  # line 138
            return -1  # line 138
        try:  # attempt to parse integer string  # line 139
            return int(name)  # attempt to parse integer string  # line 139
        except ValueError:  # line 140
            pass  # line 140
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 141
        return found[0] if found else None  # line 142

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 144
        ''' Convenience accessor for named branches. '''  # line 145
        if name == "":  # current  # line 146
            return _.branch  # current  # line 146
        try:  # attempt to parse integer string  # line 147
            return int(name)  # attempt to parse integer string  # line 147
        except ValueError:  # line 148
            pass  # line 148
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 149
        return found[0] if found else None  # line 150

    def loadBranch(_, branch: 'int'):  # line 152
        ''' Load all commit information from a branch meta data file. '''  # line 153
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 154
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 155
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 156
        _.branch = branch  # line 157

    def saveBranch(_, branch: 'int'):  # line 159
        ''' Save all commits to a branch meta data file. '''  # line 160
        tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile)), encode(branchFolder(branch, metaBack))))  # backup  # line 161
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "w", encoding=UTF8) as fd:  # line 162
            json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 163

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 165
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 173
        if verbose:  # line 174
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 174
        now = int(time.time() * 1000)  # type: int  # line 175
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 176
        revision = max(_.commits) if _.commits else 0  # type: int  # line 177
        _.commits.clear()  # line 178
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 179
        os.makedirs(encode(revisionFolder(branch, 0, base=_.root) if full else branchFolder(branch, base=_.root)))  # line 184
        if full:  # not fast branching via reference - copy all current files to new branch  # line 185
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 186
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 187
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 187
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit TODO #244 also contain message from latest revision of originating branch  # line 188
            _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 189
        _.saveBranch(branch)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 190
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 191

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 193
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 199
        now = int(time.time() * 1000)  # type: int  # line 200
        simpleMode = not (_.track or _.picky)  # line 201
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 202
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 203
        if verbose:  # line 204
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 204
        _.paths = {}  # type: Dict[str, PathInfo]  # line 205
        if simpleMode:  # branches from file system state  # line 206
            changed, msg = _.findChanges(branch, 0, progress=simpleMode)  # creates revision folder and versioned files  # line 207
            _.listChanges(changed)  # line 208
            if msg:  # display compression factor and time taken  # line 209
                printo(msg)  # display compression factor and time taken  # line 209
            _.paths.update(changed.additions.items())  # line 210
        else:  # tracking or picky mode: branch from latest revision  # line 211
            os.makedirs(encode(revisionFolder(branch, 0, base=_.root)))  # line 212
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 213
                _.loadBranch(_.branch)  # line 214
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO #245 what if last switch was to an earlier revision? no persisting of last checkout  # line 215
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 216
                for path, pinfo in _.paths.items():  # line 217
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 217
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 218
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 219
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 220
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 221

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 223
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 226
        import collections  # used almost only here  # line 227
        binfo = None  # type: BranchInfo  # typing info  # line 228
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 229
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 230
        if deps:  # need to copy all parent revisions to dependent branches first  # line 231
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 232
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 233
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 234
                for dep, _rev in deps:  # line 235
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO #246 align placement of indicator with other uses of progress  # line 236
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 237
#          if rev in _.commits:  # TODO #247 uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 239
                    shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 240
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 241
                for rev in range(minrev + 1, _rev + 1):  # line 242
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 243
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 244
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 245
                        newcommits[dep][rev] = _.commits[rev]  # line 246
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 247
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 248
        printo(pure.ljust() + "\r")  # clean line output  # line 249
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 250
        tryOrIgnore(lambda: os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?"))  # line 251
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 252
        del _.branches[branch]  # line 253
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 254
        _.saveBranches()  # persist modified branches list  # line 255
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 256
            _.commits = commits  # line 257
            _.saveBranch(branch)  # line 258
        _.commits.clear()  # clean memory  # line 259
        return binfo  # line 260

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 262
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 263
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 264
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 265
            _.paths = json.load(fd)  # line 265
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 266
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 267

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 269
        ''' Save all file information to a commit meta data file. '''  # line 270
        target = revisionFolder(branch, revision, base=_.root)  # type: str  # line 271
        tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 272
        tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 273
        with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 274
            json.dump(_.paths, fd, ensure_ascii=False)  # line 274

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 276
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 285
        import collections  # used only in this method  # line 286
        write = branch is not None and revision is not None  # line 287
        if write:  # line 288
            tryOrIgnore(lambda: os.makedirs(encode(revisionFolder(branch, revision, base=_.root))))  # line 288
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # WARN this code needs explicity argument passing for initialization due to mypy problems with default arguments  # line 289
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 290
        hashed = None  # type: _coconut.typing.Optional[str]  # line 291
        written = None  # type: int  # line 291
        compressed = 0  # type: int  # line 291
        original = 0  # type: int  # line 291
        start_time = time.time()  # type: float  # line 291
        knownPaths = {}  # type: Dict[str, List[str]]  # line 292

# Find relevant folders/files that match specified folder/glob patterns for exclusive inclusion or exclusion
        byFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 295
        onlyByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 296
        dontByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 297
        for path, pinfo in _.paths.items():  # line 298
            if pinfo is None:  # quicker than generator expression above  # line 299
                continue  # quicker than generator expression above  # line 299
            slash = path.rindex(SLASH)  # type: int  # line 300
            byFolder[path[:slash]].append(path[slash + 1:])  # line 301
        for pattern in ([] if considerOnly is None else considerOnly):  # line 302
            slash = pattern.rindex(SLASH)  # line 302
            onlyByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 302
        for pattern in ([] if dontConsider is None else dontConsider):  # line 303
            slash = pattern.rindex(SLASH)  # line 303
            dontByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 303
        for folder, paths in byFolder.items():  # line 304
            pos = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in onlyByFolder.get(folder, [])]) if considerOnly is not None else set(paths)  # type: Set[str]  # line 305
            neg = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in dontByFolder.get(folder, [])]) if dontConsider is not None else set()  # type: Set[str]  # line 306
            knownPaths[folder] = list(pos - neg)  # line 307

        for path, dirnames, filenames in os.walk(_.root):  # line 309
            path = decode(path)  # line 310
            dirnames[:] = [decode(d) for d in dirnames]  # line 311
            filenames[:] = [decode(f) for f in filenames]  # line 312
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 313
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 314
            dirnames.sort()  # line 315
            filenames.sort()  # line 315
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 316
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 317
            if dontConsider:  # line 318
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 319
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 320
                filename = relPath + SLASH + file  # line 321
                filepath = os.path.join(path, file)  # line 322
                try:  # line 323
                    stat = os.stat(encode(filepath))  # line 323
                except Exception as E:  # line 324
                    exception(E)  # line 324
                    continue  # line 324
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 325
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 326
                if show:  # indication character returned  # line 327
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 328
                    printo(pure.ljust(outstring), nl="")  # line 329
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 330
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 331
                    nameHash = hashStr(filename)  # line 332
                    try:  # line 333
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=nameHash) if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 334
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 335
                        compressed += written  # line 336
                        original += size  # line 336
                    except PermissionError as E:  # line 337
                        error("File permission error for %s" % filepath)  # line 337
                    except Exception as F:  # HINT e.g. FileNotFoundError will not add to additions  # line 338
                        exception(F)  # HINT e.g. FileNotFoundError will not add to additions  # line 338
                    continue  # with next file  # line 339
                last = _.paths[filename]  # filename is known - check for modifications  # line 340
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 341
                    try:  # line 342
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=last.nameHash) if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 343
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 344
                        continue  # line 344
                    except Exception as E:  # line 345
                        exception(E)  # line 345
                elif size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False)):  # detected a modification  # line 346
                    try:  # line 347
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=revisionFolder(branch, revision, base=_.root, file=last.nameHash) if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 348
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 349
                    except Exception as E:  # line 350
                        exception(E)  # line 350
                else:  # with next file  # line 351
                    continue  # with next file  # line 351
                compressed += written  # line 352
                original += last.size if inverse else size  # line 352
            if relPath in knownPaths:  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 353
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 353
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 354
            for file in names:  # line 355
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 356
                    continue  # don't mark ignored files as deleted  # line 356
                pth = path + SLASH + file  # type: str  # line 357
                changed.deletions[pth] = _.paths[pth]  # line 358
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, _.strict))  # line 359
        if progress:  # forces clean line of progress output  # line 360
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 360
        elif verbose:  # line 361
            info("Finished detecting changes")  # line 361
        tt = time.time() - start_time  # type: float  # line 362
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # line 362
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 363
        msg = (msg + " | " if msg else "") + ("Transfer speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 364
        return (changed, msg if msg else None)  # line 365

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 367
        ''' Returns nothing, just updates _.paths in place. '''  # line 368
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 369

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 371
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 372
        try:  # load initial paths  # line 373
            _.loadCommit(branch, startwith)  # load initial paths  # line 373
        except:  # no revisions  # line 374
            yield {}  # no revisions  # line 374
            return None  # no revisions  # line 374
        if incrementally:  # line 375
            yield _.paths  # line 375
        m = Metadata(_.root)  # type: Metadata  # next changes TODO #250 avoid loading all metadata and config  # line 376
        rev = None  # type: int  # next changes TODO #250 avoid loading all metadata and config  # line 376
        for rev in range(startwith + 1, revision + 1):  # line 377
            m.loadCommit(branch, rev)  # line 378
            for p, info in m.paths.items():  # line 379
                if info.size == None:  # line 380
                    del _.paths[p]  # line 380
                else:  # line 381
                    _.paths[p] = info  # line 381
            if incrementally:  # line 382
                yield _.paths  # line 382
        yield None  # for the default case - not incrementally  # line 383

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 385
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 386
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 387

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 389
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 392
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 393
            return (_.branch, -1)  # no branch/revision specified  # line 393
        argument = argument.strip()  # line 394
        if argument.startswith(SLASH):  # current branch  # line 395
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 395
        if argument.endswith(SLASH):  # line 396
            try:  # line 397
                return (_.getBranchByName(argument[:-1]), -1)  # line 397
            except ValueError:  # line 398
                Exit("Unknown branch label '%s'" % argument)  # line 398
        if SLASH in argument:  # line 399
            b, r = argument.split(SLASH)[:2]  # line 400
            try:  # line 401
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 401
            except ValueError:  # line 402
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 402
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 403
        if branch not in _.branches:  # line 404
            branch = None  # line 404
        try:  # either branch name/number or reverse/absolute revision number  # line 405
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 405
        except:  # line 406
            Exit("Unknown branch label or wrong number format")  # line 406
        Exit("This should never happen. Please create a issue report")  # line 407
        return (None, None)  # line 407

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 409
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 411
        while True:  # line 412
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 413
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 414
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 415
                break  # line 415
            revision -= 1  # line 416
            if revision < 0:  # line 417
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 417
        return revision, source  # line 418

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 420
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 421
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 422
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 423
            return [branch]  # found. need to load commit from other branch instead  # line 423
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 424
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 424
        return others  # line 425

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 427
        return _.getParentBranches(branch, revision)[-1]  # line 427

    @_coconut_tco  # line 429
    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 429
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 430
        m = Metadata()  # type: Metadata  # line 431
        other = branch  # type: _coconut.typing.Optional[int]  # line 432
        while other is not None:  # line 433
            m.loadBranch(other)  # line 434
            if m.commits:  # line 435
                return _coconut_tail_call(max, m.commits)  # line 435
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 436
        return None  # line 437

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 439
        ''' Copy versioned file to other branch/revision. '''  # line 440
        target = revisionFolder(toBranch, toRevision, base=_.root, file=pinfo.nameHash)  # type: str  # line 441
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 442
        shutil.copy2(encode(source), encode(target))  # line 443

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 445
        ''' Return file contents, or copy contents into file path provided. '''  # line 446
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 447
        try:  # line 448
            with openIt(source, "r", _.compress) as fd:  # line 448
                if toFile is None:  # read bytes into memory and return  # line 449
                    return fd.read()  # read bytes into memory and return  # line 449
                with open(encode(toFile), "wb") as to:  # line 450
                    while True:  # line 451
                        buffer = fd.read(bufSize)  # line 452
                        to.write(buffer)  # line 453
                        if len(buffer) < bufSize:  # line 454
                            break  # line 454
                    return None  # line 455
        except Exception as E:  # line 456
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 456
        None  # line 457

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 459
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 460
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 461
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 461
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 462
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 463
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 464
        if pinfo.size == 0:  # line 465
            with open(encode(target), "wb"):  # line 466
                pass  # line 466
            try:  # update access/modification timestamps on file system  # line 467
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 467
            except Exception as E:  # line 468
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 468
            return None  # line 469
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 470
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 472
            while True:  # line 473
                buffer = fd.read(bufSize)  # line 474
                to.write(buffer)  # line 475
                if len(buffer) < bufSize:  # line 476
                    break  # line 476
        try:  # update access/modification timestamps on file system  # line 477
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 477
        except Exception as E:  # line 478
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 478
        return None  # line 479


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 483
    ''' Initial command to start working offline. '''  # line 484
    if os.path.exists(encode(metaFolder)):  # line 485
        if '--force' not in options:  # line 486
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 486
        try:  # throw away all previous metadata before going offline  # line 487
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 488
                resource = metaFolder + os.sep + entry  # line 489
                if os.path.isdir(resource):  # line 490
                    shutil.rmtree(encode(resource))  # line 490
                else:  # line 491
                    os.unlink(encode(resource))  # line 491
        except:  # line 492
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder)  # line 492
    m = Metadata(offline=True)  # type: Metadata  # line 493
    if '--strict' in options or m.c.strict:  # always hash contents  # line 494
        m.strict = True  # always hash contents  # line 494
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 495
        m.compress = True  # plain file copies instead of compressed ones  # line 495
    if '--picky' in options or m.c.picky:  # Git-like  # line 496
        m.picky = True  # Git-like  # line 496
    elif '--track' in options or m.c.track:  # Svn-like  # line 497
        m.track = True  # Svn-like  # line 497
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 498
    if title:  # line 499
        printo(title)  # line 499
    if verbose:  # line 500
        info(usage.MARKER + "Going offline...")  # line 500
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 501
    m.branch = 0  # line 502
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 503
    if verbose or '--verbose' in options:  # line 504
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 504
    info(usage.MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 505

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 507
    ''' Finish working offline. '''  # line 508
    if verbose:  # line 509
        info(usage.MARKER + "Going back online...")  # line 509
    force = '--force' in options  # type: bool  # line 510
    m = Metadata()  # type: Metadata  # line 511
    strict = '--strict' in options or m.strict  # type: bool  # line 512
    m.loadBranches()  # line 513
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 514
        Exit("There are still unsynchronized (modified) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 514
    m.loadBranch(m.branch)  # line 515
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 516
    if options.count("--force") < 2:  # line 517
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 518
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 519
        if modified(changed):  # line 520
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 524
    try:  # line 525
        shutil.rmtree(encode(metaFolder))  # line 525
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 525
    except Exception as E:  # line 526
        Exit("Error removing offline repository: %r" % E)  # line 526
    info(usage.MARKER + "Offline repository removed, you're back online")  # line 527

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 529
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not necessary, as either branching from last  revision anyway, or branching file tree anyway.
  '''  # line 532
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 533
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 534
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 535
    m = Metadata()  # type: Metadata  # line 536
    m.loadBranch(m.branch)  # line 537
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 538
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 539
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 539
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 540
    if verbose:  # line 541
        info(usage.MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 541
    if last:  # branch from last revision  # line 542
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 542
    else:  # branch from current file tree state  # line 543
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 543
    if not stay:  # line 544
        m.branch = branch  # line 544
    m.saveBranches()  # TODO #253 or indent again?  # line 545
    info(usage.MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 546

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 548
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 549
    m = Metadata()  # type: Metadata  # line 550
    branch = None  # type: _coconut.typing.Optional[int]  # line 550
    revision = None  # type: _coconut.typing.Optional[int]  # line 550
    strict = '--strict' in options or m.strict  # type: bool  # line 551
    branch, revision = m.parseRevisionString(argument)  # line 552
    if branch not in m.branches:  # line 553
        Exit("Unknown branch")  # line 553
    m.loadBranch(branch)  # knows commits  # line 554
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 555
    if verbose:  # line 556
        info(usage.MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 556
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 557
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 558
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 563
    return changed  # returning for unit tests only TODO #254 remove?  # line 564

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False):  # TODO #255 introduce option to diff against committed revision  # line 566
    ''' The diff display code. '''  # line 567
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 568
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 569
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 570
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 571
        content = b""  # type: _coconut.typing.Optional[bytes]  # line 572
        if pinfo.size != 0:  # versioned file  # line 573
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 573
            assert content is not None  # versioned file  # line 573
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current file  # line 574
        blocks = None  # type: List[MergeBlock]  # line 575
        nl = None  # type: bytes  # line 575
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 576
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 577
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 578
        for block in blocks:  # line 579
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # TODO #256 show color via (n)curses or other library?  # line 582
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 583
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 583
            elif block.tipe == MergeBlockType.REMOVE:  # line 584
                for no, line in enumerate(block.lines):  # line 585
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 585
            elif block.tipe == MergeBlockType.REPLACE:  # line 586
                for no, line in enumerate(block.replaces.lines):  # line 587
                    printo(wrap("-~- %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 587
                for no, line in enumerate(block.lines):  # line 588
                    printo(wrap("+~+ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 588
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 591
                printo()  # line 591

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 593
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 594
    m = Metadata()  # type: Metadata  # line 595
    branch = None  # type: _coconut.typing.Optional[int]  # line 595
    revision = None  # type: _coconut.typing.Optional[int]  # line 595
    strict = '--strict' in options or m.strict  # type: bool  # line 596
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 597
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 598
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 599
    if branch not in m.branches:  # line 600
        Exit("Unknown branch")  # line 600
    m.loadBranch(branch)  # knows commits  # line 601
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 602
    if verbose:  # line 603
        info(usage.MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 603
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 604
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 605
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap)  # line 610

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 612
    ''' Create new revision from file tree changes vs. last commit. '''  # line 613
    m = Metadata()  # type: Metadata  # line 614
    if argument is not None and argument in m.tags:  # line 615
        Exit("Illegal commit message. It was already used as a tag name")  # line 615
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 616
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 618
        Exit("No file patterns staged for commit in picky mode")  # line 618
    if verbose:  # line 619
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 619
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 620
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 621
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 622
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 623
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 624
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 625
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 626
    m.saveBranch(m.branch)  # line 627
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 628
    if m.picky:  # remove tracked patterns  # line 629
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 629
    else:  # track or simple mode: set branch modified  # line 630
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 630
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 631
        m.tags.append(argument)  # memorize unique tag  # line 631
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 631
    m.saveBranches()  # line 632
    stored = 0  # type: int  # now determine new commit size on file system  # line 633
    overhead = 0  # type: int  # now determine new commit size on file system  # line 633
    count = 0  # type: int  # now determine new commit size on file system  # line 633
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 634
    for file in os.listdir(commitFolder):  # line 635
        try:  # line 636
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 637
            if file == metaFile:  # line 638
                overhead += newsize  # line 638
            else:  # line 639
                stored += newsize  # line 639
                count += 1  # line 639
        except Exception as E:  # line 640
            error(E)  # line 640
    printo(usage.MARKER + "Created new revision r%02d%s (+%02d/-%02d/%s%02d/%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, ((" '%s'" % argument) if argument is not None else ""), len(changed.additions) - len(changed.moves), len(changed.deletions) - len(changed.moves), PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", len(changed.modifications), MOVE_SYMBOL if m.c.useUnicodeFont else "#", len(changed.moves), ("%.2f MiB" % ((stored + overhead) / MEBI)) if stored > 1.25 * MEBI else (("%.2f Kib" % ((stored + overhead) / KIBI)) if stored > 1.25 * KIBI else ("%d bytes" % (stored + overhead))), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 641

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 643
    ''' Show branches and current repository state. '''  # line 644
    m = Metadata()  # type: Metadata  # line 645
    if not (m.c.useChangesCommand or '--repo' in options):  # line 646
        changes(argument, options, onlys, excps)  # line 646
        return  # line 646
    current = m.branch  # type: int  # line 647
    strict = '--strict' in options or m.strict  # type: bool  # line 648
    info(usage.MARKER + "Offline repository status")  # line 649
    info("Repository root:     %s" % os.getcwd())  # line 650
    info("Underlying VCS root: %s" % vcs)  # line 651
    info("Underlying VCS type: %s" % cmd)  # line 652
    info("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 653
    info("Current SOS version: %s" % version.__version__)  # line 654
    info("At creation version: %s" % m.version)  # line 655
    info("Metadata format:     %s" % m.format)  # line 656
    info("Content checking:    %sactivated%s" % (Fore.CYAN if m.strict else Fore.BLUE + "de", Fore.RESET))  # line 657
    info("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 658
    info("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 659
    info("Number of branches:  %d" % len(m.branches))  # line 660
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 661
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 662
    m.loadBranch(current)  # line 663
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 664
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 665
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 665
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 666
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of symbols for changed vs. unchanged  # line 671
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 675
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 676
        payload = 0  # type: int  # count used storage per branch  # line 677
        overhead = 0  # type: int  # count used storage per branch  # line 677
        original = 0  # type: int  # count used storage per branch  # line 677
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 678
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 679
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 680
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 680
                else:  # line 681
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 681
        pl_amount = float(payload) / MEBI  # type: float  # line 682
        oh_amount = float(overhead) / MEBI  # type: float  # line 682
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 684
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 685
            m.loadCommit(m.branch, commit_)  # line 686
            for pinfo in m.paths.values():  # line 687
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 687
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 688
        printo("  %s b%d%s @%s (%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 689
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 690
        info("\nTracked file patterns:")  # TODO #261 print matching untracking patterns side-by-side  # line 691
        printo(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 692
        info("\nUntracked file patterns:")  # line 693
        printo(ajoin("  | ", m.branches[m.branch].untracked, "\n"))  # line 694

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 696
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 703
    assert not (check and commit)  # line 704
    m = Metadata()  # type: Metadata  # line 705
    force = '--force' in options  # type: bool  # line 706
    strict = '--strict' in options or m.strict  # type: bool  # line 707
    if argument is not None:  # line 708
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 709
        if branch is None:  # line 710
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 710
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 711
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 712

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 715
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 716
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 717
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 718
    if check and modified(changed) and not force:  # line 723
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 724
        Exit("File tree contains changes. Use --force to proceed")  # line 725
    elif commit:  # line 726
        if not modified(changed) and not force:  # line 727
            Exit("Nothing to commit")  # line 727
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 728
        if msg:  # line 729
            printo(msg)  # line 729

    if argument is not None:  # branch/revision specified  # line 731
        m.loadBranch(branch)  # knows commits of target branch  # line 732
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 733
        revision = m.correctNegativeIndexing(revision)  # line 734
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 735
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 736

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 738
    ''' Continue work on another branch, replacing file tree changes. '''  # line 739
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 740
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 741

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 744
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 745
    else:  # full file switch  # line 746
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 747
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 748

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 755
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 756
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 757
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 758
                rms.append(a)  # line 758
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 759
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 759
        if modified(changed) and not force:  # line 760
            m.listChanges(changed, cwd)  # line 760
            Exit("File tree contains changes. Use --force to proceed")  # line 760
        if verbose:  # line 761
            info(usage.MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 761
        if not modified(todos):  # line 762
            info("No changes to current file tree")  # line 763
        else:  # integration required  # line 764
            for path, pinfo in todos.deletions.items():  # line 765
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 766
                printo("ADD " + path)  # line 767
            for path, pinfo in todos.additions.items():  # line 768
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 769
                printo("DEL " + path)  # line 770
            for path, pinfo in todos.modifications.items():  # line 771
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 772
                printo("MOD " + path)  # line 773
    m.branch = branch  # line 774
    m.saveBranches()  # store switched path info  # line 775
    info(usage.MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 776

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 778
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 782
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 783
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 784
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 785
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 786
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 787
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 788
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 789
    if verbose:  # line 790
        info(usage.MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 790

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 793
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 794
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 795
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 796
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 801
        if trackingUnion != trackingPatterns:  # nothing added  # line 802
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 803
        else:  # line 804
            info("Nothing to update")  # but write back updated branch info below  # line 805
    else:  # integration required  # line 806
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 807
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 807
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 807
        if changed.deletions.items():  # line 808
            printo("Additions:")  # line 808
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 809
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 810
            if add_all is None and mrg == MergeOperation.ASK:  # line 811
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 812
                if selection in "ao":  # line 813
                    add_all = "y" if selection == "a" else "n"  # line 813
                    selection = add_all  # line 813
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 814
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 814
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path)  # TODO document (A) as "selected not to add by user choice"  # line 815
        if changed.additions.items():  # line 816
            printo("Deletions:")  # line 816
        for path, pinfo in changed.additions.items():  # line 817
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 818
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 818
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 819
            if del_all is None and mrg == MergeOperation.ASK:  # line 820
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 821
                if selection in "ao":  # line 822
                    del_all = "y" if selection == "a" else "n"  # line 822
                    selection = del_all  # line 822
            if "y" in (del_all, selection):  # line 823
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 823
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path)  # not contained in other branch, but maybe kept  # line 824
        if changed.modifications.items():  # line 825
            printo("Modifications:")  # line 825
        for path, pinfo in changed.modifications.items():  # line 826
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 827
            binary = not m.isTextType(path)  # type: bool  # line 828
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 829
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 830
                printo(("MOD " if not binary else "BIN ") + path)  # TODO print mtime, size differences?  # line 831
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 832
            if op == "t":  # line 833
                printo("THR " + path)  # blockwise copy of contents  # line 834
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 834
            elif op == "m":  # line 835
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 836
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 836
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 837
                if current == file and verbose:  # line 838
                    info("No difference to versioned file")  # line 838
                elif file is not None:  # if None, error message was already logged  # line 839
                    merged = None  # type: bytes  # line 840
                    nl = None  # type: bytes  # line 840
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 841
                    if merged != current:  # line 842
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 843
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 843
                    elif verbose:  # TODO but update timestamp?  # line 844
                        info("No change")  # TODO but update timestamp?  # line 844
            else:  # mine or wrong input  # line 845
                printo("MNE " + path)  # nothing to do! same as skip  # line 846
    info(usage.MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 847
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 848
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 849
    m.saveBranches()  # line 850

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 852
    ''' Remove a branch entirely. '''  # line 853
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 854
    if len(m.branches) == 1:  # line 855
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 855
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 856
    if branch is None or branch not in m.branches:  # line 857
        Exit("Cannot delete unknown branch %r" % branch)  # line 857
    if verbose:  # line 858
        info(usage.MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 858
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 859
    info(usage.MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 860

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 862
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 863
    force = '--force' in options  # type: bool  # line 864
    m = Metadata()  # type: Metadata  # line 865
    if not (m.track or m.picky):  # line 866
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 866
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 867
    if pattern in patterns:  # line 868
        Exit("Pattern '%s' already tracked" % pattern)  # line 868
    if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 869
        Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 869
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 870
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 871
    patterns.append(pattern)  # line 872
    m.saveBranches()  # line 873
    info(usage.MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # TODO #262 display relative path by default?  # line 874

def remove(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 876
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 877
    m = Metadata()  # type: Metadata  # line 878
    if not (m.track or m.picky):  # line 879
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 879
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 880
    if pattern not in patterns:  # line 881
        suggestion = _coconut.set()  # type: Set[str]  # line 882
        for pat in patterns:  # line 883
            if fnmatch.fnmatch(pattern, pat):  # line 883
                suggestion.add(pat)  # line 883
        if suggestion:  # TODO use same wording as in move  # line 884
            printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 884
        Exit("Tracked pattern '%s' not found" % pattern)  # line 885
    patterns.remove(pattern)  # line 886
    m.saveBranches()  # line 887
    info(usage.MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 888

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 890
    ''' List specified directory, augmenting with repository metadata. '''  # line 891
    m = Metadata()  # type: Metadata  # line 892
    folder = (os.getcwd() if folder is None else folder)  # line 893
    if '--all' in options:  # always start at SOS repo root with --all  # line 894
        folder = m.root  # always start at SOS repo root with --all  # line 894
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 895
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 896
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 897
    if verbose:  # line 898
        info(usage.MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 898
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 899
    if relPath.startswith(os.pardir):  # line 900
        Exit("Cannot list contents of folder outside offline repository")  # line 900
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 901
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 902
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 903
        if len(m.tags) > 0:  # line 904
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 904
        return  # line 905
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 906
        if not recursive:  # avoid recursion  # line 907
            dirnames.clear()  # avoid recursion  # line 907
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 908
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 909

        folder = decode(dirpath)  # line 911
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 912
        if patterns:  # line 913
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 914
            if out:  # line 915
                printo("DIR %s\n" % relPath + out)  # line 915
            continue  # with next folder  # line 916
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 917
        if len(files) > 0:  # line 918
            printo("DIR %s" % relPath)  # line 918
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 919
            ignore = None  # type: _coconut.typing.Optional[str]  # line 920
            for ig in m.c.ignores:  # remember first match  # line 921
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 921
                    ignore = ig  # remember first match  # line 921
                    break  # remember first match  # line 921
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 922
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 922
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 922
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 922
                        break  # found a white list entry for ignored file, undo ignoring it  # line 922
            matches = []  # type: List[str]  # line 923
            if not ignore:  # line 924
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 925
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 926
                        matches.append(os.path.basename(pattern))  # line 926
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 927
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 928

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 930
    ''' List previous commits on current branch. '''  # line 931
    changes_ = "--changes" in options  # type: bool  # line 932
    diff_ = "--diff" in options  # type: bool  # line 933
    m = Metadata()  # type: Metadata  # line 934
    m.loadBranch(m.branch)  # knows commit history  # line 935
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # line 936
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 937
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 938
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 939
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 940
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 941
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 942
    commit = None  # type: CommitInfo  # line 943
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 944
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 945
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 946
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 947
    for no in range(maxi + 1):  # line 948
        if indicator:  # line 949
            printo("  %%s %%0%dd" % digits % (indicator.getIndicator(), no), nl="\r")  # line 949
        if no in m.commits:  # line 950
            commit = m.commits[no]  # line 950
        else:  # line 951
            if n.branch != n.getParentBranch(m.branch, no):  # line 952
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 952
            commit = n.commits[no]  # line 953
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 954
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 955
        if "--all" in options or no >= lastno:  # line 956
            if no >= lastno:  # line 957
                indicator = None  # line 957
            _add = news - olds  # type: FrozenSet[str]  # line 958
            _del = olds - news  # type: FrozenSet[str]  # line 959
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 961
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 963
            printo("  %s r%s @%s (%s+%02d%s/%s-%02d%s/%s%s%02d%s/%sT%02d%s) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, len(_add), Fore.RESET, Fore.RED, len(_del), Fore.RESET, Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", len(_mod), Fore.RESET, Fore.BLUE, _txt, Fore.RESET, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 964
            if changes_:  # line 965
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}), root=cwd if '--relative' in options else None)  # TODO moves detection?  # line 976
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 977
                pass  #  _diff(m, changes)  # needs from revision diff  # line 977
        olds = news  # replaces olds for next revision compare  # line 978
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 979

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 981
    ''' Exported entire repository as archive for easy transfer. '''  # line 982
    if verbose:  # line 983
        info(usage.MARKER + "Dumping repository to archive...")  # line 983
    m = Metadata()  # type: Metadata  # to load the configuration  # line 984
    progress = '--progress' in options  # type: bool  # line 985
    delta = '--full' not in options  # type: bool  # line 986
    skipBackup = '--skip-backup' in options  # type: bool  # line 987
    import functools  # line 988
    import locale  # line 988
    import warnings  # line 988
    import zipfile  # line 988
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 989
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 989
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 989
    except:  # line 990
        compression = zipfile.ZIP_STORED  # line 990

    if argument is None:  # line 992
        Exit("Argument missing (target filename)")  # line 992
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 993
    entries = []  # type: List[str]  # line 994
    if os.path.exists(encode(argument)) and not skipBackup:  # line 995
        try:  # line 996
            if verbose:  # line 997
                info("Creating backup...")  # line 997
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 998
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 999
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 999
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 999
        except Exception as E:  # line 1000
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 1000
    if verbose:  # line 1001
        info("Dumping revisions...")  # line 1001
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1002
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1002
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1003
        _zip.debug = 0  # suppress debugging output  # line 1004
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1005
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1006
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1007
        totalsize = 0  # type: int  # line 1008
        start_time = time.time()  # type: float  # line 1009
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1010
            dirpath = decode(dirpath)  # line 1011
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1012
                continue  # don't backup backups  # line 1012
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1013
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1014
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1015
            for filename in filenames:  # line 1016
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1017
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1018
                totalsize += os.stat(encode(abspath)).st_size  # line 1019
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1020
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1021
                    continue  # don't backup backups  # line 1021
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1022
                    if show:  # line 1023
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1023
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1024
        if delta:  # line 1025
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1025
    info("\r" + pure.ljust(usage.MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1026

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1028
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1029
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1030
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1031
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1031
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1032
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1033
    if maxi is None:  # line 1034
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1034
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1035
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1038
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1040
    while files:  # line 1041
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1042
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1043
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1045
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1045
    tracked = None  # type: bool  # line 1046
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1046
    tracked, commitArgs = vcsCommits[cmd]  # line 1046
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1047
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1049
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1049
    if tracked:  # line 1050
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1050

def config(arguments: 'List[str]', options: 'List[str]'=[]):  # line 1052
    command = None  # type: str  # line 1053
    key = None  # type: str  # line 1053
    value = None  # type: str  # line 1053
    v = None  # type: str  # line 1053
    command, key, value = (arguments + [None] * 2)[:3]  # line 1054
    if command is None:  # line 1055
        usage.usage("help", verbose=True)  # line 1055
    if command not in ["set", "unset", "show", "list", "add", "rm"]:  # line 1056
        Exit("Unknown config command")  # line 1056
    local = "--local" in options  # type: bool  # line 1057
    m = Metadata()  # type: Metadata  # loads layered configuration as well. TODO warning if repo not exists  # line 1058
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1059
    if command == "set":  # line 1060
        if None in (key, value):  # line 1061
            Exit("Key or value not specified")  # line 1061
        if key not in (([] if local else CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1062
            Exit("Unsupported key for %s configuration %r" % ("local " if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1062
        if key in CONFIGURABLE_FLAGS and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1063
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1063
        c[key] = value.lower() in TRUTH_VALUES if key in CONFIGURABLE_FLAGS else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1064
    elif command == "unset":  # line 1065
        if key is None:  # line 1066
            Exit("No key specified")  # line 1066
        if key not in c.keys():  # HINT: Works on local configurations when used with --local  # line 1067
            Exit("Unknown key")  # HINT: Works on local configurations when used with --local  # line 1067
        del c[key]  # line 1068
    elif command == "add":  # line 1069
        if None in (key, value):  # line 1070
            Exit("Key or value not specified")  # line 1070
        if key not in CONFIGURABLE_LISTS:  # line 1071
            Exit("Unsupported key %r" % key)  # line 1071
        if key not in c.keys():  # prepare empty list, or copy from global, add new value below  # line 1072
            c[key] = [_ for _ in c.__defaults[key]] if local else []  # prepare empty list, or copy from global, add new value below  # line 1072
        elif value in c[key]:  # line 1073
            Exit("Value already contained, nothing to do")  # line 1073
        if ";" in value:  # line 1074
            c[key].append(removePath(key, value))  # line 1074
        else:  # line 1075
            c[key].extend([removePath(key, v) for v in value.split(";")])  # line 1075
    elif command == "rm":  # line 1076
        if None in (key, value):  # line 1077
            Exit("Key or value not specified")  # line 1077
        if key not in c.keys():  # line 1078
            Exit("Unknown key %r" % key)  # line 1078
        if value not in c[key]:  # line 1079
            Exit("Unknown value %r" % value)  # line 1079
        c[key].remove(value)  # line 1080
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1081
            del c[key]  # remove local entry, to fallback to global  # line 1081
    else:  # Show or list  # line 1082
        if key == "ints":  # list valid configuration items  # line 1083
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1083
        elif key == "flags":  # line 1084
            printo(", ".join(CONFIGURABLE_FLAGS))  # line 1084
        elif key == "lists":  # line 1085
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1085
        elif key == "texts":  # line 1086
            printo(", ".join([_ for _ in defaults.keys() if _ not in (CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS)]))  # line 1086
        else:  # line 1087
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1088
            c = m.c  # always use full configuration chain  # line 1089
            try:  # attempt single key  # line 1090
                assert key is not None  # force exception  # line 1091
                c[key]  # force exception  # line 1091
                l = key in c.keys()  # type: bool  # line 1092
                g = key in c.__defaults.keys()  # type: bool  # line 1092
                printo("%s %s %r" % (key.rjust(20), out[3] if not (l or g) else (out[1] if l else out[2]), c[key]))  # line 1093
            except:  # normal value listing  # line 1094
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # line 1095
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1096
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1097
                for k, vt in sorted(vals.items()):  # line 1098
                    printo("%s %s %s" % (k.rjust(20), out[vt[1]], vt[0]))  # line 1098
                if len(c.keys()) == 0:  # line 1099
                    info("No local configuration stored")  # line 1099
                if len(c.__defaults.keys()) == 0:  # line 1100
                    info("No global configuration stored")  # line 1100
        return  # in case of list, no need to store anything  # line 1101
    if local:  # saves changes of repoConfig  # line 1102
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1102
        m.saveBranches()  # saves changes of repoConfig  # line 1102
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1102
    else:  # global config  # line 1103
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1104
        if f is None:  # TODO why no exit here?  # line 1105
            error("Error saving user configuration: %r" % h)  # TODO why no exit here?  # line 1105
        else:  # line 1106
            Exit("OK", code=0)  # line 1106

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1108
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1111
    if verbose:  # line 1112
        info(usage.MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1112
    force = '--force' in options  # type: bool  # line 1113
    soft = '--soft' in options  # type: bool  # line 1114
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1115
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1115
    m = Metadata()  # type: Metadata  # line 1116
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1117
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1118
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1119
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1120
    if not matching and not force:  # line 1121
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1121
    if not (m.track or m.picky):  # line 1122
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 1122
    if pattern not in patterns:  # list potential alternatives and exit  # line 1123
        for tracked in (t for t in patterns if os.path.dirname(t) == relPath):  # for all patterns of the same source folder TODO use SLASH rindex  # line 1124
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1125
            if alternative:  # line 1126
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1126
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: if not (force or soft):  # line 1127
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1128
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1129
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1130
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1134
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1135
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1135
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1136
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1137
    if len({st[1] for st in matches}) != len(matches):  # line 1138
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1138
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1139
    if os.path.exists(encode(newRelPath)):  # line 1140
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1141
        if exists and not (force or soft):  # line 1142
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1142
    else:  # line 1143
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1143
    if not soft:  # perform actual renaming  # line 1144
        for (source, target) in matches:  # line 1145
            try:  # line 1146
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1146
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1147
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1147
    patterns[patterns.index(pattern)] = newPattern  # line 1148
    m.saveBranches()  # line 1149

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1151
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1152
    debug("Parsing command-line arguments...")  # line 1153
    root = os.getcwd()  # line 1154
    try:  # line 1155
        onlys, excps = parseOnlyOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1156
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1157
        arguments = [c.strip() for c in sys.argv[2:] if not (c.startswith("-") and (len(c) == 2 or c[1] == "-"))]  # type: List[_coconut.typing.Optional[str]]  # line 1158
        options = [c.strip() for c in sys.argv[2:] if c.startswith("-") and (len(c) == 2 or c[1] == "-")]  # options with arguments have to be parsed from sys.argv  # line 1159
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1160
        if command[:1] in "amr":  # line 1161
            relPath, pattern = relativize(root, os.path.join(cwd, arguments[0] if arguments else "."))  # line 1161
        if command[:1] == "m":  # line 1162
            if len(arguments) < 2:  # line 1163
                Exit("Need a second file pattern argument as target for move command")  # line 1163
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1164
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1165
        if command[:1] == "a":  # e.g. addnot  # line 1166
            add(relPath, pattern, options, negative="n" in command)  # e.g. addnot  # line 1166
        elif command[:1] == "b":  # line 1167
            branch(arguments[0], arguments[1], options)  # line 1167
        elif command[:3] == "com":  # line 1168
            commit(arguments[0], options, onlys, excps)  # line 1168
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1169
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1169
        elif command[:2] == "ci":  # line 1170
            commit(arguments[0], options, onlys, excps)  # line 1170
        elif command[:3] == 'con':  # line 1171
            config(arguments, options)  # line 1171
        elif command[:2] == "de":  # line 1172
            destroy(arguments[0], options)  # line 1172
        elif command[:2] == "di":  # line 1173
            diff(arguments[0], options, onlys, excps)  # line 1173
        elif command[:2] == "du":  # line 1174
            dump(arguments[0], options)  # line 1174
        elif command[:1] == "h":  # line 1175
            usage.usage(arguments[0], verbose=verbose)  # line 1175
        elif command[:2] == "lo":  # line 1176
            log(options, cwd)  # line 1176
        elif command[:2] == "li":  # line 1177
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1177
        elif command[:2] == "ls":  # line 1178
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1178
        elif command[:1] == "m":  # e.g. mvnot  # line 1179
            move(relPath, pattern, newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1179
        elif command[:2] == "of":  # line 1180
            offline(arguments[0], arguments[1], options)  # line 1180
        elif command[:2] == "on":  # line 1181
            online(options)  # line 1181
        elif command[:1] == "p":  # line 1182
            publish(arguments[0], cmd, options, onlys, excps)  # line 1182
        elif command[:1] == "r":  # e.g. rmnot  # line 1183
            remove(relPath, pattern, optoions, negative="n" in command)  # e.g. rmnot  # line 1183
        elif command[:2] == "st":  # line 1184
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1184
        elif command[:2] == "sw":  # line 1185
            switch(arguments[0], options, onlys, excps, cwd)  # line 1185
        elif command[:1] == "u":  # line 1186
            update(arguments[0], options, onlys, excps)  # line 1186
        elif command[:1] == "v":  # line 1187
            usage.usage(arguments[0], version=True)  # line 1187
        else:  # line 1188
            Exit("Unknown command '%s'" % command)  # line 1188
        Exit(code=0)  # regular exit  # line 1189
    except (Exception, RuntimeError) as E:  # line 1190
        exception(E)  # line 1191
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing")  # line 1192

def main():  # line 1194
    global debug, info, warn, error  # to modify logger  # line 1195
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1196
    _log = Logger(logging.getLogger(__name__))  # line 1197
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1197
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1198
        sys.argv.remove(option)  # clean up program arguments  # line 1198
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1199
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1199
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1200
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1201
    debug("Detected SOS root folder: %s\nDetected VCS root folder: %s" % (("-" if root is None else root), ("-" if vcs is None else vcs)))  # line 1202
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1203
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1204
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv"):  # in offline mode or just going offline TODO what about git config?  # line 1205
        cwd = os.getcwd()  # line 1206
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1207
        parse(vcs, cwd, cmd)  # line 1208
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1209
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1210
        import subprocess  # only required in this section  # line 1211
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1212
        inp = ""  # type: str  # line 1213
        while True:  # line 1214
            so, se = process.communicate(input=inp)  # line 1215
            if process.returncode is not None:  # line 1216
                break  # line 1216
            inp = sys.stdin.read()  # line 1217
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1218
            if root is None:  # line 1219
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1219
            m = Metadata(root)  # type: Metadata  # line 1220
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1221
            m.saveBranches()  # line 1222
    else:  # line 1223
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1223


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: bool  # this is a trick allowing to modify the flags from the test suite  # line 1227
force_vcs = [None] if '--vcs' in sys.argv else []  # type: bool  # line 1228
verbose = [None] if '--verbose' in sys.argv or '-v' in sys.argv else []  # type: bool  # imported from utility, and only modified here  # line 1229
debug_ = [None] if os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv else []  # type: bool  # line 1230
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1231

_log = Logger(logging.getLogger(__name__))  # line 1233
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1233

if __name__ == '__main__':  # line 1235
    main()  # line 1235
