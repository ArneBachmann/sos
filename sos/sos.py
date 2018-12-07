#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xf03ba30d

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
try:  # line 21
    import configr  # line 21
except:  # TODO this is here to avoid import error when setup.py is called but actually needs to install its dependencies first. enhance this  # line 22
    pass  # TODO this is here to avoid import error when setup.py is called but actually needs to install its dependencies first. enhance this  # line 22


# Lazy module auto-import for quick tool startup
class shutil:  # line 26
    @_coconut_tco  # line 26
    def __getattribute__(_, key):  # line 26
        global shutil  # line 27
        import shutil  # overrides global reference  # line 28
        return _coconut_tail_call(shutil.__getattribute__, key)  # line 29
shutil = shutil()  # line 30


# Functions
def loadConfig() -> 'configr.Configr':  # line 34
    ''' Simplifies loading user-global config from file system or returning application defaults. '''  # line 35
    config = configr.Configr(usage.COMMAND, defaults=defaults)  # type: configr.Configr  # defaults are used if key is not configured, but won't be saved  # line 36
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # required for testing only  # line 37
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

    def __init__(_, path: '_coconut.typing.Optional[str]'=None, offline: 'bool'=False, remotes: 'List[str]'=[]) -> 'None':  # line 54
        ''' Create empty container object for various repository operations, and import configuration. Offline initializes a repository. '''  # line 55
        _.root = (os.getcwd() if path is None else path)  # type: str  # line 56
        _.tags = []  # type: List[str]  # list of known (unique) tags  # line 57
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 58
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 59
        _.repoConf = {}  # type: Dict[str, Any]  # per-repo configuration items  # line 60
        _.track = None  # type: bool  # line 61
        _.picky = None  # type: bool  # line 61
        _.strict = None  # type: bool  # line 61
        _.compress = None  # type: bool  # line 61
        _.version = None  # type: _coconut.typing.Optional[str]  # line 61
        _.format = None  # type: _coconut.typing.Optional[int]  # line 61
        _.remotes = []  # type: List[str]  # list of secondary storage locations (in same file system, no other protocols), which will replicate all write operations  # line 62
        _.loadBranches(offline=offline, remotes=remotes)  # loads above values from repository, or uses application defaults  # line 63

        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 65
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 66
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 67

        if Metadata.singleton is None:  # load configuration lazily only once per runtime  # line 69
            Metadata.singleton = configr.Configr(data=_.repoConf, defaults=loadConfig())  # load global configuration backed by defaults, as fallback behind the local configuration  # line 70
            if "useColorOutput" in Metadata.singleton:  # otherwise keep default  # line 71
                enableColor(Metadata.singleton.useColorOutput)  # otherwise keep default  # line 71
        _.c = Metadata.singleton  # type: configr.Configr  # line 72

    def isTextType(_, filename: 'str') -> 'bool':  # line 74
        ''' Based on the file extension or user-defined file patterns, this function determines if the file is of any diffable text type. '''  # line 75
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 76

    def correctNegativeIndexing(_, revision: 'int') -> 'int':  # line 78
        ''' As the na_e says, this deter_ines the correct positive revision nu_ber for negative indexing (-1 being last, -2 being second last). '''  # line 79
        revision = revision if revision >= 0 else (max(_.commits) if _.commits else ((lambda _coconut_none_coalesce_item: -1 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.getHighestRevision(_.branch)))) + 1 + revision  # negative indexing  # line 80
        if revision < 0 or (_.commits and revision > max(_.commits)):  # line 81
            Exit("Unknown revision r%02d" % revision)  # line 81
        return revision  # line 82

    def listChanges(_, changed: 'ChangeSet', commitTime: '_coconut.typing.Optional[float]'=None, root: '_coconut.typing.Optional[str]'=None):  # line 84
        ''' List changes. If commitTime (in ms) is defined, also check timestamps of modified files for plausibility (if mtime of new file is <= / older than in last commit, note so).
        commitTimne == None in switch and log
        root: current user's working dir to compute relative paths (cwd is usually repository root), otherwise None (repo-relative)
    '''  # line 88
        relp = lambda path, root: os.path.relpath(path, root).replace(SLASH, os.sep) if root else path  # type: _coconut.typing.Callable[[str, str], str]  # using relative paths if root is not None, otherwise SOS repo normalized paths  # line 89
        moves = dict(changed.moves.values())  # type: Dict[str, PathInfo]  # of origin-pathinfo  # line 90
        realadditions = {k: v for k, v in changed.additions.items() if k not in changed.moves}  # type: Dict[str, PathInfo]  # targets  # line 91
        realdeletions = {k: v for k, v in changed.deletions.items() if k not in moves}  # type: Dict[str, PathInfo]  # sources  # line 92
        if len(changed.moves) > 0:  # line 93
            printo(ajoin("MOV ", ["%s  <-  %s" % (relp(path, root), relp(dpath, root)) for path, (dpath, dinfo) in sorted(changed.moves.items())], "\n") + Style.RESET_ALL, color=Fore.BLUE + Style.BRIGHT)  # line 93
        if len(realadditions) > 0:  # line 94
            printo(ajoin("ADD ", sorted(["%s  (%s)" % (relp(p, root), pure.siSize(pinfo.size) if pinfo is not None else "-") for p, pinfo in realadditions.items()]), "\n"), color=Fore.GREEN)  # line 94
        if len(realdeletions) > 0:  # line 95
            printo(ajoin("DEL ", sorted([relp(p, root) for p in realdeletions.keys()]), "\n"), color=Fore.RED)  # line 95
        if len(changed.modifications) > 0:  # line 96
            printo(ajoin("MOD ", [relp(m, root) + (" <binary>" if not _.isTextType(os.path.basename(m)) else "") + ("" if commitTime is None else (" <older than previously committed>" if pi.mtime < _.paths[m].mtime else "")) + ((" [%s%s %s%s]" % (pure.signedNumber(pi.size - _.paths[m].size), siSize(pi.size - _.paths[m].size), pure.signedNumber(pi.mtime - _.paths[m].mtime), pure.timeString(pi.mtime - _.paths[m].mtime)) if verbose else "") if pi is not None else "") for (m, pi) in sorted(changed.modifications.items())], "\n"), color=Fore.YELLOW)  # line 96

    def loadBranches(_, offline: 'bool'=False, remotes: 'List[str]'=[]):  # line 98
        ''' Load list of branches and current branch info from metadata file. offline = True command avoids message. '''  # line 99
        try:  # fails if not yet created (on initial branch/commit)  # line 100
