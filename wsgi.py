import os

# Add root dotcloud folder if possible
if os.path.isdir('/home/dotcloud/current'):
    import sys
    sys.path.append('/home/dotcloud/current')

from watracest.app import app as application
