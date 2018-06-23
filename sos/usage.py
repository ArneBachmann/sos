#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x2e5eefa9

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

import enum  # line 1
sys = _coconut_sys  # line 1
from typing import Dict  # line 2
from typing import List  # line 2
from typing import Tuple  # line 2
import pure  # line 3
try:  # line 4
    from sos import version  # line 4
except:  # line 5
    import version  # line 5
try:  # line 6
    from pyfiglet import Figlet  # line 6
except:  # optional dependency  # line 7
    Figlet = None  # optional dependency  # line 7

# Constants
APP = "Subversion Offline Solution"  # type: str  # line 10
APPNAME = APP + " V%s (C) Arne Bachmann" % version.__release_version__  # type: str  # line 11
VERSION = version.__version__  # type: str  # line 12
COMMAND = "sos"  # type: str  # line 13
MARKER = r"/SOS/ "  # type: str  # line 14
del version  # unload module  # line 15


Category = enum.Enum("Category", {"Repository_handling": 2, "Working_with_branches": 4, "Working_with_files": 6, "Defining_file_patterns": 8, "Configuration": 10, "Further_commands": 12})  # line 18

CategoryAbbrev = {"repo": Category.Repository_handling, "branches": Category.Working_with_branches, "files": Category.Working_with_files, "patterns": Category.Defining_file_patterns, "config": Category.Configuration, "other": Category.Further_commands}  # type: Dict[str, Category]  # line 27

class Argument(_coconut_NamedTuple("Argument", [("name", 'str'), ("long", 'str')])):  # command argument and description  # line 36
    __slots__ = ()  # command argument and description  # line 36
    __ne__ = _coconut.object.__ne__  # command argument and description  # line 36
    def __eq__(self, other):  # command argument and description  # line 36
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # command argument and description  # line 36
# command argument and description

class Command(_coconut_NamedTuple("Command", [("category", 'Category'), ("arguments", 'List[Argument]'), ("short", 'str'), ("long", 'str')])):  # line 38
    __slots__ = ()  # line 38
    __ne__ = _coconut.object.__ne__  # line 38
    def __eq__(self, other):  # line 38
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # line 38



