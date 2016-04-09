# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import  SubmitField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField

class CommentForm(Form):
    body       =  PageDownField("Add Comment",validators=[Required()])
    submit = SubmitField('Submit')

    
