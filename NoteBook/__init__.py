from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from .config import config
import os

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .topic import topic as topic_blueprint
    app.register_blueprint(topic_blueprint, url_prefix='/topic')

    from .note import note as note_blueprint
    app.register_blueprint(note_blueprint, url_prefix='/note')

    from .comment import comment as comment_blueprint
    app.register_blueprint(comment_blueprint, url_prefix='/comment')

    from .material import material as material_blueprint
    app.register_blueprint(material_blueprint, url_prefix='/material')

    from .libstudy import libstudy as libstudy_blueprint
    app.register_blueprint(libstudy_blueprint, url_prefix='/libstudy')

    from .diary  import diary as diary_blueprint
    app.register_blueprint(diary_blueprint, url_prefix='/diary')
    
    return app


notebook = create_app(os.getenv('FLASK_CONFIG') or 'default')
