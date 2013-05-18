from StringIO import StringIO
import csv
import datetime
import locale
import mimetypes
from os.path import join
from PIL import Image

from flask import request, redirect, url_for, render_template, flash, abort, \
    make_response

from .application import app
from .config import BASE_URL, REDIRECTS, FEED_MAX_LINKS
from .pages import get_posts, get_publications, flatpages, get_pages


#
# Filters
#
@app.template_filter()
def to_rfc2822(dt):
  if not dt:
    return
  current_locale = locale.getlocale(locale.LC_TIME)
  locale.setlocale(locale.LC_TIME, "en_US")
  formatted = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
  locale.setlocale(locale.LC_TIME, current_locale)
  return formatted


#
# Context processors
#
@app.context_processor
def inject_ga():
  return dict(BASE_URL=BASE_URL)


@app.context_processor
def inject_recent_posts():
  return dict(recent_posts=get_posts())


@app.context_processor
def inject_publications():
  return dict(publications=get_publications())


#
# Routes
#
@app.route('/')
def home():
  accepted_languages = request.headers.get("Accept-Language", '').lower()
  accepted_languages = accepted_languages.split(';')[0]
  accepted_languages = accepted_languages.split(',')

  for language in accepted_languages:
    if language.startswith('fr'):
      return redirect(url_for('home_fr'))

  return redirect(url_for('home_en'))


@app.route('/en/')
def home_en():
  template = "home_en.html"
  return render_template(template)


@app.route('/fr/')
def home_fr():
  template = "home_fr.html"
  return render_template(template)


@app.route('/fr/<path:path>/')
def page(path=""):
  for orig, dest in REDIRECTS.items():
    if path.startswith(orig):
      return redirect(dest, 301)

  page = flatpages.get('fr/%s/index' % path)
  if not page:
    page = flatpages.get('fr/' + path)
  if not page:
    abort(404)
  print page
  template = page.meta.get('template', '_page_fr.html')
  return render_template(template, page=page)


@app.route('/feedback', methods=['POST'])
def feedback():

  email = request.form.get('email')
  name = request.form.get('name')
  organisation = request.form.get('organisation')

  if not email or not name or not organisation:
    flash("Some data were missing", "error")
  else:
    flash("Thank you for your feedback", "success")

    csvfile = open("../feedback.csv", "a+")
    writer = csv.writer(csvfile)
    row = [email, name, organisation, str(datetime.datetime.utcnow())]
    row = [ x.encode("utf8") for x in row ]
    writer.writerow(row)
    csvfile.close()

  return redirect(url_for("home"))


@app.route('/register', methods=['POST'])
def register():
  email = request.form.get('email')
  name = request.form.get('name')
  organisation = request.form.get('organisation')
  url = request.form.get('url')

  if not email or not name or not organisation:
    flash("Some data were missing", "error")
  else:
    flash("Thank you for your feedback", "success")

    csvfile = open("../feedback.csv", "a+")
    writer = csv.writer(csvfile)
    row = [email, name, organisation, str(datetime.datetime.utcnow())]
    row = [ x.encode("utf8") for x in row ]
    writer.writerow(row)
    csvfile.close()

  return redirect(url_for("home"))


@app.route('/news/')
def news():
  posts = get_posts()
  page = {'title': 'News'}
  return render_template("news.html", **locals())


@app.route('/news/<path:slug>/')
def post(slug):
  page = flatpages.get("news/" + slug)
  if not page:
    return redirect(url_for("news"))

  recent_posts = get_posts()
  return render_template("post.html", **locals())


# Aux

@app.route('/image/<path:path>')
def image(path):
  if '..' in path:
    abort(500)
  fd = open(join(app.root_path, "images", path))
  data = fd.read()

  hsize = int(request.args.get("h", 0))
  vsize = int(request.args.get("v", 0))
  if hsize > 1000 or vsize > 1000:
    abort(500)

  if hsize:
    image = Image.open(StringIO(data))
    x, y = image.size

    x1 = hsize
    y1 = int(1.0 * y * hsize / x)
    image.thumbnail((x1, y1), Image.ANTIALIAS)
    output = StringIO()
    image.save(output, "PNG")
    data = output.getvalue()
  if vsize:
    image = Image.open(StringIO(data))
    x, y = image.size

    x1 = int(1.0 * x * vsize / y)
    y1 = vsize
    image.thumbnail((x1, y1), Image.ANTIALIAS)
    output = StringIO()
    image.save(output, "PNG")
    data = output.getvalue()

  response = make_response(data)
  response.headers['content-type'] = mimetypes.guess_type(path)
  return response


@app.route('/feed')
def feed():
  pages = get_posts(limit=FEED_MAX_LINKS)
  now = datetime.datetime.now()

  resp = make_response(render_template('base.rss', **locals()))
  resp.headers['Content-Type'] = 'text/xml'
  return resp


@app.route('/sitemap.xml')
def sitemap():
  today = datetime.date.today()
  recently = datetime.date(year=today.year, month=today.month, day=1)
  pages = get_pages()

  resp = make_response(render_template('sitemap.xml', **locals()))
  resp.headers['Content-Type'] = 'text/xml'
  return resp


@app.errorhandler(404)
def page_not_found(error):
  page = {'title': "Page introuvable"}
  return render_template('404.html', page=page), 404


# Not needed currently since we don't do static generation (yet?)
@app.route('/403.html')
def error403():
  return render_template('403.html')


@app.route('/404.html')
def error404():
  return render_template('404.html')

@app.route('/500.html')
def error500():
  return render_template('500.html')

