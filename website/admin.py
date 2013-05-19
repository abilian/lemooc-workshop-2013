from cStringIO import StringIO
import csv
from time import strftime, gmtime

from flask import flash, redirect, url_for, make_response, request, \
    current_app as app
from flask.ext.admin import AdminIndexView, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.login import current_user, logout_user, UserMixin, login_user
from flask.ext.wtf import Form
from wtforms import PasswordField

from .models import Registration, db

#
# Flask-Login stuff
#
from website.extensions import login_manager


class AdminUser(UserMixin):
  id = 'admin'


class LoginForm(Form):
  password = PasswordField()


@login_manager.user_loader
def load_user(id):
  if id == 'admin':
    return AdminUser()


#
# Flask-Admin stuff
#
class MyAdminIndexView(AdminIndexView):

  @expose("/")
  def index(self):
    if not current_user.is_authenticated():
      return redirect(url_for("loginview.index"))
    else:
      return redirect(url_for("registrationview.index"))


class RegistrationView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated()


class ExportView(BaseView):
  def is_accessible(self):
    return current_user.is_authenticated()

  @expose("/")
  def index(self):
    csvfile = StringIO()
    writer = csv.writer(csvfile)
    regs = Registration.query.all()
    for reg in regs:
      row = [reg.first_name, reg.last_name, reg.email, reg.organization,
             reg.url, str(reg.date)]
      row = [ cell.encode('utf8') for cell in row ]
      writer.writerow(row)

    response = make_response(csvfile.getvalue())
    response.headers['content-type'] = 'application/csv'
    filename = "registrations-%s.csv" % strftime("%d:%m:%Y-%H:%M:%S", gmtime())
    response.headers['content-disposition'] = 'attachment;filename="%s"' % filename
    return response


class LoginView(BaseView):
  def is_accessible(self):
    return not current_user.is_authenticated()

  @expose("/")
  def index(self):
    if current_user.is_authenticated():
      return redirect(url_for("admin.index"))

    form = LoginForm()
    return self.render("admin/login.html", form=form)

  @expose("/", methods=['POST'])
  def post(self):
    password = request.form['password']
    if password != app.config['ADMIN_PASSWORD']:
      flash("Invalid password.")
      return redirect(url_for("login"))
    else:
      login_user(AdminUser())
      return redirect(url_for("admin.index"))


class LogoutView(BaseView):
  def is_accessible(self):
    return current_user.is_authenticated()

  @expose("/")
  def index(self):
    logout_user()
    flash("Logged out.")
    return redirect(url_for("admin.index"))


def setup(app):
  admin = app.extensions['admin'][0]
  admin.add_view(RegistrationView(Registration, db.session, name="Registrations"))
  admin.add_view(ExportView("Export"))
  admin.add_view(LoginView("Login"))
  admin.add_view(LogoutView("Logout"))
