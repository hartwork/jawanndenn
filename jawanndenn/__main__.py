# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import argparse
import errno
import logging
import os
import sys

from jawanndenn.poll import (DEFAULT_MAX_POLLS, DEFAULT_MAX_VOTER_PER_POLL,
                             apply_limits)

_BOTTLE_BACKENDS = (
    # 'cgi',  # see https://github.com/bottlepy/bottle/issues/836
    # 'flup',
    'gae',
    'wsgiref',
    # 'cherrypy',
    'paste',
    # 'rocket',
    'waitress',
    'gunicorn',
    'eventlet',
    'gevent',
    'diesel',
    # 'fapws3',  # symptom "XML Parsing Error: no root element found"
    'tornado',
    'twisted',
    'meinheld',
    'bjoern',
    'auto',
)

_DEFAULT_BACKEND = 'tornado'

_log = logging.getLogger(__name__)


def _require_hash_randomization():
    if not sys.flags.hash_randomization:
        _log.info('Hash randomization found to be disabled.')
        if os.environ.get('PYTHONHASHSEED') == 'random':
            _log.error('Unexpected re-execution loop detected, shutting down.')
            sys.exit(1)

        _log.info('Re-executing with hash randomization enabled...')
        env = os.environ.copy()
        env['PYTHONHASHSEED'] = 'random'
        argv = [sys.executable] + sys.argv
        os.execve(argv[0], argv, env)


def main():
    parser = argparse.ArgumentParser(prog='jawanndenn')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode (default: disabled)')
    parser.add_argument('--host', default='127.0.0.1', metavar='HOST',
                        help='Hostname or IP address to listen at'
                             ' (default: %(default)s)')
    parser.add_argument('--port', default=8080, type=int, metavar='PORT',
                        help='Port to listen at (default: %(default)s)')
    parser.add_argument('--url-prefix', default='', metavar='PATH',
                        help='Path to prepend to URLs'
                             ' (default: "%(default)s")')
    parser.add_argument('--database-pickle', default='~/jawanndenn.pickle',
                        metavar='FILE',
                        help='File to write the database to'
                             ' (default: %(default)s)')
    parser.add_argument('--server', default=_DEFAULT_BACKEND,
                        metavar='BACKEND',
                        help='bottle backend to use (default: %%(default)s)'
                             '; as of this writing bottle supports: %s. '
                             'For the most current list, please check '
                             'the documentation of bottle.'
                             % ', '.join(sorted(b for b in _BOTTLE_BACKENDS
                                                if b != _DEFAULT_BACKEND))
                        )

    limits = parser.add_argument_group('limit configuration')
    limits.add_argument('--max-polls', type=int, metavar='COUNT',
                        default=DEFAULT_MAX_POLLS,
                        help='Maximum number of polls total'
                             ' (default: %(default)s)')
    limits.add_argument('--max-votes-per-poll', type=int, metavar='COUNT',
                        default=DEFAULT_MAX_VOTER_PER_POLL,
                        help='Maximum number of votes per poll'
                             ' (default: %(default)s)')

    export_args = parser.add_argument_group('data export arguments')
    export_args.add_argument('--dumpdata', action='store_true',
                             help='Dump a JSON export of the database to '
                                  'standard output, then quit.')
    export_args.add_argument('--first-poll', type=int, default=1,
                             metavar='NUMBER',
                             help='Lowest primary key to use for '
                                  'poll objects (default: %(default)s)')
    export_args.add_argument('--first-poll-option', type=int, default=1,
                             metavar='NUMBER',
                             help='Lowest primary key to use for '
                                  'poll option objects (default: %(default)s)')
    export_args.add_argument('--first-ballot', type=int, default=1,
                             metavar='NUMBER',
                             help='Lowest primary key to use for '
                                  'ballot objects (default: %(default)s)')
    export_args.add_argument('--first-vote', type=int, default=1,
                             metavar='NUMBER',
                             help='Lowest primary key to use for '
                                  'vote objects (default: %(default)s)')

    options = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if options.debug else logging.INFO)

    if not options.dumpdata:
        _require_hash_randomization()

        # NOTE: gevent patching needs to happen before importing bottle
        if options.server == 'gevent':
            from gevent.monkey import patch_all
            patch_all()

    # Heavy imports are down here to keep --help fast
    from jawanndenn.app import add_routes, db, run_server, STATIC_HOME_LOCAL

    if not options.dumpdata:
        apply_limits(
            polls=options.max_polls,
            votes_per_poll=options.max_votes_per_poll,
        )

        _log.debug('Serving static files from "%s"' % STATIC_HOME_LOCAL)

    filename = os.path.expanduser(options.database_pickle)

    try:
        db.load(filename)
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
        db.save(filename)  # catch saving trouble early

    if options.dumpdata:
        db.dump_as_django_json(options)
    else:
        add_routes(options.url_prefix)
        try:
            run_server(options)
        finally:
            db.save(filename)


if __name__ == '__main__':
    main()
