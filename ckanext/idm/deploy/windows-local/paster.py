# This file is used as a starting point for debugging from IDE (for example from PyCharm).
import re
import sys

from paste.script.command import run

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(run())
