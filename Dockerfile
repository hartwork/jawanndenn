FROM python:3.7-alpine

RUN apk update && apk add bash diffutils

COPY setup.py README.rst requirements.txt  /app/
COPY jawanndenn/  /app/jawanndenn/

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

ENTRYPOINT ["/root/.local/bin/jawanndenn", "--port", "8080", "--host", "0.0.0.0"]
CMD ["--database-sqlite3", "/data/polls.sqlite3", \
     "--django-secret-key-file", "/data/django_secret_key"]

STOPSIGNAL SIGINT
