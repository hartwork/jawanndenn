# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import json
import logging
import os
import sys
from functools import partial

import pkg_resources

import bottle
import jinja2
from jawanndenn.metadata import APP_NAME
from jawanndenn.poll import PollDatabase

_log = logging.getLogger(__name__)

STATIC_HOME_LOCAL = os.path.abspath(os.path.normpath(
    os.path.join(os.path.dirname(__file__), 'static')
    if os.path.exists(os.path.join(os.path.dirname(__file__),
                                   '..', 'setup.py'))
    else pkg_resources.resource_filename(APP_NAME, 'static')
))


db = PollDatabase()


def _to_json(e):
    return json.dumps(e)


def _render_template(filename, url_prefix):
    context_dict = {
        'url_prefix': url_prefix,
    }
    environment = jinja2.Environment()
    with open(os.path.join(STATIC_HOME_LOCAL, filename)) as f:
        template = environment.from_string(f.read())
    return template.render(context_dict)


def _static(path):
    content_type = {
                'css': 'text/css',
                'js': 'application/javascript',
                'xhtml': 'application/xhtml+xml',
            }[path.split('.')[-1]]
    bottle.response.content_type = content_type
    return bottle.static_file(path, root=STATIC_HOME_LOCAL)


def _index(url_prefix):
    bottle.response.content_type = 'application/xhtml+xml'
    return _render_template('html/setup.xhtml', url_prefix)


def _create(url_prefix):
    config = json.loads(bottle.request.forms['config'])
    poll_id = db.add(config)
    bottle.redirect(url_prefix + '/poll/%s' % poll_id)


def _poll(url_prefix, poll_id):
    db.get(poll_id)
    bottle.response.content_type = 'application/xhtml+xml'
    return _render_template('html/poll.xhtml', url_prefix)


def _data(poll_id):
    poll = db.get(poll_id)
    return _to_json({
        'config': poll.config,
        'votes': poll.votes,
    })


def _vote(url_prefix, poll_id):
    voterName = bottle.request.forms['voterName']
    poll = db.get(poll_id)
    votes = [bottle.request.forms.get('option%d' % i) == 'on'
             for i in range(len(poll.options))]
    poll.vote(voterName, votes)

    bottle.redirect(url_prefix + '/poll/%s' % poll_id)


def add_routes(url_prefix='/'):
    url_prefix = url_prefix.strip('/')

    if url_prefix != '':
        url_prefix = '/' + url_prefix
        bottle.route('/', 'GET', lambda: bottle.redirect(url_prefix + '/'))

    bottle.route(url_prefix + '/', 'GET', partial(_index, url_prefix))
    bottle.route(url_prefix + '/create', 'POST', partial(_create, url_prefix))
    bottle.route(url_prefix + '/data/<poll_id>', 'GET', _data)
    bottle.route(url_prefix + '/poll/<poll_id>', 'GET', partial(_poll,
                                                                url_prefix))
    bottle.route(url_prefix + '/static/<path:path>', 'GET', _static)
    bottle.route(url_prefix + '/vote/<poll_id>', 'POST', partial(_vote,
                                                                 url_prefix))


def run_server(options):
    if options.debug:
        bottle.debug(True)

    try:
        bottle.run(
                host=options.host,
                port=options.port,
                server=options.server,
                )
    except ImportError as e:
        if (options.server == 'cherrypy' and
                e.args == ('cannot import name wsgiserver',)):
            message = 'Bottle does not support CherryPy >=9.0.0, properly.'
        elif (options.server == 'flup' and
                e.args == ('No module named _dummy_thread',)):
            message = 'flup is broken and not supported.'
        elif (options.server == 'rocket' and
                e.args == ('No module named methods.wsgi',)):
            message = 'Rocket is broken and not supported.'
        else:
            message = ('WSGI server "%s" does not seem to be available.'
                       % options.server)

        _log.error(message)
        sys.exit(2)
