#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x77128f18

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
        _.loadBranches(offline=offline, remotes=remotes)  # loads above values from repository, or uses application defaults  # line 63

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
#      branches:List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)
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
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # hide warning only when going offline  # line 128

    def saveBranches(_, also: 'Dict[str, Any]'={}):  # line 130
        ''' Save list of branches and current branch info to metadata file. '''  # line 131
        store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT, "remotes": _.remotes}  # type: Dict[str, Any]  # dictionary of repository settings (while _.repoConf stores user settings)  # line 132
        store.update(also)  # allows overriding certain values at certain points in time  # line 137
        for remote in [None] + _.remotes:  # line 138
            tryOrIgnore(lambda: shutil.copy2(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), encode(os.path.join((_.root if remote is None else remote), metaFolder, metaBack))))  # backup  # line 139
            try:  # line 140
                with codecs.open(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 140
                    json.dump((store, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints, fd knows how to encode them  # line 141
            except Exception as E:  # line 142
                error("Error saving branches%s" % ((" to remote path " + remote) if remote else ""))  # line 142

    def getRevisionByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 144
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 145
        if name == "":  # line 146
            return -1  # line 146
        try:  # attempt to parse integer string  # line 147
            return int(name)  # attempt to parse integer string  # line 147
        except ValueError:  # line 148
            pass  # line 148
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 149
        return found[0] if found else None  # line 150

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 152
        ''' Convenience accessor for named branches. '''  # line 153
        if name == "":  # current  # line 154
            return _.branch  # current  # line 154
        try:  # attempt to parse integer string  # line 155
            return int(name)  # attempt to parse integer string  # line 155
        except ValueError:  # line 156
            pass  # line 156
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 157
        return found[0] if found else None  # line 158

    def loadBranch(_, branch: 'int'):  # line 160
        ''' Load all commit information from a branch meta data file. '''  # line 161
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 162
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 163
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 164
        _.branch = branch  # line 165

    def saveBranch(_, branch: 'int'):  # line 167
        ''' Save all commits to a branch meta data file. '''  # line 168
        for remote in [None] + _.remotes:  # line 169
            tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile, base=remote)), encode(branchFolder(branch, file=metaBack, base=remote))))  # backup  # line 170
            try:  # line 171
                with codecs.open(encode(branchFolder(branch, file=metaFile, base=remote)), "w", encoding=UTF8) as fd:  # line 171
                    json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 172
            except Exception as E:  # line 173
                error("Error saving branch%s" % ((" to remote path " + remote) if remote else ""))  # line 173

    def duplicateBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 175
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 183
        if verbose:  # line 184
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 184
        now = int(time.time() * 1000)  # type: int  # line 185
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 186
        revision = max(_.commits) if _.commits else 0  # type: int  # line 187
        _.commits.clear()  # line 188
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 189
        for remote in [None] + _.remotes:  # line 194
            tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)) if full else branchFolder(branch, base=(_.root if remote is None else remote)))), lambda e: error("Duplicating remote branch folder %r" % remote))  # line 195
        if full:  # not fast branching via reference - copy all current files to new branch  # line 196
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 197
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 198
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 198
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit  # line 199
            _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 200
        _.saveBranch(branch)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 201
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 202

    def createBranch(_, branch: 'int', name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 204
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 210
        now = int(time.time() * 1000)  # type: int  # line 211
        simpleMode = not (_.track or _.picky)  # line 212
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 213
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 214
        if verbose:  # line 215
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 215
        _.paths = {}  # type: Dict[str, PathInfo]  # line 216
        if simpleMode:  # branches from file system state. not necessary to create branch folder, as it is done in findChanges below anyway  # line 217
            changed, msg = _.findChanges(branch, 0, progress=simpleMode)  # HINT creates revision folder and versioned files!  # line 218
            _.listChanges(changed)  # line 219
            if msg:  # display compression factor and time taken  # line 220
                printo(msg)  # display compression factor and time taken  # line 220
            _.paths.update(changed.additions.items())  # line 221
        else:  # tracking or picky mode: branch from latest revision  # line 222
            for remote in [None] + _.remotes:  # line 223
                tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)))), lambda e: error("Creating remote branch folder %r" % remote))  # line 224
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 225
                _.loadBranch(_.branch)  # line 226
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO #245 what if last switch was to an earlier revision? no persisting of last checkout  # line 227
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 228
                for path, pinfo in _.paths.items():  # line 229
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 229
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 230
        _.saveBranch(branch)  # save branch meta data (revisions) to branch folder  # line 231
        _.saveCommit(branch, 0)  # save commit meta data to revision folder  # line 232
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 233

    def removeBranch(_, branch: 'int') -> 'BranchInfo':  # line 235
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 238
        import collections  # used almost only here  # line 239
        binfo = None  # type: BranchInfo  # typing info  # line 240
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 241
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 242
        if deps:  # need to copy all parent revisions to dependent branches first  # line 243
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 244
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 245
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 246
                for dep, _rev in deps:  # line 247
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO #246 align placement of indicator with other uses of progress  # line 248
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 249
#          if rev in _.commits:  # TODO #247 uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 251
                    shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 252
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 253
                for rev in range(minrev + 1, _rev + 1):  # line 254
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 255
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 256
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 257
                        newcommits[dep][rev] = _.commits[rev]  # line 258
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=_.root)), encode(revisionFolder(dep, rev, base=_.root)))  # line 259
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 260
        printo(pure.ljust() + "\r")  # clean line output  # line 261
        tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch) + BACKUP_SUFFIX)))  # remove previous backup first  # line 262
        tryOrIgnore(lambda: os.rename(encode(branchFolder(branch)), encode(branchFolder(branch) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?"))  # line 263
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 264
        del _.branches[branch]  # line 265
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 266
        _.saveBranches()  # persist modified branches list  # line 267
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 268
            _.commits = commits  # line 269
            _.saveBranch(branch)  # line 270
        _.commits.clear()  # clean memory  # line 271
        return binfo  # line 272

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 274
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 275
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 276
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 277
            _.paths = json.load(fd)  # line 277
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 278
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 279

    def saveCommit(_, branch: 'int', revision: 'int'):  # line 281
        ''' Save all file information to a commit meta data file. '''  # line 282
        for remote in [None] + _.remotes:  # line 283
            try:  # line 284
                target = revisionFolder(branch, revision, base=(_.root if remote is None else remote))  # type: str  # line 285
                tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 286
                tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 287
                with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 288
                    json.dump(_.paths, fd, ensure_ascii=False)  # line 288
            except Exception as E:  # line 289
                error("Error saving commit%s" % ((" to remote path " + remote) if remote else ""))  # line 289

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 291
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly)
        progress: Show file names during processing
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
    '''  # line 300
        import collections  # used only in this method  # line 301
        write = branch is not None and revision is not None  # used for writing commits  # line 302
        if write:  # line 303
            for remote in [None] + _.remotes:  # line 303
                tryOrIgnore(lambda: os.makedirs(encode(revisionFolder(branch, revision, base=(_.root if remote is None else remote)))))  # line 304
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # WARN this code needs explicity argument passing for initialization due to mypy problems with default arguments  # line 305
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 306
        hashed = None  # type: _coconut.typing.Optional[str]  # line 307
        written = None  # type: int  # line 307
        compressed = 0  # type: int  # line 307
        original = 0  # type: int  # line 307
        start_time = time.time()  # type: float  # line 307
        knownPaths = {}  # type: Dict[str, List[str]]  # line 308

# Find relevant folders/files that match specified folder/glob patterns for exclusive inclusion or exclusion
        byFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 311
        onlyByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 312
        dontByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 313
        for path, pinfo in _.paths.items():  # line 314
            if pinfo is None:  # quicker than generator expression above  # line 315
                continue  # quicker than generator expression above  # line 315
            slash = path.rindex(SLASH)  # type: int  # line 316
            byFolder[path[:slash]].append(path[slash + 1:])  # line 317
        for pattern in ([] if considerOnly is None else considerOnly):  # line 318
            slash = pattern.rindex(SLASH)  # line 318
            onlyByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 318
        for pattern in ([] if dontConsider is None else dontConsider):  # line 319
            slash = pattern.rindex(SLASH)  # line 319
            dontByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 319
        for folder, paths in byFolder.items():  # line 320
            pos = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in onlyByFolder.get(folder, [])]) if considerOnly is not None else set(paths)  # type: Set[str]  # line 321
            neg = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in dontByFolder.get(folder, [])]) if dontConsider is not None else set()  # type: Set[str]  # line 322
            knownPaths[folder] = list(pos - neg)  # line 323

        for path, dirnames, filenames in os.walk(_.root):  # line 325
            path = decode(path)  # line 326
            dirnames[:] = [decode(d) for d in dirnames]  # line 327
            filenames[:] = [decode(f) for f in filenames]  # line 328
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 329
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 330
            dirnames.sort()  # line 331
            filenames.sort()  # line 331
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 332
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 333
            if dontConsider:  # line 334
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 335
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 336
                filename = relPath + SLASH + file  # line 337
                filepath = os.path.join(path, file)  # line 338
                try:  # line 339
                    stat = os.stat(encode(filepath))  # line 339
                except Exception as E:  # line 340
                    exception(E)  # line 340
                    continue  # line 340
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 341
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 342
                if show:  # indication character returned  # line 343
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 344
                    printo(pure.ljust(outstring), nl="")  # line 345
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 346
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 347
                    nameHash = hashStr(filename)  # line 348
                    try:  # line 349
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=nameHash) for remote in [None] + _.remotes] if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 350
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 351
                        compressed += written  # line 352
                        original += size  # line 352
                    except PermissionError as E:  # line 353
                        error("File permission error for %s" % filepath)  # line 353
                    except Exception as F:  # HINT e.g. FileNotFoundError will not add to additions  # line 354
                        exception(F)  # HINT e.g. FileNotFoundError will not add to additions  # line 354
                    continue  # with next file  # line 355
                last = _.paths[filename]  # filename is known - check for modifications  # line 356
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 357
                    try:  # line 358
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 359
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 360
                        continue  # line 360
                    except Exception as E:  # line 361
                        exception(E)  # line 361
                elif size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False)):  # detected a modification  # line 362
                    try:  # line 363
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else None, 0)  # line 364
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 365
                    except Exception as E:  # line 366
                        exception(E)  # line 366
                else:  # with next file  # line 367
                    continue  # with next file  # line 367
                compressed += written  # line 368
                original += last.size if inverse else size  # line 368
            if relPath in knownPaths:  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 369
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 369
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 370
            for file in names:  # line 371
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 372
                    continue  # don't mark ignored files as deleted  # line 372
                pth = path + SLASH + file  # type: str  # line 373
                changed.deletions[pth] = _.paths[pth]  # line 374
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, _.strict))  # line 375
        if progress:  # forces clean line of progress output  # line 376
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 376
        elif verbose:  # line 377
            info("Finished detecting changes")  # line 377
        tt = time.time() - start_time  # type: float  # line 378
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # in KiBi  # line 379
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 380
        msg = (msg + " | " if msg else "") + ("Transfer speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 381
        return (changed, msg if msg else None)  # line 382

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 384
        ''' Returns nothing, just updates _.paths in place. '''  # line 385
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 386

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 388
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 389
        try:  # load initial paths  # line 390
            _.loadCommit(branch, startwith)  # load initial paths  # line 390
        except:  # no revisions  # line 391
            yield {}  # no revisions  # line 391
            return None  # no revisions  # line 391
        if incrementally:  # line 392
            yield _.paths  # line 392
        m = Metadata(_.root)  # type: Metadata  # next changes TODO #250 avoid loading all metadata and config  # line 393
        rev = None  # type: int  # next changes TODO #250 avoid loading all metadata and config  # line 393
        for rev in range(startwith + 1, revision + 1):  # line 394
            m.loadCommit(branch, rev)  # line 395
            for p, info in m.paths.items():  # line 396
                if info.size == None:  # line 397
                    del _.paths[p]  # line 397
                else:  # line 398
                    _.paths[p] = info  # line 398
            if incrementally:  # line 399
                yield _.paths  # line 399
        yield None  # for the default case - not incrementally  # line 400

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 402
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 403
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 404

    def parseRevisionString(_, argument: 'str') -> 'Union[Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]], NoReturn]':  # line 406
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
        None is returned in case of error
        Code will sys.exit in case of unknown specified branch/revision
    '''  # line 411
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 412
            return (_.branch, -1)  # no branch/revision specified  # line 412
        if argument == "":  # nothing specified by user, raise error in caller  # line 413
            return (None, None)  # nothing specified by user, raise error in caller  # line 413
        argument = argument.strip()  # line 414
        if argument.startswith(SLASH):  # current branch  # line 415
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 415
        if argument.endswith(SLASH):  # line 416
            try:  # line 417
                return (_.getBranchByName(argument[:-1]), -1)  # line 417
            except ValueError:  # line 418
                Exit("Unknown branch label '%s'" % argument)  # line 418
        if SLASH in argument:  # line 419
            b, r = argument.split(SLASH)[:2]  # line 420
            try:  # line 421
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 421
            except ValueError:  # line 422
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 422
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 423
        if branch not in _.branches:  # line 424
            branch = None  # line 424
        try:  # either branch name/number or reverse/absolute revision number  # line 425
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 425
        except:  # line 426
            Exit("Unknown branch label or wrong number format")  # line 426
        Exit("This should never happen. Please create an issue report")  # line 427

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 429
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 431
        while True:  # line 432
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 433
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 434
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 435
                break  # line 435
            revision -= 1  # line 436
            if revision < 0:  # line 437
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 437
        return revision, source  # line 438

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 440
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 441
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 442
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 443
            return [branch]  # found. need to load commit from other branch instead  # line 443
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 444
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 444
        return others  # line 445

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 447
        return _.getParentBranches(branch, revision)[-1]  # line 447

    @_coconut_tco  # line 449
    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 449
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 450
        m = Metadata()  # type: Metadata  # line 451
        other = branch  # type: _coconut.typing.Optional[int]  # line 452
        while other is not None:  # line 453
            m.loadBranch(other)  # line 454
            if m.commits:  # line 455
                return _coconut_tail_call(max, m.commits)  # line 455
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 456
        return None  # line 457

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 459
        ''' Copy versioned file to other branch/revision. '''  # line 460
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 461
        for remote in [None] + _.remotes:  # line 462
            try:  # line 463
                target = revisionFolder(toBranch, toRevision, file=pinfo.nameHash, base=(_.root if remote is None else remote))  # type: str  # line 464
                shutil.copy2(encode(source), encode(target))  # line 465
            except Exception as E:  # line 466
                error("Copying versioned file%s" % ((" to remote path " % remote) if remote else ""))  # line 466

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 468
        ''' Return file contents, or copy contents into file path provided (used in update and restorefile). '''  # line 469
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 470
        try:  # line 471
            with openIt(source, "r", _.compress) as fd:  # line 471
                if toFile is None:  # read bytes into memory and return  # line 472
                    return fd.read()  # read bytes into memory and return  # line 472
                with open(encode(toFile), "wb") as to:  # line 473
                    while True:  # line 474
                        buffer = fd.read(bufSize)  # line 475
                        to.write(buffer)  # line 476
                        if len(buffer) < bufSize:  # line 477
                            break  # line 477
                    return None  # line 478
        except Exception as E:  # line 479
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 479
        None  # line 480

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 482
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 483
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 484
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 484
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 485
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 486
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 487
        if pinfo.size == 0:  # line 488
            with open(encode(target), "wb"):  # line 489
                pass  # line 489
            try:  # update access/modification timestamps on file system  # line 490
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 490
            except Exception as E:  # line 491
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 491
            return None  # line 492
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 493
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 495
            while True:  # line 496
                buffer = fd.read(bufSize)  # line 497
                to.write(buffer)  # line 498
                if len(buffer) < bufSize:  # line 499
                    break  # line 499
        try:  # update access/modification timestamps on file system  # line 500
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 500
        except Exception as E:  # line 501
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 501
        return None  # line 502


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], remotes: 'List[str]'=[]):  # line 506
    ''' Initial command to start working offline. '''  # line 507
    if os.path.exists(encode(metaFolder)):  # line 508
        if '--force' not in options:  # line 509
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 509
        try:  # throw away all previous metadata before going offline  # line 510
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 511
                resource = metaFolder + os.sep + entry  # line 512
                if os.path.isdir(resource):  # line 513
                    shutil.rmtree(encode(resource))  # line 513
                else:  # line 514
                    os.unlink(encode(resource))  # line 514
        except:  # line 515
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder)  # line 515
    for remote in remotes:  # line 516
        try:  # line 517
            os.makedirs(os.path.join(remote, metaFolder))  # line 517
        except Exception as E:  # line 518
            error("Creating remote repository metadata in %s" % remote)  # line 518
    m = Metadata(offline=True, remotes=remotes)  # type: Metadata  # line 519
    if '--strict' in options or m.c.strict:  # always hash contents  # line 520
        m.strict = True  # always hash contents  # line 520
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 521
        m.compress = True  # plain file copies instead of compressed ones  # line 521
    if '--picky' in options or m.c.picky:  # Git-like  # line 522
        m.picky = True  # Git-like  # line 522
    elif '--track' in options or m.c.track:  # Svn-like  # line 523
        m.track = True  # Svn-like  # line 523
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 524
    if title:  # line 525
        printo(title)  # line 525
    if verbose:  # line 526
        info(usage.MARKER + "Going offline...")  # line 526
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 527
    m.branch = 0  # line 528
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 529
    if verbose or '--verbose' in options:  # line 530
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 530
    info(usage.MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 531

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 533
    ''' Finish working offline. '''  # line 534
    if verbose:  # line 535
        info(usage.MARKER + "Going back online...")  # line 535
    force = '--force' in options  # type: bool  # line 536
    m = Metadata()  # type: Metadata  # line 537
    strict = '--strict' in options or m.strict  # type: bool  # line 538
    m.loadBranches()  # line 539
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 540
        Exit("There are still unsynchronized (modified) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 540
    m.loadBranch(m.branch)  # line 541
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 542
    if options.count("--force") < 2:  # line 543
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 544
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 545
        if modified(changed):  # line 546
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 550
    try:  # line 551
        shutil.rmtree(encode(metaFolder))  # line 551
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 551
    except Exception as E:  # line 552
        Exit("Error removing offline repository: %r" % E)  # line 552
    info(usage.MARKER + "Offline repository removed, you're back online")  # line 553

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 555
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not required here, as either branching from last revision anyway, or branching full file tree anyway.
  '''  # line 558
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 559
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 560
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 561
    m = Metadata()  # type: Metadata  # line 562
    m.loadBranch(m.branch)  # line 563
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 564
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 565
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 565
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 566
    if verbose:  # line 567
        info(usage.MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 567
    if last:  # branch from last revision  # line 568
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 568
    else:  # branch from current file tree state  # line 569
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 569
    if not stay:  # line 570
        m.branch = branch  # line 570
    m.saveBranches()  # TODO #253 or indent again?  # line 571
    info(usage.MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 572

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 574
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 575
    m = Metadata()  # type: Metadata  # line 576
    branch = None  # type: _coconut.typing.Optional[int]  # line 576
    revision = None  # type: _coconut.typing.Optional[int]  # line 576
    strict = '--strict' in options or m.strict  # type: bool  # line 577
    branch, revision = m.parseRevisionString(argument)  # line 578
    if branch is None or branch not in m.branches:  # line 579
        Exit("Unknown branch")  # line 579
    m.loadBranch(branch)  # knows commits  # line 580
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 581
    if verbose:  # line 582
        info(usage.MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 582
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 583
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 584
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 589
    return changed  # returning for unit tests only TODO #254 remove?  # line 590

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False):  # TODO #255 introduce option to diff against committed revision and not only file tree  # line 592
    ''' The diff display code. '''  # line 593
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 594
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 595
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 596
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 597
        content = b""  # type: _coconut.typing.Optional[bytes]  # line 598
        if pinfo.size != 0:  # versioned file  # line 599
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 599
            assert content is not None  # versioned file  # line 599
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current file  # line 600
        blocks = None  # type: List[MergeBlock]  # line 601
        nl = None  # type: bytes  # line 601
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 602
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 603
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 604
        for block in blocks:  # line 605
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some of previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # line 608
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 609
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 609
            elif block.tipe == MergeBlockType.REMOVE:  # line 610
                for no, line in enumerate(block.lines):  # line 611
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 611
            elif block.tipe == MergeBlockType.REPLACE:  # line 612
                for no, line in enumerate(block.replaces.lines):  # line 613
                    printo(wrap("-~- %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 613
                for no, line in enumerate(block.lines):  # line 614
                    printo(wrap("+~+ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 614
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 617
                printo()  # line 617

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 619
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 620
    m = Metadata()  # type: Metadata  # line 621
    branch = None  # type: _coconut.typing.Optional[int]  # line 621
    revision = None  # type: _coconut.typing.Optional[int]  # line 621
    strict = '--strict' in options or m.strict  # type: bool  # line 622
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 623
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 624
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 625
    if branch is None or branch not in m.branches:  # line 626
        Exit("Unknown branch")  # line 626
    m.loadBranch(branch)  # knows commits  # line 627
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 628
    if verbose:  # line 629
        info(usage.MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 629
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 630
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 631
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap)  # line 636

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 638
    ''' Create new revision from file tree changes vs. last commit. '''  # line 639
    m = Metadata()  # type: Metadata  # line 640
    if argument is not None and argument in m.tags:  # line 641
        Exit("Illegal commit message. It was already used as a tag name")  # line 641
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 642
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 644
        Exit("No file patterns staged for commit in picky mode")  # line 644
    if verbose:  # line 645
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 645
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 646
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 647
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 648
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 649
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 650
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 651
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 652
    m.saveBranch(m.branch)  # line 653
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 654
    if m.picky:  # remove tracked patterns  # line 655
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 655
    else:  # track or simple mode: set branch modified  # line 656
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 656
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 657
        m.tags.append(argument)  # memorize unique tag  # line 657
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 657
    m.saveBranches()  # line 658
    stored = 0  # type: int  # now determine new commit size on file system  # line 659
    overhead = 0  # type: int  # now determine new commit size on file system  # line 659
    count = 0  # type: int  # now determine new commit size on file system  # line 659
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 660
    for file in os.listdir(commitFolder):  # line 661
        try:  # line 662
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 663
            if file == metaFile:  # line 664
                overhead += newsize  # line 664
            else:  # line 665
                stored += newsize  # line 665
                count += 1  # line 665
        except Exception as E:  # line 666
            error(E)  # line 666
    printo(usage.MARKER_COLOR + "Created new revision r%02d%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%s%s%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, (" '%s'" % argument) if argument is not None else "", Fore.GREEN, Fore.RESET, len(changed.additions) - len(changed.moves), Fore.RED, Fore.RESET, len(changed.deletions) - len(changed.moves), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(changed.modifications), Fore.BLUE + Style.BRIGHT, MOVE_SYMBOL if m.c.useUnicodeFont else "#", Style.RESET_ALL, len(changed.moves), ("%.2f MiB" % ((stored + overhead) / MEBI)) if stored > 1.25 * MEBI else (("%.2f Kib" % ((stored + overhead) / KIBI)) if stored > 1.25 * KIBI else ("%d bytes" % (stored + overhead))), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 667

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 677
    ''' Show branches and current repository state. '''  # line 678
    m = Metadata()  # type: Metadata  # line 679
    if not (m.c.useChangesCommand or '--repo' in options):  # line 680
        changes(argument, options, onlys, excps)  # line 680
        return  # line 680
    current = m.branch  # type: int  # line 681
    strict = '--strict' in options or m.strict  # type: bool  # line 682
    printo(usage.MARKER_COLOR + "Offline repository status")  # line 683
    printo("Repository root:     %s" % os.getcwd())  # line 684
    printo("Underlying VCS root: %s" % vcs)  # line 685
    printo("Underlying VCS type: %s" % cmd)  # line 686
    printo("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 687
    printo("Current SOS version: %s" % version.__version__)  # line 688
    printo("At creation version: %s" % m.version)  # line 689
    printo("Metadata format:     %s" % m.format)  # line 690
    printo("Content checking:    %sactivated%s" % (Fore.CYAN if m.strict else Fore.BLUE + "de", Fore.RESET))  # line 691
    printo("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 692
    printo("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 693
    printo("Number of branches:  %d" % len(m.branches))  # line 694
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 695
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 696
    m.loadBranch(current)  # line 697
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 698
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 699
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 699
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 700
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of unicode symbols for changed vs. unchanged  # line 705
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 709
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 710
        payload = 0  # type: int  # count used storage per branch  # line 711
        overhead = 0  # type: int  # count used storage per branch  # line 711
        original = 0  # type: int  # count used storage per branch  # line 711
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 712
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 713
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 714
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 714
                else:  # line 715
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 715
        pl_amount = float(payload) / MEBI  # type: float  # line 716
        oh_amount = float(overhead) / MEBI  # type: float  # line 716
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 718
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 719
            m.loadCommit(m.branch, commit_)  # line 720
            for pinfo in m.paths.values():  # line 721
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 721
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 722
        printo("  %s b%d%s @%s (%s%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), Fore.RESET, len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 723
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 734
        printo("\nTracked file patterns:")  # TODO #261 print matching untracking patterns side-by-side?  # line 735
        printo(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 736
        printo("\nUntracked file patterns:")  # line 737
        printo(ajoin("  | ", m.branches[m.branch].untracked, "\n"))  # line 738

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 740
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 747
    assert not (check and commit)  # line 748
    m = Metadata()  # type: Metadata  # line 749
    force = '--force' in options  # type: bool  # line 750
    strict = '--strict' in options or m.strict  # type: bool  # line 751
    if argument is not None:  # line 752
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 753
        if branch is None:  # line 754
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 754
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 755
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 756

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 759
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 760
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 761
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 762
    if check and modified(changed) and not force:  # line 767
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 768
        Exit("File tree contains changes. Use --force to proceed")  # line 769
    elif commit:  # line 770
        if not modified(changed) and not force:  # line 771
            Exit("Nothing to commit")  # line 771
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 772
        if msg:  # line 773
            printo(msg)  # line 773

    if argument is not None:  # branch/revision specified  # line 775
        m.loadBranch(branch)  # knows commits of target branch  # line 776
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 777
        revision = m.correctNegativeIndexing(revision)  # line 778
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 779
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 780

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 782
    ''' Continue work on another branch, replacing file tree changes. '''  # line 783
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 784
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 785

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 788
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 789
    else:  # full file switch  # line 790
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 791
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 792

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 799
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 800
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 801
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 802
                rms.append(a)  # line 802
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 803
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 803
        if modified(changed) and not force:  # line 804
            m.listChanges(changed, cwd)  # line 804
            Exit("File tree contains changes. Use --force to proceed")  # line 804
        if verbose:  # line 805
            info(usage.MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 805
        if not modified(todos):  # line 806
            info("No changes to current file tree")  # line 807
        else:  # integration required  # line 808
            for path, pinfo in todos.deletions.items():  # line 809
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 810
                printo("ADD " + path, color=Fore.GREEN)  # line 811
            for path, pinfo in todos.additions.items():  # line 812
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 813
                printo("DEL " + path, color=Fore.RED)  # line 814
            for path, pinfo in todos.modifications.items():  # line 815
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 816
                printo("MOD " + path, color=Fore.YELLOW)  # line 817
    m.branch = branch  # line 818
    m.saveBranches()  # store switched path info  # line 819
    info(usage.MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 820

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 822
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 826
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 827
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 828
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 829
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 830
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 831
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 832
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 833
    if verbose:  # line 834
        info(usage.MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 834

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 837
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 838
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 839
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 840
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 845
        if trackingUnion != trackingPatterns:  # nothing added  # line 846
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 847
        else:  # line 848
            info("Nothing to update")  # but write back updated branch info below  # line 849
    else:  # integration required  # line 850
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 851
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 851
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 851
        if changed.deletions.items():  # line 852
            printo("Additions:")  # line 852
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 853
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 854
            if add_all is None and mrg == MergeOperation.ASK:  # line 855
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 856
                if selection in "ao":  # line 857
                    add_all = "y" if selection == "a" else "n"  # line 857
                    selection = add_all  # line 857
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 858
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 858
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path, color=Fore.GREEN)  # TODO #268 document merge/update output, e.g. (A) as "selected not to add by user choice"  # line 859
        if changed.additions.items():  # line 860
            printo("Deletions:")  # line 860
        for path, pinfo in changed.additions.items():  # line 861
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 862
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 862
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 863
            if del_all is None and mrg == MergeOperation.ASK:  # line 864
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 865
                if selection in "ao":  # line 866
                    del_all = "y" if selection == "a" else "n"  # line 866
                    selection = del_all  # line 866
            if "y" in (del_all, selection):  # line 867
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 867
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path, color=Fore.RED)  # not contained in other branch, but maybe kept  # line 868
        if changed.modifications.items():  # line 869
            printo("Modifications:")  # line 869
        for path, pinfo in changed.modifications.items():  # line 870
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 871
            binary = not m.isTextType(path)  # type: bool  # line 872
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 873
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 874
                printo(("MOD " if not binary else "BIN ") + path, color=Fore.YELLOW)  # TODO print mtime, size differences?  # line 875
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 876
            if op == "t":  # line 877
                printo("THR " + path, color=Fore.MAGENTA)  # blockwise copy of contents  # line 878
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 878
            elif op == "m":  # line 879
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 880
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 880
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 881
                if current == file and verbose:  # line 882
                    info("No difference to versioned file")  # line 882
                elif file is not None:  # if None, error message was already logged  # line 883
                    merged = None  # type: bytes  # line 884
                    nl = None  # type: bytes  # line 884
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 885
                    if merged != current:  # line 886
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 887
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 887
                    elif verbose:  # TODO but update timestamp?  # line 888
                        info("No change")  # TODO but update timestamp?  # line 888
            else:  # mine or wrong input  # line 889
                printo("MNE " + path, color=Fore.CYAN)  # nothing to do! same as skip  # line 890
    info(usage.MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 891
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 892
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 893
    m.saveBranches()  # line 894

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 896
    ''' Remove a branch entirely. '''  # line 897
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 898
    if len(m.branches) == 1:  # line 899
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 899
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 900
    if branch is None or branch not in m.branches:  # line 901
        Exit("Cannot delete unknown branch %r" % branch)  # line 901
    if verbose:  # line 902
        info(usage.MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 902
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 903
    info(usage.MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 904

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 906
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 907
    force = '--force' in options  # type: bool  # line 908
    m = Metadata()  # type: Metadata  # line 909
    if not (m.track or m.picky):  # line 910
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 910
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 911
    if pattern in patterns:  # line 912
        Exit("Pattern '%s' already tracked" % pattern)  # line 912
    if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 913
        Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 913
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 914
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 915
    patterns.append(pattern)  # line 916
    m.saveBranches()  # line 917
    info(usage.MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # line 918

def remove(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 920
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 921
    m = Metadata()  # type: Metadata  # line 922
    if not (m.track or m.picky):  # line 923
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' to start repository in tracking or picky mode")  # line 923
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 924
    if pattern not in patterns:  # line 925
        suggestion = _coconut.set()  # type: Set[str]  # line 926
        for pat in patterns:  # line 927
            if fnmatch.fnmatch(pattern, pat):  # line 927
                suggestion.add(pat)  # line 927
        if suggestion:  # line 928
            printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # line 928
        Exit("Tracked pattern '%s' not found" % pattern)  # line 929
    patterns.remove(pattern)  # line 930
    m.saveBranches()  # line 931
    info(usage.MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 932

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 934
    ''' List specified directory, augmenting with repository metadata. '''  # line 935
    m = Metadata()  # type: Metadata  # line 936
    folder = (os.getcwd() if folder is None else folder)  # line 937
    if '--all' in options:  # always start at SOS repo root with --all  # line 938
        folder = m.root  # always start at SOS repo root with --all  # line 938
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 939
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 940
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 941
    if verbose:  # line 942
        info(usage.MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 942
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 943
    if relPath.startswith(os.pardir):  # line 944
        Exit("Cannot list contents of folder outside offline repository")  # line 944
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 945
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 946
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 947
        if len(m.tags) > 0:  # line 948
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 948
        return  # line 949
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 950
        if not recursive:  # avoid recursion  # line 951
            dirnames.clear()  # avoid recursion  # line 951
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 952
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 953

        folder = decode(dirpath)  # line 955
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 956
        if patterns:  # line 957
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 958
            if out:  # line 959
                printo("DIR %s\n" % relPath + out)  # line 959
            continue  # with next folder  # line 960
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 961
        if len(files) > 0:  # line 962
            printo("DIR %s" % relPath)  # line 962
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 963
            ignore = None  # type: _coconut.typing.Optional[str]  # line 964
            for ig in m.c.ignores:  # remember first match  # line 965
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 965
                    ignore = ig  # remember first match  # line 965
                    break  # remember first match  # line 965
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 966
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 966
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 966
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 966
                        break  # found a white list entry for ignored file, undo ignoring it  # line 966
            matches = []  # type: List[str]  # line 967
            if not ignore:  # line 968
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 969
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 970
                        matches.append(os.path.basename(pattern))  # line 970
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 971
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 972

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 974
    ''' List previous commits on current branch. '''  # line 975
    changes_ = "--changes" in options  # type: bool  # line 976
    diff_ = "--diff" in options  # type: bool  # line 977
    m = Metadata()  # type: Metadata  # line 978
    m.loadBranch(m.branch)  # knows commit history  # line 979
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # line 980
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 981
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 982
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 983
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 984
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 985
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 986
    commit = None  # type: CommitInfo  # line 987
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 988
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 989
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 990
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 991
    for no in range(maxi + 1):  # line 992
        if indicator:  # line 993
            printo("  %%s %%0%dd" % digits % (indicator.getIndicator(), no), nl="\r")  # line 993
        if no in m.commits:  # line 994
            commit = m.commits[no]  # line 994
        else:  # line 995
            if n.branch != n.getParentBranch(m.branch, no):  # line 996
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 996
            commit = n.commits[no]  # line 997
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 998
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 999
        if "--all" in options or no >= lastno:  # line 1000
            if no >= lastno:  # line 1001
                indicator = None  # line 1001
            _add = news - olds  # type: FrozenSet[str]  # line 1002
            _del = olds - news  # type: FrozenSet[str]  # line 1003
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 1005
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 1007
            printo("  %s r%s @%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%sT%s%02d) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, Fore.RESET, len(_add), Fore.RED, Fore.RESET, len(_del), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(_mod), Fore.CYAN, Fore.RESET, _txt, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 1008
            if changes_:  # line 1009
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}), root=cwd if '--relative' in options else None)  # TODO moves detection?  # line 1020
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 1021
                pass  #  _diff(m, changes)  # needs from revision diff  # line 1021
        olds = news  # replaces olds for next revision compare  # line 1022
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 1023

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 1025
    ''' Exported entire repository as archive for easy transfer. '''  # line 1026
    if verbose:  # line 1027
        info(usage.MARKER + "Dumping repository to archive...")  # line 1027
    m = Metadata()  # type: Metadata  # to load the configuration  # line 1028
    progress = '--progress' in options  # type: bool  # line 1029
    delta = '--full' not in options  # type: bool  # line 1030
    skipBackup = '--skip-backup' in options  # type: bool  # line 1031
    import functools  # line 1032
    import locale  # line 1032
    import warnings  # line 1032
    import zipfile  # line 1032
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 1033
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 1033
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 1033
    except:  # line 1034
        compression = zipfile.ZIP_STORED  # line 1034

    if ("" if argument is None else argument) == "":  # line 1036
        Exit("Argument missing (target filename)")  # line 1036
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 1037
    entries = []  # type: List[str]  # line 1038
    if os.path.exists(encode(argument)) and not skipBackup:  # line 1039
        try:  # line 1040
            if verbose:  # line 1041
                info("Creating backup...")  # line 1041
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 1042
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 1043
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 1043
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 1043
        except Exception as E:  # line 1044
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 1044
    if verbose:  # line 1045
        info("Dumping revisions...")  # line 1045
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1046
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1046
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1047
        _zip.debug = 0  # suppress debugging output  # line 1048
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1049
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1050
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1051
        totalsize = 0  # type: int  # line 1052
        start_time = time.time()  # type: float  # line 1053
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1054
            dirpath = decode(dirpath)  # line 1055
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1056
                continue  # don't backup backups  # line 1056
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1057
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1058
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1059
            for filename in filenames:  # line 1060
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1061
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1062
                totalsize += os.stat(encode(abspath)).st_size  # line 1063
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1064
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1065
                    continue  # don't backup backups  # line 1065
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1066
                    if show:  # line 1067
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1067
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1068
        if delta:  # line 1069
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1069
    info("\r" + pure.ljust(usage.MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1070

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1072
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1073
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1074
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1075
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1075
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1076
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1077
    if maxi is None:  # line 1078
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1078
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1079
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1082
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1084
    while files:  # line 1085
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1086
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1087
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1089
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1089
    tracked = None  # type: bool  # line 1090
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1090
    tracked, commitArgs = vcsCommits[cmd]  # line 1090
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1091
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1093
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1093
    if tracked:  # line 1094
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1094

def config(arguments: 'List[_coconut.typing.Optional[str]]', options: 'List[str]'=[]):  # line 1096
    command = None  # type: str  # line 1097
    key = None  # type: str  # line 1097
    value = None  # type: str  # line 1097
    v = None  # type: str  # line 1097
    command, key, value = (arguments + [None] * 2)[:3]  # TODO not already done in parse?  # line 1098
    if command is None:  # line 1099
        usage.usage("help", verbose=True)  # line 1099
    if command not in ["set", "unset", "show", "list", "add", "rm"]:  # line 1100
        Exit("Unknown config command")  # line 1100
    local = "--local" in options  # type: bool  # line 1101
    m = Metadata()  # type: Metadata  # loads layered configuration as well  # line 1102
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1103
    if command == "set":  # line 1104
        if None in (key, value):  # line 1105
            Exit("Key or value not specified")  # line 1105
        if key not in (([] if local else CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1106
            Exit("Unsupported key for %s configuration %r" % ("local " if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1106
        if key in CONFIGURABLE_FLAGS and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1107
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1107
        c[key] = value.lower() in TRUTH_VALUES if key in CONFIGURABLE_FLAGS else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1108
    elif command == "unset":  # line 1109
        if key is None:  # line 1110
            Exit("No key specified")  # line 1110
        if key not in c.keys():  # HINT: Works on local configurations when used with --local  # line 1111
            Exit("Unknown key")  # HINT: Works on local configurations when used with --local  # line 1111
        del c[key]  # line 1112
    elif command == "add":  # line 1113
        if None in (key, value):  # line 1114
            Exit("Key or value not specified")  # line 1114
        if key not in CONFIGURABLE_LISTS:  # line 1115
            Exit("Unsupported key %r" % key)  # line 1115
        if key not in c.keys():  # prepare empty list, or copy from global, add new value below  # line 1116
            c[key] = [_ for _ in c.__defaults[key]] if local else []  # prepare empty list, or copy from global, add new value below  # line 1116
        elif value in c[key]:  # line 1117
            Exit("Value already contained, nothing to do")  # line 1117
        if ";" in value:  # line 1118
            c[key].append(removePath(key, value))  # line 1118
        else:  # line 1119
            c[key].extend([removePath(key, v) for v in value.split(";")])  # line 1119
    elif command == "rm":  # line 1120
        if None in (key, value):  # line 1121
            Exit("Key or value not specified")  # line 1121
        if key not in c.keys():  # line 1122
            Exit("Unknown key %r" % key)  # line 1122
        if value not in c[key]:  # line 1123
            Exit("Unknown value %r" % value)  # line 1123
        c[key].remove(value)  # line 1124
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1125
            del c[key]  # remove local entry, to fallback to global  # line 1125
    else:  # Show or list  # line 1126
        if key == "ints":  # list valid configuration items  # line 1127
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1127
        elif key == "flags":  # line 1128
            printo(", ".join(CONFIGURABLE_FLAGS))  # line 1128
        elif key == "lists":  # line 1129
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1129
        elif key == "texts":  # line 1130
            printo(", ".join([_ for _ in defaults.keys() if _ not in (CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS)]))  # line 1130
        else:  # line 1131
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1132
            c = m.c  # always use full configuration chain  # line 1133
            try:  # attempt single key  # line 1134
                assert key is not None  # force exception  # line 1135
                c[key]  # force exception  # line 1135
                l = key in c.keys()  # type: bool  # line 1136
                g = key in c.__defaults.keys()  # type: bool  # line 1136
                printo("%s %s %r" % (key.rjust(20), out[3] if not (l or g) else (out[1] if l else out[2]), c[key]))  # line 1137
            except:  # normal value listing  # line 1138
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # line 1139
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1140
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1141
                for k, vt in sorted(vals.items()):  # line 1142
                    printo("%s %s %s" % (k.rjust(20), out[vt[1]], vt[0]))  # line 1142
                if len(c.keys()) == 0:  # line 1143
                    info("No local configuration stored")  # line 1143
                if len(c.__defaults.keys()) == 0:  # line 1144
                    info("No global configuration stored")  # line 1144
        return  # in case of list, no need to store anything  # line 1145
    if local:  # saves changes of repoConfig  # line 1146
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1146
        m.saveBranches()  # saves changes of repoConfig  # line 1146
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1146
    else:  # global config  # line 1147
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1148
        if f is None:  # line 1149
            Exit("Error saving user configuration: %r" % h)  # line 1149

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1151
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1154
    if verbose:  # line 1155
        info(usage.MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1155
    force = '--force' in options  # type: bool  # line 1156
    soft = '--soft' in options  # type: bool  # line 1157
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1158
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1158
    m = Metadata()  # type: Metadata  # line 1159
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1160
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1161
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1162
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1163
    if not matching and not force:  # line 1164
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1164
    if not (m.track or m.picky):  # line 1165
        Exit("Repository is in simple mode. Use basic file operations to modify files, then execute 'sos commit' to version any changes")  # line 1165
    if pattern not in patterns:  # list potential alternatives and exit  # line 1166
        for tracked in (t for t in patterns if t[:t.rindex(SLASH)] == relPath):  # for all patterns of the same source folder HINT was os.path.dirpath before  # line 1167
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1168
            if alternative:  # line 1169
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1169
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: "if not (force or soft):""  # line 1170
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1171
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1172
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1173
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1177
#  oldTokens:GlobBlock[]?; newToken:GlobBlock[]?  # TODO remove optional?, only here to satisfy mypy
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1179
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1180
    if len({st[1] for st in matches}) != len(matches):  # line 1181
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1181
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1182
    if os.path.exists(encode(newRelPath)):  # line 1183
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1184
        if exists and not (force or soft):  # line 1185
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1185
    else:  # line 1186
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1186
    if not soft:  # perform actual renaming  # line 1187
        for (source, target) in matches:  # line 1188
            try:  # line 1189
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1189
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1190
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1190
    patterns[patterns.index(pattern)] = newPattern  # line 1191
    m.saveBranches()  # line 1192

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1194
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1195
    debug("Parsing command-line arguments...")  # line 1196
    root = os.getcwd()  # line 1197
    try:  # line 1198
        onlys, excps, remotes = parseArgumentOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1199
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1200
        arguments = [c.strip() for c in sys.argv[2:] if not (c.startswith("-") and (len(c) == 2 or c[1] == "-"))]  # type: List[_coconut.typing.Optional[str]]  # line 1201
        options = [c.strip() for c in sys.argv[2:] if c.startswith("-") and (len(c) == 2 or c[1] == "-")]  # options with arguments have to be parsed from sys.argv  # line 1202
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1203
        if command[:1] in "amr":  # line 1204
            relPath, pattern = relativize(root, os.path.join(cwd, arguments[0] if arguments else "."))  # line 1204
        if command[:1] == "m":  # line 1205
            if len(arguments) < 2:  # line 1206
                Exit("Need a second file pattern argument as target for move command")  # line 1206
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1207
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1208
        if command[:1] == "a":  # e.g. addnot  # line 1209
            add(relPath, pattern, options, negative="n" in command)  # e.g. addnot  # line 1209
        elif command[:1] == "b":  # line 1210
            branch(arguments[0], arguments[1], options)  # line 1210
        elif command[:3] == "com":  # line 1211
            commit(arguments[0], options, onlys, excps)  # line 1211
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1212
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1212
        elif command[:2] == "ci":  # line 1213
            commit(arguments[0], options, onlys, excps)  # line 1213
        elif command[:3] == 'con':  # line 1214
            config(arguments, options)  # line 1214
        elif command[:2] == "de":  # line 1215
            destroy((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1215
        elif command[:2] == "di":  # line 1216
            diff((lambda _coconut_none_coalesce_item: "/" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps)  # line 1216
        elif command[:2] == "du":  # line 1217
            dump((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1217
        elif command[:1] == "h":  # line 1218
            usage.usage(arguments[0], verbose=verbose)  # line 1218
        elif command[:2] == "lo":  # line 1219
            log(options, cwd)  # line 1219
        elif command[:2] == "li":  # line 1220
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1220
        elif command[:2] == "ls":  # line 1221
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1221
        elif command[:1] == "m":  # e.g. mvnot  # line 1222
            move(relPath, pattern, newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1222
        elif command[:2] == "of":  # line 1223
            offline(arguments[0], arguments[1], options, remotes)  # line 1223
        elif command[:2] == "on":  # line 1224
            online(options)  # line 1224
        elif command[:1] == "p":  # line 1225
            publish(arguments[0], cmd, options, onlys, excps)  # line 1225
        elif command[:1] == "r":  # e.g. rmnot  # line 1226
            remove(relPath, pattern, options, negative="n" in command)  # e.g. rmnot  # line 1226
        elif command[:2] == "st":  # line 1227
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1227
        elif command[:2] == "sw":  # line 1228
            switch((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps, cwd)  # line 1228
        elif command[:1] == "u":  # line 1229
            update((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps)  # line 1229
        elif command[:1] == "v":  # line 1230
            usage.usage(arguments[0], version=True)  # line 1230
        else:  # line 1231
            Exit("Unknown command '%s'" % command)  # line 1231
        Exit(code=0)  # regular exit  # line 1232
    except (Exception, RuntimeError) as E:  # line 1233
        exception(E)  # line 1234
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing")  # line 1235

def main():  # line 1237
    global debug, info, warn, error  # to modify logger  # line 1238
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1239
    _log = Logger(logging.getLogger(__name__))  # line 1240
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1240
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1241
        sys.argv.remove(option)  # clean up program arguments  # line 1241
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1242
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1242
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1243
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1244
    debug("Detected SOS root folder: %s\nDetected VCS root folder: %s" % (("-" if root is None else root), ("-" if vcs is None else vcs)))  # line 1245
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1246
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1247
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv"):  # in offline mode or just going offline  # line 1248
        cwd = os.getcwd()  # line 1249
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1250
        parse(vcs, cwd, cmd)  # line 1251
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1252
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1253
        import subprocess  # only required in this section  # line 1254
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1255
        inp = ""  # type: str  # line 1256
        while True:  # line 1257
            so, se = process.communicate(input=inp)  # line 1258
            if process.returncode is not None:  # line 1259
                break  # line 1259
            inp = sys.stdin.read()  # line 1260
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1261
            if root is None:  # line 1262
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1262
            m = Metadata(root)  # type: Metadata  # line 1263
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1264
            m.saveBranches()  # line 1265
    else:  # line 1266
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1266


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: List[None]  # this is a trick allowing to modify the flags from the test suite  # line 1270
force_vcs = [None] if '--vcs' in sys.argv else []  # type: List[None]  # line 1271
verbose = [None] if '--verbose' in sys.argv or '-v' in sys.argv else []  # type: List[None]  # imported from utility, and only modified here  # line 1272
debug_ = [None] if os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv else []  # type: List[None]  # line 1273
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1274

_log = Logger(logging.getLogger(__name__))  # line 1276
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1276

if __name__ == '__main__':  # line 1278
    main()  # line 1278
