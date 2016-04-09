#!/usr/bin/env python
# -*- coding: utf-8 -*
from NoteBook import notebook
from SourceFind import sourcefind
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from werkzeug.wsgi import DispatcherMiddleware


application = DispatcherMiddleware(notebook, {
    '/srcfind':     sourcefind
    })

def runtornado(app):
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5050)
    IOLoop.instance().start()

if __name__ == '__main__':
    import sys
    if sys.version_info.major < 3:
            reload(sys)
    sys.setdefaultencoding('utf8')
    
    runtornado(application)
