# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import cPickle as pickle
import datetime
from StringIO import StringIO

from unittest import TestCase

from jawanndenn.poll import _Poll, _PICKLE_POLL_VERSION


def _create_v1_poll():
    p = _Poll()
    p._version = 1
    del p.__dict__['_created_at']
    del p.__dict__['_equal_width']
    return p


def _save_and_load(poll):
    f = StringIO()
    pickle.dump(poll, f)
    f.seek(0)
    return pickle.load(f)


class UpgradeTest(TestCase):
    def test_upgrade_1_to_latest(self):
        v1 = _create_v1_poll()

        self.assertEquals(v1._version, 1)
        self.assertFalse(hasattr(v1, '_created_at'))
        self.assertFalse(hasattr(v1, '_equal_width'))

        latest = _save_and_load(v1)

        self.assertEquals(latest._version, _PICKLE_POLL_VERSION)
        self.assertTrue(isinstance(latest._created_at, datetime.datetime))
        self.assertTrue(isinstance(latest._equal_width, bool))
