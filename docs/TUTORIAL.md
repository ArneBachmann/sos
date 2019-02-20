# SOS Tutorial #

The purpose of this tutorial is to give a quick start into working with SOS, highlight some of its features, and explain the rationale behind some of its differences to other version control systems.


## Getting started ##
First, you need to install SOS and make it available in your system path. This is best done using the `pip` (or `pip3`) command of your Python distribution. If you don't have Python installed, do so using your system's package manager or by downloading and installing it from `https://www.python.org/downloads/` or, e.g., `https://conda.io/miniconda.html`.

Installing SOS through pip works like that:

```bash
pip install sos-vcs
```

This will install SOS and all its required software packages into your global Python distribution. If you want to test SOS first in a virtual environment, make sure your have a conda-supporting Python distribution with an activated virtual Python environment and run the `pip` command from there.

Once installed, confirm that everything is fine via

```bash
sos version
```

which shows something like

```
 ,---.          ,--.                                ,--.                 ,-----.  ,---. ,---.,--.,--.                 ,---.         ,--.          ,--.  ,--.
'   .-' ,--.,--.|  |-.,--.  ,--.,---. ,--.--. ,---. `--' ,---. ,--,--,  '  .-.  '/  .-'/  .-'|  |`--',--,--,  ,---.  '   .-'  ,---. |  |,--.,--.,-'  '-.`--' ,---. ,--,--,
`.  `-. |  ||  || .-. '\  `'  /| .-. :|  .--'(  .-' ,--.| .-. ||      \ |  | |  ||  `-,|  `-,|  |,--.|      \| .-. : `.  `-. | .-. ||  ||  ||  |'-.  .-',--.| .-. ||      \
.-'    |'  ''  '| `-' | \    / \   --.|  |   .-'  `)|  |' '-' '|  ||  | '  '-'  '|  .-'|  .-'|  ||  ||  ||  |\   --. .-'    |' '-' '|  |'  ''  '  |  |  |  |' '-' '|  ||  |
`-----'  `----'  `---'   `--'   `----'`--'   `----' `--' `---' `--''--'  `-----' `--'  `--'  `--'`--'`--''--' `----' `-----'  `---' `--' `----'   `--'  `--' `---' `--''--'

/SOS/ Subversion Offline Solution V1.6.9 (C) Arne Bachmann (PyPI: 2018.2206.2757-v1.6.0-72-ge98aaa4)
```


## First steps ##
Say you have a project you work on, but you are either **a)** using a means of transport without (affordable) internet access, **b)** experiencing a power or network outage, **c)** in need of VCS functionality for something not yet in a repository or checkout.
SOS will support you in any case.

For the sake of this tutorial, we assume you are working in a local Subversion checkout.
As I don't know any public SVN platforms to checkout from for this tutorial, **download** and **unzip** a random project from Github instead, e.g., [this one](https://github.com/ArneBachmann/realestate-sunamount/archive/master.zip), a small Coconut project.

Let's start! Imagine you are taking a train without network connectivity for some reason and want to start working on the (just downloaded) RESE project to improve some code parts. In the shell type this:

```bash
cd realestate-sunamount-master
sos offline
```

This command will create an output similar to the following one:

