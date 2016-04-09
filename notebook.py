#!/usr/bin/env python
# -*- coding: utf-8 -*
            
import os
from NoteBook import db 
from NoteBook import  notebook
from NoteBook.models import User, Note, Topic, Comment, Material, \
    Year, Month, Week, Diary
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from werkzeug.wsgi import DispatcherMiddleware


manager = Manager(notebook)
migrate = Migrate(notebook, db)

def make_shell_context():
    return dict(app=notebook, db=db, User=User, Comment=Comment, Note=Note,\
                Topic=Topic, Material=Material, Year=Year, Month=Month, Week=Week, Diary=Diary )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)



@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('NoteBook/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def runtornado():
    http_server = HTTPServer(WSGIContainer(notebook))
    http_server.listen(5050)
    IOLoop.instance().start()

if __name__ == '__main__':
    import sys
    if sys.version_info.major < 3:
            reload(sys)
    sys.setdefaultencoding('utf8')

    manager.run()
