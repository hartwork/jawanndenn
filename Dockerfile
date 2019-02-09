FROM python:2.7-stretch

RUN useradd -m jawanndenn
USER jawanndenn

COPY --chown=jawanndenn:jawanndenn setup.py README.rst  /app/
COPY --chown=jawanndenn:jawanndenn jawanndenn/  /app/jawanndenn/

RUN cd /app && python setup.py install --user && cd / && rm -rf /app/*

EXPOSE 8080

ENTRYPOINT ["/home/jawanndenn/.local/bin/jawanndenn", "--port", "8080", "--host", "0.0.0.0"]
CMD ["--database-pickle", "/data/polls.pickle"]

STOPSIGNAL SIGINT
