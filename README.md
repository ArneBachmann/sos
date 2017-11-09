> License: [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/)

### Abbreviations ###
- **SCM**: *Source Control Management*
- **SVN**: Subversion
- **VCS**: *Version Control Systems*

# Subversion Offline Solution (SOS) #
If you (love or have to) work with [`Subversion`](https://subversion.apache.org), but need/lack the flexibility of committing and branching files offline similar to how `Git` is able to, SOS is your straight-forward and super simple command-line solution:
SOS allows peforming offline operations just like distributed VCS (SCM) can do, not only inside a Subversion base folder, but in any (and even multiple) folders of your file system, be it inside or outside of repository checkouts.

[SOS](https://github.com/ArneBachmann/sos) augments [SVN](http://subversion.apache.org) with offline operation and thus serves the same need as [RCS](http://www.gnu.org/software/rcs/), [CVS](https://savannah.nongnu.org/projects/cvs), [Git](https://git-scm.com), [Gitless](http://gitless.com), [Bazaar](http://bazaar.canonical.com/en/), [Mercurial](https://www.mercurial-scm.org), and [Fossil](http://www.fossil-scm.org).


## How it works ##
This tool can either be used as a drop-in replacement for `svn` and other version control systems, as an offline extension thereof, or as a standalone VCS.
SOS will double any popular SCM command line and can execute any `svn`, `git` or other VCS commands by simply calling `sos <command>`, e.g. `sos commit -m "Message"` instead of `svn commit -m "Message"`. This works by auto-detecting the type of VCS by analyzing the current folder you are running sos from.
Once you executed `sos offline`, however, all commands go to the SOS tool instead, until you leave the offline mode via `sos online` (details below).

SOS supports three different file handling approaches that you may use to your liking, thus being able to mirror the file handling philosophies of different VCSs, including one even simpler mode for super quick and easy version management.
- **Simple mode** (default): All files are automatically committed and "tracked", but changes between branches/revisions will always be replayed in the life file tree (files will always be added or removed depending on operation)
- **Tracking mode**: Only files that match certain file name tracking patterns are respected at `commit`, `update` and `branch` (just like SVN, Gitless, and Fossil do), requiring users to specifically add or remove files to a branch
- **Picky mode**: Each operation needs the explicit declaration of file name patterns to work on (like Git does).


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


## Tipps ##
- It may be a good idea to go offline one folder higher than your base working folder to care for potential deletions or renames

## Todos ##
- branching may be expensive as all files are copied
- diffCommand = "diff -d {old!s} {new!s}"  # requires diffutils on OpenSUSE
- mergeCommand = "merge -A -L z -L a -L b c a b"  # requires rce on OpenSUSE
- [Answer](https://stackoverflow.com/questions/4934208/working-offline-with-svn-on-local-machine-temporary) when published

```
-1   a  both
-1 - b  not in curr -> insert
0   c   both
1   d   both
2   e   both
3 + g   only in curr -> potentially remove
4   f   both
4 - g   remove, but doesn't exist: must be a replacement
5 + x   added in curr -> keep or remove
6   h   in bot hother 

    _.createFile(10, "a\nb\nc\nd\ne\nf\ng\nh")
    _.createFile(11, "a\nc\nd\ne\ng\nf\nx\nh")  # missing "b", inserted g, modified g->x

S:0 T:0   a  mem = 0 "acdegfxh"
S:0 T:1 - b  -> insert(T, "b"); mem += 1 "abcdegfxh"
S:1 T:2   c  "abcdegfxh"
S:2 T:3   d  "abcdegfxh"
S:3 T:4   e  "abcdegfxh"
S:4 T:4 + g  -> del(S, 4 + mem); mem -= 1 "abcdefxh"
S:5 T:5   f  "abcdefxh"
S:5 T:6 - g  -> insert(T + mem, "g") "abcdefgxh"; mem += 1
S:6 T:6 + x  -> del(T + mem) "abcdefgh"
S:7 T:7   h
```