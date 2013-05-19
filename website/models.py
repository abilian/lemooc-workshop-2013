import hashlib
import urllib
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, UnicodeText, DateTime, func


db = SQLAlchemy()


class Registration(db.Model):
  __tablename__ = 'registration'

  id = Column(Integer, primary_key=True)
  first_name = Column(UnicodeText(200))
  last_name = Column(UnicodeText(200))
  email = Column(UnicodeText(200))
  organization = Column(UnicodeText(200))
  url = Column(UnicodeText(200))
  date = Column(DateTime, default=func.now())

  def gravatar_url(self, size=60):
    url = "http://www.gravatar.com/avatar/"
    url += hashlib.md5(self.email.encode("ascii", "ignore").lower()).hexdigest()
    url += "?" + urllib.urlencode({'d': 'mm', 's': str(size)})
    return url


def setup(app):
  db.init_app(app)
