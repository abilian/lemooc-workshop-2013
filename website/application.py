#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.frozen import Freezer
from flask.ext.markdown import Markdown
from flask.ext.assets import Environment as AssetManager
from flask.ext.babel import Babel
from flask.ext.bootstrap import Bootstrap
#from raven.contrib.flask import Sentry

from . import config
from .extensions import setup as setup_extensions
from .admin import setup as setup_admin


###############################################################################
# Create app and services

app = Flask(__name__, static_path='/static')

# Used for side-effect
from . import views


def setup_app(app, additional_config=None):
  app.config.from_object(config)
  if additional_config:
    app.config.from_object(additional_config)

  freezer = Freezer(app)
  markdown_manager = Markdown(app)
  asset_manager = AssetManager(app)
  babel = Babel(app)
  bootstrap = Bootstrap(app)
  admin = Admin(app)

  setup_extensions(app)
  setup_admin(app)

  #sentry = Sentry(app)
