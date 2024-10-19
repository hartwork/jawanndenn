# Copyright (c) 2019-2024 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import re

from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.urls import re_path


def _serve_with_headers_fixed(request, path, insecure=False, **kwargs):
    response = serve(request, path, insecure=insecure, **kwargs)

    # Allow loading of github-btn.html in an <iframe>
    if path.startswith("3rdparty/github-buttons-") and path.endswith("/docs/github-btn.html"):
        response["X-Frame-Options"] = "sameorigin"

    return response


def staticfiles_urlpatterns(prefix=None, name="static"):
    """
    Fork of django.contrib.staticfiles.urls.staticfiles_urlpatterns
    that supports DEBUG=False, directory listings, and registering
    a name for the view.

    Also, it uses view _serve_with_headers_fixed above rather than stock
    django.contrib.staticfiles.views.serve to serve files.
    """
    if prefix is None:
        prefix = settings.STATIC_URL
    return [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(prefix.lstrip("/")),
            _serve_with_headers_fixed,
            kwargs={
                "insecure": not settings.DEBUG,
                "show_indexes": settings.DEBUG,
            },
            name=name,
        ),
    ]
