# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField


class MaterialForm(Form):
    title  = StringField('Material Name', validators=[Required()])
    body       =  PageDownField( validators=[Required()])
    submit = SubmitField('Submit')


class EditMaterialForm(Form):
    body       =  PageDownField( validators=[Required()])
    submit = SubmitField('Submit')

