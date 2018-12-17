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
This works similar to `git add --all` as it mirrors all folder tree changes into the repository.
You can also specify a commit message and specify which files to commit:

```bash
sos commit "First change" --only "*.bat"
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
Use 'sos online --force' to erase all aggregated offline revisions.
```

This means that SOS won't let you go back online, i.e., remove the offline repository, until you have secured all your offline work back into the underlying VCS (if any).

You can also check the status of the repository and all its branches:

```bash
sos status --repo
```

or just `sos status`, if the configuration setting `useChangesCommand` is turned **on**:

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

Here you see (after some repository internals), that the only branch is marked as **modified**, which means it has been changed since you went offline and wasn't committed to the underlying VCS yet (after coming back online).
Make sure you don't forget to secure your changes to the underlying VCS you went offline from before issuing `sos online` to remove the offline repository.

But of course there are two more ideas about VCS we need to cover: Branching, rollback and merging.