COMMANDS = {"offline": Command(Category.Repository_handling, [Argument("[<branch-name>", "Name of the initial branch to use. Default: determined by the type of the underlying VCS"), Argument("[<message>] ]", "Initial commit message. Default: A timestamp")], "Prepare working offline with SOS, creating an initial branch from the current file tree", """Creates the offline repository metadata in a folder ".sos/" relative to the current working directory.
       The existence of this metadata folder marks the root for the offline SOS repository"""), "online": Command(Category.Repository_handling, [], "Finish working online, removing the SOS repository's metadata folder", """The user is warned if any branches remain that have not been committed/pushed to the underlying VCS.
       If not, or using the "--force"  option, the "./sos" folder is removed entirely.
       SOS will serve again only as a pass-through command for the original underlying VCS in that folder"""), "dump": Command(Category.Repository_handling, [Argument("[<path>/]<name[.sos.zip]>", "File name for the exported repository archive dump")], "Perform repository dump into an archive file", """The archive will contain only the metadata folder, not the file tree.
       After unzipping the archive, the file tree can be easily restored to the latest revision with "sos switch /" """), "help": Command(Category.Further_commands, [Argument("[<command> | <category>]", """Name of command or command category to get help for.
                                              Command is one out of everything shown per "sos help".
                                              Category is one out of "repo", "branches", "files", "patterns", or "other".""")], "Display usage and background information", """ The help command provides a compact usage and interface guide to SOS.
        For further information, read the online help at https://sos-vcs.net"""), "version": Command(Category.Further_commands, [], "Display SOS version and packing information", """Show information about the SOS source revision, plus the version identifier of the PyPI package and Git commit status"""), "log": Command(Category.Working_with_branches, [], "List revisions of current branch", """List all revisions of currently selected branch in chronological order (latest last).
       The format for each log entry is as follows:
       [*] r<revision> @<timestamp> (+<added files>/-<removed files>/~<modified files>/T<modified text files>) |<commit message or tag>|"""), "status": Command(Category.Repository_handling, [Argument("[<branch>][/<revision>]", """Branch and/or revision to show changes of file tree against (if "useChangesCommand" flag is disabled).
                                             The argument is ignored (if "useChangesCommand" is enabled)""")], "Display file tree changes or repository stats", """Display changed filepaths vs. last committed or specified revision on current or specified branch (if "useChangesCommand" flag is disabled).
       Display repository stats and settings (is "useChangesCommand" flag is enabled)"""), "branch": Command(Category.Working_with_branches, [Argument("[<name>", "Name of the new branch to create"), Argument("[<message>] ]", "Initial commit message for the new branch")], "Create a new branch", """Create a new branch and switch to work on it.
       Default: Use current file tree as basis, using automatically generated branch name and initial commit message."""), "destroy": Command(Category.Working_with_branches, [Argument("[<branch>]", "Name or index of the branch")], "Remove branch", """The current or specified branch will be removed entirely from the SOS metadata. There will be a backup, however, that can be restored manually"""), "switch": Command(Category.Working_with_branches, [Argument("[<branch>][/<revision>]", "Branch and/or revision to switch to")], "Switch to another branch", """Replace file tree contents by specified revision of current or specified other branch.
       This command will warn the user about changes in the file tree vs. the last committed revision on the current branch.
       After switching, all changes done to the file tree will be compared to the (new) current branch's latest committed revision"""), "ls": Command(Category.Working_with_files, [Argument("[<folder path>]", "Path to list")], "List files, display tracking status, and show changes", """Lists file in current or specified folder, showing modification status, and matching tracking patterns (if in track or picky mode)"""), "commit": Command(Category.Working_with_files, [Argument("[<message>]", "Message to store with the revision. Can be used to refer to the revision, and is also shown in the " "log" " command")], "Create a new revision", """Using the current file tree, create and persist a new revision of the current branch to the repository"""), "update": Command(Category.Working_with_files, [Argument("[<branch>][/<revision>]", "Branch and/or revision")], "Integrate work from another branch into the file tree", """Similarly to switch, this command updates the current file tree to the state of another revision, usually from another branch."
       In addition, it allows merging differing contents interactively or by rules specified through command-line switches.
       Default operation for files, lines and characters is add and remove"""), "changes": Command(Category.Working_with_files, [Argument("[<branch>][/<revision>]", """Branch and/or revision to show changes of file tree against""")], "Show inserted, removed, and/or modified files", """Checks the file tree for modifications against the last committed revision on the current branch.
       Additions are marked with ADD, deletions with DEL and modifications with MOD.
       Changes are detected by file size and modification timestamp (default), or by file size and file contents hash (repository created in strict mode)."""), "diff": Command(Category.Working_with_files, [Argument("[<branch>][/<revision>]", ""),], "List changes in file tree", """ (or `--from` specified revision) vs. last (or specified) revision"""), "add": Command(Category.Working_with_files, [Argument("<file pattern>", "Folder-specific file name pattern"),], "Add a tracking pattern", """Add a folder-specific file name tracking pattern to the current branch.
       Only applicable after "offline --track" or "offline --picky" """), "addnot": Command(Category.Working_with_files, [Argument("<file pattern>", "Folder-specific file name pattern"),], "Add a tracking pattern to the tracking blacklist", """Add a folder-specific file name tracking anti-pattern to the current branch"""), "rm": Command(Category.Working_with_files, [Argument("<file pattern>", "Folder-specific file name pattern"),], "Remove a tracking pattern", """Remove a folder-specific file name tracking pattern from the current branch.
       Only applicable after "offline --track" or "offline --picky" """), "rmnot": Command(Category.Working_with_files, [Argument("<file pattern>", "Folder-specific file name pattern"),], "Remove a tracking pattern from the tracking blacklist", """Remove a folder-specific file name tracking anti-pattern from the current branch."""), "mv": Command(Category.Working_with_files, [Argument("<old file pattern>", "Folder-specific file name pattern"), Argument("<new file pattern>", "Folder-specific file name pattern"),], "Rename, move, or move and rename tracked files according to the specified file patterns", """The command changes a tracking pattern and renames all tracked files that it matches.
       This command will also consider reordering of globs unless ambiguous, allowing for more complex rename actions"""), "mvnot": Command(Category.Working_with_files, [Argument("<old file pattern>", "Folder-specific file name pattern"), Argument("<new file pattern>", "Folder-specific file name pattern"),], "Modify a tracking pattern black list entry", """In contrast to "mv", this command won't affect any files, only the tracking pattern on the tracked files blacklist"""), "config set": Command(Category.Configuration, [Argument("[<param>]", "Parameter name"), Argument("[<value>]", "Parameter value")], "Define SOS setting", """For strings, flags, and numbers, this directly sets the value.
       For lists, the given string is split by semicola and defines the list's contenst.
       Use "config add" and "config rm" to modify single entries in a list configuration setting.

       Accepted values for flag-type parameters: 1/0, on/off, true/false, or yes/no"""), "config unset": Command(Category.Configuration, [Argument("[<param>]", "Parameter name")], "Clear SOS setting", """This completely removes the setting, letting SOS fall back to its default, if any.
       Removing the last entry from a list setting *will not* remove the setting itself, as this would have a different semantic
       (e.g. falling back to a default, or using the global setting instead of the local one)"""), "config add": Command(Category.Configuration, [Argument("[<param>]", "Parameter name"), Argument("[<value>]", "Parameter value")], "Add an entry to a list configuration setting", """Adds one or more semicolon-separated values to a list-type configuration setting"""), "config rm": Command(Category.Configuration, [Argument("[<param>]", "Parameter name"), Argument("[<value>]", "Parameter value")], "Remove an entry from a list configuration setting", """Removes exactly one value from a list-type configuration setting"""), "config show": Command(Category.Configuration, [Argument("[<name> | flags | texts | lists]", "Name of parameter or type of configuration parameters")], "Shows SOS configuration", """Lists all configuration parameters, also indicating storage origin (local, global, or default).
       The optional argument is either the name of a parameter to display as the only output,
       or a parameter type to enumerate all valid SOS parameters for the specified configuration type"""), "publish": Command(Category.Configuration, [Argument("[<message>]", "Commit message")], "Commit the SOS branch to the underlying VCS", """This command uses the underlying VCS's "add" and "commit" commands to create a new revision with the changes made in the current SOS branch.
       The SOS branch will consequently be marked as clean (removing the dirty flag).
       In simple repository mode, the selection of files to commit is interactively, while in track and picky mode all files tracked or picked are committed.""")}  # type: Dict[str, Command]  # line 41

