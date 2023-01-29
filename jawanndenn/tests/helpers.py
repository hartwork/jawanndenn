# Copyright (C) 2023 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

# These are to allow annotated use of .assertNumQueries
SAVEPOINT = 1
RELEASE_SAVEPOINT = 1


def SELECT(comment):
    return 1
