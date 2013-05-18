#!/usr/bin/env python
# coding=utf-8

import codecs
import os
import datetime

from argh import *

from flask import Flask
from flask.ext.frozen import Freezer
from flask.ext.markdown import Markdown
from flask.ext.assets import Environment as AssetManager
from flask.ext.babel import Babel
#from raven.contrib.flask import Sentry


from .pages import slugify, setup as setup_pages
from .models import setup as setup_models
from .config import *


###############################################################################
# Create app and services

app = Flask(__name__)
app.config.from_object(__name__)

setup_pages(app)
setup_models(app)

freezer = Freezer(app)
markdown_manager = Markdown(app)
asset_manager = AssetManager(app)
babel = Babel(app)
#sentry = Sentry(app)


###############################################################################
# Commands

# Not used (yet?)
@command
def post(section, title=None, filename=None):
  """ Create a new empty post.
  """
  if not os.path.exists(os.path.join(FLATPAGES_ROOT, section)):
    raise CommandError(u"Section '%s' does not exist" % section)
  post_date = datetime.datetime.today()
  title = unicode(title) if title else "Untitled Post"
  if not filename:
    filename = u"%s.md" % slugify(title)
  year = post_date.year
  pathargs = [section, str(year), filename, ]
  filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          FLATPAGES_ROOT, '/'.join(pathargs))
  if os.path.exists(filepath):
    raise CommandError("File %s exists" % filepath)
  content = '\n'.join([
    u"title: %s" % title,
    u"date: %s" % post_date.strftime("%Y-%m-%d"),
    u"published: false\n\n",
  ])
  try:
    codecs.open(filepath, 'w', encoding='utf8').write(content)
    print(u'Created %s' % filepath)
  except Exception, error:
    raise CommandError(error)


@command
def serve(server='0.0.0.0', port=7100):
  """ Serves this site.
  """
  debug = app.config['DEBUG'] = app.debug = True
  #asset_manager.config['ASSETS_DEBUG'] = debug
  app.run(host=server, port=port, debug=debug)


if __name__ == '__main__':
  parser = ArghParser()
  parser.add_commands([serve, post])
  parser.dispatch()
