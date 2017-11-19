import os
import sys
import subprocess
import time
import unittest
from setuptools import setup, find_packages

RELEASE = "0.9"

File = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
if os.getenv("BUILD", "false").lower() == "true":
  # First compile Coconut down to Python 3 source
  print("Transpiling Coconut for packaging...")
  assert 0 == os.system("coconut --target 3 --line-numbers sos%ssos.coco" % os.sep)
  assert 0 == os.system("coconut --target 3 --line-numbers sos%stests.coco" % os.sep)

  if os.path.exists(".git"):
    try:
      p = subprocess.Popen("git describe --always", shell = sys.platform != 'win32', bufsize = 1, stdout = subprocess.PIPE)  # use tag or hash
      so, se = p.communicate()
      extra = (so.strip() if sys.version_info.major < 3 else so.strip().decode(sys.stdout.encoding)).replace("\n", "-")
      if "\x0d" in extra: extra = extra.split("\x0d")[1]
      print("Found Git hash %s" % extra)  # TODO use logging module instead
    except: extra = "svn"
  else: extra = "svn"
  md = time.localtime()
  version = (md.tm_year, (10 + md.tm_mon) * 100 + md.tm_mday, (10 + md.tm_hour) * 100 + md.tm_min)
  versionString = '.'.join(map(str, version))
  with open("sos%sversion.py" % os.sep, "w") as fd:  # create version string at build time
    fd.write("""\
__version_info__ = ({version[0]}, {version[1]}, {version[2]})
__version__ = r'{fullName}'
__release_version__ = '{release}'
  """.format(version = version, fullName = versionString + "-" + extra, release = RELEASE))

  README = "\n".join(["# Subversion Offline Solution (SOS %s) #" % RELEASE] + open(File).read().split("\n")[1:])  # replace title in README.md
  with open(File, "w") as fd: fd.write(README)

  # Ensure unit tests are fine
  from sos import sos, tests  # needed for version strings
  if os.getenv("NOTTEST", "false").lower() == "true":
    testrun = unittest.defaultTestLoader.loadTestsFromModule(tests).run(unittest.TestResult())
    assert len(testrun.errors) == 0
    assert len(testrun.failures) == 0

  # Clean up old binaries for twine upload
  try:
    for file in (f for f in os.listdir("dist") if any([f.endswith(ext) for ext in (".tar.gz", "zip")])):
      try: os.unlink(os.path.join("dist", file))
      except: print("Cannot remove old distribution file " + file)
  except: pass
else:  # install
  from sos import sos
  with open(File, "r") as fd: README = fd.read()

print("Building SOS version " + sos.version.__version__)
setup(  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
  name = 'sos-vcs',
  version = sos.version.__version__.split("-")[0],  # without extra
  install_requires = ["appdirs >= 1.4.3", "chardet >= 3.0.4", "configr >= 2017.2117.2635"],  # all of them are optional dependecies
  test_suite = "tests",  # is this executed automatically? Is also called above
  description = "Subversion Offline Solution (SOS)",
  long_description = README,  # + '\n' + CHANGES,
  classifiers = [c.strip() for c in """
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        Intended Audience :: Other Audience
        Intended Audience :: Science/Research
        Intended Audience :: System Administrators
        Operating System :: OS Independent
        Programming Language :: Python :: 3
        """.split('\n') if c.strip()],  # https://pypi.python.org/pypi?:action=list_classifiers
#        Programming Language :: Coconut
#        License :: Creative Commons Attribution-ShareAlike 4.0
  keywords = 'VCS SCM version control system Subversion Git gitless Fossil Bazaar Mercurial CVS SVN gl fsl bzr hg',
  author = 'Arne Bachmann',
  author_email = 'ArneBachmann@users.noreply.github.com',
  maintainer = 'Arne Bachmann',
  maintainer_email = 'ArneBachmann@users.noreply.github.com',
  url = 'http://github.com/ArneBachmann/configr',
  license = 'CC-BY-SA 4.0',
  packages = ["sos"],
  package_data = {"": ["../LICENSE", "../README", "*.coco"]},
  include_package_data = False,  # if True, will *NOT* package the data!
  zip_safe = False,
  entry_points = {
    'console_scripts': [
      'sos=sos.sos:main',
      'vcos=sos.sos:main'
    ]
  },
#  extras_require = {
#    'key1':  ["library>=version", "option"],
#    'key2': ["library>=version"]
#  }
)
