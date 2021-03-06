from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from .config import config
import os    

bootstrap = Bootstrap()
moment = Moment()
pagedown = PageDown()

def create_app(config_name):
    app = Flask(__name__)

    update_config(app, config_name)
    
    register_extension(app)
    register_blueprint(app)
    
    return app


def register_extension(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)

def register_blueprint(app):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

def update_config(app, config_name):
    app.config.from_object(config[config_name])    
    config[config_name].init_app(app)


sourcefind = create_app(os.getenv('FLASK_CONFIG') or 'default')