```
 ,---.          ,--.                                ,--.                 ,-----.  ,---. ,---.,--.,--.                 ,---.         ,--.          ,--.  ,--.
'   .-' ,--.,--.|  |-.,--.  ,--.,---. ,--.--. ,---. `--' ,---. ,--,--,  '  .-.  '/  .-'/  .-'|  |`--',--,--,  ,---.  '   .-'  ,---. |  |,--.,--.,-'  '-.`--' ,---. ,--,--,
`.  `-. |  ||  || .-. '\  `'  /| .-. :|  .--'(  .-' ,--.| .-. ||      \ |  | |  ||  `-,|  `-,|  |,--.|      \| .-. : `.  `-. | .-. ||  ||  ||  |'-.  .-',--.| .-. ||      \
.-'    |'  ''  '| `-' | \    / \   --.|  |   .-'  `)|  |' '-' '|  ||  | '  '-'  '|  .-'|  .-'|  ||  ||  ||  |\   --. .-'    |' '-' '|  |'  ''  '  |  |  |  |' '-' '|  ||  |
`-----'  `----'  `---'   `--'   `----'`--'   `----' `--' `---' `--''--'  `-----' `--'  `--'  `--'`--'`--''--' `----' `-----'  `---' `--' `----'   `--'  `--' `---' `--''--'
ADD ./.gitignore  (1157 bytes)
ADD ./LICENSE  (16.33 KiB)
ADD ./README.md  (1.34 KiB)
ADD ./__coconut__.py  (26.10 KiB)
ADD ./example.coco  (3.54 KiB)
ADD ./example.py  (4.58 KiB)
ADD ./make.bat  (332 bytes)
ADD ./make.sh  (364 bytes)
ADD ./setup.py  (2.28 KiB)
ADD ./sunamount.md  (12.18 KiB)
ADD rese/__coconut__.py  (26.10 KiB)
ADD rese/__init__.py  (0 bytes)
ADD rese/sunamount.coco  (15.63 KiB)
ADD rese/sunamount.py  (21.95 KiB)
Processing speed was 15.02 MiB/s.
/SOS/ Offline repository prepared. Use 'sos online' to finish offline work
[EXIT]
```

By "going offline" this way a sub-folder `.sos` will be created that contains a baseline copy of your project.
You can immediately start hacking away and not worry about changing anything beyond repair, as you can always revert your changes to the point in time you started going offline or did your last `commit`.

You may also use the command line switches `--compress` and `--strict` to enable data compression inside the SOS internals (slow but less data overhead) and change the file change detection method to full file contents hashing instead of relying on size and timestamp only.

OK, let's start working. You open your editor and edit a source file inside `realestate-sunamount-master`, e.g. `make.bat` from:

```Powershell
@echo off
echo Compiling
...
```

to this:

```Powershell
@echo off
echo Compiling...
...
```

Satisfied with your improvement, you want to commit your change to the local offline SOS history to make a snapshot of your work that you can later refer to or go back to.
But before committing your change just yet, you'd like to see a summary of your changes to confirm everything's alright:

```bash
sos status
```

or, if you prefer a less Git-like and more Fossil-like command:

```bash
sos config set useChangesCommand on
sos changes
```

which will show you:

```
MOD ./make.bat
[EXIT]
```

The first defines a user-global SOS configuration setting unless using `--local` which would apply to the current checkout only (in contrast to what Git does via `--global`).
The useChangesCommand setting determines the behavior of the `status` command to show the repository stats instead of the checkout status (if `off` use `status --repo[sitory]` to show the stats).

Ok, so we know that `make.bat` has been modified. Let's display the changes in more detail:

```bash
sos diff
```

will show:

```
DIF ./make.bat  <LF>
old 1 |echo Compiling|
now 1 |echo Compiling...|

[EXIT]
```

which tells us exactly on what line what was changed from old to new.
The pipe symbols mark the beginning and end of each displayed line, so you can also notice trailing whitespaces.

It's now time to commit our change.
SOS was designed with minimal barriers in mind, therefore you can simply do:

```bash
sos commit
```

or `sos ci` or `sos com`.
This works similar to `git add --all && git commit -m ""` as it mirrors all folder tree changes into the repository.
You can also specify a commit message, and specify which files to commit or not exclude:

```bash
sos commit "First change" --only "*.bat" --except "*.cmd"
```

which shows the following output:

```
MOD ./make.bat
Processing speed was 177.47 kiB/s.
/SOS/ Created new revision r01 'First change' (+00/-00/±01/⇌00) summing 507 bytes in 1 files (33.93% SOS overhead)
```

The output is a condensed summary of changes.
It shows the created revision's number `01`, the commit message, the number of added, removed, modified and moved files, the number of bytes and files processed, and the percentage of metadata overhead occupied by SOS to manage the offline repository, which is usually less than one percent.

