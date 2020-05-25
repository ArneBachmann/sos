#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x8f886d11

# Compiled with Coconut version 1.4.3 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get("__coconut__")
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules["__coconut__"]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import *
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_back_pipe, _coconut_star_pipe, _coconut_back_star_pipe, _coconut_dubstar_pipe, _coconut_back_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert, _coconut_mark_as_match
_coconut_sys.path.pop(0)

# Compiled Coconut: -----------------------------------------------------------

# Copyright (c) 2017-2020  Arne Bachmann
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
except:  # TODO this is here to avoid import error when setup.py is called but actually needs to install its dependencies first  # line 15
    pass  # TODO this is here to avoid import error when setup.py is called but actually needs to install its dependencies first  # line 15


# Lazy module import for quicker tool startup
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
        if len(changed.modifications) > 0:  # line 92
            printo(ajoin("MOD ", [relp(m, root) + (" <binary>" if not _.isTextType(os.path.basename(m)) else "") + ("" if commitTime is None else (" <older than previously committed>" if pi.mtime < _.paths[m].mtime else "")) + ((" [%s%s %s%s]" % (pure.signedNumber(pi.size - _.paths[m].size), siSize(pi.size - _.paths[m].size), pure.signedNumber(pi.mtime - _.paths[m].mtime), pure.timeString(pi.mtime - _.paths[m].mtime)) if verbose else "") if pi is not None else "") for (m, pi) in sorted(changed.modifications.items())], "\n"), color=Fore.YELLOW)  # line 92
        if len(realdeletions) > 0:  # line 93
            printo(ajoin("DEL ", sorted([relp(p, root) for p in realdeletions.keys()]), "\n"), color=Fore.RED)  # line 93
        if len(realadditions) > 0:  # line 94
            printo(ajoin("ADD ", sorted(["%s  (%s)" % (relp(p, root), pure.siSize(pinfo.size) if pinfo is not None else "-") for p, pinfo in realadditions.items()]), "\n"), color=Fore.GREEN)  # line 94
        printo("+%d (%s)  -%d  %s%d (%s)  %s%d" % (len(realadditions), (pure.siSize)(sum((pinfo.size for pinfo in realadditions.values() if pinfo))), len(realdeletions), CHANGED_SYMBOL if _.c.useUnicodeFont else "~", len(changed.modifications), (pure.siSize)(sum((minfo.size for minfo in changed.modifications.values() if minfo))), MOVED_SYMBOL if _.c.useUnicodeFont else "#", len(changed.moves)), color=Fore.WHITE)  # line 95

    def loadBranches(_, offline: 'bool'=False, remotes: 'List[str]'=[]):  # line 97
        ''' Load list of branches and current branch info from metadata file.
        offline: if True, avoid messages
        remotes: manually provided remotes when using "sos offline --remote"
    '''  # line 101
        try:  # fails if not yet created (on initial branch/commit)  # line 102
#      branches:List[List]  # deserialized JSON is only list, while the real type of _.branches is a dict number -> BranchInfo (Coconut data type/named tuple)
            with codecs.open(encode(os.path.join(_.root, metaFolder, metaFile)), "r", encoding=UTF8) as fd:  # line 104
                repo, branches, config = json.load(fd)  # line 105
            _.tags = repo["tags"]  # list of commit messages to treat as globally unique tags  # line 106
            _.branch = repo["branch"]  # current branch integer  # line 107
            _.track, _.picky, _.strict, _.compress, _.version, _.format, _.remotes, remote = [repo.get(r, None) for r in ["track", "picky", "strict", "compress", "version", "format", "remotes", "remote"]]  # line 108
            if remote:  # line 109
                Exit("Cannot access remote SOS repository for local operation. You're attempting to access a backup copy. Consult manual to restore this backup for normal operation")  # line 109
            upgraded = []  # type: List[str]  # line 110
            if _.version is None:  # line 111
                _.version = "0 - pre-1.2"  # line 112
                upgraded.append("pre-1.2")  # line 113
            if len(branches[0]) < 6:  # For older versions, see https://pypi.python.org/simple/sos-vcs/  # line 114
                branches[:] = [branch + [[]] * (6 - len(branch)) for branch in branches]  # add untracking information, if missing  # line 115
                upgraded.append("2018.1210.3028")  # line 116
            if _.format is None:  # must be before 1.3.5+  # line 117
                _.format = 1  # marker for first metadata file format  # line 118
                branches[:] = [branch + [None] * (8 - len(branch)) for branch in branches]  # adds empty branching point information (branch/revision)  # line 119
                upgraded.append("1.3.5")  # line 120
            _.branches = {i.number: i for i in (BranchInfo(*item) for item in branches)}  # re-create type info  # line 121
            _.repoConf = config  # local configuration stored with repository, not in user-wide configuration  # line 122
            if _.format == 1 or _.remotes is None:  # before remotes  # line 123
                _.format = METADATA_FORMAT  # line 124
                _.remotes = []  # default is no remotes, and this conversion can never happen at "sos offline"  # line 125
                upgraded.append("1.7.0")  # remote URLs introduced  # line 126
            if upgraded:  # line 127
                for upgrade in upgraded:  # line 128
                    printo("WARNING  Upgraded repository metadata to match SOS version %r" % upgrade, color=Fore.YELLOW)  # line 128
                warn("To revert the metadata upgrade%s, restore %s/%s from %s/%s NOW" % ("s" if len(upgraded) > 1 else "", metaFolder, metaFile, metaFolder, metaBack))  # line 129
                _.saveBranches(_.remotes)  # line 130
        except Exception as E:  # if not found, create metadata folder with default values  # line 131
            _.branches = {}  # line 132
            _.track, _.picky, _.strict, _.compress, _.version, _.remotes, _.format = [defaults[k] for k in ["track", "picky", "strict", "compress"]] + [version.__version__, remotes, METADATA_FORMAT]  # line 133
            (debug if offline else warn)("Couldn't read branches metadata: %r" % E)  # hide warning only when going offline  # line 134

    def _saveBranches(_, remote: '_coconut.typing.Optional[str]', data: 'Dikt[str, Any]'):  # line 136
        ''' Subfunction to save branches to a local or remote offline repository location. '''  # line 137
        tryOrIgnore(lambda: shutil.copy2(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), encode(os.path.join((_.root if remote is None else remote), metaFolder, metaBack))))  # backup  # line 138
        try:  # line 139
            with codecs.open(encode(os.path.join((_.root if remote is None else remote), metaFolder, metaFile)), "w", encoding=UTF8) as fd:  # line 139
                json.dump((data, list(_.branches.values()), _.repoConf), fd, ensure_ascii=False)  # stores using unicode codepoints (instead of ascii encoding), the file descriptor knows how to encode them  # line 140
        except Exception as E:  # line 141
            debug("Error saving branches%s" % ((" to remote path " + remote) if remote else ""))  # line 141

    def saveBranches(_, remotes: 'List[str]'=[], also: 'Dict[str, Any]'={}):  # line 143
        ''' Save list of branches and current branch info to metadata file. '''  # line 144
        store = {"tags": _.tags, "branch": _.branch, "track": _.track, "picky": _.picky, "strict": _.strict, "compress": _.compress, "version": _.version, "format": METADATA_FORMAT, "remotes": _.remotes, "remote": False}  # type: Dict[str, Any]  # dictionary of repository settings (while _.repoConf stores user settings)  # line 145
        store.update(also)  # allows overriding certain values at certain points in time  # line 151
        for remote in [None] + remotes:  # line 152
            _._saveBranches(remote, store)  # mark remote copies as read-only, add repository master  # line 153
            store.update({"remote": True, "origin": _.root})  # mark remote copies as read-only, add repository master  # line 153

    def _extractRemotesFromArguments(_, options: 'List[str]') -> 'List[str]':  # line 155
        ''' Common behavior to parse and extract the remotes options from command line-arguments. '''  # line 156
        _a = None  # type: Any  # line 157
        remotes = None  # type: List[str]  # line 157
        noremotes = None  # type: List[str]  # line 157
        _a, _a, remotes, noremotes = parseArgumentOptions("", options)  # re-parse options for the --(only-)remotes and --exlude-remotes options  # line 158
        return [] if "--no-remotes" in options or "--no-remote" in options else list(set(remotes if remotes else _.remotes) - set(noremotes))  # line 159

    def getRevisionByName(_, name: '_coconut.typing.Optional[str]') -> '_coconut.typing.Optional[int]':  # line 161
        ''' Convenience accessor for named revisions (using commit message as tag name by convention). '''  # line 162
        if (("" if name is None else name)) == "":  # line 163
            return -1  # line 163
        try:  # attempt to parse integer string  # line 164
            return int(name)  # attempt to parse integer string  # line 164
        except ValueError:  # line 165
            pass  # line 165
        found = [number for number, commit in _.commits.items() if name == commit.message]  # find any revision by commit message (usually used for tags)  # HINT allows finding any message, not only tagged ones  # line 166
        return found[0] if found else None  # line 167

    def getBranchByName(_, name: 'str') -> '_coconut.typing.Optional[int]':  # line 169
        ''' Convenience accessor for named branches.
        returns: branch index 0.. or None if not found
    '''  # line 172
        if name == "":  # current  # line 173
            return _.branch  # current  # line 173
        try:  # attempt to parse integer string  # line 174
            return int(name)  # attempt to parse integer string  # line 174
        except ValueError:  # line 175
            pass  # line 175
        found = [number for number, branch in _.branches.items() if name == branch.name]  # line 176
        return found[0] if found else None  # line 177

    def loadBranch(_, branch: 'int'):  # line 179
        ''' Load all commit information from a branch meta data file. '''  # line 180
        with codecs.open(encode(branchFolder(branch, file=metaFile)), "r", encoding=UTF8) as fd:  # line 181
            commits = json.load(fd)  # type: List[List[Any]]  # list of CommitInfo that needs to be unmarshalled into value types  # line 182
        _.commits = {i.number: i for i in (CommitInfo(*item) for item in commits)}  # re-create type info  # line 183
        _.branch = branch  # line 184

    def saveBranch(_, branch: 'int', options: 'List[str]'=[]):  # line 186
        ''' Save all commits to a branch meta data file. '''  # line 187
        remotes = _._extractRemotesFromArguments(options)  # type: List[str]  # line 188
        for remote in [None] + remotes:  # line 189
            tryOrIgnore(lambda _=None: shutil.copy2(encode(branchFolder(branch, file=metaFile, base=remote)), encode(branchFolder(branch, file=metaBack, base=remote))))  # backup  # line 190
            try:  # line 191
                with codecs.open(encode(branchFolder(branch, file=metaFile, base=remote)), "w", encoding=UTF8) as fd:  # line 191
                    json.dump(list(_.commits.values()), fd, ensure_ascii=False)  # line 192
            except Exception as E:  # line 193
                debug("Error saving branch%s" % ((" to remote path " + remote) if remote else ""))  # line 193

    def duplicateBranch(_, branch: 'int', options: 'List[str]'=[], name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, full: 'bool'=True):  # line 195
        ''' Create branch from an existing branch/revision.
        In case of full branching, copy all revisions, otherwise create only reference to originating branch/revision.
        branch: new target branch number (must not exist yet)
        name: optional name of new branch (currently always set by caller)
        initialMessage: message for commit if not last and file tree modified
        full: always create full branch copy, don't use a parent reference
        _.branch: current branch
    '''  # line 203
        remotes = _._extractRemotesFromArguments(options)  # type: List[str]  # line 204
        if verbose:  # line 205
            info("Duplicating branch '%s' to '%s'..." % ((lambda _coconut_none_coalesce_item: ("b%d" % _.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name), (("b%d" % branch if name is None else name))))  # line 205
        now = int(time.time() * 1000)  # type: int  # line 206
        _.loadBranch(_.branch)  # load commits for current (originating) branch  # line 207
        revision = max(_.commits) if _.commits else 0  # type: int  # line 208
        _.commits.clear()  # line 209
        newBranch = dataCopy(BranchInfo, _.branches[_.branch], number=branch, ctime=now, name=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if name is None else name), tracked=[t for t in _.branches[_.branch].tracked], untracked=[u for u in _.branches[_.branch].untracked], parent=None if full else _.branch, revision=None if full else revision)  # type: BranchInfo  # line 210
        for remote in [None] + remotes:  # line 215
            tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)) if full else branchFolder(branch, base=(_.root if remote is None else remote)))), lambda e: error("Duplicating remote branch folder %r" % remote))  # line 216
        if full:  # not fast branching via reference - copy all current files to new branch  # line 217
            _.computeSequentialPathSet(_.branch, revision)  # full set of files in latest revision in _.paths  # line 218
            for path, pinfo in _.paths.items():  # copy into initial branch revision  # line 219
                _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # copy into initial branch revision  # line 219
            _.commits[0] = CommitInfo(number=0, ctime=now, message=("Branched from '%s'" % ((lambda _coconut_none_coalesce_item: "b%d" % _.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.branches[_.branch].name)) if initialMessage is None else initialMessage))  # store initial commit  # line 220
            _.saveCommit(branch, 0, remotes)  # save commit meta data to revision folder  # line 221
        _.saveBranch(branch, options)  # save branch meta data to branch folder - for fast branching, only empty dict  # line 222
        _.branches[branch] = newBranch  # save branches meta data, needs to be saved in caller code  # line 223

    def createBranch(_, branch: 'int', options: 'List[str]'=[], name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None):  # line 225
        ''' Create a new branch from the current file tree. This clears all known commits and modifies the file system.
        branch: target branch number (must not exist yet)
        name: optional name of new branch
        initialMessage: commit message for revision 0 of the new branch
        _.branch: current branch, must exist already
    '''  # line 231
        now = int(time.time() * 1000)  # type: int  # line 232
        remotes = _._extractRemotesFromArguments(options)  # type: List[str]  # line 233
        simpleMode = not (_.track or _.picky)  # type: bool  # line 234
        tracked = [t for t in _.branches[_.branch].tracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # in case of initial branch creation  # line 235
        untracked = [t for t in _.branches[_.branch].untracked] if _.track and len(_.branches) > 0 else []  # type: List[str]  # line 236
        if verbose:  # line 237
            info((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)("Creating branch '%s'..." % name))  # line 237
        _.paths = {}  # type: Dict[str, PathInfo]  # line 238
        if simpleMode:  # branches from file system state. not necessary to create branch folder, as it is done in findChanges below anyway  # line 239
            changed, msg = _.findChanges(branch, 0, progress=simpleMode, remotes=remotes)  # HINT creates revision folder and versioned files!  # line 240
            _.listChanges(changed)  # line 241
            if msg:  # display compression factor and time taken  # line 242
                printo(msg)  # display compression factor and time taken  # line 242
            _.paths.update(changed.additions.items())  # line 243
        else:  # tracking or picky mode: branch from latest revision  # line 244
            for remote in [None] + remotes:  # line 245
                tryOrDefault(lambda: os.makedirs(encode(revisionFolder(branch, 0, base=(_.root if remote is None else remote)))), lambda e: error("Creating remote branch folder %r" % remote))  # line 246
            if _.branch is not None:  # not immediately after "offline" - copy files from current branch  # line 247
                _.loadBranch(_.branch)  # line 248
                revision = max(_.commits) if _.commits else 0  # type: int  # TODO #245 what if last switch was to an earlier revision? no persisting of last checkout  # line 249
                _.computeSequentialPathSet(_.branch, revision)  # full set of files in revision to _.paths  # line 250
                for path, pinfo in _.paths.items():  # line 251
                    _.copyVersionedFile(_.branch, revision, branch, 0, pinfo)  # line 251
        _.commits = {0: CommitInfo(number=0, ctime=now, message=("Branched on %s" % strftime(now) if initialMessage is None else initialMessage))}  # store initial commit for new branch  # line 252
        _.saveBranch(branch, remotes)  # save branch meta data (revisions) to branch folder  # line 253
        _.saveCommit(branch, 0, remotes)  # save commit meta data to revision folder  # line 254
        _.branches[branch] = BranchInfo(branch, _.commits[0].ctime, name, True if len(_.branches) == 0 else _.branches[_.branch].inSync, tracked, untracked)  # save branch info, in case it is needed  # line 255

    def removeBranch(_, branch: 'int', options: 'List[str]'=[]) -> 'BranchInfo':  # line 257
        ''' Entirely remove a branch and all its revisions from the file system.
        We currently implement a simplified logic that fully re-creates all revisions for all transitively depending branches instead of only removing the one parent branch.
    '''  # line 260
        import collections  # used almost only here  # line 261
        binfo = None  # type: BranchInfo  # typing info  # line 262
        remotes = _._extractRemotesFromArguments(options)  # type: List[str]  # line 263
        deps = [(binfo.number, binfo.revision) for binfo in _.branches.values() if binfo.parent is not None and branch in _.getParentBranches(binfo.number, 0)]  # type: List[Tuple[int, int]]  # all transitively depending branches  # line 264
        newcommits = collections.defaultdict(dict)  # type: Dict[int, Dict[int, CommitInfo]]  # gathers commit info of re-created branches (branch -> revision -> info)  # line 265
        if deps:  # need to copy all parent revisions to dependent branches first  # line 266
            minrev = min((e[1] for e in deps))  # type: int  # minimum revision ever branched from parent: up to this revision we can simply them to all dependant branches  # line 267
            progress = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0])  # type: ProgressIndicator  # line 268
            for rev in range(0, minrev + 1):  # rely on caching by copying revision-wise as long as needed into all depending branches  # line 269
                for dep, _rev in deps:  # line 270
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # TODO #246 align placement of indicator with other uses of progress  # line 271
                    _.loadBranch(_.getParentBranch(branch, rev))  # load commits and set _.branch (in case branch to remove was also fast-branched)  # line 272
