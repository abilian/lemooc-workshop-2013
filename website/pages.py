import re
from unicodedata import normalize
import datetime

from flask import current_app as app
from flask.ext.flatpages import FlatPages, Page


flatpages = FlatPages()


#
# Monkey patch
#
Page__init__orig = Page.__init__

def Page__init__(self, path, meta_yaml, body, html_renderer):
  Page__init__orig(self, path, meta_yaml, body, html_renderer)
  date = self.meta.get('date')

  if not date:
    self.meta['date'] = datetime.date.today()
  elif isinstance(date, str):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    date = datetime.date(year, month, day)
    self.meta['date'] = date

  if not self.meta.get('slug'):
    self.meta['slug'] = self.path.split('/')[-1]

Page.__init__ = Page__init__


def get_pages(offset=None, limit=None):
  """
  Retrieves pages matching passed criterias.
  """
  articles = list(flatpages)
  # assign section value if none was provided in the metas
  for article in articles:
    if not article.meta.get('section'):
      article.meta['section'] = article.path.split('/')[0]

  # filter unpublished article
  if not app.debug:
    articles = [p for p in articles if p.meta.get('draft') is not True]

  articles = sorted(articles, reverse=True, key=lambda p: p.meta['date'])

  if offset and limit:
    return articles[offset:limit]
  elif limit:
    return articles[:limit]
  elif offset:
    return articles[offset:]
  else:
    return articles


def get_posts(offset=None, limit=None):
  posts = list(flatpages)

  posts = [ article for article in posts
            if article.path.startswith("news") ]

  for post in posts:
    if not 'image' in post.meta:
      post.meta['image'] = "news.jpg"

  # filter unpublished article
  #if not app.debug:
  #  posts = [p for p in posts if p.meta.get('draft') is False]

  # sort by date
  posts = sorted(posts, reverse=True,
                 key=lambda p: p.meta['date'])

  if offset and limit:
    return posts[offset:limit]
  elif limit:
    return posts[:limit]
  elif offset:
    return posts[offset:]
  else:
    return posts


def get_publications():
  publications = [ page for page in list(flatpages)
                   if page.path.startswith("publications") ]

  publications = sorted(publications, reverse=True,
                        key=lambda p: p.meta['date'])

  return publications


def get_years(pages):
  years = list(set([page.meta.get('date').year for page in pages]))
  years.reverse()
  return years


def slugify(text, delim=u'-'):
  """Generates an slightly worse ASCII-only slug."""
  _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
  result = []
  for word in _punct_re.split(text.lower()):
    word = normalize('NFKD', word).encode('ascii', 'ignore')
    if word:
      result.append(word)
  return unicode(delim.join(result))


def setup(app):
  flatpages.init_app(app)