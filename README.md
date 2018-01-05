# Subversion Offline Solution (SOS 1.1.4) #

[![Travis badge](https://travis-ci.org/ArneBachmann/sos.svg?branch=master)](https://travis-ci.org/ArneBachmann/sos)
[![Build status](https://ci.appveyor.com/api/projects/status/fe915rtx02buqe4r?svg=true)](https://ci.appveyor.com/project/ArneBachmann/sos)
[![Code coverage badge](https://coveralls.io/repos/github/ArneBachmann/sos/badge.svg?branch=master)](https://coveralls.io/github/ArneBachmann/sos?branch=master)
[![PyPI badge](https://img.shields.io/pypi/v/sos-vcs.svg)](https://badge.fury.io/py/sos-vcs)

- License: [MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/)
- [Documentation](http://sos-vcs.net) (official website), [Code Repository](https://github.com/ArneBachmann/sos) (at Github)
- [Buy a coffee](http://PayPal.Me/ArneBachmann/) for the developer to show your appreciation!

### List of Abbreviations and Definitions ###
- **MPL**: [*Mozilla Public License*](https://www.mozilla.org/en-US/MPL/)
- **PyPI**: [*Python Package Index*](https://pypi.python.org/pypi)
- **SCM**: *Source Control Management*
- **SOS**: *Subversion Offline Solution*
- **SVN**: [Apache Subversion](http://subversion.apache.org/)
- **VCS**: *Version Control System*

- **Filename**: Fixed term for file names used throughout SOS and this documentation
- **File pattern**: A filename or [glob](https://en.wikipedia.org/wiki/Glob_%28programming%29), allowing to place special characters like `*?[!]` into file names to mark ellipses
- **File tree**: A directory structure on the user's file system at a certain point in time. It's not exactly the same as a *checkout* or *working copy*, but largely comparable


## Introduction ##
If you (**love**, or simply **have to**) work with the SVN VCS, but **need** (or **lack**) the flexibility of committing and branching files offline (without a permanent network connection) similar to how *Git* is able to, SOS is your straight-forward and super simple command-line SCM solution:

SOS allows performing offline operations *a)* as a drop-in replacement for `svn` and other VCS commands, *b)* as an offline extension of those VCSs that either don't support offline branching and committing or are too complex, and *c)* as a standalone VCS.
You may run `sos offline` not only inside a SVN checkout, but in any (and also multiple, even nested) folders of your file system, even outside of VCS repository checkouts/clones.

[SOS](https://arnebachmann.github.io/sos/) thus augments [SVN](http://subversion.apache.org) with offline operation and serves the same need as [RCS](http://www.gnu.org/software/rcs/), [CVS](https://savannah.nongnu.org/projects/cvs), [Git](https://git-scm.com), [gitless](http://gitless.com), [Bazaar](http://bazaar.canonical.com/en/), [Mercurial](https://www.mercurial-scm.org), and [Fossil](http://www.fossil-scm.org).

As an additional practical benefit, the `sos` command will double as the command line interface of any popular VCS and will execute any `svn`, `git`, etc. command by `sos <command> [<arguments-and-options>]`, e.g. `sos commit -m "Message"` instead of `svn commit -m "Message"` or `git commit -m "Message"`.
Once you executed `sos offline`, however, all commands are interpreted by the SOS tool instead, until leaving the offline mode via `sos online` (with the exception of `sos config`, cf. details below).


### Flexible VCS Modes ###
SOS supports three different file handling models that you may use to your liking, thus being able to mimick different traditional VCSs, plus a new mode for super quick and easy version management (the default).
- **Simple mode**: All files are automatically versioned and tracked. Drawback: Will pickup any little modification for any file, binary or not
- **Tracking mode**: Only files that match certain file patterns are respected during `commit`, `update` and `branch` (just like in SVN, gitless, and Fossil), requiring users to specifically add or remove files per branch. Drawback: Need to declare files to track for every offline repository
- **Picky mode**: Each operation needs the explicit declaration of file patterns for versioning (like Git does). Drawback: Need to stage files for every single commit

### Unique Features of SOS ###
- Initializes repositories by default with the *simple mode*, which makes effortless versioning a piece of cake
- In the optional tracking mode, files are tracked via *file patterns* instead of pure filenames or paths (in a manner comparable to how SVN ignores files)
- Command line replacement for traditional VCS that transparently pipes commands to them
- Straightforward and simplified semantics for common VCS operations (`branch`, `commit`, integrate changes)

### Limitations ###
- Designed for use by single user, network synchronization is a non-goal. Don't attempt to use SOS in a shared location, concurrent access to the repository may corrupt your data, as there is currently no locking in place (could be augmented, but it's a non-goal too)
- Has a small user base as of now, therefore no reliable reports of compatibility and operational capability except for the automatic unit tests run on Travis CI and AppVeyor

### Compatibility ###
- SOS runs on any Python 3 distribution, including some versions of PyPy. Python 2 is not fully supported yet due to library issues, although SOS's programming language *Coconut* is generally able to transpile to valid Python 2 source code
- SOS is compatible with above mentioned traditional VCSs: SVN, Git, gitless, Bazaar, Mercurial and Fossil
- Filename encoding and console encoding: Full roundtrip support (on Windows) started only with Python 3.6.4 and has not been tested nor confirmed yet for SOS


## Latest Changes ##
- Version 1.1 released on 2017-12-30:
    - [Bug 90](https://github.com/ArneBachmann/sos/issues/90) Removed directories weren't picked up
    - [Bug 93](https://github.com/ArneBachmann/sos/issues/93) Picky mode lists any file as added
    - [Enhancement 63](https://github.com/ArneBachmann/sos/issues/63) Show more change details in `log` and `status`, and also `ls` (in [#101](https://github.com/ArneBachmann/sos/issues/101))
    - [Enhancement 86](https://github.com/ArneBachmann/sos/issues/86) Renamed command for branch removal to `destroy`
    - [Feature 8](https://github.com/ArneBachmann/sos/issues/8) Added functionality to rename tracking patterns and move files accordingly
    - [Feature 61](https://github.com/ArneBachmann/sos/issues/61) Added option to only consider or exclude certain file patterns for relevant operations using `--only` and `--except`. Note: These have to be already tracked file patterns, currently, see [#99](https://github.com/ArneBachmann/sos/issues/99) and [#100](https://github.com/ArneBachmann/sos/issues/100)
    - [Feature 80](https://github.com/ArneBachmann/sos/issues/80) Added functionality to use tags
    - [QA 79](https://github.com/ArneBachmann/sos/issues/79) Added AppVeyor automated testing
    - [QA 94](https://github.com/ArneBachmann/sos/issues/94) More test coverage
    - Many little fixes and improvements
    - Downloads until today: 1270
- Version 1.0 released on 2017-12-14:
    - First release with basic functionality
    - Lots of test cases, good test coverage
    - System integration and packaging
    - Library integration and testing
    - VCS integration
    - Downloads: 4600


## Comparison with Traditional VCSs ##
While completing version 1.0 of SOS, I incidentally discovered an interesting [article by Gregory Szorc](https://gregoryszorc.com/blog/2017/12/11/high-level-problems-with-git-and-how-to-fix-them/) that discusses central weaknesses in the design of popular VCSs, with a focus on Git. Many of his arguments I have intuitively felt to be true as well and were the reason for the development of SOS: mainly the reduction of barriers between the developer's typical workflow and the VCS, which is most often used as a structured tool for "type and save in increments", while advanced features of Git are just very difficult to remember and get done right.

- While Git is basically a large key-value store with a thin access interface on top, SOS keeps a very clear (folder) structure of branches, revisions and files
- Compared to SVN, SOS's file store is much simpler and doesn't require an integrated database

Here is a comparison between SOS and VCS's commands:
- `branch` creates a branch from the current file tree (or last commit), but also switches to it immediately (unless told not to). There is no requirement to name branches, removing all barriers
    - SOS allows to branch from the latest committed revision via `sos branch [<name>] --last`; this automatically applies when in tracking and picky mode. In consequence any changes performed since last commit will automatically be considered as a change for the next commit on the branch unless `--stay` was added as well to not switch to the new branch
- `commit` creates a numbered revision similar to SVN, but revision numbers are only unique per branch, as they aren't stored in a global namespace. The commit message is optional on purpose (since `sos commit` serves largely as a CTRL+S replacement)
    - The first revision (created during execution of `sos offline` or `sos branch`) always has the number `0`
    - Each `sos commit` increments the revision number by one; revisions are referenced by this numeric index only
- `delete` destroys and removes a branch. It's a command, not an option flag as in `git branch -d <name>`
- `move` renames a file tracking pattern and all matching files accordingly; only useful in tracking or picky mode. It supports reordering of literal substrings, but no reordering of glob markers (`*`, `?` etc.), and no adjacent glob markers. Use `--soft` to avoid files actually being renamed in the file tree. Warning: the `--force` option flag will be considered for several consecutive, potentially dangerous operations. TODO allow and consider `--force` several times on the command line
- `switch` works like `checkout` in Git for a revision of another branch (or of the current), or `update` to latest or a specific revision in SVN. Please note that switching to a different revision will in no way fix or remember that revision. The file tree will always be compared to the branch's latest commit for change detection
- `update` works a bit like `pull` in Git or `update` in SVN and replays the given branch's and/or revision's changes into the file tree. There are plenty of options to configure what changes are actually integrated. This command will not switch the current branch like `switch` does. Note, that this is not a real 3-way *merge*, just an enhanced *diff* logic.

    When differing contents are to be merged, there is always a potential for conflict; not all changes can be merged automatically with confidence. SOS takes a simplistic and pragmatic approach and largely follows a simple diff algorithm to detect and highlight changes. Insertions and deletions are noted, and modifications are partially detected and marked as such. There are different layers of changes that SOS is able to work on:
    - File addition or removal in the file tree, e.g. when updating from another branch and/or revision or switching to them
    - Line insertion or deletion inside a file, e.g. when merging file modifications during update
    - Character insertion or deletion on a text line, e.g. when non-conflicting intra-line differences are detected
    - Updating state from another branch in the `--track` or `--picky` mode will always combine all tracked file patterns. To revert this, use the `switch --meta` command to pull back in another branch's and/or revision's tracking patterns to the currently active branch
    - There may be, however, blocks of text lines that seem inserted/deleted but may have actually just been moved inside the file. SOS attempts to detect clear cases of moved blocks and silently accepts them no matter what. TODO implement and introduce option flag to avoid this behavior

### Working in *Track* and *Picky* Modes ###
Use the commands `sos add <pattern>` or `sos rm <pattern>` to add or remove file patterns. These patterns always refer to a specific (relative) file path and may contain globbing characters `?*[!]` only in the filename part of the path.


## Configuration Options ##
These options can be set or unset by the user and apply globally for all offline operations the user performs from that moment on.
Some of these options can be set on a per-repository basis during creation (e.g. `sos offline --track --strict`), others can only be set in a persistant fashion (e.g. `sos config set texttype "*.xsd"`).

### Configuration Commands ###
- `sos config set` sets a boolean flag, a string, or an initial list (semicolon-separated)
- `sos config unset` removes a setting
- `sos config add` adds a string entry to a list
- `sos config rm` removes a string entry from a list
- `sos config show` lists all defined configuration settings

### User Configuration and Defaults ###
SOS optionally uses the [`configr`](https://github.com/ArneBachmann/configr) library to manage per-user global defaults, e.g. for the `--strict` and `--track` flags that the `offline` command takes, but also for file and folder exclusion patterns.
By means of the `sos config set <key> <value>` command, you can set these flags flag with values like `1`, `no`, `on`, `false`, `enable` or `disabled`.

### Available Configuration Settings ###
- `strict`: Flag for always performing full file comparsion, not relying on file size and modification timestamp only. Default: False
- `track`: Flag for always going offline in tracking mode (SVN-style). Default: False
- `picky`: Flag for always going offline in picky mode (Git-styly). Default: False
- `compress`: Flag for compressing versioned artifacts. Default: True
- `defaultbranch`: Name of the initial branch created when going offline. Default: Dynamic per type of VCS in current working directory (e.g. `master` for Git, `trunk` for SVN)
- `texttype`: List of file patterns that should be recognized as text files that can be merged through textual diff, in addition to what Python's `mimetypes` library will detect as a `text/...` mime. *Default*: Empty list
- `bintype`: List of file patterns that should be recognized as binary files that cannot be merged textually, overriding potential matches in `texttype`. Default: Empty list
- `ignores`: List of filename patterns (without folder path) to ignore during repository operations. Any match from the corresponding white list will negate any hit for `ignores`
- `ignoresWhitelist`: List of filename patterns to be consider even if matched by an entry in the `ignores` list
- `ignoreDirs`: As `ignores`, but for folder names
- `ignoreDirsWhitelist`: As `ignoresWhitelist`, but for folder names


## Noteworthy Details ##
- SOS doesn't store branching point information (or references); each branch stands alone and has no relation whatsoever to other branches or certain revisions thereof, except incidentally its initial file contents
- File tracking patterns are stored per branch, but not versioned with commits. This means that the "what to track" metadata is not part of the changesets.
- `sos update` will **not warn** if local changes are present! This is a noteworthy exception to the failsafe approach taken for most other commands


## Hints and Tipps ##
- To save space when going offline, use the option `sos offline --compress`: It may increase the time for going offline by a larger factor (e.g. 10x), but will also reduce the amount of storage needed to version files. To enable this option for all offline repositories, use `sos config set compress on`
- When specifying file patterns including glob markers on the command line, make sure you quote them correctly. On linux (bash, sh, zsh), put your patterns into quote (`"`), otherwise the shell will replace file patterns by any matching filenames instead of forwarding the pattern literally to SOS
- Many commands can be shortened to three, two or even one initial letters
- It might in some cases be a good idea to go offline one folder higher up in the file tree than your base working folder to care for potential deletions or renames
- dirty flag only relevant in track and picky mode (?) TODO investigate - is this true, and if yes, why
- Branching larger amounts of binary files may be expensive as all files are copied and/or compressed during `sos offline`. A workaround is to `sos offline` only in the folders that are relevant for a specific task


## Development and Contribution ##
See [CONTRIBUTING.md](CONTRIBUTING.md) for information.


## Release Management ##
- Increase version number in `setup.py`
- Run `python3 setup.py clean build test sdist` to update the PyPI version number, compile and test the code, and package it into an archive. If you need evelated rights to do so, use `sudo -E python...`.
- Run `git add`, `git commit` and `git push` and let Travis CI and AppVeyor run the tests against different target platforms. If there were no problems, continue:
- Run `twine upload dist/*.tar.gz` to upload the previously created distribution archive to PyPI.
