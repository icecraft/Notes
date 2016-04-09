# -*- coding: utf-8 -*
from .. import db, login_manager
from datetime import datetime
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .topic import Topic
from .note  import Note
from .diary import Diary

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    about_me      = db.Column(db.String(128))
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow)        
    topic = db.relationship('Topic', backref='author', lazy='dynamic',
                            cascade='all, delete-orphan')
    notebook = db.relationship('Note', backref='author', lazy='dynamic',
                               cascade='all, delete-orphan')

    libstudy = db.relationship('LibStudy', backref='author', lazy='dynamic',
                               cascade='all, delete-orphan')

    diary  = db.relationship('Diary', backref='author', lazy='dynamic',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



