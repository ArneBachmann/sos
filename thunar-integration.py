import logging, os, stat, sys, time, xml.dom.minidom
assert sys.platform != "win32"

logging.basicConfig(
  level = logging.DEBUG if '--debug' in sys.argv or os.environ.get('DEBUG', "False").lower() == "true" else logging.INFO,
  stream = sys.stdout,
  format = "%(asctime)-25s %(levelname)-8s %(name)-12s:%(lineno)d | %(message)s")
_log = logging.getLogger(__name__); debug, info, warn, error = _log.debug, _log.info, _log.warning, _log.error


def escapeSpaces(bites):
  return bites.replace(b" ", br"\ ")


# Constants
SOS_DIR = os.path.abspath(os.path.dirname(__file__))
ICON_PATH = os.path.join(SOS_DIR, "extras", "logo.png")
TIMESTAMP = int(round(1000.0 * time.time()))

EMPTY_XML = b"""<?xml version="1.0" encoding="UTF-8"?>\n<actions>\n</actions>"""
FOR_FILES = "\n\t".join([b"\n\t<audio-files/>", b"<image-files/>", b"<other-files/>", b"<text-files/>", b"<video-files/>"])
FOR_DIRS = b"\n\t<directories/>"

COMMANDS = {  # TODO if called on folders not part of a SOS repo, then window may close immediately due to SVN or Git picking up the action

  # Folders
  b"Changes": (1, False, b"""xfce4-terminal --title=%s --fullscreen --working-directory=%%f -x sos changes --wait""" % (escapeSpaces("SOS Changes"))),
  b"Commit":  (2, False, b"""xfce4-terminal --title=%s --fullscreen --working-directory=%%f -x sos commit --wait""" % escapeSpaces("SOS Commit")),
  b"Diff":    (3, False, b"""xfce4-terminal --title=%s --fullscreen --working-directory=%%f -x sos diff --wait""" % escapeSpaces("SOS Diff")),
  b"Log":     (4, False, b"""xfce4-terminal --title=%s --fullscreen --working-directory=%%f -x sos log --changes -n 5 --wait""" % escapeSpaces("SOS Log")),
  b"Offline": (5, False, b"""xfce4-terminal --title=%s --fullscreen --working-directory=%%f -x %s/extras/offline.sh""" % (escapeSpaces("SOS Offline"), escapeSpaces(SOS_DIR))),
  b"Status":  (6, False, b"""xfce4-terminal --title=%s --fullscreen --working-directory=%%f -x sos status --progress --wait""" % escapeSpaces("SOS Status")),

  # Single files
  b"Diff":    (7, True,  b"""xfce4-terminal --title=%s --fullscreen --working-directory=%%d -x %s/extras/difffile.sh "%%f" """ % (escapeSpaces("SOS Diff"), escapeSpaces(SOS_DIR))),
  b"Ignore":  (8, True,  b"""xfce4-terminal --title=%s --fullscreen --working-directory=%%d -x sos config add ignores "%%f" --wait""" % escapeSpaces("SOS Ignore"))
}  # alternative: cd %%f && xterm +j -title %s -fullscreen -e sos changes --wait


# Functions
def createEntry(name, index, forFiles, command):
  ''' Returns one action entry. '''
  x = template.format(
      name = name,
      command = command,  # escaped by XML formatter
      icon = ICON_PATH,
      timestamp = "%d-%d" % (TIMESTAMP, index),
      targets = FOR_FILES if forFiles else FOR_DIRS
    ).replace("&", "&amp;")
  return xml.dom.minidom.parseString(x).childNodes[0].childNodes[1:3]



# Main code
if __name__ == '__main__':
  with open(os.path.join(SOS_DIR, "thunar-integration.template"), "rb") as fd: template = fd.read()
  for file in ("difffile.sh", "offline.sh"):
    try: os.chmod(os.path.join(SOS_DIR, "extras", file), os.stat(os.path.join(SOS_DIR, "extras", file)).st_mode | stat.S_IXUSR | stat.S_IXGRP)
    except Exception as E: error("Cannot set execute permissions for service scripts under extras/ %r" % E)

  thunarConfigFile = os.path.expanduser("~/.config/Thunar/uca.xml")
  assert "~" not in thunarConfigFile

  if os.path.exists(thunarConfigFile):
    info("Loading Thunar user interface configuration %r" % thunarConfigFile)
    with open(thunarConfigFile, "rb") as fd: thunarConfig = fd.read()
    if thunarConfig.split(b"\n")[0] == b"""<?xml encoding="UTF-8" version="1.0"?>""":  # Thunar uses non-conformant attribute order for XML header!
      info("Fixing non-conformant Thunar config file XML header")
      with open(thunarConfigFile, "wb") as fd: fd.write(b"\n".join([b"""<?xml version="1.0" encoding="UTF-8"?>"""] + thunarConfig.split(b"\n")[1:]))
    dom = xml.dom.minidom.parse(thunarConfigFile)
  else:
    dom = xml.dom.minidom.parseString(EMPTY_XML)

  # Remove previous SOS commands
  actions = dom.childNodes[0].childNodes  # actions->action
  removes = []
  for action in actions:
    if action.nodeType == action.ELEMENT_NODE and action.nodeName == b"action" and action.getElementsByTagName("name")[0].childNodes[0].nodeValue.startswith(b"SOS"):
      info("Clearing old SOS entry")
      before = action.previousSibling
      if before.nodeType == before.TEXT_NODE:
        debug("Clearing also text separator")
        removes.append(before)  # also remove textual separator
      removes.append(action)
  for remove in removes: dom.childNodes[0].removeChild(remove)

  # Add new SOS commands
  last = dom.childNodes[0].childNodes[-1]  # last text node. insertion order is relevant for display in Thunar
  for name, data in sorted(COMMANDS.items(), key = lambda a: a[1][0]):  # sorted by index
    info("Adding SOS action entry")
    action = createEntry(name, *data)
    node = dom.importNode(action[0], True)
    text = dom.importNode(action[1], True)
    dom.childNodes[0].insertBefore(node, last)
    dom.childNodes[0].insertBefore(text, last)
  with open(thunarConfigFile, "wb") as fd: fd.write(dom.toxml().replace(b"""<?xml version="1.0" ?>""", b"""<?xml version="1.0" encoding="UTF-8"?>\n"""))
