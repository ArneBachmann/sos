#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xd45a3b0a

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

# Copyright (c) 2017-2018  Arne Bachmann
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
    import sos.utility as _utility  # WARN necessary because "tests" can only mock "sos.utility.input", because "sos" does "import *" from "utility" and "sos.input" cannot be mocked for some reason  # line 10
    from sos.utility import *  # line 11
    from sos.pure import *  # line 12
except:  # line 13
    import usage  # line 14
    import version  # line 15
    import utility as _utility  # line 16
    from utility import *  # line 17
    from pure import *  # line 18

# Dependencies
import configr  # line 21


# Lazy module auto-import for quick tool startup
class shutil:  # line 25
    @_coconut_tco  # line 25
    def __getattribute__(_, key):  # line 25
        global shutil  # line 26
        import shutil  # overrides global reference  # line 27
        return _coconut_tail_call(shutil.__getattribute__, key)  # line 28
shutil = shutil()  # line 29


# Functions
def loadConfig() -> 'configr.Configr':  # line 33
    ''' Simplifies loading user-global config from file system or returning application defaults. '''  # line 34
    config = configr.Configr(usage.COMMAND, defaults=defaults)  # type: configr.Configr  # defaults are used if key is not configured, but won't be saved  # line 35
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # required for testing only  # line 36
    if f is None:  # line 37
        debug("Encountered a problem while loading the user configuration: %r" % g)  # line 37
    return config  # line 38

