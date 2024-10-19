# Copyright (C) 2020 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from django.test import RequestFactory, TestCase
from parameterized import parameterized

from jawanndenn.middleware import set_remote_addr_to_x_forwarded_for


class SetRemoteAddrToXForwardedForMiddlewareTest(TestCase):
    @parameterized.expand(
        [
            (None, "127.0.0.1"),  # inserted by Django
            ("2.2.2.2", "2.2.2.2"),
            ("  2.2.2.2  ", "2.2.2.2"),
            ("1.1.1.1,2.2.2.2", "1.1.1.1"),
            ("1.1.1.1, 2.2.2.2", "1.1.1.1"),
            ("1.1.1.1 ,2.2.2.2", "1.1.1.1"),
            ("1.1.1.1 , 2.2.2.2", "1.1.1.1"),
        ]
    )
    def test(self, http_x_forwarded_for, expected_remote_addr):
        wrapped_get_response = set_remote_addr_to_x_forwarded_for(
            get_response=lambda request: None
        )
        headers = {}
        if http_x_forwarded_for is not None:
            headers["HTTP_X_FORWARDED_FOR"] = http_x_forwarded_for
        request = RequestFactory().get("/", **headers)

        wrapped_get_response(request)

        self.assertEqual(request.META.get("REMOTE_ADDR"), expected_remote_addr)
