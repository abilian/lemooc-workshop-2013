from flask.ext.flatpages import FlatPages
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


flatpages = FlatPages()
db = SQLAlchemy()
login_manager = LoginManager()


def setup(app):
  flatpages.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)