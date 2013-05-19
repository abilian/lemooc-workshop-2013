import hashlib
import urllib
from sqlalchemy import Column, Integer, UnicodeText, DateTime, func

from .extensions import db


class Registration(db.Model):
  __tablename__ = 'registration'

  id = Column(Integer, primary_key=True)
  first_name = Column(UnicodeText(200), default=u"", nullable=False)
  last_name = Column(UnicodeText(200), default=u"", nullable=False)
  email = Column(UnicodeText(200), default=u"", nullable=False)
  organization = Column(UnicodeText(200), default=u"", nullable=False)
  url = Column(UnicodeText(200), default=u"", nullable=False)
  date = Column(DateTime, default=func.now())

  def gravatar_url(self, size=60):
    url = "http://www.gravatar.com/avatar/"
    url += hashlib.md5(self.email.encode("ascii", "ignore").lower()).hexdigest()
    url += "?" + urllib.urlencode({'d': 'mm', 's': str(size)})
    return url
