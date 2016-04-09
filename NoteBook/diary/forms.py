# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import  SubmitField
from wtforms.validators import Required
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField

class DiaryForm(Form):
    body       =  PageDownField( validators=[Required()])
    submit = SubmitField('Submit')