OPTIONS = {"sos": {None: """Pass command and options to SOS, even when not offline, e.g. 'sos --sos config add texttype "*.md"'"""}, "vcs": {None: "Pass command and options to underlying VCS, even in offline mode, e.g. " "sos --vcs add test.md" " for Git"}, "compress": {"offline": """Compress all versioned files instead of simply copying them verbatim.
                 May be significantly slower, but reduces storage overhead.
                 Same as going offline after "sos config set compress on" """}, "track": {"offline": """Defines repository mode to use SVN-like file handling per tracking patterns.
             Tracking patterns are added to or removed from a branch via "sos add" and "sos rm"; files can be moved and renamed via "sos mv" """}, "picky": {"offline": """Defines repository mode to use Git-like file handling per staging patterns.
               Staging patterns are added to or removed from a branch via "sos add" and "sos rm"; files can be moved and renamed via "sos mv" """}, "strict": {None: """Perform the command using file contents instead of relying on modification timestamp.
             File sizes are always compared in both modes""", "offline": """Defines repository property to always compare file contents instead of relying on modification timestamp.
                  File sizes are always compared in both modes.
                  Cannot be changed via user interface after repository creation.
                  Most commands, however, support a "--strict" option nevertheless"""}, "force": {None: """Executes potentially harmful operations, telling SOS that you really intend to perform that command.
             Most commands: Ignore uncommitted branches, continue to remove SOS repository metadata folders """, "offline": """If already in offline mode, remove offline repository first before creating empty offline repository anew""", "online": """Ignore uncommitted branches, continue to remove SOS repository metadata folder""", "destroy": """Ignore dirty branches (those with changes not committed back to the underlying VCS) and continue with branch destruction""", "switch": """Override safety check to break switching when file tree contains modifications"""}, "full": {"dump": """Force a full repository dump instead of a differential export"""}, "skip-backup": {"dump": "Don't create a backup of a previous dump archive before dumping the repository" ""}, "changes": {"log": "List differential changeset for each revision"}, "diff": {"log": "Display textual diff for each revision"}, "repo": {"status": """List branches and display repository status (regardless of "useChangesCommand" flag)"""}, "stay": {"branch": "Perform branch operation, but don't switch to newly created branch"}, "last": {"branch": "Use last revision instead of current file tree as basis for new branch. Doesn't affect current file tree"}, "fast": {"branch": "Use the experimental fast branch method. Always implies --last"}, "meta": {"switch": "Only switch the branch's file tracking patterns when switching the branch. Won't update any files"}, "progress": {None: """Display file names during file tree traversal, show processing speed, and show compression advantage, if the "compress" flag is enabled"""}, "log": {None: """Configures the Python logging module to include source details like log level, timestamp, module, and line number with the logged messages"""}, "verbose": {None: "Enable more verbose user output"}, "debug": {None: "Enable logging of internal details (intended for developers only)"}, "only <tracked pattern>": {None: """Restrict operation to specified already tracked tracking pattern(s). Available for commands "changes", "commit", "diff", "switch", and "update" """}, "except <tracked pattern>": {None: """Avoid operation for specified already tracked tracking pattern(s). Available for commands "changes", "commit", "diff", "switch", and "update" """}, "patterns": {"ls": "Only show tracking patterns"}, "tags": {"ls": "List all repository tags (has nothing to do with file or filepattern listing)"}, "recursive": {"ls": "Recursively list also files in sub-folders"}, "r": {"ls": "Recursively list also files in sub-folders"}, "all": {"ls": "Recursively list all files, starting from repository root", "log": """Show all commits since creation of the branch.
              Default is only showing the last "logLines" entries""", "publish": """Commit all files present at offline time, instead of only modifications thereafter.
                  When going offline with SOS on an underlying VCS checkout with modifications, use this option.
                  Otherwise - underlying VCS checkout was clean when going offline with SOS - avoid this option."""}, "a": {"ls": "Recursively list all files, starting from repository root"}, "tag": {"commit": "Store the commit message as a tag that can be used instead of numeric revisions"}, "add": {"switch": "Only add new files"}, "add-lines": {"switch": "Only add inserted lines"}, "add-chars": {"switch": "Only add new characters"}, "rm": {"switch": "Only remove vanished files"}, "rm-lines": {"switch": "Only remove deleted lines"}, "rm-chars": {"switch": "Only remove vanished characters"}, "ask": {"switch": "Ask how to proceed with modified files"}, "ask-lines": {"switch": "Ask how to proceed with modified lines"}, "ask-chars": {"switch": "Ask how to proceed with modified characters"}, "eol": {"switch": "Use EOL style from the integrated file instead. Default: EOL style of current file"}, "ignore-whitespace": {"diff": "Ignore white spaces during comparison"}, "wrap": {"diff": "Wrap text around terminal instead of cropping into terminal width"}, "soft": {"mv": "Do not move or rename files, only affect the tracking pattern"}, "local": {"config set": "Persist configuration setting in local repository, not in user-global settings store"}, "local": {"config unset": "Persist configuration setting in local repository, not in user-global settings store"}, "local": {"config add": "Persist configuration setting in local repository, not in user-global settings store"}, "local": {"config rm": "Persist configuration setting in local repository, not in user-global settings store"}, "local": {"config show": "Only show configuration settings persisted in local repository, not from user-global settings store"}, "prune": {"config rm": "Remove a list-type parameter together with the last entry"}, "sos": {None: """Pass command and arguments to SOS, even when not in offline mode, e.g. "sos --sos config set key value" to avoid passing the command to Git or SVN"""}, "n": {"log": """Maximum number of entries to show"""}, "relative": {"changes": """Display paths relative to current working directory. Default: paths relative to SOS repository root""", "log": """Display paths relative to current working directory. Default: paths relative to SOS repository root""", "switch": """Display paths relative to current working directory. Default: paths relative to SOS repository root""", "add": """Display pattern path relative to SOS repository root. Default: absolute file system path""", "remove": """Display pattern path relative to SOS repository root. Default: absolute file system path"""}}  # type: Dict[str, Dict[_coconut.typing.Optional[str], str]]  # line 262


