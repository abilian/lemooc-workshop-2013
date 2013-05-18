#!/usr/bin/env python2.7

from argh import ArghParser
from website.application import setup_app, app


###############################################################################
# Commands

# Not used (yet?)
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


def serve(server='0.0.0.0', port=7100):
  """ Serves this site.
  """
  setup_app(app)
  debug = app.config['DEBUG'] = app.debug = True
  #asset_manager.config['ASSETS_DEBUG'] = debug
  app.run(host=server, port=port, debug=debug)


if __name__ == '__main__':
  parser = ArghParser()
  parser.add_commands([serve, post])
  parser.dispatch()
