# Copyright (C) 2020 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from django.core.management import BaseCommand

from ...models import Poll


class Command(BaseCommand):
    help = "Deletes expired polls"

    def handle(self, *args, **options):
        polls_deleted, _ = Poll.objects.expired().delete()
        self.stdout.write(self.style.SUCCESS(f"{polls_deleted} poll(s) deleted"))
