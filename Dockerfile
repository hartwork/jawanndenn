FROM python:3.7-alpine

RUN apk update && apk add bash diffutils gcc musl-dev postgresql-dev postgresql-client

COPY setup.py README.rst requirements.txt  /app/
COPY jawanndenn/  /app/jawanndenn/
COPY docker-entrypoint.sh  /root/

RUN cd /app \
        && \
    pip3 install --user --no-warn-script-location -r requirements.txt \
        && \
    pip3 check \
        && \
    bash -c "diff -u0 <(pip freeze | sort -f) <(sed -e '/^#/d' -e '/^$/d' requirements.txt | sort -f)" \
        && \
    pip3 install --user --no-warn-script-location . \
        && \
    cd / \
        && \
    rm -rf /app

ENV PATH=/root/.local/bin/:${PATH}

EXPOSE 8080

ENTRYPOINT ["/root/docker-entrypoint.sh"]
CMD []

STOPSIGNAL SIGINT
