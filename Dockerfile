FROM python:2.7-stretch

COPY setup.py README.rst  /app/
COPY jawanndenn/  /app/jawanndenn/

RUN cd /app && python setup.py install --user && cd / && rm -rf /app

EXPOSE 8080

ENTRYPOINT ["/root/.local/bin/jawanndenn", "--port", "8080", "--host", "0.0.0.0"]
CMD ["--database-pickle", "/data/polls.pickle"]
