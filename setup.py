import os, shutil, subprocess, sys, time, unittest
from setuptools import setup, find_packages

RELEASE = "1.0.1"

readmeFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
if 'build' in sys.argv:
  print("Transpiling Coconut for packaging...")
  if not os.path.exists("build"):
    try: os.mkdir("build")
    except: print("Cannot create build folder")
  cmd = "-develop" if os.getenv("NODEV", "false").strip().lower() != "true" or 0 == subprocess.Popen("coconut-develop --help", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 10000000).wait() else ""

  assert 0 == os.system("coconut%s -p -l -t 3 sos%ssos.coco" % (cmd, os.sep))  # TODO remove target once Python 2 problems have been fixed
  assert 0 == os.system("coconut%s -p -l -t 3 sos%sutility.coco" % (cmd, os.sep))
  assert 0 == os.system("coconut%s -p -l -t 3 sos%stests.coco" % (cmd, os.sep))

  if os.path.exists(".git"):
    print("Preparing documentation for PyPI by converting from Markdown to reStructuredText via pandoc")
    try:
      so, se = subprocess.Popen("git describe --always", shell = sys.platform != 'win32', bufsize = 1, stdout = subprocess.PIPE).communicate()  # use tag or hash
      extra = (so.strip() if sys.version_info.major < 3 else so.strip().decode(sys.stdout.encoding)).replace("\n", "-")
      if "\x0d" in extra: extra = extra.split("\x0d")[1]
      print("Found Git hash %s" % extra)
    except: extra = "svn"
  else: extra = "svn"
  lt = time.localtime()
  version = (lt.tm_year, (10 + lt.tm_mon) * 100 + lt.tm_mday, (10 + lt.tm_hour) * 100 + lt.tm_min)
  versionString = '.'.join(map(str, version))
  with open("sos%sversion.py" % os.sep, "w") as fd:  # create version string at build time
    fd.write("""\
__version_info__ = ({version[0]}, {version[1]}, {version[2]})
__version__ = r'{fullName}'
__release_version__ = '{release}'""".format(version = version, fullName = versionString + "-" + extra, release = RELEASE))

  README = "\n".join(["# Subversion Offline Solution (SOS %s) #" % RELEASE] + open(readmeFile).read().split("\n")[1:])  # replace title in original README file
  with open(readmeFile, "w") as fd: fd.write(README)
  assert 0 == os.system("pandoc --from=markdown --to=rst --output=README.rst README.md")
  if not os.path.exists("README.rst"): shutil.copy("README.md", "README.rst")  # just to let the tests pass on CI

  import sos.sos as sos

if 'sdist' in sys.argv:
  print("Cleaning up old archives for twine upload")
  if not os.path.exists("dist"):
    try: os.mkdir("dist")
    except: print("Cannot create dist folder")
  if os.path.exists("dist"):
    rmFiles = list(sorted(os.listdir("dist")))
    try:
      for file in (f for f in (rmFiles if 'build' in sys.argv else rmFiles[:-1]) if any([f.endswith(ext) for ext in (".tar.gz", "zip")])):
        print("Removing old sdist archive %s" % file)
        try: os.unlink(os.path.join("dist", file))
        except: print("Cannot remove old distribution file " + file)
    except: pass

if 'build' not in sys.argv:
  import sos.version  # was already generated during build phase
  with open(readmeFile, "r") as fd: README = fd.read()

print("\nRunning setup() for SOS version " + sos.version.__version__)
setup(
  name = 'sos-vcs',
  version = sos.version.__version__.split("-")[0],  # without extra
  install_requires = ["appdirs >= 1.4.3", "chardet >= 3.0.4", "configr >= 2017.2129.2820", "termwidth >= 2017.2204.2811"],  # all of them are optional dependencies, also coconut-develop>=1.3.1.post0.dev8
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
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: 3 :: Only
        """.split('\n') if c.strip()],  # https://pypi.python.org/pypi?:action=list_classifiers
#        Programming Language :: Coconut
  keywords = 'VCS SCM version control system Subversion Git gitless Fossil Bazaar Mercurial CVS SVN gl fsl bzr hg',
  author = 'Arne Bachmann',
  author_email = 'ArneBachmann@users.noreply.github.com',
  maintainer = 'Arne Bachmann',
  maintainer_email = 'ArneBachmann@users.noreply.github.com',
  url = 'http://github.com/ArneBachmann/sos',
  license = 'MPL-2.0',
  packages = find_packages(),  # should return ["sos"], but returns []
  package_dir = {"sos": "sos"},
  package_data = {"": ["../LICENSE", "../README.md", "../README.rst", "*.coco"]},
  include_package_data = False,  # if True, will *NOT* package the data!
  zip_safe = False,
  entry_points = {
    'console_scripts': [
      'sos=sos.sos:main',  # Subversion offline solution
  #    'vcos=sos.sos:main',  # version control offline solution
  #    'mvcs=sos.sos:main'  # meta version control system
    ]
  },
#  extras_require = {
#    'key1':  ["library>=version", "option"],
#    'key2': ["library>=version"]
#  }
)
