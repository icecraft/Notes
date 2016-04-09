# -*- coding: utf-8 -*
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from flask.ext.pagedown.fields import PageDownField

DEFAULT_NoteBook_Contents="""### Miscellanise
### Essential
### 进阶
### 收获
### 不足
### 批判本笔记
"""

DEFAULT_NoteSource_Contents="""### Miscellanise
### Essential
### 进阶
### 总结
### 收获
### 不足
### 源码赏析
* #### 项目结构 
* #### 语句赏析 
* #### 珠海拾遗

### 批判本笔记
"""

class NoteForm(Form):
    notename  = StringField('Note Name', validators=[Required()])
    about_this = TextAreaField('brief introduction', validators=[Required()])
    body       =  PageDownField( validators=[Required()])
    submit = SubmitField('Submit')

