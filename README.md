[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![image](https://github.com/hartwork/jawanndenn/workflows/Build%20and%20test%20using%20Docker/badge.svg)](https://github.com/hartwork/jawanndenn/actions)


# What is jawanndenn?

![jawanndenn setup](https://raw.githubusercontent.com/hartwork/jawanndenn/master/jawanndenn-setup.png)

*jawanndenn* is a simple web application to schedule meetings and run
polls, a libre alternative to Doodle.
It is using the following technology:

- **Python**
  - [Docker Compose](https://docs.docker.com/compose/)
  - [Django](https://www.djangoproject.com/)
    - [Django Extensions](https://github.com/django-extensions/django-extensions)
    - [Django Ratelimit](https://github.com/jsocol/django-ratelimit) +
      [msgpack-python](https://github.com/msgpack/msgpack-python)
    - [django-redis](https://github.com/niwinz/django-redis)
    - [Django REST framework](https://www.django-rest-framework.org/)
    - [Factory Boy](https://factoryboy.readthedocs.io/en/latest/)
  - [Gunicorn](https://gunicorn.org/) +
    [gunicorn-color-logger](https://github.com/swistakm/gunicorn-color-logger)
  - [parameterized](https://github.com/wolever/parameterized)
  - [pre-commit](https://pre-commit.com/)
  - [python-rapidjson](https://github.com/python-rapidjson/python-rapidjson)
  - [sentry-python](https://github.com/getsentry/sentry-python)
  - [wait-for-it](https://github.com/clarketm/wait-for-it)

- **JavaScript / CSS / Fonts**
  - [Google Webfonts
    Helper](https://google-webfonts-helper.herokuapp.com/)
  - [jQuery](http://jquery.com/)
  - [jQuery noty](http://ned.im/noty/#/about)
  - [Materialize](http://materializecss.com/)
  - [Roboto](https://fonts.google.com/specimen/Roboto)

- **Storage**
  - [PostgreSQL](https://www.postgresql.org/)
  - [Redis](https://redis.io/)
  - [SQLite](https://www.sqlite.org/index.html)

- **Scheduling**
  - [Supercronic](https://github.com/aptible/supercronic)

*jawanndenn* is [libre software](https://www.gnu.org/philosophy/free-sw.en.html)
developed by [Sebastian Pipping](https://blog.hartwork.org/).
The server code is licensed under the
[GNU Affero GPL license](https://www.gnu.org/licenses/agpl.en.html) version 3 or later
whereas the client code is licensed under the [GNU GPL license](https://www.gnu.org/licenses/gpl.html) version 3 or later.

Please [report bugs](https://github.com/hartwork/jawanndenn/issues) and
let me know if you [like](mailto:sebastian@pipping.org) it.


# Poll Setup Format

The textarea titled "Setup (JSON)" uses a simple
[JSON](https://www.json.org/)-based format that knows the following
keys:

- `equal_width` — a bool to control whether all options are pumped up to
  the same width (`true` or `false`) to counter potential voter bias
- `lifetime` — duration after which this poll will be deleted; can be
  `"week"` or `"month"`; an enum-like string
- `options` — a list of strings, one for each option; supports
  [Markdown](https://commonmark.org/help/)-like syntax for: bold,
  italic, inline code
- `title` — the title or headline of the poll to run; supports
  [Markdown](https://commonmark.org/help/)-like syntax for: bold,
  italic, inline code


# Installation

To install the latest release without cloning the Git repository:

```console
# pip3 install jawanndenn --user
```

To install from a Git clone:

```console
# ./setup.py install --user
```


# Deployment with docker-compose

Create a simple file `.env` like this one:

```
JAWANNDENN_POSTGRES_NAME=jawanndenn
JAWANNDENN_POSTGRES_USER=jawanndenn
JAWANNDENN_POSTGRES_PASSWORD=dEb2PIcinemA8poH
JAWANNDENN_SECRET_KEY=606ea88f183a27919d5c27ec7f948906d23fdd7821684eb59e8bcf7377e3853b
```

Make sure to **adjust these values** after copy and paste!

You can then build and run a docker image using
`docker-compose up --build`.

The app is served on `localhost:54080`. PostgreSQL data is saved to
`~/.jawanndenn-docker-pgdata/` on the host system. There is also an
instance of Redis used for cross-process rate limiting, and a "cron"
housekeeping container that will go delete polls that have exceeded
their configured lifetime, every 60 minutes.

(If you need a low-maintenance SSL reverse proxy in front of jawanndenn,
[docker-ssl-reverse-proxy](https://github.com/hartwork/docker-ssl-reverse-proxy)
could be of interest.)

There is a few more environment variables that you could want to adjust
in your environment. Altogether, there are these variables:


## Environment variables

| Variable                        | Function                                                                                                                                                                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `DJANGO_SETTINGS_MODULE`        | Django settings module to use, leave as is, defaults to `jawanndenn.settings` (see `docker-compose.yml`)                                                                                                                                                                       |
| `JAWANNDENN_ALLOWED_HOSTS`      | Hostnames to serve jawanndenn at, list separated by comma, is set to `jawanndenn.de,www.jawanndenn.de` on the main production server, defaults to `127.0.0.1,0.0.0.0,localhost` (see `jawanndenn/settings.py`)                                                                 |
| `JAWANNDENN_DEBUG`              | Debug mode, disabled for all values but `True`, disabled by default, should never be enabled in production for security (see `jawanndenn/settings.py`)                                                                                                                         |
| `JAWANNDENN_MAX_POLLS`          | Maximum total number of polls to store, denial of service protection, defaults to `1000` (see `jawanndenn/settings.py` and `docker-compose.yml`)                                                                                                                               |
| `JAWANNDENN_MAX_VOTES_PER_POLL` | Maximum total number of polls to store, denial of service protection, defaults to `40` (see `jawanndenn/settings.py`)                                                                                                                                                          |
| `JAWANNDENN_POSTGRES_HOST`      | Hostname of the PostgreSQL database to connect to; defaults to `postgres` (see `docker-compose.yml`)                                                                                                                                                                           |
| `JAWANNDENN_POSTGRES_NAME`      | Database name of the PostgreSQL database to connect to; no default, always required                                                                                                                                                                                            |
| `JAWANNDENN_POSTGRES_PASSWORD`  | Password for log-in with the PostgreSQL database; no default, always required                                                                                                                                                                                                  |
| `JAWANNDENN_POSTGRES_PORT`      | Port of the PostgreSQL database to connect to; defaults to `5432` (see `docker-compose.yml`)                                                                                                                                                                                   |
| `JAWANNDENN_POSTGRES_USER`      | Username for log-in with the PostgreSQL database; no default, always required                                                                                                                                                                                                  |
| `JAWANNDENN_REDIS_HOST`         | Hostname of the Redis database to connect to; defaults to `redis` (see `docker-compose.yml`)                                                                                                                                                                                   |
| `JAWANNDENN_REDIS_PORT`         | Port of the Redis database to connect to; defaults to `6379` (see `docker-compose.yml`)                                                                                                                                                                                        |
| `JAWANNDENN_SECRET_KEY`         | [Django secret key](https://docs.djangoproject.com/en/4.0/ref/settings/#secret-key); should be long, generated, not used elsewhere; no default, always required                                                                                                                |
| `JAWANNDENN_SENTRY_DSN`         | [Data source name (DSN)](https://docs.sentry.io/product/sentry-basics/dsn-explainer/) for use with [Sentry](https://sentry.io/), disabled/empty by default (see `jawanndenn/settings.py`)                                                                                      |
| `JAWANNDENN_URL_PREFIX`         | Prefix string to insert into URLs rather after the domain name to help with hosting multiple apps under the same domain side by side; e.g. prefix `prefix123` will result in URLs like `https://<domain>/prefix123/poll/<id>`; empty by default (see `jawanndenn/settings.py`) |


## Doing backups with Docker Compose

A simple way to create and apply backups of Django's view on the
PostgreSQL poll data is the following.

Let's assume you add a `docker-compose.override.yml` like this:

```yaml
services:
  jawanndenn:
    volumes:
     - ~/.jawanndenn-docker-backups/:/home/jawanndenn/backups/:rw
```

Now [Django management command `dumpdata`](https://docs.djangoproject.com/en/dev/ref/django-admin/#dumpdata) can be used to backup the poll data to a JSON file like this:

```console
# docker compose run jawanndenn python3 -m django dumpdata -v3 --format json -o "/home/jawanndenn/backups/data-$(date -I).json"
```

To reset the database to the state of a backup, [Django management `loaddata`](https://docs.djangoproject.com/en/dev/ref/django-admin/#loaddata) would do the job:

```console
# docker compose run jawanndenn python3 -m django loaddata -v3 /home/jawanndenn/backups/data-2025-05-23.json
```


# Command line usage

When installed, invocation is as simple as

```console
# jawanndenn
```

During development, you may want to run *jawanndenn* from the Git clone
using

```console
# PYTHONPATH=. python3 -m jawanndenn --debug
```

Currently supported arguments are:

```console
# COLUMNS=80 jawanndenn --help
usage: jawanndenn [-h] [--version] [--debug] [--host HOST] [--port PORT]
                  [--url-prefix PATH] [--database-sqlite3 FILE]
                  [--django-secret-key-file FILE] [--max-polls COUNT]
                  [--max-votes-per-poll COUNT] [--dumpdata]
                  [--loaddata FILE.json]

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --debug               Enable debug mode (default: disabled)
  --host HOST           Hostname or IP address to listen at (default:
                        127.0.0.1)
  --port PORT           Port to listen at (default: 8080)
  --url-prefix PATH     Path to prepend to URLs (default: "")
  --database-sqlite3 FILE
                        File to write the database to (default:
                        ~/jawanndenn.sqlite3)
  --django-secret-key-file FILE
                        File to use for Django secret key data (default:
                        ~/jawanndenn.secret_key)

limit configuration:
  --max-polls COUNT     Maximum number of polls total (default: 1000)
  --max-votes-per-poll COUNT
                        Maximum number of votes per poll (default: 40)

data import/export arguments:
  --dumpdata            Dump a JSON export of the database to standard output,
                        then quit.
  --loaddata FILE.json  Load a JSON export of the database from FILE.json,
                        then quit.
```


# Migrating data from jawanndenn 1.x to 2.x

Migration takes four steps:

1.  Update to the latest version of jawanndenn 1.x, e.g. by running:
    `pip2 install --upgrade 'jawanndenn<2'`; the JSON data export was
    first introduced with release 1.6.3.

2.  Export existing polls:
    1.  If you're using the commend line app:
        `python2 -m jawanndenn --dumpdata > dump.json`
    2.  If you're using docker-compose:
        `docker-compose run -T jawanndenn --database-pickle /data/polls.pickle --dumpdata > dump.json`

3.  Deploy latest jawanndenn 2.x somewhere (as described above) or just
    `pip3 install 'jawanndenn>=2'` it somewhere

4.  Import the JSON dump created in step (2):

    1.  If you're using the commend line app:
        `python3 -m jawanndenn --loaddata dump.json`

    2.  If you're using docker-compose:
        `docker-compose run -T jawanndenn sh -c 'cat > /tmp/dump.json && DJANGO_SETTINGS_MODULE=jawanndenn.settings python3 -m django loaddata /tmp/dump.json' < dump.json`


# Goals

- Libre software to host yourself, unlike Doodle
- More simplistic, sexy and/or fun than
  [libre alternatives](http://alternativeto.net/software/doodle/?license=opensource),
  in alphabetic order:
  - [Bitpoll](https://github.com/fsinfuhh/Bitpoll)
    (ex. [Dudel](https://github.com/opatut/dudel))
  - [Crab Fit](https://github.com/GRA0007/crab.fit)
  - [Croodle](https://github.com/jelhan/croodle)
  - [Dudle](https://dudle.inf.tu-dresden.de/)
  - ([Drupal Date picker formatter](http://alternativeto.net/software/date-picker-formatter-dudel-for-drupal/?license=opensource))
  - ([Foodle](https://foodl.org/) (discontinued; [on
    GitHub](https://github.com/UNINETT/Foodle), ex. [DFN
    scheduler](https://terminplaner.dfn.de/), ex. [DFN
    Terminplaner+](https://terminplaner2.dfn.de/)))
  - [Framadata](https://framadate.org/)
    ([Sources](https://git.framasoft.org/framasoft/framadate), ex.
    [OpenSondage](https://github.com/leblanc-simon/OpenSondage), ex.
    [STUdS](http://studs.unistra.fr/))
  - [Nextcloud Polls](https://github.com/nextcloud/polls)
  - [Noodle](https://github.com/kmerz/noodle)
  - [Nuages](https://nuages.domainepublic.net/)
  - [Pleft](https://github.com/sander/pleft)
  - [Rallly](https://github.com/lukevella/Rallly)
  - [RDVz](https://sourceforge.net/projects/rdvz/)
  - [sowhenthen](https://github.com/kiyutink/sowhenthen)
  - [VoteOn.Date](https://gitlab.com/Glitchy-Tozier/voteon.date)
- Keep things simple, usable, maintainable
- Support invocation from the command line, e.g. for spontaneous polls
  in a LAN
- Have security in mind

Please check out the
[list of upcoming features](https://github.com/hartwork/jawanndenn/issues/created_by/hartwork).


# Non-goals

- Use of heavy frontend frameworks: building blocks only
- Read availability from calendars


# Thanks

Special thanks to Arne Maier ([@KordonDev](https://github.com/KordonDev))
for reporting an XSS vulnerability, responsibly.
