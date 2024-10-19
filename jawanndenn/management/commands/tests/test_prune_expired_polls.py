# Copyright (C) 2020 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from datetime import timedelta
from io import StringIO

from django.test import TestCase
from django.utils.timezone import now

from ....models import Poll
from ....tests.factories import PollFactory
from ..prune_expired_polls import Command


class PruneExpiredPollsTest(TestCase):
    def test_deletes_expired_polls_and_those_only(self):
        expired_poll = PollFactory(expires_at=now())
        not_yet_expired_poll = PollFactory(expires_at=now() + timedelta(minutes=1))
        never_expiring_poll = PollFactory(expires_at=None)

        stdout = StringIO()
        Command(stdout=stdout).handle()

        with self.assertRaises(Poll.DoesNotExist):
            expired_poll.refresh_from_db()

        for poll in (not_yet_expired_poll, never_expiring_poll):
            poll.refresh_from_db()  # would raise DoesNotExist if deleted

        self.assertIn("1 poll(s) deleted", stdout.getvalue())
