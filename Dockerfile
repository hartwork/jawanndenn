FROM python:3.8-alpine

RUN apk update && apk add \
        bash \
        diffutils \
        g++ \
        gcc \
        musl-dev \
        postgresql-client \
        postgresql-dev \
        shadow

RUN mkdir -p /var/mail  # to avoid warning "Creating mailbox file: No such file or directory"
RUN useradd --create-home --uid 1001 --non-unique jawanndenn
USER jawanndenn
ENV PATH=/home/jawanndenn/.local/bin/:${PATH}


COPY --chown=jawanndenn:jawanndenn requirements.txt  /tmp/app/
RUN cd /tmp/app \
        && \
    pip3 install --user --ignore-installed --disable-pip-version-check pip setuptools wheel \
        && \
    hash pip3 \
        && \
    pip3 install --user -r requirements.txt \
        && \
    pip3 check \
        && \
    bash -c "diff -u0 <(pip freeze | sort -f) <(sed -e '/^#/d' -e '/^$/d' requirements.txt | sort -f)"

USER root
RUN apk update && apk upgrade
# Enable testing repository for nothing but package "supercronic".
# It's done down here so that we get as little as possible from testing.
RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
RUN apk update && apk add supercronic
USER jawanndenn

COPY --chown=jawanndenn:jawanndenn jawanndenn/          /tmp/app/jawanndenn/
COPY --chown=jawanndenn:jawanndenn setup.py README.rst  /tmp/app/
RUN cd /tmp/app \
        && \
    pip3 install --user . \
        && \
    rm -rf /tmp/app

COPY --chown=jawanndenn:jawanndenn crontab docker-entrypoint.sh  /home/jawanndenn/


EXPOSE 54080

ENTRYPOINT ["/home/jawanndenn/docker-entrypoint.sh"]
CMD []

STOPSIGNAL SIGINT
