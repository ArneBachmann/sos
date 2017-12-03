# Subversion Offline Solution (SOS 0.9.4) #

[![Travis badge](https://travis-ci.org/ArneBachmann/sos.svg?branch=master)](https://travis-ci.org/ArneBachmann/sos)
[![PyPI badge](https://img.shields.io/pypi/v/sos-vcs.svg)](https://badge.fury.io/py/sos-vcs)
[![Conda badge](https://img.shields.io/conda/pn/conda-forge/python.svg)]()
[![Code coverage badge](https://coveralls.io/repos/github/ArneBachmann/sos/badge.svg?branch=master)](https://coveralls.io/github/ArneBachmann/sos?branch=master)

License: [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/)

#### Abbreviations ####
- **SCM**: *Source Control Management*
- **SVN**: Subversion
- **VCS**: *Version Control Systems*


## Introduction ##
If you (love, or simply have to) work with the *Subversion* VCS, but **need** (or **lack**) the flexibility of committing and branching files offline (without a permanent network connection) similar to how *Git* is able to, SOS is your straight-forward and super simple command-line SCM solution:

SOS allows performing offline operations *a)* as a drop-in replacement for `svn` and other VCS commands, *b)* as an offline extension of those VCSs that don't support offline branching and committing, and *c)* as a standalone VCS.
You may run `sos offline` not only inside a Subversion checkout, but in any (and also multiple) folders of your file system, even outside of VCS repository checkouts/clones.

[SOS](https://github.com/ArneBachmann/sos) thus augments [SVN](http://subversion.apache.org) with offline operation and serves the same need as [RCS](http://www.gnu.org/software/rcs/), [CVS](https://savannah.nongnu.org/projects/cvs), [Git](https://git-scm.com), [gitless](http://gitless.com), [Bazaar](http://bazaar.canonical.com/en/), [Mercurial](https://www.mercurial-scm.org), and [Fossil](http://www.fossil-scm.org).

As an additional practical benefit, the `sos` command will double as the command line interface of any popular SCM and will execute any `svn`, `git`, etc. commands by via `sos <command> [<arguments-and-options>]`, e.g. `sos commit -m "Message"` instead of `svn commit -m "Message"` or `git commit -m "Message"`.
Once you executed `sos offline`, however, all commands are interpreted by the SOS tool instead, until leaving the offline mode via `sos online` (with the exception of `sos config`, cf. details below).

SOS supports three different file handling approaches that you may use to your liking, thus being able to mirror the file handling philosophies of different traditional VCSs, plus a new default mode for super quick and easy version management.
- **Simple mode**: All files are automatically versioned and tracked. Drawback: Will pickup any little modification for any file
- **Tracking mode**: Only files that match certain file name tracking patterns are respected during `commit`, `update` and `branch` (just like in SVN, gitless, and Fossil), requiring users to specifically add or remove files per branch. Drawback: Need to declare files to track for every offline repository
- **Picky mode**: Each operation needs the explicit declaration of file name patterns to stage for versioning (like Git does). Drawback: Need to stage files for every single commit


## Comparison with traditional VCS ##
- `switch` works like `checkout` in Git or `update to revision` in SVN
- `update` works a bit like `pull` in Git or `update` in SVN


## Commit semantics ##
- Committing always creates a new revision with an incremented index.


## Update and merge semantics ##
There are several level of consideration:
- File addition/removal per revision, e.g. when updating from another branch and/or revision or switching to them
- Line insertion/deletion per file, e.g. when merging file modifications during update
- Character insertion/deletion per line, e.g. when non-conflicting intra-line differences are detected
- Updating in track or picky mode will always integrate tracked file patterns. To revert this, use the `switch --meta` command to pull back in another branch's or revision's tracking patterns.


## Config options ##
- `strict`: Flag for always performing full file comparsion, not relying on file size and modification timestamp only. Default: False
- `track`: Flag for always going offline in tracking mode (SVN-style). Default: False
- `picky`: Flag for always going offline in picky mode (Git-styly). Default: False
- `compress`: Flag for compressing versioned artifacts. Default: True
- `defaultbranch`: Name of the initial branch created when going offline. Default: Dynamic per type of VCS in current working directory (e.g. `master` for Git, `trunk` for SVN)
- `texttype`: Semicolon-separated list of glob patterns for file names that should be recognized as text files that can be merged through textual diff, in addition to what Python's `mimetypes` library can do. Default: Empty
- `bintype`: Semicolon-separated list of glob patterns for file names that should be recognized as binary files that cannot be merged through textual diff. Default: Empty
- `ignores`: List of glob patterns for files to ignore during commit/diff/changes/update etc.
- `ignoresWhitelist`: List of glob patterns that allow files to be added although captured by a blacklist pattern from `ignores`
- `ignoreDirs`: As `ignores`, but for folder names
- `ignoreDirsWhitelist`: As `ignoresWhitelist`, but for folder names

## Branch semantics ##
- SOS always branches from a branch's last revision. Exception: Simple mode always considers current file tree instead, unless TODO --last for tracked mode?

    There may be, however, blocks of text lines that seem inserted/deleted but may have actually just been moved inside the file. SOS attempts to detect clear cases of moved blocks and silently accepts them no matter what.

Levels of interactive merging:
- One rule set for entire revision
- One rule set per file
- One decision per block of lines
- Conflict resolution decision per conflicted line


## Noteworthy details ##
- There is no relation between a checkout, branch point and any committed revision.
- Branches are always created from current file system state and have no reference to other branches or specific revisions
- Updating is allowed even if uncommitted changes are connected (no matter if from last revision or after switching to any other revision)
- Python 2 support was ditched completely, as type safety was difficult to guarantee and external library support also missing

## User configuration and defaults ##
SOS optionally uses the [`configr`]() library to manage per-user global defaults for the `--strict`, `--track` and `--picky` parameters that the `offline` command takes.
By means of the `sos config set <key> <value>` command, you can set the `strict`, `track` or `picky` flag with values like `1`, `yes`, `on`, `true`.
It's also possible to define a per-user global defaults for file and folder exclude patterns.

## FAQ ##
> Q: I don't want to risk data loss in case SOS has some undiscovered bugs. What can I do?
>
> A: Configure SOS to store all versioned files as plain file copies instead of compressed files: `sos config set compress off` should do the trick. All offline repositories created after that will simply copy files when branching and/or versioning: note, however, that the filenames will be hashed and stored in the metadata file.


## Hints and tipps ##
- It may be a good idea to go offline one folder higher up in the file tree than your base working folder to care for potential deletions or renames
- Switching inside a branch never modifies the tracking patterns, as they are not linked to any specific revision
- dirty flag only relevant in track and picky mode (?)
- Branching larger amounts of binary files may be expensive as all files are copied and/or compressed during `sos offline`


## Release management ##
- Run `export BUILD=true && python3 setup.py clean build sdist` to compile and test the code, increment the version number, and package into an archive. If you need evelated rights, use `sudo -E python...`
- Run `git add`, `git commit` and `git push` and let Travis CI run the tests for different target platforms. If there were no problems, continue:
- Run `twine upload dist/*.tar.gz` to upload the module to PyPI (make sure only one file exists, otherwise a rights problem could be present)


## Todos ##
- diffCommand = "diff -d {old!s} {new!s}"  # requires diffutils on OpenSUSE
- mergeCommand = "merge -A -L z -L a -L b c a b"  # requires rce on OpenSUSE
- [Answer](https://stackoverflow.com/questions/4934208/working-offline-with-svn-on-local-machine-temporary) when published
