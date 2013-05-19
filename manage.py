#!/usr/bin/env python2.7
# coding: utf-8
from datetime import datetime

from os import mkdir
from os.path import exists
import csv

from flask.ext.script import Manager

from website.application import setup_app, app
from website.models import db, Registration


def create_app():
  setup_app(app)
  return app

manager = Manager(create_app)


@manager.shell
def make_shell_context():
  """
  Updates shell. (XXX: not sure what this does).
  """
  return dict(app=app, db=db)


@manager.command
def dump_routes():
  """
  Dump all the routes declared by the application.
  """
  for rule in app.url_map.iter_rules():
    print rule


@manager.command
def load_data():
  feedback = csv.reader(open("feedback.csv"))
  for row in feedback:
    row = map(lambda x: unicode(x, "utf8"), row)
    date = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S.%f")
    reg = Registration(email=row[0],
                       first_name=u"",
                       last_name=row[1],
                       organization=row[2],
                       date=date)
    db.session.add(reg)
  db.session.commit()


@manager.command
def create_db():
  if not exists("data"):
    mkdir("data")

  with app.app_context():
    db.create_all()


@manager.command
def drop_db():
  """
  Drop the DB.
  """
  # TODO: ask for confirmation.
  with app.app_context():
    db.drop_all()


@manager.command
def serve(server='0.0.0.0', port=7100):
  """ Serves this site.
  """
  debug = app.config['DEBUG'] = app.debug = True
  #asset_manager.config['ASSETS_DEBUG'] = debug
  app.run(host=server, port=port, debug=debug)


if __name__ == '__main__':
  manager.run()
