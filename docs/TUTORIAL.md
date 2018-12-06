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

or

```bash
sos help
```


## First steps ##
Say you have a project you work on, but you are  either *a)* using a means of transport without (affordable) internet access, *b)* experiencing a power or network outage, *c)* need VCS functionality for something not yet in a repository or checkout. SOS will be there for you immediately.

For the sake of this tutorial, we assume you are working in a local Subversion checkout.
As I don't know any public SVN platforms to checkout for this repository, instead download and unzip a random project from Github, e.g., [one](https://github.com/ArneBachmann/realestate-sunamount/archive/master.zip) of my small Coconut projects.

Let's start! You are on the train without network connectivity for some reason and want to start working on the (just downloaded) RESE project to improve some code parts.

```bash
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

"Going offline" will create a sub-folder `.sos` that contains a baseline copy of your project.
You can immediately start hacking away and not worry about changing anything beyond repair, as you can always revert your changes to the point in time your started going offline.

You may also use the command line switches `--compress` and `--strict` to enable data compression inside the SOS internals (slow but less data overhead) and change the file change detection to full file hashing instead of only checking size and timestamp.

OK, let's start working. You open your editor and edit a source file inside `realestate-sunamount-master`, e.g. `make.bat` from

```Powershell
@echo off
echo Compiling
...
```

to

```Powershell
@echo off
echo Compiling...
...
```

Before committing your change to the SOS offline-repository just yet, you'd like to see a summary of your changes:

```bash
sos status
```

or, if you prefer a less Git-like and more Fossil-like command,

```bash
sos changes
```

which will show you:

```
MOD ./make.bat
[EXIT]
```

Ok, so we know that `make.bat` has been modified. Let's display the changes in detail:

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

which tells us exactly what was changed from old to new. The pipe symbols mark the beginning and end of each displayed line, so you can also see whitespaces.
