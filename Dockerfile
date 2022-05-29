FROM python:3.10-alpine

RUN echo '@edge-community https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories \
        && \
    apk add --update \
        bash \
        diffutils \
        g++ \
        gcc \
        musl-dev \
        postgresql-client \
        postgresql-dev \
        shadow \
        supercronic@edge-community

SHELL ["/bin/bash", "-c"]
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
    pip3 install --user --require-hashes -r requirements.txt \
        && \
    pip3 check \
        && \
    diff -u0 <(pip freeze | sort -f) <(sed -e '/--hash=/d' -e 's/ \\$//' -e '/^#/d' -e '/^$/d' requirements.txt | sort -f)

USER root
RUN apk upgrade --update
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