#          if rev in _.commits:  # TODO #247 uncomment? - if not, it was an empty commit? because on non-commit branches there's no revision 0?
                    newcommits[dep][rev] = _.commits[rev]  # line 274
                    for remote in [None] + remotes:  # line 275
                        shutil.copytree(encode(revisionFolder(_.branch, rev, base=(_.root if remote is None else remote))), encode(revisionFolder(dep, rev, base=(_.root if remote is None else remote))))  # line 276
            for dep, _rev in deps:  # copy remaining revisions by branch instead by revision  # line 277
                for rev in range(minrev + 1, _rev + 1):  # line 278
                    printo("\rIntegrating revision %02d into dependant branch %02d %s" % (rev, dep, progress.getIndicator()))  # line 279
                    _.loadBranch(_.getParentBranch(dep, rev))  # WARN using dep intead of branch here!  # line 280
                    if rev in _.commits:  # false only if no added or modified files during fast-branch?  # line 281
                        newcommits[dep][rev] = _.commits[rev]  # line 282
                        for remote in [None] + remotes:  # line 283
                            shutil.copytree(encode(revisionFolder(_.branch, rev, base=(_.root if remote is None else remote))), encode(revisionFolder(dep, rev, base=(_.root if remote is None else remote))))  # line 284
                _.branches[dep] = dataCopy(BranchInfo, _.branches[dep], parent=None, revision=None)  # delete fast-branching reference information  # line 285
        printo(pure.ljust() + "\r")  # clean line output  # line 286
        for remote in [None] + remotes:  # line 287
            tryOrIgnore(lambda: shutil.rmtree(encode(branchFolder(branch, base=remote) + BACKUP_SUFFIX)))  # remove previous backup first  # line 288
            tryOrIgnore(lambda: os.rename(encode(branchFolder(branch, base=remote)), encode(branchFolder(branch, base=remote) + BACKUP_SUFFIX)), lambda E: Exit("Cannot rename branch metadata to prepare removal. Are there locked or open files?", excp=E))  # line 289
        binfo = _.branches[branch]  # keep reference to removed branch info for caller  # line 290
        del _.branches[branch]  # line 291
        _.branch = (branch + 1) if (branch + 1) in _.branches else max(_.branches)  # switch to another valid branch  # line 292
        _.saveBranches(remotes)  # persist modified branches list  # line 293
        for branch, commits in newcommits.items():  # now store aggregated commit infos  # line 294
            _.commits = commits  # line 295
            _.saveBranch(branch, remotes)  # line 296
        _.commits.clear()  # clean memory  # line 297
        return binfo  # line 298

    def loadCommit(_, branch: 'int', revision: 'int'):  # line 300
        ''' Load all file information from a commit meta data; if branched from another branch before specified revision, load correct revision recursively. '''  # line 301
        _branch = _.getParentBranch(branch, revision)  # type: int  # line 302
        with codecs.open(encode(revisionFolder(_branch, revision, base=_.root, file=metaFile)), "r", encoding=UTF8) as fd:  # line 303
            _.paths = json.load(fd)  # line 303
        _.paths = {path: PathInfo(*item) for path, item in _.paths.items()}  # re-create type info  # line 304
        _.branch = branch  # store current branch information = "switch" to loaded branch/commit  # line 305

    def saveCommit(_, branch: 'int', revision: 'int', remotes: 'List[str]'=[]):  # line 307
        ''' Save all file information to a commit meta data file. '''  # line 308
        for remote in [None] + remotes:  # line 309
            try:  # line 310
                target = revisionFolder(branch, revision, base=(_.root if remote is None else remote))  # type: str  # line 311
                try:  # line 312
                    os.makedirs(encode(target), exist_ok=True)  # line 312
                except:  # line 313
                    pass  # line 313
                tryOrIgnore(lambda _=None: shutil.copy2(encode(os.path.join(target, metaFile)), encode(os.path.join(target, metaBack))))  # ignore error for first backup  # line 314
                with codecs.open(encode(os.path.join(target, metaFile)), "w", encoding=UTF8) as fd:  # line 315
                    json.dump(_.paths, fd, ensure_ascii=False)  # line 315
            except Exception as E:  # line 316
                debug("Error saving commit%s" % ((" to remote path " + remote) if remote else ""))  # line 316

    def findChanges(_, branch: '_coconut.typing.Optional[int]'=None, revision: '_coconut.typing.Optional[int]'=None, checkContent: 'bool'=False, inverse: 'bool'=False, considerOnly: '_coconut.typing.Optional[FrozenSet[str]]'=None, dontConsider: '_coconut.typing.Optional[FrozenSet[str]]'=None, progress: 'bool'=False, remotes: '_coconut.typing.Optional[List[str]]'=None) -> 'Tuple[ChangeSet, _coconut.typing.Optional[str]]':  # line 318
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
    '''  # line 331
        import collections  # used almost only here  # line 332
        write = branch is not None and revision is not None  # used for writing commits  # line 333
        if write:  # TODO "??" should not be necessary, as write is always True when committing, where remotes is provided externally anyway  # line 334
            for remote in [None] + ((_.remotes if remotes is None else remotes)):  # TODO "??" should not be necessary, as write is always True when committing, where remotes is provided externally anyway  # line 334
                try:  # exist_ok doesn't always work  # line 335
                    os.makedirs(encode(revisionFolder(branch, revision, base=(_.root if remote is None else remote))), exist_ok=True)  # exist_ok doesn't always work  # line 335
                except:  # line 336
                    pass  # line 336
        changed = ChangeSet({}, {}, {}, {})  # type: ChangeSet  # WARN this code needs explicity argument passing for initialization due to mypy problems with default arguments  # line 337
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # optional file list progress indicator  # line 338
        hashed = None  # type: _coconut.typing.Optional[str]  # line 339
        written = None  # type: int  # line 339
        compressed = 0  # type: int  # line 339
        original = 0  # type: int  # line 339
        start_time = time.time()  # type: float  # line 339
        knownPaths = {}  # type: Dict[str, List[str]]  # line 340

# Find relevant folders/files that match specified folder/glob patterns for exclusive inclusion or exclusion
        byFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 343
        onlyByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 344
        dontByFolder = collections.defaultdict(list)  # type: Dict[str, List[str]]  # line 345
        for path, pinfo in _.paths.items():  # line 346
            if pinfo is None:  # quicker than generator expression above  # line 347
                continue  # quicker than generator expression above  # line 347
            slash = path.rindex(SLASH)  # type: int  # line 348
            byFolder[path[:slash]].append(path[slash + 1:])  # line 349
        for pattern in ([] if considerOnly is None else considerOnly):  # line 350
            slash = pattern.rindex(SLASH)  # line 350
            onlyByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 350
        for pattern in ([] if dontConsider is None else dontConsider):  # line 351
            slash = pattern.rindex(SLASH)  # line 351
            dontByFolder[pattern[:slash]].append(pattern[slash + 1:])  # line 351
        for folder, paths in byFolder.items():  # line 352
            pos = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in onlyByFolder.get(folder, [])]) if considerOnly is not None else set(paths)  # type: Set[str]  # line 353
            neg = set.union(set(), *[fnmatch.filter(paths, pattern) for pattern in dontByFolder.get(folder, [])]) if dontConsider is not None else set()  # type: Set[str]  # line 354
            knownPaths[folder] = list(pos - neg)  # line 355

        for path, dirnames, filenames in os.walk(_.root):  # line 357
            path = decode(path)  # line 358
            dirnames[:] = [decode(d) for d in dirnames]  # line 359
            filenames[:] = [decode(f) for f in filenames]  # line 360
            dirnames[:] = [d for d in dirnames if len([n for n in _.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in _.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 361
            filenames[:] = [f for f in filenames if len([n for n in _.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 362
            dirnames.sort()  # line 363
            filenames.sort()  # line 363
            relPath = os.path.relpath(path, _.root).replace(os.sep, SLASH)  # type: str  # line 364
            walk = list(filenames if considerOnly is None else reduce(lambda last, pattern: last | set(fnmatch.filter(filenames, os.path.basename(pattern))), (p for p in considerOnly if os.path.dirname(p).replace(os.sep, SLASH) == relPath), _coconut.set()))  # type: List[str]  # line 365
            if dontConsider:  # line 366
                walk[:] = [fn for fn in walk if not any((fnmatch.fnmatch(fn, os.path.basename(p)) for p in dontConsider if os.path.dirname(p).replace(os.sep, SLASH) == relPath))]  # line 367
            for file in walk:  # if m.track or m.picky: only files that match any path-relevant tracking patterns  # line 368
                filename = relPath + SLASH + file  # line 369
                filepath = os.path.join(path, file)  # line 370
                try:  # line 371
                    stat = os.stat(encode(filepath))  # line 371
                except Exception as E:  # line 372
                    printo(exception(E))  # line 372
                    continue  # line 372
                size, mtime = stat.st_size, int(stat.st_mtime * 1000)  # line 373
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 374
                if show:  # indication character returned  # line 375
                    outstring = "\r%s %s  %s" % ("Preparing" if write else "Checking", show, filename)  # line 376
                    printo(pure.ljust(outstring), nl="")  # line 377
                progressSymbols = PROGRESS_MARKER[1 if _.c.useUnicodeFont else 0]  # type: str  # line 378
                if filename not in _.paths:  # detected file not present (or untracked) in (other) branch  # line 379
                    nameHash = hashStr(filename)  # line 380
                    try:  # line 381
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=nameHash) for remote in [None] + _.remotes] if write else None, callback=(lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if show else None) if size > 0 else (None, 0)  # line 382
                        changed.additions[filename] = PathInfo(nameHash, size, mtime, hashed)  # line 383
                        compressed += written  # line 384
                        original += size  # line 384
                    except PermissionError as E:  # line 385
                        error("File permission error for %s" % filepath)  # line 385
                    except Exception as F:  # HINT e.g. FileNotFoundError will not add to additions  # line 386
                        printo(exception(F))  # HINT e.g. FileNotFoundError will not add to additions  # line 386
                    continue  # with next file  # line 387
                last = _.paths[filename]  # filename is known - check for modifications  # line 388
                if last.size is None:  # was removed before but is now added back - does not apply for tracking mode (which never marks files for removal in the history)  # line 389
                    try:  # line 390
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not (progress and show) else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if size > 0 else (None, 0)  # line 391
                        changed.additions[filename] = PathInfo(last.nameHash, size, mtime, hashed)  # line 392
                        continue  # line 392
                        compressed += written  # line 393
                        original += last.size if inverse else size  # line 393
                    except Exception as E:  # line 394
                        printo(exception(E))  # line 394
                elif (size != last.size or (not checkContent and mtime != last.mtime) or (checkContent and tryOrDefault(lambda: (hashFile(filepath, _.compress, symbols=progressSymbols)[0] != last.hash), default=False))):  # detected a modification TODO invert error = False?  # line 395
                    try:  # line 399
                        hashed, written = hashFile(filepath, _.compress, symbols=progressSymbols, saveTo=[revisionFolder(branch, revision, base=(_.root if remote is None else remote), file=last.nameHash) for remote in [None] + _.remotes] if write else None, callback=None if not (progress and show) else lambda sign: printo(pure.ljust(outstring + " " + sign), nl="")) if (last.size if inverse else size) > 0 else (last.hash if inverse else hashFile(filepath, _.compress, symbols=progressSymbols, callback=None if not progress else lambda sign: printo(pure.ljust(outstring + " " + sign), nl=""))[0], 0)  # line 400
                        changed.modifications[filename] = PathInfo(last.nameHash, last.size if inverse else size, last.mtime if inverse else mtime, hashed)  # line 404
                        compressed += written  # line 405
                        original += last.size if inverse else size  # line 405
                    except Exception as E:  # line 406
                        printo(exception(E))  # line 406
                else:  # with next file  # line 407
                    continue  # with next file  # line 407
            if relPath in knownPaths:  # at least one file is tracked or --only HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 408
                knownPaths[relPath][:] = list(set(knownPaths[relPath]) - set(walk))  # at least one file is tracked or --only HINT may leave empty lists in dict, but removing them costs more than traversing them silently  # line 408
        for path, names in knownPaths.items():  # all paths that weren't walked by  # line 409
            for file in names:  # line 410
                if len([n for n in _.c.ignores if fnmatch.fnmatch(file, n)]) > 0 and len([p for p in _.c.ignoresWhitelist if fnmatch.fnmatch(file, p)]) == 0:  # don't mark ignored files as deleted  # line 411
                    continue  # don't mark ignored files as deleted  # line 411
                pth = path + SLASH + file  # type: str  # line 412
                changed.deletions[pth] = _.paths[pth]  # line 413
        changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, _.strict))  # line 414
        if progress:  # forces clean line of progress output  # line 415
            printo("\r" + pure.ljust() + "\r", nl="")  # forces clean line of progress output  # line 415
        elif verbose:  # line 416
            info("Finished detecting changes")  # line 416
        tt = time.time() - start_time  # type: float  # time taken  # line 417
        speed = (original / (KIBI * tt)) if tt > 0. else 0.  # type: float  # in KiBi  # line 418
        msg = (("Compression advantage is %.1f%%" % (original * 100. / compressed - 100.)) if _.compress and write and compressed > 0 else "")  # type: str  # line 419
        msg = (msg + " | " if msg else "") + "Processing speed was %.2f %sB/s%s." % (speed if speed < 1500. else speed / KIBI, ("ki" if speed < 1500. else "Mi") if speed > 0. else "", (" to %d remote locations" % len(_.remotes)) if _.remotes else "")  # line 420
        return (changed, msg if msg else None)  # line 421

    def computeSequentialPathSet(_, branch: 'int', revision: 'int'):  # line 423
        ''' Returns nothing, just updates _.paths in place. '''  # line 424
        next(_.computeSequentialPathSetIterator(branch, revision, incrementally=False))  # simply invoke the generator once to get full results  # line 425

    def computeSequentialPathSetIterator(_, branch: 'int', revision: 'int', incrementally: 'bool'=True, startwith: 'int'=0) -> '_coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]':  # line 427
        ''' In-memory computation of current list of valid PathInfo entries for specified branch and through specified revision. '''  # line 428
        try:  # load initial paths  # line 429
            _.loadCommit(branch, startwith)  # load initial paths  # line 429
        except:  # no revisions  # line 430
            yield {}  # no revisions  # line 430
            return None  # no revisions  # line 430
        if incrementally:  # line 431
            yield _.paths  # line 431
        m = Metadata(_.root)  # type: Metadata  # next changes TODO #250 avoid loading all metadata and config  # line 432
        rev = None  # type: int  # next changes TODO #250 avoid loading all metadata and config  # line 432
        for rev in range(startwith + 1, revision + 1):  # line 433
            m.loadCommit(branch, rev)  # line 434
            for p, info in m.paths.items():  # line 435
                if info.size == None:  # line 436
                    del _.paths[p]  # line 436
                else:  # line 437
                    _.paths[p] = info  # line 437
            if incrementally:  # line 438
                yield _.paths  # line 438
        yield None  # for the default case - not incrementally  # line 439

    def getTrackingPatterns(_, branch: '_coconut.typing.Optional[int]'=None, negative: 'bool'=False) -> 'FrozenSet[str]':  # line 441
        ''' Returns list of tracking patterns (or untracking patterns if negative) for provided branch or current branch. '''  # line 442
        return _coconut.frozenset() if not (_.track or _.picky) else frozenset(_.branches[(_.branch if branch is None else branch)].untracked if negative else _.branches[(_.branch if branch is None else branch)].tracked)  # line 443

    def parseRevisionString(_, argument: 'str') -> 'Union[Tuple[_coconut.typing.Optional[int], _coconut.typing.Optional[int]], NoReturn]':  # line 445
        ''' Parse (an optionally) combined branch and revision string, separated by a slash.
        Commit identifiers can be str or int for branch, and int for revision.
        Revision identifiers can be negative, with -1 being last commit (Python convention)
        (None, None) is returned in case of illegal inputs
        sys.exit() is called in case of unknown branch/revision
    '''  # line 451
        argument = (("/" if argument is None else argument)).strip()  # line 452
        if argument == SLASH:  # no branch/revision specified  # line 453
            return (_.branch, -1)  # no branch/revision specified  # line 453
        if argument == "":  # nothing specified by user, raise error in caller  # line 454
            return (None, None)  # nothing specified by user, raise error in caller  # line 454
        if argument.startswith(SLASH):  # current branch  # line 455
            return (_.branch, _.getRevisionByName(argument[1:]))  # current branch  # line 455
        if argument.endswith(SLASH):  # line 456
            try:  # line 457
                return (_.getBranchByName(argument[:-1]), -1)  # line 457
            except ValueError as E:  # line 458
                Exit("Unknown branch label '%s'" % argument, excp=E)  # line 458
        if SLASH in argument:  # line 459
            b, r = argument.split(SLASH)[:2]  # line 460
            try:  # line 461
                return (_.getBranchByName(b), _.getRevisionByName(r))  # line 461
            except ValueError as E:  # line 462
                Exit("Unknown branch label or wrong number format '%s/%s'" % (b, r), excp=E)  # line 462
        branch = _.getBranchByName(argument)  # type: _coconut.typing.Optional[int]  # returns number if given (revision) integer  # line 463
        if branch not in _.branches:  # line 464
            branch = None  # line 464
        try:  # either branch name/number or reverse/absolute revision number  # line 465
            return ((_.branch if branch is None else branch), ((lambda _coconut_none_coalesce_item: -1 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(_.getRevisionByName(argument))) if branch is None else -1)  # either branch name/number or reverse/absolute revision number  # line 465
        except Exception as E:  # line 466
            Exit("Unknown branch label or wrong branch/revision number format", excp=E)  # line 466
        Exit("This should never happen. Please create an issue report")  # line 467

    def findRevision(_, branch: 'int', revision: 'int', nameHash: 'str') -> 'Tuple[int, str]':  # line 469
        ''' Find latest revision that contained the file physically, not returning the actual parent branch it is stored on.
        Returns (highest revision <= specified revision containing the file, file path to file on (actual parent) branch).'''  # line 471
        while True:  # line 472
            _branch = _.getParentBranch(branch, revision)  # type: int  # line 473
            source = revisionFolder(_branch, revision, base=_.root, file=nameHash)  # type: str  # line 474
            if os.path.exists(encode(source)) and os.path.isfile(source):  # line 475
                break  # line 475
            revision -= 1  # line 476
            if revision < 0:  # line 477
                Exit("Cannot determine versioned file '%s' from specified branch '%d'" % (nameHash, branch))  # line 477
        return revision, source  # line 478

    def getParentBranches(_, branch: 'int', revision: 'int') -> 'List[int]':  # line 480
        ''' Determine originating branch for a (potentially branched) revision, traversing all branch parents until found. '''  # line 481
        others = [_.branches[branch].parent]  # type: List[int]  # reference to originating parent branch, or None  # line 482
        if others[0] is None or revision > _.branches[branch].revision:  # found. need to load commit from other branch instead  # line 483
            return [branch]  # found. need to load commit from other branch instead  # line 483
        while _.branches[others[-1]].parent is not None and revision <= _.branches[others[-1]].revision:  # find true original branch for revision  # line 484
            others.append(_.branches[others[-1]].parent)  # find true original branch for revision  # line 484
        return others  # line 485

    def getParentBranch(_, branch: 'int', revision: 'int') -> 'int':  # line 487
        return _.getParentBranches(branch, revision)[-1]  # line 487

    def getHighestRevision(_, branch: 'int') -> '_coconut.typing.Optional[int]':  # line 489
        ''' Find highest revision of a branch, even if current branch has no commits. '''  # line 490
        m = Metadata()  # type: Metadata  # line 491
        other = branch  # type: _coconut.typing.Optional[int]  # line 492
        while other is not None:  # line 493
            m.loadBranch(other)  # line 494
            if m.commits:  # line 495
                return max(m.commits)  # line 495
            other = _.branches[branch].parent  # reference to originating parent branch, or None  # line 496
        return None  # line 497

    def copyVersionedFile(_, branch: 'int', revision: 'int', toBranch: 'int', toRevision: 'int', pinfo: 'PathInfo'):  # line 499
        ''' Copy versioned file to other branch/revision. '''  # line 500
        revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 501
        for remote in [None] + _.remotes:  # line 502
            try:  # line 503
                target = revisionFolder(toBranch, toRevision, file=pinfo.nameHash, base=(_.root if remote is None else remote))  # type: str  # line 504
                shutil.copy2(encode(source), encode(target))  # line 505
            except Exception as E:  # line 506
                error("Copying versioned file%s" % ((" to remote path " % remote) if remote else ""))  # line 506

    def readOrCopyVersionedFile(_, branch: 'int', revision: 'int', nameHash: 'str', toFile: '_coconut.typing.Optional[str]'=None) -> '_coconut.typing.Optional[bytes]':  # line 508
        ''' Return file contents, or copy contents into file path provided (used in update and restorefile). '''  # line 509
        source = _.findRevision(branch, revision, nameHash)[1]  # type: str  # revisionFolder(_.getParentBranch(branch, revision), _.findRevision(branch, revision, nameHash)[0], base = _.root, file = nameHash)  # line 510
        try:  # line 511
            with openIt(source, "r", _.compress) as fd:  # line 511
                if toFile is None:  # read bytes into memory and return  # line 512
                    return fd.read()  # read bytes into memory and return  # line 512
                with open(encode(toFile), "wb") as to:  # line 513
                    while True:  # line 514
                        buffer = fd.read(bufSize)  # line 515
                        to.write(buffer)  # line 516
                        if len(buffer) < bufSize:  # line 517
                            break  # line 517
                    return None  # line 518
        except Exception as E:  # line 519
            warn("Cannot read versioned file: %r (%d:%d:%s)" % (E, branch, revision, nameHash))  # line 519
        None  # line 520

    def restoreFile(_, relPath: '_coconut.typing.Optional[str]', branch: 'int', revision: 'int', pinfo: 'PathInfo', ensurePath: 'bool'=False) -> '_coconut.typing.Optional[bytes]':  # line 522
        ''' Recreate file for given revision, or return binary contents if path is None. '''  # line 523
        if relPath is None:  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 524
            return _.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # _.findRevision(branch, revision, pinfo.nameHash)[0], pinfo.nameHash) if pinfo.size > 0 else b''  # just return contents  # line 524
        target = os.path.join(_.root, relPath.replace(SLASH, os.sep))  # type: str  # line 525
        if ensurePath:  #  and not os.path.exists(encode(os.path.dirname(target))):  # line 526
            try:  # line 527
                os.makedirs(encode(os.path.dirname(target)), exist_ok=True)  # line 527
            except:  # line 528
                pass  # line 528
        if pinfo.size == 0:  # line 529
            with open(encode(target), "wb"):  # line 530
                pass  # line 530
            try:  # update access/modification timestamps on file system  # line 531
                os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 531
            except Exception as E:  # line 532
                error("Cannot update file's timestamp after restoration '%r'" % E)  # line 532
            return None  # line 533
        _revision, source = _.findRevision(branch, revision, pinfo.nameHash)  # line 534
# Restore file by copying buffer-wise
        with openIt(source, "r", _.compress) as fd, open(encode(target), "wb") as to:  # using Coconut's Enhanced Parenthetical Continuation  # line 536
            while True:  # line 537
                buffer = fd.read(bufSize)  # line 538
                to.write(buffer)  # line 539
                if len(buffer) < bufSize:  # line 540
                    break  # line 540
        try:  # update access/modification timestamps on file system  # line 541
            os.utime(encode(target), (pinfo.mtime / 1000., pinfo.mtime / 1000.))  # update access/modification timestamps on file system  # line 541
        except Exception as E:  # line 542
            error("Cannot update file's timestamp after restoration '%r'" % E)  # line 542
        return None  # line 543


# Main client operations
def offline(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], remotes: 'List[str]'=[]):  # line 547
    ''' Initial command to start working offline. '''  # line 548
    if os.path.exists(encode(metaFolder)):  # line 549
        if '--force' not in options:  # line 550
            Exit("Repository folder is either already offline or older branches and commits were left over\nUse 'sos online' to check for out-of-sync branches, or\nWipe existing offline branches with 'sos offline --force'")  # line 550
        try:  # throw away all previous metadata before going offline  # line 551
            for entry in os.listdir(metaFolder):  # TODO #251 why not rmtree the metadata alltogether as in "online"? I think removing .sos/ made problems on CI. test again  # line 552
                resource = metaFolder + os.sep + entry  # line 553
                if os.path.isdir(resource):  # line 554
                    shutil.rmtree(encode(resource))  # line 554
                else:  # line 555
                    os.unlink(encode(resource))  # line 555
        except Exception as E:  # line 556
            Exit("Cannot reliably remove previous repository contents. Please remove %s folder manually prior to going offline" % metaFolder, excp=E)  # line 556
    for remote in remotes:  # line 557
        try:  # line 558
            os.makedirs(os.path.join(remote, metaFolder))  # line 558
        except Exception as E:  # line 559
            error("Creating remote repository metadata in %s" % remote)  # line 559
    m = Metadata(offline=True, remotes=remotes)  # type: Metadata  # line 560
    if '--strict' in options or m.c.strict:  # always hash contents  # line 561
        m.strict = True  # always hash contents  # line 561
    if '--compress' in options or m.c.compress:  # plain file copies instead of compressed ones  # line 562
        m.compress = True  # plain file copies instead of compressed ones  # line 562
    if '--picky' in options or m.c.picky:  # Git-like  # line 563
        m.picky = True  # Git-like  # line 563
    elif '--track' in options or m.c.track:  # Svn-like  # line 564
        m.track = True  # Svn-like  # line 564
    title = usage.getTitle()  # type: _coconut.typing.Optional[str]  # line 565
    if title:  # line 566
        printo(title)  # line 566
    if verbose:  # line 567
        info(MARKER + "Going offline...")  # line 567
    m.createBranch(0, remotes, (defaults["defaultbranch"] if name is None else name), ("Offline repository created on %s" % strftime() if initialMessage is None else initialMessage))  # main branch's name may be None (e.g. for fossil)  # line 568
    m.branch = 0  # line 569
    m.saveBranches(remotes=remotes, also={"version": version.__version__})  # stores version info only once. no change immediately after going offline, going back online won't issue a warning  # line 570
    if verbose or '--verbose' in options:  # line 571
        info("%d file%s added to initial branch %r" % (len(m.paths), "s" if len(m.paths) > 1 else "", m.branches[m.branch].name))  # line 571
    info(MARKER + "Offline repository prepared. Use 'sos online' to finish offline work")  # line 572

def online(options: '_coconut.typing.Sequence[str]'=[]):  # line 574
    ''' Finish working offline. '''  # line 575
    if verbose:  # line 576
        info(MARKER + "Going back online...")  # line 576
    force = '--force' in options  # type: bool  # line 577
    m = Metadata()  # type: Metadata  # line 578
    remotes = m._extractRemotesFromArguments(options)  # type: List[str]  # line 579
    strict = '--strict' in options or m.strict  # type: bool  # line 580
    m.loadBranches()  # line 581
    if any([not b.inSync for b in m.branches.values()]) and not force:  # line 582
        Exit("There are still unsynchronized (modified) branches\nUse 'sos log' to list them.\nUse 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.\nUse 'sos online --force' to erase all aggregated offline revisions without further action.")  # line 582
    m.loadBranch(m.branch)  # line 583
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 584
    if options.count("--force") < 2:  # line 585
        m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 586
        changed, msg = m.findChanges(checkContent=strict, considerOnly=None if not (m.track or m.picky) else m.getTrackingPatterns(), dontConsider=None if not (m.track or m.picky) else m.getTrackingPatterns(negative=True), progress='--progress' in options)  # HINT no option for --only/--except here on purpose. No check for picky here, because online is not a command that considers staged files (but we could use --only here, alternatively)  # line 587
        if modified(changed):  # line 588
            Exit("File tree is modified vs. current branch\nUse 'sos online --force --force' to continue with removing the offline repository")  # line 592
    try:  # line 593
        shutil.rmtree(encode(metaFolder))  # line 593
        info("Exited offline mode. Continue working with your traditional VCS." + (" Remote copies have to be removed manually." if remotes else ""))  # line 593
    except Exception as E:  # line 594
        Exit("Error removing offline repository.", excp=E)  # line 594
    info(MARKER + "Offline repository removed, you're back online")  # line 595

def branch(name: '_coconut.typing.Optional[str]'=None, initialMessage: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 597
    ''' Create a new branch (from file tree or last revision) and (by default) continue working on it.
      Force not required here, as either branching from last revision anyway, or branching full file tree anyway.
  '''  # line 600
    last = '--last' in options  # type: bool  # use last revision for branching, not current file tree  # line 601
    stay = '--stay' in options  # type: bool  # continue on current branch after branching (don't switch)  # line 602
    fast = '--fast' in options  # type: bool  # branch by referencing TODO #252 move to default and use --full instead for old behavior  # line 603
    m = Metadata()  # type: Metadata  # line 604
    remotes = m._extractRemotesFromArguments(options)  # type: List[str]  # line 605
    m.loadBranch(m.branch)  # line 606
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 607
    if name and m.getBranchByName(name) is not None:  # attempted to create a named branch  # line 608
        Exit("Branch '%s' already exists. Cannot proceed" % name)  # attempted to create a named branch  # line 608
    branch = max(m.branches.keys()) + 1  # next branch's key - this isn't atomic but we assume single-user non-concurrent use here  # line 609
    if verbose:  # line 610
        info(MARKER + "Branching to %sbranch b%d%s%s..." % ("unnamed " if name is None else "", branch, " '%s'" % name if name is not None else "", " from last revision" if last else ""))  # line 610
    if last:  # branch from last revision  # line 611
        m.duplicateBranch(branch, remotes, name, (initialMessage + " " if initialMessage else "") + "(Branched from b%d/r%02d)" % (m.branch, maxi), not fast)  # branch from last revision  # line 611
    else:  # branch from current file tree state  # line 612
        m.createBranch(branch, remotes, name, ("Branched from file tree after b%d/r%02d" % (m.branch, maxi) if initialMessage is None else initialMessage))  # branch from current file tree state  # line 612
    if not stay:  # line 613
        m.branch = branch  # line 613
    m.saveBranches(remotes)  # TODO #253 or indent again?  # line 614
    info(MARKER + "%s new %sbranch b%d%s" % ("Continue work after branching" if stay else "Switched to", "unnamed " if name is None else "", branch, " '%s'" % name if name else ""))  # line 615

def changes(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None) -> 'ChangeSet':  # line 617
    ''' Show changes of file tree vs. (last or specified) revision on current or specified branch. '''  # line 618
    m = Metadata()  # type: Metadata  # line 619
    branch = None  # type: _coconut.typing.Optional[int]  # line 619
    revision = None  # type: _coconut.typing.Optional[int]  # line 619
    strict = '--strict' in options or m.strict  # type: bool  # line 620
    branch, revision = m.parseRevisionString(argument)  # line 621
    if branch is None or branch not in m.branches:  # line 622
        Exit("Unknown branch")  # line 622
    m.loadBranch(branch)  # knows commits  # line 623
    revision = m.correctNegativeIndexing(revision)  # m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 624
    if verbose:  # line 625
        info(MARKER + "Changes of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 625
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 626
    changed, msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 627
    m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else time.time(), root=os.path.abspath(cwd) if '--relative' in options else None)  # line 632
    return changed  # returning for unit tests only TODO #254 remove?  # line 633

def _diff(m: 'Metadata', branch: 'int', revision: 'int', changed: 'ChangeSet', ignoreWhitespace: 'bool', textWrap: 'bool'=False, classic: 'bool'=False):  # TODO #255 introduce option to diff against committed revision and not only file tree  # line 635
    ''' The diff display code. '''  # line 636
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 637
    wrap = (lambda s: s) if textWrap else (lambda s: s[:termWidth])  # type: _coconut.typing.Callable[[str], str]  # HINT since we don't know the actual width of unicode strings, we cannot be sure this is really maximizing horizontal space (like ljust), but probably not worth iteratively finding the right size  # line 638
    onlyBinaryModifications = dataCopy(ChangeSet, changed, modifications={k: v for k, v in changed.modifications.items() if not m.isTextType(os.path.basename(k))})  # type: ChangeSet  # line 639
    m.listChanges(onlyBinaryModifications, commitTime=m.commits[max(m.commits)].ctime)  # only list modified binary files  # line 640
    for path, pinfo in sorted((c for c in changed.modifications.items() if m.isTextType(os.path.basename(c[0])))):  # only consider modified text files TODO also show timestamp change for binary files (+full compare?)  # line 641
        content = b""  # type: _coconut.typing.Optional[bytes]  # stored state (old = "curr")  # line 642
        if pinfo.size != 0:  # versioned file  # line 643
            content = m.restoreFile(None, branch, revision, pinfo)  # versioned file  # line 643
            assert content is not None  # versioned file  # line 643
        abspath = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # current state (new = "into")  # line 644
        if classic:  # line 645
            mergeClassic(content, abspath, "b%d/r%02d" % (branch, revision), os.path.basename(abspath), pinfo.mtime, number_)  # line 645
            continue  # line 645
        blocks = None  # type: List[MergeBlock]  # line 646
        nl = None  # type: bytes  # line 646
        blocks, nl = merge(filename=abspath, into=content, diffOnly=True, ignoreWhitespace=ignoreWhitespace)  # only determine change blocks  # line 647
        printo("DIF %s%s  %s" % (path, " <timestamp or newline>" if len(blocks) == 1 and blocks[0].tipe == MergeBlockType.KEEP else "", NL_NAMES[nl]), color=Fore.WHITE)  # line 648
        linemax = pure.requiredDecimalDigits(max([block.line for block in blocks]) if len(blocks) > 0 else 1)  # type: int  # line 649
        for block in blocks:  # line 650
#      if block.tipe in [MergeBlockType.INSERT, MergeBlockType.REMOVE]:
#        pass  # TODO print some of previous and following lines - which aren't accessible here anymore
            if block.tipe == MergeBlockType.INSERT:  # line 653
                for no, line in enumerate(block.lines):  # SVN diff uses --,++-+- only  # line 654
                    printo(wrap("--- %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.RED)  # SVN diff uses --,++-+- only  # line 654
            elif block.tipe == MergeBlockType.REMOVE:  # line 655
                for no, line in enumerate(block.lines):  # line 656
                    printo(wrap("+++ %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.GREEN)  # line 656
            elif block.tipe == MergeBlockType.REPLACE:  # line 657
                for no, line in enumerate(block.replaces.lines):  # line 658
                    printo(wrap("old %%0%dd |%%s|" % linemax % (no + block.replaces.line, line)), color=Fore.MAGENTA)  # line 658
                for no, line in enumerate(block.lines):  # line 659
                    printo(wrap("now %%0%dd |%%s|" % linemax % (no + block.line, line)), color=Fore.CYAN)  # line 659
#      elif block.tipe == MergeBlockType.KEEP: pass  # TODO #257 allow to show kept stuff, or a part of pre-post lines
#      elif block.tipe == MergeBlockType.MOVE:  # intra-line modifications
            if block.tipe != MergeBlockType.KEEP:  # line 662
                printo()  # line 662

def diff(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 664
    ''' Show text file differences of file tree vs. (last or specified) revision on current or specified branch. '''  # line 665
    m = Metadata()  # type: Metadata  # line 666
    branch = None  # type: _coconut.typing.Optional[int]  # line 666
    revision = None  # type: _coconut.typing.Optional[int]  # line 666
    strict = '--strict' in options or m.strict  # type: bool  # line 667
    ignoreWhitespace = '--ignore-whitespace' in options or '--iw' in options  # type: bool  # line 668
    wrap = '--wrap' in options  # type: bool  # allow text to wrap around  # line 669
    branch, revision = m.parseRevisionString(argument)  # if nothing given, use last commit  # line 670
    if branch is None or branch not in m.branches:  # line 671
        Exit("Unknown branch")  # line 671
    m.loadBranch(branch)  # knows commits  # line 672
    revision = m.correctNegativeIndexing(revision)  #  m.branches[branch].revision if not m.commits else (revision if revision >= 0 else max(m.commits) + 1 + revision)  # negative indexing  # line 673
    if verbose:  # line 674
        info(MARKER + "Textual differences of file tree vs. revision '%s/r%02d'" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 674
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision  # line 675
    changed, msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, m.getTrackingPatterns() | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((m.getTrackingPatterns(negative=True) | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # line 676
    _diff(m, branch, revision, changed, ignoreWhitespace=ignoreWhitespace, textWrap=wrap, classic='--classic' in options)  # line 681

def commit(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 683
    ''' Create new revision from file tree changes vs. last commit. '''  # line 684
    m = Metadata()  # type: Metadata  # line 685
    if argument is not None and argument in m.tags:  # line 686
        Exit("Illegal commit message. It was already used as a (unique) tag name and cannot be reused")  # line 686
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # SVN-like mode  # line 687
# No untracking patterns needed here
    if m.picky and not trackingPatterns:  # line 689
        Exit("No file patterns staged for commit in picky mode")  # line 689
    if verbose:  # line 690
        info((lambda _coconut_none_coalesce_item: "b%d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Committing changes to branch '%s'..." % m.branches[m.branch].name))  # line 690
    remotes = m._extractRemotesFromArguments(options)  # line 691
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, check=False, commit=True, onlys=onlys, excps=excps)  # special flag creates new revision for detected changes, but aborts if no changes  # line 692
    changed = dataCopy(ChangeSet, changed, moves=detectMoves(changed, strict))  # line 693
    m.paths = {k: v for k, v in changed.additions.items()}  # copy to avoid wrong file numbers report below  # line 694
    m.paths.update(changed.modifications)  # update pathset to changeset only  # line 695
    (m.paths.update)({k: dataCopy(PathInfo, v, size=None, hash=None) for k, v in changed.deletions.items()})  # line 696
    m.saveCommit(m.branch, revision, remotes)  # revision has already been incremented  # line 697
    m.commits[revision] = CommitInfo(number=revision, ctime=int(time.time() * 1000), message=argument)  # comment can be None  # line 698
    m.saveBranch(m.branch, remotes)  # line 699
    m.loadBranches()  # TODO #258 is it necessary to load again?  # line 700
    if m.picky:  # remove tracked patterns  # line 701
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=[], inSync=False)  # remove tracked patterns  # line 701
    else:  # track or simple mode: set branch modified  # line 702
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=False)  # track or simple mode: set branch modified  # line 702
    if "--tag" in options and argument is not None:  # memorize unique tag  # line 703
        m.tags.append(argument)  # memorize unique tag  # line 703
        info("Version was tagged with %s" % argument)  # memorize unique tag  # line 703
    m.saveBranches(remotes)  # line 704
    stored = 0  # type: int  # now determine new commit size on file system  # line 705
    overhead = 0  # type: int  # now determine new commit size on file system  # line 705
    count = 0  # type: int  # now determine new commit size on file system  # line 705
    commitFolder = revisionFolder(m.branch, revision)  # type: str  # line 706
    for file in os.listdir(commitFolder):  # line 707
        try:  # line 708
            newsize = os.stat(encode(os.path.join(commitFolder, file))).st_size  # type: int  # line 709
            if file == metaFile:  # line 710
                overhead += newsize  # line 710
            else:  # line 711
                stored += newsize  # line 711
                count += 1  # line 711
        except Exception as E:  # line 712
            error(E)  # line 712
    printo(MARKER_COLOR + "Created new revision r%02d%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%s%s%s%02d) summing %s in %d files (%.2f%% SOS overhead)" % (revision, (" '%s'" % argument) if argument is not None else "", Fore.GREEN, Fore.RESET, len(changed.additions) - len(changed.moves), Fore.RED, Fore.RESET, len(changed.deletions) - len(changed.moves), Fore.YELLOW, CHANGED_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(changed.modifications), Fore.BLUE + Style.BRIGHT, MOVED_SYMBOL if m.c.useUnicodeFont else "#", Style.RESET_ALL, len(changed.moves), pure.siSize(stored + overhead), count, (overhead * 100. / (stored + overhead)) if stored + overhead > 0 else 0.))  # line 713

def status(argument: '_coconut.typing.Optional[str]'=None, vcs: '_coconut.typing.Optional[str]'=None, cmd: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 725
    ''' Show branches and current repository state. '''  # line 726
    m = Metadata()  # type: Metadata  # line 727
    if not (m.c.useChangesCommand or any((option.startswith('--repo') for option in options))):  # line 728
        changes(argument, options, onlys, excps)  # line 728
        return  # line 728
    current = m.branch  # type: int  # line 729
    strict = '--strict' in options or m.strict  # type: bool  # line 730
    printo(MARKER_COLOR + "Offline repository status")  # line 731
    printo("Repository root:     %s" % os.getcwd())  # line 732
    printo("Underlying VCS root: %s" % vcs)  # line 733
    printo("Underlying VCS type: %s" % cmd)  # line 734
    printo("Installation path:   %s" % os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  # because sos/sos.py  # line 735
    printo("Current SOS version: %s" % version.__version__)  # line 736
    printo("At creation version: %s" % m.version)  # line 737
    printo("Metadata format:     %s" % m.format)  # line 738
    printo("Content checking:    %s" % (Fore.CYAN + "size, then content" if m.strict else Fore.BLUE + "size & timestamp") + Fore.RESET)  # TODO size then timestamp?  # line 739
    printo("Data compression:    %sactivated%s" % (Fore.CYAN if m.compress else Fore.BLUE + "de", Fore.RESET))  # line 740
    printo("Repository mode:     %s%s" % (Fore.CYAN + "track" if m.track else (Fore.MAGENTA + "picky" if m.picky else Fore.GREEN + "simple"), Fore.RESET))  # line 741
    printo("Number of branches:  %d" % len(m.branches))  # line 742
    if m.remotes:  # HINT #290  # line 743
        printo("Remote duplicates:   %s" % ", ".join(m.remotes))  # HINT #290  # line 743
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 744
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 745
    m.loadBranch(current)  # line 746
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: _coconut.typing.Optional[int]  # line 747
    if maxi is not None:  # load all commits up to specified revision, except no commits  # line 748
        m.computeSequentialPathSet(current, maxi)  # load all commits up to specified revision, except no commits  # line 748
    changed, _msg = m.findChanges(checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress=True)  # line 749
    printo("%s File tree %s%s" % (Fore.YELLOW + (CROSS_SYMBOL if m.c.useUnicodeFont else "!") if modified(changed) else Fore.GREEN + (CHECKMARK_SYMBOL if m.c.useUnicodeFont else " "), "has changes" if modified(changed) else "is unchanged", Fore.RESET))  # TODO #259 bad choice of unicode symbols for changed vs. unchanged  # line 754
    sl = max([len((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(b.name)) for b in m.branches.values()])  # type: int  # line 758
    for branch in sorted(m.branches.values(), key=lambda b: b.number):  # line 759
        payload = 0  # type: int  # line 760
        overhead = 0  # type: int  # line 760
        for dn, ds, fs in os.walk(branchFolder(branch.number)):  # line 761
            for f in fs:  # TODO #260 count all backup folders as overhead instead? check "onlydeveloped" code for that logic  # line 762
                if f == metaFile or f.endswith(BACKUP_SUFFIX):  # line 763
                    overhead += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 763
                else:  # line 764
                    payload += tryOrDefault(lambda _=None: os.stat(encode(os.path.join(dn, f))).st_size, 0)  # line 764
        pl_amount = float(payload) / MEBI  # type: float  # line 765
        oh_amount = float(overhead) / MEBI  # type: float  # line 765
# if pl_amount >= 1100.:   convert to string
        m.loadBranch(branch.number)  # knows commit history  # line 767
        original = 0  # type: int  # compute occupied storage per branch  # line 768
        updates = []  # type: _coconut.typing.Sequence[int]  # compute occupied storage per branch  # line 768
        for commit_ in range(1 + max(m.commits) if m.commits else 0):  # line 769
            m.loadCommit(m.branch, commit_)  # line 770
            for pinfo in m.paths.values():  # line 771
                original += (lambda _coconut_none_coalesce_item: 0 if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(pinfo.size)  # line 771
            updates.append(len(m.paths))  # number of additions or removals TODO count "moves" as 1 instead of 2  # line 772
        maxi = max(m.commits) if m.commits else m.branches[branch.number].revision  # line 773
        printo("  %s b%d%s @%s (%s%s) with %d commits (median %d), using %.2f MiB (+%.3f%% for SOS%s)%s" % ("*" if current == branch.number else " ", branch.number, ((" %%%ds" % (sl + 2)) % (("'%s'" % branch.name) if branch.name else "")), strftime(branch.ctime), (Fore.GREEN + "in sync") if branch.inSync else (Fore.YELLOW + "modified"), Fore.RESET, len(m.commits), median(updates) if updates else 0.0, pl_amount + oh_amount, oh_amount * 100. / (pl_amount + oh_amount), ", %s compression/branch deduplication" % (("%.2f%s" % (float(original) / float(payload), MULT_SYMBOL if m.c.useUnicodeFont else "x")) if payload > 0 else "full") if m.compress or (len(m.commits) > 0 and len(m.commits) != max(m.commits) + 1) else "", (". Last comment: '%s'" % m.commits[maxi].message) if maxi in m.commits and m.commits[maxi].message else ""))  # line 774
    if m.track or m.picky and (len(m.branches[m.branch].tracked) > 0 or len(m.branches[m.branch].untracked) > 0):  # line 787
        printo(Fore.GREEN + "Tracked" + Fore.RESET + " file patterns:")  # TODO #261 print matching untracking patterns side-by-side?  # line 788
        printo(ajoin(Fore.GREEN + "  | " + Fore.RESET, m.branches[m.branch].tracked, "\n"))  # line 789
        printo(Fore.RED + "Untracked" + Fore.RESET + " file patterns:")  # line 790
        printo(ajoin(Fore.RED + "  | " + Fore.RESET, m.branches[m.branch].untracked, "\n"))  # line 791

def exitOnChanges(argument: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[], check: 'bool'=True, commit: 'bool'=False, onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None) -> 'Tuple[Metadata, _coconut.typing.Optional[int], int, ChangeSet, bool, bool, FrozenSet[str], FrozenSet[str]]':  # line 793
    ''' Common behavior for switch, update, delete, commit.
      Should not be called for picky mode, unless tracking patterns were already added.
      argument: optional branch/revision, used only in switch and update
      check: stop program on detected change (default yes)
      commit: don't stop on changes and write to file system
      Returns (Metadata, (current or target) branch, revision, set of changes vs. last commit on current branch, strict, force flags.
  '''  # line 800
    assert not (check and commit)  # line 801
    m = Metadata()  # type: Metadata  # line 802
    remotes = m._extractRemotesFromArguments(options)  # type: List[str]  # line 803
    force = '--force' in options  # type: bool  # line 804
    strict = '--strict' in options or m.strict  # type: bool  # line 805
    if argument is not None:  # line 806
        branch, revision = m.parseRevisionString(argument)  # for early abort  # line 807
        if branch is None:  # line 808
            Exit("Branch '%s' doesn't exist. Cannot proceed" % argument)  # line 808
    m.loadBranch(m.branch)  # knows last commits of *current* branch  # line 809
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # line 810

# Determine current changes
    trackingPatterns = m.getTrackingPatterns()  # type: FrozenSet[str]  # line 813
    untrackingPatterns = m.getTrackingPatterns(negative=True)  # type: FrozenSet[str]  # line 814
    m.computeSequentialPathSet(m.branch, maxi)  # load all commits up to specified revision  # line 815
    changed, msg = m.findChanges(m.branch if commit else None, maxi + 1 if commit else None, checkContent=strict, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns), dontConsider=excps if not (m.track or m.picky) else (untrackingPatterns if excps is None else excps), progress='--progress' in options, remotes=remotes)  # line 816
    if check and modified(changed) and not force:  # line 822
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 823
        Exit("File tree contains changes. Use --force to proceed")  # line 824
    elif commit:  # line 825
        if not modified(changed) and not force:  # line 826
            Exit("Nothing to commit")  # line 826
        m.listChanges(changed, commitTime=m.commits[max(m.commits)].ctime if m.commits else 0)  # line 827
        if msg:  # line 828
            printo(msg)  # line 828

    if argument is not None:  # branch/revision specified  # line 830
        m.loadBranch(branch)  # knows commits of target branch  # line 831
        maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # line 832
        revision = m.correctNegativeIndexing(revision)  # line 833
        return (m, branch, revision, changed, strict, force, m.getTrackingPatterns(branch), m.getTrackingPatterns(branch, negative=True))  # line 834
    return (m, m.branch, maxi + (1 if commit else 0), changed, strict, force, trackingPatterns, untrackingPatterns)  # line 835

def switch(argument: 'str', options: 'List[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None, cwd: '_coconut.typing.Optional[str]'=None):  # line 837
    ''' Continue work on another branch, replacing file tree changes. '''  # line 838
    m, branch, revision, changed, strict, _force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, ["--force"] + options)  # --force continuation to delay check to this function  # line 839
    force = '--force' in options  # type: bool  # needed as we fake force in above access  # line 840

# Determine file changes from other branch to current file tree
    if '--meta' in options:  # only switch meta data (tracking patterns only)  # line 843
        m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], tracked=m.branches[branch].tracked, untracked=m.branches[branch].untracked)  # line 844
    else:  # full file switch  # line 845
        m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for target branch into memory  # line 846
        todos, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingPatterns | m.getTrackingPatterns(branch)), dontConsider=excps if not (m.track or m.picky) else ((untrackingPatterns | m.getTrackingPatterns(branch, negative=True)) if excps is None else excps), progress='--progress' in options)  # determine difference of other branch vs. file tree (forced or in sync with current branch; "addition" means exists now and should be removed)  # line 847

# Now check for potential conflicts
        changed.deletions.clear()  # local deletions never create conflicts, modifications always  # line 854
        rms = []  # type: _coconut.typing.Sequence[str]  # local additions can be ignored if restoration from switch would be same  # line 855
        for a, pinfo in changed.additions.items():  # has potential corresponding re-add in switch operation:  # line 856
            if a in todos.deletions and pinfo.size == todos.deletions[a].size and (pinfo.hash == todos.deletions[a].hash if m.strict else pinfo.mtime == todos.deletions[a].mtime):  # line 857
                rms.append(a)  # line 857
        for rm in rms:  # TODO could also silently accept remote DEL for local ADD  # line 858
            del changed.additions[rm]  # TODO could also silently accept remote DEL for local ADD  # line 858
        if modified(changed) and not force:  # line 859
            m.listChanges(changed, cwd)  # line 859
            Exit("File tree contains changes. Use --force to proceed")  # line 859
        if verbose:  # line 860
            info(MARKER + "Switching to branch %sb%d/r%02d..." % ("'%s' " % m.branches[branch].name if m.branches[branch].name else "", branch, revision))  # line 860
        if not modified(todos):  # line 861
            info("No changes to current file tree")  # line 862
        else:  # integration required  # line 863
            for path, pinfo in todos.deletions.items():  # line 864
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # is deleted in current file tree: restore from branch to reach target state  # line 865
                printo("ADD " + path, color=Fore.GREEN)  # line 866
            for path, pinfo in todos.additions.items():  # line 867
                os.unlink(encode(os.path.join(m.root, path.replace(SLASH, os.sep))))  # is added in current file tree: remove from branch to reach target state  # line 868
                printo("DEL " + path, color=Fore.RED)  # line 869
            for path, pinfo in todos.modifications.items():  # line 870
                m.restoreFile(path, branch, revision, pinfo)  # is modified in current file tree: restore from branch to reach target  # line 871
                printo("MOD " + path, color=Fore.YELLOW)  # line 872
    m.branch = branch  # line 873
    m.saveBranches(m._extractRemotesFromArguments(options))  # store switched path info  # line 874
    info(MARKER + "Switched to branch %sb%d/r%02d" % ("'%s' " % (m.branches[branch].name if m.branches[branch].name else ""), branch, revision))  # line 875

def update(argument: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 877
    ''' Load and integrate a specified other branch/revision into current life file tree.
      In tracking mode, this also updates the set of tracked patterns.
      User options for merge operation: --add/--rm/--ask --add-lines/--rm-lines/--ask-lines (inside each file), --add-chars/--rm-chars/--ask-chars
  '''  # line 881
    mrg = getAnyOfMap({"--add": MergeOperation.INSERT, "--rm": MergeOperation.REMOVE, "--ask": MergeOperation.ASK}, options, MergeOperation.BOTH)  # type: MergeOperation  # default operation is replicate remote state  # line 882
    mrgline = getAnyOfMap({'--add-lines': MergeOperation.INSERT, '--rm-lines': MergeOperation.REMOVE, "--ask-lines": MergeOperation.ASK}, options, mrg)  # type: MergeOperation  # default operation for modified files is same as for files  # line 883
    mrgchar = getAnyOfMap({'--add-chars': MergeOperation.INSERT, '--rm-chars': MergeOperation.REMOVE, "--ask-chars": MergeOperation.ASK}, options, mrgline)  # type: MergeOperation  # default operation for modified files is same as for lines  # line 884
    eol = '--eol' in options  # type: bool  # use remote eol style  # line 885
    m = Metadata()  # type: Metadata  # TODO same is called inside stop on changes - could return both current and designated branch instead  # line 886
    currentBranch = m.branch  # type: _coconut.typing.Optional[int]  # line 887
    m, branch, revision, changes_, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(argument, options, check=False, onlys=onlys, excps=excps)  # don't check for current changes, only parse arguments  # line 888
    if verbose:  # line 889
        info(MARKER + "Integrating changes from '%s/r%02d' into file tree..." % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 889

# Determine file changes from other branch over current file tree
    m.computeSequentialPathSet(branch, revision)  # load all commits up to specified revision for branch to integrate  # line 892
    trackingUnion = trackingPatterns | m.getTrackingPatterns(branch)  # type: FrozenSet[str]  # line 893
    untrackingUnion = untrackingPatterns | m.getTrackingPatterns(branch, negative=True)  # type: FrozenSet[str]  # line 894
    changed, _msg = m.findChanges(checkContent=strict, inverse=True, considerOnly=onlys if not (m.track or m.picky) else pure.conditionalIntersection(onlys, trackingUnion), dontConsider=excps if not (m.track or m.picky) else (untrackingUnion if onlys is None else onlys), progress='--progress' in options)  # determine difference of other branch vs. file tree. "addition" means exists now but not in other, and should be removed unless in tracking mode  # line 895
    if mrg != MergeOperation.ASK and not changed.modifications and not (mrg.value & MergeOperation.INSERT.value and changed.additions or (mrg.value & MergeOperation.REMOVE.value and changed.deletions)):  # no file ops, TODO ASK handling is clumsy here  # line 900
        if trackingUnion != trackingPatterns:  # nothing added  # line 901
            info("No file changes detected, but tracking patterns were merged (run 'sos switch /-1 --meta' to undo)")  # TODO write test to see if this works  # line 902
        else:  # line 903
            info("Nothing to update")  # but write back updated branch info below  # line 904
    else:  # integration required  # line 905
        add_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 906
        del_all = None  # type: _coconut.typing.Optional[str]  # user input markers to continue to add/delete all remaining  # line 906
        selection = None  # type: str  # user input markers to continue to add/delete all remaining  # line 906
        if changed.deletions.items():  # line 907
            printo("Additions:")  # line 907
        for path, pinfo in changed.deletions.items():  # file-based update. Deletions mark files not present in current file tree -> needs addition!  # line 908
            selection = "y" if mrg.value & MergeOperation.INSERT.value else "n"  # default for non-ask case  # line 909
            if add_all is None and mrg == MergeOperation.ASK:  # line 910
                selection = user_input("  Restore %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 911
                if selection in "ao":  # line 912
                    add_all = "y" if selection == "a" else "n"  # line 912
                    selection = add_all  # line 912
            if "y" in (add_all, selection):  # deleted in current file tree: restore from branch to reach target  # line 913
                m.restoreFile(path, branch, revision, pinfo, ensurePath=True)  # deleted in current file tree: restore from branch to reach target  # line 913
            printo(("ADD " if "y" in (add_all, selection) else "(A) ") + path, color=Fore.GREEN)  # TODO #268 document merge/update output, e.g. (A) as "selected not to add by user choice"  # line 914
        if changed.additions.items():  # line 915
            printo("Deletions:")  # line 915
        for path, pinfo in changed.additions.items():  # line 916
            if m.track or m.picky:  # because untracked files of other branch cannot be detected (which is good)  # line 917
                Exit("This should never happen. Please create an issue report on Github")  # because untracked files of other branch cannot be detected (which is good)  # line 917
            selection = "y" if mrg.value & MergeOperation.REMOVE.value else "n"  # line 918
            if del_all is None and mrg == MergeOperation.ASK:  # line 919
                selection = user_input("  Delete %r? *[Y]es, [N]o, yes to [A]ll, n[O] to all: " % path, "ynao", "y")  # line 920
                if selection in "ao":  # line 921
                    del_all = "y" if selection == "a" else "n"  # line 921
                    selection = del_all  # line 921
            if "y" in (del_all, selection):  # line 922
                os.unlink(encode(m.root + os.sep + path.replace(SLASH, os.sep)))  # line 922
            printo(("DEL " if "y" in (del_all, selection) else "(D) ") + path, color=Fore.RED)  # not contained in other branch, but maybe kept  # line 923
        if changed.modifications.items():  # line 924
            printo("Modifications:")  # line 924
        for path, pinfo in changed.modifications.items():  # line 925
            into = os.path.normpath(os.path.join(m.root, path.replace(SLASH, os.sep)))  # type: str  # line 926
            binary = not m.isTextType(path)  # type: bool  # line 927
            op = "m"  # type: str  # merge as default for text files, always asks for binary (TODO unless --theirs or --mine)  # line 928
            if mrg == MergeOperation.ASK or binary:  # TODO this may ask user even if no interaction was asked for  # line 929
                printo(("MOD " if not binary else "BIN ") + path, color=Fore.YELLOW)  # TODO print mtime, size differences?  # line 930
                op = user_input("  Resolve %r: *M[I]ne (skip), [T]heirs" % into + (": " if binary else ", [M]erge: "), "it" if binary else "itm", "i")  # line 931
            if op == "t":  # line 932
                printo("THR " + path, color=Fore.MAGENTA)  # blockwise copy of contents  # line 933
                m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash, toFile=into)  # blockwise copy of contents  # line 933
            elif op == "m":  # line 934
                with open(encode(into), "rb") as fd:  # TODO slurps current file  # line 935
                    current = fd.read()  # type: bytes  # TODO slurps current file  # line 935
                file = m.readOrCopyVersionedFile(branch, revision, pinfo.nameHash) if pinfo.size > 0 else b''  # type: _coconut.typing.Optional[bytes]  # slurp versioned file  # line 936
                if current == file and verbose:  # line 937
                    info("No difference to versioned file")  # line 937
                elif file is not None:  # if None, error message was already logged  # line 938
                    merged = None  # type: bytes  # line 939
                    nl = None  # type: bytes  # line 939
                    merged, nl = merge(file=file, into=current, mergeOperation=mrgline, charMergeOperation=mrgchar, eol=eol)  # line 940
                    if merged != into:  # line 941
                        printo("MRG " + path, color=Fore.CYAN)  # line 942
                        with open(encode(into), "wb") as fd:  # TODO write to temp file first, in case writing fails  # line 943
                            fd.write(merged)  # TODO write to temp file first, in case writing fails  # line 943
                    elif verbose:  # TODO but update timestamp?  # line 944
                        info("No change")  # TODO but update timestamp?  # line 944
            else:  # mine or wrong input  # line 945
                printo("MNE " + path, color=Fore.CYAN)  # nothing to do! same as skip  # line 946
    info(MARKER + "Integrated changes from '%s/r%02d' into file tree" % ((lambda _coconut_none_coalesce_item: "b%d" % branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision))  # line 947
    m.branches[currentBranch] = dataCopy(BranchInfo, m.branches[currentBranch], inSync=False, tracked=list(trackingUnion))  # line 948
    m.branch = currentBranch  # need to restore setting before saving TODO operate on different objects instead  # line 949
    m.saveBranches(m._extractRemotesFromArguments(options))  # line 950

def destroy(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 952
    ''' Remove a branch entirely. '''  # line 953
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options)  # line 954
    if len(m.branches) == 1:  # line 955
        Exit("Cannot remove the only remaining branch. Use 'sos online' to leave offline mode")  # line 955
    branch, revision = m.parseRevisionString(argument)  # not from exitOnChanges, because we have to set argument to None there  # line 956
    if branch is None or branch not in m.branches:  # line 957
        Exit("Cannot delete unknown branch %r" % branch)  # line 957
    if verbose:  # line 958
        info(MARKER + "Removing branch b%d%s..." % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name))))  # line 958
    binfo = m.removeBranch(branch, options)  # need to keep a reference to removed entry for output below  # line 959
    info(MARKER + "Branch b%d%s removed" % (branch, " '%s'" % ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(binfo.name))))  # line 960

def add(relPaths: '_coconut.typing.Sequence[str]', patterns: '_coconut.typing.Sequence[str]', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 962
    ''' Add a tracked files pattern to current branch's tracked files. negative means tracking blacklisting. '''  # line 963
    force = '--force' in options  # type: bool  # line 964
    m = Metadata()  # type: Metadata  # line 965
    if not (m.track or m.picky):  # line 966
        Exit("Repository is in simple mode. Create offline repositories via 'sos offline --track' or 'sos offline --picky' or configure a user-wide default via 'sos config track on'")  # line 967
    knownpatterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 968
    for relPath, pattern in zip(relPaths, patterns):  # line 969
        if pattern in knownpatterns:  # line 970
            Exit("Pattern '%s' already tracked" % pattern)  # line 971
        if not force and not os.path.exists(encode(relPath.replace(SLASH, os.sep))):  # line 972
            Exit("The pattern folder doesn't exist. Use --force to add the file pattern anyway")  # line 973
        if not force and len(fnmatch.filter(os.listdir(os.path.abspath(relPath.replace(SLASH, os.sep))), os.path.basename(pattern.replace(SLASH, os.sep)))) == 0:  # doesn't match any current file  # line 974
            Exit("Pattern doesn't match any file in specified folder. Use --force to add it anyway")  # line 975
        knownpatterns.append(pattern)  # line 976
    m.saveBranches(m._extractRemotesFromArguments(options))  # line 977
    info(MARKER + "Added tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern.replace(SLASH, os.sep)), relPath if '--relative' in options else os.path.abspath(relPath)))  # line 978

def remove(relPaths: '_coconut.typing.Sequence[str]', patterns: '_coconut.typing.Sequence[str]', options: '_coconut.typing.Sequence[str]'=[], negative: 'bool'=False):  # line 980
    ''' Remove a tracked files pattern from current branch's tracked files. '''  # line 981
    m = Metadata()  # type: Metadata  # line 982
    if not (m.track or m.picky):  # line 983
        Exit("Repository is in simple mode. Use 'offline --track' or 'offline --picky' to start repository in tracking or picky mode")  # line 984
    knownpatterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 985
    for relPath, pattern in zip(relPaths, patterns):  # line 986
        if pattern not in knownpatterns:  # line 987
            suggestion = _coconut.set()  # type: Set[str]  # line 988
            for pat in knownpatterns:  # line 989
                if fnmatch.fnmatch(pattern, pat):  # line 989
                    suggestion.add(pat)  # line 989
            if suggestion:  # line 990
                printo("Do you mean any of the following tracked file patterns? '%s'" % (", ".join(sorted(suggestion))))  # line 990
            Exit("Tracked pattern '%s' not found" % pattern)  # line 991
    knownpatterns.remove(pattern)  # line 992
    m.saveBranches(m._extractRemotesFromArguments(options))  # line 993
    info(MARKER + "Removed tracking pattern '%s' for folder '%s'" % (os.path.basename(pattern), relPath if '--relative' in options else os.path.abspath(relPath.replace(SLASH, os.sep))))  # line 994

def ls(folder: '_coconut.typing.Optional[str]'=None, options: '_coconut.typing.Sequence[str]'=[]):  # line 996
    ''' List specified directory, augmenting with repository metadata. '''  # line 997
    m = Metadata()  # type: Metadata  # line 998
    folder = (os.getcwd() if folder is None else folder)  # line 999
    if '--all' in options or '-a' in options:  # always start at SOS repo root with --all  # line 1000
        folder = m.root  # always start at SOS repo root with --all  # line 1000
    recursive = '--recursive' in options or '-r' in options or '--all' in options  # type: bool  # line 1001
    patterns = '--patterns' in options or '-p' in options  # type: bool  # line 1002
    DOT = (DOT_SYMBOL if m.c.useUnicodeFont else " ") * 3  # type: str  # TODO or "."?  # line 1003
    if verbose:  # line 1004
        info(MARKER + "Repository is in %s mode" % ("tracking" if m.track else ("picky" if m.picky else "simple")))  # line 1004
    relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # type: str  # line 1005
    if relPath.startswith(os.pardir):  # line 1006
        Exit("Cannot list contents of folder outside offline repository")  # line 1006
    trackingPatterns = m.getTrackingPatterns() if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 1007
    untrackingPatterns = m.getTrackingPatterns(negative=True) if m.track or m.picky else _coconut.frozenset()  # type: _coconut.typing.Optional[FrozenSet[str]]  # for current branch  # line 1008
    if '--tags' in options:  # TODO this has nothing to do with "ls" - it's an entirely different command. Move if something like "sos tag" has been implemented  # line 1009
        if len(m.tags) > 0:  # line 1010
            printo(ajoin("TAG ", sorted(m.tags), nl="\n"))  # line 1010
        return  # line 1011
    for dirpath, dirnames, _filenames in os.walk(folder):  # line 1012
        if not recursive:  # avoid recursion  # line 1013
            dirnames.clear()  # avoid recursion  # line 1013
        dirnames[:] = sorted([decode(d) for d in dirnames])  # line 1014
        dirnames[:] = [d for d in dirnames if len([n for n in m.c.ignoreDirs if fnmatch.fnmatch(d, n)]) == 0 or len([p for p in m.c.ignoreDirsWhitelist if fnmatch.fnmatch(d, p)]) > 0]  # global ignores  # line 1015

        folder = decode(dirpath)  # line 1017
        relPath = relativize(m.root, os.path.join(folder, "-"))[0]  # line 1018
        if patterns:  # line 1019
            out = ajoin("TRK ", [os.path.basename(p) for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath], nl="\n")  # type: str  # line 1020
            if out:  # line 1021
                printo("DIR %s\n" % relPath + out)  # line 1021
            continue  # with next folder  # line 1022
        files = list(sorted((entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry)))))  # type: List[str]  # line 1023
        if len(files) > 0:  # line 1024
            printo("DIR %s" % relPath)  # line 1024
        for file in files:  # for each file list all tracking patterns that match, or none (e.g. in picky mode after commit)  # line 1025
            ignore = None  # type: _coconut.typing.Optional[str]  # line 1026
            for ig in m.c.ignores:  # remember first match  # line 1027
                if fnmatch.fnmatch(file, ig):  # remember first match  # line 1027
                    ignore = ig  # remember first match  # line 1027
                    break  # remember first match  # line 1027
            if ignore:  # found a white list entry for ignored file, undo ignoring it  # line 1028
                for wl in m.c.ignoresWhitelist:  # found a white list entry for ignored file, undo ignoring it  # line 1028
                    if fnmatch.fnmatch(file, wl):  # found a white list entry for ignored file, undo ignoring it  # line 1028
                        ignore = None  # found a white list entry for ignored file, undo ignoring it  # line 1028
                        break  # found a white list entry for ignored file, undo ignoring it  # line 1028
            matches = []  # type: List[str]  # line 1029
            if not ignore:  # line 1030
                for pattern in (p for p in trackingPatterns if os.path.dirname(p).replace(os.sep, SLASH) == relPath):  # only patterns matching current folder  # line 1031
                    if fnmatch.fnmatch(file, os.path.basename(pattern)):  # line 1032
                        matches.append(os.path.basename(pattern))  # line 1032
            matches.sort(key=lambda element: len(element))  # sort in-place  # line 1033
            printo("%s %s%s" % ("IGN" if ignore is not None else ("TRK" if len(matches) > 0 else DOT), file, "  (%s)" % ignore if ignore is not None else ("  (%s)" % ("; ".join(matches)) if len(matches) > 0 else "")))  # line 1034

