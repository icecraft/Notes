# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField

class TopicForm(Form):
    topicname  = StringField('Topic Name', validators=[Required()])
    about_this = TextAreaField('brief introduction', validators=[Required()])
    body       =  PageDownField( validators=[Required()])
    submit = SubmitField('Submit')

    