To get an overview of the recent SOS commit history:

```bash
sos log
```

which shows:

```
/SOS/ Offline commit history of branch 'trunk'
    r0 @2018-12-06 23:26:29 (+14/-00/±00/T00) |Offline repository created on 2018-12-06 23:26:29|
  ➙ r1 @2018-12-07 15:11:08 (+00/-00/±01/T01) |First change|
[EXIT 0.0s]
```

Or even:

```bash
sos log --changes`
```

which also shows the files modifed in each commit:

```
/SOS/ Offline commit history of branch 'trunk'
    r0 @2018-12-06 23:26:29 (+14/-00/±00/T00) |Offline repository created on 2018-12-06 23:26:29|
ADD ./.gitignore  (-)
ADD ./LICENSE  (-)
ADD ./README.md  (-)
ADD ./__coconut__.py  (-)
ADD ./example.coco  (-)
ADD ./example.py  (-)
ADD ./make.bat  (-)
ADD ./make.sh  (-)
ADD ./setup.py  (-)
ADD ./sunamount.md  (-)
ADD rese/__coconut__.py  (-)
ADD rese/__init__.py  (-)
ADD rese/sunamount.coco  (-)
ADD rese/sunamount.py  (-)
  ➙ r1 @2018-12-07 15:11:08 (+00/-00/±01/T01) |First change|
MOD ./make.bat
[EXIT]
```

You can work this way as long as you want and record regular snapshots of your work until you want to go back online:

```bash
sos online
```

which tells you something important:

```
[EXIT There are still unsynchronized (modified) branches.]
Use 'sos log' to list them.
Use 'sos commit' and 'sos switch' to commit out-of-sync branches to your VCS before leaving offline mode.
Use 'sos online --force' to erase all aggregated offline revisions without further action.
```

This means that SOS won't let you go back online, i.e., remove the offline repository, until you have secured all your offline work back into the underlying VCS (if any).

You can also check the status of the repository and all its branches:

```bash
sos status --repo
```

or just `sos status`, if the configuration setting `useChangesCommand` has been turned **on** (locally or globally):

```
/SOS/ Offline repository status
Repository root:     /home/ash/Desktop/realestate-sunamount-master
Underlying VCS root: None
Underlying VCS type: None
Installation path:   /home/ash/Desktop/all/projects/sos
Current SOS version: 2018.2207.2518-v1.6.0-77-g396bea8
At creation version: 2018.2206.2757-v1.6.0-72-ge98aaa4
Metadata format:     2
Content checking:    size & timestamp
Data compression:    deactivated
Repository mode:     simple
Number of branches:  1
✔ File tree is unchanged
  * b0 'trunk' @2018-12-06 23:26:29 (modified) with 2 commits, using 0.13 MiB (+2.001% SOS overhead). Last comment: 'First change'
[EXIT]
```

Here you see (after some repository internals), that the only branch is marked as **modified**, which means it has been changed since you went offline and wasn't committed to the underlying VCS yet, i.e., using the `sos publish` command.
Make sure you don't forget to secure your changes to the underlying VCS you went offline from before issuing `sos online` to remove the offline repository. You can also use SOS to do that, using `sos commit --vcs -m "Message"` to trigger a underlying VCS commit and clear the dirty flag.


## Branching ##

This section explains how to rollback changes and how to work on different branches while offline.

Let's say we suddenly get the inspiration to work on another idea, but want to pick up work were we left.
This is were branching comes into play:

```bash
sos branch --fast
```

which shows:

```
ADD ./.gitignore  (1157 bytes)
ADD ./LICENSE  (16.33 KiB)
ADD ./README.md  (1.34 KiB)
ADD ./__coconut__.py  (26.10 KiB)
ADD ./example.coco  (3.54 KiB)
ADD ./example.py  (4.58 KiB)
ADD ./make.bat  (335 bytes)
ADD ./make.sh  (364 bytes)
ADD ./setup.py  (2.28 KiB)
ADD ./sunamount.md  (12.18 KiB)
ADD rese/__coconut__.py  (26.10 KiB)
ADD rese/__init__.py  (0 bytes)
ADD rese/sunamount.coco  (15.63 KiB)
ADD rese/sunamount.py  (21.95 KiB)
Processing speed was 15.95 MiB/s.
/SOS/ Switched to new unnamed branch b1
[EXIT]
```

A new branch was created, and you have been switched to work on it, as you can see by:

```bash
sos status
```

that confirms:

```
/SOS/ Offline repository status
...
Number of branches:  2
✔ File tree is unchanged
    b0 'trunk' @2018-12-06 23:26:29 (modified) with 2 commits, using 0.13 MiB (+2.001% SOS overhead). Last comment: 'First change'
  * b1         @2018-12-20 17:54:11 (modified) with 1 commits, using 0.13 MiB (+1.796% SOS overhead). Last comment: 'Branched from file tree after b0/r01'
