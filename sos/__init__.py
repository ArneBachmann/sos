''' Package definition. '''
import sys
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
if sys.version_info.major >= 3:
  from sos.sos import *
  import sos.version
else:  # Python 2
  from sos import *
  import version
