# -*- coding: utf-8 -*
from .. import db
from datetime import datetime
from markdown import markdown
import bleach

class LibStudy(db.Model):
    __tablename__ = 'libstudies'
    id = db.Column(db.Integer, primary_key=True)
    about_this = db.Column(db.Text())    
    libstudyname  = db.Column(db.String(64), unique=True, index=True)
    contents =  db.Column(db.Text())
    contents_html = db.Column(db.Text())
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow)
    lastupdate_timestamp     = db.Column(db.DateTime, default=datetime.utcnow)            
    author_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return "<LibStudy %r>"  % self.libstudyname
    
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p']
        target.contents_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
        
db.event.listen(LibStudy.contents, 'set', LibStudy.on_changed_body)
    

    
