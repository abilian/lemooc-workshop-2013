# coding=utf-8

from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Length, Email, URL


class PreRegistrationForm(Form):
  pass


class RegistrationForm(Form):

  msg = u"Champ obligatoire. Maximum %(max)d caractères."

  first_name = TextField(u"Prénom",
                         validators=[Length(min=1, max=100, message=msg)])

  last_name = TextField(u"Nom",
                        validators=[Length(min=1, max=100, message=msg)])

  email = TextField(u"E-mail",
                    validators=[Length(max=100), Email()])

  organization = TextField(u"Organisation / Institution",
                           validators=[Length(min=1, max=200, message=msg)])

  url = TextField(u"URL",
                  validators=[
                    Length(max=200, message=msg),
                    URL()])
