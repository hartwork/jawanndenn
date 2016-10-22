# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

import argparse

import bottle


_STATIC_HOME_LOCAL = 'static'
_STATIC_HOME_REMOTE = '/static'


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    options = parser.parse_args()

    if options.debug:
        bottle.debug(True)

    bottle.run()


main()
