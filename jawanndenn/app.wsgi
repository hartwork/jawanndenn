# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import errno
import os
import logging

import bottle

if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'setup.py')):
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jawanndenn.app import db


logging.basicConfig(
        filename=os.path.expanduser('~/jawanndenn.log'),
        level=logging.WARNING)

_db_filename = os.path.expanduser('~/jawanndenn.pickle')

try:
    db.load(_db_filename)
except IOError as e:
    if e.errno != errno.ENOENT:
        raise

db.save(_db_filename)  # catch saving trouble early


class AutoSaveApp(object):
    def __init__(self, app):
        self._app = app

    def _on_request_finished(self):
        db.save(_db_filename)

    def __call__(self, environ, start_response):
        if environ.get('wsgi.multiprocess', True):
            raise ValueError('Single-process deployment needed')

        try:
            return self._app(environ, start_response)
        finally:
            self._on_request_finished()


application = AutoSaveApp(bottle.default_app())
