#!/usr/bin/env python
import os
from NoteNavi import application as notenavi
from flask.ext.script import Manager, Shell
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


manager = Manager(notenavi)


def make_shell_context():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def runtornado():
    http_server = HTTPServer(WSGIContainer(notenavi))
    http_server.listen(5050)
    IOLoop.instance().start()

if __name__ == '__main__':
    import sys
    if sys.version_info.major < 3:
            reload(sys)
    sys.setdefaultencoding('utf8')
    manager.run()
