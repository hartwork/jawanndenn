FROM python:2.7-stretch

# first add the normal user 'jawanndenn' to run the app
# use id 1001 since this is compatible with openshift
RUN useradd --create-home --uid 1001 --non-unique jawanndenn

# switch to the user
USER jawanndenn
# from now on we are running with normal user privileges

# put the temp files to /tmp/app so we can remove them completely after installing
# /tmp is open to everyone
COPY --chown=jawanndenn:jawanndenn setup.py README.rst  /tmp/app/
COPY --chown=jawanndenn:jawanndenn jawanndenn/  /tmp/app/jawanndenn/

RUN cd /tmp/app && python setup.py install --user && cd / && rm -rf /tmp/app/

EXPOSE 8080

ENTRYPOINT ["/home/jawanndenn/.local/bin/jawanndenn", "--port", "8080", "--host", "0.0.0.0"]
CMD ["--database-pickle", "/data/polls.pickle"]

STOPSIGNAL SIGINT
