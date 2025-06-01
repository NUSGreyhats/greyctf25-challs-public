# start by pulling the python image
FROM python:3.10-alpine

RUN apk update && apk add socat

RUN pip install pycryptodome

COPY ./uwusignatures.py /srv/app/run.py
RUN chmod 555 /srv/app/run.py

WORKDIR /srv/app

CMD [ "socat", "TCP-LISTEN:5399,nodelay,reuseaddr,fork", "EXEC:\"timeout -s KILL 10m python3.10 -u /srv/app/run.py\"" ]