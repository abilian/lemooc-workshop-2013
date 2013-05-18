#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask.ext.frozen import Freezer
from flask.ext.markdown import Markdown
from flask.ext.assets import Environment as AssetManager
from flask.ext.babel import Babel
#from raven.contrib.flask import Sentry

from . import config
from .models import setup as setup_models
from .pages import setup as setup_pages


###############################################################################
# Create app and services

app = Flask(__name__, static_path='/static')

# Used for side-effect
from . import views


def setup_app(app):
  app.config.from_object(config)

  setup_pages(app)
  setup_models(app)

  freezer = Freezer(app)
  markdown_manager = Markdown(app)
  asset_manager = AssetManager(app)
  babel = Babel(app)
  #sentry = Sentry(app)