#      branches:List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 102
                repo, branches, config = json.load(fd)  # line 103
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 104
            _.branch = repo["branch"]  # current branch integer  # line 105
            _.track, _.picky, _.strict, _.compress, _.version, _.format, _.remotes, remote = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format", "remotes", "remote"]]  # line 106
            if remote:  # line 107
                Exit("Cannot access remote SOS repository for local operation. You're attempting to access a backup copy. Consult manual to restore this backup for normal operation")  # line 107
            upgraded = []  # type: List[str]  # line 108
            if _.version is None:  # line 109
                _.version = "0 - pre-1.2"  # line 110
                upgraded.append("pre-1.2")  # line 111
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 112
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 113
                upgraded.append("2018.1210.3028")  # line 114
            if _.format is None:  # must be before 1.3.5+  # line 115
                _.format = 1  # marker for first metadata file format  # line 116
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 117
                upgraded.append("1.3.5")  # line 118
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 119
            _.repoConf = config  # local configuration stored with repository, not in user-wide configuration  # line 120
            if _.format == 1 or _.remotes is None:  # before remotes  # line 121
                _.format = METADATA_FORMAT  # line 122
                _.remotes = []  # default is no remotes  # line 123
                upgraded.append("1.7.0")  # remote URLs introduced  # line 124
            if upgraded:  # line 125
                for upgrade in upgraded:  # line 126
                    printo("WARNING  Upgraded repository metadata to match SOS version %r" % upgrade, color=Fore.YELLOW)  # line 126
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 127
                _.saveBranches()  # line 128
        except Exception as E:  # if not found, create metadata folder with default values  # line 129
            _.branches = {}  # line 130
            _.track, _.picky, _.strict, _.compress, _.version, _.remotes, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, remotes, METADATA_FORMAT]  # line 131
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # hide warning only when going offline  # line 132

    def _saveBranches(_, remote: '_coconut.typing.Optional[str]', data: 'Dikt[str, Any]'):  # line 134
        tryOrIgnore(lambda: shutil.copy2(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), encode(os.path.join((_.root if remote is None else remote), metaFolder, metaBack))))  # backup  # line 135
        try:  # line 136
            with codecs.open(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 136
                json.dump((data, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints (instead of ascii encoding), the file descriptor knows how to encode them  # line 137
        except Exception as E:  # line 138
            debug("Error saving branches%s" % ((" to remote path " + remote) if remote else ""))  # line 138

    def saveBranches(_, also: 'Dict[str, Any]'={}):  # line 140
        ''' Save list of branches and current branch info to metadata file. '''  # line 141
        store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT, "remotes": _.remotes, "remote": False}  # type: Dict[str, Any]  # dictionary of repository settings (while _.repoConf stores user settings)  # line 142
        store.update(also)  # allows overriding certain values at certain points in time  # line 148
        for remote in [None] + _.remotes:  # line 149
            _._saveBranches(remote, store)  # mark remote copies as read-only  # line 150
            store["remote"] = True  # mark remote copies as read-only  # line 150

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 152
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 153
        if name == "":  # line 154
            return -1  # line 154
        try:  # attempt to parse integer string  # line 155
            return int(name)  # attempt to parse integer string  # line 155
        except ValueError:  # line 156
            pass  # line 156
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 157
        return found[0] if found else None  # line 158

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 160
        ''' Convenience accessor for named branches. '''  # line 161
        if name == "":  # current  # line 162
            return _.branch  # current  # line 162
        try:  # attempt to parse integer string  # line 163
            return int(name)  # attempt to parse integer string  # line 163
        except ValueError:  # line 164
            pass  # line 164
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 165
        return found[0] if found else None  # line 166

    def loadBranch(_, branch: 'int'):  # line 168
        ''' Load all commit information from a branch meta data file. '''  # line 169
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 170
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 171
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 172
        _.branch = branch  # line 173

    def saveBranch(_, branch: 'int'):  # line 175
        ''' Save all commits to a branch meta data file. '''  # line 176
        for remote in [None] + _.remotes:  # line 177
            tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile, base=remote)), encode(branchFolder(branch, file=metaBack, base=remote))))  # backup  # line 178
            try:  # line 179
                with codecs.open(encode(branchFolder(branch, file=metaFile, base=remote)), "w", encoding=UTF8) as fd:  # line 179
                    json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 180
            except Exception as E:  # line 181
                debug("Error saving branch%s" % ((" to remote path " + remote) if remote else ""))  # line 181

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 183
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 191
        if verbose:  # line 192
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 192
        now = int(time.time() * 1000)  # type: int  # line 193
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 194
        revision = max(_.commits) if _.commits else 0  # type: int  # line 195
        _.commits.clear()  # line 196
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 197
        for remote in [None] + _.remotes:  # line 202
            tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)) if full else branchFolder(branch, base=(_.root if remote is None else remote)))), lambda e: error("Duplicating remote branch folder %r" % remote))  # line 203
        if full:  # not fast branching via reference - copy all current files to new branch  # line 204
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 205
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 206
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 206
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit  # line 207
            _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 208
        _.saveBranch(branch)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 209
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 210

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 212
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 218
        now = int(time.time() * 1000)  # type: int  # line 219
        simpleMode = not (_.track or _.picky)  # line 220
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 221
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 222
        if verbose:  # line 223
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 223
        _.paths = {}  # type: Dict[str, PathInfo]  # line 224
        if simpleMode:  # branches from file system state. not necessary to create branch folder, as it is done in findChanges below anyway  # line 225
            changed, msg = _.findChanges(branch, 0, progress=simpleMode)  # HINT creates revision folder and versioned files!  # line 226
            _.listChanges(changed)  # line 227
            if msg:  # display compression factor and time taken  # line 228
                printo(msg)  # display compression factor and time taken  # line 228
            _.paths.update(changed.additions.items())  # line 229
        else:  # tracking or picky mode: branch from latest revision  # line 230
            for remote in [None] + _.remotes:  # line 231
                tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)))), lambda e: error("Creating remote branch folder %r" % remote))  # line 232
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 233
                _.loadBranch(_.branch)  # line 234
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO #245 what if last switch was to an earlier revision? no persisting of last checkout  # line 235
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 236
                for path, pinfo in _.paths.items():  # line 237
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 237
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 238
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 239
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 240
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 241

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 243
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 246
        import collections  # used almost only here  # line 247
        binfo = None  # type: BranchInfo  # typing info  # line 248
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 249
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 250
        if deps:  # need to copy all parent revisions to dependent branches first  # line 251
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 252
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 253
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 254
                for dep, _rev in deps:  # line 255
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO #246 align placement of indicator with other uses of progress  # line 256
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 257
#          if rev in _.commits:  # TODO #247 uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 259
                    shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 260
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 261
                for rev in range(minrev + 1, _rev + 1):  # line 262
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 263
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 264
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 265
                        newcommits[dep][rev] = _.commits[rev]  # line 266
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 267
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 268
        printo(pure.ljust() + "\r")  # clean line output  # line 269
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 270
        tryOrIgnore(lambda: os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?", exception=E))  # line 271
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 272
        del _.branches[branch]  # line 273
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 274
        _.saveBranches()  # persist modified branches list  # line 275
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 276
            _.commits = commits  # line 277
            _.saveBranch(branch)  # line 278
        _.commits.clear()  # clean memory  # line 279
        return binfo  # line 280

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 282
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 283
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 284
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 285
            _.paths = json.load(fd)  # line 285
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 286
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 287

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 289
        ''' Save all file information to a commit meta data file. '''  # line 290
        for remote in [None] + _.remotes:  # line 291
            try:  # line 292
                target = revisionFolder(branch, revision, base=(_.root if remote is None else remote))  # type: str  # line 293
                tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 294
                tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 295
                with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 296
                    json.dump(_.paths, fd, ensure_ascii=False)  # line 296
            except Exception as E:  # line 297
                debug("Error saving commit%s" % ((" to remote path " + remote) if remote else ""))  # line 297

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 299
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly!)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 308
        import collections  # used almost only here  # line 309
        write = branch is not None and revision is not None  # used for writing commits  # line 310
        if write:  # line 311
            for remote in [None] + _.remotes:  # line 311
                tryOrIgnore(lambda: os.makedirs(encode(revisionFolder(branch, revision, base=(_.root if remote is None else remote)))))  # line 312
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # WARN this code needs explicity argument passing for initialization due to mypy problems with default arguments  # line 313
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 314
        hashed = None  # type: _coconut.typing.Optional[str]  # line 315
        written = None  # type: int  # line 315
        compressed = 0  # type: int  # line 315
        original = 0  # type: int  # line 315
        start_time = time.time()  # type: float  # line 315
        knownPaths = {}  # type: Dict[str, List[str]]  # line 316