def log(options: '_coconut.typing.Sequence[str]'=[], cwd: '_coconut.typing.Optional[str]'=None):  # line 1036
    ''' List previous commits on current branch. '''  # line 1037
    changes_ = "--changes" in options  # type: bool  # line 1038
    diff_ = "--diff" in options  # type: bool  # line 1039
    only_add = "--only-adds" in options  # type: bool  # line 1040
    only_del = "--only-dels" in options  # type: bool  # line 1041
    only_mod = "--only-mods" in options  # type: bool  # line 1042
    only_mov = "--only-movs" in options  # type: bool  # line 1043
    if not (only_add or only_del or only_mod or only_mov):  # line 1044
        only_add = only_del = only_mod = only_mov = True  # line 1044
    m = Metadata()  # type: Metadata  # line 1045
    m.loadBranch(m.branch)  # knows commit history  # line 1046
    number_ = tryOrDefault(lambda _=None: max(1, int(sys.argv[sys.argv.index("-n") + 1])), m.c.logLines)  # type: _coconut.typing.Optional[int]  # WARN only works because we don't pick a positional argument in parse  # line 1047
    maxi = max(m.commits) if m.commits else m.branches[m.branch].revision  # type: int  # one commit guaranteed for first offline branch, for fast-branched branches a revision in branchinfo  # line 1048
    info((lambda _coconut_none_coalesce_item: "r%02d" % m.branch if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(MARKER + "Offline commit history of branch %r" % m.branches[m.branch].name))  # TODO also retain info of "from branch/revision" on branching?  # line 1049
    nl = len("%d" % maxi)  # type: int  # determine space needed for revision  # line 1050
    changesetIterator = m.computeSequentialPathSetIterator(m.branch, maxi)  # type: _coconut.typing.Optional[Iterator[Dict[str, PathInfo]]]  # line 1051
    olds = _coconut.frozenset()  # type: FrozenSet[str]  # last revision's entries  # line 1052
    last = {}  # type: Dict[str, PathInfo]  # path infos from previous revision  # line 1053
    n = Metadata()  # type: Metadata  # used for reading parent branch information  # line 1054
    commit = None  # type: CommitInfo  # used for reading parent branch information  # line 1054
    indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if '--all' not in options and maxi > number_ else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1055
    digits = pure.requiredDecimalDigits(maxi) if indicator else None  # type: _coconut.typing.Optional[int]  # line 1056
    lastno = max(0, maxi + 1 - number_)  # type: int  # line 1057
    for no in range(maxi + 1):  # line 1058
        if indicator:  # line 1059
            printo("  %%s %%0%dd" % digits % ((lambda _coconut_none_coalesce_item: " " if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(indicator.getIndicator()), no), nl="\r")  # line 1059
        if no in m.commits:  # line 1060
            commit = m.commits[no]  # line 1060
        else:  # line 1061
            if n.branch != n.getParentBranch(m.branch, no):  # line 1062
                n.loadBranch(n.getParentBranch(m.branch, no))  # line 1062
            commit = n.commits[no]  # line 1063
        nxts = next(changesetIterator)  # type: Dict[str, PathInfo]  # line 1064
        news = frozenset(nxts.keys())  # type: FrozenSet[str]  # line 1065
        if "--all" in options or no >= lastno:  # line 1066
            if no >= lastno:  # line 1067
                indicator = None  # line 1067
            _add = news - olds  # type: FrozenSet[str]  # line 1068
            _del = olds - news  # type: FrozenSet[str]  # line 1069
#    _mod_:Dict[str,PathInfo] = {k: nxts[k] for k in news - _add - _del}
            _mod = frozenset([_ for _, info in {k: nxts[k] for k in news - _add - _del}.items() if last[_].size != info.size or (last[_].hash != info.hash if m.strict else last[_].mtime != info.mtime)])  # type: FrozenSet[str]  # line 1071
#    _mov:FrozenSet[str] = detectMoves(ChangeSet(nxts, {o: None for o in olds}, m.strict)  # TODO determine moves - can we reuse detectMoves(changes)?
            _txt = len([m_ for m_ in _mod if m.isTextType(m_)])  # type: int  # line 1073
            printo("  %s r%s @%s (%s+%s%02d/%s-%s%02d/%s%s%s%02d/%sT%s%02d) |%s|%s%s%s" % ((ARROW_SYMBOL if m.c.useUnicodeFont else "*") if commit.number == maxi else " ", ("%%%ds" % nl) % commit.number, strftime(commit.ctime), Fore.GREEN, Fore.RESET, len(_add), Fore.RED, Fore.RESET, len(_del), Fore.YELLOW, CHANGED_SYMBOL if m.c.useUnicodeFont else "~", Fore.RESET, len(_mod), Fore.CYAN, Fore.RESET, _txt, (lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message), Fore.MAGENTA, "TAG" if ((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(commit.message)) in m.tags else "", Fore.RESET))  # line 1074
            if changes_:  # line 1075
                m.listChanges(ChangeSet({a: None for a in _add} if only_add else {}, {d: None for d in _del} if only_del else {}, {m: None for m in _mod} if only_mod else {}, {}), root=cwd if '--relative' in options else None)  # TODO why using None here? to avoid stating files for performance reasons?  # line 1086
            if diff_:  #  _diff(m, changes)  # needs from revision diff  # line 1087
                pass  #  _diff(m, changes)  # needs from revision diff  # line 1087
        olds = news  # replaces olds for next revision compare  # line 1088
        last = {k: v for k, v in nxts.items()}  # create new reference  # line 1089

def dump(argument: 'str', options: '_coconut.typing.Sequence[str]'=[]):  # line 1091
    ''' Exported entire repository as archive for easy transfer. '''  # line 1092
    if verbose:  # line 1093
        info(MARKER + "Dumping repository to archive...")  # line 1093
    m = Metadata()  # type: Metadata  # to load the configuration  # line 1094
    progress = '--progress' in options  # type: bool  # line 1095
    delta = '--full' not in options  # type: bool  # line 1096
    skipBackup = '--skip-backup' in options  # type: bool  # line 1097
    import functools  # line 1098
    import locale  # line 1098
    import warnings  # line 1098
    import zipfile  # line 1098
    try:  # HINT zlib is the library that contains the deflated algorithm  # line 1099
        import zlib  # HINT zlib is the library that contains the deflated algorithm  # line 1099
        compression = zipfile.ZIP_DEFLATED  # HINT zlib is the library that contains the deflated algorithm  # line 1099
    except:  # line 1100
        compression = zipfile.ZIP_STORED  # line 1100

    if ("" if argument is None else argument) == "":  # line 1102
        Exit("Argument missing (target filename)")  # line 1102
    argument = argument if "." in argument else argument + DUMP_FILE  # TODO this logic lacks a bit, "v1.2" would not receive the suffix  # line 1103
    entries = []  # type: List[str]  # line 1104
    if os.path.exists(encode(argument)) and not skipBackup:  # line 1105
        try:  # line 1106
            if verbose:  # line 1107
                info("Creating backup...")  # line 1107
            shutil.copy2(encode(argument), encode(argument + BACKUP_SUFFIX))  # line 1108
            if delta:  # list of pure relative paths without leading dot, normal slashes  # line 1109
                with zipfile.ZipFile(argument, "r") as _zip:  # list of pure relative paths without leading dot, normal slashes  # line 1109
                    entries = _zip.namelist()  # list of pure relative paths without leading dot, normal slashes  # line 1109
        except Exception as E:  # line 1110
            Exit("Error creating backup copy before dumping. Please resolve and retry.", excp=E)  # line 1110
    if verbose:  # line 1111
        info("Dumping revisions...")  # line 1111
    if delta:  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1112
        warnings.filterwarnings('ignore', 'Duplicate name.*')  # , UserWarning, "zipfile", 0)  # don't show duplicate entries warnings  # line 1112
    with zipfile.ZipFile(argument, "a" if delta else "w", compression) as _zip:  # create  # line 1113
        _zip.debug = 0  # suppress debugging output  # line 1114
        _zip.comment = ("Repository dump from %r" % strftime()).encode(UTF8)  # line 1115
        repopath = os.path.join(os.getcwd(), metaFolder)  # type: str  # line 1116
        indicator = ProgressIndicator(PROGRESS_MARKER[1 if m.c.useUnicodeFont else 0]) if progress else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 1117
        totalsize = 0  # type: int  # line 1118
        start_time = time.time()  # type: float  # line 1119
        for dirpath, dirnames, filenames in os.walk(repopath):  # TODO use index knowledge instead of walking to avoid adding stuff not needed?  # line 1120
            dirpath = decode(dirpath)  # line 1121
            if dirpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1122
                continue  # don't backup backups  # line 1122
            printo(pure.ljust(dirpath))  # TODO improve progress indicator output to | dir | dumpuing file  # line 1123
            dirnames[:] = sorted([decode(d) for d in dirnames], key=functools.cmp_to_key(lambda a, b: tryOrDefault(lambda: locale.strcoll("%8d" % int(a[1:]), "%8d" % int(b[1:])), locale.strcoll(a, b))))  # HINT sort for reproducible delta dumps  # line 1124
            filenames[:] = sorted([decode(f) for f in filenames])  # line 1125
            for filename in filenames:  # line 1126
                abspath = os.path.join(dirpath, filename)  # type: str  # line 1127
                relpath = os.path.join(metaFolder, os.path.relpath(abspath, repopath)).replace(os.sep, "/")  # type: str  # line 1128
                totalsize += os.stat(encode(abspath)).st_size  # line 1129
                show = indicator.getIndicator() if progress else None  # type: _coconut.typing.Optional[str]  # line 1130
                if relpath.endswith(BACKUP_SUFFIX):  # don't backup backups  # line 1131
                    continue  # don't backup backups  # line 1131
                if not delta or relpath.endswith(metaFile) or relpath not in entries:  # always update metadata, otherwise only add new revision files  # line 1132
                    if show:  # line 1133
                        printo("\r" + pure.ljust("Dumping %s @%.2f MiB/s %s" % (show, totalsize / (MEBI * (time.time() - start_time)), filename)), nl="")  # line 1133
                    _zip.write(abspath, relpath)  # write entry into archive  # line 1134
        if delta:  # line 1135
            _zip.comment = ("Delta dump from %r" % strftime()).encode(UTF8)  # line 1135
    info("\r" + pure.ljust(MARKER + "Finished dumping %s repository @%.2f MiB/s." % ("differential" if delta else "entire", totalsize / (MEBI * (time.time() - start_time)))))  # clean line  # line 1136

def publish(message: '_coconut.typing.Optional[str]', cmd: 'str', options: '_coconut.typing.Sequence[str]'=[], onlys: '_coconut.typing.Optional[FrozenSet[str]]'=None, excps: '_coconut.typing.Optional[FrozenSet[str]]'=None):  # line 1138
    ''' Write changes made to the branch into one commit of the underlying VCS without further checks. '''  # line 1139
    m = Metadata()  # type: Metadata  # TODO SOS only commit whats different from VCS state?  # line 1140
    if not (m.track or m.picky):  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1141
        Exit("Not implemented for simple repository mode yet")  # TODO add manual file picking mode instead (add by extension, recursive, ... see issue for details)  # line 1141
    m, branch, revision, changed, strict, force, trackingPatterns, untrackingPatterns = exitOnChanges(None, options, onlys=onlys, excps=excps)  # line 1142
    maxi = m.getHighestRevision(branch)  # type: _coconut.typing.Optional[int]  # line 1143
    if maxi is None:  # line 1144
        Exit("No revision to publish on current branch (or any of its parents after fast-branching)")  # line 1144
    m.computeSequentialPathSet(branch, maxi, startwith=1 if maxi >= 1 and not '--all' in options and not (m.track or m.picky) else 0)  # load all commits up to specified revision  # line 1145
# HINT logic to only add changed files vs. originating file state - would require in-depth underlying VCS knowledge. We currentöy assume commit 0 as base
# TODO discuss: only commit changes from r1.. onward vs. r0?, or attempt to add everything in repo, even if unchanged? the problem is that for different branches we might need to switch also underlying branches
    import subprocess  # only required in this section  # line 1148
# HINT stash/rollback for Git? or implement a global mechanism to revert?
    files = list(m.paths.keys())  # type: _coconut.typing.Sequence[str]  # line 1150
    while files:  # line 1151
        command = fitStrings(files, prefix="%s add" % cmd, process=lambda _=None: '"%s"' % _.replace("\"", "\\\""))  # type: str  # considering maximum command-line length, filename quoting, and spaces  # line 1152
        returncode = subprocess.Popen(command, shell=False).wait()  # type: int  # line 1153
#    returncode:int = 0; debug(command)
        if returncode != 0:  # line 1155
            Exit("Error adding files from SOS revision to underlying VCS. Leaving %s in potentially inconsistent state" % vcsNames[cmd])  # line 1155
    tracked = None  # type: bool  # line 1156
    commitArgs = None  # type: _coconut.typing.Optional[str]  # line 1156
    tracked, commitArgs = vcsCommits[cmd]  # line 1156
    returncode = subprocess.Popen(('%s commit -m "%s" %s' % (cmd, (("Committed from SOS %s/r%02d on %s" % ((lambda _coconut_none_coalesce_item: ("b%d" % m.branch) if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(m.branches[branch].name), revision, strftime())).replace("\"", "\\\"") if message is None else message), ("" if commitArgs is None else commitArgs))))  # TODO quote-escaping on Windows  # line 1157
#  debug(('%s commit -m "%s" %s' % (cmd, message ?? ("Committed from SOS %s/r%02d on %s" % (m.branches[branch].name ?? ("b%d" % m.branch), revision, strftime())).replace("\"", "\\\""), commitArgs ?? "")))
    if returncode != 0:  # line 1159
        Exit("Error committing files from SOS revision to underlying VCS. Please check current %s state" % cmd)  # line 1159
    if tracked:  # line 1160
        warn("Please note that all the files added in this commit will continue to be tracked by the underlying VCS")  # line 1160
    m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed to underlying  # line 1161
    m.saveBranches()  # line 1162

def config(arguments: 'List[_coconut.typing.Optional[str]]', options: 'List[str]'=[]):  # line 1164
    ''' Configure command: manage configuration settings. '''  # line 1165
    command = None  # type: str  # line 1166
    key = None  # type: str  # line 1166
    value = None  # type: str  # line 1166
    v = None  # type: str  # line 1166
    command, key, value = (arguments + [None] * 2)[:3]  # line 1167
    if command is None:  # TODO or "config"?  # line 1168
        usage.usage("help", verbose=True)  # TODO or "config"?  # line 1168
    if command not in ("set", "unset", "show", "list", "add", "rm"):  # line 1169
        Exit("Unknown config command %r" % command)  # line 1169
    local = "--local" in options  # type: bool  # otherwise user-global by default  # line 1170
    m = Metadata()  # type: Metadata  # loads nested configuration (local - global - defaults)  # line 1171
    c = m.c if local else m.c.__defaults  # type: configr.Configr  # will only modify the selected parameter set  # line 1172
    location = "local" if local else "global"  # type: str  # line 1173
    if command == "set":  # line 1174
        if None in (key, value):  # line 1175
            Exit("Key or value not specified")  # line 1175
        if key not in ((([] if local else ONLY_GLOBAL_FLAGS) + CONFIGURABLE_FLAGS + ["defaultbranch"]) + CONFIGURABLE_LISTS + CONFIGURABLE_INTS):  # TODO move defaultbranch to configurable_texts?  # line 1176
            Exit("Unsupported key for %s configuration %r" % (location, key))  # TODO move defaultbranch to configurable_texts?  # line 1176
        if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) and value.lower() not in TRUTH_VALUES + FALSE_VALUES:  # line 1177
            Exit("Cannot set flag to %r. Try 'on' or 'off' instead" % value.lower())  # line 1177
        c[key] = value.lower() in TRUTH_VALUES if key in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS) else (tryOrIgnore(lambda _=None: int(value), lambda E: error("Not an integer value: %r" % E)) if key in CONFIGURABLE_INTS else (removePath(key, value.strip()) if key not in CONFIGURABLE_LISTS else [removePath(key, v) for v in safeSplit(value, ";")]))  # TODO sanitize texts?  # line 1178
    elif command == "unset":  # line 1179
        if key is None:  # line 1180
            Exit("No key specified")  # line 1180
        if key not in c.keys(with_nested=False):  # line 1181
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, location))  # line 1182
        del c[key]  # line 1183
    elif command == "add":  # TODO copy list from defaults if not local/global  # line 1184
        if None in (key, value):  # line 1185
            Exit("Key or value not specified")  # line 1185
        if key not in CONFIGURABLE_LISTS:  # line 1186
            Exit("Unsupported key %r for list addition" % key)  # line 1186
        if key not in c.keys():  # prepare empty list, or copy from underlying, add new value below TODO also allow one more level of underlying?  # line 1187
            c[key] = [_ for _ in c.__defaults[key]] if key in c.__defaults[key] else []  # prepare empty list, or copy from underlying, add new value below TODO also allow one more level of underlying?  # line 1187
        elif value in c[key]:  # line 1188
            Exit("Value already contained, nothing to do")  # line 1188
        if ";" not in value:  # line 1189
            c[key].append(removePath(key, value.strip()))  # line 1189
        else:  # line 1190
            c[key].extend([removePath(key, v) for v in safeSplit(value, ";")])  # line 1190
    elif command == "rm":  # line 1191
        if None in (key, value):  # line 1192
            Exit("Key or value not specified")  # line 1192
        if key not in c.keys(with_nested=False):  # line 1193
            Exit(("Unknown key %r" % key) if not key in c.keys(with_nested=local, with_defaults=True) else "Key %r not defined in %s scope" % (key, location))  # line 1194
        if value not in c[key]:  # line 1195
            Exit("Unknown value %r" % value)  # line 1195
        c[key].remove(value)  # line 1196
        if local and len(c[key]) == 0 and "--prune" in options:  # remove local entry, to fallback to global  # line 1197
            del c[key]  # remove local entry, to fallback to global  # line 1197
    else:  # Show or list  # line 1198
        if key == "ints":  # list valid configuration items  # line 1199
            printo(", ".join(CONFIGURABLE_INTS))  # list valid configuration items  # line 1199
        elif key == "flags":  # line 1200
            printo(", ".join(ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS))  # line 1200
        elif key == "lists":  # line 1201
            printo(", ".join(CONFIGURABLE_LISTS))  # line 1201
        elif key == "texts":  # line 1202
            printo(", ".join([_ for _ in defaults.keys() if _ not in (ONLY_GLOBAL_FLAGS + CONFIGURABLE_FLAGS + CONFIGURABLE_INTS + CONFIGURABLE_LISTS)]))  # line 1202
        else:  # no key: list all  # line 1203
            out = {3: "[default]", 2: "[global] ", 1: "[local]  "}  # type: Dict[int, str]  # in contrast to Git, we don't need (nor want) to support a "system" config scope  # line 1204
            c = m.c  # always use full configuration chain  # line 1205
            try:  # attempt single key  # line 1206
                assert key is not None  # force exception if no key specified  # line 1207
                c[key]  # force exception if no key specified  # line 1207
                l = key in c.keys(with_nested=False)  # type: bool  # line 1208
                g = key in c.__defaults.keys(with_nested=False)  # type: bool  # line 1208
                printo(key.rjust(20), color=Fore.WHITE, nl="")  # line 1209
                printo(" " + (out[3] if not (l or g) else (out[1] if l else out[2])) + " ", color=Fore.CYAN, nl="")  # line 1210
                printo(repr(c[key]))  # line 1211
            except:  # normal value listing  # line 1212
                vals = {k: (repr(v), 3) for k, v in defaults.items()}  # type: Dict[str, Tuple[str, int]]  # copy-by-value  # line 1213
                vals.update({k: (repr(v), 2) for k, v in c.__defaults.items()})  # line 1214
                vals.update({k: (repr(v), 1) for k, v in c.__map.items()})  # line 1215
                for k, vt in sorted(vals.items()):  # line 1216
                    printo(k.rjust(20), color=Fore.WHITE, nl="")  # line 1217
                    printo(" " + out[vt[1]] + " ", color=Fore.CYAN, nl="")  # line 1218
                    printo(vt[0])  # line 1219
                if len(c.keys()) == 0:  # line 1220
                    info("No local configuration stored.")  # line 1220
                if len(c.__defaults.keys()) == 0:  # line 1221
                    info("No global configuration stored.")  # line 1221
        return  # in case of list, no need to store anything  # line 1222
    if local:  # saves changes of repoConfig  # line 1223
        m.repoConf = c.__map  # saves changes of repoConfig  # line 1223
        m.saveBranches(m._extractRemotesFromArguments(options))  # saves changes of repoConfig  # line 1223
        Exit("OK", code=0)  # saves changes of repoConfig  # line 1223
    else:  # global config  # line 1224
        f, h = saveConfig(c)  # only saves c.__defaults (nested Configr)  # line 1225
        if f is None:  # line 1226
            Exit("Error saving user configuration: %r" % h)  # line 1226

