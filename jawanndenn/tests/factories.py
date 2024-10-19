# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from jawanndenn.models import Ballot, Poll, PollOption, Vote


class PollFactory(DjangoModelFactory):
    class Meta:
        model = Poll

    title = Sequence(lambda n: f"Title {n}")


class PollOptionFactory(DjangoModelFactory):
    class Meta:
        model = PollOption

    poll = SubFactory(PollFactory)
    position = Sequence(int)
    name = Sequence(lambda n: f"Option {n}")


class BallotFactory(DjangoModelFactory):
    class Meta:
        model = Ballot

    poll = SubFactory(PollFactory)
    voter_name = Sequence(lambda n: f"User {n}")


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    option = SubFactory(PollOptionFactory)
