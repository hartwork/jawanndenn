FROM python:2.7-wheezy

ADD . /app

RUN cd /app && python setup.py install --user && cd / && rm -rf /app

EXPOSE 8080

CMD ["/root/.local/bin/jawanndenn", "--port", "8080", "--host", "0.0.0.0", "--database-pickle", "/data/polls.pickle"]
