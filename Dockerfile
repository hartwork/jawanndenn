FROM python:2.7-alpine

ADD . /app

WORKDIR /app

RUN python setup.py install --user

EXPOSE 8080

WORKDIR /

CMD ["/root/.local/bin/jawanndenn", "--port", "8080", "--host", "0.0.0.0", "--filepath", "/data/polls.pickle"]
