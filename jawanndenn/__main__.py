# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import argparse
import logging
import os
import signal
import string
import subprocess
import sys
from unittest.mock import patch

from jawanndenn import DEFAULT_MAX_POLLS, DEFAULT_MAX_VOTES_PER_POLL
from jawanndenn.metadata import VERSION_STR

_log = logging.getLogger(__name__)


def _require_hash_randomization():
    if not sys.flags.hash_randomization:
        _log.info("Hash randomization found to be disabled.")
        if os.environ.get("PYTHONHASHSEED") == "random":
            _log.error("Unexpected re-execution loop detected, shutting down.")
            sys.exit(1)

        _log.info("Re-executing with hash randomization enabled...")
        env = os.environ.copy()
        env["PYTHONHASHSEED"] = "random"
        argv = [sys.executable] + sys.argv
        os.execve(argv[0], argv, env)


def _generate_random_printable_django_secret_key():
    alphabet = "".join(
        b for b in string.printable if b not in string.whitespace and b not in "'\\"
    )
    # reduce number of retries while not introducing modulo bias
    alphabet = "".join(alphabet for _ in range(256 // len(alphabet)))
    chars = []
    while len(chars) < 50:
        index = ord(os.urandom(1))
        if index >= len(alphabet):  # detect and avoid modulo bias
            continue
        chars.append(alphabet[index])
    return "".join(chars)


def _process_django_secret_key_file(filename):
    secret_key_encoding = "utf-8"
    try:
        with open(filename, encoding=secret_key_encoding) as f:
            secret_key = f.read()
    except FileNotFoundError:
        secret_key = _generate_random_printable_django_secret_key()
        with open(filename, "w", encoding=secret_key_encoding) as f:
            f.write(secret_key)
    return secret_key


def _inner_main():
    parser = argparse.ArgumentParser(prog="jawanndenn")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION_STR}")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode (default: disabled)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        metavar="HOST",
        help="Hostname or IP address to listen at (default: %(default)s)",
    )
    parser.add_argument(
        "--port",
        default=8080,
        type=int,
        metavar="PORT",
        help="Port to listen at (default: %(default)s)",
    )
    parser.add_argument(
        "--url-prefix",
        default="",
        metavar="PATH",
        help='Path to prepend to URLs (default: "%(default)s")',
    )
    parser.add_argument(
        "--database-sqlite3",
        default="~/jawanndenn.sqlite3",
        metavar="FILE",
        help="File to write the database to (default: %(default)s)",
    )
    parser.add_argument(
        "--django-secret-key-file",
        default="~/jawanndenn.secret_key",
        metavar="FILE",
        help="File to use for Django secret key data (default: %(default)s)",
    )

    limits = parser.add_argument_group("limit configuration")
    limits.add_argument(
        "--max-polls",
        type=int,
        metavar="COUNT",
        default=DEFAULT_MAX_POLLS,
        help="Maximum number of polls total (default: %(default)s)",
    )
    limits.add_argument(
        "--max-votes-per-poll",
        type=int,
        metavar="COUNT",
        default=DEFAULT_MAX_VOTES_PER_POLL,
        help="Maximum number of votes per poll (default: %(default)s)",
    )

    export_args = parser.add_argument_group("data import/export arguments")
    export_args.add_argument(
        "--dumpdata",
        action="store_true",
        help="Dump a JSON export of the database to standard output, then quit.",
    )
    export_args.add_argument(
        "--loaddata",
        metavar="FILE.json",
        help="Load a JSON export of the database from FILE.json, then quit.",
    )

    options = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if options.debug else logging.INFO)

    if not options.dumpdata and not options.loaddata:
        _require_hash_randomization()

    secret_key = _process_django_secret_key_file(
        os.path.expanduser(options.django_secret_key_file)
    )

    # NOTE: These are read by the the Django settings module
    os.environ["JAWANNDENN_ALLOWED_HOSTS"] = ",".join(
        [options.host, "127.0.0.1", "0.0.0.0", "localhost"]
    )
    os.environ["JAWANNDENN_DEBUG"] = str(options.debug)
    os.environ["JAWANNDENN_MAX_POLLS"] = str(options.max_polls)
    os.environ["JAWANNDENN_MAX_VOTES_PER_POLL"] = str(options.max_votes_per_poll)
    os.environ["JAWANNDENN_SECRET_KEY"] = secret_key
    os.environ["JAWANNDENN_SQLITE_FILE"] = os.path.expanduser(options.database_sqlite3)
    os.environ["JAWANNDENN_URL_PREFIX"] = options.url_prefix

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jawanndenn.settings")

    # Heavy imports are down here to keep --help fast
    from django.core.management import execute_from_command_line

    with patch("sys.stdout", sys.stderr):
        execute_from_command_line(["./manage.py", "migrate"])
        print()

    if options.dumpdata:
        execute_from_command_line(["./manage.py", "dumpdata"])
    elif options.loaddata:
        print("Importing JSON dump -- this may take a few seconds...", file=sys.stderr)
        execute_from_command_line(["./manage.py", "loaddata", os.path.abspath(options.loaddata)])
    else:
        sys.exit(
            subprocess.call(
                [
                    "gunicorn",
                    "--name=jawanndenn",
                    f"--bind={options.host}:{options.port}",
                    "--workers=1",  # due to use of sqlite3 storage
                    "--access-logfile=-",
                    "--logger-class=gunicorn_color.Logger",
                    "jawanndenn.wsgi",
                ]
            )
        )


def main():
    try:
        _inner_main()
    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)


if __name__ == "__main__":
    main()