def getTitleFont(text: 'str', width: 'int') -> 'Tuple[str, str]':  # line 442
    ''' Finds best fitting font for termimal window width, falling back to SOS marker if nothing fits current terminal width. Returns (actual text, selected Figlet font). '''  # line 443
    x = sorted((t for t in [(max((len(_) for _ in Figlet(font=f, width=999).renderText(text).split("\n"))), f) for f in ["big", "modular", "bell", "nscript", "pebbles", "puffy", "roman", "rounded", "santaclara", "script", "small", "soft", "standard", "univers", "thin"]] if t[0] <= width))  # type: List[Tuple[int, str]]  # line 444
    if len(x) == 0:  # replace by shortest text  # line 445
        text = MARKER  # replace by shortest text  # line 445
    return (text, sorted((t for t in [(max((len(_) for _ in Figlet(font=f, width=999).renderText(text).split("\n"))), f) for f in ["big", "modular", "bell", "nscript", "pebbles", "puffy", "roman", "rounded", "santaclara", "script", "small", "soft", "standard", "univers", "thin"]] if t[0] <= width))[-1][1])  # line 446

@_coconut_tco  # https://github.com/pwaller/pyfiglet/blob/master/doc/figfont.txt  # line 448
def getTitle(large: 'bool'=True) -> '_coconut.typing.Optional[str]':  # https://github.com/pwaller/pyfiglet/blob/master/doc/figfont.txt  # line 448
    ''' Large: use ascii-art. '''  # line 449
    if not large:  # line 450
        return APP  # line 450
    if not Figlet:  # line 451
        return None  # line 451
    text, font = getTitleFont(APP, width=pure.termWidth)  # line 452
    return _coconut_tail_call("\n".join, (_ for _ in Figlet(font=font, width=pure.termWidth).renderText(text).split("\n") if _.replace(" ", "") != ""))  # line 453

