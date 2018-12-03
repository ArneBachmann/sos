#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x7b5b23f2

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
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 74

    def correctNegativeIndexing(_, revision: 'int') -> 'int':  # line 76
        ''' As the na_e says, this deter_ines the correct positive revision nu_ber for negative indexing (-1 being last, -2 being second last). '''  # line 77
        revision = revision if revision >= 0 else (max(_.commits) if _.commits else ((lambda _coconut_none_coalesce_item: -1 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.getHighestRevision(_.branch)))) + 1 + revision  # negative indexing  # line 78
        if revision < 0 or (_.commits and revision > max(_.commits)):  # line 79
            Exit("Unknown revision r%02d" % revision)  # line 79
        return revision  # line 80

    def listChanges(_, changed: 'ChangeSet', commitTime: '_coconut.typing.Optional[float]'=None, root: '_coconut.typing.Optional[str]'=None):  # line 82
        ''' List changes. If commitTime (in ms) is defined, also check timestamps of modified files for plausibility (if mtime of new file is <= / older than in last commit, note so).
        commitTimne == None in switch and log
        root: current user's working dir to compute relative paths (cwd is usually repository root), otherwise None (repo-relative)
    '''  # line 86
        relp = lambda path, root: os.path.relpath(path, root).replace(SLASH, os.sep) if root else path  # type: _coconut.typing.Callable[[str, str], str]  # using relative paths if root is not None, otherwise SOS repo normalized paths  # line 87
        moves = dict(changed.moves.values())  # type: Dict[str, PathInfo]  # of origin-pathinfo  # line 88
        realadditions = {k: v for k, v in changed.additions.items() if k not in changed.moves}  # type: Dict[str, PathInfo]  # targets  # line 89
        realdeletions = {k: v for k, v in changed.deletions.items() if k not in moves}  # type: Dict[str, PathInfo]  # sources  # line 90
        if len(changed.moves) > 0:  # line 91
            printo(ajoin("MOV ", ["%s  <-  %s" % (relp(path, root), relp(dpath, root)) for path, (dpath, dinfo) in sorted(changed.moves.items())], "\n") + Style.RESET_ALL, color=Fore.BLUE + Style.BRIGHT)  # line 91
        if len(realadditions) > 0:  # line 92
            printo(ajoin("ADD ", sorted(["%s  (%s)" % (relp(p, root), pure.siSize(pinfo.size) if pinfo is not None else "-") for p, pinfo in realadditions.items()]), "\n"), color=Fore.GREEN)  # line 92
        if len(realdeletions) > 0:  # line 93
            printo(ajoin("DEL ", sorted([relp(p, root) for p in realdeletions.keys()]), "\n"), color=Fore.RED)  # line 93
        if len(changed.modifications) > 0:  # line 94
            printo(ajoin("MOD ", [relp(m, root) + (" <binary>" if not _.isTextType(os.path.basename(m)) else "") + ("" if commitTime is None else (" <older than previously committed>" if pi.mtime < _.paths[m].mtime else "")) + ((" [%s%s %s%s]" % (pure.signedNumber(pi.size - _.paths[m].size), siSize(pi.size - _.paths[m].size), pure.signedNumber(pi.mtime - _.paths[m].mtime), pure.timeString(pi.mtime - _.paths[m].mtime)) if verbose else "") if pi is not None else "") for (m, pi) in sorted(changed.modifications.items())], "\n"), color=Fore.YELLOW)  # line 94

    def loadBranches(_, offline: 'bool'=False, remotes: 'List[str]'=[]):  # line 96
        ''' Load list of branches and current branch info from metadata file. offline = True command avoids message. '''  # line 97
        try:  # fails if not yet created (on initial branch/commit)  # line 98
