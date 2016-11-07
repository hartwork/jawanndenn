# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import errno
import os
import logging
from threading import Lock

import bottle

if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'setup.py')):
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jawanndenn.app import db


logging.basicConfig(
        filename=os.path.expanduser('~/jawanndenn.log'),
        level=logging.WARNING)

_db_filename = os.path.expanduser('~/jawanndenn.pickle')
_db_lock = Lock()

try:
    db.load(_db_filename)
except IOError as e:
    if e.errno != errno.ENOENT:
        raise

db.save(_db_filename)  # catch saving trouble early


def _post():
    # TODO Do not save as often
    with _db_lock:
        db.save(_db_filename)


class Lifetime(object):
    def __init__(self, app, pre, post):
        self._app = app
        self._pre = pre
        self._post = post
        assert callable(post)

    def __call__(self, environ, start_response):
        self._pre()
        try:
            return self._app(environ, start_response)
        finally:
            self._post()


application = Lifetime(bottle.default_app(), lambda: None, _post)
