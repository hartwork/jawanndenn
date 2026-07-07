ARG PY_VER="3.14"
FROM python:${PY_VER}-alpine

# NOTE: Build-only dependencies are uninstalled again further down, so the two lists need to be kept in sync!
RUN echo '@edge-community https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories \
        && \
    apk add --update \
        diffutils \
        g++ \
        gcc \
        linux-headers \
        musl-dev \
        npm \
        postgresql17-dev \
        shadow \
        \
        bash \
        postgresql17-client \
        supercronic@edge-community

SHELL ["/bin/bash", "-c"]
RUN mkdir -p /var/mail  # to avoid warning "Creating mailbox file: No such file or directory"
RUN useradd --create-home --uid 1001 --non-unique jawanndenn
USER jawanndenn
ENV PATH=/home/jawanndenn/.local/bin/:${PATH}


COPY --chown=jawanndenn:jawanndenn requirements*.txt  /tmp/app/
RUN set -x \
        && \
    cd /tmp/app \
        && \
    pip3 install --user --ignore-installed --disable-pip-version-check pip setuptools wheel \
        && \
    hash pip3 \
        && \
    pip3 install --user --no-binary :all: --require-hashes -r requirements.txt \
        && \
    pip3 check \
        && \
    diff -u0 \
            <(sed -e '/--hash=/d' -e 's/ \\$//' -e '/^#/d' -e '/^$/d' -e 's,-,_,g' requirements-*.txt | sort -f) \
            <(pip3 freeze | sed -e '/^setuptools==/d' -e '/^wheel==/d' -e 's,-,_,g' | sort -f) \
        && \
    diff -u1 \
            <(grep == requirements-direct.txt | sed 's,==.*,,') \
            <(grep == requirements-direct.txt | sed 's,==.*,,' | sort -f) \
        && \
    diff -u1 \
            <(grep == requirements-indirect.txt | sed 's,==.*,,') \
            <(grep == requirements-indirect.txt | sed 's,==.*,,' | sort -f)

RUN mkdir -p /tmp/app/jawanndenn/
COPY --chown=jawanndenn:jawanndenn jawanndenn/frontend/ /tmp/app/jawanndenn/frontend/
RUN cd /tmp/app/jawanndenn/frontend/ \
        && \
    npm ci \
        && \
    npm run build \
        && \
    ls -lh ../index.html  # i.e. fail Docker build if missing

USER root
# NOTE: Build-only dependencies have been installed explicitely further up, so the two lists need to be kept in sync!
RUN apk del \
            diffutils \
            g++ \
            gcc \
            linux-headers \
            musl-dev \
            npm \
            postgresql17-dev \
            shadow \
        && \
    apk upgrade --update
USER jawanndenn

COPY --chown=jawanndenn:jawanndenn jawanndenn/                     /tmp/app/jawanndenn/
COPY --chown=jawanndenn:jawanndenn .coveragerc setup.py README.md  /tmp/app/
RUN cd /tmp/app \
        && \
    pip3 install --user . \
        && \
    cp -v .coveragerc ~/.local/lib/python*/site-packages/jawanndenn/ \
        && \
    rm -rf /tmp/app

COPY --chown=jawanndenn:jawanndenn crontab docker-entrypoint.sh  /home/jawanndenn/


EXPOSE 54080

ENTRYPOINT ["/home/jawanndenn/docker-entrypoint.sh"]
CMD []

STOPSIGNAL SIGINT
