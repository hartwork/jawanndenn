# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import json
from functools import wraps

from django.conf import settings
from django.db import transaction
from django.http import (HttpResponseBadRequest, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import redirect
from django.template.response import SimpleTemplateResponse
from django.views.decorators.http import require_GET, require_POST
from jawanndenn.markup import safe_html
from jawanndenn.models import Ballot, Poll, PollOption, Vote


def _except_poll_does_not_exist(wrappee):
    @wraps(wrappee)
    def wrapper(*args, **kwargs):
        try:
            return wrappee(*args, **kwargs)
        except Poll.DoesNotExist:
            return HttpResponseNotFound('No such poll')

    return wrapper


@require_GET
def index_get_view(request):
    context = {
        'url_prefix': settings.JAWANNDENN_URL_PREFIX,
    }

    response = SimpleTemplateResponse(template='html/setup.xhtml',
                                      context=context,
                                      content_type='application/xhtml+xml')
    response._request = request
    return response


@require_POST
def poll_post_view(request):
    config = json.loads(request.POST.get('config', '{}'))
    poll_equal_width = bool(config.get('equal_width', False))
    poll_title = safe_html(config.get('title', ''))
    poll_option_names = map(safe_html, config.get('options', []))

    with transaction.atomic():
        if Poll.objects.count() >= settings.JAWANNDENN_MAX_POLLS:
            return HttpResponseBadRequest(
                f'Maximum number of {settings.JAWANNDENN_MAX_POLLS} polls '
                'reached, please contact the administrator.')

        poll = Poll.objects.create(title=poll_title,
                                   equal_width=poll_equal_width)
        for i, option_name in enumerate(poll_option_names):
            PollOption.objects.create(poll=poll, position=i, name=option_name)

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
def poll_get_view(request, poll_id):
    context = {
        'url_prefix': settings.JAWANNDENN_URL_PREFIX,
    }

    response = SimpleTemplateResponse(template='html/poll.xhtml',
                                      context=context,
                                      content_type='application/xhtml+xml')
    response._request = request
    return response


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
