DEBUG = False
ASSETS_DEBUG = True
FLATPAGES_AUTO_RELOAD = False

BASE_URL = 'http://workshop.lemooc.com/'
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = '../pages'
BABEL_DEFAULT_LOCALE = 'fr'


# App configuration
FEED_MAX_LINKS = 25
SECTION_MAX_LINKS = 12

SECRET_KEY = "CHANGEME"

REDIRECTS = {
}

SQLALCHEMY_DATABASE_URI = "sqlite:///../data/lemooc.db"
SQLALCHEMY_ECHO = False

try:
  from local_config import *
except:
  pass
