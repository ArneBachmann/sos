#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xb21dc8bd

# Compiled with Coconut version 1.4.0-post_dev8 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get("__coconut__")
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules["__coconut__"]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_addpattern, _coconut_sentinel
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
# TODO needed as paths differ when installed via pip TODO #243 investigate further
from sos import usage  # line 7
from sos import version  # line 8
from sos import utility as _utility  # WARN necessary because "tests" can only mock "sos.utility.input", because "sos" does "import *" from "utility" and "sos.input" cannot be mocked for some reason  # line 9
from sos.utility import *  # line 10
from sos.pure import *  # line 11

# Dependencies
try:  # line 14
    import configr  # line 14
except:  # TODO this is here to avoid import error when setup.py is called but actually needs to install its dependencies first. Enhance this  # line 15
    pass  # TODO this is here to avoid import error when setup.py is called but actually needs to install its dependencies first. Enhance this  # line 15


# Lazy module auto-import for quick tool startup
shutil = None  # type: Union[object]  # line 19
class shutil:  # line 20
    @_coconut_tco  # line 20
    def __getattribute__(_, key):  # line 20
        global shutil  # line 21
        import shutil  # overrides global reference  # line 22
        return _coconut_tail_call(shutil.__getattribute__, key)  # line 23
shutil = shutil()  # line 24


# Functions
def loadConfig() -> 'configr.Configr':  # line 28
    ''' Simplifies loading user-global config from file system or returning application defaults. '''  # line 29
    config = configr.Configr(usage.COMMAND, defaults=defaults)  # type: configr.Configr  # defaults are used if key is not configured, but won't be saved  # line 30
    f, g = config.loadSettings(clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # required for testing only  # line 31
    if f is None:  # line 32
        debug("Encountered a problem while loading the user configuration: %r" % g)  # line 32
    return config  # line 33

@_coconut_tco  # line 35
def saveConfig(config: 'configr.Configr') -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[Exception]]':  # line 35
    return _coconut_tail_call(config.saveSettings, clientCodeLocation=os.path.abspath(__file__), location=os.environ.get("TEST", None))  # saves global config, not local one  # line 36


# Main data class
class Metadata:  # line 40
    ''' This class doesn't represent the entire repository state in memory,
      but serves as a container for different repo operations,
      using only parts of its attributes at any point in time. Use with care.
  '''  # line 44

    singleton = None  # type: _coconut.typing.Optional[configr.Configr]  # line 46

    def __init__(_, path: '_coconut.typing.Optional[str]'=None, offline: 'bool'=False, remotes: 'List[str]'=[]) -> 'None':  # line 48
        ''' Create empty container object for various repository operations, and import configuration. Offline initializes a repository.
        path: manual root path configuration, otherwise auto-detect
        offline:
        remotes: only used for "sos offline --remote ..." or "--only-remote[s]"
    '''  # line 53
        _.root = (os.getcwd() if path is None else path)  # type: str  # line 54
        _.tags = []  # type: List[str]  # list of known (unique) tags  # line 55
        _.branch = None  # type: _coconut.typing.Optional[int]  # current branch number  # line 56
        _.branches = {}  # type: Dict[int, BranchInfo]  # branch number zero represents the initial state at branching  # line 57
        _.repoConf = {}  # type: Dict[str, Any]  # per-repo configuration items  # line 58
        _.track = None  # type: _coconut.typing.Optional[bool]  # line 59
        _.picky = None  # type: _coconut.typing.Optional[bool]  # line 59
        _.strict = None  # type: _coconut.typing.Optional[bool]  # line 59
        _.compress = None  # type: _coconut.typing.Optional[bool]  # line 59
        _.version = None  # type: _coconut.typing.Optional[str]  # line 59
        _.format = None  # type: _coconut.typing.Optional[int]  # line 59
        _.remotes = []  # type: List[str]  # list of secondary storage locations (in same file system, no other protocols), which will replicate all write operations  # line 60
        _.loadBranches(offline=offline, remotes=remotes)  # loads above values from repository, or uses application defaults  # line 61

        _.commits = {}  # type: Dict[int, CommitInfo]  # consecutive numbers per branch, starting at 0  # line 63
        _.paths = {}  # type: Dict[str, PathInfo]  # utf-8 encoded relative, normalized file system paths  # line 64
        _.commit = None  # type: _coconut.typing.Optional[int]  # current revision number  # line 65

        if Metadata.singleton is None:  # load configuration lazily only once per runtime  # line 67
            Metadata.singleton = configr.Configr(data=_.repoConf, defaults=loadConfig())  # load global configuration backed by defaults, as fallback behind the local configuration  # line 68
            if "useColorOutput" in Metadata.singleton:  # otherwise keep default  # line 69
                enableColor(Metadata.singleton.useColorOutput)  # otherwise keep default  # line 69
        _.c = Metadata.singleton  # type: configr.Configr  # line 70

    def isTextType(_, filename: 'str') -> 'bool':  # line 72
        ''' Based on the file extension or user-defined file patterns, this function determines if the file is of any diffable text type. '''  # line 73
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
        ''' Load list of branches and current branch info from metadata file.
        offline: if True, avoid messages
        remotes: manually provided remotes when using "sos offline --remote"
    '''  # line 100
        try:  # fails if not yet created (on initial branch/commit)  # line 101
