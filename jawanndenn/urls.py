# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import re
from http import HTTPStatus

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from django.views.defaults import permission_denied
from jawanndenn.views import serve_using_finders
from ratelimit.decorators import ratelimit
from ratelimit.exceptions import Ratelimited

from .views import (index_get_view, poll_data_get_view, poll_get_view,
                    poll_post_view, vote_post_view)


class _HttpResponseTooManyRequests(HttpResponse):
    status_code = HTTPStatus.TOO_MANY_REQUESTS

    def __init__(self):
        super().__init__(f'<h1>{self.status_code} Too Many Requests</h1>',
                         content_type='text/html')


def _staticfiles_urlpatterns():
    '''
    Fork of django.contrib.staticfiles.urls.staticfiles_urlpatterns
    that supports DEBUG=False and settings.STATICFILES_FINDERS
    '''
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(
            settings.STATIC_URL.lstrip('/')),
                serve_using_finders, kwargs={
                'show_indexes': settings.DEBUG,
            }, name='static'),
    ]


def _permission_denied_or_too_many_requests(request, exception=None):
    if isinstance(exception, Ratelimited):
        return _HttpResponseTooManyRequests()

    return permission_denied(request, exception)


def _decorate_view_of_url_pattern(decorator, url_pattern):
    url_pattern.callback = decorator(url_pattern.callback)
    return url_pattern


def _decorate_view_triple(decorator, view):
    urlconf_module, _app_name, _namespace = view

    for url_pattern in urlconf_module:
        _decorate_view_of_url_pattern(decorator, url_pattern)

    return view


_limit_read_access = ratelimit(key='user_or_ip', rate='180/m', block=True)

_limit_write_access = ratelimit(key='user_or_ip', rate='30/m', block=True)

_app_urlpatterns = [
    path('', _limit_read_access(index_get_view), name='frontpage'),
    path('create', _limit_write_access(poll_post_view), name='poll-creation'),
    path('data/<poll_id>',
         _limit_read_access(poll_data_get_view), name='poll-data'),
    path('poll/<poll_id>',
         _limit_read_access(poll_get_view), name='poll-detail'),
    path('vote/<poll_id>', _limit_write_access(vote_post_view), name='vote'),

    path('admin/', _decorate_view_triple(_limit_write_access,
                                         admin.site.urls)),
]

if settings.JAWANNDENN_URL_PREFIX:
    from django.views.generic.base import RedirectView
    urlpatterns = [
        path('', _limit_read_access(
            RedirectView.as_view(url=settings.JAWANNDENN_URL_PREFIX + '/'))),
        path(settings.JAWANNDENN_URL_PREFIX.strip('/') + '/',
             include(_app_urlpatterns)),
    ]
else:
    urlpatterns = _app_urlpatterns

urlpatterns += [_decorate_view_of_url_pattern(_limit_read_access, url_pattern)
                for url_pattern in _staticfiles_urlpatterns()]

handler403 = _permission_denied_or_too_many_requests
