# Subversion Offline Solution (SOS 0.9.6) #

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
If you (**love**, or simply **have to**) work with the *Subversion* VCS, but **need** (or **lack**) the flexibility of committing and branching files offline (without a permanent network connection) similar to how *Git* is able to, SOS is your straight-forward and super simple command-line SCM solution:

SOS allows performing offline operations *a)* as a drop-in replacement for `svn` and other VCS commands, *b)* as an offline extension of those VCSs that either don't support offline branching and committing or are too complex, and *c)* as a standalone VCS.
You may run `sos offline` not only inside a Subversion checkout, but in any (and also multiple, even nested) folders of your file system, even outside of VCS repository checkouts/clones.

[SOS](https://github.com/ArneBachmann/sos) thus augments [SVN](http://subversion.apache.org) with offline operation and serves the same need as [RCS](http://www.gnu.org/software/rcs/), [CVS](https://savannah.nongnu.org/projects/cvs), [Git](https://git-scm.com), [gitless](http://gitless.com), [Bazaar](http://bazaar.canonical.com/en/), [Mercurial](https://www.mercurial-scm.org), and [Fossil](http://www.fossil-scm.org).

As an additional practical benefit, the `sos` command will double as the command line interface of any popular SCM and will execute any `svn`, `git`, etc. command by `sos <command> [<arguments-and-options>]`, e.g. `sos commit -m "Message"` instead of `svn commit -m "Message"` or `git commit -m "Message"`.
Once you executed `sos offline`, however, all commands are interpreted by the SOS tool instead, until leaving the offline mode via `sos online` (with the exception of `sos config`, cf. details below).

SOS supports three different file handling models that you may use to your liking, thus being able to mimick different traditional VCSs, plus a new mode for super quick and easy version management (the default).
- **Simple mode**: All files are automatically versioned and tracked. Drawback: Will pickup any little modification for any file, binary or not
- **Tracking mode**: Only files that match certain file name tracking patterns are respected during `commit`, `update` and `branch` (just like in SVN, gitless, and Fossil), requiring users to specifically add or remove files per branch. Drawback: Need to declare files to track for every offline repository
- **Picky mode**: Each operation needs the explicit declaration of file name patterns for versioning (like Git does). Drawback: Need to stage files for every single commit


## Comparison with traditional VCS ##
- `switch` works like `checkout` in Git or `update to revision` in SVN
- `update` works a bit like `pull` in Git or `update` in SVN


## Compatibility ##
- SOS runs on any Python 3 distribution. Support for Python 2 is only partial, the test suite doesn't run through entirely yet
- SOS is compatible with above mentioned traditional VCSs: Subversion, Git, gitless, Bazaar, Mercurial and Fossil
- File name encoding and console encoding: Full roundtrip support (on Windows) started only with Python 3.6.4 and has not been tested nor confirmed yet for SOS


## Commit semantics ##
- A *commit* is the act of creating an immutable snapshot of the (tracked) file tree. Its result is a numbered *revision*, which is also called a *change set*.
- The first revision (after `sos offline` or `soso branch`) always has the number `0`
- Each `sos commit` increments the revision number by one; revisions are referenced by this numeric index only


## Update and merge semantics ##
When differing contents are merged, there is always a potential for conflict; not all changes can be merged automatically with confidence. SOS takes a simplistic and pragmatic approach and largely follows a simple diff algorithm to highlight changes. Insertions and deletions are noted, and modifications are partially detected and marked as such. There are different layers of changes that SOS is able to work on:
- File addition or removal per revision, e.g. when updating from another branch and/or revision or switching to them
- Line insertion or deletion inside a file, e.g. when merging file modifications during update
- Character insertion or deletion on a text line, e.g. when non-conflicting intra-line differences are detected
- Updating in `--track` or `--picky` mode will always combine all tracked file patterns. To revert this, use the `switch --meta` command to pull back in another branch's or revision's tracking patterns to the currently active branch.
- There may be, however, blocks of text lines that seem inserted/deleted but may have actually just been moved inside the file. SOS attempts to detect clear cases of moved blocks and silently accepts them no matter what. TODO introduce option flag to avoid this behavior


## Working in track and picky modes ##
Use the commands `sos add <pattern>` or `sos rm <pattern>` to add file paths and glob patterns.


## Config options ##
These options can be set or unset by the user and apply for all offline operations from that moment on.
Some of these options can be set on a per-repository basis during creation (e.g. `sos offline --track --strict`), others can only be set globally (e.g. `sos config set compress no`).
- `strict`: Flag for always performing full file comparsion, not relying on file size and modification timestamp only. Default: False
- `track`: Flag for always going offline in tracking mode (SVN-style). Default: False
- `picky`: Flag for always going offline in picky mode (Git-styly). Default: False
- `compress`: Flag for compressing versioned artifacts. Default: True
- `defaultbranch`: Name of the initial branch created when going offline. Default: Dynamic per type of VCS in current working directory (e.g. `master` for Git, `trunk` for SVN)
- `texttype`: Semicolon-separated list of glob patterns for file names that should be recognized as text files that can be merged through textual diff, in addition to what Python's `mimetypes` library can do. Default: Empty list
- `bintype`: Semicolon-separated list of glob patterns for file names that should be recognized as binary files that cannot be merged textually. Default: Empty list
- `ignores`: List of glob patterns for files to ignore during commit/diff/changes/update etc.
- `ignoresWhitelist`: List of glob patterns that allow files to be added although captured by a blacklist pattern from `ignores`
- `ignoreDirs`: As `ignores`, but for folder names
- `ignoreDirsWhitelist`: As `ignoresWhitelist`, but for folder names


## Branch semantics ##
- SOS usually branches from the current file tree state in simple mode, but allows to branch from the latest revision via `sos branch <name> --last`; this is always true in track and picky mode.
- The branch command switches to the new branch by default. Use `sos branch <name> --stay` to continue working on the current branch

Levels of interactive merging:
- One rule set for entire revision
- One rule set per file
- One decision per block of lines
- Conflict resolution decision per conflicted line


## Noteworthy details ##
- SOS doesn't store branching point information; each branch stands alone and has no relation to other branches or certain revisions thereof, except incidentally its initial file contents
- File tracking patterns are stored per branch, but not versioned with commits. This means that the "what to track" metadata is not part of the changesets.
- Updating is allowed even if uncommitted changes are present (no matter if from last revision or after switching to any other revision) TODO explain
- Python 2 support was ditched completely for the time being, as type safety was difficult to guarantee and external library support is partially missing TODO retest

## User configuration and defaults ##
SOS optionally uses the [`configr`]() library to manage per-user global defaults, e.g. for the `--strict`, `--track` and `--picky` parameters that the `offline` command takes, but also for file and folder exclude patterns.
By means of the `sos config set <key> <value>` command, you can set the `strict`, `track` or `picky` flag with values like `1`, `yes`, `on`, `true`.


## FAQ ##
> Q: I don't want to risk data loss in case SOS has some undiscovered bugs. What can I do?
>
> A: Configure SOS to store all versioned files as plain file copies instead of compressed files: `sos config set compress off` before going offline should do the trick. All offline repositories created after that will simply copy files when branching and/or versioning: note, however, that the filenames will be hashed and stored in the metadata file instead (which is human-readable, thankfully).


## Hints and tipps ##
- Many commands can be shortened to three, two or even one initial letters
- It might in some cases be a good idea to go offline one folder higher up in the file tree than your base working folder to care for potential deletions or renames
- dirty flag only relevant in track and picky mode (?) TODO investigate - is this true, and if yes, why
- Branching larger amounts of binary files may be expensive as all files are copied and/or compressed during `sos offline`. A workaround is to `sos offline` only in the folders that are relevant for a specific task


## Development ##
Pull requests against `master`.


## Release management ##
- Run `export BUILD=true && python3 setup.py clean build sdist` to compile and test the code, increment the version number, and package into an archive. If you need evelated rights, use `sudo -E python...`
- Run `git add`, `git commit` and `git push` and let Travis CI run the tests for different target platforms. If there were no problems, continue:
- Run `twine upload dist/*.tar.gz` to upload the module to PyPI (make sure only one file exists, otherwise a rights problem could be present)


## Todos ##
- diffCommand = "diff -d {old!s} {new!s}"  # requires diffutils on OpenSUSE
- mergeCommand = "merge -A -L z -L a -L b c a b"  # requires rce on OpenSUSE
- [Answer](https://stackoverflow.com/questions/4934208/working-offline-with-svn-on-local-machine-temporary) when published
