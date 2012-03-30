import os


# Redis settings
REDIS_URL = os.environ.get('REDIS_TO_GO', 'redis://localhost:6379/0')

# Database keys settings
DATABASE_KEY = 'watracest:ragefaces'
DATABASE_EXISTS_KEY = 'watracest:ragefaces-exists'
EXPIRE_TIME = 3600
SESSION_KEY = 'face'

# Site url to parse and user agent to use
SITE_URL = 'http://alltheragefaces.com/sort/new'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) ' \
             'AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 ' \
             'Safari/535.7'

# Secret key (please, set proper value in local settings)
SECRET_KEY = 'OD\xa8\xaf\x12\x9eO\x86\xc3\xa9y\x9a\xb9X3G'


try:
    from settings_local import *
except ImportError:
    pass
