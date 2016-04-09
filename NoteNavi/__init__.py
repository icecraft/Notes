from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)

    register_extension(app)
    
    return app


def register_extension(app):
    bootstrap.init_app(app)



import os    
application = create_app(os.getenv('FLASK_CONFIG') or 'default')

@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
