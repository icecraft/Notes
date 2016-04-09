# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from wtforms import ValidationError

class settingForm(Form):
    body       =  StringField( validators=[Required()])
    submit = SubmitField('Submit')
