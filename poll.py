import hashlib
import os
from threading import Lock


_MAX_POLLS = 100
_MAX_VOTERS_PER_POLL = 40

_KEY_OPTIONS = 'options'
_KEY_TITLE = 'title'


def _get_random_sha256():
    return hashlib.sha256(os.urandom(256 / 8)).hexdigest()


class _Poll(object):
    def __init__(self):
        self.config = []
        self.votes = []
        self._lock = Lock()

    @staticmethod
    def from_config(config):
        poll = _Poll()

        if _KEY_OPTIONS not in config \
                or _KEY_TITLE not in config:
            raise ValueError('Malformed configuration: %s' % config)

        poll.config = config
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
            self.votes.append((person, votes))


class PollDatabase(object):
    def __init__(self):
        self._db = {}
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
