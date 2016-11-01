# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

import argparse
import errno
import logging
import os
import sys


def _require_hash_randomization():
    if not sys.flags.hash_randomization:
        logging.info('Hash randomization found to be disabled.')
        if os.environ.get('PYTHONHASHSEED') == 'random':
            logging.error('Unexpected re-execution loop detected, shutting down.')
            sys.exit(1)

        logging.info('Re-executing with hash randomization enabled...')
        env = os.environ.copy()
        env['PYTHONHASHSEED'] = 'random'
        argv = [sys.executable] + sys.argv
        os.execve(argv[0], argv, env)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=8080, type=int)
    parser.add_argument('--server', default='paste')
    options = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if options.debug else logging.INFO)

    _require_hash_randomization()

    from jawanndenn.app import db, run_server, STATIC_HOME_LOCAL

    logging.debug('Serving static files from "%s"' % STATIC_HOME_LOCAL)

    filename = os.path.expanduser('~/jawanndenn.pickle')

    try:
        db.load(filename)
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
        db.save(filename)  # catch saving trouble early

    try:
        run_server(options)
    finally:
        db.save(filename)


if __name__ == '__main__':
    main()
