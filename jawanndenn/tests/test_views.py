# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from http import HTTPStatus

import rapidjson as json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from jawanndenn.models import Ballot, Poll
from jawanndenn.tests.factories import (BallotFactory, PollFactory,
                                        PollOptionFactory, VoteFactory)
from parameterized import parameterized


class AdminLoginPageTest(TestCase):
    def test(self):
        url = reverse('admin:index')
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'Django administration')


class IndexGetViewTest(TestCase):
    def test(self):
        url = reverse('frontpage')

        response = self.client.get(url)

        self.assertContains(response, 'Create a new poll')


class PollPostViewTest(TestCase):
    url = reverse('poll-creation')

    def test_malformed__config_not_json(self):
        data = {
            'config': 'not JSON',
        }
        before_creation = timezone.now()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertFalse(Poll.objects.filter(created__gte=before_creation)
                         .exists())

    def test_well_formed(self):
        poll_title = 'Some short title'
        poll_option_names = ['Option One', 'Option Two']
        poll_equal_width = True
        data = {
            'config': json.dumps({
                'equal_width': poll_equal_width,
                'title': poll_title,
                'options': poll_option_names,
            }),
        }
        before_creation = timezone.now()

        response = self.client.post(self.url, data)

        poll = Poll.objects.get(created__gte=before_creation)
        self.assertEqual(poll.equal_width, poll_equal_width)
        self.assertEqual(list(poll.options
                              .order_by('position')
                              .values_list('name', flat=True)),
                         poll_option_names)
        self.assertEqual(poll.title, poll_title)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, poll.get_absolute_url())


class PollDataGetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.poll = PollFactory(equal_width=True)
        cls.ballot = BallotFactory(poll=cls.poll)
        cls.votes = [
            VoteFactory(ballot=cls.ballot, option__poll=cls.poll,
                        yes=(position == 0))
            for position
            in range(2)
        ]

    def test_poll_exists(self):
        url = reverse('poll-data', args=[self.poll.slug])
        expected_data = {
            'config': {
                'equal_width': self.poll.equal_width,
                'options': [v.option.name for v in self.votes],
                'title': self.poll.title,
            },
            'votes': [
                [self.ballot.voter_name, [v.yes for v in self.votes]],
            ],
        }

        response = self.client.get(url)

        actual_data = json.loads(response.content)
        self.assertEqual(actual_data, expected_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_poll_does_not_exist(self):
        url = reverse('poll-data', args=['whatever'])

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class PollGetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.poll = PollFactory()

    def test_poll_exists(self):
        url = self.poll.get_absolute_url()

        response = self.client.get(url)

        self.assertContains(response, 'Vote!')

    def test_poll_does_not_exist(self):
        url = reverse('poll-detail', args=['no_such_poll'])

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class VotePostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.poll = PollFactory()
        for _ in range(2):
            PollOptionFactory(poll=cls.poll)

    def test_poll_exists(self):
        url = reverse('vote', args=[self.poll.slug])
        voter_name = 'Maria'
        data = {
            'voterName': voter_name,
            'option0': 'on',
            'option1': 'off',
        }

        response = self.client.post(url, data)

        ballot = Ballot.objects.get(poll=self.poll)
        self.assertEqual(list(ballot.votes
                              .order_by('option__position')
                              .values_list('yes', flat=True)), [True, False])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, self.poll.get_absolute_url())

    def test_poll_does_not_exist(self):
        url = reverse('vote', args=['no_such_poll'])
        data = {}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class ServeUsingFindersTest(TestCase):
    @parameterized.expand([
        ('jawanndenn', 'js/html.js'),
        ('django.contrib.admin', 'admin/css/responsive.css'),
    ])
    def test(self, _app, path):
        url = reverse('static', kwargs={'path': path})

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
