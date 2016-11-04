# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import os
import sys

import bottle

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from jawanndenn import app
app  # mark as used

application = bottle.default_app()
