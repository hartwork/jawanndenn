# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.utils import timezone
from rest_framework.fields import BooleanField, CharField, ChoiceField, ListField
from rest_framework.serializers import Serializer

from jawanndenn.markup import safe_html
from jawanndenn.models import Poll, PollOption


class _PollLifetime:
    MONTH = "month"
    WEEK = "week"
    CHOICES = (MONTH, WEEK)

    @classmethod
    def to_relativedelta(cls, lifetime):
        return relativedelta(
            **(
                {
                    cls.MONTH: {"months": 1},
                    cls.WEEK: {"days": 7},
                }[lifetime]
            )
        )


class PollConfigSerializer(Serializer):
    equal_width = BooleanField(default=False)
    title = CharField()
    options = ListField(child=CharField(), allow_empty=False)
    lifetime = ChoiceField(choices=_PollLifetime.CHOICES, default=_PollLifetime.MONTH)

    def create(self, validated_data):
        poll_expires_at = timezone.now() + _PollLifetime.to_relativedelta(
            validated_data["lifetime"]
        )
        poll_equal_width = validated_data["equal_width"]
        poll_title = safe_html(validated_data["title"])
        poll_option_names = [
            safe_html(str(option_name)) for option_name in validated_data["options"]
        ]

        with transaction.atomic():
            poll = Poll.objects.create(
                title=poll_title, expires_at=poll_expires_at, equal_width=poll_equal_width
            )
            for i, option_name in enumerate(poll_option_names):
                PollOption.objects.create(poll=poll, position=i, name=option_name)

            return poll