[EXIT]
```

OK, we work on that new branch and make a change in `rese/sunamount.coco` and move the `import sys` statement to the top of the file:

```bash
sos diff
```
shows accordingly:

```
MOD rese/sunamount.coco <binary>
```

It seems that SOS treated the Coconut source file as binary.
We will tell SOS to treat `*.coco` files globally as textual files and repeat:

```bash
sos config add texttype "*.coco" --local
sos diff
```

shows finally:

```
DIF rese/sunamount.coco  <LF>
+++ 011 |import sys|

--- 274 |  import sys|

[EXIT]
```

OK, the import statement has been removed from line 274 and inserted before line 11 (0-based) or inserted after line 11 (1-based). TODO check
We can now commit the changes and go back to our original branch to continue working there:

```bash
sos commit "Moved import statement"
sos log
sos status
```

```
/SOS/ Offline commit history of branch None
    r0 @2018-12-20 17:54:11 (+14/-00/±00/T00) |Branched from file tree after b0/r01|
  ➙ r1 @2018-12-20 18:03:41 (+00/-00/±01/T01) |Moved import statement|
[EXIT]

SOS/ Offline repository status
...
✔ File tree is unchanged
    b0 'trunk' @2018-12-06 23:26:29 (modified) with 2 commits, using 0.13 MiB (+2.001% SOS overhead). Last comment: 'First change'
  * b1         @2018-12-20 17:54:11 (modified) with 2 commits, using 0.15 MiB (+1.794% SOS overhead). Last comment: 'Moved import statement'
[EXIT]
```

```bash
sos switch 0
```

or `sos switch master`:

```
MOD rese/sunamount.coco
/SOS/ Switched to branch 'master' b0/r01
[EXIT]
```

You can see that the switch modified the source file that we modified back to its original state.
We might now decide that we even want to go back to the original project state on the trunk branch.
This rollback is also performed by the switch command:

```bash
sos switch /0
```

will restore the current branch's initial state, which - in case of the first branch - is the state when we went offline:

```
MOD ./make.bat
/SOS/ Switched to branch 'trunk' b0/r00
[EXIT]
```

When you call changes and status, you'll see a major difference to other VCS and something stemming from SOS's simple data model:

```bash
sos ch

sos status --repository
```

```
MOD ./make.bat <older than previously committed>
[EXIT]

/SOS/ Offline repository status
...
✖ File tree has changes
  * b0 'trunk' @2018-12-06 23:26:29 (modified) with 2 commits, using 0.13 MiB (+2.001% SOS overhead). Last comment: 'First change'
    b1         @2018-12-20 17:54:11 (modified) with 2 commits, using 0.15 MiB (+1.794% SOS overhead). Last comment: 'Moved import statement'
[EXIT]
```

You can see that the `make.bat` file is recognized as modified, also that SOS determined it to be older than a recent commit (by file modification timestamp).
The reason for marking the file as modified is that SOS compares the file tree always against the latest revision of the current branch.
There is no going back to a previous revision and forgetting about the relative future commits like Git can (by resetting its index).
The rationale behind it is that most work is sequential.

If were to make a change now - from the file tree at branch/revision 0/0, it would be added as revision 2 of branch 0.
Go ahead and change `rese/sunamount.coco` to import the `logging` module right before the `import time` statement:

```bash
sos diff
```

Which results in:

```
DIF ./make.bat  <LF>
old 1 |echo Compiling...|
now 1 |echo Compiling|

