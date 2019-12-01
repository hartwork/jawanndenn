# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import cPickle as pickle
import datetime
import hashlib
import json
import logging
import os
import shutil
import tempfile
from threading import Lock

from dateutil.tz import tzlocal
from jawanndenn.markup import safe_html

DEFAULT_MAX_POLLS = 1000
DEFAULT_MAX_VOTER_PER_POLL = 40

_MAX_POLLS = DEFAULT_MAX_POLLS
_MAX_VOTERS_PER_POLL = DEFAULT_MAX_VOTER_PER_POLL

_KEY_OPTIONS = 'options'
_KEY_TITLE = 'title'
_KEY_EQUAL_WIDTH = 'equal_width'

_PICKLE_PROTOCOL_VERSION = 2

_PICKLE_CONTENT_VERSION = 1
_PICKLE_POLL_VERSION = 3
_PICKLE_POLL_DATABASE_VERSION = 1


_log = logging.getLogger(__name__)


def _get_random_sha256():
    return hashlib.sha256(os.urandom(256 / 8)).hexdigest()


def apply_limits(polls, votes_per_poll):
    global _MAX_POLLS
    global _MAX_VOTERS_PER_POLL
    _MAX_POLLS = polls
    _MAX_VOTERS_PER_POLL = votes_per_poll


class _Poll(object):
    def __init__(self):
        # Version 1
        self.config = {}
        self.votes = []
        self._lock = Lock()
        self._version = _PICKLE_POLL_VERSION

        # Version 2 and later
        self._created_at = datetime.datetime.now()

        # Version 3 and later
        self._equal_width = False

    def __getstate__(self):
        d = self.__dict__.copy()
        del d['_lock']
        return d

    def __setstate__(self, d):
        self.__dict__.update(d)
        self._lock = Lock()

        initial_version = self._version

        if self._version == 1:
            self._version = 2
            self._created_at = datetime.datetime.now()

        if self._version == 2:
            self._version = 3
            self._equal_width = False

        assert self._version == _PICKLE_POLL_VERSION

        if self._version != initial_version:
            _log.debug('Upgraded poll from version %d to version %d'
                       % (initial_version, self._version))

    @staticmethod
    def from_config(config):
        poll = _Poll()

        if _KEY_OPTIONS not in config \
                or _KEY_TITLE not in config:
            raise ValueError('Malformed configuration: %s' % config)

        poll.config = {
            _KEY_EQUAL_WIDTH: bool(config.get(_KEY_EQUAL_WIDTH, False)),
            _KEY_TITLE: safe_html(config[_KEY_TITLE]),
            _KEY_OPTIONS: map(safe_html, config[_KEY_OPTIONS]),
        }
        return poll

    @property
    def options(self):
        return self.config[_KEY_OPTIONS]

    def vote(self, person, votes):
        with self._lock:
            if len(self.votes) >= _MAX_VOTERS_PER_POLL:
                raise ValueError('Too many votes per poll')
            if len(votes) != len(self.options):
                raise ValueError('Malformed vote')
            self.votes.append((safe_html(person), votes))


class PollDatabase(object):
    def __init__(self):
        self._db = {}
        self._db_lock = Lock()
        self._version = _PICKLE_POLL_DATABASE_VERSION

    def __getstate__(self):
        d = self.__dict__.copy()
        del d['_db_lock']
        return d

    def __setstate__(self, d):
        self.__dict__.update(d)
        self._db_lock = Lock()

    def add(self, config):
        poll = _Poll.from_config(config)
        poll_id = _get_random_sha256()

        with self._db_lock:
            if len(self._db) >= _MAX_POLLS:
                raise ValueError('Too many polls')
            if poll_id in self._db:
                raise ValueError('ID collision: %s' % poll_id)
            self._db[poll_id] = poll

        return poll_id

    def get(self, poll_id):
        with self._db_lock:
            return self._db[poll_id]

    def load(self, filename):
        with open(filename, 'rb') as f:
            d = pickle.load(f)

        if d['version'] != _PICKLE_CONTENT_VERSION:
            raise ValueError('Content version mismatch')

        self.__dict__.update(d['data'].__dict__)
        _log.info('%d polls loaded.' % len(self._db))

    def save(self, filename):
        with self._db_lock:
            d = {
                'version': _PICKLE_CONTENT_VERSION,
                'data': self,
            }

            fd, tempfilename = tempfile.mkstemp(
                    dir=os.path.dirname(filename),
                    prefix='%s-tmp' % os.path.basename(
                            filename.replace('.pickle', '')),
                    suffix='.pickle',
                    )

            with os.fdopen(fd, 'w') as f:
                pickle.dump(d, f, _PICKLE_PROTOCOL_VERSION)

            shutil.move(tempfilename, filename)

            _log.info('%d polls saved.' % len(self._db))

    @staticmethod
    def _datetime_to_str(dt, tzinfo):
        return dt.replace(tzinfo=tzinfo).isoformat()

    def dump_as_django_json(self, options):
        tzinfo = tzlocal()
        objects = []

        next_poll_option_pk = options.first_poll_option
        next_ballot_pk = options.first_ballot
        next_vote_pk = options.first_vote

        for poll_index, (poll_slug, poll) in enumerate(self._db.items()):
            poll_pk = options.first_poll + poll_index
            poll_created_str = self._datetime_to_str(poll._created_at, tzinfo)

            objects.append({
                'model': 'jawanndenn.poll',
                'pk': poll_pk,
                'fields': {
                    'created': poll_created_str,
                    'modified': poll_created_str,
                    'slug': poll_slug,
                    'title': poll.config[_KEY_TITLE],
                    'equal_width': poll.config[_KEY_EQUAL_WIDTH],
                },
            })

            option_pk_for_position = {}
            for option_position, option_name in enumerate(poll.config[
                                                              _KEY_OPTIONS]):
                poll_option_pk = next_poll_option_pk
                objects.append({
                    'model': 'jawanndenn.polloption',
                    'pk': poll_option_pk,
                    'fields': {
                        'poll': poll_pk,
                        'position': option_position,
                        'name': option_name,
                    },
                })
                next_poll_option_pk += 1
                option_pk_for_position[option_position] = poll_option_pk

            for (voter_name, votes) in poll.votes:
                ballot_pk = next_ballot_pk
                objects.append({
                    'model': 'jawanndenn.ballot',
                    'pk': ballot_pk,
                    'fields': {
                        'created': poll_created_str,  # best we have
                        'modified': poll_created_str,  # best we have
                        'poll': poll_pk,
                        'voter_name': voter_name,
                    },
                })
                next_ballot_pk += 1

                for vote_position, vote in enumerate(votes):
                    objects.append({
                        'model': 'jawanndenn.vote',
                        'pk': next_vote_pk,
                        'fields': {
                            'ballot': ballot_pk,
                            'option': option_pk_for_position[vote_position],
                            'yes': vote,
                        }
                    })
                    next_vote_pk += 1

        print(json.dumps(objects, sort_keys=True, indent=2))
