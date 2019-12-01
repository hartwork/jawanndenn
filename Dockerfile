FROM python:3.7-alpine

COPY setup.py README.rst  /app/
COPY jawanndenn/  /app/jawanndenn/

RUN cd /app && python setup.py install --user && cd / && rm -rf /app

ENV PATH=/root/.local/bin/:${PATH}

EXPOSE 8080

ENTRYPOINT ["/root/.local/bin/jawanndenn", "--port", "8080", "--host", "0.0.0.0"]
CMD ["--database-sqlite3", "/data/polls.sqlite3", \
     "--django-secret-key-file", "/data/django_secret_key"]

STOPSIGNAL SIGINT