#      branches:List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 103
                repo, branches, config = json.load(fd)  # line 104
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 105
            _.branch = repo["branch"]  # current branch integer  # line 106
            _.track, _.picky, _.strict, _.compress, _.version, _.format, _.remotes, remote = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format", "remotes", "remote"]]  # line 107
            if remote:  # line 108
                Exit("Cannot access remote SOS repository for local operation. You're attempting to access a backup copy. Consult manual to restore this backup for normal operation")  # line 108
            upgraded = []  # type: List[str]  # line 109
            if _.version is None:  # line 110
                _.version = "0 - pre-1.2"  # line 111
                upgraded.append("pre-1.2")  # line 112
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 113
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 114
                upgraded.append("2018.1210.3028")  # line 115
            if _.format is None:  # must be before 1.3.5+  # line 116
                _.format = 1  # marker for first metadata file format  # line 117
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 118
                upgraded.append("1.3.5")  # line 119
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 120
            _.repoConf = config  # local configuration stored with repository, not in user-wide configuration  # line 121
            if _.format == 1 or _.remotes is None:  # before remotes  # line 122
                _.format = METADATA_FORMAT  # line 123
                _.remotes = []  # default is no remotes, and this conversion can never happen at "sos offline"  # line 124
                upgraded.append("1.7.0")  # remote URLs introduced  # line 125
            if upgraded:  # line 126
                for upgrade in upgraded:  # line 127
                    printo("WARNING  Upgraded repository metadata to match SOS version %r" % upgrade, color=Fore.YELLOW)  # line 127
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 128
                _.saveBranches(_.remotes)  # line 129
        except Exception as E:  # if not found, create metadata folder with default values  # line 130
            _.branches = {}  # line 131
            _.track, _.picky, _.strict, _.compress, _.version, _.remotes, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, remotes, METADATA_FORMAT]  # line 132
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # hide warning only when going offline  # line 133

    def _saveBranches(_, remote: '_coconut.typing.Optional[str]', data: 'Dikt[str, Any]'):  # line 135
        ''' Subfunction to save branches to a local or remote offline repository location. '''  # line 136
        tryOrIgnore(lambda: shutil.copy2(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), encode(os.path.join((_.root if remote is None else remote), metaFolder, metaBack))))  # backup  # line 137
        try:  # line 138
            with codecs.open(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 138
                json.dump((data, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints (instead of ascii encoding), the file descriptor knows how to encode them  # line 139
        except Exception as E:  # line 140
            debug("Error saving branches%s" % ((" to remote path " + remote) if remote else ""))  # line 140

    def saveBranches(_, remotes: 'List[str]'=[], also: 'Dict[str, Any]'={}):  # line 142
        ''' Save list of branches and current branch info to metadata file. '''  # line 143
        store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT, "remotes": _.remotes, "remote": False}  # type: Dict[str, Any]  # dictionary of repository settings (while _.repoConf stores user settings)  # line 144
        store.update(also)  # allows overriding certain values at certain points in time  # line 150
        for remote in [None] + remotes:  # line 151
            _._saveBranches(remote, store)  # mark remote copies as read-only  # line 152
            store["remote"] = True  # mark remote copies as read-only  # line 152

    def _extractRemotesFromArguments(_, options: 'List[str]') -> 'List[str]':  # line 154
        ''' Common behavior to parse and extract the remotes options from command line-arguments. '''  # line 155
        _a = None  # type: Any  # line 156
        remotes = None  # type: List[str]  # line 156
        noremotes = None  # type: List[str]  # line 156
        _a, _a, remotes, noremotes = parseArgumentOptions("", options)  # re-parse options for the --(only-)remotes and --exlude-remotes options  # line 157
        return [] if "--no-remotes" in options or "--no-remote" in options else list(set(remotes if remotes else _.remotes) - set(noremotes))  # line 158

    def getRevisionByName(_, name: '_coconut.typing.Optional[str]') -> '_coconut.typing.Optional[int]':  # line 160
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 161
        if (("" if name is None else name)) == "":  # line 162
            return -1  # line 162
        try:  # attempt to parse integer string  # line 163
            return int(name)  # attempt to parse integer string  # line 163
        except ValueError:  # line 164
            pass  # line 164
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 165
        return found[0] if found else None  # line 166

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 168
        ''' Convenience accessor for named branches.
        returns: branch index 0.. or None if not found
    '''  # line 171
        if name == "":  # current  # line 172
            return _.branch  # current  # line 172
        try:  # attempt to parse integer string  # line 173
            return int(name)  # attempt to parse integer string  # line 173
        except ValueError:  # line 174
            pass  # line 174
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 175
        return found[0] if found else None  # line 176

    def loadBranch(_, branch: 'int'):  # line 178
        ''' Load all commit information from a branch meta data file. '''  # line 179
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 180
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 181
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 182
        _.branch = branch  # line 183

    def saveBranch(_, branch: 'int', options: 'List[str]'=[]):  # line 185
        ''' Save all commits to a branch meta data file. '''  # line 186
        remotes = _._extractRemotesFromArguments(options)  # type: List[str]  # line 187
        for remote in [None] + remotes:  # line 188
            tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile, base=remote)), encode(branchFolder(branch, file=metaBack, base=remote))))  # backup  # line 189
            try:  # line 190
                with codecs.open(encode(branchFolder(branch, file=metaFile, base=remote)), "w", encoding=UTF8) as fd:  # line 190
                    json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 191
            except Exception as E:  # line 192
                debug("Error saving branch%s" % ((" to remote path " + remote) if remote else ""))  # line 192

    def duplicateBranch(_, branch: 'int', options: 'List[str]'=[], name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 194
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 202
        remotes = _._extractRemotesFromArguments(options)  # type: List[str]  # line 203
        if verbose:  # line 204
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 204
        now = int(time.time() * 1000)  # type: int  # line 205
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 206
        revision = max(_.commits) if _.commits else 0  # type: int  # line 207
        _.commits.clear()  # line 208
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 209
        for remote in [None] + remotes:  # line 214
            tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)) if full else branchFolder(branch, base=(_.root if remote is None else remote)))), lambda e: error("Duplicating remote branch folder %r" % remote))  # line 215
        if full:  # not fast branching via reference - copy all current files to new branch  # line 216
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 217
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 218
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 218
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit  # line 219
            _.saveCommit(branch, 0, remotes)  # save commit meta data to revision folder  # line 220
        _.saveBranch(branch, options)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 221
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 222

    def createBranch(_, branch: 'int', options: 'List[str]'=[], name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 224
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 230
        now = int(time.time() * 1000)  # type: int  # line 231
        remotes = _._extractRemotesFromArguments(options)  # type: List[str]  # line 232
        simpleMode = not (_.track or _.picky)  # type: bool  # line 233
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 234
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 235
        if verbose:  # line 236
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 236
        _.paths = {}  # type: Dict[str, PathInfo]  # line 237
        if simpleMode:  # branches from file system state. not necessary to create branch folder, as it is done in findChanges below anyway  # line 238
            changed, msg = _.findChanges(branch, 0, progress=simpleMode, remotes=remotes)  # HINT creates revision folder and versioned files!  # line 239
            _.listChanges(changed)  # line 240
            if msg:  # display compression factor and time taken  # line 241
                printo(msg)  # display compression factor and time taken  # line 241
            _.paths.update(changed.additions.items())  # line 242
        else:  # tracking or picky mode: branch from latest revision  # line 243
            for remote in [None] + remotes:  # line 244
                tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)))), lambda e: error("Creating remote branch folder %r" % remote))  # line 245
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 246
                _.loadBranch(_.branch)  # line 247
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO #245 what if last switch was to an earlier revision? no persisting of last checkout  # line 248
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 249
                for path, pinfo in _.paths.items():  # line 250
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 250
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 251
        _.saveBranch(branch, remotes)  # save branch meta data (revisions) to branch folder  # line 252
        _.saveCommit(branch, 0, remotes)  # save commit meta data to revision folder  # line 253
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 254

    def removeBranch(_, branch: 'int', options: 'List[str]'=[]) -> 'BranchInfo':  # line 256
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 259
        import collections  # used almost only here  # line 260
        binfo = None  # type: BranchInfo  # typing info  # line 261
        remotes = _._extractRemotesFromArguments(options)  # type: List[str]  # line 262
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 263
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 264
        if deps:  # need to copy all parent revisions to dependent branches first  # line 265
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 266
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 267
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 268
                for dep, _rev in deps:  # line 269
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO #246 align placement of indicator with other uses of progress  # line 270
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 271
#          if rev in _.commits:  # TODO #247 uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 273
                    for remote in [None] + remotes:  # line 274
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=(_.root if remote is None else remote))), encode(revisionFolder(dep, rev, base=(_.root if remote is None else remote))))  # line 275
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 276
                for rev in range(minrev + 1, _rev + 1):  # line 277
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 278
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 279
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 280
                        newcommits[dep][rev] = _.commits[rev]  # line 281
                        for remote in [None] + remotes:  # line 282
                            shutil.copytree(encode(revisionFolder(_.branch, rev, base=(_.root if remote is None else remote))), encode(revisionFolder(dep, rev, base=(_.root if remote is None else remote))))  # line 283
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 284
        printo(pure.ljust() + "\r")  # clean line output  # line 285
        for remote in [None] + remotes:  # line 286
            tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch, base=remote) + BACKUP_SUFFIX)))  # remove previous backup first  # line 287
            tryOrIgnore(lambda: os.rename(encode(branchFolder(branch, base=remote)), encode(branchFolder(branch, base=remote) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?", excp=E))  # line 288
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 289
        del _.branches[branch]  # line 290
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 291
        _.saveBranches(remotes)  # persist modified branches list  # line 292
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 293
            _.commits = commits  # line 294
            _.saveBranch(branch, remotes)  # line 295
        _.commits.clear()  # clean memory  # line 296
        return binfo  # line 297

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 299
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 300
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 301
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 302
            _.paths = json.load(fd)  # line 302
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 303
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 304

    def saveCommit(_, branch: 'int', revision: 'int', remotes: 'List[str]'=[]):  # line 306
        ''' Save all file information to a commit meta data file. '''  # line 307
        for remote in [None] + remotes:  # line 308
            try:  # line 309
                target = revisionFolder(branch, revision, base=(_.root if remote is None else remote))  # type: str  # line 310
                tryOrIgnore(lambda _=None: os.makedirs(encode(target)))  # line 311
                tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 312
                with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 313
                    json.dump(_.paths, fd, ensure_ascii=False)  # line 313
            except Exception as E:  # line 314
                debug("Error saving commit%s" % ((" to remote path " + remote) if remote else ""))  # line 314

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False, remotes: '_coconut.typing.Optional[List[str]]'=None) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 316
        ''' Find changes on the file system vs. in-memory paths (which should reflect the latest commit state).
        Only if both branch and revision are *not* None, write modified/added files to the specified revision folder (thus creating a new revision)
        branch: branch to write to
        revision: revision to write to
        checkContent: also computes file content hashes
        inverse: retain original state (size, mtime, hash) instead of updated one
        considerOnly: set of tracking patterns. None for all (in simple mode). For update operation, consider union of other and current branch
        dontConsider: set of tracking patterns to not consider in changes (always overrides considerOnly!)
        progress: Show file names during processing
        remotes: all remote locations to write to
        returns: (ChangeSet = the state of file tree *differences*, unless "inverse" is True -> then return original data, message)
        WARN: when changing this function's signature, remember to change the patched() function in the test suite
    '''  # line 329
        import collections  # used almost only here  # line 330
        write = branch is not None and revision is not None  # used for writing commits  # line 331
        if write:  # TODO ?? should not be necessary, as write is only true when committing, where remotes is provided externally anyway  # line 332
            for remote in [None] + ((_.remotes if remotes is None else remotes)):  # TODO ?? should not be necessary, as write is only true when committing, where remotes is provided externally anyway  # line 332
                tryOrIgnore(lambda: os.makedirs(encode(revisionFolder(branch, revision, base=(_.root if remote is None else remote)))))  # line 333
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # WARN this code needs explicity argument passing for initialization due to mypy problems with default arguments  # line 334
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 335
        hashed = None  # type: _coconut.typing.Optional[str]  # line 336
        written = None  # type: int  # line 336
        compressed = 0  # type: int  # line 336
        original = 0  # type: int  # line 336
        start_time = time.time()  # type: float  # line 336
        knownPaths = {}  # type: Dict[str, List[str]]  # line 337

# Find relevant folders/files that match specified folder/glob patterns for exclusive inclusion or exclusion
        byFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 340
        onlyByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 341
        dontByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 342
        for path, pinfo in _.paths.items():  # line 343
            if pinfo is None:  # quicker than generator expression above  # line 344
                continue  # quicker than generator expression above  # line 344
            slash = path.rindex(SLASH)  # type: int  # line 345
            byFolder[path[:slash]].append(path[slash + 1:])  # line 346
        for pattern in ([] if considerOnly is None else considerOnly):  # line 347
            slash = pattern.rindex(SLASH)  # line 347
            onlyByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 347
        for pattern in ([] if dontConsider is None else dontConsider):  # line 348
            slash = pattern.rindex(SLASH)  # line 348
            dontByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 348
        for folder, paths in byFolder.items():  # line 349
            pos = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in onlyByFolder.get(folder, [])]) if considerOnly is not None else set(paths)  # type: Set[str]  # line 350
            neg = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in dontByFolder.get(folder, [])]) if dontConsider is not None else set()  # type: Set[str]  # line 351
            knownPaths[folder] = list(pos - neg)  # line 352

        for path, dirnames, filenames in os.walk(_.root):  # line 354
            path = decode(path)  # line 355
            dirnames[:] = [decode(d) for d in dirnames]  # line 356
            filenames[:] = [decode(f) for f in filenames]  # line 357
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 358
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 359
            dirnames.sort()  # line 360
            filenames.sort()  # line 360
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 361
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 362
            if dontConsider:  # line 363
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 364
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 365
                filename = relPath + SLASH + file  # line 366
                filepath = os.path.join(path, file)  # line 367
                try:  # line 368
                    stat = os.stat(encode(filepath))  # line 368
                except Exception as E:  # line 369
                    printo(exception(E))  # line 369
                    continue  # line 369
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 370
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 371
                if show:  # indication character returned  # line 372
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 373
                    printo(pure.ljust(outstring), nl="")  # line 374
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 375
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 376
                    nameHash = hashStr(filename)  # line 377
                    try:  # line 378
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=nameHash) for remote in [None] + _.remotes] if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 379
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 380
                        compressed += written  # line 381
                        original += size  # line 381
                    except PermissionError as E:  # line 382
                        error("File permission error for %s" % filepath)  # line 382
                    except Exception as F:  # HINT e.g. FileNotFoundError will not add to additions  # line 383
                        printo(exception(F))  # HINT e.g. FileNotFoundError will not add to additions  # line 383
                    continue  # with next file  # line 384
                last = _.paths[filename]  # filename is known - check for modifications  # line 385
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 386
                    try:  # line 387
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not (progress and show) else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 388
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 389
                        continue  # line 389
                        compressed += written  # line 390
                        original += last.size if inverse else size  # line 390
                    except Exception as E:  # line 391
                        printo(exception(E))  # line 391
                elif (size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False))):  # detected a modification TODO invert error = False?  # line 392
                    try:  # line 396
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not (progress and show) else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else hashFile(filepath, _.compress, symbols=progressSymbols, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl=""))[0], 0)  # line 397
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 401
                        compressed += written  # line 402
                        original += last.size if inverse else size  # line 402
                    except Exception as E:  # line 403
                        printo(exception(E))  # line 403
                else:  # with next file  # line 404
                    continue  # with next file  # line 404
            if relPath in knownPaths:  # at least one file is tracked or --only HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 405
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked or --only HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 405
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 406
            for file in names:  # line 407
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 408
                    continue  # don't mark ignored files as deleted  # line 408
                pth = path + SLASH + file  # type: str  # line 409
                changed.deletions[pth] = _.paths[pth]  # line 410
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, _.strict))  # line 411
        if progress:  # forces clean line of progress output  # line 412
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 412
        elif verbose:  # line 413
            info("Finished detecting changes")  # line 413
        tt = time.time() - start_time  # type: float  # time taken  # line 414
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # in KiBi  # line 415
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 416
        msg = (msg + " | " if msg else "") + ("Processing speed was %.2f %siB/s." % (speed if speed < 1500. else speed / KIBI, "k" if speed < 1500. else "M") if original > 0 and tt > 0. else "")  # line 417
        return (changed, msg if msg else None)  # line 418

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 420
        ''' Returns nothing, just updates _.paths in place. '''  # line 421
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 422

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 424
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 425
        try:  # load initial paths  # line 426
            _.loadCommit(branch, startwith)  # load initial paths  # line 426
        except:  # no revisions  # line 427
            yield {}  # no revisions  # line 427
            return None  # no revisions  # line 427
        if incrementally:  # line 428
            yield _.paths  # line 428
        m = Metadata(_.root)  # type: Metadata  # next changes TODO #250 avoid loading all metadata and config  # line 429
        rev = None  # type: int  # next changes TODO #250 avoid loading all metadata and config  # line 429
        for rev in range(startwith + 1, revision + 1):  # line 430
            m.loadCommit(branch, rev)  # line 431
            for p, info in m.paths.items():  # line 432
                if info.size == None:  # line 433
                    del _.paths[p]  # line 433
                else:  # line 434
                    _.paths[p] = info  # line 434
            if incrementally:  # line 435
                yield _.paths  # line 435
        yield None  # for the default case - not incrementally  # line 436

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 438
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 439
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 440

    def parseRevisionString(_, argument: 'str') -> 'Union[Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]], NoReturn]':  # line 442
        ''' Parse (an optionally) combined branch and revision string, separated by a slash.
        Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit (Python convention)
        (None, None) is returned in case of illegal inputs
        sys.exit() is called in case of unknown branch/revision
    '''  # line 448
        argument = (("/" if argument is None else argument)).strip()  # line 449
        if argument == SLASH:  # no branch/revision specified  # line 450
            return (_.branch, -1)  # no branch/revision specified  # line 450
        if argument == "":  # nothing specified by user, raise error in caller  # line 451
            return (None, None)  # nothing specified by user, raise error in caller  # line 451
        if argument.startswith(SLASH):  # current branch  # line 452
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 452
        if argument.endswith(SLASH):  # line 453
            try:  # line 454
                return (_.getBranchByName(argument[:-1]), -1)  # line 454
            except ValueError as E:  # line 455
                Exit("Unknown branch label '%s'" % argument, excp=E)  # line 455
        if SLASH in argument:  # line 456
            b, r = argument.split(SLASH)[:2]  # line 457
            try:  # line 458
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 458
            except ValueError as E:  # line 459
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r), excp=E)  # line 459
        branch = _.getBranchByName(argument)  # type: _coconut.typing.Optional[int]  # returns number if given (revision) integer  # line 460
        if branch not in _.branches:  # line 461
            branch = None  # line 461
        try:  # either branch name/number or reverse/absolute revision number  # line 462
            return ((_.branch if branch is None else branch), ((lambda _coconut_none_coalesce_item: -1 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.getRevisionByName(argument))) if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 462
        except Exception as E:  # line 463
            Exit("Unknown branch label or wrong branch/revision number format", excp=E)  # line 463
        Exit("This should never happen. Please create an issue report")  # line 464

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 466
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 468
        while True:  # line 469
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 470
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 471
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 472
                break  # line 472
            revision -= 1  # line 473
            if revision < 0:  # line 474
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 474
        return revision, source  # line 475

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 477
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 478
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 479
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 480
            return [branch]  # found. need to load commit from other branch instead  # line 480
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 481
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 481
        return others  # line 482

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 484
        return _.getParentBranches(branch, revision)[-1]  # line 484

    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 486
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 487
        m = Metadata()  # type: Metadata  # line 488
        other = branch  # type: _coconut.typing.Optional[int]  # line 489
        while other is not None:  # line 490
            m.loadBranch(other)  # line 491
            if m.commits:  # line 492
                return max(m.commits)  # line 492
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 493
        return None  # line 494

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 496
        ''' Copy versioned file to other branch/revision. '''  # line 497
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 498
        for remote in [None] + _.remotes:  # line 499
            try:  # line 500
                target = revisionFolder(toBranch, toRevision, file=pinfo.nameHash, base=(_.root if remote is None else remote))  # type: str  # line 501
                shutil.copy2(encode(source), encode(target))  # line 502
            except Exception as E:  # line 503
                error("Copying versioned file%s" % ((" to remote path " % remote) if remote else ""))  # line 503

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 505
        ''' Return file contents, or copy contents into file path provided (used in update and restorefile). '''  # line 506
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 507
        try:  # line 508
            with openIt(source, "r", _.compress) as fd:  # line 508
                if toFile is None:  # read bytes into memory and return  # line 509
                    return fd.read()  # read bytes into memory and return  # line 509
                with open(encode(toFile), "wb") as to:  # line 510
                    while True:  # line 511
                        buffer = fd.read(bufSize)  # line 512
                        to.write(buffer)  # line 513
                        if len(buffer) < bufSize:  # line 514
                            break  # line 514
                    return None  # line 515
        except Exception as E:  # line 516
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 516
        None  # line 517

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 519
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 520
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 521
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 521
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 522
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 523
            tryOrIgnore(lambda _=None: os.makedirs(encode(os.path.dirname(target))))  # line 524
        if pinfo.size == 0:  # line 525
            with open(encode(target), "wb"):  # line 526
                pass  # line 526
            try:  # update access/modification timestamps on file system  # line 527
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 527
            except Exception as E:  # line 528
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 528
            return None  # line 529
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 530
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 532
            while True:  # line 533
                buffer = fd.read(bufSize)  # line 534
                to.write(buffer)  # line 535
                if len(buffer) < bufSize:  # line 536
                    break  # line 536
        try:  # update access/modification timestamps on file system  # line 537
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 537
        except Exception as E:  # line 538
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 538
        return None  # line 539


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], remotes: 'List[str]'=[]):  # line 543
    ''' Initial command to start working offline. '''  # line 544
    if os.path.exists(encode(metaFolder)):  # line 545
        if '--force' not in options:  # line 546
            Exit("Repository folder is either already offline or older branches and commits were left over\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 546
        try:  # throw away all previous metadata before going offline  # line 547
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 548
                resource = metaFolder + os.sep + entry  # line 549
                if os.path.isdir(resource):  # line 550
                    shutil.rmtree(encode(resource))  # line 550
                else:  # line 551
                    os.unlink(encode(resource))  # line 551
        except Exception as E:  # line 552
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder, excp=E)  # line 552
    for remote in remotes:  # line 553
        try:  # line 554
            os.makedirs(os.path.join(remote, metaFolder))  # line 554
        except Exception as E:  # line 555
            error("Creating remote repository metadata in %s" % remote)  # line 555
    m = Metadata(offline=True, remotes=remotes)  # type: Metadata  # line 556
    if '--strict' in options or m.c.strict:  # always hash contents  # line 557
        m.strict = True  # always hash contents  # line 557
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 558
        m.compress = True  # plain file copies instead of compressed ones  # line 558
    if '--picky' in options or m.c.picky:  # Git-like  # line 559
        m.picky = True  # Git-like  # line 559
    elif '--track' in options or m.c.track:  # Svn-like  # line 560
        m.track = True  # Svn-like  # line 560
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 561
    if title:  # line 562
        printo(title)  # line 562
    if verbose:  # line 563
        info(MARKER + "Going offline...")  # line 563
    m.createBranch(0, remotes, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 564
    m.branch = 0  # line 565
    m.saveBranches(remotes=remotes, also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 566
    if verbose or '--verbose' in options:  # line 567
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 567
    info(MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 568

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 570
    ''' Finish working offline. '''  # line 571
    if verbose:  # line 572
        info(MARKER + "Going back online...")  # line 572
    force = '--force' in options  # type: bool  # line 573
    m = Metadata()  # type: Metadata  # line 574
    remotes = m._extractRemotesFromArguments(options)  # type: List[str]  # line 575
    strict = '--strict' in options or m.strict  # type: bool  # line 576
    m.loadBranches()  # line 577
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 578
        Exit("There are still unsynchronized (modified) branches\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions without further action.")  # line 578
    m.loadBranch(m.branch)  # line 579
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 580
    if options.count("--force") < 2:  # line 581
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 582
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 583
        if modified(changed):  # line 584
            Exit("File tree is modified vs. current branch\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 588
    try:  # line 589
        shutil.rmtree(encode(metaFolder))  # line 589
        info("Exited offline mode. Continue working with your traditional VCS." + (" Remote copies have to be removed manually." if remotes else ""))  # line 589
    except Exception as E:  # line 590
        Exit("Error removing offline repository.", excp=E)  # line 590
    info(MARKER + "Offline repository removed, you're back online")  # line 591

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 593
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not required here, as either branching from last revision anyway, or branching full file tree anyway.
  '''  # line 596
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 597
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 598
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 599
    m = Metadata()  # type: Metadata  # line 600
    remotes = m._extractRemotesFromArguments(options)  # line 601
    m.loadBranch(m.branch)  # line 602
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 603
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 604
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 604
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 605
    if verbose:  # line 606
        info(MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 606
    if last:  # branch from last revision  # line 607
        m.duplicateBranch(branch, remotes, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 607
    else:  # branch from current file tree state  # line 608
        m.createBranch(branch, remotes, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 608
    if not stay:  # line 609
        m.branch = branch  # line 609
    m.saveBranches(remotes)  # TODO #253 or indent again?  # line 610
    info(MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 611

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 613
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 614
    m = Metadata()  # type: Metadata  # line 615
    branch = None  # type: _coconut.typing.Optional[int]  # line 615
    revision = None  # type: _coconut.typing.Optional[int]  # line 615
    strict = '--strict' in options or m.strict  # type: bool  # line 616
    branch, revision = m.parseRevisionString(argument)  # line 617
    if branch is None or branch not in m.branches:  # line 618
        Exit("Unknown branch")  # line 618
    m.loadBranch(branch)  # knows commits  # line 619
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 620
    if verbose:  # line 621
        info(MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 621
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 622
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 623
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 628
    return changed  # returning for unit tests only TODO #254 remove?  # line 629

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False, classic: 'bool'=False):  # TODO #255 introduce option to diff against committed revision and not only file tree  # line 631
    ''' The diff display code. '''  # line 632
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 633
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 634
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 635
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 636
    for path, pinfo in sorted((c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0])))):  # only consider modified text files TODO also show timestamp change for binary files (+full compare?)  # line 637
        content = b""  # type: _coconut.typing.Optional[bytes]  # stored state (old = "curr")  # line 638
        if pinfo.size != 0:  # versioned file  # line 639
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 639
            assert content is not None  # versioned file  # line 639
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current state (new = "into")  # line 640
        if classic:  # line 641
            mergeClassic(content, abspath, "b%d/r%02d" % (branch, revision), os.path.basename(abspath), pinfo.mtime, number_)  # line 641
            continue  # line 641
        blocks = None  # type: List[MergeBlock]  # line 642
        nl = None  # type: bytes  # line 642
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 643
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]))  # line 644
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 645
        for block in blocks:  # line 646
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some of previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # line 649
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 650
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 650
            elif block.tipe == MergeBlockType.REMOVE:  # line 651
                for no, line in enumerate(block.lines):  # line 652
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 652
            elif block.tipe == MergeBlockType.REPLACE:  # line 653
                for no, line in enumerate(block.replaces.lines):  # line 654
                    printo(wrap("old %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 654
                for no, line in enumerate(block.lines):  # line 655
                    printo(wrap("now %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 655
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 658
                printo()  # line 658

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 660
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 661
    m = Metadata()  # type: Metadata  # line 662
    branch = None  # type: _coconut.typing.Optional[int]  # line 662
    revision = None  # type: _coconut.typing.Optional[int]  # line 662
    strict = '--strict' in options or m.strict  # type: bool  # line 663
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 664
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 665
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 666
    if branch is None or branch not in m.branches:  # line 667
        Exit("Unknown branch")  # line 667
    m.loadBranch(branch)  # knows commits  # line 668
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 669
    if verbose:  # line 670
        info(MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 670
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 671
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 672
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap, classic='--classic' in options)  # line 677

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 679
    ''' Create new revision from file tree changes vs. last commit. '''  # line 680
    m = Metadata()  # type: Metadata  # line 681
    if argument is not None and argument in m.tags:  # line 682
        Exit("Illegal commit message. It was already used as a (unique) tag name and cannot be reused")  # line 682
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 683
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 685
        Exit("No file patterns staged for commit in picky mode")  # line 685
    if verbose:  # line 686
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 686
    remotes = m._extractRemotesFromArguments(options)  # line 687
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 688
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 689
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 690
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 691
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 692
    m.saveCommit(m.branch, revision, remotes)  # revision has already been incremented  # line 693
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 694
    m.saveBranch(m.branch, remotes)  # line 695
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 696
    if m.picky:  # remove tracked patterns  # line 697
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 697
    else:  # track or simple mode: set branch modified  # line 698
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 698
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 699
        m.tags.append(argument)  # memorize unique tag  # line 699
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 699
    m.saveBranches(remotes)  # line 700
    stored = 0  # type: int  # now determine new commit size on file system  # line 701
    overhead = 0  # type: int  # now determine new commit size on file system  # line 701
    count = 0  # type: int  # now determine new commit size on file system  # line 701
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 702
    for file in os.listdir(commitFolder):  # line 703
        try:  # line 704
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 705
            if file == metaFile:  # line 706
                overhead += newsize  # line 706
            else:  # line 707
                stored += newsize  # line 707
                count += 1  # line 707
        except Exception as E:  # line 708
            error(E)  # line 708
    printo(MARKER_COLOR + "Created new revision r%02d%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%s%s%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, (" '%s'" % argument) if argument is not None else "", Fore.GREEN, Fore.RESET, len(changed.additions) - len(changed.moves), Fore.RED, Fore.RESET, len(changed.deletions) - len(changed.moves), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(changed.modifications), Fore.BLUE + Style.BRIGHT, MOVE_SYMBOL if m.c.useUnicodeFont else "#", Style.RESET_ALL, len(changed.moves), pure.siSize(stored + overhead), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 709

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 721
    ''' Show branches and current repository state. '''  # line 722
    m = Metadata()  # type: Metadata  # line 723
    if not (m.c.useChangesCommand or any((option.startswith('--repo') for option in options))):  # line 724
        changes(argument, options, onlys, excps)  # line 724
        return  # line 724
    current = m.branch  # type: int  # line 725
    strict = '--strict' in options or m.strict  # type: bool  # line 726
    printo(MARKER_COLOR + "Offline repository status")  # line 727
    printo("Repository root:     %s" % os.getcwd())  # line 728
    printo("Underlying VCS root: %s" % vcs)  # line 729
    printo("Underlying VCS type: %s" % cmd)  # line 730
    printo("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 731
    printo("Current SOS version: %s" % version.__version__)  # line 732
    printo("At creation version: %s" % m.version)  # line 733
    printo("Metadata format:     %s" % m.format)  # line 734
    printo("Content checking:    %s" % (Fore.CYAN + "size, then content" if m.strict else Fore.BLUE + "size & timestamp") + Fore.RESET)  # TODO size then timestamp?  # line 735
    printo("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 736
    printo("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 737
    printo("Number of branches:  %d" % len(m.branches))  # line 738
    if m.remotes:  # HINT #290  # line 739
        printo("Remote duplicates:   %s" % ", ".join(m.remotes))  # HINT #290  # line 739
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 740
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 741
    m.loadBranch(current)  # line 742
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 743
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 744
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 744
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 745
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of unicode symbols for changed vs. unchanged  # line 750
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 754
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 755
        payload = 0  # type: int  # line 756
        overhead = 0  # type: int  # line 756
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 757
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 758
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 759
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 759
                else:  # line 760
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 760
        pl_amount = float(payload) / MEBI  # type: float  # line 761
        oh_amount = float(overhead) / MEBI  # type: float  # line 761
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 763
        original = 0  # type: int  # compute occupied storage per branch  # line 764
        updates = []  # type: _coconut.typing.Sequence[int]  # compute occupied storage per branch  # line 764
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 765
            m.loadCommit(m.branch, commit_)  # line 766
            for pinfo in m.paths.values():  # line 767
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 767
            updates.append(len(m.paths))  # number of additions or removals TODO count moves as 1 instead of 2  # line 768
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 769
        printo("  %s b%d%s @%s (%s%s) with %d commits (median %d each), using %.2f MiB (+%.3f%% SOS overhead%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), Fore.RESET, len(m.commits), median(updates) if updates else 0.0, pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 770
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 783
        printo(Fore.GREEN + "Tracked" + Fore.RESET + " file patterns:")  # TODO #261 print matching untracking patterns side-by-side?  # line 784
        printo(ajoin(Fore.GREEN + "  | " + Fore.RESET, m.branches[m.branch].tracked, "\n"))  # line 785
        printo(Fore.RED + "Untracked" + Fore.RESET + " file patterns:")  # line 786
        printo(ajoin(Fore.RED + "  | " + Fore.RESET, m.branches[m.branch].untracked, "\n"))  # line 787

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 789
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 796
    assert not (check and commit)  # line 797
    m = Metadata()  # type: Metadata  # line 798
    remotes = m._extractRemotesFromArguments(options)  # type: List[str]  # line 799
    force = '--force' in options  # type: bool  # line 800
    strict = '--strict' in options or m.strict  # type: bool  # line 801
    if argument is not None:  # line 802
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 803
        if branch is None:  # line 804
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 804
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 805
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 806

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 809
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 810
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 811
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options, remotes=remotes)  # line 812
    if check and modified(changed) and not force:  # line 818
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 819
        Exit("File tree contains changes. Use --force to proceed")  # line 820
    elif commit:  # line 821
        if not modified(changed) and not force:  # line 822
            Exit("Nothing to commit")  # line 822
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 823
        if msg:  # line 824
            printo(msg)  # line 824

    if argument is not None:  # branch/revision specified  # line 826
        m.loadBranch(branch)  # knows commits of target branch  # line 827
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 828
        revision = m.correctNegativeIndexing(revision)  # line 829
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 830
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 831

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 833
    ''' Continue work on another branch, replacing file tree changes. '''  # line 834
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # --force continuation to delay check to this function  # line 835
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 836

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data (tracking patterns only)  # line 839
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 840
    else:  # full file switch  # line 841
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 842
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 843

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 850
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 851
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 852
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 853
                rms.append(a)  # line 853
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 854
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 854
        if modified(changed) and not force:  # line 855
            m.listChanges(changed, cwd)  # line 855
            Exit("File tree contains changes. Use --force to proceed")  # line 855
        if verbose:  # line 856
            info(MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 856
        if not modified(todos):  # line 857
            info("No changes to current file tree")  # line 858
        else:  # integration required  # line 859
            for path, pinfo in todos.deletions.items():  # line 860
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 861
                printo("ADD " + path, color=Fore.GREEN)  # line 862
            for path, pinfo in todos.additions.items():  # line 863
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 864
                printo("DEL " + path, color=Fore.RED)  # line 865
            for path, pinfo in todos.modifications.items():  # line 866
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 867
                printo("MOD " + path, color=Fore.YELLOW)  # line 868
    m.branch = branch  # line 869
    m.saveBranches(m._extractRemotesFromArguments(options))  # store switched path info  # line 870
    info(MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 871

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 873
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 877
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 878
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 879
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 880
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 881
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 882
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 883
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 884
    if verbose:  # line 885
        info(MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 885

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 888
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 889
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 890
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 891
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 896
        if trackingUnion != trackingPatterns:  # nothing added  # line 897
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 898
        else:  # line 899
            info("Nothing to update")  # but write back updated branch info below  # line 900
    else:  # integration required  # line 901
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 902
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 902
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 902
        if changed.deletions.items():  # line 903
            printo("Additions:")  # line 903
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 904
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 905
            if add_all is None and mrg == MergeOperation.ASK:  # line 906
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 907
                if selection in "ao":  # line 908
                    add_all = "y" if selection == "a" else "n"  # line 908
                    selection = add_all  # line 908
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 909
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 909
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path, color=Fore.GREEN)  # TODO #268 document merge/update output, e.g. (A) as "selected not to add by user choice"  # line 910
        if changed.additions.items():  # line 911
            printo("Deletions:")  # line 911
        for path, pinfo in changed.additions.items():  # line 912
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 913
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 913
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 914
            if del_all is None and mrg == MergeOperation.ASK:  # line 915
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 916
                if selection in "ao":  # line 917
                    del_all = "y" if selection == "a" else "n"  # line 917
                    selection = del_all  # line 917
            if "y" in (del_all, selection):  # line 918
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 918
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path, color=Fore.RED)  # not contained in other branch, but maybe kept  # line 919
        if changed.modifications.items():  # line 920
            printo("Modifications:")  # line 920
        for path, pinfo in changed.modifications.items():  # line 921
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 922
            binary = not m.isTextType(path)  # type: bool  # line 923
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 924
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 925
                printo(("MOD " if not binary else "BIN ") + path, color=Fore.YELLOW)  # TODO print mtime, size differences?  # line 926
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 927
            if op == "t":  # line 928
                printo("THR " + path, color=Fore.MAGENTA)  # blockwise copy of contents  # line 929
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 929
            elif op == "m":  # line 930
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 931
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 931
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # slurp versioned file  # line 932
                if current == file and verbose:  # line 933
                    info("No difference to versioned file")  # line 933
                elif file is not None:  # if None, error message was already logged  # line 934
                    merged = None  # type: bytes  # line 935
                    nl = None  # type: bytes  # line 935
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 936
                    if merged != into:  # line 937
                        printo("MRG " + path, color=Fore.CYAN)  # line 938
                        with open(encode(into), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 939
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 939
                    elif verbose:  # TODO but update timestamp?  # line 940
                        info("No change")  # TODO but update timestamp?  # line 940
            else:  # mine or wrong input  # line 941
                printo("MNE " + path, color=Fore.CYAN)  # nothing to do! same as skip  # line 942
    info(MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 943
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 944
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 945
    m.saveBranches(m._extractRemotesFromArguments(options))  # line 946

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 948
    ''' Remove a branch entirely. '''  # line 949
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 950
    if len(m.branches) == 1:  # line 951
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 951
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 952
    if branch is None or branch not in m.branches:  # line 953
        Exit("Cannot delete unknown branch %r" % branch)  # line 953
    if verbose:  # line 954
        info(MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 954
    binfo = m.removeBranch(branch, options)  # need to keep a reference to removed entry for output below  # line 955
    info(MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 956

def add(relPaths: '_coconut.typing.Sequence[str]', patterns: '_coconut.typing.Sequence[str]', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 958
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 959
    force = '--force' in options  # type: bool  # line 960
    m = Metadata()  # type: Metadata  # line 961
    if not (m.track or m.picky):  # line 962
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 963
    knownpatterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 964
    for relPath, pattern in zip(relPaths, patterns):  # line 965
        if pattern in knownpatterns:  # line 966
            Exit("Pattern '%s' already tracked" % pattern)  # line 967
        if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 968
            Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 969
        if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 970
            Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 971
        knownpatterns.append(pattern)  # line 972
    m.saveBranches(m._extractRemotesFromArguments(options))  # line 973
    info(MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # line 974

def remove(relPaths: '_coconut.typing.Sequence[str]', patterns: '_coconut.typing.Sequence[str]', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 976
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 977
    m = Metadata()  # type: Metadata  # line 978
    if not (m.track or m.picky):  # line 979
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' to start repository in tracking or picky mode")  # line 980
    knownpatterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 981
    for relPath, pattern in zip(relPaths, patterns):  # line 982
        if pattern not in knownpatterns:  # line 983
            suggestion = _coconut.set()  # type: Set[str]  # line 984
            for pat in knownpatterns:  # line 985
                if fnmatch.fnmatch(pattern, pat):  # line 985
                    suggestion.add(pat)  # line 985
            if suggestion:  # line 986
                printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # line 986
            Exit("Tracked pattern '%s' not found" % pattern)  # line 987
    knownpatterns.remove(pattern)  # line 988
    m.saveBranches(m._extractRemotesFromArguments(options))  # line 989
    info(MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 990

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 992
    ''' List specified directory, augmenting with repository metadata. '''  # line 993
    m = Metadata()  # type: Metadata  # line 994
    folder = (os.getcwd() if folder is None else folder)  # line 995
    if '--all' in options or '-a' in options:  # always start at SOS repo root with --all  # line 996
        folder = m.root  # always start at SOS repo root with --all  # line 996
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 997
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 998
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 999
    if verbose:  # line 1000
        info(MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 1000
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 1001
    if relPath.startswith(os.pardir):  # line 1002
        Exit("Cannot list contents of folder outside offline repository")  # line 1002
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 1003
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 1004
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 1005
        if len(m.tags) > 0:  # line 1006
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 1006
        return  # line 1007
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 1008
        if not recursive:  # avoid recursion  # line 1009
            dirnames.clear()  # avoid recursion  # line 1009
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 1010
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 1011

        folder = decode(dirpath)  # line 1013
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 1014
        if patterns:  # line 1015
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 1016
            if out:  # line 1017
                printo("DIR %s\n" % relPath + out)  # line 1017
            continue  # with next folder  # line 1018
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 1019
        if len(files) > 0:  # line 1020
            printo("DIR %s" % relPath)  # line 1020
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 1021
            ignore = None  # type: _coconut.typing.Optional[str]  # line 1022
            for ig in m.c.ignores:  # remember first match  # line 1023
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 1023
                    ignore = ig  # remember first match  # line 1023
                    break  # remember first match  # line 1023
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 1024
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 1024
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 1024
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 1024
                        break  # found a white list entry for ignored file, undo ignoring it  # line 1024
            matches = []  # type: List[str]  # line 1025
            if not ignore:  # line 1026
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 1027
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 1028
                        matches.append(os.path.basename(pattern))  # line 1028
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 1029
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 1030

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 1032
    ''' List previous commits on current branch. '''  # line 1033
    changes_ = "--changes" in options  # type: bool  # line 1034
    diff_ = "--diff" in options  # type: bool  # line 1035
    m = Metadata()  # type: Metadata  # line 1036
    m.loadBranch(m.branch)  # knows commit history  # line 1037
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 1038
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 1039
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Offline commit history of branch %r" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 1040
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 1041
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 1042
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 1043
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 1044
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 1045
    commit = None  # type: CommitInfo  # used for reading parent branch information  # line 1045
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1046
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 1047
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 1048
    for no in range(maxi + 1):  # line 1049
        if indicator:  # line 1050
            printo("  %%s %%0%dd" % digits % ((lambda _coconut_none_coalesce_item: " " if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(indicator.getIndicator()), no), nl="\r")  # line 1050
        if no in m.commits:  # line 1051
            commit = m.commits[no]  # line 1051
        else:  # line 1052
            if n.branch != n.getParentBranch(m.branch, no):  # line 1053
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 1053
            commit = n.commits[no]  # line 1054
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 1055
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 1056
        if "--all" in options or no >= lastno:  # line 1057
            if no >= lastno:  # line 1058
                indicator = None  # line 1058
            _add = news - olds  # type: FrozenSet[str]  # line 1059
            _del = olds - news  # type: FrozenSet[str]  # line 1060
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 1062
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 1064
            printo("  %s r%s @%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%sT%s%02d) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, Fore.RESET, len(_add), Fore.RED, Fore.RESET, len(_del), Fore.YELLOW, PLUSMINUS_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(_mod), Fore.CYAN, Fore.RESET, _txt, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 1065
            if changes_:  # line 1066
                m.listChanges(ChangeSet({a: None for a in _add}, {d: None for d in _del}, {m: None for m in _mod}, {}), root=cwd if '--relative' in options else None)  # TODO why using None here? to avoid stating files for performance reasons?  # line 1077
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 1078
                pass  #  _diff(m, changes)  # needs from revision diff  # line 1078
        olds = news  # replaces olds for next revision compare  # line 1079
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 1080

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 1082
    ''' Exported entire repository as archive for easy transfer. '''  # line 1083
    if verbose:  # line 1084
        info(MARKER + "Dumping repository to archive...")  # line 1084
    m = Metadata()  # type: Metadata  # to load the configuration  # line 1085
    progress = '--progress' in options  # type: bool  # line 1086
    delta = '--full' not in options  # type: bool  # line 1087
    skipBackup = '--skip-backup' in options  # type: bool  # line 1088
    import functools  # line 1089
    import locale  # line 1089
    import warnings  # line 1089
    import zipfile  # line 1089
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 1090
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 1090
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 1090
    except:  # line 1091
        compression = zipfile.ZIP_STORED  # line 1091

    if ("" if argument is None else argument) == "":  # line 1093
        Exit("Argument missing (target filename)")  # line 1093
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 1094
    entries = []  # type: List[str]  # line 1095
    if os.path.exists(encode(argument)) and not skipBackup:  # line 1096
        try:  # line 1097
            if verbose:  # line 1098
                info("Creating backup...")  # line 1098
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 1099
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 1100
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 1100
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 1100
        except Exception as E:  # line 1101
            Exit("Error creating backup copy before dumping. Please resolve and retry.", excp=E)  # line 1101
    if verbose:  # line 1102
        info("Dumping revisions...")  # line 1102
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1103
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1103
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1104
        _zip.debug = 0  # suppress debugging output  # line 1105
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1106
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1107
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1108
        totalsize = 0  # type: int  # line 1109
        start_time = time.time()  # type: float  # line 1110
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1111
            dirpath = decode(dirpath)  # line 1112
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1113
                continue  # don't backup backups  # line 1113
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1114
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1115
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1116
            for filename in filenames:  # line 1117
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1118
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1119
                totalsize += os.stat(encode(abspath)).st_size  # line 1120
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1121
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1122
                    continue  # don't backup backups  # line 1122
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1123
                    if show:  # line 1124
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1124
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1125
        if delta:  # line 1126
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1126
    info("\r" + pure.ljust(MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1127

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1129
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1130
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1131
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1132
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1132
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1133
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1134
    if maxi is None:  # line 1135
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1135
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1136
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1139
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1141
    while files:  # line 1142
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1143
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1144
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1146
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1146
    tracked = None  # type: bool  # line 1147
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1147
    tracked, commitArgs = vcsCommits[cmd]  # line 1147
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1148
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1150
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1150
    if tracked:  # line 1151
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1151
    m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed to underlying  # line 1152
    m.saveBranches()  # line 1153

def config(arguments: 'List[_coconut.typing.Optional[str]]', options: 'List[str]'=[]):  # line 1155
    ''' Configure command: manage configuration settings. '''  # line 1156
    command = None  # type: str  # line 1157
    key = None  # type: str  # line 1157
    value = None  # type: str  # line 1157
    v = None  # type: str  # line 1157
    command, key, value = (arguments + [None] * 2)[:3]  # line 1158
    if command is None:  # line 1159
        usage.usage("help", verbose=True)  # line 1159
    if command not in ("set", "unset", "show", "list", "add", "rm"):  # line 1160
        Exit("Unknown config command %r" % command)  # line 1160
    local = "--local" in options  # type: bool  # otherwise user-global by default  # line 1161
    m = Metadata()  # type: Metadata  # loads nested configuration (local - global - defaults)  # line 1162
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # will only modify the selected parameter set  # line 1163
    location = "local" if local else "global"  # type: str  # line 1164
    if command == "set":  # line 1165
        if None in (key, value):  # line 1166
            Exit("Key or value not specified")  # line 1166
        if key not in ((([] if local else ONLY_GLOBAL_FLAGS) + CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1167
            Exit("Unsupported key for %s configuration %r" % (location, key))  # TODO move defaultbranch to configurable_texts?  # line 1167
        if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1168
            Exit("Cannot set flag to %r. Try 'on' or 'off' instead" % value.lower())  # line 1168
        c[key] = value.lower() in TRUTH_VALUES if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1169
    elif command == "unset":  # line 1170
        if key is None:  # line 1171
            Exit("No key specified")  # line 1171
        if key not in c.keys(with_nested=False):  # line 1172
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, location))  # line 1173
        del c[key]  # line 1174
    elif command == "add":  # TODO copy list from defaults if not local/global  # line 1175
        if None in (key, value):  # line 1176
            Exit("Key or value not specified")  # line 1176
        if key not in CONFIGURABLE_LISTS:  # line 1177
            Exit("Unsupported key %r for list addition" % key)  # line 1177
        if key not in c.keys():  # prepare empty list, or copy from underlying, add new value below TODO also allow one more level of underlying?  # line 1178
            c[key] = [_ for _ in c.__defaults[key]] if key in c.__defaults[key] else []  # prepare empty list, or copy from underlying, add new value below TODO also allow one more level of underlying?  # line 1178
        elif value in c[key]:  # line 1179
            Exit("Value already contained, nothing to do")  # line 1179
        if ";" not in value:  # line 1180
            c[key].append(removePath(key, value.strip()))  # line 1180
        else:  # line 1181
            c[key].extend([removePath(key, v) for v in safeSplit(value, ";")])  # line 1181
    elif command == "rm":  # line 1182
        if None in (key, value):  # line 1183
            Exit("Key or value not specified")  # line 1183
        if key not in c.keys(with_nested=False):  # line 1184
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, location))  # line 1185
        if value not in c[key]:  # line 1186
            Exit("Unknown value %r" % value)  # line 1186
        c[key].remove(value)  # line 1187
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1188
            del c[key]  # remove local entry, to fallback to global  # line 1188
    else:  # Show or list  # line 1189
        if key == "ints":  # list valid configuration items  # line 1190
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1190
        elif key == "flags":  # line 1191
            printo(", ".join(ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS))  # line 1191
        elif key == "lists":  # line 1192
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1192
        elif key == "texts":  # line 1193
            printo(", ".join([_ for _ in defaults.keys() if _ not in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS + CONFIGURABLE_INTS + CONFIGURABLE_LISTS)]))  # line 1193
        else:  # no key: list all  # line 1194
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1195
            c = m.c  # always use full configuration chain  # line 1196
            try:  # attempt single key  # line 1197
                assert key is not None  # force exception if no key specified  # line 1198
                c[key]  # force exception if no key specified  # line 1198
                l = key in c.keys(with_nested=False)  # type: bool  # line 1199
                g = key in c.__defaults.keys(with_nested=False)  # type: bool  # line 1199
                printo(key.rjust(20), color=Fore.WHITE, nl="")  # line 1200
                printo(" " + (out[3] if not (l or g) else (out[1] if l else out[2])) + " ", color=Fore.CYAN, nl="")  # line 1201
                printo(repr(c[key]))  # line 1202
            except:  # normal value listing  # line 1203
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # copy-by-value  # line 1204
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1205
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1206
                for k, vt in sorted(vals.items()):  # line 1207
                    printo(k.rjust(20), color=Fore.WHITE, nl="")  # line 1208
                    printo(" " + out[vt[1]] + " ", color=Fore.CYAN, nl="")  # line 1209
                    printo(vt[0])  # line 1210
                if len(c.keys()) == 0:  # line 1211
                    info("No local configuration stored.")  # line 1211
                if len(c.__defaults.keys()) == 0:  # line 1212
                    info("No global configuration stored.")  # line 1212
        return  # in case of list, no need to store anything  # line 1213
    if local:  # saves changes of repoConfig  # line 1214
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1214
        m.saveBranches(m._extractRemotesFromArguments(options))  # saves changes of repoConfig  # line 1214
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1214
    else:  # global config  # line 1215
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1216
        if f is None:  # line 1217
            Exit("Error saving user configuration: %r" % h)  # line 1217

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1219
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1222
    if verbose:  # line 1223
        info(MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1223
    force = '--force' in options  # type: bool  # line 1224
    soft = '--soft' in options  # type: bool  # line 1225
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1226
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1226
    m = Metadata()  # type: Metadata  # line 1227
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1228
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1229
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1230
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1231
    if not matching and not force:  # line 1232
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1232
    if not (m.track or m.picky):  # line 1233
        Exit("Repository is in simple mode. Use basic file operations to modify files, then execute 'sos commit' to version any changes")  # line 1233
    if pattern not in patterns:  # list potential alternatives and exit  # line 1234
        for tracked in (t for t in patterns if t[:t.rindex(SLASH)] == relPath):  # for all patterns of the same source folder HINT was os.path.dirpath before  # line 1235
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1236
            if alternative:  # line 1237
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1237
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: "if not (force or soft):""  # line 1238
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1239
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1240
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1241
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1245
#  oldTokens:GlobBlock[]?; newToken:GlobBlock[]?  # TODO remove optional?, only here to satisfy mypy
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1247
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1248
    if len({st[1] for st in matches}) != len(matches):  # line 1249
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1249
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1250
    if os.path.exists(encode(newRelPath)):  # line 1251
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1252
        if exists and not (force or soft):  # line 1253
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1253
    else:  # line 1254
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1254
    if not soft:  # perform actual renaming  # line 1255
        for (source, target) in matches:  # line 1256
            try:  # line 1257
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1257
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1258
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1258
    patterns[patterns.index(pattern)] = newPattern  # line 1259
    m.saveBranches(m._extractRemotesFromArguments(options))  # line 1260

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1262
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1263
    debug("Parsing command-line arguments...")  # line 1264
    root = os.getcwd()  # line 1265
    try:  # line 1266
        onlys, excps, remotes, noremotes = parseArgumentOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1267
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1268
        arguments = [c.strip() for c in sys.argv[2:] if not ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # line 1269
        options = [c.strip() for c in sys.argv[2:] if ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # options *with* arguments have to be parsed directly from sys.argv inside using functions  # line 1270
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1271
        if command[:1] in "amr":  # line 1272
            try:  # line 1273
                relPaths, patterns = unzip([relativize(root, os.path.join(cwd, argument)) for argument in ((["."] if arguments is None else arguments))])  # line 1273
            except:  # line 1274
                command = "ls"  # convert command into ls --patterns  # line 1275
                arguments[0] = None  # convert command into ls --patterns  # line 1275
                options.extend(["--patterns", "--all"])  # convert command into ls --patterns  # line 1275
# Exit("Need one or more file patterns as argument (escape them according to your shell)")
        if command[:1] == "m":  # line 1277
            if len(arguments) < 2:  # line 1278
                Exit("Need a second file pattern argument as target for move command")  # line 1278
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1279
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1280
        if command == "raise":  # line 1281
            raise Exception("provoked exception")  # line 1281
        elif command[:1] == "a":  # e.g. addnot  # line 1282
            add(relPaths, patterns, options, negative="n" in command)  # e.g. addnot  # line 1282
        elif command[:1] == "b":  # line 1283
            branch(arguments[0], arguments[1], options)  # line 1283
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1284
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1284
        elif command[:2] == "ci":  # line 1285
            commit(arguments[0], options, onlys, excps)  # line 1285
        elif command[:3] == "com":  # line 1286
            commit(arguments[0], options, onlys, excps)  # line 1286
        elif command[:3] == 'con':  # line 1287
            config(arguments, options)  # line 1287
        elif command[:2] == "de":  # line 1288
            destroy((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1288
        elif command[:2] == "di":  # TODO no consistent handling of single dash/characters argument-options  # line 1289
            diff((lambda _coconut_none_coalesce_item: "/" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[2 if arguments[0] == '-n' else 0]), options, onlys, excps)  # TODO no consistent handling of single dash/characters argument-options  # line 1289
        elif command[:2] == "du":  # line 1290
            dump((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1290
        elif command[:1] == "h":  # line 1291
            usage.usage(arguments[0], verbose=verbose)  # line 1291
        elif command[:2] == "lo":  # line 1292
            log(options, cwd)  # line 1292
        elif command[:2] == "li":  # line 1293
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1293
        elif command[:2] == "ls":  # line 1294
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1294
        elif command[:1] == "m":  # e.g. mvnot  # line 1295
            move(relPaths[0], patterns[0], newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1295
        elif command[:2] == "of":  # line 1296
            offline(arguments[0], arguments[1], options, remotes)  # line 1296
        elif command[:2] == "on":  # line 1297
            online(options)  # line 1297
        elif command[:1] == "p":  # line 1298
            publish(arguments[0], cmd, options, onlys, excps)  # line 1298
        elif command[:1] == "r":  # e.g. rmnot  # line 1299
            remove(relPaths, patterns, options, negative="n" in command)  # e.g. rmnot  # line 1299
        elif command[:2] == "st":  # line 1300
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1300
        elif command[:2] == "sw":  # line 1301
            switch((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps, cwd)  # line 1301
        elif command[:1] == "u":  # line 1302
            update((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps)  # line 1302
        elif command[:1] == "v":  # line 1303
            usage.usage(arguments[0], version=True)  # line 1303
        else:  # line 1304
            Exit("Unknown command '%s'" % command)  # line 1304
        Exit(code=0)  # regular exit  # line 1305
    except (Exception, RuntimeError) as E:  # line 1306
        Exit("An internal error occurred in SOS\nPlease report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', and what you were doing.", excp=E)  # line 1307

def main():  # line 1309
    global debug, info, warn, error  # to modify logger  # line 1310
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1311
    _log = Logger(logging.getLogger(__name__))  # line 1312
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1312
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1313
        sys.argv.remove(option)  # clean up program arguments  # line 1313
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1314
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1314
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1315
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (=still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1316
    debug("Detected SOS root folder: %s" % (("-" if root is None else root)))  # line 1317
    debug("Detected VCS root folder: %s" % (("-" if vcs is None else vcs)))  # line 1318
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1319
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1320
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv") or force_sos and (root is not None or (("" if command is None else command))[:3] == "con"):  # in offline mode or just going offline  # line 1321
        cwd = os.getcwd()  # line 1323
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1324
        parse(vcs, cwd, cmd)  # line 1325
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1326
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1327
        import subprocess  # only required in this section  # line 1328
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1329
        inp = ""  # type: str  # line 1330
        while True:  # line 1331
            so, se = process.communicate(input=inp)  # line 1332
            if process.returncode is not None:  # line 1333
                break  # line 1333
            inp = sys.stdin.read()  # line 1334
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit to underlying VCS - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1335
            if root is None:  # line 1336
                Exit("Cannot determine SOS root folder: Not working offline, thus unable to mark offline repository as synchronized")  # line 1336
            m = Metadata(root)  # type: Metadata  # line 1337
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1338
            m.saveBranches()  # line 1339
    else:  # line 1340
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1340


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: List[None]  # this is a trick allowing to modify the module-level flags from the test suite  # line 1344
force_vcs = [None] if '--vcs' in sys.argv else []  # type: List[None]  # line 1345
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1346

_log = Logger(logging.getLogger(__name__))  # line 1348
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1348

if __name__ == '__main__':  # line 1350
    main()  # line 1350
