FROM python:3.12-alpine AS python

FROM pwn.red/jail
COPY --from=python / /srv
COPY server.py /srv/app/run
COPY Creds.py /srv/app/Creds.py
COPY SecurePickle.py /srv/app/SecurePickle.py
RUN chmod +x /srv/app/run

ENV JAIL_MEM=0
ENV JAIL_CPU=0
ENV JAIL_TIME=3600