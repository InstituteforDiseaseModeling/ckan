# This file is used as a starting point for debugging from IDE (for example from PyCharm).
import re
import sys

from paste.script.command import run

if __name__ == u'__main__':
    sys.argv[0] = re.sub(ur'(-script\.pyw?|\.exe)?$', u'', sys.argv[0])
    sys.exit(run())
