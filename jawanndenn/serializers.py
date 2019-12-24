# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from django.db import transaction
from jawanndenn.markup import safe_html
from jawanndenn.models import Poll, PollOption
from rest_framework.fields import BooleanField, CharField, ListField
from rest_framework.serializers import Serializer


class PollConfigSerializer(Serializer):
    equal_width = BooleanField(default=False)
    title = CharField()
    options = ListField(child=CharField(), allow_empty=False)

    def create(self, validated_data):
        poll_equal_width = validated_data['equal_width']
        poll_title = safe_html(validated_data['title'])
        poll_option_names = [safe_html(str(option_name))
                             for option_name
                             in validated_data['options']]

        with transaction.atomic():
            poll = Poll.objects.create(title=poll_title,
                                       equal_width=poll_equal_width)
            for i, option_name in enumerate(poll_option_names):
                PollOption.objects.create(poll=poll, position=i,
                                          name=option_name)

            return poll
