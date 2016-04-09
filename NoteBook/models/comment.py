# -*- coding: utf-8 -*
from .. import db
from datetime import datetime
from markdown import markdown
import bleach

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    contents =  db.Column(db.Text())
    contents_html = db.Column(db.Text())
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow)
    lastupdate_timestamp  = db.Column(db.DateTime, default=datetime.utcnow)        
    note_id      = db.Column(db.Integer, db.ForeignKey('notes.id'))
    topic_id     = db.Column(db.Integer, db.ForeignKey('topics.id'))
    
    def __repr__(self):
        return "<Comment %r>"  % self.note.notename if self.note else self.topic.topicname
    
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p']
        target.contents_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
        
db.event.listen(Comment.contents, 'set', Comment.on_changed_body)
    

    
