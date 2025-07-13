# Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import re
from importlib import resources

from django.urls import re_path
from django.views.static import serve

FAVICON_FILES = [
    "apple-touch-icon.png",
    "favicon-96x96.png",
    "favicon.ico",
    "favicon.svg",
    "site.webmanifest",
    "web-app-manifest-192x192.png",
    "web-app-manifest-512x512.png",
]

_FAVICON_FILES_PATTERN = "|".join(re.escape(filename) for filename in FAVICON_FILES)


def favicon_urlpatterns(name="favicon"):
    return [
        re_path(
            "^(?P<path>%s)$" % _FAVICON_FILES_PATTERN,
            serve,
            kwargs={
                "document_root": str(resources.files("jawanndenn").joinpath("static", "favicon")),
            },
            name=name,
        ),
    ]
