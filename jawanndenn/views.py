# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from functools import wraps

import rapidjson as json  # lgtm [py/import-and-import-from]
from django.conf import settings
from django.db import transaction
from django.http import (Http404, HttpResponseBadRequest, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.module_loading import import_string
from django.views.decorators.http import require_GET, require_POST
from django.views.defaults import bad_request
from django.views.static import serve
from jawanndenn.markup import safe_html
from jawanndenn.models import Ballot, Poll, Vote
from jawanndenn.serializers import PollConfigSerializer
from rapidjson import JSONDecodeError
from rest_framework.exceptions import ValidationError

_staticfile_finders = [import_string(cls_string)()
                       for cls_string in settings.STATICFILES_FINDERS]


def _except_poll_does_not_exist(wrappee):
    """Decorator that turns Poll.DoesNotExist into 404 Not Found"""
    @wraps(wrappee)
    def wrapper(*args, **kwargs):
        try:
            return wrappee(*args, **kwargs)
        except Poll.DoesNotExist:
            return HttpResponseNotFound('No such poll')

    return wrapper


def _except_validation_error(wrappee):
    """Decorator that turns ValidationError into 400 Bad Request"""
    @wraps(wrappee)
    def wrapper(request, *args, **kwargs):
        try:
            return wrappee(request, *args, **kwargs)
        except ValidationError as exception:
            return bad_request(request, exception)

    return wrapper


@require_GET
def index_get_view(request):
    return TemplateResponse(request,
                            template='html/setup.xhtml',
                            content_type='application/xhtml+xml')


@require_POST
@_except_validation_error
def poll_post_view(request):
    config_json = request.POST.get('config', '{}')
    try:
        config = json.loads(config_json)
    except JSONDecodeError:
        raise ValidationError('Poll configuration is not well-formed JSON.')

    serializer = PollConfigSerializer(data=config)
    serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        if Poll.objects.count() >= settings.JAWANNDENN_MAX_POLLS:
            return HttpResponseBadRequest(
                f'Maximum number of {settings.JAWANNDENN_MAX_POLLS} polls '
                'reached, please contact the administrator.')

        poll = serializer.save()

    return redirect(poll)


@require_GET
@_except_poll_does_not_exist
def poll_data_get_view(request, poll_id):
    with transaction.atomic():
        poll = Poll.objects.get(slug=poll_id)
        poll_config = {
            'equal_width': poll.equal_width,
            'title': poll.title,
            'options': list(poll.options.order_by('position')
                            .values_list('name', flat=True)),
        }
        votes = [
            [ballot.voter_name, [vote.yes for vote
                                 in ballot.votes.order_by('option__position')]]
            for ballot
            in poll.ballots.order_by('created', 'id')
        ]

    data = {
        'config': poll_config,
        'votes': votes,
    }

    return JsonResponse(data)


@require_GET
@_except_poll_does_not_exist
def poll_get_view(request, poll_id):
    Poll.objects.get(slug=poll_id)

    return TemplateResponse(request,
                            template='html/poll.xhtml',
                            content_type='application/xhtml+xml')


@require_POST
@_except_poll_does_not_exist
def vote_post_view(request, poll_id):
    with transaction.atomic():
        poll = Poll.objects.get(slug=poll_id)

        if poll.ballots.count() >= settings.JAWANNDENN_MAX_VOTES_PER_POLL:
            return HttpResponseBadRequest(
                f'Maximum number of {settings.JAWANNDENN_MAX_VOTES_PER_POLL} '
                'votes reached for this poll'
                ', please contact the administrator.')

        voter_name = safe_html(request.POST.get('voterName'))
        votes = [
            request.POST.get(f'option{i}', 'off') == 'on'
            for i
            in range(poll.options.count())
        ]

        ballot = Ballot.objects.create(poll=poll, voter_name=voter_name)
        for option, vote in zip(poll.options.order_by('position'), votes):
            Vote.objects.create(ballot=ballot, option=option, yes=vote)

    return redirect(poll)


@require_GET
def serve_using_finders(request, path, show_indexes=False):
    """
    Wrapper around django.views.static.serve that uses
    settings.STATICFILES_FINDERS rather than a single document_root
    """
    for finder in _staticfile_finders:
        fullpath = finder.find(path)
        if fullpath:
            document_root = fullpath[:-len(path)] if path else fullpath
            return serve(request, path, document_root=document_root,
                         show_indexes=show_indexes)
    else:
        raise Http404