def usage(argument: 'str', version: 'bool'=False, verbose: 'bool'=False):  # line 455
    if version:  # line 456
        title = getTitle()  # type: _coconut.typing.Optional[str]  # line 457
        if title:  # line 458
            print(title + "\n")  # line 458
    print("%s%s%s" % (MARKER, APPNAME if version else APP, "" if not version else " (PyPI: %s)" % VERSION))  # line 459
    if version:  # line 460
        sys.exit(0)  # line 460
    category = CategoryAbbrev.get(argument, None)  # type: _coconut.typing.Optional[Category]  # convert shorthand for category  # line 461
    command = argument if category is None else None  # type: _coconut.typing.Optional[str]  # line 462
    if command is None:  # line 463
        print("\nUsage:\n  sos <command> [<argument1>, [<argument2>]] [<option1>, [<options...]]")  # line 463
    for _value, cat in sorted([(_.value, _) for _ in list(Category)]) if category is None else [(None, category)]:  # over one or all categories  # line 464
        ofcategory = {command_: values for command_, values in COMMANDS.items() if values.category == cat and (command is None or command_ == command)}  # type: Dict[str, Command]  # select commands from chosen category  # line 465
        if len(ofcategory) == 0:  # line 466
            continue  # line 466
        print("\n%s:" % cat.name.replace("_", " "))  # line 467
        for name, cmd in sorted(ofcategory.items()):  # line 468
            args = "  %s %s  " % (name, " ".join([c.name for c in cmd.arguments]))  # type: str  # command argument names  # line 469
            print("%s\n%s" % (args + cmd.short, pure.ajoin(" " * len(args), pure.splitStrip(cmd.long), nl="\n")))  # line 470
            if command is None and not verbose:  # TODO align commands correctly when in short mode  # line 471
                continue  # TODO align commands correctly when in short mode  # line 471
            if cmd.arguments:  # line 472
                print("\n  Arguments:")  # line 472
            maxlen = 4 + 2 + max((len(s.name) for s in cmd.arguments)) if len(cmd.arguments) > 0 else 0  # type: int  # argument name length max plus indentation  # line 473
            for c in cmd.arguments:  # line 474
                print(pure.ljust("    %s  " % c.name, maxlen) + ("\n" + pure.ljust(width=maxlen)).join(pure.splitStrip(c.long)))  # line 474
            matchingoptions = [(optname, pure.splitStrip(description)) for optname, description in [(optname, dikt[name]) for optname, dikt in OPTIONS.items() if name in dikt]]  # type: List[Tuple[str, _coconut.typing.Sequence[str]]]  # line 475
            if matchingoptions:  # line 476
                print("\n  Options:")  # line 477
                maxoptlen = max([len(optname) for optname, __ in matchingoptions])  # type: int  # line 478
                for optname, descriptions in sorted(matchingoptions):  # line 479
                    if len(descriptions) == 0:  # line 480
                        continue  # line 480
                    print("    %s%s  %s%s" % ("--" if len(optname) > 1 else "-", pure.ljust(optname, maxoptlen + (0 if len(optname) > 1 else 1)), descriptions[0], "\n" + pure.ajoin(" " * (6 + maxoptlen + (2 if len(optname) > 1 else 1)), descriptions[1:], nl="\n") if len(descriptions) > 1 else ""))  # line 481
            matchingoptions = [] if cmd is None else [(optname, pure.splitStrip(dikt[None]) if None in dikt else []) for optname, dikt in OPTIONS.items()]  # add all text for the generic description  # line 482
            if matchingoptions:  # line 483
                print("\n  Common options:")  # line 484
                maxoptlen = max([len(optname) for optname, __ in matchingoptions])  # line 485
                for optname, descriptions in sorted(matchingoptions):  # line 486
                    if len(descriptions) == 0:  # line 487
                        continue  # line 487
                    print("    %s%s  %s%s" % ("--" if len(optname) > 1 else "-", pure.ljust(optname, maxoptlen + (0 if len(optname) > 1 else 1)), descriptions[0], "\n" + pure.ajoin(" " * (6 + maxoptlen + (2 if len(optname) > 1 else 1)), descriptions[1:], nl="\n") if len(descriptions) > 1 else ""))  # line 488
    if command is None:  # line 489
        print("\nCommon options:")  # line 490
        genericOptions = {k: v[None] for k, v in OPTIONS.items() if None in v}  # type: Dict[str, str]  # line 491
        maxlen = max((len(_) for _ in genericOptions))  # line 492
        for optname, description in sorted(genericOptions.items()):  # line 493
            print("  %s%s  %s" % ("--" if len(optname) > 1 else "-", pure.ljust(optname, maxlen), pure.ajoin(" " * (2 + 2 + maxlen + 2), pure.splitStrip(description), nl="\n", first=False)))  # line 494

# TODO wrap text at terminal boundaries automatically, if space suffices
#    [<branch>][/<revision>]      Revision string. Branch is optional (defaulting to current branch) and may be a label or number >= 0
#                                 Revision is an optional integer and may be negative to reference from the latest commits (-1 is most recent revision), or a tag name"""
    sys.exit(0)  # line 499