DIF rese/sunamount.coco  <LF>
+++ 11 |import logging|

[EXIT]
```

The rollback of the make file is marked as a change, and the added import is shown.
We continue and commit:

```bash
sos commit "Added import statement"
sos log
```

```
MOD ./make.bat <older than previously committed>
MOD rese/sunamount.coco
Processing speed was 6.54 MiB/s.
/SOS/ Created new revision r02 'Added import statement' (+00/-00/±02/⇌00) summing 16.31 KiB in 2 files (2.12% SOS overhead)
[EXIT]

/SOS/ Offline commit history of branch 'trunk'
    r0 @2018-12-06 23:26:29 (+14/-00/±00/T00) |Offline repository created on 2018-12-06 23:26:29|
    r1 @2018-12-07 15:11:08 (+00/-00/±01/T01) |First change|
  ➙ r2 @2018-12-20 18:26:12 (+00/-00/±02/T02) |Added import statement|
[EXIT]
```

Ok, we covered branching and rollback.
Now we go to the royal discipline - merging changes into the file tree.

If you want to replay changes from another branch into the current file tree, you would invoke:

```bash
sos update 1

sos diff
```

```
MOD ./make.bat
MOD rese/sunamount.coco
[EXIT]

DIF ./make.bat  <LF>
old 1 |echo Compiling|
now 1 |echo Compiling...|

DIF rese/sunamount.coco  <LF>
old 011 |import logging|
now 011 |import sys|

--- 274 |  import sys|

[EXIT]
```

OK, let's review that. Here, `upgrade` does nothing different than a switch, but doesn't change the current branch.
This is not very useful, since both branches look now completely the same.
To make it worthwhile, check out the documentation for the `update` command:

```bash
sos help update
```

which shows the full variety of options:

```
/SOS/ Subversion Offline Solution

Working with files:
  update [<branch>][/<revision>]  Integrate work from another branch into the file tree without switching the branch
                                  Similarly to switch, this command updates the current file tree to the state of another revision, usually from another branch.
                                  In addition, it allows merging differing contents interactively or by rules specified through command-line switches.
                                  Default operation for files, lines and characters is add and remove (recreate other branch in file tree)

  Arguments:
    [<branch>][/<revision>]  Branch and/or revision

  Options:
    --add             Only add new files (won't remove)
    --add-lines       Only add inserted lines
    --ask             Ask how to proceed with modified files
    --ask-lines       Ask how to proceed with modified lines
    --eol             Use EOL style from the integrated file instead. Default: EOL style of current file
    --except-remotes  Don't operate on specified remote targets
    --no-remotes      Do not operate on any remote targets
    --only-remotes    Only operate on specified remote targets (vs. all configured during 'offline')
    --rm              Only remove vanished files (won't add)
    --rm-lines        Only remove deleted lines
```

You can do this, of course, in combination with file patterns like `--only code/*.py` and do this step by step for each file pattern you like.
Let's go back to where we started and do a more selective `update`:

```bash
sos switch trunk && sos update 1 --only make.bat --ask-lines
```

Which reverts and asks for user input:

```
MOD ./make.bat
MOD rese/sunamount.coco
/SOS/ Switched to branch 'trunk' b0/r02
[EXIT]
Modifications:
- echo Compiling...
+ echo Compiling
 Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input:
```

You can now select to keep your version or change to the referred other branch's version via 't', or both: Type `b` and hit enter.
You can see the merge result:

```bash
sos diff
```

```
DIF ./make.bat  <LF>
+++ 1 |echo Compiling...|

[EXIT]
```

Which shows that the existing `echo Compiling` was augmented by the modified version `echo Compiling...` from the other branch.
