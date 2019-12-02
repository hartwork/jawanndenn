#!/usr/bin/env bash
# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

set -e
set -u

PS4='# '
set -x


if [[ $# -gt 0 ]]; then
    exec "$@"
fi

manage_py() {
    DJANGO_SETTINGS_MODULE=jawanndenn.settings python3 -m django "$@"
}

wait_for_database_args=(
    --stable 0
    --wait-when-down 1
    --wait-when-alive 1
)
manage_py wait_for_database "${wait_for_database_args[@]}"

manage_py migrate

gunicorn_args=(
    --name=jawanndenn
    --bind=0.0.0.0:54080
    --workers="$(nproc --ignore=1)"
    --access-logfile=-
    --logger-class=gunicorn_color.Logger
    jawanndenn.wsgi
)
exec gunicorn "${gunicorn_args[@]}"