def move(relPath: 'str', pattern: 'str', newRelPath: 'str', newPattern: 'str', options: 'List[str]'=[], negative: 'bool'=False):  # line 1228
    ''' Path differs: Move files, create folder if not existing. Pattern differs: Attempt to rename file, unless exists in target or not unique.
      for "mvnot" don't do any renaming (or do?)
  '''  # line 1231
    if verbose:  # line 1232
        info(MARKER + "Renaming %r to %r" % (pattern, newPattern))  # line 1232
    force = '--force' in options  # type: bool  # line 1233
    soft = '--soft' in options  # type: bool  # line 1234
    if not os.path.exists(encode(relPath.replace(SLASH, os.sep))) and not force:  # line 1235
        Exit("Source folder doesn't exist. Use --force to proceed anyway")  # line 1235
    m = Metadata()  # type: Metadata  # line 1236
    patterns = m.branches[m.branch].untracked if negative else m.branches[m.branch].tracked  # type: List[str]  # line 1237
    files = os.listdir(relPath.replace(SLASH, os.sep)) if os.path.exists(encode(relPath.replace(SLASH, os.sep))) else []  # type: List[str]  # line 1238
    files[:] = [f for f in files if len([n for n in m.c.ignores if fnmatch.fnmatch(f, n)]) == 0 or len([p for p in m.c.ignoresWhitelist if fnmatch.fnmatch(f, p)]) > 0]  # line 1239
    matching = fnmatch.filter(files, os.path.basename(pattern))  # type: List[str]  # find matching files in source  # line 1240
    if not matching and not force:  # line 1241
        Exit("No files match the specified file pattern. Use --force to proceed anyway")  # line 1241
    if not (m.track or m.picky):  # line 1242
        Exit("Repository is in simple mode. Use basic file operations to modify files, then execute 'sos commit' to version any changes")  # line 1242
    if pattern not in patterns:  # list potential alternatives and exit  # line 1243
        for tracked in (t for t in patterns if t[:t.rindex(SLASH)] == relPath):  # for all patterns of the same source folder HINT was os.path.dirpath before  # line 1244
            alternative = fnmatch.filter(files, os.path.basename(tracked))  # type: _coconut.typing.Sequence[str]  # find if it matches any of the files in the source folder, too  # line 1245
            if alternative:  # line 1246
                info("  '%s' matches %d file%s" % (tracked, len(alternative), "s" if len(alternative) > 1 else ""))  # line 1246
        Exit("File pattern '%s' is not tracked on current branch. 'sos move' only works on tracked patterns" % pattern)  # HINT removed: "if not (force or soft):""  # line 1247
    basePattern = os.path.basename(pattern)  # type: str  # pure glob without folder  # line 1248
    newBasePattern = os.path.basename(newPattern)  # type: str  # line 1249
    if basePattern.count("*") < newBasePattern.count("*") or (basePattern.count("?") - basePattern.count("[?]")) < (newBasePattern.count("?") - newBasePattern.count("[?]")) or (basePattern.count("[") - basePattern.count("\\[")) < (newBasePattern.count("[") - newBasePattern.count("\\[")) or (basePattern.count("]") - basePattern.count("\\]")) < (newBasePattern.count("]") - newBasePattern.count("\\]")):  # line 1250
        Exit("Glob markers from '%s' to '%s' don't match, cannot move/rename tracked matching file(s)" % (basePattern, newBasePattern))  # line 1254
