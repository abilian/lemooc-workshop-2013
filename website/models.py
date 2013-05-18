from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer


db = SQLAlchemy()


class Registration(db.Model):
  __tablename__ = 'registration'

  id = Column(Integer, primary_key=True)


def setup(app):
  db.init_app(app)
