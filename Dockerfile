FROM python:3.8-alpine

RUN apk update && apk add bash diffutils gcc musl-dev postgresql-dev postgresql-client shadow

RUN mkdir /var/mail  # to avoid warning "Creating mailbox file: No such file or directory"
RUN useradd --create-home --uid 1001 --non-unique jawanndenn
USER jawanndenn


COPY --chown=jawanndenn:jawanndenn requirements.txt  /tmp/app/
RUN cd /tmp/app \
        && \
    pip3 install --user --no-warn-script-location -r requirements.txt \
        && \
    pip3 check \
        && \
    bash -c "diff -u0 <(pip freeze | sort -f) <(sed -e '/^#/d' -e '/^$/d' requirements.txt | sort -f)"

COPY --chown=jawanndenn:jawanndenn jawanndenn/          /tmp/app/jawanndenn/
COPY --chown=jawanndenn:jawanndenn setup.py README.rst  /tmp/app/
RUN cd /tmp/app \
        && \
    pip3 install --user --no-warn-script-location . \
        && \
    rm -rf /tmp/app

COPY --chown=jawanndenn:jawanndenn docker-entrypoint.sh  /home/jawanndenn/


ENV PATH=/home/jawanndenn/.local/bin/:${PATH}

EXPOSE 54080

ENTRYPOINT ["/home/jawanndenn/docker-entrypoint.sh"]
CMD []

STOPSIGNAL SIGINT