#      branches:List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 100
                repo, branches, config = json.load(fd)  # line 101
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 102
            _.branch = repo["branch"]  # current branch integer  # line 103
            _.track, _.picky, _.strict, _.compress, _.version, _.format, _.remotes, remote = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format", "remotes", "remote"]]  # line 104
            if remote:  # line 105
                Exit("Cannot access remote SOS repository for local operation. You're attempting to access a backup copy. Consult manual to restore this backup for normal operation")  # line 105
            upgraded = []  # type: List[str]  # line 106
            if _.version is None:  # line 107
                _.version = "0 - pre-1.2"  # line 108
                upgraded.append("pre-1.2")  # line 109
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 110
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 111
                upgraded.append("2018.1210.3028")  # line 112
            if _.format is None:  # must be before 1.3.5+  # line 113
                _.format = 1  # marker for first metadata file format  # line 114
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 115
                upgraded.append("1.3.5")  # line 116
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 117
            _.repoConf = config  # local configuration stored with repository, not in user-wide configuration  # line 118
            if _.format == 1 or _.remotes is None:  # before remotes  # line 119
                _.format = METADATA_FORMAT  # line 120
                _.remotes = []  # default is no remotes  # line 121
                upgraded.append("1.7.0")  # remote URLs introduced  # line 122
            if upgraded:  # line 123
                for upgrade in upgraded:  # line 124
                    printo("WARNING  Upgraded repository metadata to match SOS version %r" % upgrade, color=Fore.YELLOW)  # line 124
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 125
                _.saveBranches()  # line 126
        except Exception as E:  # if not found, create metadata folder with default values  # line 127
            _.branches = {}  # line 128
            _.track, _.picky, _.strict, _.compress, _.version, _.remotes, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, remotes, METADATA_FORMAT]  # line 129
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # hide warning only when going offline  # line 130

    def _saveBranches(_, remote: '_coconut.typing.Optional[str]', data: 'Dikt[str, Any]'):  # line 132
        tryOrIgnore(lambda: shutil.copy2(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), encode(os.path.join((_.root if remote is None else remote), metaFolder, metaBack))))  # backup  # line 133
        try:  # line 134
            with codecs.open(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 134
                json.dump((data, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints (instead of ascii encoding), the file descriptor knows how to encode them  # line 135
        except Exception as E:  # line 136
            debug("Error saving branches%s" % ((" to remote path " + remote) if remote else ""))  # line 136

    def saveBranches(_, also: 'Dict[str, Any]'={}):  # line 138
        ''' Save list of branches and current branch info to metadata file. '''  # line 139
        store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT, "remotes": _.remotes, "remote": False}  # type: Dict[str, Any]  # dictionary of repository settings (while _.repoConf stores user settings)  # line 140
        store.update(also)  # allows overriding certain values at certain points in time  # line 146
        for remote in [None] + _.remotes:  # line 147
            _._saveBranches(remote, store)  # mark remote copies as read-only  # line 148
            store["remote"] = True  # mark remote copies as read-only  # line 148

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 150
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 151
        if name == "":  # line 152
            return -1  # line 152
        try:  # attempt to parse integer string  # line 153
            return int(name)  # attempt to parse integer string  # line 153
        except ValueError:  # line 154
            pass  # line 154
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 155
        return found[0] if found else None  # line 156

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 158
        ''' Convenience accessor for named branches. '''  # line 159
        if name == "":  # current  # line 160
            return _.branch  # current  # line 160
        try:  # attempt to parse integer string  # line 161
            return int(name)  # attempt to parse integer string  # line 161
        except ValueError:  # line 162
            pass  # line 162
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 163
        return found[0] if found else None  # line 164

    def loadBranch(_, branch: 'int'):  # line 166
        ''' Load all commit information from a branch meta data file. '''  # line 167
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 168
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 169
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 170
        _.branch = branch  # line 171

    def saveBranch(_, branch: 'int'):  # line 173
        ''' Save all commits to a branch meta data file. '''  # line 174
        for remote in [None] + _.remotes:  # line 175
            tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile, base=remote)), encode(branchFolder(branch, file=metaBack, base=remote))))  # backup  # line 176
            try:  # line 177
                with codecs.open(encode(branchFolder(branch, file=metaFile, base=remote)), "w", encoding=UTF8) as fd:  # line 177
                    json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 178
            except Exception as E:  # line 179
                debug("Error saving branch%s" % ((" to remote path " + remote) if remote else ""))  # line 179

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 181
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 189
        if verbose:  # line 190
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 190
        now = int(time.time() * 1000)  # type: int  # line 191
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 192
        revision = max(_.commits) if _.commits else 0  # type: int  # line 193
        _.commits.clear()  # line 194
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 195
        for remote in [None] + _.remotes:  # line 200
            tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)) if full else branchFolder(branch, base=(_.root if remote is None else remote)))), lambda e: error("Duplicating remote branch folder %r" % remote))  # line 201
        if full:  # not fast branching via reference - copy all current files to new branch  # line 202
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 203
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 204
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 204
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit  # line 205
            _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 206
        _.saveBranch(branch)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 207
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 208

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 210
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 216
        now = int(time.time() * 1000)  # type: int  # line 217
        simpleMode = not (_.track or _.picky)  # line 218
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 219
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 220
        if verbose:  # line 221
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 221
        _.paths = {}  # type: Dict[str, PathInfo]  # line 222
        if simpleMode:  # branches from file system state. not necessary to create branch folder, as it is done in findChanges below anyway  # line 223
            changed, msg = _.findChanges(branch, 0, progress=simpleMode)  # HINT creates revision folder and versioned files!  # line 224
            _.listChanges(changed)  # line 225
            if msg:  # display compression factor and time taken  # line 226
                printo(msg)  # display compression factor and time taken  # line 226
            _.paths.update(changed.additions.items())  # line 227
        else:  # tracking or picky mode: branch from latest revision  # line 228
            for remote in [None] + _.remotes:  # line 229
                tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)))), lambda e: error("Creating remote branch folder %r" % remote))  # line 230
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 231
                _.loadBranch(_.branch)  # line 232
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO #245 what if last switch was to an earlier revision? no persisting of last checkout  # line 233
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 234
                for path, pinfo in _.paths.items():  # line 235
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 235
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 236
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 237
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 238
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 239

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 241
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 244
        import collections  # used almost only here  # line 245
        binfo = None  # type: BranchInfo  # typing info  # line 246
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 247
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 248
        if deps:  # need to copy all parent revisions to dependent branches first  # line 249
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 250
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 251
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 252
                for dep, _rev in deps:  # line 253
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO #246 align placement of indicator with other uses of progress  # line 254
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 255
#          if rev in _.commits:  # TODO #247 uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 257
                    shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 258
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 259
                for rev in range(minrev + 1, _rev + 1):  # line 260
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 261
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 262
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 263
                        newcommits[dep][rev] = _.commits[rev]  # line 264
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 265
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 266
        printo(pure.ljust() + "\r")  # clean line output  # line 267
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 268
        tryOrIgnore(lambda: os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?"))  # line 269
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 270
        del _.branches[branch]  # line 271
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 272
        _.saveBranches()  # persist modified branches list  # line 273
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 274
            _.commits = commits  # line 275
            _.saveBranch(branch)  # line 276
        _.commits.clear()  # clean memory  # line 277
        return binfo  # line 278

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 280
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 281
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 282
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 283
            _.paths = json.load(fd)  # line 283
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 284
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 285

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 287
        ''' Save all file information to a commit meta data file. '''  # line 288
        for remote in [None] + _.remotes:  # line 289
            try:  # line 290
                target = revisionFolder(branch, revision, base=(_.root if remote is None else remote))  # type: str  # line 291
                tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 292
                tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 293
                with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 294
                    json.dump(_.paths, fd, ensure_ascii=False)  # line 294
            except Exception as E:  # line 295
                debug("Error saving commit%s" % ((" to remote path " + remote) if remote else ""))  # line 295

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 297
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly!)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 306
        import collections  # used almost only here  # line 307
        write = branch is not None and revision is not None  # used for writing commits  # line 308
        if write:  # line 309
            for remote in [None] + _.remotes:  # line 309
                tryOrIgnore(lambda: os.makedirs(encode(revisionFolder(branch, revision, base=(_.root if remote is None else remote)))))  # line 310
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # WARN this code needs explicity argument passing for initialization due to mypy problems with default arguments  # line 311
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 312
        hashed = None  # type: _coconut.typing.Optional[str]  # line 313
        written = None  # type: int  # line 313
        compressed = 0  # type: int  # line 313
        original = 0  # type: int  # line 313
        start_time = time.time()  # type: float  # line 313
        knownPaths = {}  # type: Dict[str, List[str]]  # line 314