@_coconut_tco  # line 40
def saveConfig(config: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 40
    return _coconut_tail_call(config.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # saves global config, not local one  # line 41


# Main data class
class Metadata:  # line 45
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 49

    singleton = None  # type: _coconut.typing.Optional[configr.Configr]  # line 51

    def __init__(_, path: '_coconut.typing.Optional[str]'=None, offline: 'bool'=False, remotes: 'List[str]'=[]) -> 'None':  # line 53
        ''' Create empty container object for various repository operations, and import configuration. Offline initializes a repository. '''  # line 54
        _.root = (os.getcwd() if path is None else path)  # type: str  # line 55
        _.tags = []  # type: List[str]  # list of known (unique) tags  # line 56
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 57
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 58
        _.repoConf = {}  # type: Dict[str, Any]  # per-repo configuration items  # line 59
        _.track = None  # type: bool  # line 60
        _.picky = None  # type: bool  # line 60
        _.strict = None  # type: bool  # line 60
        _.compress = None  # type: bool  # line 60
        _.version = None  # type: _coconut.typing.Optional[str]  # line 60
        _.format = None  # type: _coconut.typing.Optional[int]  # line 60
        _.remotes = []  # type: List[str]  # list of secondary storage locations (in same file system, no other protocols), which will replicate all write operations  # line 61
        _.loadBranches(offline=offline, remotes=remotes)  # loads above values from repository, or uses application defaults  # line 62

        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 64
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 65
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 66

        if Metadata.singleton is None:  # load configuration lazily only once per runtime  # line 68
            Metadata.singleton = configr.Configr(data=_.repoConf, defaults=loadConfig())  # load global configuration backed by defaults, as fallback behind the local configuration  # line 69
            if "useColorOutput" in Metadata.singleton:  # otherwise keep default  # line 70
                enableColor(Metadata.singleton.useColorOutput)  # otherwise keep default  # line 70
        _.c = Metadata.singleton  # type: configr.Configr  # line 71

    def isTextType(_, filename: 'str') -> 'bool':  # line 73
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 73

    def correctNegativeIndexing(_, revision: 'int') -> 'int':  # line 75
        ''' As the na_e says, this deter_ines the correct positive revision nu_ber for negative indexing (-1 being last, -2 being second last). '''  # line 76
        revision = revision if revision >= 0 else (max(_.commits) if _.commits else ((lambda _coconut_none_coalesce_item: -1 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.getHighestRevision(_.branch)))) + 1 + revision  # negative indexing  # line 77
        if revision < 0 or (_.commits and revision > max(_.commits)):  # line 78
            Exit("Unknown revision r%02d" % revision)  # line 78
        return revision  # line 79

    def listChanges(_, changed: 'ChangeSet', commitTime: '_coconut.typing.Optional[float]'=None, root: '_coconut.typing.Optional[str]'=None):  # line 81
        ''' List changes. If commitTime (in ms) is defined, also check timestamps of modified files for plausibility (if mtime of new file is <= / older than in last commit, note so).
        commitTimne == None in switch and log
        root: current user's working dir to compute relative paths (cwd is usually repository root), otherwise None (repo-relative)
    '''  # line 85
        relp = lambda path, root: os.path.relpath(path, root).replace(SLASH, os.sep) if root else path  # type: _coconut.typing.Callable[[str, str], str]  # using relative paths if root is not None, otherwise SOS repo normalized paths  # line 86
        moves = dict(changed.moves.values())  # type: Dict[str, PathInfo]  # of origin-pathinfo  # line 87
        realadditions = {k: v for k, v in changed.additions.items() if k not in changed.moves}  # type: Dict[str, PathInfo]  # targets  # line 88
        realdeletions = {k: v for k, v in changed.deletions.items() if k not in moves}  # type: Dict[str, PathInfo]  # sources  # line 89
        if len(changed.moves) > 0:  # line 90
            printo(ajoin("MOV ", ["%s  <-  %s" % (relp(path, root), relp(dpath, root)) for path, (dpath, dinfo) in sorted(changed.moves.items())], "\n") + Style.RESET_ALL, color=Fore.BLUE + Style.BRIGHT)  # line 90
        if len(realadditions) > 0:  # line 91
            printo(ajoin("ADD ", sorted(["%s  (%s)" % (relp(p, root), pure.siSize(pinfo.size) if pinfo is not None else "-") for p, pinfo in realadditions.items()]), "\n"), color=Fore.GREEN)  # line 91
        if len(realdeletions) > 0:  # line 92
            printo(ajoin("DEL ", sorted([relp(p, root) for p in realdeletions.keys()]), "\n"), color=Fore.RED)  # line 92
        if len(changed.modifications) > 0:  # line 93
            printo(ajoin("MOD ", [relp(m, root) + (" <binary>" if not _.isTextType(os.path.basename(m)) else "") + ("" if commitTime is None else (" <older than previously committed>" if pi.mtime < _.paths[m].mtime else "")) + ((" [%s%s %s%s]" % (pure.signedNumber(pi.size - _.paths[m].size), siSize(pi.size - _.paths[m].size), pure.signedNumber(pi.mtime - _.paths[m].mtime), pure.timeString(pi.mtime - _.paths[m].mtime)) if verbose else "") if pi is not None else "") for (m, pi) in sorted(changed.modifications.items())], "\n"), color=Fore.YELLOW)  # line 93

    def loadBranches(_, offline: 'bool'=False, remotes: 'List[str]'=[]):  # line 95
        ''' Load list of branches and current branch info from metadata file. offline = True command avoids message. '''  # line 96
        try:  # fails if not yet created (on initial branch/commit)  # line 97
#      branches:List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 99
                repo, branches, config = json.load(fd)  # line 100
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 101
            _.branch = repo["branch"]  # current branch integer  # line 102
            _.track, _.picky, _.strict, _.compress, _.version, _.format, _.remotes, remote = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format", "remotes", "remote"]]  # line 103
            if remote:  # line 104
                Exit("Cannot access remote SOS repository for local operation. You're attempting to access a backup copy. Consult manual to restore this backup for normal operation")  # line 104
            upgraded = []  # type: List[str]  # line 105
            if _.version is None:  # line 106
                _.version = "0 - pre-1.2"  # line 107
                upgraded.append("pre-1.2")  # line 108
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 109
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 110
                upgraded.append("2018.1210.3028")  # line 111
            if _.format is None:  # must be before 1.3.5+  # line 112
                _.format = 1  # marker for first metadata file format  # line 113
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 114
                upgraded.append("1.3.5")  # line 115
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 116
            _.repoConf = config  # local configuration stored with repository, not in user-wide configuration  # line 117
            if _.format == 1 or _.remotes is None:  # before remotes  # line 118
                _.format = METADATA_FORMAT  # line 119
                _.remotes = []  # default is no remotes  # line 120
                upgraded.append("1.7.0")  # remote URLs introduced  # line 121
            if upgraded:  # line 122
                for upgrade in upgraded:  # line 123
                    printo("WARNING  Upgraded repository metadata to match SOS version %r" % upgrade, color=Fore.YELLOW)  # line 123
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 124
                _.saveBranches()  # line 125
        except Exception as E:  # if not found, create metadata folder with default values  # line 126
            _.branches = {}  # line 127
            _.track, _.picky, _.strict, _.compress, _.version, _.remotes, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, remotes, METADATA_FORMAT]  # line 128
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # hide warning only when going offline  # line 129

    def _saveBranches(_, remote: '_coconut.typing.Optional[str]', data: 'Dikt[str, Any]'):  # line 131
        tryOrIgnore(lambda: shutil.copy2(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), encode(os.path.join((_.root if remote is None else remote), metaFolder, metaBack))))  # backup  # line 132
        try:  # line 133
            with codecs.open(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 133
                json.dump((data, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints (instead of ascii encoding), the file descriptor knows how to encode them  # line 134
        except Exception as E:  # line 135
            debug("Error saving branches%s" % ((" to remote path " + remote) if remote else ""))  # line 135

    def saveBranches(_, also: 'Dict[str, Any]'={}):  # line 137
        ''' Save list of branches and current branch info to metadata file. '''  # line 138
        store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT, "remotes": _.remotes, "remote": False}  # type: Dict[str, Any]  # dictionary of repository settings (while _.repoConf stores user settings)  # line 139
        store.update(also)  # allows overriding certain values at certain points in time  # line 145
        for remote in [None] + _.remotes:  # line 146
            _._saveBranches(remote, store)  # mark remote copies as read-only  # line 147
            store["remote"] = True  # mark remote copies as read-only  # line 147

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 149
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 150
        if name == "":  # line 151
            return -1  # line 151
        try:  # attempt to parse integer string  # line 152
            return int(name)  # attempt to parse integer string  # line 152
        except ValueError:  # line 153
            pass  # line 153
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 154
        return found[0] if found else None  # line 155

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 157
        ''' Convenience accessor for named branches. '''  # line 158
        if name == "":  # current  # line 159
            return _.branch  # current  # line 159
        try:  # attempt to parse integer string  # line 160
            return int(name)  # attempt to parse integer string  # line 160
        except ValueError:  # line 161
            pass  # line 161
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 162
        return found[0] if found else None  # line 163

    def loadBranch(_, branch: 'int'):  # line 165
        ''' Load all commit information from a branch meta data file. '''  # line 166
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 167
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 168
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 169
        _.branch = branch  # line 170

    def saveBranch(_, branch: 'int'):  # line 172
        ''' Save all commits to a branch meta data file. '''  # line 173
        for remote in [None] + _.remotes:  # line 174
            tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile, base=remote)), encode(branchFolder(branch, file=metaBack, base=remote))))  # backup  # line 175
            try:  # line 176
                with codecs.open(encode(branchFolder(branch, file=metaFile, base=remote)), "w", encoding=UTF8) as fd:  # line 176
                    json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 177
            except Exception as E:  # line 178
                debug("Error saving branch%s" % ((" to remote path " + remote) if remote else ""))  # line 178

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 180
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 188
        if verbose:  # line 189
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 189
        now = int(time.time() * 1000)  # type: int  # line 190
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 191
        revision = max(_.commits) if _.commits else 0  # type: int  # line 192
        _.commits.clear()  # line 193
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 194
        for remote in [None] + _.remotes:  # line 199
            tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)) if full else branchFolder(branch, base=(_.root if remote is None else remote)))), lambda e: error("Duplicating remote branch folder %r" % remote))  # line 200
        if full:  # not fast branching via reference - copy all current files to new branch  # line 201
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 202
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 203
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 203
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit  # line 204
            _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 205
        _.saveBranch(branch)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 206
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 207

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 209
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 215
        now = int(time.time() * 1000)  # type: int  # line 216
        simpleMode = not (_.track or _.picky)  # line 217
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 218
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 219
        if verbose:  # line 220
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 220
        _.paths = {}  # type: Dict[str, PathInfo]  # line 221
        if simpleMode:  # branches from file system state. not necessary to create branch folder, as it is done in findChanges below anyway  # line 222
            changed, msg = _.findChanges(branch, 0, progress=simpleMode)  # HINT creates revision folder and versioned files!  # line 223
            _.listChanges(changed)  # line 224
            if msg:  # display compression factor and time taken  # line 225
                printo(msg)  # display compression factor and time taken  # line 225
            _.paths.update(changed.additions.items())  # line 226
        else:  # tracking or picky mode: branch from latest revision  # line 227
            for remote in [None] + _.remotes:  # line 228
                tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)))), lambda e: error("Creating remote branch folder %r" % remote))  # line 229
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 230
                _.loadBranch(_.branch)  # line 231
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO #245 what if last switch was to an earlier revision? no persisting of last checkout  # line 232
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 233
                for path, pinfo in _.paths.items():  # line 234
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 234
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 235
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 236
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 237
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 238

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 240
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 243
        import collections  # used almost only here  # line 244
        binfo = None  # type: BranchInfo  # typing info  # line 245
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 246
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 247
        if deps:  # need to copy all parent revisions to dependent branches first  # line 248
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 249
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 250
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 251
                for dep, _rev in deps:  # line 252
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO #246 align placement of indicator with other uses of progress  # line 253
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 254
#          if rev in _.commits:  # TODO #247 uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 256
                    shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 257
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 258
                for rev in range(minrev + 1, _rev + 1):  # line 259
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 260
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 261
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 262
                        newcommits[dep][rev] = _.commits[rev]  # line 263
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 264
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 265
        printo(pure.ljust() + "\r")  # clean line output  # line 266
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 267
        tryOrIgnore(lambda: os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?"))  # line 268
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 269
        del _.branches[branch]  # line 270
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 271
        _.saveBranches()  # persist modified branches list  # line 272
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 273
            _.commits = commits  # line 274
            _.saveBranch(branch)  # line 275
        _.commits.clear()  # clean memory  # line 276
        return binfo  # line 277

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 279
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 280
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 281
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 282
            _.paths = json.load(fd)  # line 282
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 283
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 284

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 286
        ''' Save all file information to a commit meta data file. '''  # line 287
        for remote in [None] + _.remotes:  # line 288
            try:  # line 289
                target = revisionFolder(branch, revision, base=(_.root if remote is None else remote))  # type: str  # line 290
                tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 291
                tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 292
                with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 293
                    json.dump(_.paths, fd, ensure_ascii=False)  # line 293
            except Exception as E:  # line 294
                debug("Error saving commit%s" % ((" to remote path " + remote) if remote else ""))  # line 294

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 296
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly!)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 305
        import collections  # used almost only here  # line 306
        write = branch is not None and revision is not None  # used for writing commits  # line 307
        if write:  # line 308
            for remote in [None] + _.remotes:  # line 308
                tryOrIgnore(lambda: os.makedirs(encode(revisionFolder(branch, revision, base=(_.root if remote is None else remote)))))  # line 309
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # WARN this code needs explicity argument passing for initialization due to mypy problems with default arguments  # line 310
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 311
        hashed = None  # type: _coconut.typing.Optional[str]  # line 312
        written = None  # type: int  # line 312
        compressed = 0  # type: int  # line 312
        original = 0  # type: int  # line 312
        start_time = time.time()  # type: float  # line 312
        knownPaths = {}  # type: Dict[str, List[str]]  # line 313