#  oldTokens:GlobBlock[]?; newToken:GlobBlock[]?  # TODO remove optional?, only here to satisfy mypy
    oldTokens, newTokens = tokenizeGlobPatterns(os.path.basename(pattern), os.path.basename(newPattern))  # line 1256
    matches = convertGlobFiles(matching, oldTokens, newTokens)  # type: _coconut.typing.Sequence[Tuple[str, str]]  # computes list of source - target filename pairs  # line 1257
    if len({st[1] for st in matches}) != len(matches):  # line 1258
        Exit("Some target filenames are not unique and different move/rename actions would point to the same target file")  # line 1258
    matches = reorderRenameActions(matches, exitOnConflict=not soft)  # attempts to find conflict-free renaming order, or exits  # line 1259
    if os.path.exists(encode(newRelPath)):  # line 1260
        exists = [filename[1] for filename in matches if os.path.exists(encode(os.path.join(newRelPath, filename[1]).replace(SLASH, os.sep)))]  # type: _coconut.typing.Sequence[str]  # line 1261
        if exists and not (force or soft):  # line 1262
            Exit("%s files would write over existing files in %s cases. Use --force to execute it anyway" % ("Moving" if relPath != newRelPath else "Renaming", "all" if len(exists) == len(matches) else "some"))  # line 1262
    else:  # line 1263
        os.makedirs(encode(os.path.abspath(newRelPath.replace(SLASH, os.sep))))  # line 1263
    if not soft:  # perform actual renaming  # line 1264
        for (source, target) in matches:  # line 1265
            try:  # line 1266
                shutil.move(encode(os.path.abspath(os.path.join(relPath, source).replace(SLASH, os.sep))), encode(os.path.abspath(os.path.join(newRelPath, target).replace(SLASH, os.sep))))  # line 1266
            except Exception as E:  # one error can lead to another in case of delicate renaming order  # line 1267
                error("Cannot move/rename file '%s' to '%s'" % (source, os.path.join(newRelPath, target)))  # one error can lead to another in case of delicate renaming order  # line 1267
    patterns[patterns.index(pattern)] = newPattern  # line 1268
    m.saveBranches(m._extractRemotesFromArguments(options))  # line 1269