# Find relevant folders/files that match specified folder/glob patterns for exclusive inclusion or exclusion
        byFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 317
        onlyByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 318
        dontByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 319
        for path, pinfo in _.paths.items():  # line 320
            if pinfo is None:  # quicker than generator expression above  # line 321
                continue  # quicker than generator expression above  # line 321
            slash = path.rindex(SLASH)  # type: int  # line 322
            byFolder[path[:slash]].append(path[slash + 1:])  # line 323
        for pattern in ([] if considerOnly is None else considerOnly):  # line 324
            slash = pattern.rindex(SLASH)  # line 324
            onlyByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 324
        for pattern in ([] if dontConsider is None else dontConsider):  # line 325
            slash = pattern.rindex(SLASH)  # line 325
            dontByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 325
        for folder, paths in byFolder.items():  # line 326
            pos = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in onlyByFolder.get(folder, [])]) if considerOnly is not None else set(paths)  # type: Set[str]  # line 327
            neg = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in dontByFolder.get(folder, [])]) if dontConsider is not None else set()  # type: Set[str]  # line 328
            knownPaths[folder] = list(pos - neg)  # line 329

        for path, dirnames, filenames in os.walk(_.root):  # line 331
            path = decode(path)  # line 332
            dirnames[:] = [decode(d) for d in dirnames]  # line 333
            filenames[:] = [decode(f) for f in filenames]  # line 334
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 335
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 336
            dirnames.sort()  # line 337
            filenames.sort()  # line 337
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 338
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 339
            if dontConsider:  # line 340
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 341
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 342
                filename = relPath + SLASH + file  # line 343
                filepath = os.path.join(path, file)  # line 344
                try:  # line 345
                    stat = os.stat(encode(filepath))  # line 345
                except Exception as E:  # line 346
                    exception(E)  # line 346
                    continue  # line 346
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 347
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 348
                if show:  # indication character returned  # line 349
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 350
                    printo(pure.ljust(outstring), nl="")  # line 351
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 352
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 353
                    nameHash = hashStr(filename)  # line 354
                    try:  # line 355
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=nameHash) for remote in [None] + _.remotes] if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 356
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 357
                        compressed += written  # line 358
                        original += size  # line 358
                    except PermissionError as E:  # line 359
                        error("File permission error for %s" % filepath)  # line 359
                    except Exception as F:  # HINT e.g. FileNotFoundError will not add to additions  # line 360
                        exception(F)  # HINT e.g. FileNotFoundError will not add to additions  # line 360
                    continue  # with next file  # line 361
                last = _.paths[filename]  # filename is known - check for modifications  # line 362
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 363
                    try:  # line 364
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 365
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 366
                        continue  # line 366
                        compressed += written  # line 367
                        original += last.size if inverse else size  # line 367
                    except Exception as E:  # line 368
                        exception(E)  # line 368
                elif (size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False))):  # detected a modification TODO invert error = False?  # line 369
                    try:  # line 373
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else hashFile(filepath, _.compress, symbols=progressSymbols, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl=""))[0], 0)  # line 374
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 378
                        compressed += written  # line 379
                        original += last.size if inverse else size  # line 379
                    except Exception as E:  # line 380
                        exception(E)  # line 380
                else:  # with next file  # line 381
                    continue  # with next file  # line 381
            if relPath in knownPaths:  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 382
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 382
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 383
            for file in names:  # line 384
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 385
                    continue  # don't mark ignored files as deleted  # line 385
                pth = path + SLASH + file  # type: str  # line 386
                changed.deletions[pth] = _.paths[pth]  # line 387
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, _.strict))  # line 388
        if progress:  # forces clean line of progress output  # line 389
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 389
        elif verbose:  # line 390
            info("Finished detecting changes")  # line 390
        tt = time.time() - start_time  # type: float  # line 391
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # in KiBi  # line 392
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 393
        msg = (msg + " | " if msg else "") + ("Processing speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 394
        return (changed, msg if msg else None)  # line 395

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 397
        ''' Returns nothing, just updates _.paths in place. '''  # line 398
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 399

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 401
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 402
        try:  # load initial paths  # line 403
            _.loadCommit(branch, startwith)  # load initial paths  # line 403
        except:  # no revisions  # line 404
            yield {}  # no revisions  # line 404
            return None  # no revisions  # line 404
        if incrementally:  # line 405
            yield _.paths  # line 405
        m = Metadata(_.root)  # type: Metadata  # next changes TODO #250 avoid loading all metadata and config  # line 406
        rev = None  # type: int  # next changes TODO #250 avoid loading all metadata and config  # line 406
        for rev in range(startwith + 1, revision + 1):  # line 407
            m.loadCommit(branch, rev)  # line 408
            for p, info in m.paths.items():  # line 409
                if info.size == None:  # line 410
                    del _.paths[p]  # line 410
                else:  # line 411
                    _.paths[p] = info  # line 411
            if incrementally:  # line 412
                yield _.paths  # line 412
        yield None  # for the default case - not incrementally  # line 413

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 415
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 416
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 417

    def parseRevisionString(_, argument: 'str') -> 'Union[Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]], NoReturn]':  # line 419
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
        None is returned in case of error
        Code will sys.exit in case of unknown specified branch/revision
    '''  # line 424
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 425
            return (_.branch, -1)  # no branch/revision specified  # line 425
        if argument == "":  # nothing specified by user, raise error in caller  # line 426
            return (None, None)  # nothing specified by user, raise error in caller  # line 426
        argument = argument.strip()  # line 427
        if argument.startswith(SLASH):  # current branch  # line 428
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 428
        if argument.endswith(SLASH):  # line 429
            try:  # line 430
                return (_.getBranchByName(argument[:-1]), -1)  # line 430
            except ValueError:  # line 431
                Exit("Unknown branch label '%s'" % argument)  # line 431
        if SLASH in argument:  # line 432
            b, r = argument.split(SLASH)[:2]  # line 433
            try:  # line 434
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 434
            except ValueError:  # line 435
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 435
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 436
        if branch not in _.branches:  # line 437
            branch = None  # line 437
        try:  # either branch name/number or reverse/absolute revision number  # line 438
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 438
        except:  # line 439
            Exit("Unknown branch label or wrong number format")  # line 439
        Exit("This should never happen. Please create an issue report")  # line 440

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 442
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 444
        while True:  # line 445
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 446
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 447
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 448
                break  # line 448
            revision -= 1  # line 449
            if revision < 0:  # line 450
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 450
        return revision, source  # line 451

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 453
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 454
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 455
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 456
            return [branch]  # found. need to load commit from other branch instead  # line 456
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 457
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 457
        return others  # line 458

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 460
        return _.getParentBranches(branch, revision)[-1]  # line 460

    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 462
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 463
        m = Metadata()  # type: Metadata  # line 464
        other = branch  # type: _coconut.typing.Optional[int]  # line 465
        while other is not None:  # line 466
            m.loadBranch(other)  # line 467
            if m.commits:  # line 468
                return max(m.commits)  # line 468
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 469
        return None  # line 470

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 472
        ''' Copy versioned file to other branch/revision. '''  # line 473
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 474
        for remote in [None] + _.remotes:  # line 475
            try:  # line 476
                target = revisionFolder(toBranch, toRevision, file=pinfo.nameHash, base=(_.root if remote is None else remote))  # type: str  # line 477
                shutil.copy2(encode(source), encode(target))  # line 478
            except Exception as E:  # line 479
                error("Copying versioned file%s" % ((" to remote path " % remote) if remote else ""))  # line 479

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 481
        ''' Return file contents, or copy contents into file path provided (used in update and restorefile). '''  # line 482
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 483
        try:  # line 484
            with openIt(source, "r", _.compress) as fd:  # line 484
                if toFile is None:  # read bytes into memory and return  # line 485
                    return fd.read()  # read bytes into memory and return  # line 485
                with open(encode(toFile), "wb") as to:  # line 486
                    while True:  # line 487
                        buffer = fd.read(bufSize)  # line 488
                        to.write(buffer)  # line 489
                        if len(buffer) < bufSize:  # line 490
                            break  # line 490
                    return None  # line 491
        except Exception as E:  # line 492
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 492
        None  # line 493

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 495
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 496
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 497
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 497
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 498
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 499
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 500
        if pinfo.size == 0:  # line 501
            with open(encode(target), "wb"):  # line 502
                pass  # line 502
            try:  # update access/modification timestamps on file system  # line 503
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 503
            except Exception as E:  # line 504
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 504
            return None  # line 505
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 506
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 508
            while True:  # line 509
                buffer = fd.read(bufSize)  # line 510
                to.write(buffer)  # line 511
                if len(buffer) < bufSize:  # line 512
                    break  # line 512
        try:  # update access/modification timestamps on file system  # line 513
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 513
        except Exception as E:  # line 514
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 514
        return None  # line 515


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], remotes: 'List[str]'=[]):  # line 519
    ''' Initial command to start working offline. '''  # line 520
    if os.path.exists(encode(metaFolder)):  # line 521
        if '--force' not in options:  # line 522
            Exit("Repository folder is either already offline or older branches and commits were left over\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 522
        try:  # throw away all previous metadata before going offline  # line 523
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 524
                resource = metaFolder + os.sep + entry  # line 525
                if os.path.isdir(resource):  # line 526
                    shutil.rmtree(encode(resource))  # line 526
                else:  # line 527
                    os.unlink(encode(resource))  # line 527
        except:  # line 528
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder)  # line 528
    for remote in remotes:  # line 529
        try:  # line 530
            os.makedirs(os.path.join(remote, metaFolder))  # line 530
        except Exception as E:  # line 531
            error("Creating remote repository metadata in %s" % remote)  # line 531
    m = Metadata(offline=True, remotes=remotes)  # type: Metadata  # line 532
    if '--strict' in options or m.c.strict:  # always hash contents  # line 533
        m.strict = True  # always hash contents  # line 533
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 534
        m.compress = True  # plain file copies instead of compressed ones  # line 534
    if '--picky' in options or m.c.picky:  # Git-like  # line 535
        m.picky = True  # Git-like  # line 535
    elif '--track' in options or m.c.track:  # Svn-like  # line 536
        m.track = True  # Svn-like  # line 536
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 537
    if title:  # line 538
        printo(title)  # line 538
    if verbose:  # line 539
        info(MARKER + "Going offline...")  # line 539
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 540
    m.branch = 0  # line 541
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 542
    if verbose or '--verbose' in options:  # line 543
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 543
    info(MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 544

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 546
    ''' Finish working offline. '''  # line 547
    if verbose:  # line 548
        info(MARKER + "Going back online...")  # line 548
    force = '--force' in options  # type: bool  # line 549
    m = Metadata()  # type: Metadata  # line 550
    strict = '--strict' in options or m.strict  # type: bool  # line 551
    m.loadBranches()  # line 552
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 553
        Exit("There are still unsynchronized (modified) branches\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions.")  # line 553
    m.loadBranch(m.branch)  # line 554
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 555
    if options.count("--force") < 2:  # line 556
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 557
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 558
        if modified(changed):  # line 559
            Exit("File tree is modified vs. current branch\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 563
    try:  # line 564
        shutil.rmtree(encode(metaFolder))  # line 564
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 564
    except Exception as E:  # line 565
        Exit("Error removing offline repository: %r" % E)  # line 565
    info(MARKER + "Offline repository removed, you're back online")  # line 566

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 568
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not required here, as either branching from last revision anyway, or branching full file tree anyway.
  '''  # line 571
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 572
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 573
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 574
    m = Metadata()  # type: Metadata  # line 575
    m.loadBranch(m.branch)  # line 576
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 577
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 578
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 578
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 579
    if verbose:  # line 580
        info(MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 580
    if last:  # branch from last revision  # line 581
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 581
    else:  # branch from current file tree state  # line 582
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 582
    if not stay:  # line 583
        m.branch = branch  # line 583
    m.saveBranches()  # TODO #253 or indent again?  # line 584
    info(MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 585

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 587
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 588
    m = Metadata()  # type: Metadata  # line 589
    branch = None  # type: _coconut.typing.Optional[int]  # line 589
    revision = None  # type: _coconut.typing.Optional[int]  # line 589
    strict = '--strict' in options or m.strict  # type: bool  # line 590
    branch, revision = m.parseRevisionString(argument)  # line 591
    if branch is None or branch not in m.branches:  # line 592
        Exit("Unknown branch")  # line 592
    m.loadBranch(branch)  # knows commits  # line 593
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 594
    if verbose:  # line 595
        info(MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 595
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 596
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 597
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 602
    return changed  # returning for unit tests only TODO #254 remove?  # line 603

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False, classic: 'bool'=False):  # TODO #255 introduce option to diff against committed revision and not only file tree  # line 605
    ''' The diff display code. '''  # line 606
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 607
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 608
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 609
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 610
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 611
        content = b""  # type: _coconut.typing.Optional[bytes]  # stored state (old = "curr")  # line 612
        if pinfo.size != 0:  # versioned file  # line 613
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 613
            assert content is not None  # versioned file  # line 613
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current state (new = "into")  # line 614
        if classic:  # line 615
            mergeClassic(content, abspath, "b%d/r%02d" % (branch, revision), os.path.basename(abspath), pinfo.mtime, number_)  # line 615
            continue  # line 615
        blocks = None  # type: List[MergeBlock]  # line 616
        nl = None  # type: bytes  # line 616
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 617
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 618
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 619
        for block in blocks:  # line 620
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some of previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # line 623
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 624
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 624
            elif block.tipe == MergeBlockType.REMOVE:  # line 625
                for no, line in enumerate(block.lines):  # line 626
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 626
            elif block.tipe == MergeBlockType.REPLACE:  # line 627
                for no, line in enumerate(block.replaces.lines):  # line 628
                    printo(wrap("old %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 628
                for no, line in enumerate(block.lines):  # line 629
                    printo(wrap("now %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 629
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 632
                printo()  # line 632

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 634
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 635
    m = Metadata()  # type: Metadata  # line 636
    branch = None  # type: _coconut.typing.Optional[int]  # line 636
    revision = None  # type: _coconut.typing.Optional[int]  # line 636
    strict = '--strict' in options or m.strict  # type: bool  # line 637
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 638
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 639
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 640
    if branch is None or branch not in m.branches:  # line 641
        Exit("Unknown branch")  # line 641
    m.loadBranch(branch)  # knows commits  # line 642
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 643
    if verbose:  # line 644
        info(MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 644
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 645
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 646
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap, classic='--classic' in options)  # line 651

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 653
    ''' Create new revision from file tree changes vs. last commit. '''  # line 654
    m = Metadata()  # type: Metadata  # line 655
    if argument is not None and argument in m.tags:  # line 656
        Exit("Illegal commit message. It was already used as a (unique) tag name and cannot be reused")  # line 656
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 657
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 659
        Exit("No file patterns staged for commit in picky mode")  # line 659
    if verbose:  # line 660
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 660
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 661
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 662
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 663
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 664
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 665
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 666
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 667
    m.saveBranch(m.branch)  # line 668
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 669
    if m.picky:  # remove tracked patterns  # line 670
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 670
    else:  # track or simple mode: set branch modified  # line 671
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 671
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 672
        m.tags.append(argument)  # memorize unique tag  # line 672
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 672
    m.saveBranches()  # line 673
    stored = 0  # type: int  # now determine new commit size on file system  # line 674
    overhead = 0  # type: int  # now determine new commit size on file system  # line 674
    count = 0  # type: int  # now determine new commit size on file system  # line 674
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 675
    for file in os.listdir(commitFolder):  # line 676
        try:  # line 677
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 678
            if file == metaFile:  # line 679
                overhead += newsize  # line 679
            else:  # line 680
                stored += newsize  # line 680
                count += 1  # line 680
        except Exception as E:  # line 681
            error(E)  # line 681
    printo(MARKER_COLOR + "Created new revision r%02d%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%s%s%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, (" '%s'" % argument) if argument is not None else "", Fore.GREEN, Fore.RESET, len(changed.additions) - len(changed.moves), Fore.RED, Fore.RESET, len(changed.deletions) - len(changed.moves), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(changed.modifications), Fore.BLUE + Style.BRIGHT, MOVE_SYMBOL if m.c.useUnicodeFont else "#", Style.RESET_ALL, len(changed.moves), pure.siSize(stored + overhead), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 682

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 694
    ''' Show branches and current repository state. '''  # line 695
    m = Metadata()  # type: Metadata  # line 696
    if not (m.c.useChangesCommand or '--repo' in options):  # line 697
        changes(argument, options, onlys, excps)  # line 697
        return  # line 697
    current = m.branch  # type: int  # line 698
    strict = '--strict' in options or m.strict  # type: bool  # line 699
    printo(MARKER_COLOR + "Offline repository status")  # line 700
    printo("Repository root:     %s" % os.getcwd())  # line 701
    printo("Underlying VCS root: %s" % vcs)  # line 702
    printo("Underlying VCS type: %s" % cmd)  # line 703
    printo("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 704
    printo("Current SOS version: %s" % version.__version__)  # line 705
    printo("At creation version: %s" % m.version)  # line 706
    printo("Metadata format:     %s" % m.format)  # line 707
    printo("Content checking:    %s" % (Fore.CYAN + "size, then content" if m.strict else Fore.BLUE + "size & timestamp") + Fore.RESET)  # TODO size then timestamp?  # line 708
    printo("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 709
    printo("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 710
    printo("Number of branches:  %d" % len(m.branches))  # line 711
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 712
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 713
    m.loadBranch(current)  # line 714
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 715
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 716
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 716
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 717
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of unicode symbols for changed vs. unchanged  # line 722
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 726
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 727
        payload = 0  # type: int  # count used storage per branch  # line 728
        overhead = 0  # type: int  # count used storage per branch  # line 728
        original = 0  # type: int  # count used storage per branch  # line 728
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 729
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 730
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 731
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 731
                else:  # line 732
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 732
        pl_amount = float(payload) / MEBI  # type: float  # line 733
        oh_amount = float(overhead) / MEBI  # type: float  # line 733
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 735
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 736
            m.loadCommit(m.branch, commit_)  # line 737
            for pinfo in m.paths.values():  # line 738
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 738
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 739
        printo("  %s b%d%s @%s (%s%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), Fore.RESET, len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 740
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 751
        printo(Fore.GREEN + "Tracked" + Fore.RESET + " file patterns:")  # TODO #261 print matching untracking patterns side-by-side?  # line 752
        printo(ajoin(Fore.GREEN + "  | " + Fore.RESET, m.branches[m.branch].tracked, "\n"))  # line 753
        printo(Fore.RED + "Untracked" + Fore.RESET + " file patterns:")  # line 754
        printo(ajoin(Fore.RED + "  | " + Fore.RESET, m.branches[m.branch].untracked, "\n"))  # line 755

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 757
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 764
    assert not (check and commit)  # line 765
    m = Metadata()  # type: Metadata  # line 766
    force = '--force' in options  # type: bool  # line 767
    strict = '--strict' in options or m.strict  # type: bool  # line 768
    if argument is not None:  # line 769
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 770
        if branch is None:  # line 771
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 771
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 772
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 773

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 776
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 777
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 778
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 779
    if check and modified(changed) and not force:  # line 784
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 785
        Exit("File tree contains changes. Use --force to proceed")  # line 786
    elif commit:  # line 787
        if not modified(changed) and not force:  # line 788
            Exit("Nothing to commit")  # line 788
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 789
        if msg:  # line 790
            printo(msg)  # line 790

    if argument is not None:  # branch/revision specified  # line 792
        m.loadBranch(branch)  # knows commits of target branch  # line 793
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 794
        revision = m.correctNegativeIndexing(revision)  # line 795
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 796
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 797

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 799
    ''' Continue work on another branch, replacing file tree changes. '''  # line 800
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 801
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 802

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 805
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 806
    else:  # full file switch  # line 807
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 808
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 809

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 816
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 817
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 818
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 819
                rms.append(a)  # line 819
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 820
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 820
        if modified(changed) and not force:  # line 821
            m.listChanges(changed, cwd)  # line 821
            Exit("File tree contains changes. Use --force to proceed")  # line 821
        if verbose:  # line 822
            info(MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 822
        if not modified(todos):  # line 823
            info("No changes to current file tree")  # line 824
        else:  # integration required  # line 825
            for path, pinfo in todos.deletions.items():  # line 826
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 827
                printo("ADD " + path, color=Fore.GREEN)  # line 828
            for path, pinfo in todos.additions.items():  # line 829
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 830
                printo("DEL " + path, color=Fore.RED)  # line 831
            for path, pinfo in todos.modifications.items():  # line 832
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 833
                printo("MOD " + path, color=Fore.YELLOW)  # line 834
    m.branch = branch  # line 835
    m.saveBranches()  # store switched path info  # line 836
    info(MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 837

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 839
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 843
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 844
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 845
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 846
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 847
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 848
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 849
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 850
    if verbose:  # line 851
        info(MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 851

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 854
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 855
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 856
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 857
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 862
        if trackingUnion != trackingPatterns:  # nothing added  # line 863
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 864
        else:  # line 865
            info("Nothing to update")  # but write back updated branch info below  # line 866
    else:  # integration required  # line 867
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 868
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 868
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 868
        if changed.deletions.items():  # line 869
            printo("Additions:")  # line 869
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 870
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 871
            if add_all is None and mrg == MergeOperation.ASK:  # line 872
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 873
                if selection in "ao":  # line 874
                    add_all = "y" if selection == "a" else "n"  # line 874
                    selection = add_all  # line 874
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 875
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 875
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path, color=Fore.GREEN)  # TODO #268 document merge/update output, e.g. (A) as "selected not to add by user choice"  # line 876
        if changed.additions.items():  # line 877
            printo("Deletions:")  # line 877
        for path, pinfo in changed.additions.items():  # line 878
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 879
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 879
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 880
            if del_all is None and mrg == MergeOperation.ASK:  # line 881
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 882
                if selection in "ao":  # line 883
                    del_all = "y" if selection == "a" else "n"  # line 883
                    selection = del_all  # line 883
            if "y" in (del_all, selection):  # line 884
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 884
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path, color=Fore.RED)  # not contained in other branch, but maybe kept  # line 885
        if changed.modifications.items():  # line 886
            printo("Modifications:")  # line 886
        for path, pinfo in changed.modifications.items():  # line 887
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 888
            binary = not m.isTextType(path)  # type: bool  # line 889
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 890
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 891
                printo(("MOD " if not binary else "BIN ") + path, color=Fore.YELLOW)  # TODO print mtime, size differences?  # line 892
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 893
            if op == "t":  # line 894
                printo("THR " + path, color=Fore.MAGENTA)  # blockwise copy of contents  # line 895
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 895
            elif op == "m":  # line 896
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 897
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 897
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 898
                if current == file and verbose:  # line 899
                    info("No difference to versioned file")  # line 899
                elif file is not None:  # if None, error message was already logged  # line 900
                    merged = None  # type: bytes  # line 901
                    nl = None  # type: bytes  # line 901
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 902
                    if merged != current:  # line 903
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 904
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 904
                    elif verbose:  # TODO but update timestamp?  # line 905
                        info("No change")  # TODO but update timestamp?  # line 905
            else:  # mine or wrong input  # line 906
                printo("MNE " + path, color=Fore.CYAN)  # nothing to do! same as skip  # line 907
    info(MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 908
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 909
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 910
    m.saveBranches()  # line 911

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 913
    ''' Remove a branch entirely. '''  # line 914
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 915
    if len(m.branches) == 1:  # line 916
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 916
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 917
    if branch is None or branch not in m.branches:  # line 918
        Exit("Cannot delete unknown branch %r" % branch)  # line 918
    if verbose:  # line 919
        info(MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 919
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 920
    info(MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 921

def add(relPaths: '_coconut.typing.Sequence[str]', patterns: '_coconut.typing.Sequence[str]', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 923
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 924
    force = '--force' in options  # type: bool  # line 925
    m = Metadata()  # type: Metadata  # line 926
    if not (m.track or m.picky):  # line 927
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 928
    knownpatterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 929
    for relPath, pattern in zip(relPaths, patterns):  # line 930
        if pattern in knownpatterns:  # line 931
            Exit("Pattern '%s' already tracked" % pattern)  # line 932
        if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 933
            Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 934
        if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 935
            Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 936
        knownpatterns.append(pattern)  # line 937
    m.saveBranches()  # line 938
    info(MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # line 939

def remove(relPaths: '_coconut.typing.Sequence[str]', patterns: '_coconut.typing.Sequence[str]', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 941
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 942
    m = Metadata()  # type: Metadata  # line 943
    if not (m.track or m.picky):  # line 944
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' to start repository in tracking or picky mode")  # line 945
    knownpatterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 946
    for relPath, pattern in zip(relPaths, patterns):  # line 947
        if pattern not in knownpatterns:  # line 948
            suggestion = _coconut.set()  # type: Set[str]  # line 949
            for pat in knownpatterns:  # line 950
                if fnmatch.fnmatch(pattern, pat):  # line 950
                    suggestion.add(pat)  # line 950
            if suggestion:  # line 951
                printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # line 951
            Exit("Tracked pattern '%s' not found" % pattern)  # line 952
    knownpatterns.remove(pattern)  # line 953
    m.saveBranches()  # line 954
    info(MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 955

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 957
    ''' List specified directory, augmenting with repository metadata. '''  # line 958
    m = Metadata()  # type: Metadata  # line 959
    folder = (os.getcwd() if folder is None else folder)  # line 960
    if '--all' in options or '-a' in options:  # always start at SOS repo root with --all  # line 961
        folder = m.root  # always start at SOS repo root with --all  # line 961
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 962
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 963
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 964
    if verbose:  # line 965
        info(MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 965
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 966
    if relPath.startswith(os.pardir):  # line 967
        Exit("Cannot list contents of folder outside offline repository")  # line 967
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 968
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 969
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 970
        if len(m.tags) > 0:  # line 971
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 971
        return  # line 972
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 973
        if not recursive:  # avoid recursion  # line 974
            dirnames.clear()  # avoid recursion  # line 974
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 975
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 976

        folder = decode(dirpath)  # line 978
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 979
        if patterns:  # line 980
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 981
            if out:  # line 982
                printo("DIR %s\n" % relPath + out)  # line 982
            continue  # with next folder  # line 983
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 984
        if len(files) > 0:  # line 985
            printo("DIR %s" % relPath)  # line 985
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 986
            ignore = None  # type: _coconut.typing.Optional[str]  # line 987
            for ig in m.c.ignores:  # remember first match  # line 988
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 988
                    ignore = ig  # remember first match  # line 988
                    break  # remember first match  # line 988
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 989
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 989
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 989
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 989
                        break  # found a white list entry for ignored file, undo ignoring it  # line 989
            matches = []  # type: List[str]  # line 990
            if not ignore:  # line 991
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 992
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 993
                        matches.append(os.path.basename(pattern))  # line 993
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 994
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 995

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 997
    ''' List previous commits on current branch. '''  # line 998
    changes_ = "--changes" in options  # type: bool  # line 999
    diff_ = "--diff" in options  # type: bool  # line 1000
    m = Metadata()  # type: Metadata  # line 1001
    m.loadBranch(m.branch)  # knows commit history  # line 1002
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 1003
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 1004
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Offline commit history of branch %r" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 1005
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 1006
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 1007
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 1008
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 1009
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 1010
    commit = None  # type: CommitInfo  # used for reading parent branch information  # line 1010
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1011
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 1012
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 1013
    for no in range(maxi + 1):  # line 1014
        if indicator:  # line 1015
            printo("  %%s %%0%dd" % digits % ((lambda _coconut_none_coalesce_item: " " if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(indicator.getIndicator()), no), nl="\r")  # line 1015
        if no in m.commits:  # line 1016
            commit = m.commits[no]  # line 1016
        else:  # line 1017
            if n.branch != n.getParentBranch(m.branch, no):  # line 1018
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 1018
            commit = n.commits[no]  # line 1019
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 1020
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 1021
        if "--all" in options or no >= lastno:  # line 1022
            if no >= lastno:  # line 1023
                indicator = None  # line 1023
            _add = news - olds  # type: FrozenSet[str]  # line 1024
            _del = olds - news  # type: FrozenSet[str]  # line 1025
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 1027
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 1029
            printo("  %s r%s @%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%sT%s%02d) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, Fore.RESET, len(_add), Fore.RED, Fore.RESET, len(_del), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(_mod), Fore.CYAN, Fore.RESET, _txt, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 1030
            if changes_:  # line 1031
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}), root=cwd if '--relative' in options else None)  # TODO why using None here? to avoid stating files for performance reasons?  # line 1042
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 1043
                pass  #  _diff(m, changes)  # needs from revision diff  # line 1043
        olds = news  # replaces olds for next revision compare  # line 1044
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 1045

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 1047
    ''' Exported entire repository as archive for easy transfer. '''  # line 1048
    if verbose:  # line 1049
        info(MARKER + "Dumping repository to archive...")  # line 1049
    m = Metadata()  # type: Metadata  # to load the configuration  # line 1050
    progress = '--progress' in options  # type: bool  # line 1051
    delta = '--full' not in options  # type: bool  # line 1052
    skipBackup = '--skip-backup' in options  # type: bool  # line 1053
    import functools  # line 1054
    import locale  # line 1054
    import warnings  # line 1054
    import zipfile  # line 1054
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 1055
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 1055
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 1055
    except:  # line 1056
        compression = zipfile.ZIP_STORED  # line 1056

    if ("" if argument is None else argument) == "":  # line 1058
        Exit("Argument missing (target filename)")  # line 1058
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 1059
    entries = []  # type: List[str]  # line 1060
    if os.path.exists(encode(argument)) and not skipBackup:  # line 1061
        try:  # line 1062
            if verbose:  # line 1063
                info("Creating backup...")  # line 1063
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 1064
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 1065
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 1065
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 1065
        except Exception as E:  # line 1066
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 1066
    if verbose:  # line 1067
        info("Dumping revisions...")  # line 1067
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1068
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1068
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1069
        _zip.debug = 0  # suppress debugging output  # line 1070
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1071
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1072
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1073
        totalsize = 0  # type: int  # line 1074
        start_time = time.time()  # type: float  # line 1075
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1076
            dirpath = decode(dirpath)  # line 1077
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1078
                continue  # don't backup backups  # line 1078
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1079
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1080
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1081
            for filename in filenames:  # line 1082
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1083
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1084
                totalsize += os.stat(encode(abspath)).st_size  # line 1085
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1086
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1087
                    continue  # don't backup backups  # line 1087
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1088
                    if show:  # line 1089
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1089
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1090
        if delta:  # line 1091
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1091
    info("\r" + pure.ljust(MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1092

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1094
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1095
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1096
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1097
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1097
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1098
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1099
    if maxi is None:  # line 1100
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1100
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1101
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1104
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1106
    while files:  # line 1107
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1108
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1109
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1111
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1111
    tracked = None  # type: bool  # line 1112
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1112
    tracked, commitArgs = vcsCommits[cmd]  # line 1112
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1113
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1115
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1115
    if tracked:  # line 1116
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1116

def config(arguments: 'List[_coconut.typing.Optional[str]]', options: 'List[str]'=[]):  # line 1118
    command = None  # type: str  # line 1119
    key = None  # type: str  # line 1119
    value = None  # type: str  # line 1119
    v = None  # type: str  # line 1119
    command, key, value = (arguments + [None] * 2)[:3]  # line 1120
    if command is None:  # line 1121
        usage.usage("help", verbose=True)  # line 1121
    if command not in ("set", "unset", "show", "list", "add", "rm"):  # line 1122
        Exit("Unknown config command %r" % command)  # line 1122
    local = "--local" in options  # type: bool  # line 1123
    m = Metadata()  # type: Metadata  # loads nested configuration (local - global - defaults)  # line 1124
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1125
    if command == "set":  # line 1126
        if None in (key, value):  # line 1127
            Exit("Key or value not specified")  # line 1127
        if key not in ((([] if local else ONLY_GLOBAL_FLAGS) + CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1128
            Exit("Unsupported key for %s configuration %r" % ("local" if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1128
        if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1129
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1129
        c[key] = value.lower() in TRUTH_VALUES if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1130
    elif command == "unset":  # line 1131
        if key is None:  # line 1132
            Exit("No key specified")  # line 1132
        if key not in c.keys(with_nested=False):  # line 1133
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, "local" if local else "global"))  # line 1134
        del c[key]  # line 1135
    elif command == "add":  # TODO copy list from defaults if not local/global  # line 1136
        if None in (key, value):  # line 1137
            Exit("Key or value not specified")  # line 1137
        if key not in CONFIGURABLE_LISTS:  # line 1138
            Exit("Unsupported key %r for list addition" % key)  # line 1138
        if key not in c.keys():  # prepare empty list, or copy from underlying, add new value below TODO also allow one more level of underlying?  # line 1139
            c[key] = [_ for _ in c.__defaults[key]] if key in c.__defaults[key] else []  # prepare empty list, or copy from underlying, add new value below TODO also allow one more level of underlying?  # line 1139
        elif value in c[key]:  # line 1140
            Exit("Value already contained, nothing to do")  # line 1140
        if ";" not in value:  # line 1141
            c[key].append(removePath(key, value.strip()))  # line 1141
        else:  # line 1142
            c[key].extend([removePath(key, v) for v in safeSplit(value, ";")])  # line 1142
    elif command == "rm":  # line 1143
        if None in (key, value):  # line 1144
            Exit("Key or value not specified")  # line 1144
        if key not in c.keys(with_nested=False):  # line 1145
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, "local" if local else "global"))  # line 1146
        if value not in c[key]:  # line 1147
            Exit("Unknown value %r" % value)  # line 1147
        c[key].remove(value)  # line 1148
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1149
            del c[key]  # remove local entry, to fallback to global  # line 1149
    else:  # Show or list  # line 1150
        if key == "ints":  # list valid configuration items  # line 1151
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1151
        elif key == "flags":  # line 1152
            printo(", ".join(ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS))  # line 1152
        elif key == "lists":  # line 1153
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1153
        elif key == "texts":  # line 1154
            printo(", ".join([_ for _ in defaults.keys() if _ not in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS + CONFIGURABLE_INTS + CONFIGURABLE_LISTS)]))  # line 1154
        else:  # no key: list all  # line 1155
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1156
            c = m.c  # always use full configuration chain  # line 1157
            try:  # attempt single key  # line 1158
                assert key is not None  # force exception if no key specified  # line 1159
                c[key]  # force exception if no key specified  # line 1159
                l = key in c.keys(with_nested=False)  # type: bool  # line 1160
                g = key in c.__defaults.keys(with_nested=False)  # type: bool  # line 1160
                printo(key.rjust(20), color=Fore.WHITE, nl="")  # line 1161
                printo(" " + (out[3] if not (l or g) else (out[1] if l else out[2])) + " ", color=Fore.CYAN, nl="")  # line 1162
                printo(repr(c[key]))  # line 1163
            except:  # normal value listing  # line 1164
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # copy-by-value  # line 1165
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1166
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1167
                for k, vt in sorted(vals.items()):  # line 1168
                    printo(k.rjust(20), color=Fore.WHITE, nl="")  # line 1169
                    printo(" " + out[vt[1]] + " ", color=Fore.CYAN, nl="")  # line 1170
                    printo(vt[0])  # line 1171
                if len(c.keys()) == 0:  # line 1172
                    info("No local configuration stored.")  # line 1172
                if len(c.__defaults.keys()) == 0:  # line 1173
                    info("No global configuration stored.")  # line 1173
        return  # in case of list, no need to store anything  # line 1174
    if local:  # saves changes of repoConfig  # line 1175
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1175
        m.saveBranches()  # saves changes of repoConfig  # line 1175
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1175
    else:  # global config  # line 1176
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1177
        if f is None:  # line 1178
            Exit("Error saving user configuration: %r" % h)  # line 1178

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1180
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1183
    if verbose:  # line 1184
        info(MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1184
    force = '--force' in options  # type: bool  # line 1185
    soft = '--soft' in options  # type: bool  # line 1186
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1187
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1187
    m = Metadata()  # type: Metadata  # line 1188
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1189
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1190
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1191
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1192
    if not matching and not force:  # line 1193
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1193
    if not (m.track or m.picky):  # line 1194
        Exit("Repository is in simple mode. Use basic file operations to modify files, then execute 'sos commit' to version any changes")  # line 1194
    if pattern not in patterns:  # list potential alternatives and exit  # line 1195
        for tracked in (t for t in patterns if t[:t.rindex(SLASH)] == relPath):  # for all patterns of the same source folder HINT was os.path.dirpath before  # line 1196
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1197
            if alternative:  # line 1198
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1198
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: "if not (force or soft):""  # line 1199
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1200
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1201
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1202
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1206
#  oldTokens:GlobBlock[]?; newToken:GlobBlock[]?  # TODO remove optional?, only here to satisfy mypy
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1208
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1209
    if len({st[1] for st in matches}) != len(matches):  # line 1210
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1210
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1211
    if os.path.exists(encode(newRelPath)):  # line 1212
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1213
        if exists and not (force or soft):  # line 1214
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1214
    else:  # line 1215
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1215
    if not soft:  # perform actual renaming  # line 1216
        for (source, target) in matches:  # line 1217
            try:  # line 1218
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1218
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1219
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1219
    patterns[patterns.index(pattern)] = newPattern  # line 1220
    m.saveBranches()  # line 1221

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1223
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1224
    debug("Parsing command-line arguments...")  # line 1225
    root = os.getcwd()  # line 1226
    try:  # line 1227
        onlys, excps, remotes = parseArgumentOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1228
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1229
        arguments = [c.strip() for c in sys.argv[2:] if not ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # line 1230
        options = [c.strip() for c in sys.argv[2:] if ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # options *with* arguments have to be parsed directly from sys.argv inside using functions  # line 1231
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1232
        if command[:1] in "amr":  # line 1233
            try:  # line 1234
                relPaths, patterns = unzip([relativize(root, os.path.join(cwd, argument)) for argument in ((["."] if arguments is None else arguments))])  # line 1234
            except:  # line 1235
                command = "ls"  # convert command into ls --patterns  # line 1236
                arguments[0] = None  # convert command into ls --patterns  # line 1236
                options.extend(["--patterns", "--all"])  # convert command into ls --patterns  # line 1236
# Exit("Need one or more file patterns as argument (escape them according to your shell)")
        if command[:1] == "m":  # line 1238
            if len(arguments) < 2:  # line 1239
                Exit("Need a second file pattern argument as target for move command")  # line 1239
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1240
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1241
        if command == "raise":  # line 1242
            raise Exception("provoked exception")  # line 1242
        elif command[:1] == "a":  # e.g. addnot  # line 1243
            add(relPaths, patterns, options, negative="n" in command)  # e.g. addnot  # line 1243
        elif command[:1] == "b":  # line 1244
            branch(arguments[0], arguments[1], options)  # line 1244
        elif command[:3] == "com":  # line 1245
            commit(arguments[0], options, onlys, excps)  # line 1245
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1246
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1246
        elif command[:2] == "ci":  # line 1247
            commit(arguments[0], options, onlys, excps)  # line 1247
        elif command[:3] == 'con':  # line 1248
            config(arguments, options)  # line 1248
        elif command[:2] == "de":  # line 1249
            destroy((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1249
        elif command[:2] == "di":  # TODO no consistent handling of single dash/characters argument-options  # line 1250
            diff((lambda _coconut_none_coalesce_item: "/" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[2 if arguments[0] == '-n' else 0]), options, onlys, excps)  # TODO no consistent handling of single dash/characters argument-options  # line 1250
        elif command[:2] == "du":  # line 1251
            dump((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1251
        elif command[:1] == "h":  # line 1252
            usage.usage(arguments[0], verbose=verbose)  # line 1252
        elif command[:2] == "lo":  # line 1253
            log(options, cwd)  # line 1253
        elif command[:2] == "li":  # line 1254
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1254
        elif command[:2] == "ls":  # line 1255
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1255
        elif command[:1] == "m":  # e.g. mvnot  # line 1256
            move(relPaths[0], patterns[0], newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1256
        elif command[:2] == "of":  # line 1257
            offline(arguments[0], arguments[1], options, remotes)  # line 1257
        elif command[:2] == "on":  # line 1258
            online(options)  # line 1258
        elif command[:1] == "p":  # line 1259
            publish(arguments[0], cmd, options, onlys, excps)  # line 1259
        elif command[:1] == "r":  # e.g. rmnot  # line 1260
            remove(relPaths, patterns, options, negative="n" in command)  # e.g. rmnot  # line 1260
        elif command[:2] == "st":  # line 1261
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1261
        elif command[:2] == "sw":  # line 1262
            switch((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps, cwd)  # line 1262
        elif command[:1] == "u":  # line 1263
            update((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps)  # line 1263
        elif command[:1] == "v":  # line 1264
            usage.usage(arguments[0], version=True)  # line 1264
        else:  # line 1265
            Exit("Unknown command '%s'" % command)  # line 1265
        Exit(code=0)  # regular exit  # line 1266
    except (Exception, RuntimeError) as E:  # line 1267
        exception(E)  # line 1268
        Exit("An internal error occurred in SOS\nPlease report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.")  # line 1269

def main():  # line 1271
    global debug, info, warn, error  # to modify logger  # line 1272
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1273
    _log = Logger(logging.getLogger(__name__))  # line 1274
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1274
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1275
        sys.argv.remove(option)  # clean up program arguments  # line 1275
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1276
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1276
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1277
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1278
    debug("Detected SOS root folder: %s" % (("-" if root is None else root)))  # line 1279
    debug("Detected VCS root folder: %s" % (("-" if vcs is None else vcs)))  # line 1280
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1281
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1282
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv"):  # in offline mode or just going offline  # line 1283
        cwd = os.getcwd()  # line 1284
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1285
        parse(vcs, cwd, cmd)  # line 1286
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1287
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1288
        import subprocess  # only required in this section  # line 1289
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1290
        inp = ""  # type: str  # line 1291
        while True:  # line 1292
            so, se = process.communicate(input=inp)  # line 1293
            if process.returncode is not None:  # line 1294
                break  # line 1294
            inp = sys.stdin.read()  # line 1295
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1296
            if root is None:  # line 1297
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1297
            m = Metadata(root)  # type: Metadata  # line 1298
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1299
            m.saveBranches()  # line 1300
    else:  # line 1301
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1301


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: List[None]  # this is a trick allowing to modify the module-level flags from the test suite  # line 1305
force_vcs = [None] if '--vcs' in sys.argv else []  # type: List[None]  # line 1306
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1307

_log = Logger(logging.getLogger(__name__))  # line 1309
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1309

if __name__ == '__main__':  # line 1311
    main()  # line 1311
