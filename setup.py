# Copyright Arne Bachmann
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Options: clean build release sdist --mypy --force test --log cover --verbose test checkdocs


import os, shutil, subprocess, sys, time
from setuptools import setup, find_packages

COMPATIBILITY_LEVEL = "3.4"

readmeFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
with open("RELEASE", "r") as fd: RELEASE = fd.read()
if 'release' in sys.argv:
  with open("RELEASE", "w") as fd: fd.write(".".join(RELEASE.split(".")[:2] + [str(int(RELEASE.split(".")[2]) + 1)]))
  with open("RELEASE", "r") as fd: RELEASE = fd.read()
  print("New revision is %s" % RELEASE)
  sys.exit(0)

if 'build' in sys.argv:
  if os.environ.get("CI", "False").lower() != "true":  # code only run locally, not on CI
    print("Transpiling Coconut files to Python...")
    cmd = "-develop" if 0 == subprocess.Popen("coconut-develop --help", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 1000000).wait() and os.getenv("NODEV", "false").strip().lower() != "true" else ""
    if "--mypy" in sys.argv:
      try: shutil.rmtree(".mypy_cache/")
      except: pass
    assert 0 == os.system("coconut%s %s %s -l -t %s -j sys sos%s" % (cmd, "-p" if not "--mypy" in sys.argv else "", "--force" if "--force" in sys.argv else "", COMPATIBILITY_LEVEL, (" --mypy --ignore-missing-imports --warn-incomplete-stub --warn-redundant-casts --python-version %s" % COMPATIBILITY_LEVEL) if "--mypy" in sys.argv else ""))  #  or useChanges
  if "--mypy" in sys.argv:  sys.argv.remove('--mypy')
  if "--force" in sys.argv: sys.argv.remove('--force')

  if os.path.exists(".git"):  # must be local development, but ignored
    try:
      so, se = subprocess.Popen("git describe --always", shell = sys.platform != 'win32', bufsize = 1, stdout = subprocess.PIPE).communicate()  # use tag or hash
      extra = so.strip().decode(sys.stdout.encoding).replace("\n", "-")
      if "\x0d" in extra: extra = extra.split("\x0d")[1]
      print("Found Git hash %s" % extra)
    except: extra = "svn"
  else: extra = "svn"  # in case this is checked out and built not from Github
  lt = time.localtime()
  version = (lt.tm_year, (10 + lt.tm_mon) * 100 + lt.tm_mday, (10 + lt.tm_hour) * 100 + lt.tm_min)  # NO don't generate new version when using --dev option (to allow "pip install -e .") - was actually a mis-installation
  versionString = '.'.join(map(str, version))
  with open("sos%sversion.py" % os.sep, "w") as fd:  # create version string at build time
    fd.write("""\
__version_info__ = ({version[0]}, {version[1]}, {version[2]})
__version__ = r'{fullName}'
__release_version__ = '{release}'""".format(version = version, fullName = versionString + "-" + extra, release = RELEASE))

  README = "\n".join(["# SOS v%s #" % RELEASE] + open(readmeFile, "r", encoding = "utf-8").read().split("\n")[1:])  # replace title in original README.md file
  with open(readmeFile, "w", encoding = "utf-8") as fd: fd.write(README.replace("\r", ""))
  print("Preparing documentation for PyPI by converting from Markdown to reStructuredText via pandoc")
  if 0 != subprocess.Popen("pandoc --from=markdown --to=rst --output=README.rst README.md", shell = True, bufsize = 1).wait(): print("Warning: Cannot run pandoc")
  if not os.path.exists("README.rst"): shutil.copy("README.md", "README.rst")  # just to continue

if 'test' in sys.argv:
  import logging  # manual setup of logger in current main thread
  logging.basicConfig(level = logging.DEBUG, stream = sys.stderr, format = "%(asctime)-23s %(levelname)-8s %(name)s:%(lineno)d | %(message)s" if '--log' in sys.argv else "%(message)s")
  sys.argv.append("--verbose")
  sys.argv.pop()  # remove --verbose flag
  print("Warning: Won't create distribution archive after running unit tests")

if 'sdist' in sys.argv:
  print("Cleaning up old archives for twine upload")
  if os.path.exists("dist"):
    rmFiles = list(sorted(os.listdir("dist")))
    try:
      for file in (f for f in rmFiles if any([f.endswith(ext) for ext in (".tar.gz", "zip")])):
        print("Removing old sdist archive %s" % file)
        try: os.unlink(os.path.join("dist", file))
        except: print("Cannot remove old distribution file " + file)
    except: pass

if 'cover' in sys.argv:
  sys.argv.remove('cover')
  if 'test' in sys.argv: sys.argv.remove('test')
  if 0 != os.system("coverage run --branch --debug=sys --source=sos sos/tests.py && coverage html && coverage annotate sos/tests.py"):
    print("Cannot create coverage report when tests fail")

if 'checkdocs' in sys.argv:
  try: import collective.checkdocs
  except: raise Exception("Setup requires the pip package 'collective.checkdocs'")

import sos.version

with open(readmeFile.split(".")[0] + ".rst", "r", encoding = "utf-8") as fd: README = fd.read()
print("\nRunning setup() for SOS version " + sos.version.__version__)
setup(
  name = 'sos-vcs',
  version = sos.version.__version__.split("-")[0],  # without extra
  install_requires = ["chardet>=3.0.4", "wcwidth", "configr>=2018.2004.2239", "termwidth>=2019.1125.2909", "PyFiglet>=0.7.5", 'colorama>=0.3.9;sys_platform=="win32"', 'enum34;python_version<"3.4"'],  # most of them are optional dependencies
  python_requires = '>=%s' % COMPATIBILITY_LEVEL,  # https://www.python.org/dev/peps/pep-0508/#environment-markers
  setup_requires = "setuptools >= 39",
#  requires = ["coconut-develop[cPyparsing,jobs,mypy-mypyc]"],  # doesn't work
  test_suite = "sos.tests",
  description = "Subversion Offline Solution (SOS)",
  long_description = README,
  classifiers = [c.strip() for c in """
        Development Status :: 5 - Production/Stable
        License :: Free To Use But Restricted
        Intended Audience :: Developers
        Intended Audience :: Other Audience
        Intended Audience :: Science/Research
        Intended Audience :: System Administrators
        License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
        Operating System :: OS Independent
        Programming Language :: Other
        Programming Language :: Python
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: 3 :: Only
        """.split('\n') if c.strip()],  # https://pypi.python.org/pypi?:action=list_classifiers
  #      Programming Language :: Coconut
  keywords = 'VCS SCM version control system Subversion Git gitless Fossil Bazaar Mercurial CVS SVN gl fsl bzr hg',
  author = 'Arne Bachmann',
  author_email = 'ArneBachmann@users.noreply.github.com',
  maintainer = 'Arne Bachmann',
  maintainer_email = 'ArneBachmann@users.noreply.github.com',
  url = 'http://github.com/ArneBachmann/sos',
  license = 'MPL-2.0',
  packages = find_packages(),  # should return ["sos"], but returns []
  package_dir = {"sos": "sos"},
  package_data = {"": ["../LICENSE", "../*.md", "../README.rst", "*.coco", "docs/*.md"]},  # *.py is included in any case
  include_package_data = False,  # if True, will *NOT* package the data!
  zip_safe = False,  # TODO re-add and test extras section for backport = enum34
  extras_require = { ':python_version < "3.5"': 'typing >= 3.5.3' },
  entry_points = {
    'console_scripts': [
      'sos=sos.sos:main'  # Subversion offline solution
    ]
  }
)
