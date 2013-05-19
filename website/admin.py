from flask.ext.admin.contrib.sqlamodel import ModelView

from .models import Registration, db


class RegistrationView(ModelView):
  pass


def setup(app):
  admin = app.extensions['admin'][0]
  admin.add_view(RegistrationView(Registration, db.session))
