# Copyright (c) 2024 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from django.http import FileResponse
from django.test import TestCase
from django.urls import reverse_lazy
from parameterized import parameterized


class SecurityTxtTest(TestCase):
    @parameterized.expand(
        [
            (
                "default location",
                "/.well-known/security.txt",
            ),
            (
                "legacy location",
                "/security.txt",
            ),
            (
                "through reverse",
                reverse_lazy("security_txt", kwargs={"path": "security.txt"}),
            ),
        ]
    )
    def test_file_served_properly(self, _label, url):
        self.assertTrue(url.endswith("/security.txt"))

        response = self.client.get(url)

        self.assertIsInstance(response, FileResponse)
        self.assertEqual(response.headers["Content-Type"], "text/plain")
