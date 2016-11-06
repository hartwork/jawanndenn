# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import cPickle as pickle
import datetime
from StringIO import StringIO

from unittest import TestCase

from jawanndenn.poll import _Poll


def _create_v1_poll():
    p = _Poll()
    p._version = 1
    del p.__dict__['_created_at']
    return p


def _save_and_load(poll):
    f = StringIO()
    pickle.dump(poll, f)
    f.seek(0)
    return pickle.load(f)


class UpgradeTest(TestCase):
    def test_upgrade_1_to_2(self):
        v1 = _create_v1_poll()

        self.assertEquals(v1._version, 1)
        self.assertFalse(hasattr(v1, '_created_at'))

        v2 = _save_and_load(v1)

        self.assertEquals(v2._version, 2)
        self.assertTrue(isinstance(v2._created_at, datetime.datetime))
