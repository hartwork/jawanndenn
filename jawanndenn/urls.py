"""jawanndenn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from .views import (index_get_view, poll_data_get_view, poll_get_view,
                    poll_post_view, vote_post_view)


def _staticfiles_urlpatterns():
    '''
    Fork of django.contrib.staticfiles.urls.staticfiles_urlpatterns
    that supports DEBUG=False
    '''
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(
            settings.STATIC_URL.lstrip('/')),
                serve, kwargs={
                'document_root': settings.STATICFILES_DIRS[0],
                'show_indexes': settings.DEBUG,
            }),
    ]


_app_urlpatterns = [
    path('', index_get_view),
    path('create', poll_post_view),
    path('data/<poll_id>', poll_data_get_view),
    path('poll/<poll_id>', poll_get_view, name='poll-detail'),
    path('vote/<poll_id>', vote_post_view),

    path('admin/', admin.site.urls),
]

if settings.JAWANNDENN_URL_PREFIX:
    from django.views.generic.base import RedirectView
    urlpatterns = [
        path('', RedirectView.as_view(
            url=settings.JAWANNDENN_URL_PREFIX + '/')),
        path(settings.JAWANNDENN_URL_PREFIX.strip('/') + '/',
             include(_app_urlpatterns)),
    ]
else:
    urlpatterns = _app_urlpatterns

urlpatterns += _staticfiles_urlpatterns()
