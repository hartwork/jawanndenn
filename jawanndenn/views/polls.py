# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from functools import wraps

import rapidjson as json  # lgtm [py/import-and-import-from]
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.defaults import bad_request
from rapidjson import JSONDecodeError
from rest_framework.exceptions import ValidationError

from jawanndenn import DEFAULT_MAX_POLLS, DEFAULT_MAX_VOTES_PER_POLL
from jawanndenn.markup import safe_html
from jawanndenn.models import Ballot, Poll, Vote
from jawanndenn.serializers import PollConfigSerializer


def _except_poll_does_not_exist(wrappee):
    """Decorator that turns Poll.DoesNotExist into 404 Not Found"""

    @wraps(wrappee)
    def wrapper(*args, **kwargs):
        try:
            return wrappee(*args, **kwargs)
        except Poll.DoesNotExist:
            return HttpResponseNotFound("No such poll")

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
    return TemplateResponse(request, template="html/setup.htm")


@require_POST
@_except_validation_error
def poll_post_view(request):
    config_json = request.POST.get("config", "{}")
    try:
        config = json.loads(config_json)
    except JSONDecodeError:
        raise ValidationError("Poll configuration is not well-formed JSON.")

    serializer = PollConfigSerializer(data=config)
    serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        max_polls = getattr(settings, "JAWANNDENN_MAX_POLLS", DEFAULT_MAX_POLLS)
        if Poll.objects.count() >= max_polls:
            return HttpResponseBadRequest(
                f"Maximum number of {max_polls} polls reached, please contact the administrator."
            )

        poll = serializer.save()

    return redirect(poll)


@require_GET
@_except_poll_does_not_exist
def poll_data_get_view(request, poll_id):
    with transaction.atomic():
        poll = Poll.objects.get(slug=poll_id)
        poll_config = {
            "equal_width": poll.equal_width,
            "title": poll.title,
            "options": list(poll.options.order_by("position").values_list("name", flat=True)),
        }

        votes = []
        ballot = None
        ballot_votes = []

        for vote in (
            Vote.objects.filter(ballot__poll=poll)
            .select_related("ballot")
            .order_by("ballot__created", "ballot__id", "option__position")
        ):
            if vote.ballot != ballot:
                if ballot is not None:
                    votes.append([ballot.voter_name, ballot_votes])
                ballot = vote.ballot
                ballot_votes = []
            ballot_votes.append(vote.yes)

        if ballot is not None:
            votes.append([ballot.voter_name, ballot_votes])

    data = {
        "config": poll_config,
        "votes": votes,
    }

    return JsonResponse(data)


@require_GET
@_except_poll_does_not_exist
def poll_get_view(request, poll_id):
    Poll.objects.get(slug=poll_id)

    return TemplateResponse(request, template="html/poll.htm")


@require_POST
@_except_poll_does_not_exist
def vote_post_view(request, poll_id):
    with transaction.atomic():
        poll = Poll.objects.get(slug=poll_id)

        max_votes_per_poll = getattr(
            settings, "JAWANNDENN_MAX_VOTES_PER_POLL", DEFAULT_MAX_VOTES_PER_POLL
        )
        if poll.ballots.count() >= max_votes_per_poll:
            return HttpResponseBadRequest(
                f"Maximum number of {max_votes_per_poll} "
                "votes reached for this poll"
                ", please contact the administrator."
            )

        voter_name = safe_html(request.POST.get("voterName"))
        votes = [
            request.POST.get(f"option{i}", "off") == "on" for i in range(poll.options.count())
        ]

        ballot = Ballot.objects.create(poll=poll, voter_name=voter_name)
        for option, vote in zip(poll.options.order_by("position"), votes):
            Vote.objects.create(ballot=ballot, option=option, yes=vote)

    return redirect(poll)