# Find relevant folders/files that match specified folder/glob patterns for exclusive inclusion or exclusion
        byFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 319
        onlyByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 320
        dontByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 321
        for path, pinfo in _.paths.items():  # line 322
            if pinfo is None:  # quicker than generator expression above  # line 323
                continue  # quicker than generator expression above  # line 323
            slash = path.rindex(SLASH)  # type: int  # line 324
            byFolder[path[:slash]].append(path[slash + 1:])  # line 325
        for pattern in ([] if considerOnly is None else considerOnly):  # line 326
            slash = pattern.rindex(SLASH)  # line 326
            onlyByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 326
        for pattern in ([] if dontConsider is None else dontConsider):  # line 327
            slash = pattern.rindex(SLASH)  # line 327
            dontByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 327
        for folder, paths in byFolder.items():  # line 328
            pos = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in onlyByFolder.get(folder, [])]) if considerOnly is not None else set(paths)  # type: Set[str]  # line 329
            neg = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in dontByFolder.get(folder, [])]) if dontConsider is not None else set()  # type: Set[str]  # line 330
            knownPaths[folder] = list(pos - neg)  # line 331

        for path, dirnames, filenames in os.walk(_.root):  # line 333
            path = decode(path)  # line 334
            dirnames[:] = [decode(d) for d in dirnames]  # line 335
            filenames[:] = [decode(f) for f in filenames]  # line 336
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 337
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 338
            dirnames.sort()  # line 339
            filenames.sort()  # line 339
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 340
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 341
            if dontConsider:  # line 342
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 343
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 344
                filename = relPath + SLASH + file  # line 345
                filepath = os.path.join(path, file)  # line 346
                try:  # line 347
                    stat = os.stat(encode(filepath))  # line 347
                except Exception as E:  # line 348
                    printo(exception(E))  # line 348
                    continue  # line 348
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 349
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 350
                if show:  # indication character returned  # line 351
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 352
                    printo(pure.ljust(outstring), nl="")  # line 353
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 354
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 355
                    nameHash = hashStr(filename)  # line 356
                    try:  # line 357
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=nameHash) for remote in [None] + _.remotes] if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 358
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 359
                        compressed += written  # line 360
                        original += size  # line 360
                    except PermissionError as E:  # line 361
                        error("File permission error for %s" % filepath)  # line 361
                    except Exception as F:  # HINT e.g. FileNotFoundError will not add to additions  # line 362
                        printo(exception(F))  # HINT e.g. FileNotFoundError will not add to additions  # line 362
                    continue  # with next file  # line 363
                last = _.paths[filename]  # filename is known - check for modifications  # line 364
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 365
                    try:  # line 366
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 367
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 368
                        continue  # line 368
                        compressed += written  # line 369
                        original += last.size if inverse else size  # line 369
                    except Exception as E:  # line 370
                        printo(exception(E))  # line 370
                elif (size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False))):  # detected a modification TODO invert error = False?  # line 371
                    try:  # line 375
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else hashFile(filepath, _.compress, symbols=progressSymbols, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl=""))[0], 0)  # line 376
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 380
                        compressed += written  # line 381
                        original += last.size if inverse else size  # line 381
                    except Exception as E:  # line 382
                        printo(exception(E))  # line 382
                else:  # with next file  # line 383
                    continue  # with next file  # line 383
            if relPath in knownPaths:  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 384
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 384
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 385
            for file in names:  # line 386
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 387
                    continue  # don't mark ignored files as deleted  # line 387
                pth = path + SLASH + file  # type: str  # line 388
                changed.deletions[pth] = _.paths[pth]  # line 389
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, _.strict))  # line 390
        if progress:  # forces clean line of progress output  # line 391
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 391
        elif verbose:  # line 392
            info("Finished detecting changes")  # line 392
        tt = time.time() - start_time  # type: float  # line 393
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # in KiBi  # line 394
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 395
        msg = (msg + " | " if msg else "") + ("Processing speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 396
        return (changed, msg if msg else None)  # line 397

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 399
        ''' Returns nothing, just updates _.paths in place. '''  # line 400
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 401

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 403
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 404
        try:  # load initial paths  # line 405
            _.loadCommit(branch, startwith)  # load initial paths  # line 405
        except:  # no revisions  # line 406
            yield {}  # no revisions  # line 406
            return None  # no revisions  # line 406
        if incrementally:  # line 407
            yield _.paths  # line 407
        m = Metadata(_.root)  # type: Metadata  # next changes TODO #250 avoid loading all metadata and config  # line 408
        rev = None  # type: int  # next changes TODO #250 avoid loading all metadata and config  # line 408
        for rev in range(startwith + 1, revision + 1):  # line 409
            m.loadCommit(branch, rev)  # line 410
            for p, info in m.paths.items():  # line 411
                if info.size == None:  # line 412
                    del _.paths[p]  # line 412
                else:  # line 413
                    _.paths[p] = info  # line 413
            if incrementally:  # line 414
                yield _.paths  # line 414
        yield None  # for the default case - not incrementally  # line 415

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 417
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 418
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 419

    def parseRevisionString(_, argument: 'str') -> 'Union[Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]], NoReturn]':  # line 421
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
        None is returned in case of error
        Code will sys.exit in case of unknown specified branch/revision
    '''  # line 426
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 427
            return (_.branch, -1)  # no branch/revision specified  # line 427
        if argument == "":  # nothing specified by user, raise error in caller  # line 428
            return (None, None)  # nothing specified by user, raise error in caller  # line 428
        argument = argument.strip()  # line 429
        if argument.startswith(SLASH):  # current branch  # line 430
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 430
        if argument.endswith(SLASH):  # line 431
            try:  # line 432
                return (_.getBranchByName(argument[:-1]), -1)  # line 432
            except ValueError as E:  # line 433
                Exit("Unknown branch label '%s'" % argument, exception=E)  # line 433
        if SLASH in argument:  # line 434
            b, r = argument.split(SLASH)[:2]  # line 435
            try:  # line 436
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 436
            except ValueError as E:  # line 437
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r), exception=E)  # line 437
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 438
        if branch not in _.branches:  # line 439
            branch = None  # line 439
        try:  # either branch name/number or reverse/absolute revision number  # line 440
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 440
        except Exception as E:  # line 441
            Exit("Unknown branch label or wrong number format", exception=E)  # line 441
        Exit("This should never happen. Please create an issue report")  # line 442

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 444
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 446
        while True:  # line 447
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 448
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 449
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 450
                break  # line 450
            revision -= 1  # line 451
            if revision < 0:  # line 452
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 452
        return revision, source  # line 453

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 455
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 456
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 457
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 458
            return [branch]  # found. need to load commit from other branch instead  # line 458
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 459
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 459
        return others  # line 460

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 462
        return _.getParentBranches(branch, revision)[-1]  # line 462

    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 464
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 465
        m = Metadata()  # type: Metadata  # line 466
        other = branch  # type: _coconut.typing.Optional[int]  # line 467
        while other is not None:  # line 468
            m.loadBranch(other)  # line 469
            if m.commits:  # line 470
                return max(m.commits)  # line 470
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 471
        return None  # line 472

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 474
        ''' Copy versioned file to other branch/revision. '''  # line 475
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 476
        for remote in [None] + _.remotes:  # line 477
            try:  # line 478
                target = revisionFolder(toBranch, toRevision, file=pinfo.nameHash, base=(_.root if remote is None else remote))  # type: str  # line 479
                shutil.copy2(encode(source), encode(target))  # line 480
            except Exception as E:  # line 481
                error("Copying versioned file%s" % ((" to remote path " % remote) if remote else ""))  # line 481

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 483
        ''' Return file contents, or copy contents into file path provided (used in update and restorefile). '''  # line 484
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 485
        try:  # line 486
            with openIt(source, "r", _.compress) as fd:  # line 486
                if toFile is None:  # read bytes into memory and return  # line 487
                    return fd.read()  # read bytes into memory and return  # line 487
                with open(encode(toFile), "wb") as to:  # line 488
                    while True:  # line 489
                        buffer = fd.read(bufSize)  # line 490
                        to.write(buffer)  # line 491
                        if len(buffer) < bufSize:  # line 492
                            break  # line 492
                    return None  # line 493
        except Exception as E:  # line 494
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 494
        None  # line 495

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 497
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 498
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 499
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 499
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 500
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 501
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 502
        if pinfo.size == 0:  # line 503
            with open(encode(target), "wb"):  # line 504
                pass  # line 504
            try:  # update access/modification timestamps on file system  # line 505
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 505
            except Exception as E:  # line 506
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 506
            return None  # line 507
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 508
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 510
            while True:  # line 511
                buffer = fd.read(bufSize)  # line 512
                to.write(buffer)  # line 513
                if len(buffer) < bufSize:  # line 514
                    break  # line 514
        try:  # update access/modification timestamps on file system  # line 515
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 515
        except Exception as E:  # line 516
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 516
        return None  # line 517


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], remotes: 'List[str]'=[]):  # line 521
    ''' Initial command to start working offline. '''  # line 522
    if os.path.exists(encode(metaFolder)):  # line 523
        if '--force' not in options:  # line 524
            Exit("Repository folder is either already offline or older branches and commits were left over\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 524
        try:  # throw away all previous metadata before going offline  # line 525
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 526
                resource = metaFolder + os.sep + entry  # line 527
                if os.path.isdir(resource):  # line 528
                    shutil.rmtree(encode(resource))  # line 528
                else:  # line 529
                    os.unlink(encode(resource))  # line 529
        except Exception as E:  # line 530
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder, exception=E)  # line 530
    for remote in remotes:  # line 531
        try:  # line 532
            os.makedirs(os.path.join(remote, metaFolder))  # line 532
        except Exception as E:  # line 533
            error("Creating remote repository metadata in %s" % remote)  # line 533
    m = Metadata(offline=True, remotes=remotes)  # type: Metadata  # line 534
    if '--strict' in options or m.c.strict:  # always hash contents  # line 535
        m.strict = True  # always hash contents  # line 535
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 536
        m.compress = True  # plain file copies instead of compressed ones  # line 536
    if '--picky' in options or m.c.picky:  # Git-like  # line 537
        m.picky = True  # Git-like  # line 537
    elif '--track' in options or m.c.track:  # Svn-like  # line 538
        m.track = True  # Svn-like  # line 538
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 539
    if title:  # line 540
        printo(title)  # line 540
    if verbose:  # line 541
        info(MARKER + "Going offline...")  # line 541
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 542
    m.branch = 0  # line 543
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 544
    if verbose or '--verbose' in options:  # line 545
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 545
    info(MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 546

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 548
    ''' Finish working offline. '''  # line 549
    if verbose:  # line 550
        info(MARKER + "Going back online...")  # line 550
    force = '--force' in options  # type: bool  # line 551
    m = Metadata()  # type: Metadata  # line 552
    strict = '--strict' in options or m.strict  # type: bool  # line 553
    m.loadBranches()  # line 554
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 555
        Exit("There are still unsynchronized (modified) branches\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions.")  # line 555
    m.loadBranch(m.branch)  # line 556
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 557
    if options.count("--force") < 2:  # line 558
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 559
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 560
        if modified(changed):  # line 561
            Exit("File tree is modified vs. current branch\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 565
    try:  # line 566
        shutil.rmtree(encode(metaFolder))  # line 566
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 566
    except Exception as E:  # line 567
        Exit("Error removing offline repository.", exception=E)  # line 567
    info(MARKER + "Offline repository removed, you're back online")  # line 568

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 570
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not required here, as either branching from last revision anyway, or branching full file tree anyway.
  '''  # line 573
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 574
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 575
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 576
    m = Metadata()  # type: Metadata  # line 577
    m.loadBranch(m.branch)  # line 578
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 579
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 580
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 580
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 581
    if verbose:  # line 582
        info(MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 582
    if last:  # branch from last revision  # line 583
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 583
    else:  # branch from current file tree state  # line 584
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 584
    if not stay:  # line 585
        m.branch = branch  # line 585
    m.saveBranches()  # TODO #253 or indent again?  # line 586
    info(MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 587

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 589
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 590
    m = Metadata()  # type: Metadata  # line 591
    branch = None  # type: _coconut.typing.Optional[int]  # line 591
    revision = None  # type: _coconut.typing.Optional[int]  # line 591
    strict = '--strict' in options or m.strict  # type: bool  # line 592
    branch, revision = m.parseRevisionString(argument)  # line 593
    if branch is None or branch not in m.branches:  # line 594
        Exit("Unknown branch")  # line 594
    m.loadBranch(branch)  # knows commits  # line 595
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 596
    if verbose:  # line 597
        info(MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 597
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 598
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 599
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 604
    return changed  # returning for unit tests only TODO #254 remove?  # line 605

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False, classic: 'bool'=False):  # TODO #255 introduce option to diff against committed revision and not only file tree  # line 607
    ''' The diff display code. '''  # line 608
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 609
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 610
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 611
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 612
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 613
        content = b""  # type: _coconut.typing.Optional[bytes]  # stored state (old = "curr")  # line 614
        if pinfo.size != 0:  # versioned file  # line 615
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 615
            assert content is not None  # versioned file  # line 615
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current state (new = "into")  # line 616
        if classic:  # line 617
            mergeClassic(content, abspath, "b%d/r%02d" % (branch, revision), os.path.basename(abspath), pinfo.mtime, number_)  # line 617
            continue  # line 617
        blocks = None  # type: List[MergeBlock]  # line 618
        nl = None  # type: bytes  # line 618
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 619
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 620
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 621
        for block in blocks:  # line 622
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some of previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # line 625
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 626
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 626
            elif block.tipe == MergeBlockType.REMOVE:  # line 627
                for no, line in enumerate(block.lines):  # line 628
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 628
            elif block.tipe == MergeBlockType.REPLACE:  # line 629
                for no, line in enumerate(block.replaces.lines):  # line 630
                    printo(wrap("old %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 630
                for no, line in enumerate(block.lines):  # line 631
                    printo(wrap("now %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 631
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 634
                printo()  # line 634

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 636
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 637
    m = Metadata()  # type: Metadata  # line 638
    branch = None  # type: _coconut.typing.Optional[int]  # line 638
    revision = None  # type: _coconut.typing.Optional[int]  # line 638
    strict = '--strict' in options or m.strict  # type: bool  # line 639
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 640
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 641
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 642
    if branch is None or branch not in m.branches:  # line 643
        Exit("Unknown branch")  # line 643
    m.loadBranch(branch)  # knows commits  # line 644
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 645
    if verbose:  # line 646
        info(MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 646
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 647
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 648
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap, classic='--classic' in options)  # line 653

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 655
    ''' Create new revision from file tree changes vs. last commit. '''  # line 656
    m = Metadata()  # type: Metadata  # line 657
    if argument is not None and argument in m.tags:  # line 658
        Exit("Illegal commit message. It was already used as a (unique) tag name and cannot be reused")  # line 658
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 659
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 661
        Exit("No file patterns staged for commit in picky mode")  # line 661
    if verbose:  # line 662
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 662
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 663
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 664
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 665
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 666
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 667
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 668
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 669
    m.saveBranch(m.branch)  # line 670
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 671
    if m.picky:  # remove tracked patterns  # line 672
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 672
    else:  # track or simple mode: set branch modified  # line 673
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 673
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 674
        m.tags.append(argument)  # memorize unique tag  # line 674
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 674
    m.saveBranches()  # line 675
    stored = 0  # type: int  # now determine new commit size on file system  # line 676
    overhead = 0  # type: int  # now determine new commit size on file system  # line 676
    count = 0  # type: int  # now determine new commit size on file system  # line 676
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 677
    for file in os.listdir(commitFolder):  # line 678
        try:  # line 679
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 680
            if file == metaFile:  # line 681
                overhead += newsize  # line 681
            else:  # line 682
                stored += newsize  # line 682
                count += 1  # line 682
        except Exception as E:  # line 683
            error(E)  # line 683
    printo(MARKER_COLOR + "Created new revision r%02d%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%s%s%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, (" '%s'" % argument) if argument is not None else "", Fore.GREEN, Fore.RESET, len(changed.additions) - len(changed.moves), Fore.RED, Fore.RESET, len(changed.deletions) - len(changed.moves), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(changed.modifications), Fore.BLUE + Style.BRIGHT, MOVE_SYMBOL if m.c.useUnicodeFont else "#", Style.RESET_ALL, len(changed.moves), pure.siSize(stored + overhead), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 684

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 696
    ''' Show branches and current repository state. '''  # line 697
    m = Metadata()  # type: Metadata  # line 698
    if not (m.c.useChangesCommand or any((option.startswith('--repo') for option in options))):  # line 699
        changes(argument, options, onlys, excps)  # line 699
        return  # line 699
    current = m.branch  # type: int  # line 700
    strict = '--strict' in options or m.strict  # type: bool  # line 701
    printo(MARKER_COLOR + "Offline repository status")  # line 702
    printo("Repository root:     %s" % os.getcwd())  # line 703
    printo("Underlying VCS root: %s" % vcs)  # line 704
    printo("Underlying VCS type: %s" % cmd)  # line 705
    printo("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 706
    printo("Current SOS version: %s" % version.__version__)  # line 707
    printo("At creation version: %s" % m.version)  # line 708
    printo("Metadata format:     %s" % m.format)  # line 709
    printo("Content checking:    %s" % (Fore.CYAN + "size, then content" if m.strict else Fore.BLUE + "size & timestamp") + Fore.RESET)  # TODO size then timestamp?  # line 710
    printo("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 711
    printo("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 712
    printo("Number of branches:  %d" % len(m.branches))  # line 713
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 714
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 715
    m.loadBranch(current)  # line 716
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 717
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 718
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 718
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 719
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of unicode symbols for changed vs. unchanged  # line 724
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 728
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 729
        payload = 0  # type: int  # count used storage per branch  # line 730
        overhead = 0  # type: int  # count used storage per branch  # line 730
        original = 0  # type: int  # count used storage per branch  # line 730
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 731
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 732
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 733
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 733
                else:  # line 734
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 734
        pl_amount = float(payload) / MEBI  # type: float  # line 735
        oh_amount = float(overhead) / MEBI  # type: float  # line 735
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 737
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 738
            m.loadCommit(m.branch, commit_)  # line 739
            for pinfo in m.paths.values():  # line 740
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 740
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 741
        printo("  %s b%d%s @%s (%s%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), Fore.RESET, len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 742
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 753
        printo(Fore.GREEN + "Tracked" + Fore.RESET + " file patterns:")  # TODO #261 print matching untracking patterns side-by-side?  # line 754
        printo(ajoin(Fore.GREEN + "  | " + Fore.RESET, m.branches[m.branch].tracked, "\n"))  # line 755
        printo(Fore.RED + "Untracked" + Fore.RESET + " file patterns:")  # line 756
        printo(ajoin(Fore.RED + "  | " + Fore.RESET, m.branches[m.branch].untracked, "\n"))  # line 757

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 759
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 766
    assert not (check and commit)  # line 767
    m = Metadata()  # type: Metadata  # line 768
    force = '--force' in options  # type: bool  # line 769
    strict = '--strict' in options or m.strict  # type: bool  # line 770
    if argument is not None:  # line 771
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 772
        if branch is None:  # line 773
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 773
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 774
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 775

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 778
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 779
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 780
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 781
    if check and modified(changed) and not force:  # line 786
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 787
        Exit("File tree contains changes. Use --force to proceed")  # line 788
    elif commit:  # line 789
        if not modified(changed) and not force:  # line 790
            Exit("Nothing to commit")  # line 790
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 791
        if msg:  # line 792
            printo(msg)  # line 792

    if argument is not None:  # branch/revision specified  # line 794
        m.loadBranch(branch)  # knows commits of target branch  # line 795
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 796
        revision = m.correctNegativeIndexing(revision)  # line 797
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 798
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 799

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 801
    ''' Continue work on another branch, replacing file tree changes. '''  # line 802
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 803
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 804

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 807
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 808
    else:  # full file switch  # line 809
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 810
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 811

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 818
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 819
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 820
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 821
                rms.append(a)  # line 821
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 822
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 822
        if modified(changed) and not force:  # line 823
            m.listChanges(changed, cwd)  # line 823
            Exit("File tree contains changes. Use --force to proceed")  # line 823
        if verbose:  # line 824
            info(MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 824
        if not modified(todos):  # line 825
            info("No changes to current file tree")  # line 826
        else:  # integration required  # line 827
            for path, pinfo in todos.deletions.items():  # line 828
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 829
                printo("ADD " + path, color=Fore.GREEN)  # line 830
            for path, pinfo in todos.additions.items():  # line 831
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 832
                printo("DEL " + path, color=Fore.RED)  # line 833
            for path, pinfo in todos.modifications.items():  # line 834
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 835
                printo("MOD " + path, color=Fore.YELLOW)  # line 836
    m.branch = branch  # line 837
    m.saveBranches()  # store switched path info  # line 838
    info(MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 839

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 841
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 845
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 846
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 847
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 848
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 849
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 850
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 851
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 852
    if verbose:  # line 853
        info(MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 853

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 856
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 857
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 858
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 859
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 864
        if trackingUnion != trackingPatterns:  # nothing added  # line 865
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 866
        else:  # line 867
            info("Nothing to update")  # but write back updated branch info below  # line 868
    else:  # integration required  # line 869
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 870
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 870
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 870
        if changed.deletions.items():  # line 871
            printo("Additions:")  # line 871
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 872
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 873
            if add_all is None and mrg == MergeOperation.ASK:  # line 874
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 875
                if selection in "ao":  # line 876
                    add_all = "y" if selection == "a" else "n"  # line 876
                    selection = add_all  # line 876
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 877
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 877
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path, color=Fore.GREEN)  # TODO #268 document merge/update output, e.g. (A) as "selected not to add by user choice"  # line 878
        if changed.additions.items():  # line 879
            printo("Deletions:")  # line 879
        for path, pinfo in changed.additions.items():  # line 880
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 881
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 881
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 882
            if del_all is None and mrg == MergeOperation.ASK:  # line 883
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 884
                if selection in "ao":  # line 885
                    del_all = "y" if selection == "a" else "n"  # line 885
                    selection = del_all  # line 885
            if "y" in (del_all, selection):  # line 886
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 886
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path, color=Fore.RED)  # not contained in other branch, but maybe kept  # line 887
        if changed.modifications.items():  # line 888
            printo("Modifications:")  # line 888
        for path, pinfo in changed.modifications.items():  # line 889
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 890
            binary = not m.isTextType(path)  # type: bool  # line 891
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 892
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 893
                printo(("MOD " if not binary else "BIN ") + path, color=Fore.YELLOW)  # TODO print mtime, size differences?  # line 894
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 895
            if op == "t":  # line 896
                printo("THR " + path, color=Fore.MAGENTA)  # blockwise copy of contents  # line 897
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 897
            elif op == "m":  # line 898
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 899
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 899
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 900
                if current == file and verbose:  # line 901
                    info("No difference to versioned file")  # line 901
                elif file is not None:  # if None, error message was already logged  # line 902
                    merged = None  # type: bytes  # line 903
                    nl = None  # type: bytes  # line 903
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 904
                    if merged != current:  # line 905
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 906
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 906
                    elif verbose:  # TODO but update timestamp?  # line 907
                        info("No change")  # TODO but update timestamp?  # line 907
            else:  # mine or wrong input  # line 908
                printo("MNE " + path, color=Fore.CYAN)  # nothing to do! same as skip  # line 909
    info(MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 910
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 911
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 912
    m.saveBranches()  # line 913

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 915
    ''' Remove a branch entirely. '''  # line 916
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 917
    if len(m.branches) == 1:  # line 918
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 918
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 919
    if branch is None or branch not in m.branches:  # line 920
        Exit("Cannot delete unknown branch %r" % branch)  # line 920
    if verbose:  # line 921
        info(MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 921
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 922
    info(MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 923

def add(relPaths: '_coconut.typing.Sequence[str]', patterns: '_coconut.typing.Sequence[str]', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 925
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 926
    force = '--force' in options  # type: bool  # line 927
    m = Metadata()  # type: Metadata  # line 928
    if not (m.track or m.picky):  # line 929
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 930
    knownpatterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 931
    for relPath, pattern in zip(relPaths, patterns):  # line 932
        if pattern in knownpatterns:  # line 933
            Exit("Pattern '%s' already tracked" % pattern)  # line 934
        if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 935
            Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 936
        if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 937
            Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 938
        knownpatterns.append(pattern)  # line 939
    m.saveBranches()  # line 940
    info(MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # line 941

def remove(relPaths: '_coconut.typing.Sequence[str]', patterns: '_coconut.typing.Sequence[str]', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 943
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 944
    m = Metadata()  # type: Metadata  # line 945
    if not (m.track or m.picky):  # line 946
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' to start repository in tracking or picky mode")  # line 947
    knownpatterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 948
    for relPath, pattern in zip(relPaths, patterns):  # line 949
        if pattern not in knownpatterns:  # line 950
            suggestion = _coconut.set()  # type: Set[str]  # line 951
            for pat in knownpatterns:  # line 952
                if fnmatch.fnmatch(pattern, pat):  # line 952
                    suggestion.add(pat)  # line 952
            if suggestion:  # line 953
                printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # line 953
            Exit("Tracked pattern '%s' not found" % pattern)  # line 954
    knownpatterns.remove(pattern)  # line 955
    m.saveBranches()  # line 956
    info(MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 957

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 959
    ''' List specified directory, augmenting with repository metadata. '''  # line 960
    m = Metadata()  # type: Metadata  # line 961
    folder = (os.getcwd() if folder is None else folder)  # line 962
    if '--all' in options or '-a' in options:  # always start at SOS repo root with --all  # line 963
        folder = m.root  # always start at SOS repo root with --all  # line 963
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 964
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 965
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 966
    if verbose:  # line 967
        info(MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 967
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 968
    if relPath.startswith(os.pardir):  # line 969
        Exit("Cannot list contents of folder outside offline repository")  # line 969
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 970
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 971
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 972
        if len(m.tags) > 0:  # line 973
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 973
        return  # line 974
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 975
        if not recursive:  # avoid recursion  # line 976
            dirnames.clear()  # avoid recursion  # line 976
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 977
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 978

        folder = decode(dirpath)  # line 980
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 981
        if patterns:  # line 982
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 983
            if out:  # line 984
                printo("DIR %s\n" % relPath + out)  # line 984
            continue  # with next folder  # line 985
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 986
        if len(files) > 0:  # line 987
            printo("DIR %s" % relPath)  # line 987
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 988
            ignore = None  # type: _coconut.typing.Optional[str]  # line 989
            for ig in m.c.ignores:  # remember first match  # line 990
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 990
                    ignore = ig  # remember first match  # line 990
                    break  # remember first match  # line 990
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 991
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 991
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 991
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 991
                        break  # found a white list entry for ignored file, undo ignoring it  # line 991
            matches = []  # type: List[str]  # line 992
            if not ignore:  # line 993
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 994
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 995
                        matches.append(os.path.basename(pattern))  # line 995
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 996
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 997

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 999
    ''' List previous commits on current branch. '''  # line 1000
    changes_ = "--changes" in options  # type: bool  # line 1001
    diff_ = "--diff" in options  # type: bool  # line 1002
    m = Metadata()  # type: Metadata  # line 1003
    m.loadBranch(m.branch)  # knows commit history  # line 1004
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 1005
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 1006
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Offline commit history of branch %r" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 1007
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 1008
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 1009
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 1010
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 1011
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 1012
    commit = None  # type: CommitInfo  # used for reading parent branch information  # line 1012
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1013
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 1014
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 1015
    for no in range(maxi + 1):  # line 1016
        if indicator:  # line 1017
            printo("  %%s %%0%dd" % digits % ((lambda _coconut_none_coalesce_item: " " if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(indicator.getIndicator()), no), nl="\r")  # line 1017
        if no in m.commits:  # line 1018
            commit = m.commits[no]  # line 1018
        else:  # line 1019
            if n.branch != n.getParentBranch(m.branch, no):  # line 1020
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 1020
            commit = n.commits[no]  # line 1021
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 1022
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 1023
        if "--all" in options or no >= lastno:  # line 1024
            if no >= lastno:  # line 1025
                indicator = None  # line 1025
            _add = news - olds  # type: FrozenSet[str]  # line 1026
            _del = olds - news  # type: FrozenSet[str]  # line 1027
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 1029
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 1031
            printo("  %s r%s @%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%sT%s%02d) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, Fore.RESET, len(_add), Fore.RED, Fore.RESET, len(_del), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(_mod), Fore.CYAN, Fore.RESET, _txt, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 1032
            if changes_:  # line 1033
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}), root=cwd if '--relative' in options else None)  # TODO why using None here? to avoid stating files for performance reasons?  # line 1044
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 1045
                pass  #  _diff(m, changes)  # needs from revision diff  # line 1045
        olds = news  # replaces olds for next revision compare  # line 1046
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 1047

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 1049
    ''' Exported entire repository as archive for easy transfer. '''  # line 1050
    if verbose:  # line 1051
        info(MARKER + "Dumping repository to archive...")  # line 1051
    m = Metadata()  # type: Metadata  # to load the configuration  # line 1052
    progress = '--progress' in options  # type: bool  # line 1053
    delta = '--full' not in options  # type: bool  # line 1054
    skipBackup = '--skip-backup' in options  # type: bool  # line 1055
    import functools  # line 1056
    import locale  # line 1056
    import warnings  # line 1056
    import zipfile  # line 1056
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 1057
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 1057
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 1057
    except:  # line 1058
        compression = zipfile.ZIP_STORED  # line 1058

    if ("" if argument is None else argument) == "":  # line 1060
        Exit("Argument missing (target filename)")  # line 1060
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 1061
    entries = []  # type: List[str]  # line 1062
    if os.path.exists(encode(argument)) and not skipBackup:  # line 1063
        try:  # line 1064
            if verbose:  # line 1065
                info("Creating backup...")  # line 1065
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 1066
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 1067
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 1067
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 1067
        except Exception as E:  # line 1068
            Exit("Error creating backup copy before dumping. Please resolve and retry.", exception=E)  # line 1068
    if verbose:  # line 1069
        info("Dumping revisions...")  # line 1069
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1070
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1070
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1071
        _zip.debug = 0  # suppress debugging output  # line 1072
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1073
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1074
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1075
        totalsize = 0  # type: int  # line 1076
        start_time = time.time()  # type: float  # line 1077
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1078
            dirpath = decode(dirpath)  # line 1079
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1080
                continue  # don't backup backups  # line 1080
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1081
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1082
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1083
            for filename in filenames:  # line 1084
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1085
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1086
                totalsize += os.stat(encode(abspath)).st_size  # line 1087
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1088
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1089
                    continue  # don't backup backups  # line 1089
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1090
                    if show:  # line 1091
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1091
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1092
        if delta:  # line 1093
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1093
    info("\r" + pure.ljust(MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1094

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1096
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1097
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1098
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1099
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1099
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1100
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1101
    if maxi is None:  # line 1102
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1102
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1103
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1106
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1108
    while files:  # line 1109
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1110
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1111
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1113
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1113
    tracked = None  # type: bool  # line 1114
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1114
    tracked, commitArgs = vcsCommits[cmd]  # line 1114
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1115
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1117
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1117
    if tracked:  # line 1118
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1118

def config(arguments: 'List[_coconut.typing.Optional[str]]', options: 'List[str]'=[]):  # line 1120
    command = None  # type: str  # line 1121
    key = None  # type: str  # line 1121
    value = None  # type: str  # line 1121
    v = None  # type: str  # line 1121
    command, key, value = (arguments + [None] * 2)[:3]  # line 1122
    if command is None:  # line 1123
        usage.usage("help", verbose=True)  # line 1123
    if command not in ("set", "unset", "show", "list", "add", "rm"):  # line 1124
        Exit("Unknown config command %r" % command)  # line 1124
    local = "--local" in options  # type: bool  # line 1125
    m = Metadata()  # type: Metadata  # loads nested configuration (local - global - defaults)  # line 1126
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1127
    if command == "set":  # line 1128
        if None in (key, value):  # line 1129
            Exit("Key or value not specified")  # line 1129
        if key not in ((([] if local else ONLY_GLOBAL_FLAGS) + CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1130
            Exit("Unsupported key for %s configuration %r" % ("local" if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1130
        if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1131
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1131
        c[key] = value.lower() in TRUTH_VALUES if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1132
    elif command == "unset":  # line 1133
        if key is None:  # line 1134
            Exit("No key specified")  # line 1134
        if key not in c.keys(with_nested=False):  # line 1135
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, "local" if local else "global"))  # line 1136
        del c[key]  # line 1137
    elif command == "add":  # TODO copy list from defaults if not local/global  # line 1138
        if None in (key, value):  # line 1139
            Exit("Key or value not specified")  # line 1139
        if key not in CONFIGURABLE_LISTS:  # line 1140
            Exit("Unsupported key %r for list addition" % key)  # line 1140
        if key not in c.keys():  # prepare empty list, or copy from underlying, add new value below TODO also allow one more level of underlying?  # line 1141
            c[key] = [_ for _ in c.__defaults[key]] if key in c.__defaults[key] else []  # prepare empty list, or copy from underlying, add new value below TODO also allow one more level of underlying?  # line 1141
        elif value in c[key]:  # line 1142
            Exit("Value already contained, nothing to do")  # line 1142
        if ";" not in value:  # line 1143
            c[key].append(removePath(key, value.strip()))  # line 1143
        else:  # line 1144
            c[key].extend([removePath(key, v) for v in safeSplit(value, ";")])  # line 1144
    elif command == "rm":  # line 1145
        if None in (key, value):  # line 1146
            Exit("Key or value not specified")  # line 1146
        if key not in c.keys(with_nested=False):  # line 1147
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, "local" if local else "global"))  # line 1148
        if value not in c[key]:  # line 1149
            Exit("Unknown value %r" % value)  # line 1149
        c[key].remove(value)  # line 1150
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1151
            del c[key]  # remove local entry, to fallback to global  # line 1151
    else:  # Show or list  # line 1152
        if key == "ints":  # list valid configuration items  # line 1153
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1153
        elif key == "flags":  # line 1154
            printo(", ".join(ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS))  # line 1154
        elif key == "lists":  # line 1155
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1155
        elif key == "texts":  # line 1156
            printo(", ".join([_ for _ in defaults.keys() if _ not in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS + CONFIGURABLE_INTS + CONFIGURABLE_LISTS)]))  # line 1156
        else:  # no key: list all  # line 1157
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1158
            c = m.c  # always use full configuration chain  # line 1159
            try:  # attempt single key  # line 1160
                assert key is not None  # force exception if no key specified  # line 1161
                c[key]  # force exception if no key specified  # line 1161
                l = key in c.keys(with_nested=False)  # type: bool  # line 1162
                g = key in c.__defaults.keys(with_nested=False)  # type: bool  # line 1162
                printo(key.rjust(20), color=Fore.WHITE, nl="")  # line 1163
                printo(" " + (out[3] if not (l or g) else (out[1] if l else out[2])) + " ", color=Fore.CYAN, nl="")  # line 1164
                printo(repr(c[key]))  # line 1165
            except:  # normal value listing  # line 1166
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # copy-by-value  # line 1167
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1168
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1169
                for k, vt in sorted(vals.items()):  # line 1170
                    printo(k.rjust(20), color=Fore.WHITE, nl="")  # line 1171
                    printo(" " + out[vt[1]] + " ", color=Fore.CYAN, nl="")  # line 1172
                    printo(vt[0])  # line 1173
                if len(c.keys()) == 0:  # line 1174
                    info("No local configuration stored.")  # line 1174
                if len(c.__defaults.keys()) == 0:  # line 1175
                    info("No global configuration stored.")  # line 1175
        return  # in case of list, no need to store anything  # line 1176
    if local:  # saves changes of repoConfig  # line 1177
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1177
        m.saveBranches()  # saves changes of repoConfig  # line 1177
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1177
    else:  # global config  # line 1178
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1179
        if f is None:  # line 1180
            Exit("Error saving user configuration: %r" % h)  # line 1180

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1182
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1185
    if verbose:  # line 1186
        info(MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1186
    force = '--force' in options  # type: bool  # line 1187
    soft = '--soft' in options  # type: bool  # line 1188
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1189
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1189
    m = Metadata()  # type: Metadata  # line 1190
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1191
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1192
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1193
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1194
    if not matching and not force:  # line 1195
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1195
    if not (m.track or m.picky):  # line 1196
        Exit("Repository is in simple mode. Use basic file operations to modify files, then execute 'sos commit' to version any changes")  # line 1196
    if pattern not in patterns:  # list potential alternatives and exit  # line 1197
        for tracked in (t for t in patterns if t[:t.rindex(SLASH)] == relPath):  # for all patterns of the same source folder HINT was os.path.dirpath before  # line 1198
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1199
            if alternative:  # line 1200
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1200
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: "if not (force or soft):""  # line 1201
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1202
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1203
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1204
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1208
#  oldTokens:GlobBlock[]?; newToken:GlobBlock[]?  # TODO remove optional?, only here to satisfy mypy
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1210
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1211
    if len({st[1] for st in matches}) != len(matches):  # line 1212
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1212
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1213
    if os.path.exists(encode(newRelPath)):  # line 1214
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1215
        if exists and not (force or soft):  # line 1216
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1216
    else:  # line 1217
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1217
    if not soft:  # perform actual renaming  # line 1218
        for (source, target) in matches:  # line 1219
            try:  # line 1220
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1220
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1221
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1221
    patterns[patterns.index(pattern)] = newPattern  # line 1222
    m.saveBranches()  # line 1223

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1225
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1226
    debug("Parsing command-line arguments...")  # line 1227
    root = os.getcwd()  # line 1228
    try:  # line 1229
        onlys, excps, remotes = parseArgumentOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1230
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1231
        arguments = [c.strip() for c in sys.argv[2:] if not ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # line 1232
        options = [c.strip() for c in sys.argv[2:] if ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # options *with* arguments have to be parsed directly from sys.argv inside using functions  # line 1233
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1234
        if command[:1] in "amr":  # line 1235
            try:  # line 1236
                relPaths, patterns = unzip([relativize(root, os.path.join(cwd, argument)) for argument in ((["."] if arguments is None else arguments))])  # line 1236
            except:  # line 1237
                command = "ls"  # convert command into ls --patterns  # line 1238
                arguments[0] = None  # convert command into ls --patterns  # line 1238
                options.extend(["--patterns", "--all"])  # convert command into ls --patterns  # line 1238
# Exit("Need one or more file patterns as argument (escape them according to your shell)")
        if command[:1] == "m":  # line 1240
            if len(arguments) < 2:  # line 1241
                Exit("Need a second file pattern argument as target for move command")  # line 1241
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1242
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1243
        if command == "raise":  # line 1244
            raise Exception("provoked exception")  # line 1244
        elif command[:1] == "a":  # e.g. addnot  # line 1245
            add(relPaths, patterns, options, negative="n" in command)  # e.g. addnot  # line 1245
        elif command[:1] == "b":  # line 1246
            branch(arguments[0], arguments[1], options)  # line 1246
        elif command[:3] == "com":  # line 1247
            commit(arguments[0], options, onlys, excps)  # line 1247
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1248
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1248
        elif command[:2] == "ci":  # line 1249
            commit(arguments[0], options, onlys, excps)  # line 1249
        elif command[:3] == 'con':  # line 1250
            config(arguments, options)  # line 1250
        elif command[:2] == "de":  # line 1251
            destroy((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1251
        elif command[:2] == "di":  # TODO no consistent handling of single dash/characters argument-options  # line 1252
            diff((lambda _coconut_none_coalesce_item: "/" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[2 if arguments[0] == '-n' else 0]), options, onlys, excps)  # TODO no consistent handling of single dash/characters argument-options  # line 1252
        elif command[:2] == "du":  # line 1253
            dump((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1253
        elif command[:1] == "h":  # line 1254
            usage.usage(arguments[0], verbose=verbose)  # line 1254
        elif command[:2] == "lo":  # line 1255
            log(options, cwd)  # line 1255
        elif command[:2] == "li":  # line 1256
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1256
        elif command[:2] == "ls":  # line 1257
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1257
        elif command[:1] == "m":  # e.g. mvnot  # line 1258
            move(relPaths[0], patterns[0], newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1258
        elif command[:2] == "of":  # line 1259
            offline(arguments[0], arguments[1], options, remotes)  # line 1259
        elif command[:2] == "on":  # line 1260
            online(options)  # line 1260
        elif command[:1] == "p":  # line 1261
            publish(arguments[0], cmd, options, onlys, excps)  # line 1261
        elif command[:1] == "r":  # e.g. rmnot  # line 1262
            remove(relPaths, patterns, options, negative="n" in command)  # e.g. rmnot  # line 1262
        elif command[:2] == "st":  # line 1263
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1263
        elif command[:2] == "sw":  # line 1264
            switch((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps, cwd)  # line 1264
        elif command[:1] == "u":  # line 1265
            update((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps)  # line 1265
        elif command[:1] == "v":  # line 1266
            usage.usage(arguments[0], version=True)  # line 1266
        else:  # line 1267
            Exit("Unknown command '%s'" % command)  # line 1267
        Exit(code=0)  # regular exit  # line 1268
    except (Exception, RuntimeError) as E:  # line 1269
        Exit("An internal error occurred in SOS\nPlease report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.", exception=E)  # line 1270

def main():  # line 1272
    global debug, info, warn, error  # to modify logger  # line 1273
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1274
    _log = Logger(logging.getLogger(__name__))  # line 1275
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1275
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1276
        sys.argv.remove(option)  # clean up program arguments  # line 1276
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1277
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1277
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1278
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1279
    debug("Detected SOS root folder: %s" % (("-" if root is None else root)))  # line 1280
    debug("Detected VCS root folder: %s" % (("-" if vcs is None else vcs)))  # line 1281
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1282
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1283
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv"):  # in offline mode or just going offline  # line 1284
        cwd = os.getcwd()  # line 1285
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1286
        parse(vcs, cwd, cmd)  # line 1287
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1288
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1289
        import subprocess  # only required in this section  # line 1290
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1291
        inp = ""  # type: str  # line 1292
        while True:  # line 1293
            so, se = process.communicate(input=inp)  # line 1294
            if process.returncode is not None:  # line 1295
                break  # line 1295
            inp = sys.stdin.read()  # line 1296
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1297
            if root is None:  # line 1298
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1298
            m = Metadata(root)  # type: Metadata  # line 1299
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1300
            m.saveBranches()  # line 1301
    else:  # line 1302
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1302


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: List[None]  # this is a trick allowing to modify the module-level flags from the test suite  # line 1306
force_vcs = [None] if '--vcs' in sys.argv else []  # type: List[None]  # line 1307
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1308

_log = Logger(logging.getLogger(__name__))  # line 1310
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1310

if __name__ == '__main__':  # line 1312
    main()  # line 1312
