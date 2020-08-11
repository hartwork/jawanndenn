#!/usr/bin/env bash
# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

set -e
set -u

PS4='# '
set -x

id
ip addr

cd ~/.local/lib/python*/site-packages/jawanndenn

manage_py() {
    python3 -m django "$@"
}

wait_for_it_args=(
    --service "${JAWANNDENN_REDIS_HOST}:${JAWANNDENN_REDIS_PORT}"
    --service "${JAWANNDENN_POSTGRES_HOST}:${JAWANNDENN_POSTGRES_PORT}"
    --parallel
)
wait-for-it "${wait_for_it_args[@]}"

if [[ $# -gt 0 ]]; then
    case "$1" in
    test)
        manage_py "$@"
        exit 0
        ;;
    *)
        exec "$@"
        ;;
    esac
fi

manage_py migrate

gunicorn_args=(
    --name=jawanndenn
    --bind=0.0.0.0:54080
    --workers="$(nproc --ignore=1)"
    --timeout 5
    --access-logfile=-
    --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
    --logger-class=gunicorn_color.Logger
    jawanndenn.wsgi
)
exec gunicorn "${gunicorn_args[@]}"