# Find relevant folders/files that match specified folder/glob patterns for exclusive inclusion or exclusion
        byFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 316
        onlyByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 317
        dontByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 318
        for path, pinfo in _.paths.items():  # line 319
            if pinfo is None:  # quicker than generator expression above  # line 320
                continue  # quicker than generator expression above  # line 320
            slash = path.rindex(SLASH)  # type: int  # line 321
            byFolder[path[:slash]].append(path[slash + 1:])  # line 322
        for pattern in ([] if considerOnly is None else considerOnly):  # line 323
            slash = pattern.rindex(SLASH)  # line 323
            onlyByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 323
        for pattern in ([] if dontConsider is None else dontConsider):  # line 324
            slash = pattern.rindex(SLASH)  # line 324
            dontByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 324
        for folder, paths in byFolder.items():  # line 325
            pos = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in onlyByFolder.get(folder, [])]) if considerOnly is not None else set(paths)  # type: Set[str]  # line 326
            neg = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in dontByFolder.get(folder, [])]) if dontConsider is not None else set()  # type: Set[str]  # line 327
            knownPaths[folder] = list(pos - neg)  # line 328

        for path, dirnames, filenames in os.walk(_.root):  # line 330
            path = decode(path)  # line 331
            dirnames[:] = [decode(d) for d in dirnames]  # line 332
            filenames[:] = [decode(f) for f in filenames]  # line 333
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 334
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 335
            dirnames.sort()  # line 336
            filenames.sort()  # line 336
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 337
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 338
            if dontConsider:  # line 339
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 340
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 341
                filename = relPath + SLASH + file  # line 342
                filepath = os.path.join(path, file)  # line 343
                try:  # line 344
                    stat = os.stat(encode(filepath))  # line 344
                except Exception as E:  # line 345
                    exception(E)  # line 345
                    continue  # line 345
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 346
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 347
                if show:  # indication character returned  # line 348
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 349
                    printo(pure.ljust(outstring), nl="")  # line 350
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 351
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 352
                    nameHash = hashStr(filename)  # line 353
                    try:  # line 354
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=nameHash) for remote in [None] + _.remotes] if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 355
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 356
                        compressed += written  # line 357
                        original += size  # line 357
                    except PermissionError as E:  # line 358
                        error("File permission error for %s" % filepath)  # line 358
                    except Exception as F:  # HINT e.g. FileNotFoundError will not add to additions  # line 359
                        exception(F)  # HINT e.g. FileNotFoundError will not add to additions  # line 359
                    continue  # with next file  # line 360
                last = _.paths[filename]  # filename is known - check for modifications  # line 361
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 362
                    try:  # line 363
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 364
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 365
                        continue  # line 365
                    except Exception as E:  # line 366
                        exception(E)  # line 366
                elif size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False)):  # detected a modification TODO invert error = False?  # line 367
                    try:  # line 370
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else hashFile(filepath, _.compress, symbols=progressSymbols, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl=""))[0], 0)  # line 371
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 375
                    except Exception as E:  # line 376
                        exception(E)  # line 376
                else:  # with next file  # line 377
                    continue  # with next file  # line 377
                compressed += written  # line 378
                original += last.size if inverse else size  # line 378
            if relPath in knownPaths:  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 379
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 379
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 380
            for file in names:  # line 381
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 382
                    continue  # don't mark ignored files as deleted  # line 382
                pth = path + SLASH + file  # type: str  # line 383
                changed.deletions[pth] = _.paths[pth]  # line 384
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, _.strict))  # line 385
        if progress:  # forces clean line of progress output  # line 386
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 386
        elif verbose:  # line 387
            info("Finished detecting changes")  # line 387
        tt = time.time() - start_time  # type: float  # line 388
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # in KiBi  # line 389
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 390
        msg = (msg + " | " if msg else "") + ("Processing speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 391
        return (changed, msg if msg else None)  # line 392

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 394
        ''' Returns nothing, just updates _.paths in place. '''  # line 395
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 396

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 398
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 399
        try:  # load initial paths  # line 400
            _.loadCommit(branch, startwith)  # load initial paths  # line 400
        except:  # no revisions  # line 401
            yield {}  # no revisions  # line 401
            return None  # no revisions  # line 401
        if incrementally:  # line 402
            yield _.paths  # line 402
        m = Metadata(_.root)  # type: Metadata  # next changes TODO #250 avoid loading all metadata and config  # line 403
        rev = None  # type: int  # next changes TODO #250 avoid loading all metadata and config  # line 403
        for rev in range(startwith + 1, revision + 1):  # line 404
            m.loadCommit(branch, rev)  # line 405
            for p, info in m.paths.items():  # line 406
                if info.size == None:  # line 407
                    del _.paths[p]  # line 407
                else:  # line 408
                    _.paths[p] = info  # line 408
            if incrementally:  # line 409
                yield _.paths  # line 409
        yield None  # for the default case - not incrementally  # line 410

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 412
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 413
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 414

    def parseRevisionString(_, argument: 'str') -> 'Union[Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]], NoReturn]':  # line 416
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
        None is returned in case of error
        Code will sys.exit in case of unknown specified branch/revision
    '''  # line 421
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 422
            return (_.branch, -1)  # no branch/revision specified  # line 422
        if argument == "":  # nothing specified by user, raise error in caller  # line 423
            return (None, None)  # nothing specified by user, raise error in caller  # line 423
        argument = argument.strip()  # line 424
        if argument.startswith(SLASH):  # current branch  # line 425
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 425
        if argument.endswith(SLASH):  # line 426
            try:  # line 427
                return (_.getBranchByName(argument[:-1]), -1)  # line 427
            except ValueError:  # line 428
                Exit("Unknown branch label '%s'" % argument)  # line 428
        if SLASH in argument:  # line 429
            b, r = argument.split(SLASH)[:2]  # line 430
            try:  # line 431
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 431
            except ValueError:  # line 432
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 432
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 433
        if branch not in _.branches:  # line 434
            branch = None  # line 434
        try:  # either branch name/number or reverse/absolute revision number  # line 435
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 435
        except:  # line 436
            Exit("Unknown branch label or wrong number format")  # line 436
        Exit("This should never happen. Please create an issue report")  # line 437

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 439
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 441
        while True:  # line 442
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 443
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 444
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 445
                break  # line 445
            revision -= 1  # line 446
            if revision < 0:  # line 447
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 447
        return revision, source  # line 448

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 450
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 451
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 452
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 453
            return [branch]  # found. need to load commit from other branch instead  # line 453
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 454
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 454
        return others  # line 455

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 457
        return _.getParentBranches(branch, revision)[-1]  # line 457

    @_coconut_tco  # line 459
    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 459
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 460
        m = Metadata()  # type: Metadata  # line 461
        other = branch  # type: _coconut.typing.Optional[int]  # line 462
        while other is not None:  # line 463
            m.loadBranch(other)  # line 464
            if m.commits:  # line 465
                return _coconut_tail_call(max, m.commits)  # line 465
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 466
        return None  # line 467

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 469
        ''' Copy versioned file to other branch/revision. '''  # line 470
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 471
        for remote in [None] + _.remotes:  # line 472
            try:  # line 473
                target = revisionFolder(toBranch, toRevision, file=pinfo.nameHash, base=(_.root if remote is None else remote))  # type: str  # line 474
                shutil.copy2(encode(source), encode(target))  # line 475
            except Exception as E:  # line 476
                error("Copying versioned file%s" % ((" to remote path " % remote) if remote else ""))  # line 476

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 478
        ''' Return file contents, or copy contents into file path provided (used in update and restorefile). '''  # line 479
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 480
        try:  # line 481
            with openIt(source, "r", _.compress) as fd:  # line 481
                if toFile is None:  # read bytes into memory and return  # line 482
                    return fd.read()  # read bytes into memory and return  # line 482
                with open(encode(toFile), "wb") as to:  # line 483
                    while True:  # line 484
                        buffer = fd.read(bufSize)  # line 485
                        to.write(buffer)  # line 486
                        if len(buffer) < bufSize:  # line 487
                            break  # line 487
                    return None  # line 488
        except Exception as E:  # line 489
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 489
        None  # line 490

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 492
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 493
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 494
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 494
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 495
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 496
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 497
        if pinfo.size == 0:  # line 498
            with open(encode(target), "wb"):  # line 499
                pass  # line 499
            try:  # update access/modification timestamps on file system  # line 500
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 500
            except Exception as E:  # line 501
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 501
            return None  # line 502
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 503
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 505
            while True:  # line 506
                buffer = fd.read(bufSize)  # line 507
                to.write(buffer)  # line 508
                if len(buffer) < bufSize:  # line 509
                    break  # line 509
        try:  # update access/modification timestamps on file system  # line 510
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 510
        except Exception as E:  # line 511
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 511
        return None  # line 512


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], remotes: 'List[str]'=[]):  # line 516
    ''' Initial command to start working offline. '''  # line 517
    if os.path.exists(encode(metaFolder)):  # line 518
        if '--force' not in options:  # line 519
            Exit("Repository folder is either already offline or older branches and commits were left over\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 519
        try:  # throw away all previous metadata before going offline  # line 520
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 521
                resource = metaFolder + os.sep + entry  # line 522
                if os.path.isdir(resource):  # line 523
                    shutil.rmtree(encode(resource))  # line 523
                else:  # line 524
                    os.unlink(encode(resource))  # line 524
        except:  # line 525
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder)  # line 525
    for remote in remotes:  # line 526
        try:  # line 527
            os.makedirs(os.path.join(remote, metaFolder))  # line 527
        except Exception as E:  # line 528
            error("Creating remote repository metadata in %s" % remote)  # line 528
    m = Metadata(offline=True, remotes=remotes)  # type: Metadata  # line 529
    if '--strict' in options or m.c.strict:  # always hash contents  # line 530
        m.strict = True  # always hash contents  # line 530
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 531
        m.compress = True  # plain file copies instead of compressed ones  # line 531
    if '--picky' in options or m.c.picky:  # Git-like  # line 532
        m.picky = True  # Git-like  # line 532
    elif '--track' in options or m.c.track:  # Svn-like  # line 533
        m.track = True  # Svn-like  # line 533
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 534
    if title:  # line 535
        printo(title)  # line 535
    if verbose:  # line 536
        info(MARKER + "Going offline...")  # line 536
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 537
    m.branch = 0  # line 538
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 539
    if verbose or '--verbose' in options:  # line 540
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 540
    info(MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 541

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 543
    ''' Finish working offline. '''  # line 544
    if verbose:  # line 545
        info(MARKER + "Going back online...")  # line 545
    force = '--force' in options  # type: bool  # line 546
    m = Metadata()  # type: Metadata  # line 547
    strict = '--strict' in options or m.strict  # type: bool  # line 548
    m.loadBranches()  # line 549
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 550
        Exit("There are still unsynchronized (modified) branches\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions.")  # line 550
    m.loadBranch(m.branch)  # line 551
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 552
    if options.count("--force") < 2:  # line 553
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 554
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 555
        if modified(changed):  # line 556
            Exit("File tree is modified vs. current branch\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 560
    try:  # line 561
        shutil.rmtree(encode(metaFolder))  # line 561
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 561
    except Exception as E:  # line 562
        Exit("Error removing offline repository: %r" % E)  # line 562
    info(MARKER + "Offline repository removed, you're back online")  # line 563

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 565
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not required here, as either branching from last revision anyway, or branching full file tree anyway.
  '''  # line 568
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 569
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 570
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 571
    m = Metadata()  # type: Metadata  # line 572
    m.loadBranch(m.branch)  # line 573
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 574
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 575
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 575
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 576
    if verbose:  # line 577
        info(MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 577
    if last:  # branch from last revision  # line 578
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 578
    else:  # branch from current file tree state  # line 579
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 579
    if not stay:  # line 580
        m.branch = branch  # line 580
    m.saveBranches()  # TODO #253 or indent again?  # line 581
    info(MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 582

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 584
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 585
    m = Metadata()  # type: Metadata  # line 586
    branch = None  # type: _coconut.typing.Optional[int]  # line 586
    revision = None  # type: _coconut.typing.Optional[int]  # line 586
    strict = '--strict' in options or m.strict  # type: bool  # line 587
    branch, revision = m.parseRevisionString(argument)  # line 588
    if branch is None or branch not in m.branches:  # line 589
        Exit("Unknown branch")  # line 589
    m.loadBranch(branch)  # knows commits  # line 590
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 591
    if verbose:  # line 592
        info(MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 592
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 593
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 594
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 599
    return changed  # returning for unit tests only TODO #254 remove?  # line 600

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False, classic: 'bool'=False):  # TODO #255 introduce option to diff against committed revision and not only file tree  # line 602
    ''' The diff display code. '''  # line 603
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 604
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 605
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 606
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 607
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 608
        content = b""  # type: _coconut.typing.Optional[bytes]  # stored state (old = "curr")  # line 609
        if pinfo.size != 0:  # versioned file  # line 610
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 610
            assert content is not None  # versioned file  # line 610
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current state (new = "into")  # line 611
        if classic:  # line 612
            mergeClassic(content, abspath, "b%d/r%02d" % (branch, revision), os.path.basename(abspath), pinfo.mtime, number_)  # line 612
            continue  # line 612
        blocks = None  # type: List[MergeBlock]  # line 613
        nl = None  # type: bytes  # line 613
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 614
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 615
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 616
        for block in blocks:  # line 617
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some of previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # line 620
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 621
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 621
            elif block.tipe == MergeBlockType.REMOVE:  # line 622
                for no, line in enumerate(block.lines):  # line 623
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 623
            elif block.tipe == MergeBlockType.REPLACE:  # line 624
                for no, line in enumerate(block.replaces.lines):  # line 625
                    printo(wrap("old %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 625
                for no, line in enumerate(block.lines):  # line 626
                    printo(wrap("now %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 626
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 629
                printo()  # line 629

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 631
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 632
    m = Metadata()  # type: Metadata  # line 633
    branch = None  # type: _coconut.typing.Optional[int]  # line 633
    revision = None  # type: _coconut.typing.Optional[int]  # line 633
    strict = '--strict' in options or m.strict  # type: bool  # line 634
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 635
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 636
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 637
    if branch is None or branch not in m.branches:  # line 638
        Exit("Unknown branch")  # line 638
    m.loadBranch(branch)  # knows commits  # line 639
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 640
    if verbose:  # line 641
        info(MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 641
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 642
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 643
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap, classic='--classic' in options)  # line 648

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 650
    ''' Create new revision from file tree changes vs. last commit. '''  # line 651
    m = Metadata()  # type: Metadata  # line 652
    if argument is not None and argument in m.tags:  # line 653
        Exit("Illegal commit message. It was already used as a (unique) tag name and cannot be reused")  # line 653
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 654
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 656
        Exit("No file patterns staged for commit in picky mode")  # line 656
    if verbose:  # line 657
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 657
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 658
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 659
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 660
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 661
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 662
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 663
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 664
    m.saveBranch(m.branch)  # line 665
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 666
    if m.picky:  # remove tracked patterns  # line 667
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 667
    else:  # track or simple mode: set branch modified  # line 668
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 668
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 669
        m.tags.append(argument)  # memorize unique tag  # line 669
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 669
    m.saveBranches()  # line 670
    stored = 0  # type: int  # now determine new commit size on file system  # line 671
    overhead = 0  # type: int  # now determine new commit size on file system  # line 671
    count = 0  # type: int  # now determine new commit size on file system  # line 671
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 672
    for file in os.listdir(commitFolder):  # line 673
        try:  # line 674
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 675
            if file == metaFile:  # line 676
                overhead += newsize  # line 676
            else:  # line 677
                stored += newsize  # line 677
                count += 1  # line 677
        except Exception as E:  # line 678
            error(E)  # line 678
    printo(MARKER_COLOR + "Created new revision r%02d%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%s%s%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, (" '%s'" % argument) if argument is not None else "", Fore.GREEN, Fore.RESET, len(changed.additions) - len(changed.moves), Fore.RED, Fore.RESET, len(changed.deletions) - len(changed.moves), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(changed.modifications), Fore.BLUE + Style.BRIGHT, MOVE_SYMBOL if m.c.useUnicodeFont else "#", Style.RESET_ALL, len(changed.moves), pure.siSize(stored + overhead), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 679

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 691
    ''' Show branches and current repository state. '''  # line 692
    m = Metadata()  # type: Metadata  # line 693
    if not (m.c.useChangesCommand or '--repo' in options):  # line 694
        changes(argument, options, onlys, excps)  # line 694
        return  # line 694
    current = m.branch  # type: int  # line 695
    strict = '--strict' in options or m.strict  # type: bool  # line 696
    printo(MARKER_COLOR + "Offline repository status")  # line 697
    printo("Repository root:     %s" % os.getcwd())  # line 698
    printo("Underlying VCS root: %s" % vcs)  # line 699
    printo("Underlying VCS type: %s" % cmd)  # line 700
    printo("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 701
    printo("Current SOS version: %s" % version.__version__)  # line 702
    printo("At creation version: %s" % m.version)  # line 703
    printo("Metadata format:     %s" % m.format)  # line 704
    printo("Content checking:    %s" % (Fore.CYAN + "size, then content" if m.strict else Fore.BLUE + "size & timestamp") + Fore.RESET)  # TODO size then timestamp?  # line 705
    printo("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 706
    printo("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 707
    printo("Number of branches:  %d" % len(m.branches))  # line 708
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 709
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 710
    m.loadBranch(current)  # line 711
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 712
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 713
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 713
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 714
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of unicode symbols for changed vs. unchanged  # line 719
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 723
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 724
        payload = 0  # type: int  # count used storage per branch  # line 725
        overhead = 0  # type: int  # count used storage per branch  # line 725
        original = 0  # type: int  # count used storage per branch  # line 725
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 726
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 727
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 728
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 728
                else:  # line 729
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 729
        pl_amount = float(payload) / MEBI  # type: float  # line 730
        oh_amount = float(overhead) / MEBI  # type: float  # line 730
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 732
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 733
            m.loadCommit(m.branch, commit_)  # line 734
            for pinfo in m.paths.values():  # line 735
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 735
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 736
        printo("  %s b%d%s @%s (%s%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), Fore.RESET, len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 737
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 748
        printo(Fore.GREEN + "Tracked" + Fore.RESET + " file patterns:")  # TODO #261 print matching untracking patterns side-by-side?  # line 749
        printo(ajoin(Fore.GREEN + "  | " + Fore.RESET, m.branches[m.branch].tracked, "\n"))  # line 750
        printo(Fore.RED + "Untracked" + Fore.RESET + " file patterns:")  # line 751
        printo(ajoin(Fore.RED + "  | " + Fore.RESET, m.branches[m.branch].untracked, "\n"))  # line 752

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 754
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 761
    assert not (check and commit)  # line 762
    m = Metadata()  # type: Metadata  # line 763
    force = '--force' in options  # type: bool  # line 764
    strict = '--strict' in options or m.strict  # type: bool  # line 765
    if argument is not None:  # line 766
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 767
        if branch is None:  # line 768
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 768
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 769
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 770

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 773
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 774
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 775
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 776
    if check and modified(changed) and not force:  # line 781
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 782
        Exit("File tree contains changes. Use --force to proceed")  # line 783
    elif commit:  # line 784
        if not modified(changed) and not force:  # line 785
            Exit("Nothing to commit")  # line 785
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 786
        if msg:  # line 787
            printo(msg)  # line 787

    if argument is not None:  # branch/revision specified  # line 789
        m.loadBranch(branch)  # knows commits of target branch  # line 790
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 791
        revision = m.correctNegativeIndexing(revision)  # line 792
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 793
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 794

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 796
    ''' Continue work on another branch, replacing file tree changes. '''  # line 797
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 798
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 799

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 802
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 803
    else:  # full file switch  # line 804
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 805
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 806

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 813
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 814
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 815
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 816
                rms.append(a)  # line 816
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 817
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 817
        if modified(changed) and not force:  # line 818
            m.listChanges(changed, cwd)  # line 818
            Exit("File tree contains changes. Use --force to proceed")  # line 818
        if verbose:  # line 819
            info(MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 819
        if not modified(todos):  # line 820
            info("No changes to current file tree")  # line 821
        else:  # integration required  # line 822
            for path, pinfo in todos.deletions.items():  # line 823
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 824
                printo("ADD " + path, color=Fore.GREEN)  # line 825
            for path, pinfo in todos.additions.items():  # line 826
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 827
                printo("DEL " + path, color=Fore.RED)  # line 828
            for path, pinfo in todos.modifications.items():  # line 829
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 830
                printo("MOD " + path, color=Fore.YELLOW)  # line 831
    m.branch = branch  # line 832
    m.saveBranches()  # store switched path info  # line 833
    info(MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 834

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 836
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 840
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 841
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 842
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 843
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 844
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 845
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 846
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 847
    if verbose:  # line 848
        info(MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 848

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 851
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 852
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 853
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 854
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 859
        if trackingUnion != trackingPatterns:  # nothing added  # line 860
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 861
        else:  # line 862
            info("Nothing to update")  # but write back updated branch info below  # line 863
    else:  # integration required  # line 864
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 865
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 865
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 865
        if changed.deletions.items():  # line 866
            printo("Additions:")  # line 866
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 867
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 868
            if add_all is None and mrg == MergeOperation.ASK:  # line 869
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 870
                if selection in "ao":  # line 871
                    add_all = "y" if selection == "a" else "n"  # line 871
                    selection = add_all  # line 871
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 872
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 872
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path, color=Fore.GREEN)  # TODO #268 document merge/update output, e.g. (A) as "selected not to add by user choice"  # line 873
        if changed.additions.items():  # line 874
            printo("Deletions:")  # line 874
        for path, pinfo in changed.additions.items():  # line 875
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 876
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 876
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 877
            if del_all is None and mrg == MergeOperation.ASK:  # line 878
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 879
                if selection in "ao":  # line 880
                    del_all = "y" if selection == "a" else "n"  # line 880
                    selection = del_all  # line 880
            if "y" in (del_all, selection):  # line 881
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 881
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path, color=Fore.RED)  # not contained in other branch, but maybe kept  # line 882
        if changed.modifications.items():  # line 883
            printo("Modifications:")  # line 883
        for path, pinfo in changed.modifications.items():  # line 884
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 885
            binary = not m.isTextType(path)  # type: bool  # line 886
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 887
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 888
                printo(("MOD " if not binary else "BIN ") + path, color=Fore.YELLOW)  # TODO print mtime, size differences?  # line 889
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 890
            if op == "t":  # line 891
                printo("THR " + path, color=Fore.MAGENTA)  # blockwise copy of contents  # line 892
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 892
            elif op == "m":  # line 893
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 894
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 894
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 895
                if current == file and verbose:  # line 896
                    info("No difference to versioned file")  # line 896
                elif file is not None:  # if None, error message was already logged  # line 897
                    merged = None  # type: bytes  # line 898
                    nl = None  # type: bytes  # line 898
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 899
                    if merged != current:  # line 900
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 901
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 901
                    elif verbose:  # TODO but update timestamp?  # line 902
                        info("No change")  # TODO but update timestamp?  # line 902
            else:  # mine or wrong input  # line 903
                printo("MNE " + path, color=Fore.CYAN)  # nothing to do! same as skip  # line 904
    info(MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 905
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 906
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 907
    m.saveBranches()  # line 908

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 910
    ''' Remove a branch entirely. '''  # line 911
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 912
    if len(m.branches) == 1:  # line 913
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 913
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 914
    if branch is None or branch not in m.branches:  # line 915
        Exit("Cannot delete unknown branch %r" % branch)  # line 915
    if verbose:  # line 916
        info(MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 916
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 917
    info(MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 918

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 920
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 921
    force = '--force' in options  # type: bool  # line 922
    m = Metadata()  # type: Metadata  # line 923
    if not (m.track or m.picky):  # line 924
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 924
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 925
    if pattern in patterns:  # line 926
        Exit("Pattern '%s' already tracked" % pattern)  # line 926
    if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 927
        Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 927
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 928
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 929
    patterns.append(pattern)  # line 930
    m.saveBranches()  # line 931
    info(MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # line 932

def remove(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 934
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 935
    m = Metadata()  # type: Metadata  # line 936
    if not (m.track or m.picky):  # line 937
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' to start repository in tracking or picky mode")  # line 937
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 938
    if pattern not in patterns:  # line 939
        suggestion = _coconut.set()  # type: Set[str]  # line 940
        for pat in patterns:  # line 941
            if fnmatch.fnmatch(pattern, pat):  # line 941
                suggestion.add(pat)  # line 941
        if suggestion:  # line 942
            printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # line 942
        Exit("Tracked pattern '%s' not found" % pattern)  # line 943
    patterns.remove(pattern)  # line 944
    m.saveBranches()  # line 945
    info(MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 946

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 948
    ''' List specified directory, augmenting with repository metadata. '''  # line 949
    m = Metadata()  # type: Metadata  # line 950
    folder = (os.getcwd() if folder is None else folder)  # line 951
    if '--all' in options or '-a' in options:  # always start at SOS repo root with --all  # line 952
        folder = m.root  # always start at SOS repo root with --all  # line 952
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 953
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 954
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 955
    if verbose:  # line 956
        info(MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 956
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 957
    if relPath.startswith(os.pardir):  # line 958
        Exit("Cannot list contents of folder outside offline repository")  # line 958
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 959
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 960
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 961
        if len(m.tags) > 0:  # line 962
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 962
        return  # line 963
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 964
        if not recursive:  # avoid recursion  # line 965
            dirnames.clear()  # avoid recursion  # line 965
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 966
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 967

        folder = decode(dirpath)  # line 969
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 970
        if patterns:  # line 971
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 972
            if out:  # line 973
                printo("DIR %s\n" % relPath + out)  # line 973
            continue  # with next folder  # line 974
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 975
        if len(files) > 0:  # line 976
            printo("DIR %s" % relPath)  # line 976
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 977
            ignore = None  # type: _coconut.typing.Optional[str]  # line 978
            for ig in m.c.ignores:  # remember first match  # line 979
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 979
                    ignore = ig  # remember first match  # line 979
                    break  # remember first match  # line 979
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 980
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 980
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 980
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 980
                        break  # found a white list entry for ignored file, undo ignoring it  # line 980
            matches = []  # type: List[str]  # line 981
            if not ignore:  # line 982
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 983
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 984
                        matches.append(os.path.basename(pattern))  # line 984
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 985
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 986

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 988
    ''' List previous commits on current branch. '''  # line 989
    changes_ = "--changes" in options  # type: bool  # line 990
    diff_ = "--diff" in options  # type: bool  # line 991
    m = Metadata()  # type: Metadata  # line 992
    m.loadBranch(m.branch)  # knows commit history  # line 993
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 994
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 995
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Offline commit history of branch %r" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 996
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 997
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 998
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 999
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 1000
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 1001
    commit = None  # type: CommitInfo  # used for reading parent branch information  # line 1001
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1002
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 1003
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 1004
    for no in range(maxi + 1):  # line 1005
        if indicator:  # line 1006
            printo("  %%s %%0%dd" % digits % ((lambda _coconut_none_coalesce_item: " " if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(indicator.getIndicator()), no), nl="\r")  # line 1006
        if no in m.commits:  # line 1007
            commit = m.commits[no]  # line 1007
        else:  # line 1008
            if n.branch != n.getParentBranch(m.branch, no):  # line 1009
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 1009
            commit = n.commits[no]  # line 1010
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 1011
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 1012
        if "--all" in options or no >= lastno:  # line 1013
            if no >= lastno:  # line 1014
                indicator = None  # line 1014
            _add = news - olds  # type: FrozenSet[str]  # line 1015
            _del = olds - news  # type: FrozenSet[str]  # line 1016
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 1018
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 1020
            printo("  %s r%s @%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%sT%s%02d) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, Fore.RESET, len(_add), Fore.RED, Fore.RESET, len(_del), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(_mod), Fore.CYAN, Fore.RESET, _txt, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 1021
            if changes_:  # line 1022
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}), root=cwd if '--relative' in options else None)  # TODO why using None here? to avoid stating files for performance reasons?  # line 1033
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 1034
                pass  #  _diff(m, changes)  # needs from revision diff  # line 1034
        olds = news  # replaces olds for next revision compare  # line 1035
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 1036

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 1038
    ''' Exported entire repository as archive for easy transfer. '''  # line 1039
    if verbose:  # line 1040
        info(MARKER + "Dumping repository to archive...")  # line 1040
    m = Metadata()  # type: Metadata  # to load the configuration  # line 1041
    progress = '--progress' in options  # type: bool  # line 1042
    delta = '--full' not in options  # type: bool  # line 1043
    skipBackup = '--skip-backup' in options  # type: bool  # line 1044
    import functools  # line 1045
    import locale  # line 1045
    import warnings  # line 1045
    import zipfile  # line 1045
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 1046
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 1046
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 1046
    except:  # line 1047
        compression = zipfile.ZIP_STORED  # line 1047

    if ("" if argument is None else argument) == "":  # line 1049
        Exit("Argument missing (target filename)")  # line 1049
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 1050
    entries = []  # type: List[str]  # line 1051
    if os.path.exists(encode(argument)) and not skipBackup:  # line 1052
        try:  # line 1053
            if verbose:  # line 1054
                info("Creating backup...")  # line 1054
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 1055
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 1056
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 1056
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 1056
        except Exception as E:  # line 1057
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 1057
    if verbose:  # line 1058
        info("Dumping revisions...")  # line 1058
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1059
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1059
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1060
        _zip.debug = 0  # suppress debugging output  # line 1061
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1062
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1063
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1064
        totalsize = 0  # type: int  # line 1065
        start_time = time.time()  # type: float  # line 1066
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1067
            dirpath = decode(dirpath)  # line 1068
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1069
                continue  # don't backup backups  # line 1069
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1070
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1071
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1072
            for filename in filenames:  # line 1073
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1074
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1075
                totalsize += os.stat(encode(abspath)).st_size  # line 1076
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1077
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1078
                    continue  # don't backup backups  # line 1078
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1079
                    if show:  # line 1080
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1080
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1081
        if delta:  # line 1082
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1082
    info("\r" + pure.ljust(MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1083

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1085
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1086
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1087
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1088
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1088
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1089
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1090
    if maxi is None:  # line 1091
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1091
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1092
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1095
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1097
    while files:  # line 1098
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1099
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1100
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1102
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1102
    tracked = None  # type: bool  # line 1103
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1103
    tracked, commitArgs = vcsCommits[cmd]  # line 1103
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1104
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1106
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1106
    if tracked:  # line 1107
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1107

def config(arguments: 'List[_coconut.typing.Optional[str]]', options: 'List[str]'=[]):  # line 1109
    command = None  # type: str  # line 1110
    key = None  # type: str  # line 1110
    value = None  # type: str  # line 1110
    v = None  # type: str  # line 1110
    command, key, value = (arguments + [None] * 2)[:3]  # line 1111
    if command is None:  # line 1112
        usage.usage("help", verbose=True)  # line 1112
    if command not in ("set", "unset", "show", "list", "add", "rm"):  # line 1113
        Exit("Unknown config command %r" % command)  # line 1113
    local = "--local" in options  # type: bool  # line 1114
    m = Metadata()  # type: Metadata  # loads layered configuration as well  # line 1115
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1116
    if command == "set":  # line 1117
        if None in (key, value):  # line 1118
            Exit("Key or value not specified")  # line 1118
        if key not in ((([] if local else ONLY_GLOBAL_FLAGS) + CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1119
            Exit("Unsupported key for %s configuration %r" % ("local" if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1119
        if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1120
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1120
        c[key] = value.lower() in TRUTH_VALUES if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1121
    elif command == "unset":  # line 1122
        if key is None:  # line 1123
            Exit("No key specified")  # line 1123
        if key not in c.keys(with_nested=False):  # line 1124
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, "local" if local else "global"))  # line 1125
        del c[key]  # line 1126
    elif command == "add":  # line 1127
        if None in (key, value):  # line 1128
            Exit("Key or value not specified")  # line 1128
        if key not in CONFIGURABLE_LISTS:  # line 1129
            Exit("Unsupported key %r for list addition" % key)  # line 1129
        if key not in c.keys():  # prepare empty list, or copy from underlying, add new value below  # line 1130
            c[key] = [_ for _ in c.__defaults[key]] if key in c.__defaults[key] else []  # prepare empty list, or copy from underlying, add new value below  # line 1130
        elif value in c[key]:  # line 1131
            Exit("Value already contained, nothing to do")  # line 1131
        if ";" in value:  # line 1132
            c[key].append(removePath(key, value))  # line 1132
        else:  # line 1133
            c[key].extend([removePath(key, v) for v in value.split(";")])  # line 1133
    elif command == "rm":  # line 1134
        if None in (key, value):  # line 1135
            Exit("Key or value not specified")  # line 1135
        if key not in c.keys(with_nested=False):  # line 1136
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, "local" if local else "global"))  # line 1137
        if value not in c[key]:  # line 1138
            Exit("Unknown value %r" % value)  # line 1138
        c[key].remove(value)  # line 1139
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1140
            del c[key]  # remove local entry, to fallback to global  # line 1140
    else:  # Show or list  # line 1141
        if key == "ints":  # list valid configuration items  # line 1142
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1142
        elif key == "flags":  # line 1143
            printo(", ".join(ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS))  # line 1143
        elif key == "lists":  # line 1144
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1144
        elif key == "texts":  # line 1145
            printo(", ".join([_ for _ in defaults.keys() if _ not in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS + CONFIGURABLE_INTS + CONFIGURABLE_LISTS)]))  # line 1145
        else:  # no key: list all  # line 1146
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1147
            c = m.c  # always use full configuration chain  # line 1148
            try:  # attempt single key  # line 1149
                assert key is not None  # force exception if no key specified  # line 1150
                c[key]  # force exception if no key specified  # line 1150
                l = key in c.keys(with_nested=False)  # type: bool  # line 1151
                g = key in c.__defaults.keys(with_nested=False)  # type: bool  # line 1151
                printo(key.rjust(20), color=Fore.WHITE, nl="")  # line 1152
                printo(" " + (out[3] if not (l or g) else (out[1] if l else out[2])) + " ", color=Fore.CYAN, nl="")  # line 1153
                printo(repr(c[key]))  # line 1154
            except:  # normal value listing  # line 1155
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # copy-by-value  # line 1156
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1157
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1158
                for k, vt in sorted(vals.items()):  # line 1159
                    printo(k.rjust(20), color=Fore.WHITE, nl="")  # line 1160
                    printo(" " + out[vt[1]] + " ", color=Fore.CYAN, nl="")  # line 1161
                    printo(vt[0])  # line 1162
                if len(c.keys()) == 0:  # line 1163
                    info("No local configuration stored")  # line 1163
                if len(c.__defaults.keys()) == 0:  # line 1164
                    info("No global configuration stored.")  # line 1164
        return  # in case of list, no need to store anything  # line 1165
    if local:  # saves changes of repoConfig  # line 1166
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1166
        m.saveBranches()  # saves changes of repoConfig  # line 1166
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1166
    else:  # global config  # line 1167
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1168
        if f is None:  # line 1169
            Exit("Error saving user configuration: %r" % h)  # line 1169

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1171
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1174
    if verbose:  # line 1175
        info(MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1175
    force = '--force' in options  # type: bool  # line 1176
    soft = '--soft' in options  # type: bool  # line 1177
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1178
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1178
    m = Metadata()  # type: Metadata  # line 1179
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1180
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1181
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1182
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1183
    if not matching and not force:  # line 1184
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1184
    if not (m.track or m.picky):  # line 1185
        Exit("Repository is in simple mode. Use basic file operations to modify files, then execute 'sos commit' to version any changes")  # line 1185
    if pattern not in patterns:  # list potential alternatives and exit  # line 1186
        for tracked in (t for t in patterns if t[:t.rindex(SLASH)] == relPath):  # for all patterns of the same source folder HINT was os.path.dirpath before  # line 1187
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1188
            if alternative:  # line 1189
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1189
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: "if not (force or soft):""  # line 1190
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1191
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1192
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1193
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1197
#  oldTokens:GlobBlock[]?; newToken:GlobBlock[]?  # TODO remove optional?, only here to satisfy mypy
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1199
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1200
    if len({st[1] for st in matches}) != len(matches):  # line 1201
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1201
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1202
    if os.path.exists(encode(newRelPath)):  # line 1203
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1204
        if exists and not (force or soft):  # line 1205
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1205
    else:  # line 1206
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1206
    if not soft:  # perform actual renaming  # line 1207
        for (source, target) in matches:  # line 1208
            try:  # line 1209
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1209
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1210
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1210
    patterns[patterns.index(pattern)] = newPattern  # line 1211
    m.saveBranches()  # line 1212

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1214
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1215
    debug("Parsing command-line arguments...")  # line 1216
    root = os.getcwd()  # line 1217
    try:  # line 1218
        onlys, excps, remotes = parseArgumentOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1219
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1220
        arguments = [c.strip() for c in sys.argv[2:] if not ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # line 1221
        options = [c.strip() for c in sys.argv[2:] if ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # options *with* arguments have to be parsed directly from sys.argv inside using functions  # line 1222
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1223
        if command[:1] in "amr":  # line 1224
            relPath, pattern = relativize(root, os.path.join(cwd, arguments[0] if arguments else "."))  # line 1224
        if command[:1] == "m":  # line 1225
            if len(arguments) < 2:  # line 1226
                Exit("Need a second file pattern argument as target for move command")  # line 1226
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1227
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1228
        if command == "raise":  # line 1229
            raise Exception("provoked exception")  # line 1229
        elif command[:1] == "a":  # e.g. addnot  # TODO allow multiple paths semicolon-separated  # line 1230
            add(relPath, pattern, options, negative="n" in command)  # e.g. addnot  # TODO allow multiple paths semicolon-separated  # line 1230
        elif command[:1] == "b":  # line 1231
            branch(arguments[0], arguments[1], options)  # line 1231
        elif command[:3] == "com":  # line 1232
            commit(arguments[0], options, onlys, excps)  # line 1232
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1233
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1233
        elif command[:2] == "ci":  # line 1234
            commit(arguments[0], options, onlys, excps)  # line 1234
        elif command[:3] == 'con':  # line 1235
            config(arguments, options)  # line 1235
        elif command[:2] == "de":  # line 1236
            destroy((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1236
        elif command[:2] == "di":  # TODO no consistent handling of single dash/characters argument-options  # line 1237
            diff((lambda _coconut_none_coalesce_item: "/" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[2 if arguments[0] == '-n' else 0]), options, onlys, excps)  # TODO no consistent handling of single dash/characters argument-options  # line 1237
        elif command[:2] == "du":  # line 1238
            dump((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1238
        elif command[:1] == "h":  # line 1239
            usage.usage(arguments[0], verbose=verbose)  # line 1239
        elif command[:2] == "lo":  # line 1240
            log(options, cwd)  # line 1240
        elif command[:2] == "li":  # line 1241
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1241
        elif command[:2] == "ls":  # line 1242
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1242
        elif command[:1] == "m":  # e.g. mvnot  # line 1243
            move(relPath, pattern, newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1243
        elif command[:2] == "of":  # line 1244
            offline(arguments[0], arguments[1], options, remotes)  # line 1244
        elif command[:2] == "on":  # line 1245
            online(options)  # line 1245
        elif command[:1] == "p":  # line 1246
            publish(arguments[0], cmd, options, onlys, excps)  # line 1246
        elif command[:1] == "r":  # e.g. rmnot  # line 1247
            remove(relPath, pattern, options, negative="n" in command)  # e.g. rmnot  # line 1247
        elif command[:2] == "st":  # line 1248
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1248
        elif command[:2] == "sw":  # line 1249
            switch((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps, cwd)  # line 1249
        elif command[:1] == "u":  # line 1250
            update((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps)  # line 1250
        elif command[:1] == "v":  # line 1251
            usage.usage(arguments[0], version=True)  # line 1251
        else:  # line 1252
            Exit("Unknown command '%s'" % command)  # line 1252
        Exit(code=0)  # regular exit  # line 1253
    except (Exception, RuntimeError) as E:  # line 1254
        exception(E)  # line 1255
        Exit("An internal error occurred in SOS\nPlease report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.")  # line 1256

def main():  # line 1258
    global debug, info, warn, error  # to modify logger  # line 1259
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1260
    _log = Logger(logging.getLogger(__name__))  # line 1261
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1261
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1262
        sys.argv.remove(option)  # clean up program arguments  # line 1262
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1263
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1263
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1264
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1265
    debug("Detected SOS root folder: %s" % (("-" if root is None else root)))  # line 1266
    debug("Detected VCS root folder: %s" % (("-" if vcs is None else vcs)))  # line 1267
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1268
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1269
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv"):  # in offline mode or just going offline  # line 1270
        cwd = os.getcwd()  # line 1271
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1272
        parse(vcs, cwd, cmd)  # line 1273
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1274
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1275
        import subprocess  # only required in this section  # line 1276
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1277
        inp = ""  # type: str  # line 1278
        while True:  # line 1279
            so, se = process.communicate(input=inp)  # line 1280
            if process.returncode is not None:  # line 1281
                break  # line 1281
            inp = sys.stdin.read()  # line 1282
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1283
            if root is None:  # line 1284
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1284
            m = Metadata(root)  # type: Metadata  # line 1285
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1286
            m.saveBranches()  # line 1287
    else:  # line 1288
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1288


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: List[None]  # this is a trick allowing to modify the module-level flags from the test suite  # line 1292
force_vcs = [None] if '--vcs' in sys.argv else []  # type: List[None]  # line 1293
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1294

_log = Logger(logging.getLogger(__name__))  # line 1296
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1296

if __name__ == '__main__':  # line 1298
    main()  # line 1298
