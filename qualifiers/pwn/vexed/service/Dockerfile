FROM python:3.12 AS app
RUN pip install --no-cache-dir capstone

FROM pwn.red/jail
COPY --from=app / /srv
COPY ./server.py /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_MEM=0
ENV JAIL_CPU=0
ENV JAIL_TIME=60
