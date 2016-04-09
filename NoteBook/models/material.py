# -*- coding: utf-8 -*
from .. import db
from datetime import datetime
from markdown import markdown
import bleach

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(64), unique=True, index=True)
    contents =  db.Column(db.Text())
    contents_html = db.Column(db.Text())
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow)
    lastupdate_timestamp  = db.Column(db.DateTime, default=datetime.utcnow)        
    
    def __repr__(self):
        return "<Material %r>"  % self.title
    
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p']
        target.contents_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
        
db.event.listen(Material.contents, 'set', Material.on_changed_body)
