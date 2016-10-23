# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

from __future__ import print_function

import argparse
import json
import sys

import bottle

from poll import PollDatabase


_STATIC_HOME_LOCAL = 'static'
_STATIC_HOME_REMOTE = '/static'


_db = PollDatabase()


def _to_json(e):
    return json.dumps(e)


@bottle.get('/static/<path:path>')
def static(path):
    content_type = {
                'css': 'text/css',
                'js': 'application/javascript',
                'xhtml': 'application/xhtml+xml',
            }[path.split('.')[-1]]
    bottle.response.content_type = content_type
    return bottle.static_file(path, root=_STATIC_HOME_LOCAL)


@bottle.get('/')
def index():
    bottle.redirect('%s/%s' % (_STATIC_HOME_REMOTE, 'setup.xhtml'))


@bottle.post('/create')
def create():
    config = json.loads(bottle.request.body.read())
    poll_id = _db.add(config)
    return _to_json({
                'pollId': poll_id,
            })


@bottle.get('/poll/<poll_id>')
def poll(poll_id):
    poll_id  # mark as used
    bottle.response.content_type = 'application/xhtml+xml'
    return bottle.static_file('poll.xhtml', root=_STATIC_HOME_LOCAL)


@bottle.get('/data/<poll_id>')
def data(poll_id):
    poll = _db.get(poll_id)
    return _to_json({
        'config': {
            'options': poll.options,
        },
        'votes': poll.votes,
    })


@bottle.post('/vote/<poll_id>')
def vote(poll_id):
    voterName = bottle.request.forms['voterName']
    poll = _db.get(poll_id)
    votes = [bottle.request.forms.get('option%d' % i) == 'on'
            for i in xrange(len(poll.options))]
    poll.vote(voterName, votes)

    bottle.redirect('/poll/%s' % poll_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=8080, type=int)
    options = parser.parse_args()

    if not sys.flags.hash_randomization:
        print('ERROR: Hash randomization found to be disabled. '
                'Please re-run using "python -R ..." for security.',
                file=sys.stderr)
        sys.exit(2)

    if options.debug:
        bottle.debug(True)

    bottle.run(host=options.host, port=options.port)


main()
