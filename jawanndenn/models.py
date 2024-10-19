# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import hashlib
import os

from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel


def _get_random_sha256():
    return hashlib.sha256(os.urandom(256 // 8)).hexdigest()


class PollQuerySet(models.QuerySet):
    def expired(self):
        return self.filter(expires_at__lt=now())


class Poll(TimeStampedModel):
    slug = models.CharField(max_length=64, default=_get_random_sha256, unique=True)
    title = models.CharField(max_length=255)
    equal_width = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True)

    objects = PollQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse("poll-detail", args=[self.slug])


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    position = models.PositiveSmallIntegerField()  # starting at 0
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("poll", "position")


class Ballot(TimeStampedModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="ballots")
    voter_name = models.CharField(max_length=255)


class Vote(models.Model):
    ballot = models.ForeignKey(Ballot, related_name="votes", on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    yes = models.BooleanField()

    class Meta:
        unique_together = ("ballot", "option")
