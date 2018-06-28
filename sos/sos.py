#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x55ccf4b5

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

    def __init__(_, path: '_coconut.typing.Optional[str]'=None, offline: 'bool'=False, remotes: 'List[str]'=[]) -> 'None':  # line 54
        ''' Create empty container object for various repository operations, and import configuration. Offline initializes a repository. '''  # line 55
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
        _.remotes = []  # type: List[str]  # list of secondary storage locations (in same file system, no other protocols), which will replicate all write operations  # line 62
        _.loadBranches(offline=offline, remotes = remotes)  # loads above values from repository, or uses application defaults  # line 63

        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 65
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 66
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 67

        if Metadata.singleton is None:  # load configuration only once per runtime  # line 69
            Metadata.singleton = configr.Configr(data=_.repoConf, defaults=loadConfig())  # load global configuration with defaults behind the local configuration  # line 70
        _.c = Metadata.singleton  # type: configr.Configr  # line 71

    def isTextType(_, filename: 'str') -> 'bool':  # line 73
        return (((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(mimetypes.guess_type(filename)[0])).startswith("text/") or any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.texttype])) and not any([fnmatch.fnmatch(filename, pattern) for pattern in _.c.bintype])  # line 73

    def correctNegativeIndexing(_, revision: 'int') -> 'int':  # line 75
        ''' As the na_e says, this deter_ines the correct positive revision nu_ber for negative indexing (-1 being last, -2 being second last). '''  # line 76
        revision = revision if revision >= 0 else (max(_.commits) if _.commits else (lambda _coconut_none_coalesce_item: -1 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.getHighestRevision(_.branch))) + 1 + revision  # negative indexing  # line 77
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
        realadditions = {k: v for k, v in changed.additions.items() if k not in changed.moves}  # type: Dict[str, PathInfo]  # line 88
        realdeletions = {k: v for k, v in changed.deletions.items() if k not in moves}  # type: Dict[str, PathInfo]  # line 89
        if len(changed.moves) > 0:  # line 90
            printo(ajoin("MOV ", ["%s  <-  %s" % (relp(path, root), relp(dpath, root)) for path, (dpath, dinfo) in sorted(changed.moves.items())], "\n") + Style.RESET_ALL, color=Fore.BLUE + Style.BRIGHT)  # line 90
        if len(realadditions) > 0:  # line 91
            printo(ajoin("ADD ", sorted([relp(p, root) for p in realadditions.keys()]), "\n"), color=Fore.GREEN)  # line 91
        if len(realdeletions) > 0:  # line 92
            printo(ajoin("DEL ", sorted([relp(p, root) for p in realdeletions.keys()]), "\n"), color=Fore.RED)  # line 92
        if len(changed.modifications) > 0:  # line 93
            printo(ajoin("MOD ", [relp(m, root) if commitTime is None else (relp(m, root) + (" <older than previously committed>" if pi.mtime < _.paths[m].mtime else "")) for (m, pi) in sorted(changed.modifications.items())], "\n"), color=Fore.YELLOW)  # line 93

    def loadBranches(_, offline: 'bool'=False, remotes: 'List[str]'=[]):  # line 95
        ''' Load list of branches and current branch info from metadata file. offline = True command avoids message. '''  # line 96
        try:  # fails if not yet created (on initial branch/commit)  # line 97
            branches = None  # type: List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)  # line 98
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 99
                repo, branches, config = json.load(fd)  # line 100
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 101
            _.branch = repo["branch"]  # current branch integer  # line 102
            _.track, _.picky, _.strict, _.compress, _.version, _.format, _.remotes = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format", "remotes"]]  # line 103
            upgraded = []  # type: List[str]  # line 104
            if _.version is None:  # line 105
                _.version = "0 - pre-1.2"  # line 106
                upgraded.append("pre-1.2")  # line 107
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 108
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 109
                upgraded.append("2018.1210.3028")  # line 110
            if _.format is None:  # must be before 1.3.5+  # line 111
                _.format = 1  # marker for first metadata file format  # line 112
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 113
                upgraded.append("1.3.5")  # line 114
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 115
            _.repoConf = config  # line 116
            if _.format == 1 or _.remotes is None:  # before remotes  # line 117
                _.format = METADATA_FORMAT  # line 118
                _.remotes = []  # default is no remotes  # line 119
                upgraded.append("1.7.0")  # remote URLs introduced  # line 120
            if upgraded:  # line 121
                for upgrade in upgraded:  # line 122
                    printo("WARNING  Upgraded repository metadata to match SOS version %r" % upgrade, color=Fore.YELLOW)  # line 122
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 123
                _.saveBranches()  # line 124
        except Exception as E:  # if not found, create metadata folder with default values  # line 125
            _.branches = {}  # line 126
            _.track, _.picky, _.strict, _.compress, _.version, _.remotes, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, remotes, METADATA_FORMAT]  # line 127
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # hide warning only when going offline  # line 129

    def saveBranches(_, also: 'Dict[str, Any]'={}):  # line 131
        ''' Save list of branches and current branch info to metadata file. '''  # line 132
        store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT, "remotes": _.remotes}  # type: Dict[str, Any]  # dictionary of repository settings (while _.repoConf stores user settings)  # line 133
        store.update(also)  # allows overriding certain values at certain points in time  # line 138
        for remote in [None] + _.remotes:  # line 139
            tryOrIgnore(lambda: shutil.copy2(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), encode(os.path.join((_.root if remote is None else remote), metaFolder, metaBack))))  # backup  # line 140
            try:  # line 141
                with codecs.open(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 141
                    json.dump((store, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints, fd knows how to encode them  # line 142
            except Exception as E:  # line 143
                error("Saving branches%s" % ((" to remote path " + remote) if remote else ""))  # line 143

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 145
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 146
        if name == "":  # line 147
            return -1  # line 147
        try:  # attempt to parse integer string  # line 148
            return int(name)  # attempt to parse integer string  # line 148
        except ValueError:  # line 149
            pass  # line 149
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 150
        return found[0] if found else None  # line 151

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 153
        ''' Convenience accessor for named branches. '''  # line 154
        if name == "":  # current  # line 155
            return _.branch  # current  # line 155
        try:  # attempt to parse integer string  # line 156
            return int(name)  # attempt to parse integer string  # line 156
        except ValueError:  # line 157
            pass  # line 157
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 158
        return found[0] if found else None  # line 159

    def loadBranch(_, branch: 'int'):  # line 161
        ''' Load all commit information from a branch meta data file. '''  # line 162
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 163
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 164
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 165
        _.branch = branch  # line 166

    def saveBranch(_, branch: 'int'):  # line 168
        ''' Save all commits to a branch meta data file. '''  # line 169
        for remote in [None] + _.remotes:  # line 170
            tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile, base=remote)), encode(branchFolder(branch, file=metaBack, base=remote))))  # backup  # line 171
            try:  # line 172
                with codecs.open(encode(branchFolder(branch, file=metaFile, base=remote)), "w", encoding=UTF8) as fd:  # line 172
                    json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 173
            except Exception as E:  # line 174
                error("Saving branch%s" % ((" to remote path " + remote) if remote else ""))  # line 174

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 176
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 184
        if verbose:  # line 185
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 185
        now = int(time.time() * 1000)  # type: int  # line 186
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 187
        revision = max(_.commits) if _.commits else 0  # type: int  # line 188
        _.commits.clear()  # line 189
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 190
        for remote in [None] + _.remotes:  # line 195
            tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)) if full else branchFolder(branch, base=(_.root if remote is None else remote)))), lambda: error("Duplicating remote branch folder %r" % remote))  # line 196
        if full:  # not fast branching via reference - copy all current files to new branch  # line 197
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 198
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 199
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 199
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit TODO #244 also contain message from latest revision of originating branch  # line 200
            _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 201
        _.saveBranch(branch)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 202
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 203

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 205
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 211
        now = int(time.time() * 1000)  # type: int  # line 212
        simpleMode = not (_.track or _.picky)  # line 213
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 214
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 215
        if verbose:  # line 216
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 216
        _.paths = {}  # type: Dict[str, PathInfo]  # line 217
        if simpleMode:  # branches from file system state. not necessary to create branch folder, as it is done in findChanges below anyway  # line 218
            changed, msg = _.findChanges(branch, 0, progress=simpleMode)  # HINT creates revision folder and versioned files!  # line 219
            _.listChanges(changed)  # line 220
            if msg:  # display compression factor and time taken  # line 221
                printo(msg)  # display compression factor and time taken  # line 221
            _.paths.update(changed.additions.items())  # line 222
        else:  # tracking or picky mode: branch from latest revision  # line 223
            for remote in [None] + _.remotes:  # line 224
                tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)))), lambda: error("Creating remote branch folder %r" % remote))  # line 225
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 226
                _.loadBranch(_.branch)  # line 227
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO #245 what if last switch was to an earlier revision? no persisting of last checkout  # line 228
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 229
                for path, pinfo in _.paths.items():  # line 230
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 230
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 231
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 232
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 233
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 234

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 236
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 239
        import collections  # used almost only here  # line 240
        binfo = None  # type: BranchInfo  # typing info  # line 241
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 242
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 243
        if deps:  # need to copy all parent revisions to dependent branches first  # line 244
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 245
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 246
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 247
                for dep, _rev in deps:  # line 248
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO #246 align placement of indicator with other uses of progress  # line 249
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 250
#          if rev in _.commits:  # TODO #247 uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 252
                    shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 253
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 254
                for rev in range(minrev + 1, _rev + 1):  # line 255
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 256
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 257
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 258
                        newcommits[dep][rev] = _.commits[rev]  # line 259
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 260
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 261
        printo(pure.ljust() + "\r")  # clean line output  # line 262
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 263
        tryOrIgnore(lambda: os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?"))  # line 264
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 265
        del _.branches[branch]  # line 266
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 267
        _.saveBranches()  # persist modified branches list  # line 268
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 269
            _.commits = commits  # line 270
            _.saveBranch(branch)  # line 271
        _.commits.clear()  # clean memory  # line 272
        return binfo  # line 273

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 275
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 276
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 277
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 278
            _.paths = json.load(fd)  # line 278
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 279
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 280

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 282
        ''' Save all file information to a commit meta data file. '''  # line 283
        for remote in [None] + _.remotes:  # line 284
            try:  # line 285
                target = revisionFolder(branch, revision, base=(_.root if remote is None else remote))  # type: str  # line 286
                tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 287
                tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 288
                with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 289
                    json.dump(_.paths, fd, ensure_ascii=False)  # line 289
            except Exception as E:  # line 290
                error("Saving commit%s" % ((" to remote path " + remote) if remote else ""))  # line 290

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 292
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 301
        import collections  # used only in this method  # line 302
        write = branch is not None and revision is not None  # used for writing commits  # line 303
        if write:  # line 304
            for remote in [None] + _.remotes:  # line 304
                tryOrIgnore(lambda: os.makedirs(encode(revisionFolder(branch, revision, base=(_.root if remote is None else remote)))))  # line 305
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # WARN this code needs explicity argument passing for initialization due to mypy problems with default arguments  # line 306
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 307
        hashed = None  # type: _coconut.typing.Optional[str]  # line 308
        written = None  # type: int  # line 308
        compressed = 0  # type: int  # line 308
        original = 0  # type: int  # line 308
        start_time = time.time()  # type: float  # line 308
        knownPaths = {}  # type: Dict[str, List[str]]  # line 309

# Find relevant folders/files that match specified folder/glob patterns for exclusive inclusion or exclusion
        byFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 312
        onlyByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 313
        dontByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 314
        for path, pinfo in _.paths.items():  # line 315
            if pinfo is None:  # quicker than generator expression above  # line 316
                continue  # quicker than generator expression above  # line 316
            slash = path.rindex(SLASH)  # type: int  # line 317
            byFolder[path[:slash]].append(path[slash + 1:])  # line 318
        for pattern in ([] if considerOnly is None else considerOnly):  # line 319
            slash = pattern.rindex(SLASH)  # line 319
            onlyByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 319
        for pattern in ([] if dontConsider is None else dontConsider):  # line 320
            slash = pattern.rindex(SLASH)  # line 320
            dontByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 320
        for folder, paths in byFolder.items():  # line 321
            pos = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in onlyByFolder.get(folder, [])]) if considerOnly is not None else set(paths)  # type: Set[str]  # line 322
            neg = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in dontByFolder.get(folder, [])]) if dontConsider is not None else set()  # type: Set[str]  # line 323
            knownPaths[folder] = list(pos - neg)  # line 324

        for path, dirnames, filenames in os.walk(_.root):  # line 326
            path = decode(path)  # line 327
            dirnames[:] = [decode(d) for d in dirnames]  # line 328
            filenames[:] = [decode(f) for f in filenames]  # line 329
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 330
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 331
            dirnames.sort()  # line 332
            filenames.sort()  # line 332
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 333
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 334
            if dontConsider:  # line 335
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 336
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 337
                filename = relPath + SLASH + file  # line 338
                filepath = os.path.join(path, file)  # line 339
                try:  # line 340
                    stat = os.stat(encode(filepath))  # line 340
                except Exception as E:  # line 341
                    exception(E)  # line 341
                    continue  # line 341
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 342
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 343
                if show:  # indication character returned  # line 344
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 345
                    printo(pure.ljust(outstring), nl="")  # line 346
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 347
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 348
                    nameHash = hashStr(filename)  # line 349
                    try:  # line 350
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=nameHash) for remote in [None] + _.remotes] if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 351
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 352
                        compressed += written  # line 353
                        original += size  # line 353
                    except PermissionError as E:  # line 354
                        error("File permission error for %s" % filepath)  # line 354
                    except Exception as F:  # HINT e.g. FileNotFoundError will not add to additions  # line 355
                        exception(F)  # HINT e.g. FileNotFoundError will not add to additions  # line 355
                    continue  # with next file  # line 356
                last = _.paths[filename]  # filename is known - check for modifications  # line 357
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 358
                    try:  # line 359
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 360
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 361
                        continue  # line 361
                    except Exception as E:  # line 362
                        exception(E)  # line 362
                elif size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False)):  # detected a modification  # line 363
                    try:  # line 364
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 365
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 366
                    except Exception as E:  # line 367
                        exception(E)  # line 367
                else:  # with next file  # line 368
                    continue  # with next file  # line 368
                compressed += written  # line 369
                original += last.size if inverse else size  # line 369
            if relPath in knownPaths:  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 370
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 370
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 371
            for file in names:  # line 372
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 373
                    continue  # don't mark ignored files as deleted  # line 373
                pth = path + SLASH + file  # type: str  # line 374
                changed.deletions[pth] = _.paths[pth]  # line 375
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, _.strict))  # line 376
        if progress:  # forces clean line of progress output  # line 377
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 377
        elif verbose:  # line 378
            info("Finished detecting changes")  # line 378
        tt = time.time() - start_time  # type: float  # line 379
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # in KiBi  # line 380
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 381
        msg = (msg + " | " if msg else "") + ("Transfer speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 382
        return (changed, msg if msg else None)  # line 383

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 385
        ''' Returns nothing, just updates _.paths in place. '''  # line 386
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 387

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 389
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 390
        try:  # load initial paths  # line 391
            _.loadCommit(branch, startwith)  # load initial paths  # line 391
        except:  # no revisions  # line 392
            yield {}  # no revisions  # line 392
            return None  # no revisions  # line 392
        if incrementally:  # line 393
            yield _.paths  # line 393
        m = Metadata(_.root)  # type: Metadata  # next changes TODO #250 avoid loading all metadata and config  # line 394
        rev = None  # type: int  # next changes TODO #250 avoid loading all metadata and config  # line 394
        for rev in range(startwith + 1, revision + 1):  # line 395
            m.loadCommit(branch, rev)  # line 396
            for p, info in m.paths.items():  # line 397
                if info.size == None:  # line 398
                    del _.paths[p]  # line 398
                else:  # line 399
                    _.paths[p] = info  # line 399
            if incrementally:  # line 400
                yield _.paths  # line 400
        yield None  # for the default case - not incrementally  # line 401

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 403
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 404
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 405

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 407
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 410
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 411
            return (_.branch, -1)  # no branch/revision specified  # line 411
        argument = argument.strip()  # line 412
        if argument.startswith(SLASH):  # current branch  # line 413
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 413
        if argument.endswith(SLASH):  # line 414
            try:  # line 415
                return (_.getBranchByName(argument[:-1]), -1)  # line 415
            except ValueError:  # line 416
                Exit("Unknown branch label '%s'" % argument)  # line 416
        if SLASH in argument:  # line 417
            b, r = argument.split(SLASH)[:2]  # line 418
            try:  # line 419
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 419
            except ValueError:  # line 420
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 420
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 421
        if branch not in _.branches:  # line 422
            branch = None  # line 422
        try:  # either branch name/number or reverse/absolute revision number  # line 423
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 423
        except:  # line 424
            Exit("Unknown branch label or wrong number format")  # line 424
        Exit("This should never happen. Please create a issue report")  # line 425
        return (None, None)  # line 425

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 427
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 429
        while True:  # line 430
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 431
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 432
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 433
                break  # line 433
            revision -= 1  # line 434
            if revision < 0:  # line 435
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 435
        return revision, source  # line 436

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 438
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 439
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 440
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 441
            return [branch]  # found. need to load commit from other branch instead  # line 441
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 442
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 442
        return others  # line 443

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 445
        return _.getParentBranches(branch, revision)[-1]  # line 445

    @_coconut_tco  # line 447
    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 447
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 448
        m = Metadata()  # type: Metadata  # line 449
        other = branch  # type: _coconut.typing.Optional[int]  # line 450
        while other is not None:  # line 451
            m.loadBranch(other)  # line 452
            if m.commits:  # line 453
                return _coconut_tail_call(max, m.commits)  # line 453
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 454
        return None  # line 455

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 457
        ''' Copy versioned file to other branch/revision. '''  # line 458
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 459
        for remote in [None] + _.remotes:  # line 460
            try:  # line 461
                target = revisionFolder(toBranch, toRevision, file=pinfo.nameHash, base=(_.root if remote is None else remote))  # type: str  # line 462
                shutil.copy2(encode(source), encode(target))  # line 463
            except Exception as E:  # line 464
                error("Copying versioned file%s" % ((" to remote path " % remote) if remote else ""))  # line 464

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 466
        ''' Return file contents, or copy contents into file path provided (used in update and restorefile). '''  # line 467
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 468
        try:  # line 469
            with openIt(source, "r", _.compress) as fd:  # line 469
                if toFile is None:  # read bytes into memory and return  # line 470
                    return fd.read()  # read bytes into memory and return  # line 470
                with open(encode(toFile), "wb") as to:  # line 471
                    while True:  # line 472
                        buffer = fd.read(bufSize)  # line 473
                        to.write(buffer)  # line 474
                        if len(buffer) < bufSize:  # line 475
                            break  # line 475
                    return None  # line 476
        except Exception as E:  # line 477
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 477
        None  # line 478

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 480
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 481
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 482
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 482
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 483
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 484
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 485
        if pinfo.size == 0:  # line 486
            with open(encode(target), "wb"):  # line 487
                pass  # line 487
            try:  # update access/modification timestamps on file system  # line 488
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 488
            except Exception as E:  # line 489
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 489
            return None  # line 490
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 491
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 493
            while True:  # line 494
                buffer = fd.read(bufSize)  # line 495
                to.write(buffer)  # line 496
                if len(buffer) < bufSize:  # line 497
                    break  # line 497
        try:  # update access/modification timestamps on file system  # line 498
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 498
        except Exception as E:  # line 499
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 499
        return None  # line 500


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], remotes: 'List[str]'=[]):  # line 504
    ''' Initial command to start working offline. '''  # line 505
    if os.path.exists(encode(metaFolder)):  # line 506
        if '--force' not in options:  # line 507
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 507
        try:  # throw away all previous metadata before going offline  # line 508
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 509
                resource = metaFolder + os.sep + entry  # line 510
                if os.path.isdir(resource):  # line 511
                    shutil.rmtree(encode(resource))  # line 511
                else:  # line 512
                    os.unlink(encode(resource))  # line 512
        except:  # line 513
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder)  # line 513
    for remote in remotes:  # line 514
        try:  # line 515
            os.makedirs(os.path.join(remote, metaFolder))  # line 515
        except Exception as E:  # line 516
            error("Creating remote repository metadata in %s" % remote)  # line 516
    m = Metadata(offline=True, remotes=remotes)  # type: Metadata  # line 517
    if '--strict' in options or m.c.strict:  # always hash contents  # line 518
        m.strict = True  # always hash contents  # line 518
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 519
        m.compress = True  # plain file copies instead of compressed ones  # line 519
    if '--picky' in options or m.c.picky:  # Git-like  # line 520
        m.picky = True  # Git-like  # line 520
    elif '--track' in options or m.c.track:  # Svn-like  # line 521
        m.track = True  # Svn-like  # line 521
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 522
    if title:  # line 523
        printo(title)  # line 523
    if verbose:  # line 524
        info(usage.MARKER + "Going offline...")  # line 524
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 525
    m.branch = 0  # line 526
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 527
    if verbose or '--verbose' in options:  # line 528
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 528
    info(usage.MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 529

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 531
    ''' Finish working offline. '''  # line 532
    if verbose:  # line 533
        info(usage.MARKER + "Going back online...")  # line 533
    force = '--force' in options  # type: bool  # line 534
    m = Metadata()  # type: Metadata  # line 535
    strict = '--strict' in options or m.strict  # type: bool  # line 536
    m.loadBranches()  # line 537
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 538
        Exit("There are still unsynchronized (modified) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 538
    m.loadBranch(m.branch)  # line 539
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 540
    if options.count("--force") < 2:  # line 541
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 542
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 543
        if modified(changed):  # line 544
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 548
    try:  # line 549
        shutil.rmtree(encode(metaFolder))  # line 549
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 549
    except Exception as E:  # line 550
        Exit("Error removing offline repository: %r" % E)  # line 550
    info(usage.MARKER + "Offline repository removed, you're back online")  # line 551

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 553
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not necessary, as either branching from last  revision anyway, or branching file tree anyway.
  '''  # line 556
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 557
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 558
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 559
    m = Metadata()  # type: Metadata  # line 560
    m.loadBranch(m.branch)  # line 561
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 562
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 563
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 563
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 564
    if verbose:  # line 565
        info(usage.MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 565
    if last:  # branch from last revision  # line 566
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 566
    else:  # branch from current file tree state  # line 567
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 567
    if not stay:  # line 568
        m.branch = branch  # line 568
    m.saveBranches()  # TODO #253 or indent again?  # line 569
    info(usage.MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 570

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 572
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 573
    m = Metadata()  # type: Metadata  # line 574
    branch = None  # type: _coconut.typing.Optional[int]  # line 574
    revision = None  # type: _coconut.typing.Optional[int]  # line 574
    strict = '--strict' in options or m.strict  # type: bool  # line 575
    branch, revision = m.parseRevisionString(argument)  # line 576
    if branch not in m.branches:  # line 577
        Exit("Unknown branch")  # line 577
    m.loadBranch(branch)  # knows commits  # line 578
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 579
    if verbose:  # line 580
        info(usage.MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 580
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 581
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 582
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 587
    return changed  # returning for unit tests only TODO #254 remove?  # line 588

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False):  # TODO #255 introduce option to diff against committed revision  # line 590
    ''' The diff display code. '''  # line 591
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 592
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 593
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 594
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 595
        content = b""  # type: _coconut.typing.Optional[bytes]  # line 596
        if pinfo.size != 0:  # versioned file  # line 597
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 597
            assert content is not None  # versioned file  # line 597
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current file  # line 598
        blocks = None  # type: List[MergeBlock]  # line 599
        nl = None  # type: bytes  # line 599
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 600
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 601
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 602
        for block in blocks:  # line 603
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # TODO #256 show color via (n)curses or other library?  # line 606
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 607
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 607
            elif block.tipe == MergeBlockType.REMOVE:  # line 608
                for no, line in enumerate(block.lines):  # line 609
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 609
            elif block.tipe == MergeBlockType.REPLACE:  # line 610
                for no, line in enumerate(block.replaces.lines):  # line 611
                    printo(wrap("-~- %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 611
                for no, line in enumerate(block.lines):  # line 612
                    printo(wrap("+~+ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 612
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 615
                printo()  # line 615

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 617
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 618
    m = Metadata()  # type: Metadata  # line 619
    branch = None  # type: _coconut.typing.Optional[int]  # line 619
    revision = None  # type: _coconut.typing.Optional[int]  # line 619
    strict = '--strict' in options or m.strict  # type: bool  # line 620
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 621
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 622
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 623
    if branch not in m.branches:  # line 624
        Exit("Unknown branch")  # line 624
    m.loadBranch(branch)  # knows commits  # line 625
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 626
    if verbose:  # line 627
        info(usage.MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 627
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 628
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 629
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap)  # line 634

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 636
    ''' Create new revision from file tree changes vs. last commit. '''  # line 637
    m = Metadata()  # type: Metadata  # line 638
    if argument is not None and argument in m.tags:  # line 639
        Exit("Illegal commit message. It was already used as a tag name")  # line 639
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 640
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 642
        Exit("No file patterns staged for commit in picky mode")  # line 642
    if verbose:  # line 643
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 643
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 644
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 645
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 646
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 647
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 648
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 649
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 650
    m.saveBranch(m.branch)  # line 651
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 652
    if m.picky:  # remove tracked patterns  # line 653
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 653
    else:  # track or simple mode: set branch modified  # line 654
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 654
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 655
        m.tags.append(argument)  # memorize unique tag  # line 655
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 655
    m.saveBranches()  # line 656
    stored = 0  # type: int  # now determine new commit size on file system  # line 657
    overhead = 0  # type: int  # now determine new commit size on file system  # line 657
    count = 0  # type: int  # now determine new commit size on file system  # line 657
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 658
    for file in os.listdir(commitFolder):  # line 659
        try:  # line 660
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 661
            if file == metaFile:  # line 662
                overhead += newsize  # line 662
            else:  # line 663
                stored += newsize  # line 663
                count += 1  # line 663
        except Exception as E:  # line 664
            error(E)  # line 664
    printo(usage.MARKER_COLOR + "Created new revision r%02d%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%s%s%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, (" '%s'" % argument) if argument is not None else "", Fore.GREEN, Fore.RESET, len(changed.additions) - len(changed.moves), Fore.RED, Fore.RESET, len(changed.deletions) - len(changed.moves), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(changed.modifications), Fore.BLUE + Style.BRIGHT, MOVE_SYMBOL if m.c.useUnicodeFont else "#", Style.RESET_ALL, len(changed.moves), ("%.2f MiB" % ((stored + overhead) / MEBI)) if stored > 1.25 * MEBI else (("%.2f Kib" % ((stored + overhead) / KIBI)) if stored > 1.25 * KIBI else ("%d bytes" % (stored + overhead))), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 665

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 675
    ''' Show branches and current repository state. '''  # line 676
    m = Metadata()  # type: Metadata  # line 677
    if not (m.c.useChangesCommand or '--repo' in options):  # line 678
        changes(argument, options, onlys, excps)  # line 678
        return  # line 678
    current = m.branch  # type: int  # line 679
    strict = '--strict' in options or m.strict  # type: bool  # line 680
    printo(usage.MARKER_COLOR + "Offline repository status")  # line 681
    printo("Repository root:     %s" % os.getcwd())  # line 682
    printo("Underlying VCS root: %s" % vcs)  # line 683
    printo("Underlying VCS type: %s" % cmd)  # line 684
    printo("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 685
    printo("Current SOS version: %s" % version.__version__)  # line 686
    printo("At creation version: %s" % m.version)  # line 687
    printo("Metadata format:     %s" % m.format)  # line 688
    printo("Content checking:    %sactivated%s" % (Fore.CYAN if m.strict else Fore.BLUE + "de", Fore.RESET))  # line 689
    printo("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 690
    printo("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 691
    printo("Number of branches:  %d" % len(m.branches))  # line 692
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 693
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 694
    m.loadBranch(current)  # line 695
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 696
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 697
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 697
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 698
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of symbols for changed vs. unchanged  # line 703
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 707
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 708
        payload = 0  # type: int  # count used storage per branch  # line 709
        overhead = 0  # type: int  # count used storage per branch  # line 709
        original = 0  # type: int  # count used storage per branch  # line 709
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 710
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 711
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 712
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 712
                else:  # line 713
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 713
        pl_amount = float(payload) / MEBI  # type: float  # line 714
        oh_amount = float(overhead) / MEBI  # type: float  # line 714
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 716
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 717
            m.loadCommit(m.branch, commit_)  # line 718
            for pinfo in m.paths.values():  # line 719
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 719
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 720
        printo("  %s b%d%s @%s (%s%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), Fore.RESET, len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 721
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 732
        printo("\nTracked file patterns:")  # TODO #261 print matching untracking patterns side-by-side?  # line 733
        printo(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 734
        printo("\nUntracked file patterns:")  # line 735
        printo(ajoin("  | ", m.branches[m.branch].untracked, "\n"))  # line 736

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 738
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 745
    assert not (check and commit)  # line 746
    m = Metadata()  # type: Metadata  # line 747
    force = '--force' in options  # type: bool  # line 748
    strict = '--strict' in options or m.strict  # type: bool  # line 749
    if argument is not None:  # line 750
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 751
        if branch is None:  # line 752
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 752
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 753
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 754

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 757
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 758
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 759
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 760
    if check and modified(changed) and not force:  # line 765
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 766
        Exit("File tree contains changes. Use --force to proceed")  # line 767
    elif commit:  # line 768
        if not modified(changed) and not force:  # line 769
            Exit("Nothing to commit")  # line 769
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 770
        if msg:  # line 771
            printo(msg)  # line 771

    if argument is not None:  # branch/revision specified  # line 773
        m.loadBranch(branch)  # knows commits of target branch  # line 774
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 775
        revision = m.correctNegativeIndexing(revision)  # line 776
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 777
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 778

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 780
    ''' Continue work on another branch, replacing file tree changes. '''  # line 781
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 782
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 783

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 786
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 787
    else:  # full file switch  # line 788
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 789
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 790

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 797
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 798
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 799
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 800
                rms.append(a)  # line 800
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 801
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 801
        if modified(changed) and not force:  # line 802
            m.listChanges(changed, cwd)  # line 802
            Exit("File tree contains changes. Use --force to proceed")  # line 802
        if verbose:  # line 803
            info(usage.MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 803
        if not modified(todos):  # line 804
            info("No changes to current file tree")  # line 805
        else:  # integration required  # line 806
            for path, pinfo in todos.deletions.items():  # line 807
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 808
                printo("ADD " + path, color=Fore.GREEN)  # line 809
            for path, pinfo in todos.additions.items():  # line 810
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 811
                printo("DEL " + path, color=Fore.RED)  # line 812
            for path, pinfo in todos.modifications.items():  # line 813
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 814
                printo("MOD " + path, color=Fore.YELLOW)  # line 815
    m.branch = branch  # line 816
    m.saveBranches()  # store switched path info  # line 817
    info(usage.MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 818

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 820
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 824
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 825
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 826
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 827
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 828
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 829
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 830
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 831
    if verbose:  # line 832
        info(usage.MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 832

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 835
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 836
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 837
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 838
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 843
        if trackingUnion != trackingPatterns:  # nothing added  # line 844
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 845
        else:  # line 846
            info("Nothing to update")  # but write back updated branch info below  # line 847
    else:  # integration required  # line 848
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 849
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 849
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 849
        if changed.deletions.items():  # line 850
            printo("Additions:")  # line 850
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 851
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 852
            if add_all is None and mrg == MergeOperation.ASK:  # line 853
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 854
                if selection in "ao":  # line 855
                    add_all = "y" if selection == "a" else "n"  # line 855
                    selection = add_all  # line 855
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 856
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 856
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path, color=Fore.GREEN)  # TODO document (A) as "selected not to add by user choice"  # line 857
        if changed.additions.items():  # line 858
            printo("Deletions:")  # line 858
        for path, pinfo in changed.additions.items():  # line 859
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 860
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 860
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 861
            if del_all is None and mrg == MergeOperation.ASK:  # line 862
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 863
                if selection in "ao":  # line 864
                    del_all = "y" if selection == "a" else "n"  # line 864
                    selection = del_all  # line 864
            if "y" in (del_all, selection):  # line 865
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 865
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path, color=Fore.RED)  # not contained in other branch, but maybe kept  # line 866
        if changed.modifications.items():  # line 867
            printo("Modifications:")  # line 867
        for path, pinfo in changed.modifications.items():  # line 868
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 869
            binary = not m.isTextType(path)  # type: bool  # line 870
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 871
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 872
                printo(("MOD " if not binary else "BIN ") + path, color=Fore.YELLOW)  # TODO print mtime, size differences?  # line 873
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 874
            if op == "t":  # line 875
                printo("THR " + path, color=Fore.MAGENTA)  # blockwise copy of contents  # line 876
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 876
            elif op == "m":  # line 877
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 878
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 878
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 879
                if current == file and verbose:  # line 880
                    info("No difference to versioned file")  # line 880
                elif file is not None:  # if None, error message was already logged  # line 881
                    merged = None  # type: bytes  # line 882
                    nl = None  # type: bytes  # line 882
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 883
                    if merged != current:  # line 884
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 885
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 885
                    elif verbose:  # TODO but update timestamp?  # line 886
                        info("No change")  # TODO but update timestamp?  # line 886
            else:  # mine or wrong input  # line 887
                printo("MNE " + path, color=Fore.CYAN)  # nothing to do! same as skip  # line 888
    info(usage.MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 889
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 890
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 891
    m.saveBranches()  # line 892

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 894
    ''' Remove a branch entirely. '''  # line 895
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 896
    if len(m.branches) == 1:  # line 897
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 897
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 898
    if branch is None or branch not in m.branches:  # line 899
        Exit("Cannot delete unknown branch %r" % branch)  # line 899
    if verbose:  # line 900
        info(usage.MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 900
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 901
    info(usage.MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 902

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 904
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 905
    force = '--force' in options  # type: bool  # line 906
    m = Metadata()  # type: Metadata  # line 907
    if not (m.track or m.picky):  # line 908
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 908
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 909
    if pattern in patterns:  # line 910
        Exit("Pattern '%s' already tracked" % pattern)  # line 910
    if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 911
        Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 911
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 912
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 913
    patterns.append(pattern)  # line 914
    m.saveBranches()  # line 915
    info(usage.MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # TODO #262 display relative path by default?  # line 916

def remove(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 918
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 919
    m = Metadata()  # type: Metadata  # line 920
    if not (m.track or m.picky):  # line 921
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 921
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 922
    if pattern not in patterns:  # line 923
        suggestion = _coconut.set()  # type: Set[str]  # line 924
        for pat in patterns:  # line 925
            if fnmatch.fnmatch(pattern, pat):  # line 925
                suggestion.add(pat)  # line 925
        if suggestion:  # TODO use same wording as in move  # line 926
            printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 926
        Exit("Tracked pattern '%s' not found" % pattern)  # line 927
    patterns.remove(pattern)  # line 928
    m.saveBranches()  # line 929
    info(usage.MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 930

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 932
    ''' List specified directory, augmenting with repository metadata. '''  # line 933
    m = Metadata()  # type: Metadata  # line 934
    folder = (os.getcwd() if folder is None else folder)  # line 935
    if '--all' in options:  # always start at SOS repo root with --all  # line 936
        folder = m.root  # always start at SOS repo root with --all  # line 936
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 937
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 938
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 939
    if verbose:  # line 940
        info(usage.MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 940
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 941
    if relPath.startswith(os.pardir):  # line 942
        Exit("Cannot list contents of folder outside offline repository")  # line 942
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 943
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 944
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 945
        if len(m.tags) > 0:  # line 946
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 946
        return  # line 947
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 948
        if not recursive:  # avoid recursion  # line 949
            dirnames.clear()  # avoid recursion  # line 949
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 950
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 951

        folder = decode(dirpath)  # line 953
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 954
        if patterns:  # line 955
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 956
            if out:  # line 957
                printo("DIR %s\n" % relPath + out)  # line 957
            continue  # with next folder  # line 958
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 959
        if len(files) > 0:  # line 960
            printo("DIR %s" % relPath)  # line 960
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 961
            ignore = None  # type: _coconut.typing.Optional[str]  # line 962
            for ig in m.c.ignores:  # remember first match  # line 963
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 963
                    ignore = ig  # remember first match  # line 963
                    break  # remember first match  # line 963
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 964
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 964
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 964
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 964
                        break  # found a white list entry for ignored file, undo ignoring it  # line 964
            matches = []  # type: List[str]  # line 965
            if not ignore:  # line 966
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 967
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 968
                        matches.append(os.path.basename(pattern))  # line 968
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 969
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 970

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 972
    ''' List previous commits on current branch. '''  # line 973
    changes_ = "--changes" in options  # type: bool  # line 974
    diff_ = "--diff" in options  # type: bool  # line 975
    m = Metadata()  # type: Metadata  # line 976
    m.loadBranch(m.branch)  # knows commit history  # line 977
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # line 978
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 979
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 980
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 981
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 982
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 983
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 984
    commit = None  # type: CommitInfo  # line 985
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 986
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 987
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 988
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 989
    for no in range(maxi + 1):  # line 990
        if indicator:  # line 991
            printo("  %%s %%0%dd" % digits % (indicator.getIndicator(), no), nl="\r")  # line 991
        if no in m.commits:  # line 992
            commit = m.commits[no]  # line 992
        else:  # line 993
            if n.branch != n.getParentBranch(m.branch, no):  # line 994
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 994
            commit = n.commits[no]  # line 995
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 996
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 997
        if "--all" in options or no >= lastno:  # line 998
            if no >= lastno:  # line 999
                indicator = None  # line 999
            _add = news - olds  # type: FrozenSet[str]  # line 1000
            _del = olds - news  # type: FrozenSet[str]  # line 1001
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 1003
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 1005
            printo("  %s r%s @%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%sT%s%02d) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, Fore.RESET, len(_add), Fore.RED, Fore.RESET, len(_del), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(_mod), Fore.CYAN, Fore.RESET, _txt, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 1006
            if changes_:  # line 1007
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}), root=cwd if '--relative' in options else None)  # TODO moves detection?  # line 1018
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 1019
                pass  #  _diff(m, changes)  # needs from revision diff  # line 1019
        olds = news  # replaces olds for next revision compare  # line 1020
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 1021

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 1023
    ''' Exported entire repository as archive for easy transfer. '''  # line 1024
    if verbose:  # line 1025
        info(usage.MARKER + "Dumping repository to archive...")  # line 1025
    m = Metadata()  # type: Metadata  # to load the configuration  # line 1026
    progress = '--progress' in options  # type: bool  # line 1027
    delta = '--full' not in options  # type: bool  # line 1028
    skipBackup = '--skip-backup' in options  # type: bool  # line 1029
    import functools  # line 1030
    import locale  # line 1030
    import warnings  # line 1030
    import zipfile  # line 1030
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 1031
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 1031
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 1031
    except:  # line 1032
        compression = zipfile.ZIP_STORED  # line 1032

    if argument is None:  # line 1034
        Exit("Argument missing (target filename)")  # line 1034
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 1035
    entries = []  # type: List[str]  # line 1036
    if os.path.exists(encode(argument)) and not skipBackup:  # line 1037
        try:  # line 1038
            if verbose:  # line 1039
                info("Creating backup...")  # line 1039
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 1040
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 1041
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 1041
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 1041
        except Exception as E:  # line 1042
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 1042
    if verbose:  # line 1043
        info("Dumping revisions...")  # line 1043
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1044
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1044
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1045
        _zip.debug = 0  # suppress debugging output  # line 1046
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1047
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1048
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1049
        totalsize = 0  # type: int  # line 1050
        start_time = time.time()  # type: float  # line 1051
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1052
            dirpath = decode(dirpath)  # line 1053
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1054
                continue  # don't backup backups  # line 1054
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1055
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1056
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1057
            for filename in filenames:  # line 1058
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1059
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1060
                totalsize += os.stat(encode(abspath)).st_size  # line 1061
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1062
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1063
                    continue  # don't backup backups  # line 1063
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1064
                    if show:  # line 1065
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1065
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1066
        if delta:  # line 1067
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1067
    info("\r" + pure.ljust(usage.MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1068

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1070
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1071
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1072
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1073
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1073
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1074
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1075
    if maxi is None:  # line 1076
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1076
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1077
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1080
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1082
    while files:  # line 1083
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1084
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1085
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1087
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1087
    tracked = None  # type: bool  # line 1088
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1088
    tracked, commitArgs = vcsCommits[cmd]  # line 1088
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1089
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1091
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1091
    if tracked:  # line 1092
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1092

def config(arguments: 'List[str]', options: 'List[str]'=[]):  # line 1094
    command = None  # type: str  # line 1095
    key = None  # type: str  # line 1095
    value = None  # type: str  # line 1095
    v = None  # type: str  # line 1095
    command, key, value = (arguments + [None] * 2)[:3]  # line 1096
    if command is None:  # line 1097
        usage.usage("help", verbose=True)  # line 1097
    if command not in ["set", "unset", "show", "list", "add", "rm"]:  # line 1098
        Exit("Unknown config command")  # line 1098
    local = "--local" in options  # type: bool  # line 1099
    m = Metadata()  # type: Metadata  # loads layered configuration as well. TODO warning if repo not exists  # line 1100
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1101
    if command == "set":  # line 1102
        if None in (key, value):  # line 1103
            Exit("Key or value not specified")  # line 1103
        if key not in (([] if local else CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1104
            Exit("Unsupported key for %s configuration %r" % ("local " if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1104
        if key in CONFIGURABLE_FLAGS and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1105
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1105
        c[key] = value.lower() in TRUTH_VALUES if key in CONFIGURABLE_FLAGS else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1106
    elif command == "unset":  # line 1107
        if key is None:  # line 1108
            Exit("No key specified")  # line 1108
        if key not in c.keys():  # HINT: Works on local configurations when used with --local  # line 1109
            Exit("Unknown key")  # HINT: Works on local configurations when used with --local  # line 1109
        del c[key]  # line 1110
    elif command == "add":  # line 1111
        if None in (key, value):  # line 1112
            Exit("Key or value not specified")  # line 1112
        if key not in CONFIGURABLE_LISTS:  # line 1113
            Exit("Unsupported key %r" % key)  # line 1113
        if key not in c.keys():  # prepare empty list, or copy from global, add new value below  # line 1114
            c[key] = [_ for _ in c.__defaults[key]] if local else []  # prepare empty list, or copy from global, add new value below  # line 1114
        elif value in c[key]:  # line 1115
            Exit("Value already contained, nothing to do")  # line 1115
        if ";" in value:  # line 1116
            c[key].append(removePath(key, value))  # line 1116
        else:  # line 1117
            c[key].extend([removePath(key, v) for v in value.split(";")])  # line 1117
    elif command == "rm":  # line 1118
        if None in (key, value):  # line 1119
            Exit("Key or value not specified")  # line 1119
        if key not in c.keys():  # line 1120
            Exit("Unknown key %r" % key)  # line 1120
        if value not in c[key]:  # line 1121
            Exit("Unknown value %r" % value)  # line 1121
        c[key].remove(value)  # line 1122
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1123
            del c[key]  # remove local entry, to fallback to global  # line 1123
    else:  # Show or list  # line 1124
        if key == "ints":  # list valid configuration items  # line 1125
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1125
        elif key == "flags":  # line 1126
            printo(", ".join(CONFIGURABLE_FLAGS))  # line 1126
        elif key == "lists":  # line 1127
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1127
        elif key == "texts":  # line 1128
            printo(", ".join([_ for _ in defaults.keys() if _ not in (CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS)]))  # line 1128
        else:  # line 1129
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1130
            c = m.c  # always use full configuration chain  # line 1131
            try:  # attempt single key  # line 1132
                assert key is not None  # force exception  # line 1133
                c[key]  # force exception  # line 1133
                l = key in c.keys()  # type: bool  # line 1134
                g = key in c.__defaults.keys()  # type: bool  # line 1134
                printo("%s %s %r" % (key.rjust(20), out[3] if not (l or g) else (out[1] if l else out[2]), c[key]))  # line 1135
            except:  # normal value listing  # line 1136
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # line 1137
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1138
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1139
                for k, vt in sorted(vals.items()):  # line 1140
                    printo("%s %s %s" % (k.rjust(20), out[vt[1]], vt[0]))  # line 1140
                if len(c.keys()) == 0:  # line 1141
                    info("No local configuration stored")  # line 1141
                if len(c.__defaults.keys()) == 0:  # line 1142
                    info("No global configuration stored")  # line 1142
        return  # in case of list, no need to store anything  # line 1143
    if local:  # saves changes of repoConfig  # line 1144
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1144
        m.saveBranches()  # saves changes of repoConfig  # line 1144
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1144
    else:  # global config  # line 1145
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1146
        if f is None:  # TODO why no exit here?  # line 1147
            error("Error saving user configuration: %r" % h)  # TODO why no exit here?  # line 1147
        else:  # line 1148
            Exit("OK", code=0)  # line 1148

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1150
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1153
    if verbose:  # line 1154
        info(usage.MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1154
    force = '--force' in options  # type: bool  # line 1155
    soft = '--soft' in options  # type: bool  # line 1156
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1157
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1157
    m = Metadata()  # type: Metadata  # line 1158
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1159
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1160
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1161
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1162
    if not matching and not force:  # line 1163
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1163
    if not (m.track or m.picky):  # line 1164
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 1164
    if pattern not in patterns:  # list potential alternatives and exit  # line 1165
        for tracked in (t for t in patterns if os.path.dirname(t) == relPath):  # for all patterns of the same source folder TODO use SLASH rindex  # line 1166
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1167
            if alternative:  # line 1168
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1168
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: if not (force or soft):  # line 1169
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1170
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1171
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1172
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1176
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1177
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1177
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1178
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1179
    if len({st[1] for st in matches}) != len(matches):  # line 1180
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1180
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1181
    if os.path.exists(encode(newRelPath)):  # line 1182
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1183
        if exists and not (force or soft):  # line 1184
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1184
    else:  # line 1185
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1185
    if not soft:  # perform actual renaming  # line 1186
        for (source, target) in matches:  # line 1187
            try:  # line 1188
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1188
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1189
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1189
    patterns[patterns.index(pattern)] = newPattern  # line 1190
    m.saveBranches()  # line 1191

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1193
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1194
    debug("Parsing command-line arguments...")  # line 1195
    root = os.getcwd()  # line 1196
    try:  # line 1197
        onlys, excps, remotes = parseArgumentOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1198
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1199
        arguments = [c.strip() for c in sys.argv[2:] if not (c.startswith("-") and (len(c) == 2 or c[1] == "-"))]  # type: List[_coconut.typing.Optional[str]]  # line 1200
        options = [c.strip() for c in sys.argv[2:] if c.startswith("-") and (len(c) == 2 or c[1] == "-")]  # options with arguments have to be parsed from sys.argv  # line 1201
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1202
        if command[:1] in "amr":  # line 1203
            relPath, pattern = relativize(root, os.path.join(cwd, arguments[0] if arguments else "."))  # line 1203
        if command[:1] == "m":  # line 1204
            if len(arguments) < 2:  # line 1205
                Exit("Need a second file pattern argument as target for move command")  # line 1205
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1206
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1207
        if command[:1] == "a":  # e.g. addnot  # line 1208
            add(relPath, pattern, options, negative="n" in command)  # e.g. addnot  # line 1208
        elif command[:1] == "b":  # line 1209
            branch(arguments[0], arguments[1], options)  # line 1209
        elif command[:3] == "com":  # line 1210
            commit(arguments[0], options, onlys, excps)  # line 1210
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1211
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1211
        elif command[:2] == "ci":  # line 1212
            commit(arguments[0], options, onlys, excps)  # line 1212
        elif command[:3] == 'con':  # line 1213
            config(arguments, options)  # line 1213
        elif command[:2] == "de":  # line 1214
            destroy(arguments[0], options)  # line 1214
        elif command[:2] == "di":  # line 1215
            diff(arguments[0], options, onlys, excps)  # line 1215
        elif command[:2] == "du":  # line 1216
            dump(arguments[0], options)  # line 1216
        elif command[:1] == "h":  # line 1217
            usage.usage(arguments[0], verbose=verbose)  # line 1217
        elif command[:2] == "lo":  # line 1218
            log(options, cwd)  # line 1218
        elif command[:2] == "li":  # line 1219
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1219
        elif command[:2] == "ls":  # line 1220
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1220
        elif command[:1] == "m":  # e.g. mvnot  # line 1221
            move(relPath, pattern, newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1221
        elif command[:2] == "of":  # line 1222
            offline(arguments[0], arguments[1], options, remotes)  # line 1222
        elif command[:2] == "on":  # line 1223
            online(options)  # line 1223
        elif command[:1] == "p":  # line 1224
            publish(arguments[0], cmd, options, onlys, excps)  # line 1224
        elif command[:1] == "r":  # e.g. rmnot  # line 1225
            remove(relPath, pattern, optoions, negative="n" in command)  # e.g. rmnot  # line 1225
        elif command[:2] == "st":  # line 1226
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1226
        elif command[:2] == "sw":  # line 1227
            switch(arguments[0], options, onlys, excps, cwd)  # line 1227
        elif command[:1] == "u":  # line 1228
            update(arguments[0], options, onlys, excps)  # line 1228
        elif command[:1] == "v":  # line 1229
            usage.usage(arguments[0], version=True)  # line 1229
        else:  # line 1230
            Exit("Unknown command '%s'" % command)  # line 1230
        Exit(code=0)  # regular exit  # line 1231
    except (Exception, RuntimeError) as E:  # line 1232
        exception(E)  # line 1233
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing")  # line 1234

def main():  # line 1236
    global debug, info, warn, error  # to modify logger  # line 1237
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1238
    _log = Logger(logging.getLogger(__name__))  # line 1239
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1239
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1240
        sys.argv.remove(option)  # clean up program arguments  # line 1240
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1241
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1241
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1242
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1243
    debug("Detected SOS root folder: %s\nDetected VCS root folder: %s" % (("-" if root is None else root), ("-" if vcs is None else vcs)))  # line 1244
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1245
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1246
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv"):  # in offline mode or just going offline TODO what about git config?  # line 1247
        cwd = os.getcwd()  # line 1248
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1249
        parse(vcs, cwd, cmd)  # line 1250
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1251
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1252
        import subprocess  # only required in this section  # line 1253
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1254
        inp = ""  # type: str  # line 1255
        while True:  # line 1256
            so, se = process.communicate(input=inp)  # line 1257
            if process.returncode is not None:  # line 1258
                break  # line 1258
            inp = sys.stdin.read()  # line 1259
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1260
            if root is None:  # line 1261
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1261
            m = Metadata(root)  # type: Metadata  # line 1262
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1263
            m.saveBranches()  # line 1264
    else:  # line 1265
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1265


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: bool  # this is a trick allowing to modify the flags from the test suite  # line 1269
force_vcs = [None] if '--vcs' in sys.argv else []  # type: bool  # line 1270
verbose = [None] if '--verbose' in sys.argv or '-v' in sys.argv else []  # type: bool  # imported from utility, and only modified here  # line 1271
debug_ = [None] if os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv else []  # type: bool  # line 1272
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1273

_log = Logger(logging.getLogger(__name__))  # line 1275
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1275

if __name__ == '__main__':  # line 1277
    main()  # line 1277