def parse(vcs: 'str', cwd: 'str', cmd: 'str'):  # line 1271
    ''' Main operation. root is underlying VCS base dir. main() has already chdir'ed into SOS root folder, cwd is original working directory for add, rm, mv. '''  # line 1272
    debug("Parsing command-line arguments...")  # line 1273
    root = os.getcwd()  # line 1274
    try:  # line 1275
        onlys, excps, remotes, noremotes = parseArgumentOptions(cwd, sys.argv)  # extracts folder-relative paths (used in changes, commit, diff, switch, update)  # line 1276
        command = sys.argv[1].strip() if len(sys.argv) > 1 else ""  # line 1277
        arguments = [c.strip() for c in sys.argv[2:] if not ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # line 1278
        options = [c.strip() for c in sys.argv[2:] if ((len(c) == 2 and c.startswith("-")) or (len(c) > 2 and c[1] == "-"))]  # type: List[str]  # options *with* arguments have to be parsed directly from sys.argv inside using functions  # line 1279
        debug("Processing command %r with arguments %r and options %r." % (command, [_ for _ in arguments if _ is not None], options))  # line 1280
        if command[:1] in "amr":  # line 1281
            try:  # line 1282
                relPaths, patterns = unzip([relativize(root, os.path.join(cwd, argument)) for argument in ((["."] if arguments is None else arguments))])  # line 1282
            except:  # line 1283
                command = "ls"  # convert command into ls --patterns  # line 1284
                arguments[0] = None  # convert command into ls --patterns  # line 1284
                options.extend(["--patterns", "--all"])  # convert command into ls --patterns  # line 1284
# Exit("Need one or more file patterns as argument (escape them according to your shell)")
        if command[:1] == "m":  # line 1286
            if len(arguments) < 2:  # line 1287
                Exit("Need a second file pattern argument as target for move command")  # line 1287
            newRelPath, newPattern = relativize(root, os.path.join(cwd, arguments[1]))  # line 1288
        arguments[:] = (arguments + [None] * 3)[:3]  # line 1289
        if command == "raise":  # line 1290
            raise Exception("provoked exception")  # line 1290
        elif command[:1] == "a":  # e.g. addnot  # line 1291
            add(relPaths, patterns, options, negative="n" in command)  # e.g. addnot  # line 1291
        elif command[:1] == "b":  # line 1292
            branch(arguments[0], arguments[1], options)  # line 1292
        elif command[:2] == "ch":  # "changes" (legacy)  # line 1293
            changes(arguments[0], options, onlys, excps, cwd)  # "changes" (legacy)  # line 1293
        elif command[:2] == "ci":  # line 1294
            commit(arguments[0], options, onlys, excps)  # line 1294
        elif command[:3] == "com":  # line 1295
            commit(arguments[0], options, onlys, excps)  # line 1295
        elif command[:3] == 'con':  # line 1296
            config(arguments, options)  # line 1296
        elif command[:2] == "de":  # line 1297
            destroy((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1297
        elif command[:2] == "di":  # TODO no consistent handling of single dash/characters argument-options  # line 1298
            diff((lambda _coconut_none_coalesce_item: "/" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[2 if arguments[0] == '-n' else 0]), options, onlys, excps)  # TODO no consistent handling of single dash/characters argument-options  # line 1298
        elif command[:2] == "du":  # line 1299
            dump((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options)  # line 1299
        elif command[:1] == "h":  # line 1300
            usage.usage(arguments[0], verbose=verbose)  # line 1300
        elif command[:2] == "lo":  # line 1301
            log(options, cwd)  # line 1301
        elif command[:2] == "li":  # line 1302
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1302
        elif command[:2] == "ls":  # line 1303
            ls(os.path.relpath((lambda _coconut_none_coalesce_item: cwd if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), root), options)  # line 1303
        elif command[:1] == "m":  # e.g. mvnot  # line 1304
            move(relPaths[0], patterns[0], newRelPath, newPattern, options, negative="n" in command)  # e.g. mvnot  # line 1304
        elif command[:2] == "of":  # line 1305
            offline(arguments[0], arguments[1], options, remotes)  # line 1305
        elif command[:2] == "on":  # line 1306
            online(options)  # line 1306
        elif command[:1] == "p":  # line 1307
            publish(arguments[0], cmd, options, onlys, excps)  # line 1307
        elif command[:1] == "r":  # e.g. rmnot  # line 1308
            remove(relPaths, patterns, options, negative="n" in command)  # e.g. rmnot  # line 1308
        elif command[:2] == "st":  # line 1309
            status(arguments[0], vcs, cmd, options, onlys, excps)  # line 1309
        elif command[:2] == "sw":  # line 1310
            switch((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps, cwd)  # line 1310
        elif command[:1] == "u":  # line 1311
            update((lambda _coconut_none_coalesce_item: "" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(arguments[0]), options, onlys, excps)  # line 1311
        elif command[:1] == "v":  # line 1312
            usage.usage(arguments[0], version=True)  # line 1312
        else:  # line 1313
            Exit("Unknown command '%s'" % command)  # line 1313
        Exit(code=0)  # regular exit  # line 1314
    except (Exception, RuntimeError) as E:  # line 1315
        Exit("An internal error occurred in SOS\nPlease report above message to the project maintainer at  https://github.com/ArneBachmann/sos/issues  via 'New Issue'.\nPlease state your installed version via 'sos version', what you were doing, and the full error message and/or output.", excp=E)  # line 1316

def main():  # line 1318
    global debug, info, warn, error  # to modify logger  # line 1319
    logging.basicConfig(level=level, stream=sys.stderr, format=("%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s"))  # line 1320
    _log = Logger(logging.getLogger(__name__))  # line 1321
    debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1321
    for option in (o for o in ['--log', '--debug', '--verbose', '-v', '--sos', '--vcs'] if o in sys.argv):  # clean up program arguments  # line 1322
        sys.argv.remove(option)  # clean up program arguments  # line 1322
    if '--help' in sys.argv or len(sys.argv) < 2:  # line 1323
        usage.usage(sys.argv[sys.argv.index('--help') + 1] if '--help' in sys.argv and len(sys.argv) > sys.argv.index('--help') + 1 else None, verbose=verbose)  # line 1323
    command = sys.argv[1] if len(sys.argv) > 1 else None  # type: _coconut.typing.Optional[str]  # line 1324
    root, vcs, cmd = findSosVcsBase()  # root is None if no .sos folder exists up the folder tree (=still working online); vcs is checkout/repo root folder; cmd is the VCS base command  # line 1325
    debug("Detected SOS root folder: %s" % (("-" if root is None else root)))  # line 1326
    debug("Detected VCS root folder: %s" % (("-" if vcs is None else vcs)))  # line 1327
    defaults["defaultbranch"] = (lambda _coconut_none_coalesce_item: "default" if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(vcsBranches.get(cmd, vcsBranches[SVN]))  # sets dynamic default with SVN fallback  # line 1328
    defaults["useChangesCommand"] = cmd == "fossil"  # sets dynamic default with SVN fallback  # line 1329
    if (not force_vcs or force_sos) and (root is not None or (("" if command is None else command))[:2] == "of" or (("_" if command is None else command))[:1] in "hv") or force_sos and (root is not None or (("" if command is None else command))[:3] == "con"):  # in offline mode or just going offline  # line 1330
        cwd = os.getcwd()  # line 1332
        os.chdir(cwd if command[:2] == "of" else (cwd if root is None else root))  # line 1333
        parse(vcs, cwd, cmd)  # line 1334
    elif force_vcs or cmd is not None:  # online mode - delegate to VCS  # line 1335
        info("%s: Running '%s %s'" % (usage.COMMAND.upper(), cmd, " ".join(sys.argv[1:])))  # line 1336
        import subprocess  # only required in this section  # line 1337
        process = subprocess.Popen([cmd] + sys.argv[1:], shell=False, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)  # line 1338
        inp = ""  # type: str  # line 1339
        while True:  # line 1340
            so, se = process.communicate(input=inp)  # line 1341
            if process.returncode is not None:  # line 1342
                break  # line 1342
            inp = sys.stdin.read()  # line 1343
        if sys.argv[1][:2] == "co" and process.returncode == 0:  # successful commit to underlying VCS - assume now in sync again (but leave meta data folder with potential other feature branches behind until "online")  # line 1344
            if root is None:  # line 1345
                Exit("Cannot determine SOS root folder: Not working offline, thus unable to mark offline repository as synchronized")  # line 1345
            m = Metadata(root)  # type: Metadata  # line 1346
            m.branches[m.branch] = dataCopy(BranchInfo, m.branches[m.branch], inSync=True)  # mark as committed  # line 1347
            m.saveBranches()  # line 1348
    else:  # line 1349
        Exit("No offline repository present, and unable to detect VCS file tree")  # line 1349


# Main part
force_sos = [None] if '--sos' in sys.argv else []  # type: List[None]  # this is a trick allowing to modify the module-level flags from the test suite  # line 1353
force_vcs = [None] if '--vcs' in sys.argv else []  # type: List[None]  # line 1354
level = logging.DEBUG if '--debug' in sys.argv else logging.INFO  # type: int  # line 1355

_log = Logger(logging.getLogger(__name__))  # line 1357
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 1357

if __name__ == '__main__':  # line 1359
    main()  # line 1359
