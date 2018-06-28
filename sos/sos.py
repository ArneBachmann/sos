#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x4bb2e600

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
                error("Saving branches%s" % ((" to remote path " + remote) if remote else ""))  # line 142

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
                error("Saving branch%s" % ((" to remote path " + remote) if remote else ""))  # line 173

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
            tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)) if full else branchFolder(branch, base=(_.root if remote is None else remote)))), lambda: error("Duplicating remote branch folder %r" % remote))  # line 195
        if full:  # not fast branching via reference - copy all current files to new branch  # line 196
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 197
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 198
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 198
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit TODO #244 also contain message from latest revision of originating branch  # line 199
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
                tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)))), lambda: error("Creating remote branch folder %r" % remote))  # line 224
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
                error("Saving commit%s" % ((" to remote path " + remote) if remote else ""))  # line 289

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

    def parseRevisionString(_, argument: 'str') -> 'Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]]':  # line 406
        ''' Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit.
    '''  # line 409
        if argument is None or argument == SLASH:  # no branch/revision specified  # line 410
            return (_.branch, -1)  # no branch/revision specified  # line 410
        argument = argument.strip()  # line 411
        if argument.startswith(SLASH):  # current branch  # line 412
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 412
        if argument.endswith(SLASH):  # line 413
            try:  # line 414
                return (_.getBranchByName(argument[:-1]), -1)  # line 414
            except ValueError:  # line 415
                Exit("Unknown branch label '%s'" % argument)  # line 415
        if SLASH in argument:  # line 416
            b, r = argument.split(SLASH)[:2]  # line 417
            try:  # line 418
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 418
            except ValueError:  # line 419
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r))  # line 419
        branch = _.getBranchByName(argument)  # type: int  # returns number if given (revision) integer  # line 420
        if branch not in _.branches:  # line 421
            branch = None  # line 421
        try:  # either branch name/number or reverse/absolute revision number  # line 422
            return ((_.branch if branch is None else branch), int(argument if argument else "-1") if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 422
        except:  # line 423
            Exit("Unknown branch label or wrong number format")  # line 423
        Exit("This should never happen. Please create a issue report")  # line 424
        return (None, None)  # line 424

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 426
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 428
        while True:  # line 429
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 430
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 431
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 432
                break  # line 432
            revision -= 1  # line 433
            if revision < 0:  # line 434
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 434
        return revision, source  # line 435

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 437
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 438
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 439
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 440
            return [branch]  # found. need to load commit from other branch instead  # line 440
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 441
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 441
        return others  # line 442

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 444
        return _.getParentBranches(branch, revision)[-1]  # line 444

    @_coconut_tco  # line 446
    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 446
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 447
        m = Metadata()  # type: Metadata  # line 448
        other = branch  # type: _coconut.typing.Optional[int]  # line 449
        while other is not None:  # line 450
            m.loadBranch(other)  # line 451
            if m.commits:  # line 452
                return _coconut_tail_call(max, m.commits)  # line 452
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 453
        return None  # line 454

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 456
        ''' Copy versioned file to other branch/revision. '''  # line 457
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 458
        for remote in [None] + _.remotes:  # line 459
            try:  # line 460
                target = revisionFolder(toBranch, toRevision, file=pinfo.nameHash, base=(_.root if remote is None else remote))  # type: str  # line 461
                shutil.copy2(encode(source), encode(target))  # line 462
            except Exception as E:  # line 463
                error("Copying versioned file%s" % ((" to remote path " % remote) if remote else ""))  # line 463

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 465
        ''' Return file contents, or copy contents into file path provided (used in update and restorefile). '''  # line 466
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 467
        try:  # line 468
            with openIt(source, "r", _.compress) as fd:  # line 468
                if toFile is None:  # read bytes into memory and return  # line 469
                    return fd.read()  # read bytes into memory and return  # line 469
                with open(encode(toFile), "wb") as to:  # line 470
                    while True:  # line 471
                        buffer = fd.read(bufSize)  # line 472
                        to.write(buffer)  # line 473
                        if len(buffer) < bufSize:  # line 474
                            break  # line 474
                    return None  # line 475
        except Exception as E:  # line 476
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 476
        None  # line 477

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 479
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 480
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 481
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 481
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 482
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 483
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 484
        if pinfo.size == 0:  # line 485
            with open(encode(target), "wb"):  # line 486
                pass  # line 486
            try:  # update access/modification timestamps on file system  # line 487
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 487
            except Exception as E:  # line 488
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 488
            return None  # line 489
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 490
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 492
            while True:  # line 493
                buffer = fd.read(bufSize)  # line 494
                to.write(buffer)  # line 495
                if len(buffer) < bufSize:  # line 496
                    break  # line 496
        try:  # update access/modification timestamps on file system  # line 497
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 497
        except Exception as E:  # line 498
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 498
        return None  # line 499


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], remotes: 'List[str]'=[]):  # line 503
    ''' Initial command to start working offline. '''  # line 504
    if os.path.exists(encode(metaFolder)):  # line 505
        if '--force' not in options:  # line 506
            Exit("Repository folder is either already offline or older branches and commits were left over.\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 506
        try:  # throw away all previous metadata before going offline  # line 507
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 508
                resource = metaFolder + os.sep + entry  # line 509
                if os.path.isdir(resource):  # line 510
                    shutil.rmtree(encode(resource))  # line 510
                else:  # line 511
                    os.unlink(encode(resource))  # line 511
        except:  # line 512
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder)  # line 512
    for remote in remotes:  # line 513
        try:  # line 514
            os.makedirs(os.path.join(remote, metaFolder))  # line 514
        except Exception as E:  # line 515
            error("Creating remote repository metadata in %s" % remote)  # line 515
    m = Metadata(offline=True, remotes=remotes)  # type: Metadata  # line 516
    if '--strict' in options or m.c.strict:  # always hash contents  # line 517
        m.strict = True  # always hash contents  # line 517
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 518
        m.compress = True  # plain file copies instead of compressed ones  # line 518
    if '--picky' in options or m.c.picky:  # Git-like  # line 519
        m.picky = True  # Git-like  # line 519
    elif '--track' in options or m.c.track:  # Svn-like  # line 520
        m.track = True  # Svn-like  # line 520
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 521
    if title:  # line 522
        printo(title)  # line 522
    if verbose:  # line 523
        info(usage.MARKER + "Going offline...")  # line 523
    m.createBranch(0, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 524
    m.branch = 0  # line 525
    m.saveBranches(also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 526
    if verbose or '--verbose' in options:  # line 527
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 527
    info(usage.MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 528

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 530
    ''' Finish working offline. '''  # line 531
    if verbose:  # line 532
        info(usage.MARKER + "Going back online...")  # line 532
    force = '--force' in options  # type: bool  # line 533
    m = Metadata()  # type: Metadata  # line 534
    strict = '--strict' in options or m.strict  # type: bool  # line 535
    m.loadBranches()  # line 536
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 537
        Exit("There are still unsynchronized (modified) branches.\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions")  # line 537
    m.loadBranch(m.branch)  # line 538
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 539
    if options.count("--force") < 2:  # line 540
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 541
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 542
        if modified(changed):  # line 543
            Exit("File tree is modified vs. current branch.\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 547
    try:  # line 548
        shutil.rmtree(encode(metaFolder))  # line 548
        info("Exited offline mode. Continue working with your traditional VCS.")  # line 548
    except Exception as E:  # line 549
        Exit("Error removing offline repository: %r" % E)  # line 549
    info(usage.MARKER + "Offline repository removed, you're back online")  # line 550

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 552
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not necessary, as either branching from last  revision anyway, or branching file tree anyway.
  '''  # line 555
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 556
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 557
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 558
    m = Metadata()  # type: Metadata  # line 559
    m.loadBranch(m.branch)  # line 560
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 561
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 562
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 562
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 563
    if verbose:  # line 564
        info(usage.MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 564
    if last:  # branch from last revision  # line 565
        m.duplicateBranch(branch, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 565
    else:  # branch from current file tree state  # line 566
        m.createBranch(branch, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 566
    if not stay:  # line 567
        m.branch = branch  # line 567
    m.saveBranches()  # TODO #253 or indent again?  # line 568
    info(usage.MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 569

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 571
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 572
    m = Metadata()  # type: Metadata  # line 573
    branch = None  # type: _coconut.typing.Optional[int]  # line 573
    revision = None  # type: _coconut.typing.Optional[int]  # line 573
    strict = '--strict' in options or m.strict  # type: bool  # line 574
    branch, revision = m.parseRevisionString(argument)  # line 575
    if branch not in m.branches:  # line 576
        Exit("Unknown branch")  # line 576
    m.loadBranch(branch)  # knows commits  # line 577
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 578
    if verbose:  # line 579
        info(usage.MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 579
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 580
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 581
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 586
    return changed  # returning for unit tests only TODO #254 remove?  # line 587

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False):  # TODO #255 introduce option to diff against committed revision  # line 589
    ''' The diff display code. '''  # line 590
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 591
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 592
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 593
    for path, pinfo in (c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0]))):  # only consider modified text files  # line 594
        content = b""  # type: _coconut.typing.Optional[bytes]  # line 595
        if pinfo.size != 0:  # versioned file  # line 596
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 596
            assert content is not None  # versioned file  # line 596
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current file  # line 597
        blocks = None  # type: List[MergeBlock]  # line 598
        nl = None  # type: bytes  # line 598
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 599
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 600
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 601
        for block in blocks:  # line 602
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # TODO #256 show color via (n)curses or other library?  # line 605
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 606
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 606
            elif block.tipe == MergeBlockType.REMOVE:  # line 607
                for no, line in enumerate(block.lines):  # line 608
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 608
            elif block.tipe == MergeBlockType.REPLACE:  # line 609
                for no, line in enumerate(block.replaces.lines):  # line 610
                    printo(wrap("-~- %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 610
                for no, line in enumerate(block.lines):  # line 611
                    printo(wrap("+~+ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 611
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 614
                printo()  # line 614

def diff(argument: 'str'="", options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 616
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 617
    m = Metadata()  # type: Metadata  # line 618
    branch = None  # type: _coconut.typing.Optional[int]  # line 618
    revision = None  # type: _coconut.typing.Optional[int]  # line 618
    strict = '--strict' in options or m.strict  # type: bool  # line 619
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 620
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 621
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 622
    if branch not in m.branches:  # line 623
        Exit("Unknown branch")  # line 623
    m.loadBranch(branch)  # knows commits  # line 624
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 625
    if verbose:  # line 626
        info(usage.MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 626
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 627
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 628
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap)  # line 633

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 635
    ''' Create new revision from file tree changes vs. last commit. '''  # line 636
    m = Metadata()  # type: Metadata  # line 637
    if argument is not None and argument in m.tags:  # line 638
        Exit("Illegal commit message. It was already used as a tag name")  # line 638
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 639
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 641
        Exit("No file patterns staged for commit in picky mode")  # line 641
    if verbose:  # line 642
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 642
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 643
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 644
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 645
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 646
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 647
    m.saveCommit(m.branch, revision)  # revision has already been incremented  # line 648
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 649
    m.saveBranch(m.branch)  # line 650
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 651
    if m.picky:  # remove tracked patterns  # line 652
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 652
    else:  # track or simple mode: set branch modified  # line 653
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 653
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 654
        m.tags.append(argument)  # memorize unique tag  # line 654
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 654
    m.saveBranches()  # line 655
    stored = 0  # type: int  # now determine new commit size on file system  # line 656
    overhead = 0  # type: int  # now determine new commit size on file system  # line 656
    count = 0  # type: int  # now determine new commit size on file system  # line 656
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 657
    for file in os.listdir(commitFolder):  # line 658
        try:  # line 659
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 660
            if file == metaFile:  # line 661
                overhead += newsize  # line 661
            else:  # line 662
                stored += newsize  # line 662
                count += 1  # line 662
        except Exception as E:  # line 663
            error(E)  # line 663
    printo(usage.MARKER_COLOR + "Created new revision r%02d%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%s%s%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, (" '%s'" % argument) if argument is not None else "", Fore.GREEN, Fore.RESET, len(changed.additions) - len(changed.moves), Fore.RED, Fore.RESET, len(changed.deletions) - len(changed.moves), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(changed.modifications), Fore.BLUE + Style.BRIGHT, MOVE_SYMBOL if m.c.useUnicodeFont else "#", Style.RESET_ALL, len(changed.moves), ("%.2f MiB" % ((stored + overhead) / MEBI)) if stored > 1.25 * MEBI else (("%.2f Kib" % ((stored + overhead) / KIBI)) if stored > 1.25 * KIBI else ("%d bytes" % (stored + overhead))), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 664

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 674
    ''' Show branches and current repository state. '''  # line 675
    m = Metadata()  # type: Metadata  # line 676
    if not (m.c.useChangesCommand or '--repo' in options):  # line 677
        changes(argument, options, onlys, excps)  # line 677
        return  # line 677
    current = m.branch  # type: int  # line 678
    strict = '--strict' in options or m.strict  # type: bool  # line 679
    printo(usage.MARKER_COLOR + "Offline repository status")  # line 680
    printo("Repository root:     %s" % os.getcwd())  # line 681
    printo("Underlying VCS root: %s" % vcs)  # line 682
    printo("Underlying VCS type: %s" % cmd)  # line 683
    printo("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 684
    printo("Current SOS version: %s" % version.__version__)  # line 685
    printo("At creation version: %s" % m.version)  # line 686
    printo("Metadata format:     %s" % m.format)  # line 687
    printo("Content checking:    %sactivated%s" % (Fore.CYAN if m.strict else Fore.BLUE + "de", Fore.RESET))  # line 688
    printo("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 689
    printo("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 690
    printo("Number of branches:  %d" % len(m.branches))  # line 691
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 692
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 693
    m.loadBranch(current)  # line 694
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 695
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 696
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 696
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 697
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of symbols for changed vs. unchanged  # line 702
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 706
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 707
        payload = 0  # type: int  # count used storage per branch  # line 708
        overhead = 0  # type: int  # count used storage per branch  # line 708
        original = 0  # type: int  # count used storage per branch  # line 708
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 709
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 710
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 711
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 711
                else:  # line 712
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 712
        pl_amount = float(payload) / MEBI  # type: float  # line 713
        oh_amount = float(overhead) / MEBI  # type: float  # line 713
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 715
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 716
            m.loadCommit(m.branch, commit_)  # line 717
            for pinfo in m.paths.values():  # line 718
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 718
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 719
        printo("  %s b%d%s @%s (%s%s) with %d commits, using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), Fore.RESET, len(m.commits), pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 720
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 731
        printo("\nTracked file patterns:")  # TODO #261 print matching untracking patterns side-by-side?  # line 732
        printo(ajoin("  | ", m.branches[m.branch].tracked, "\n"))  # line 733
        printo("\nUntracked file patterns:")  # line 734
        printo(ajoin("  | ", m.branches[m.branch].untracked, "\n"))  # line 735

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 737
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 744
    assert not (check and commit)  # line 745
    m = Metadata()  # type: Metadata  # line 746
    force = '--force' in options  # type: bool  # line 747
    strict = '--strict' in options or m.strict  # type: bool  # line 748
    if argument is not None:  # line 749
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 750
        if branch is None:  # line 751
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 751
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 752
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 753

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 756
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 757
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 758
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options)  # line 759
    if check and modified(changed) and not force:  # line 764
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 765
        Exit("File tree contains changes. Use --force to proceed")  # line 766
    elif commit:  # line 767
        if not modified(changed) and not force:  # line 768
            Exit("Nothing to commit")  # line 768
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 769
        if msg:  # line 770
            printo(msg)  # line 770

    if argument is not None:  # branch/revision specified  # line 772
        m.loadBranch(branch)  # knows commits of target branch  # line 773
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 774
        revision = m.correctNegativeIndexing(revision)  # line 775
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 776
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 777

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 779
    ''' Continue work on another branch, replacing file tree changes. '''  # line 780
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # force continuation to delay check to this function  # line 781
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 782

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data  # line 785
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 786
    else:  # full file switch  # line 787
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 788
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 789

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 796
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 797
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 798
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 799
                rms.append(a)  # line 799
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 800
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 800
        if modified(changed) and not force:  # line 801
            m.listChanges(changed, cwd)  # line 801
            Exit("File tree contains changes. Use --force to proceed")  # line 801
        if verbose:  # line 802
            info(usage.MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 802
        if not modified(todos):  # line 803
            info("No changes to current file tree")  # line 804
        else:  # integration required  # line 805
            for path, pinfo in todos.deletions.items():  # line 806
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 807
                printo("ADD " + path, color=Fore.GREEN)  # line 808
            for path, pinfo in todos.additions.items():  # line 809
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 810
                printo("DEL " + path, color=Fore.RED)  # line 811
            for path, pinfo in todos.modifications.items():  # line 812
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 813
                printo("MOD " + path, color=Fore.YELLOW)  # line 814
    m.branch = branch  # line 815
    m.saveBranches()  # store switched path info  # line 816
    info(usage.MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 817

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 819
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 823
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 824
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 825
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 826
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 827
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 828
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 829
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 830
    if verbose:  # line 831
        info(usage.MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 831

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 834
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 835
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 836
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 837
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 842
        if trackingUnion != trackingPatterns:  # nothing added  # line 843
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 844
        else:  # line 845
            info("Nothing to update")  # but write back updated branch info below  # line 846
    else:  # integration required  # line 847
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 848
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 848
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 848
        if changed.deletions.items():  # line 849
            printo("Additions:")  # line 849
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 850
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 851
            if add_all is None and mrg == MergeOperation.ASK:  # line 852
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 853
                if selection in "ao":  # line 854
                    add_all = "y" if selection == "a" else "n"  # line 854
                    selection = add_all  # line 854
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 855
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 855
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path, color=Fore.GREEN)  # TODO document (A) as "selected not to add by user choice"  # line 856
        if changed.additions.items():  # line 857
            printo("Deletions:")  # line 857
        for path, pinfo in changed.additions.items():  # line 858
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 859
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 859
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 860
            if del_all is None and mrg == MergeOperation.ASK:  # line 861
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 862
                if selection in "ao":  # line 863
                    del_all = "y" if selection == "a" else "n"  # line 863
                    selection = del_all  # line 863
            if "y" in (del_all, selection):  # line 864
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 864
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path, color=Fore.RED)  # not contained in other branch, but maybe kept  # line 865
        if changed.modifications.items():  # line 866
            printo("Modifications:")  # line 866
        for path, pinfo in changed.modifications.items():  # line 867
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 868
            binary = not m.isTextType(path)  # type: bool  # line 869
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 870
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 871
                printo(("MOD " if not binary else "BIN ") + path, color=Fore.YELLOW)  # TODO print mtime, size differences?  # line 872
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 873
            if op == "t":  # line 874
                printo("THR " + path, color=Fore.MAGENTA)  # blockwise copy of contents  # line 875
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 875
            elif op == "m":  # line 876
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 877
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 877
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # parse lines  # line 878
                if current == file and verbose:  # line 879
                    info("No difference to versioned file")  # line 879
                elif file is not None:  # if None, error message was already logged  # line 880
                    merged = None  # type: bytes  # line 881
                    nl = None  # type: bytes  # line 881
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 882
                    if merged != current:  # line 883
                        with open(encode(path), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 884
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 884
                    elif verbose:  # TODO but update timestamp?  # line 885
                        info("No change")  # TODO but update timestamp?  # line 885
            else:  # mine or wrong input  # line 886
                printo("MNE " + path, color=Fore.CYAN)  # nothing to do! same as skip  # line 887
    info(usage.MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 888
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 889
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 890
    m.saveBranches()  # line 891

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 893
    ''' Remove a branch entirely. '''  # line 894
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 895
    if len(m.branches) == 1:  # line 896
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 896
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 897
    if branch is None or branch not in m.branches:  # line 898
        Exit("Cannot delete unknown branch %r" % branch)  # line 898
    if verbose:  # line 899
        info(usage.MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 899
    binfo = m.removeBranch(branch)  # need to keep a reference to removed entry for output below  # line 900
    info(usage.MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 901

def add(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 903
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 904
    force = '--force' in options  # type: bool  # line 905
    m = Metadata()  # type: Metadata  # line 906
    if not (m.track or m.picky):  # line 907
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 907
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 908
    if pattern in patterns:  # line 909
        Exit("Pattern '%s' already tracked" % pattern)  # line 909
    if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 910
        Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 910
    if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 911
        Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 912
    patterns.append(pattern)  # line 913
    m.saveBranches()  # line 914
    info(usage.MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # TODO #262 display relative path by default?  # line 915

def remove(relPath: 'str', pattern: 'str', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 917
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 918
    m = Metadata()  # type: Metadata  # line 919
    if not (m.track or m.picky):  # line 920
        Exit("Repository is in simple mode. Needs 'offline --track' or 'offline --picky' instead")  # line 920
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 921
    if pattern not in patterns:  # line 922
        suggestion = _coconut.set()  # type: Set[str]  # line 923
        for pat in patterns:  # line 924
            if fnmatch.fnmatch(pattern, pat):  # line 924
                suggestion.add(pat)  # line 924
        if suggestion:  # TODO use same wording as in move  # line 925
            printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # TODO use same wording as in move  # line 925
        Exit("Tracked pattern '%s' not found" % pattern)  # line 926
    patterns.remove(pattern)  # line 927
    m.saveBranches()  # line 928
    info(usage.MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 929

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 931
    ''' List specified directory, augmenting with repository metadata. '''  # line 932
    m = Metadata()  # type: Metadata  # line 933
    folder = (os.getcwd() if folder is None else folder)  # line 934
    if '--all' in options:  # always start at SOS repo root with --all  # line 935
        folder = m.root  # always start at SOS repo root with --all  # line 935
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 936
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 937
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 938
    if verbose:  # line 939
        info(usage.MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 939
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 940
    if relPath.startswith(os.pardir):  # line 941
        Exit("Cannot list contents of folder outside offline repository")  # line 941
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 942
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 943
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 944
        if len(m.tags) > 0:  # line 945
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 945
        return  # line 946
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 947
        if not recursive:  # avoid recursion  # line 948
            dirnames.clear()  # avoid recursion  # line 948
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 949
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 950

        folder = decode(dirpath)  # line 952
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 953
        if patterns:  # line 954
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 955
            if out:  # line 956
                printo("DIR %s\n" % relPath + out)  # line 956
            continue  # with next folder  # line 957
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 958
        if len(files) > 0:  # line 959
            printo("DIR %s" % relPath)  # line 959
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 960
            ignore = None  # type: _coconut.typing.Optional[str]  # line 961
            for ig in m.c.ignores:  # remember first match  # line 962
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 962
                    ignore = ig  # remember first match  # line 962
                    break  # remember first match  # line 962
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 963
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 963
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 963
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 963
                        break  # found a white list entry for ignored file, undo ignoring it  # line 963
            matches = []  # type: List[str]  # line 964
            if not ignore:  # line 965
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 966
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 967
                        matches.append(os.path.basename(pattern))  # line 967
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 968
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 969

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 971
    ''' List previous commits on current branch. '''  # line 972
    changes_ = "--changes" in options  # type: bool  # line 973
    diff_ = "--diff" in options  # type: bool  # line 974
    m = Metadata()  # type: Metadata  # line 975
    m.loadBranch(m.branch)  # knows commit history  # line 976
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # line 977
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 978
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(usage.MARKER + "Offline commit history of branch '%s'" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 979
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 980
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 981
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 982
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 983
    commit = None  # type: CommitInfo  # line 984
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 985
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 986
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 987
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 988
    for no in range(maxi + 1):  # line 989
        if indicator:  # line 990
            printo("  %%s %%0%dd" % digits % (indicator.getIndicator(), no), nl="\r")  # line 990
        if no in m.commits:  # line 991
            commit = m.commits[no]  # line 991
        else:  # line 992
            if n.branch != n.getParentBranch(m.branch, no):  # line 993
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 993
            commit = n.commits[no]  # line 994
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 995
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 996
        if "--all" in options or no >= lastno:  # line 997
            if no >= lastno:  # line 998
                indicator = None  # line 998
            _add = news - olds  # type: FrozenSet[str]  # line 999
            _del = olds - news  # type: FrozenSet[str]  # line 1000
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 1002
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 1004
            printo("  %s r%s @%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%sT%s%02d) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, Fore.RESET, len(_add), Fore.RED, Fore.RESET, len(_del), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(_mod), Fore.CYAN, Fore.RESET, _txt, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 1005
            if changes_:  # line 1006
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}), root=cwd if '--relative' in options else None)  # TODO moves detection?  # line 1017
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 1018
                pass  #  _diff(m, changes)  # needs from revision diff  # line 1018
        olds = news  # replaces olds for next revision compare  # line 1019
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 1020

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 1022
    ''' Exported entire repository as archive for easy transfer. '''  # line 1023
    if verbose:  # line 1024
        info(usage.MARKER + "Dumping repository to archive...")  # line 1024
    m = Metadata()  # type: Metadata  # to load the configuration  # line 1025
    progress = '--progress' in options  # type: bool  # line 1026
    delta = '--full' not in options  # type: bool  # line 1027
    skipBackup = '--skip-backup' in options  # type: bool  # line 1028
    import functools  # line 1029
    import locale  # line 1029
    import warnings  # line 1029
    import zipfile  # line 1029
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 1030
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 1030
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 1030
    except:  # line 1031
        compression = zipfile.ZIP_STORED  # line 1031

    if argument is None:  # line 1033
        Exit("Argument missing (target filename)")  # line 1033
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 1034
    entries = []  # type: List[str]  # line 1035
    if os.path.exists(encode(argument)) and not skipBackup:  # line 1036
        try:  # line 1037
            if verbose:  # line 1038
                info("Creating backup...")  # line 1038
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 1039
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 1040
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 1040
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 1040
        except Exception as E:  # line 1041
            Exit("Error creating backup copy before dumping. Please resolve and retry. %r" % E)  # line 1041
    if verbose:  # line 1042
        info("Dumping revisions...")  # line 1042
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1043
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1043
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1044
        _zip.debug = 0  # suppress debugging output  # line 1045
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1046
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1047
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1048
        totalsize = 0  # type: int  # line 1049
        start_time = time.time()  # type: float  # line 1050
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1051
            dirpath = decode(dirpath)  # line 1052
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1053
                continue  # don't backup backups  # line 1053
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1054
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1055
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1056
            for filename in filenames:  # line 1057
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1058
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1059
                totalsize += os.stat(encode(abspath)).st_size  # line 1060
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1061
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1062
                    continue  # don't backup backups  # line 1062
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1063
                    if show:  # line 1064
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1064
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1065
        if delta:  # line 1066
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1066
    info("\r" + pure.ljust(usage.MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1067

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1069
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1070
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1071
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1072
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1072
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1073
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1074
    if maxi is None:  # line 1075
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1075
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1076
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1079
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1081
    while files:  # line 1082
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1083
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1084
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1086
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1086
    tracked = None  # type: bool  # line 1087
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1087
    tracked, commitArgs = vcsCommits[cmd]  # line 1087
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1088
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1090
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1090
    if tracked:  # line 1091
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1091

def config(arguments: 'List[str]', options: 'List[str]'=[]):  # line 1093
    command = None  # type: str  # line 1094
    key = None  # type: str  # line 1094
    value = None  # type: str  # line 1094
    v = None  # type: str  # line 1094
    command, key, value = (arguments + [None] * 2)[:3]  # line 1095
    if command is None:  # line 1096
        usage.usage("help", verbose=True)  # line 1096
    if command not in ["set", "unset", "show", "list", "add", "rm"]:  # line 1097
        Exit("Unknown config command")  # line 1097
    local = "--local" in options  # type: bool  # line 1098
    m = Metadata()  # type: Metadata  # loads layered configuration as well. TODO warning if repo not exists  # line 1099
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # line 1100
    if command == "set":  # line 1101
        if None in (key, value):  # line 1102
            Exit("Key or value not specified")  # line 1102
        if key not in (([] if local else CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1103
            Exit("Unsupported key for %s configuration %r" % ("local " if local else "global", key))  # TODO move defaultbranch to configurable_texts?  # line 1103
        if key in CONFIGURABLE_FLAGS and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1104
            Exit("Cannot set flag to '%s'. Try on/off instead" % value.lower())  # line 1104
        c[key] = value.lower() in TRUTH_VALUES if key in CONFIGURABLE_FLAGS else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1105
    elif command == "unset":  # line 1106
        if key is None:  # line 1107
            Exit("No key specified")  # line 1107
        if key not in c.keys():  # HINT: Works on local configurations when used with --local  # line 1108
            Exit("Unknown key")  # HINT: Works on local configurations when used with --local  # line 1108
        del c[key]  # line 1109
    elif command == "add":  # line 1110
        if None in (key, value):  # line 1111
            Exit("Key or value not specified")  # line 1111
        if key not in CONFIGURABLE_LISTS:  # line 1112
            Exit("Unsupported key %r" % key)  # line 1112
        if key not in c.keys():  # prepare empty list, or copy from global, add new value below  # line 1113
            c[key] = [_ for _ in c.__defaults[key]] if local else []  # prepare empty list, or copy from global, add new value below  # line 1113
        elif value in c[key]:  # line 1114
            Exit("Value already contained, nothing to do")  # line 1114
        if ";" in value:  # line 1115
            c[key].append(removePath(key, value))  # line 1115
        else:  # line 1116
            c[key].extend([removePath(key, v) for v in value.split(";")])  # line 1116
    elif command == "rm":  # line 1117
        if None in (key, value):  # line 1118
            Exit("Key or value not specified")  # line 1118
        if key not in c.keys():  # line 1119
            Exit("Unknown key %r" % key)  # line 1119
        if value not in c[key]:  # line 1120
            Exit("Unknown value %r" % value)  # line 1120
        c[key].remove(value)  # line 1121
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1122
            del c[key]  # remove local entry, to fallback to global  # line 1122
    else:  # Show or list  # line 1123
        if key == "ints":  # list valid configuration items  # line 1124
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1124
        elif key == "flags":  # line 1125
            printo(", ".join(CONFIGURABLE_FLAGS))  # line 1125
        elif key == "lists":  # line 1126
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1126
        elif key == "texts":  # line 1127
            printo(", ".join([_ for _ in defaults.keys() if _ not in (CONFIGURABLE_FLAGS + CONFIGURABLE_LISTS)]))  # line 1127
        else:  # line 1128
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1129
            c = m.c  # always use full configuration chain  # line 1130
            try:  # attempt single key  # line 1131
                assert key is not None  # force exception  # line 1132
                c[key]  # force exception  # line 1132
                l = key in c.keys()  # type: bool  # line 1133
                g = key in c.__defaults.keys()  # type: bool  # line 1133
                printo("%s %s %r" % (key.rjust(20), out[3] if not (l or g) else (out[1] if l else out[2]), c[key]))  # line 1134
            except:  # normal value listing  # line 1135
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # line 1136
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1137
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1138
                for k, vt in sorted(vals.items()):  # line 1139
                    printo("%s %s %s" % (k.rjust(20), out[vt[1]], vt[0]))  # line 1139
                if len(c.keys()) == 0:  # line 1140
                    info("No local configuration stored")  # line 1140
                if len(c.__defaults.keys()) == 0:  # line 1141
                    info("No global configuration stored")  # line 1141
        return  # in case of list, no need to store anything  # line 1142
    if local:  # saves changes of repoConfig  # line 1143
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1143
        m.saveBranches()  # saves changes of repoConfig  # line 1143
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1143
    else:  # global config  # line 1144
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1145
        if f is None:  # TODO why no exit here?  # line 1146
            error("Error saving user configuration: %r" % h)  # TODO why no exit here?  # line 1146
        else:  # line 1147
            Exit("OK", code=0)  # line 1147

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1149
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1152
    if verbose:  # line 1153
        info(usage.MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1153
    force = '--force' in options  # type: bool  # line 1154
    soft = '--soft' in options  # type: bool  # line 1155
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1156
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1156
    m = Metadata()  # type: Metadata  # line 1157
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1158
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1159
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1160
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1161
    if not matching and not force:  # line 1162
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1162
    if not (m.track or m.picky):  # line 1163
        Exit("Repository is in simple mode. Simply use basic file operations to modify files, then execute 'sos commit' to version the changes")  # line 1163
    if pattern not in patterns:  # list potential alternatives and exit  # line 1164
        for tracked in (t for t in patterns if os.path.dirname(t) == relPath):  # for all patterns of the same source folder TODO use SLASH rindex  # line 1165
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1166
            if alternative:  # line 1167
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1167
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: if not (force or soft):  # line 1168
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1169
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1170
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1171
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1175
    oldTokens = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1176
    newToken = None  # type: _coconut.typing.Sequence[GlobBlock]  # line 1176
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1177
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1178
    if len({st[1] for st in matches}) != len(matches):  # line 1179
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1179
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1180
    if os.path.exists(encode(newRelPath)):  # line 1181
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1182
        if exists and not (force or soft):  # line 1183
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1183
    else:  # line 1184
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1184
    if not soft:  # perform actual renaming  # line 1185
        for (source, target) in matches:  # line 1186
            try:  # line 1187
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1187
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1188
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1188
    patterns[patterns.index(pattern)] = newPattern  # line 1189
    m.saveBranches()  # line 1190

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1192
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1193
    debug("Parsing command-line arguments...")  # line 1194
    root = os.getcwd()  # line 1195
    try:  # line 1196
        onlys, excps, remotes = parseArgumentOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1197
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1198
        arguments = [c.strip() for c in sys.argv[2:] if not (c.startswith("-") and (len(c) == 2 or c[1] == "-"))]  # type: List[_coconut.typing.Optional[str]]  # line 1199
        options = [c.strip() for c in sys.argv[2:] if c.startswith("-") and (len(c) == 2 or c[1] == "-")]  # options with arguments have to be parsed from sys.argv  # line 1200
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1201
        if command[:1] in "amr":  # line 1202
            relPath, pattern = relativize(root, os.path.join(cwd, arguments[0] if arguments else "."))  # line 1202
        if command[:1] == "m":  # line 1203
            if len(arguments) < 2:  # line 1204
                Exit("Need a second file pattern argument as target for move command")  # line 1204
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1205
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1206
        if command[:1] == "a":  # e.g. addnot  # line 1207
            add(relPath, pattern, options, negative="n" in command)  # e.g. addnot  # line 1207
        elif command[:1] == "b":  # line 1208
            branch(arguments[0], arguments[1], options)  # line 1208
        elif command[:3] == "com":  # line 1209
            commit(arguments[0], options, onlys, excps)  # line 1209
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1210
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1210
        elif command[:2] == "ci":  # line 1211
            commit(arguments[0], options, onlys, excps)  # line 1211
        elif command[:3] == 'con':  # line 1212
            config(arguments, options)  # line 1212
        elif command[:2] == "de":  # line 1213
            destroy(arguments[0], options)  # line 1213
        elif command[:2] == "di":  # line 1214
            diff(arguments[0], options, onlys, excps)  # line 1214
        elif command[:2] == "du":  # line 1215
            dump(arguments[0], options)  # line 1215
        elif command[:1] == "h":  # line 1216
            usage.usage(arguments[0], verbose=verbose)  # line 1216
        elif command[:2] == "lo":  # line 1217
            log(options, cwd)  # line 1217
        elif command[:2] == "li":  # line 1218
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1218
        elif command[:2] == "ls":  # line 1219
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1219
        elif command[:1] == "m":  # e.g. mvnot  # line 1220
            move(relPath, pattern, newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1220
        elif command[:2] == "of":  # line 1221
            offline(arguments[0], arguments[1], options, remotes)  # line 1221
        elif command[:2] == "on":  # line 1222
            online(options)  # line 1222
        elif command[:1] == "p":  # line 1223
            publish(arguments[0], cmd, options, onlys, excps)  # line 1223
        elif command[:1] == "r":  # e.g. rmnot  # line 1224
            remove(relPath, pattern, optoions, negative="n" in command)  # e.g. rmnot  # line 1224
        elif command[:2] == "st":  # line 1225
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1225
        elif command[:2] == "sw":  # line 1226
            switch(arguments[0], options, onlys, excps, cwd)  # line 1226
        elif command[:1] == "u":  # line 1227
            update(arguments[0], options, onlys, excps)  # line 1227
        elif command[:1] == "v":  # line 1228
            usage.usage(arguments[0], version=True)  # line 1228
        else:  # line 1229
            Exit("Unknown command '%s'" % command)  # line 1229
        Exit(code=0)  # regular exit  # line 1230
    except (Exception, RuntimeError) as E:  # line 1231
        exception(E)  # line 1232
        Exit("An internal error occurred in SOS. Please report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing")  # line 1233

def main():  # line 1235
    global debug, info, warn, error  # to modify logger  # line 1236
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1237
    _log = Logger(logging.getLogger(__name__))  # line 1238
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1238
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1239
        sys.argv.remove(option)  # clean up program arguments  # line 1239
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1240
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1240
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1241
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1242
    debug("Detected SOS root folder: %s\nDetected VCS root folder: %s" % (("-" if root is None else root), ("-" if vcs is None else vcs)))  # line 1243
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1244
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1245
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv"):  # in offline mode or just going offline TODO what about git config?  # line 1246
        cwd = os.getcwd()  # line 1247
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1248
        parse(vcs, cwd, cmd)  # line 1249
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1250
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1251
        import subprocess  # only required in this section  # line 1252
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1253
        inp = ""  # type: str  # line 1254
        while True:  # line 1255
            so, se = process.communicate(input=inp)  # line 1256
            if process.returncode is not None:  # line 1257
                break  # line 1257
            inp = sys.stdin.read()  # line 1258
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1259
            if root is None:  # line 1260
                Exit("Cannot determine VCS root folder: Unable to mark repository as synchronized and will show a warning when leaving offline mode")  # line 1260
            m = Metadata(root)  # type: Metadata  # line 1261
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1262
            m.saveBranches()  # line 1263
    else:  # line 1264
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1264


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: bool  # this is a trick allowing to modify the flags from the test suite  # line 1268
force_vcs = [None] if '--vcs' in sys.argv else []  # type: bool  # line 1269
verbose = [None] if '--verbose' in sys.argv or '-v' in sys.argv else []  # type: bool  # imported from utility, and only modified here  # line 1270
debug_ = [None] if os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv else []  # type: bool  # line 1271
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1272

_log = Logger(logging.getLogger(__name__))  # line 1274
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1274

if __name__ == '__main__':  # line 1276
    main()  # line 1276
