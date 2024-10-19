# Copyright (c) 2019-2024 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class ServeUsingFindersTest(TestCase):
    @parameterized.expand(
        [
            # Our app, some arbitrary asset
            ("jawanndenn", "js/html.js", "DENY"),
            # Our app, asset used in <iframe>
            ("jawanndenn", "3rdparty/github-buttons-4.0.1/docs/github-btn.html", "sameorigin"),
            # Arbitrary asset of arbitary other app
            ("django.contrib.admin", "admin/css/responsive.css", "DENY"),
        ]
    )
    def test(self, _app, path, expected_x_frame_options):
        url = reverse("static", kwargs={"path": path})

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["X-Frame-Options"], expected_x_frame_options)
