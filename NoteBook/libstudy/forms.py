# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from flask.ext.pagedown.fields import PageDownField

DEFAULT_LibStudy_Contents="""### Miscellanise
### Essential
### 进阶
### 收获
### 不足
### 你能想到的应用场景
### 头脑风暴--想象一下你如何使用该模块
### 学习本模块时的特殊方法
### 批判本笔记
"""


class LibStudyForm(Form):
    libstudyname  = StringField(' Python Lib Name', validators=[Required()])
    about_this = TextAreaField('brief introduction', validators=[Required()])
    body       =  PageDownField( validators=[Required()])
    submit = SubmitField('Submit')

